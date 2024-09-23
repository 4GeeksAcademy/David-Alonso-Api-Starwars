"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, PlanetFavView, CharacterFavView


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

# Handle/serialize errors like a JSON objectAlberto el mejor !
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

########################################## GET #########################################

#######GET USERS#########


@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()    
    results = list (map(lambda usuario: usuario.serialize (), all_users))
    
    if not all_users:
        return jsonify(message="Users not found"), 404
        
    return jsonify(results), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)    
   
    if user is None:
        return jsonify(message="User not found"), 404
        
    return jsonify(user.serialize()), 200

@app.route('/user/favorites', methods=['GET'])
def get_user_fav():
    
    users = User.query.all()
    
    user_favorites = []
    
    for user in users:
        user_favorites.append({
            "user_id": user.id,
            "username": user.username,
            "character_favorites": [character_fav.character.serialize() for character_fav in user.character_fav],
            "planet_favorites": [planet_fav.planet.serialize() for planet_fav in user.planet_fav]
        })
    
    return jsonify(user_favorites), 200

###### GET CHARACTERS #########

@app.route('/character', methods=['GET'])
def get_characters():
    all_characters = Character.query.all()    
    results = list (map(lambda character: character.serialize (), all_characters)) 
    

    return jsonify(results), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.filter_by(id=character_id).first() 
     
    return jsonify(character.serialize()), 200

@app.route('/character_fav', methods=['GET'])
def get_character_fav():
    characters_fav = CharacterFavView.query.all() 
    results = list(map(lambda item: item.serialize(), characters_fav))
    
    if not characters_fav:
        return jsonify(message="No se han encontrado personajes favoritos"), 404

    return jsonify(results), 200


###### GET PLANETS ##########

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planet.query.all()    
    results = list (map(lambda planet: planet.serialize (), all_planets)) 


    return jsonify(results), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)

    if planet is None: 
        return jsonify (message="Planet not found"), 404
     
    return jsonify(planet.serialize()), 200

@app.route('/planet_fav', methods=['GET'])
def get_planet_fav():
    planets_fav = PlanetFavView.query.all() 
    results = list(map(lambda item: item.serialize(), planets_fav))

    if not planets_fav:
        return jsonify(message = "Planets not found"), 404

    
    return jsonify (results), 200


########################################## DELETE #########################################


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()

   

    return jsonify({'message': f'{user_id} has been delete'}), 200

@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"error": "Character not found"}), 404
    db.session.delete(character)
    db.session.commit()

   
    return jsonify({'message': f'{character_id} character has been delete'}), 200

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    db.session.delete(planet)
    db.session.commit()

   
    return jsonify({'message': f'{planet_id} planet has been delete'}), 200


########################################## POST #########################################


###### POST USERS ##########



###### POST CHARACTERS ##########

@app.route('/user', methods=['POST'])
def add_new_user():
    request_body_user = request.get_json()

   
    if (
        "email" not in request_body_user
        or "password" not in request_body_user
        or "username" not in request_body_user
    ):
        return jsonify({"error": "Datos incompletos"}), 400

    new_user = User(
        username=request_body_user["username"],
        email=request_body_user["email"],
        password=request_body_user["password"],
        is_active=request_body_user["is_active"],
        firstname = request_body_user["firstname"],
        lastname = request_body_user["lastname"]
   
   

    )

    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "msg": "A new user has been added"
    }

    return jsonify(response_body), 200


@app.route('/character', methods=['POST'])
def add_character():
    body = request.get_json()

    if 'name' not in body:
        return jsonify ('Indica el nombre'), 400
    if body['name'] == '':
        return jsonify ('El nombre es obligatorio'), 400

    characters = Character( **body)
    db.session.add(characters)
    db.session.commit()

    response_body ={
        "msg":"New character added"
    }
     
    return jsonify(response_body), 200

@app.route('/planet', methods=['POST'])
def add_planet():
    body = request.get_json()

    if 'name' not in body:
        return jsonify ('Indica el nombre'), 400
    if body['name'] == '':
        return jsonify ('El nombre es obligatorio'), 400

    planet = Planet( **body)
    db.session.add(planet)
    db.session.commit()

    response_body ={
        "msg":"New planet added"
    }
    return (response_body),200

@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)

    if not user:
        return jsonify({"error": "User not found"}), 404
    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    # Verificar si el planeta ya está en la lista de favoritos
    if planet in user.favorite_planets:
        return jsonify({"msg": "Planet already in favorites"}), 400

    # Añadir el planeta a los favoritos del usuario
    user.favorite_planets.append(planet)
    db.session.commit()

    return jsonify({
        "msg": f"Planet {planet.name} has been added to favorites",
        "favorite_planets": [p.serialize() for p in user.favorite_planets]
    }), 200



    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
