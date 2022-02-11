from django.urls import path
import os
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.static import serve
from . import views

urlpatterns = [
    #path('', TemplateView.as_view(template_name='home/main.html')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Add
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # Keep
    path('', include('ads.urls')),                   # Add,
    path('home/', include('home.urls')),                   # Add,

    #register
    url(r'^accounts/register/$', views.RegisterView.register , name="register")

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

# Switch to social login if it is configured - Keep for later. Para el login con github
try:
    from . import github_settings
    social_login = 'registration/login_social.html'
    urlpatterns.insert(0,
        path('accounts/login/', auth_views.LoginView.as_view(template_name=social_login))
    )
    print('Using',social_login,'as the login template')
except:
    print('Using registration/login.html as the login template')
