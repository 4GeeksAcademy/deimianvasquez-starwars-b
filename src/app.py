"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import requests
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, People, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# get all people
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    people = list(map(lambda item: item.serialize(), people))
    return jsonify(people), 200

# get one people
@app.route('/people/<int:theid>', methods=['GET'])
def get_one_people(theid=None):
    people = People.query.get(theid)
    if people is None:
        raise APIException('User not found', status_code=404)
    people = people.serialize()
    return jsonify(people), 200


# get all planets
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets = list(map(lambda item: item.serialize(), planets))
    return jsonify(planets), 200

# get one planet
@app.route('/planets/<int:theid>', methods=['GET'])
def get_one_planet(theid=None):
    planets = Planets.query.get(theid)
    if planets is None:
        raise APIException('User not found', status_code=404)
    planets = planets.serialize()
    return jsonify(planets), 200


# get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda item: item.serialize(), users))
    return jsonify(users), 200


#get all favorites from one user
@app.route('/users/favorites/<int:theid>', methods=['GET'])
def get_user_favorites(theid=None):
    # user = User.query.get(theid)
    # if user is None:
    #     return jsonify({"message":"not found"}), 404

    # fav = Favorite.query.filter_by(user_id=theid).all()
    user = User.query.filter_by(id=theid).first()



    return jsonify(user.serialize()), 200


# add favorite to user
@app.route('/favorites/people/<int:theid>', methods=['POST'])
def add_people_favorite(theid=None):
    request_body = request.get_json()
    user = User.query.get(request_body["user_id"])
    if user is None:
        raise APIException('User not found', status_code=404)
    people = People.query.get(theid)
    if people is None:
        raise APIException('People not found', status_code=404)
    favorite = Favorite()
    favorite.user_id = request_body["user_id"]
    favorite.people_id = theid
    db.session.add(favorite)
    db.session.commit()
    return jsonify("ok"), 200


# add favorite to user
@app.route('/favorites/planets/<int:theid>', methods=['POST'])
def add_planets_favorite(theid=None):
    request_body = request.get_json()
    user = User.query.get(request_body["user_id"])
    if user is None:
        raise APIException('User not found', status_code=404)
    planets = Planets.query.get(theid)
    if planets is None:
        raise APIException('Planets not found', status_code=404)
    favorite = Favorite()
    favorite.user_id = request_body["user_id"]
    favorite.planet_id = theid
    db.session.add(favorite)
    db.session.commit()
    return jsonify("ok"), 200


# population people
@app.route('/people/population', methods=['GET'])
def get_people_population():
    # consulto la api de swapi people
    response = requests.get("https://www.swapi.tech/api/people?page=1&limit=300")
    response = response.json()
    response = response.get("results")

    for item in response:
        result = requests.get(item.get("url"))
        result = result.json()
        result = result.get("result")
        people = People()
        people.name = result.get("properties").get("name")
        people.height = result.get("properties").get("height")
        people.mass = result.get("properties").get("mass")
        people.hair_color = result.get("properties").get("hair_color")
        people.skin_color = result.get("properties").get("skin_color")
        people.eye_color = result.get("properties").get("eye_color")
        people.birth_year = result.get("properties").get("birth_year")
        people.gender = result.get("properties").get("gender")
        
        try:
            db.session.add(people)
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()
            return jsonify("error"), 500
    return jsonify("ok"), 200


@app.route('/planets/population', methods=['GET'])
def get_planets_population():
    # consulto la api de swapi people
    response = requests.get("https://www.swapi.tech/api/planets?page=1&limit=300")
    response = response.json()
    response = response.get("results")

    for item in response:
        result = requests.get(item.get("url"))
        result = result.json()
        result = result.get("result")
        people = Planets()
        people.name = result.get("properties").get("name")
        people.diameter = result.get("properties").get("diameter")
        people.rotation_period = result.get("properties").get("rotation_period")
        people.orbital_period = result.get("properties").get("orbital_period")
        people.gravity = result.get("properties").get("gravity")
        people.population = result.get("properties").get("population")
        people.climate = result.get("properties").get("climate")
        people.terrain = result.get("properties").get("terrain")
        people.surface_water = result.get("properties").get("surface_water")
        
        try:
            db.session.add(people)
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()
            return jsonify("error"), 500
    return jsonify("ok"), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)