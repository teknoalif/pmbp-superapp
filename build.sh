# Install dependencies
pip install -r requirements.txt

# Jalankan migrasi database
python manage.py migrate --noinput

# Kumpulkan file statis (CSS/JS)
python manage.py collectstatic --noinput
