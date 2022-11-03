from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage

DEFAULT_STORAGE_LOCATION = getattr(settings, "DEFAULT_STORAGE_LOCATION", None)
if DEFAULT_STORAGE_LOCATION == None:
    raise ImproperlyConfigured("DEFAULT_STORAGE_LOCATION is not in settings.py")

class ProtectedMedia(FileSystemStorage):
    location = DEFAULT_STORAGE_LOCATION