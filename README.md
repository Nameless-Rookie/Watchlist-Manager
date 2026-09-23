# Watchlist Manager

Watchlist Manager is a beginner-friendly Django website for keeping a personal list of movies and TV shows. Each person creates an account and gets a private watchlist. They can add titles, update them, write notes, give ratings, and find titles using search, filters, and sorting.

The project deliberately uses normal Django templates, HTML, CSS, JavaScript, and SQLite. It does not use a frontend framework, external API, AI, or a custom user model.

## Features

- Register, log in, and log out using Django's built-in authentication system.
- Add, view, edit, and delete watchlist items.
- Choose Movie or TV Show, a genre, release year, and viewing status.
- Mark an item as Want to Watch, Watching, or Watched.
- Add a personal rating from 0 to 10 after marking an item as Watched.
- Save a short personal review or note.
- Search titles and notes; filter by type, genre, and status; sort by newest, title, or rating.
- See dashboard counts and the average of all entered ratings.
- Use the Django admin site to manage data.
- Keep each user's items private, even if someone changes an item ID in the address bar.

## Technologies used

- Python 3
- Django
- SQLite (Django's default local database)
- HTML templates
- CSS and a few lines of JavaScript for the small-screen navigation menu

## Project structure

```text
watchlist_manager/
├── manage.py                     # Django command-line entry point
├── requirements.txt              # Python dependency list
├── db.sqlite3                    # SQLite database (created after migration)
├── watchlist_manager/            # Project configuration
│   ├── settings.py
│   └── urls.py
├── watchlist/                    # Main application
│   ├── admin.py                  # Admin configuration
│   ├── forms.py                  # Registration and watch-item forms
│   ├── models.py                 # WatchItem database model
│   ├── urls.py                   # Application URL routes
│   ├── views.py                  # Page logic
│   ├── migrations/               # Database migration files
│   └── templates/watchlist/      # App page templates
├── templates/
│   ├── base.html                 # Shared navigation, messages, footer
│   └── registration/             # Login and registration templates
└── static/watchlist/style.css    # Site styling
```

## Set up and run the project

Open a terminal in the folder containing `manage.py` and use these commands.

### 1. Create and activate a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install Django

```bash
python -m pip install -r requirements.txt
```

### 3. Create the database tables

```bash
python manage.py migrate
```

### 4. Create an admin account (optional but recommended)

```bash
python manage.py createsuperuser
```

Choose a username, email if desired, and password. The admin website will be at `http://127.0.0.1:8000/admin/` after the server starts.

### 5. Start the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser. Stop the server with `Ctrl+C`.

## How to use the application

1. From the home page, choose **Create free account** and register.
2. Select **Add item** and enter a movie or TV show. Title, type, genre, and release year are required.
3. Use **My Watchlist** to search, filter, sort, view, edit, or delete your titles.
4. Select **Dashboard** to see totals for each status, average rating, and recent titles.
5. To rate a title, first choose the **Watched** status and then enter a number from 0 to 10.
6. To use the admin site, log in at `/admin/` with the superuser account created above.

## Important Django files explained

| File | Purpose |
| --- | --- |
| `manage.py` | Runs Django commands such as `runserver`, `migrate`, and `createsuperuser`. |
| `watchlist_manager/settings.py` | Stores project settings, installed apps, template folder, static files, SQLite database, and login redirects. |
| `watchlist_manager/urls.py` | Sends the root URL to the `watchlist` app and makes `/admin/` available. |
| `watchlist/models.py` | Defines the `WatchItem` table and its fields. |
| `watchlist/forms.py` | Defines the registration form and validates add/edit data. |
| `watchlist/views.py` | Fetches data, performs dashboard calculations, and renders templates. |
| `watchlist/urls.py` | Connects readable paths such as `/watchlist/add/` to views. |
| `watchlist/admin.py` | Makes WatchItem easier to view and filter in Django admin. |
| `templates/` | Contains the HTML pages shown to users. |
| `static/watchlist/style.css` | Contains the dark, responsive visual design. |

## Database model

The application has one custom model: `WatchItem`.

| Field | Meaning |
| --- | --- |
| `user` | A link to Django's built-in User table. This makes every item belong to one person. |
| `title` | Movie or TV show name. |
| `item_type` | Choice of Movie or TV Show. |
| `genre` | Selected category such as Drama, Comedy, or Sci-Fi. |
| `status` | Want to Watch, Watching, or Watched. |
| `rating` | Optional decimal score from 0 to 10. |
| `review` | Optional short personal note. |
| `release_year` | Year the title was released. |
| `created_at` | Date and time Django automatically added the record. |

The database prevents the same user from adding the same title, type, and release year twice. Different users can still save the same title because their lists are separate.

## Main URLs and views

| URL | View purpose |
| --- | --- |
| `/` | Shows the landing page. |
| `/register/` | Creates a Django User account and logs the new user in. |
| `/login/` | Uses Django's built-in login view. |
| `/logout/` | Safely logs out with a POST form. |
| `/dashboard/` | Calculates and displays personal summary counts. |
| `/watchlist/` | Lists the current user's items with search, filters, and sorting. |
| `/watchlist/add/` | Creates a new item for the current user. |
| `/watchlist/<id>/` | Shows one item belonging to the current user. |
| `/watchlist/<id>/edit/` | Updates one owned item. |
| `/watchlist/<id>/delete/` | Shows confirmation and deletes one owned item. |

## Security and validation notes

- Pages that show or change watchlist data use `@login_required`, so visitors are redirected to the login page.
- Detail, edit, and delete views fetch an item using both its ID and `user=request.user`. This returns a 404 page if a different user tries to guess an ID.
- Django's CSRF token protects all forms that change data.
- Django's `UserCreationForm` checks the username and password rules.
- The watch-item form checks the rating range, reasonable release year, status/rating combination, and simple duplicates.

## Useful development commands

```bash
# Check the project for Django configuration errors
python manage.py check

# Run the automated tests
python manage.py test

# Make a new migration after changing models.py
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

## Assumptions

- The rating is personal and optional. A rating can be entered only after setting the status to Watched.
- Genres are a short fixed list to keep the form simple and easy to filter during a beginner project.
- This is configured for local development. Before putting it online, set `DEBUG = False`, use a secret environment variable for `SECRET_KEY`, and configure allowed hosts.
