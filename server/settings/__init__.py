import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()

app_stage = env("DJANGO_APP_STAGE")

if app_stage == 'prod':
    
    from .production import *
else:
    from .development import *