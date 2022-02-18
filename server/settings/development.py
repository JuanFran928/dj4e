from .base import *

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

print('desarrollo')

DATABASES = { #aqui se puede cambiar a postgresql, con usuario y contraseña
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}