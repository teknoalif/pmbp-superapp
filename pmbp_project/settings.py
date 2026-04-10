import os
from pathlib import Path
# import dj_database_url # Import untuk handle database cloud

# 1. PATH DASAR
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. SECURITY (Kunci Rahasia)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-4gdkv1*s%_%g83$k*l6n$1*w=msb!8t58rzyyavg*r*6&h82j$')

# 3. MODE DEBUG
# Biarkan True saat testing lokal agar eror terlihat jelas
DEBUG = False

# 4. HOST YANG DIIZINKAN
ALLOWED_HOSTS = [
    'laporan-pmbp.kakalif.my.id',
    'pmbp-superapp.vercel.app',
    '.vercel.app',
    'localhost',
    '127.0.0.1'
]

# 5. APLIKASI YANG TERINSTAL
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core', # Aplikasi utama PMBP
]

# 6. MIDDLEWARE (Jembatan Proses)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Menangani CSS/JS di Vercel
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pmbp_project.urls'

# 7. PENGATURAN TEMPLATE (HTML)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pmbp_project.wsgi.application'

# 8. PENGATURAN DATABASE (Lokal vs Cloud)
# Jika di Vercel/Produksi, gunakan Supabase. Jika lokal, gunakan SQLite agar cepat.
if os.getenv('DATABASE_URL'):
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
else:
    # Pakai database lokal Kakak saat testing
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
    }

# 9. VALIDASI PASSWORD
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 10. LOKALISASI (Waktu Indonesia)
LANGUAGE_CODE = 'id-id'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True

# 11. FILE STATIS (CSS, JS, LOGO)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Penyimpanan statis untuk Vercel
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 12. MEDIA FILES (FOTO DOKUMENTASI)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 13. REDIRECT LOGIN/LOGOUT
LOGIN_REDIRECT_URL = 'dashboard_admin'
LOGOUT_REDIRECT_URL = 'input_laporan'

# Pengaturan Redirect Login
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard_admin'
LOGOUT_REDIRECT_URL = 'login'

