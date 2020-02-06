# This file is part of the research.fi API service
#
# Copyright 2019 Ministry of Education and Culture, Finland
#
# :author: CSC - IT Center for Science Ltd., Espoo Finland servicedesk@csc.fi
# :license: MIT
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<path>.*)$',
        views.ElasticsearchProxyView.as_view(), name='elasticsearch-proxy-view'),
]
