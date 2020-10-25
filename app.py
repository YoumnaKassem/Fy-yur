#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Done: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.TEXT())
    shows = db.relationship('Show', backref='venue', lazy=True)
    # Done: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.TEXT())
    shows = db.relationship('Show', backref='artist', lazy=True)

class Show(db.Model):
  __tablename__= 'shows'

  id = db.Column(db.Integer(), primary_key=True)
  start_time = db.Column(db.String())
  venue_id = db.Column(db.Integer(), db.ForeignKey('venues.id'))
  artist_id = db.Column(db.Integer(), db.ForeignKey('artists.id'))

  # Done: implement any missing fields, as a database migration using Flask-Migrate
# Done Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')
#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # Done: replace with real venues data.
  allvenues=Venue.query.all()
  allresults=[]
  for venue in allvenues:
    cityname=venue.city
    venues_in_this_city=Venue.query.filter(Venue.city==cityname).all()
    venues = [every_venue for every_venue in venues_in_this_city]
    for every_venue in venues_in_this_city:
      result = {
      'city': every_venue.city,
      'state': every_venue.state,
      'venues': venues
      }
    allresults.append(result)
  # Remove all duplicated objects from allresults
  data = [every_venue for n, every_venue in enumerate(
    allresults) if every_venue not in allresults[n + 1:]]
  return render_template('pages/venues.html', areas=data)

# --------------------------------------------------------------------

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term=request.form.get('search_term')
  # Done: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  venues_meet_search_term=Venue.query.filter(Venue.name.contains(search_term)).all()
  responsedata=[]
  count=0

  for venue in venues_meet_search_term:
    # upcoming_shows = Show.query.filter_by(venue_id=venue.id).filter(
    # Show.start_time > datetime.utcnow().isoformat()).all()
    responsedata.append({
    'id':venue.id,
    'name':venue.name
    # 'upcoming_shows': upcoming_shows
    })
    count+=1
  response={
  "count":count,
  "data":responsedata
  }

  return render_template('pages/search_venues.html', results=response, search_term=search_term)

# -----------------------------------------------------------------------
# shows the venue page with the given venue_id

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # Done: replace with real venue data from the venues table, using venue_id
  venue=Venue.query.filter_by(id=venue_id).first()
  shows=Show.query.filter_by(venue_id=venue.id).all()
  past_shows=[]
  upcoming_shows=[]
  for show in shows:
    past_shows_row= Show.query.filter(show.start_time < datetime.utcnow().isoformat()).all()
    for pastshow in past_shows_row:
      artist_name= Artist.query.filter_by(id=pastshow.artist_id).first().name
      image_link= Artist.query.filter_by(id=pastshow.artist_id).first().image_link
      past_shows.append({
      "artist_id":pastshow.artist_id,
      "artist_name":artist_name,
      "artist_image_link":image_link,
      "start_time":pastshow.start_time
      })
    upcoming_shows_row= Show.query.filter(show.start_time > datetime.utcnow().isoformat()).all()
    for upcomingshow in upcoming_shows_row:
      artist_name= Artist.query.filter_by(id=upcomingshow.artist_id).first().name
      image_link= Artist.query.filter_by(id=upcomingshow.artist_id).first().image_link
      upcoming_shows.append({
      "artist_id":upcomingshow.artist_id,
      "artist_name":artist_name,
      "artist_image_link":image_link,
      "start_time":upcomingshow.start_time
      })
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
    }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm()
  try:
    new_venue = Venue(name=request.form.get('name'),
      city=request.form.get('city'),
      state=request.form.get('state'),
      address=request.form.get('address'),
      phone=request.form.get('phone'),
      genres=request.form.get('genres'),
      # seeking_description=request.form.get('seeking_description'),
      # image_link=request.form.get('image_link'),
      facebook_link=request.form.get('facebook_link')
      # website=request.form.get('website'),  
      )
    db.session.add(new_venue)
    db.session.commit()
    flash('Venue ' + request.form.get('name') + ' was successfully listed!')
  except:
    flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
  # Done: insert form data as a new Venue record in the db, instead
  # Done: modify data to be the data object returned from db insertion
  # on successful db insert, flash success
  # Done: on unsuccessful db insert, flash an error instead.
  return render_template('pages/home.html')

# -----------------------------------------------------------------------------

# delete venue
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.filter_by(id=venue_id).first()
    name = venue.name
    db.session.delete(venue)
    db.session.commit()
    flash('Venue, ' + name + 'deleted.')
  except:
    flash('Venue, ' + name + 'could not be deleted')
  # Done: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  show all artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=Artist.query.all()
  return render_template('pages/artists.html', artists=data)

# ---------------------------------------------------------------

