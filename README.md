
# MovieApp

A Django-based web application for browsing and discovering movies, with user authentication and integration with the TMDb API.

## Features
- User registration and login
- Browse latest movies
- Movie information from TMDb
- Responsive UI with static files (CSS, JS, images)

## Requirements
- Python 3.8+
- Django 3.2+
- Gunicorn
- WhiteNoise
- dj-database-url
- psycopg2-binary
- requests
- tmdbv3api
- Pillow

## Local Development

1. **Clone the repository:**
   ```
   git clone <your-repo-url>
   cd MovieApp-main
   ```
2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
3. **Apply migrations:**
   ```
   python manage.py migrate
   ```
4. **Create a superuser (optional):**
   ```
   python manage.py createsuperuser
   ```
5. **Run the development server:**
   ```
   python manage.py runserver
   ```
6. **Access the app:**
   Open your browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Deployment on Render

1. **Push your code to GitHub.**
2. **Set up environment variables on Render:**
   - `DJANGO_SECRET_KEY`
   - `DEBUG` (set to `False`)
   - `DATABASE_URL` (for production database)
3. **Procfile:**
   ```
   web: gunicorn First.wsgi
   ```
4. **Static Files:**
   - Ensure `STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')` in `First/settings.py`.
   - Add `'whitenoise.middleware.WhiteNoiseMiddleware',` to `MIDDLEWARE`.
   - Run `python manage.py collectstatic` and commit the `staticfiles/` directory.
5. **On Render:**
   - New Web Service → Connect your repo
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn First.wsgi`
   - Demo: https://movieapp-main.onrender.com/
## License

This project is licensed under the MIT License.
