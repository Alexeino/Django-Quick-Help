# PostgreSQL Integration with Django Quick code

# Database should be created by postgresql already before migrations

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'django_react_auth',
       'USER': 'postgres',
       'PASSWORD': 'android@321',
       'HOST': 'localhost',
       'PORT': '5432',
   }
}

