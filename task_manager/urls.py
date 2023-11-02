
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


# Implement Django views and URL patterns
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/",include('Accounts.urls')),
    path("",include('tasks.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
