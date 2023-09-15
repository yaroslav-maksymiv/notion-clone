from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.social.urls')),

    path('api/users/', include('users.urls')),
    path('api/', include('base.urls')),

    re_path(r"^$", TemplateView.as_view(template_name='index.html')),
    re_path(r"^(?:.*)/?$", TemplateView.as_view(template_name='index.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
