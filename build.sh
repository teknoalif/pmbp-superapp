# Install library yang dibutuhkan
pip install -r requirements.txt

# Jalankan migrasi database ke Supabase secara otomatis
python manage.py migrate --noinput

# Kumpulkan file CSS dan JS agar tampilan rapi
python manage.py collectstatic --noinput
