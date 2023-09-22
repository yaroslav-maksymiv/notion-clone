DJOSER = {
    'LOGIN_FIELD': 'email',
    'SOCIAL_AUTH_TOKEN_STRATEGY': 'djoser.social.token.jwt.TokenStrategy',
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': [
        'http://localhost:3000',
        'http://localhost:8000',
        'http://127.0.0.1:3000',
        'http://127.0.0.1:8000',
    ],
    'SERIALIZERS': {},
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'notion-clone',
        'USER': 'postgres',
        'PASSWORD': 'qwert',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

INTERNAL_IPS = [
    "127.0.0.1",
]

ALLOWED_HOSTS = [
    "*"
]

CORS_ALLOW_ALL_ORIGINS = True