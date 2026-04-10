# Install dependencies
pip install -r requirements.txt

# Collect static files
python3.9 manage.py collectstatic --noinput

# Migrasi Database
python3.9 manage.py migrate
