DATABASES = {
    'default': {
        #        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'emif_dev', # Or path to database file if using sqlite3.
        'USER': 'emif_dev', # Not used with sqlite3.
        'PASSWORD': 'emif_dev', # Not used with sqlite3.
        'HOST': 'localhost', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
        'AUTOCOMMIT': True,
        'autocommit': True,
        'OPTIONS': {
            'autocommit': True,
        },
    },
}

