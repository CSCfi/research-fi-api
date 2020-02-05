from django.conf import settings
import base64

# Get value for HTTP basic authentication header
def get_basic_authentication_header_value():
    if settings.ELASTICSEARCH_HA_PROXY_USERNAME is not None and settings.ELASTICSEARCH_HA_PROXY_PASSWORD is not None:
        credentials_string = settings.ELASTICSEARCH_HA_PROXY_USERNAME + ':' + settings.ELASTICSEARCH_HA_PROXY_PASSWORD
        return 'Basic ' + base64.b64encode(credentials_string.encode()).decode('ascii')
    else:
        return None