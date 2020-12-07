from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from mdb import SearchMovie, MovieDetails
import os

app = Flask(__name__) 
db_uri = 'sqlite:///movies.db'
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
Bootstrap(app)
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), nullable = False, unique = True)
    year = db.Column(db.Integer, nullable = False)
    description = db.Column(db.Text, nullable = False)
    rating = db.Column(db.Float, nullable = False)

    ranking = db.Column(db.Integer)
    review = db.Column(db.String(250))
    img_url = db.Column(db.String(250), nullable = False)

class Edit(FlaskForm):
    rating = StringField('Your Rating, Out Of 10, e.g 7.5', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    # rank = StringField('Your Rank', validators= [DataRequired()])
    submit = SubmitField('Done')

    def validate_rating(self, rating):
        try:
            float(rating.data)
        
        except ValueError:
            raise ValidationError('Enter a valid rating number')

class Add(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Search')


@app.route("/")
def home():
    movies = Movie.query.order_by(Movie.rating).all()

    for i in range(len(movies)):
        movies[i].ranking = len(movies) - i 
    db.session.commit()
    return render_template("index.html", movies = movies)

@app.route("/add", methods=['GET', 'POST'])
def add():
    form = Add()
    if form.validate_on_submit():
        search_term = form.title.data

        return redirect(url_for('select', name = search_term))

    return render_template('add.html', form = form)

@app.route("/edit", methods=['GET', 'POST'])
def edit():
    id = request.args.get('movieID')
    if id == None:
       return redirect(url_for('home')) 
    else: 
        movie = Movie.query.get(id)
        form = Edit()

        if form.validate_on_submit():
            movie.rating = form.rating.data
            movie.review = form.review.data
            # movie.ranking = form.rank.data
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('edit.html', movie = movie, form = form)

@app.route('/delete')
def delete():
    id = request.args.get('id')
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/select')
def select():
    name = request.args.get('name')
    results = SearchMovie(name)
    results.search()

    return render_template('select.html', results = results.results_list)

@app.route('/data')
def data():
    id = request.args.get('id')
    if id == None:
       return redirect(url_for('home')) 
    else:     
        movie = MovieDetails(int(id)).result

        newMovie = Movie(title = movie['title'], year = movie['year'], description = movie['sum'],
                        rating = 0, ranking = 0, review = 'none', img_url = movie['img_url'])

        db.session.add(newMovie)
        db.session.commit()

        return redirect(url_for('edit', movieID = newMovie.id))


