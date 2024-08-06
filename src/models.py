from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    favorite = db.relationship('Favorite', backref='user', uselist=True)

    def __repr__(self):
        # return '<User %r>' % self.name
        return f"<User {self.name}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created": self.created,
            "favorites": list(map(lambda item: item.serialize(), self.favorite))
        }


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    height = db.Column(db.String(120), nullable=False)
    mass = db.Column(db.String(120), nullable=False)
    hair_color = db.Column(db.String(120), nullable=False)
    skin_color = db.Column(db.String(120), nullable=False)
    eye_color = db.Column(db.String(120), nullable=False)
    birth_year = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    created= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    favorite = db.relationship('Favorite', backref='people')

    def __repr__(self):
        return '<People %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "created": self.created
        }


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    diameter = db.Column(db.String(120), nullable=False)
    rotation_period = db.Column(db.String(120), nullable=False)
    orbital_period = db.Column(db.String(120), nullable=False)
    gravity = db.Column(db.String(120), nullable=False)
    population = db.Column(db.String(120), nullable=False)
    climate = db.Column(db.String(120), nullable=False)
    terrain = db.Column(db.String(120), nullable=False)
    surface_water = db.Column(db.String(120), nullable=False)
    created= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    favorite = db.relationship('Favorite', backref='deimian')

    def __repr__(self):
        return '<Planets %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "created": self.created
        }
    

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    created= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # user

    def __repr__(self):
        return '<Favorites %r>' % self.id
    

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id,
            "created": self.created, 
            "user":self.user.name
        }
    


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }