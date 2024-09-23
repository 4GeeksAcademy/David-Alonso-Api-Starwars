import os
from flask_admin import Admin
from models import db, User, Character, Planet, PlanetFavView, CharacterFavView
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(PlanetFavView, db.session))
    admin.add_view(ModelView(CharacterFavView, db.session))
    
    # class Planet_fav(ModelView):
    #     can_create = False
    #     can_edit = False
    #     can_delete = Falsefd
        
    #     column_list = ('user_id', 'planet_id')  # Puedes ajustar los campos que quieras mostrar

    # # Agregar la vista de favoritos a la administración
    # admin.add_view(Planet_fav(Planet_fav, db.session, name='Planet Favoerites'))

    
    # Add your models here, for example this is how we add a the User model to the admin
     

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))