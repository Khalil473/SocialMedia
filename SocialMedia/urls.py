from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("user_auth.urls")),
    path("profiles/", include("user_profile.urls")),
    path("content/", include("content.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
