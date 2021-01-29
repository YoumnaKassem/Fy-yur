Venue-Artist Booking App
-----

## Introduction

Venue-Artist Booking App is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

# Overview

Artists and musical venues can use this app to find each other.
This app let user:
* create new venues, artists, and create new shows.
* search for venues and artists.
* learn more about a specific artist or venue.

## Tech Stack

### 1. Backend Dependencies:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be ORM library of choice
 * **PostgreSQL**  as a database server
 * **Python3** and **Flask** as a server language and a server framework
 * **Flask-Migrate** for creating and running schema migrations
You can download and install the dependencies mentioned above using `pip` as:
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```

### 2. Frontend Dependencies
HTML, CSS, and Javascript with Bootstrap 3
```
node -v
npm -v
```
Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:
```
npm init -y
npm install bootstrap@3
```


## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependences
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in the `MODELS` section of `app.py`.
* Controllers are also located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`



