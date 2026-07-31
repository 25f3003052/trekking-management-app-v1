from flask import Flask
from config import DevelopmentConfig
from models import db
import models


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app) # linkin the database with the app. 

from routes import *





# Flask -> 
if __name__ == "__main__":
    with app.app_context(): 
        db.create_all() 
        admin = models.User.query.filter_by(user_name='admin').first()
        if not admin:
            admin = models.User(user_name='admin',name='admin',email_id="admin@gmail.com",address="address",is_admin=True,pincode=234,age=30,gender="Male",phone="234234")

            admin.set_password("admin")
            db.session.add(admin)
            db.session.commit()


    app.run(debug=True,port=8000)