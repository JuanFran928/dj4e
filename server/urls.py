from django.urls import path
import os
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ads.urls')),                   # Add,
    path('home/', include('home.urls')),                   # Add,
    path('auth/', include('authentication.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

# Serve the static HTML
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urlpatterns += [
    url(r'^site/(?P<path>.*)$', serve,
        {'document_root': os.path.join(BASE_DIR, 'site'),
           'show_indexes': True},
        name='site_path'
    ),
]

# Coge el favicon
urlpatterns += [
    path('favicon.ico', serve, {
            'path': 'favicon.ico',
            'document_root': os.path.join(BASE_DIR, 'home/static'),
        }
    ),
]


