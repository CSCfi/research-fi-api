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
import re
from common import utils

class ApmProxyView(ProxyView):
    """
    Proxies POST request to Application Performance Monitoring.
    Adds HTTP basic authentication header.
    All other HTTP requests are blocked and responded with status code 405 Method Not Allowed.
    """
    # The URL of the Application Performance Monitoring api.
    upstream = settings.HA_PROXY_HOST + '/apm'

    # The Content-Type that will be added to the response in case the upstream server doesn’t send it
    default_content_type = 'application/json'

    # The max number of attempts for a request.
    retries = None

    def get_request_headers(self):
        """
        Add HTTP basic authentication header to request.
        """
        # Call super to get default headers
        headers = super(ApmProxyView, self).get_request_headers()
        # Add HTTP basic authentication header
        basic_authentication_header_value = utils.get_basic_authentication_header_value(settings.HTTP_AUTH_USERNAME, settings.HTTP_AUTH_PASSWORD)
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

        allowed_methods = ("POST")

        # Reject disallowed requst methods
        if request.method not in allowed_methods:
            return HttpResponseNotAllowed(allowed_methods)

        # Forward request to Application Performance Monitoring
        try:
            return super(ApmProxyView, self).dispatch(request, *args, **kwargs)
        except Exception as e:
            print('Error: Cannot connect to Application Performance Monitoring at ' + upstream)
            print(e)
            return HttpResponse(status=HTTPStatus.BAD_GATEWAY.value)
