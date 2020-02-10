# This file is part of the research.fi API service
#
# Copyright 2019 Ministry of Education and Culture, Finland
#
# :author: CSC - IT Center for Science Ltd., Espoo Finland servicedesk@csc.fi
# :license: MIT
from django.http import HttpResponseNotAllowed, HttpResponse
from django.conf import settings
from http import HTTPStatus
from revproxy.views import ProxyView
from .utils import get_basic_authentication_header_value
import re

class ElasticsearchProxyView(ProxyView):
    """
    Proxies GET request to Elasticsearch.
    Proxies POST request to Elasticsearch when the POST request URL contains "_search".
    Adds HTTP basic authentication header.
    All other HTTP requests are blocked and responded with status code 405 Method Not Allowed.
    """
    # The URL of the proxied server.
    upstream = settings.ELASTICSEARCH_HOST

    # The Content-Type that will be added to the response in case the upstream server doesn’t send it
    default_content_type = 'application/json'

    # The max number of attempts for a request.
    retries = None

    def get_request_headers(self):
        """
        Add HTTP basic authentication header to request.
        """
        # Call super to get default headers
        headers = super(ElasticsearchProxyView, self).get_request_headers()
        # Add HTTP basic authentication header
        basic_authentication_header_value = get_basic_authentication_header_value(settings.ELASTICSEARCH_HA_PROXY_USERNAME, settings.ELASTICSEARCH_HA_PROXY_PASSWORD)
        if basic_authentication_header_value is not None:
            headers['Authorization'] = basic_authentication_header_value
        return headers

    def dispatch(self, request, *args, **kwargs):
        """
        Extend ProxyView dispatch method.
        Check HTTP request methods.
        Return HTTP status 405 when request is not allowed.
        Return HTTP status 502 Bad Gateway in case connection to Elasticsearch fails.
        """

        allowed_methods = ("GET", "POST")

        # Debug print end user source IP address from headers field 'X-Forwarded-For'. It is set by the load balancer. 
        if 'X-Forwarded-For' in request.headers:
            print(request.headers['X-Forwarded-For'])

        # Reject disallowed requst methods
        if request.method not in allowed_methods:
            return HttpResponseNotAllowed(allowed_methods)

        # Reject POST unless request URL contains "_search" in certain place in url
        # Request URL is expected to be of form: /portalapi/<comma separated list of index names>/_search
        if request.method == "POST":
            if not re.search(r'.*\/portalapi\/[,a-zA-Z0-9]*(\/)?_search', request.path):
                return HttpResponseNotAllowed(allowed_methods)

        # Forward request to Elasticsearch
        try:
            return super(ElasticsearchProxyView, self).dispatch(request, *args, **kwargs)
        except Exception as e:
            print('Error: Cannot connect to Elasticsearch at ' + settings.ELASTICSEARCH_HOST)
            print(e)
            return HttpResponse(status=HTTPStatus.BAD_GATEWAY.value)

    # The URL of the proxied server.
    upstream = settings.ELASTICSEARCH_HOST