# search for artist
@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term=request.form.get('search_term')
  # Done: implement search on artists with partial string search. Ensure it is case-insensitive.
  artists=Artist.query.filter(Artist.name.contains(search_term)).all()
  data=[]
  count=0
  for artist in artists:
    # num_upcoming_shows= Show.query.filter_by(artist_id=artist.id).filter(Show.start_time>datatime.utcnow().isoformat()).all
    count+=1
    data.append({
      "id":artist.id,
      "name":artist.name,
      # "num_upcoming_shows":num_upcoming_shows
      })
  response={
    "count": count,
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

# -----------------------------------------------------------------------------

# show artist given its id
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist=Artist.query.filter_by(id=artist_id).first()
  # shows the Artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  pastshows=[]
  upcomingshows=[]
  shows=Show.query.filter_by(artist_id=artist.id)
  for show in shows:
    past_shows_row= Show.query.filter(show.start_time < datetime.utcnow().isoformat()).all()
    for past_show in past_shows_row:
      venue_name= Venue.query.filter_by(id=past_show.venue_id).first().name
      venue_image_link= Venue.query.filter_by(id=past_show.venue_id).first().image_link
      pastshows.append({
      "venue_id":past_show.venue_id,
      "venue_name":venue_name,
      "venue_image_link":venue_image_link,
      "start_time":past_show.start_time
      })
    upcoming_shows_row= Show.query.filter(show.start_time > datetime.utcnow().isoformat()).all()
    for upcoming_show in upcoming_shows_row:
      venue_name= Venue.query.filter_by(id=upcoming_show.venue_id).first().name
      venue_image_link= Venue.query.filter_by(id=upcoming_show.venue_id).first().image_link
      upcomingshows.append({
      "venue_id":upcoming_show.venue_id,
      "venue_name":venue_name,
      "venue_image_link":venue_image_link,
      "start_time":upcoming_show.start_time
      })
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows":pastshows,
    "upcoming_shows": upcomingshows,
    "past_shows_count":len(pastshows),
    "upcoming_shows_count":len(upcomingshows)
    }
  return render_template('pages/show_artist.html', artist=data)

#  Update Artist
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter_by(id=artist_id).first()
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  # Done: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter_by(id=artist_id).first()
  if artist:
    try:
      artist.name = form.name.data,
      artist.city = form.city.data,
      artist.state = form.state.data,
      artist.phone = form.phone.data,
      artist.genres = form.genres.data
      # adding & commiting the updated artist record to the database
      db.session.add(artist)
      db.session.commit()
    except:
      flash('this Artist ' + request.form.get('name') + ' not able to be updated.')
  # Done: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  return redirect(url_for('show_artist', artist_id=artist_id))

# -----------------------------------------------------------------
# Update Venue

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter_by(id=venue_id).first()
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.seeking_description.data = venue.seeking_description
  form.genres.data = venue.genres
  # Done: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm()
  venue = Venue.query.filter_by(id=venue_id).first()
  if venue:
    try:
      venue.name = form.name.data,
      venue.city = form.city.data,
      venue.state = form.state.data,
      venue.address = form.address.data,
      venue.phone = form.phone.data,
      venue.seeking_description = form.seeking_description.data,
      venue.image_link = form.image_link.data,
      venue.genres = form.genres.data
      # adding & commiting the updated record into the database
      db.session.add(venue)
      db.session.commit()
    except:
      flash('This Venue ' + request.form.get('name') + ' not able to be updated.')
  # Done: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm()
  try:
    new_artist = Artist(name=request.form.get('name'),
      city=request.form.get('city'),
      state=request.form.get('state'),
      genres=request.form.get('genres'),
      # address=request.form.get('address'),
      phone=request.form.get('phone'),
      # image_link=request.form.get('image_link'),
      facebook_link=request.form.get('facebook_link')
      # website=request.form.get('website'),    
      )
    db.session.add(new_artist)
    db.session.commit()
    flash('Artist ' + request.form.get('name') + ' was successfully listed!')
  except:
    flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')
  # called upon submitting the new artist listing form
  # Done: insert form data as a new Artist record in the db, instead
  # Done: modify data to be the data object returned from db insertion
  # on successful db insert, flash success
  # Done: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data=[]
  shows=Show.query.all()
  for show in shows:
    show_in_detail={
    "venue_id":show.venue_id,
    "venue_name":Venue.query.filter_by(id=show.venue_id).first().name,
    "artist_id":show.artist_id,
    "artist_name":Artist.query.filter_by(id=show.artist_id).first().name,
    "artist_image_link":Artist.query.filter_by(id=show.artist_id).first().image_link,
    "start_time":show.start_time
    }
    data.append(show_in_detail)
  # Done: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  return render_template('pages/shows.html', shows=data)

# ---------------------------------------------------------------------------

# create new show
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm()
  try:
    show=Show(venue_id=request.form.get('venue_id'),
      artist_id=request.form.get('artist_id'),
      start_time=request.form.get('start_time')
      )
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    flash('An error occurred. Show could not be listed.')
  # called to create new shows in the db, upon submitting new show listing form
  # Done: insert form data as a new Show record in the db, instead
  # on successful db insert, flash success
  # Done: on unsuccessful db insert, flash an error instead. 
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
