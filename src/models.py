from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    firstname = db.Column(db.String(250), unique=False, nullable=False)
    lastname = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(40), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)
    character_fav = db.relationship("CharacterFavView", back_populates="user")
    planet_fav = db.relationship("PlanetFavView", back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "favorite_planets": [planet.serialize() for planet in self.planet_fav]
        }
# fdfdf

class Character(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    especies = db.Column(db.String(250), nullable=False)
    role = db.Column(db.String(250), nullable=False)
    lifestatus = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    character_fav = db.relationship("CharacterFavView", back_populates="character")

    def __repr__(self):
            return '<Characters %r>' % self.name
    def serialize (self):
          return {
                "id": self.id,
                "name": self.name,
                "especies": self.especies,
                "role": self.role,
                "lifestatus": self.lifestatus,
                "gender": self.gender
                }

class Planet(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    galactic_location = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(40), nullable=False)
    population = db.Column(db.String(40), nullable=False)
    native_species = db.Column(db.String(40), nullable=False)
    govemment = db.Column(db.String(40), nullable=False)
    planet_fav = db.relationship("PlanetFavView", back_populates="planet")

    def __repr__(self):
            return '<Planets %r>' % self.name
    def serialize (self):
          return {
                "id": self.id,
                "name": self.name,
                "galactic_location": self.galactic_location,
                "climate": self.climate,
                "population": self.population,
                "native_species": self.native_species,
                "govemment": self.govemment
            
            }
    
class PlanetFavView(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    user = db.relationship("User", back_populates="planet_fav")
    planet = db.relationship("Planet", back_populates="planet_fav")
   
        
    def __repr__(self):
        return '<PlanetFavView %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "user_id": self.user_id
        }
    
class CharacterFavView(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))
    user = db.relationship("User", back_populates="character_fav")
    character = db.relationship("Character", back_populates="character_fav")
   
        
    def __repr__(self):
        return '<CharacterFavView %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "character_id": self.character_id,
            "user_id": self.user_id
        }
    
