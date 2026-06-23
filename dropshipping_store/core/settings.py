import os
from pathlib import Path
import environ
import dj_database_url

# Projenin kök dizinini belirleme (Bu kısım eksikti)
BASE_DIR = Path(__file__).resolve().parent.parent

# Çevresel değişkenleri (.env) yükleme
env = environ.Env()
# .env dosyasının yolunu açıkça belirtmek olası okuma hatalarını önler
environ.Env.read_env(os.path.join(BASE_DIR, '.env')) 

# --- GÜVENLİK VE TEMEL AYARLAR ---
SECRET_KEY = env('SECRET_KEY', default='django-insecure-local-key-12345')
DEBUG = env.bool('DEBUG', default=True)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

# --- UYGULAMALAR ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Kendi uygulamalarımız
    'shop.apps.ShopConfig',
]

# --- VERİTABANI ---
# Bulut PostgreSQL (Neon.tech / Supabase vb.) veya yerel SQLite bağlantısı
DATABASES = {
    'default': dj_database_url.config(
        # BASE_DIR kullanımı pathlib'e (modern Django standardına) uygun olarak güncellendi
        default=env('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
    )
}

# --- SEPET AYARLARI ---
CART_SESSION_ID = 'cart'

# --- SHOPIER API BİLGİLERİ ---
SHOPIER_API_KEY = env('SHOPIER_API_KEY', default='magaza_api_anahtariniz')
SHOPIER_API_SECRET = env('SHOPIER_API_SECRET', default='magaza_api_sirriniz')