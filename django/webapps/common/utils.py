from django.conf import settings
import base64

# Get value for HTTP basic authentication header
def get_basic_authentication_header_value(username=None, password=None):
    if username is not None and password is not None:
        credentials_string = username + ':' + password
        return 'Basic ' + base64.b64encode(credentials_string.encode()).decode('ascii')
    else:
        return None