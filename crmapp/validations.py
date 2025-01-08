from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_custom_url(value):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if not re.match(regex, value) and not re.match(r'^[A-Z0-9.-]+\.[A-Z]{2,6}$', value, re.IGNORECASE):
        raise ValidationError(
            _('Enter a valid URL.'),
            params={'value': value},
        )

