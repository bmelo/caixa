from django.template import Library

register = Library()

def media_root():
    """
    Returns the string contained in the setting MEDIA_ROOT.
    """
    try:
        from django.conf import settings
    except ImportError:
        return ''
    return settings.MEDIA_ROOT
media_root = register.simple_tag(media_root)
