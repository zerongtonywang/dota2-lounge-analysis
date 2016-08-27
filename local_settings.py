SECRET_KEY = 'c^i)1=av5m!y567=7vu-1i_pnr-58(uz+9j%zkq-9t1o306weq'
DEBUG = True
DEV = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd2lbetting',
        'USER': 'd2lbettinguser',
        'PASSWORD': 'd2lbettingpassword',
        'HOST': 'localhost',
        'PORT': '',
    }
}
