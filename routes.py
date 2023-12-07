from flask import Flask, render_template ,request, jsonify
import requests
import base64
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, DECIMAL

from sqlalchemy.orm import declarative_base, relationship, sessionmaker


from functions import Functions
import os
from flask import Flask
from flask_mysqldb import MySQL


app = Flask(__name__)

#Configure Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"

db = SQLAlchemy(app)

app.app_context().push()

class User(db.Model):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    tests = relationship('Test', back_populates='user')

class ImageSet(db.Model):
    __tablename__ = 'ImageSet'

    imageset_id = Column(Integer, primary_key=True, autoincrement=True)
    imageset_name = Column(String(255), nullable=False)
    tests = relationship('Test', back_populates='imageset')

class Test(db.Model):
    __tablename__ = 'Test'

    test_id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, nullable=False)
    highscore_percentage = Column(DECIMAL(5,2), nullable=False)
    
    user_id = Column(Integer, ForeignKey('User.user_id'))
    user = relationship('User', back_populates='tests')

    imageset_id = Column(Integer, ForeignKey('ImageSet.imageset_id'))
    imageset = relationship('ImageSet', back_populates='tests')
	



# two decorators, same function
@app.route('/')
@app.route('/Index')
def Index():
    return render_template('index.html', the_title='Phantomzeichner')

@app.route('/get_images', methods=['GET'])
def get_images():
    # Assuming the request content type is set to 'application/json'
   
    key_value = request.args.get('number')
    print(key_value)

    return jsonify(images=Functions.get_images_by_base_id(key_value))



@app.route('/baseIds')
def BaseIds():
    return jsonify(images=Functions.get_baseids())

@app.route('/baseImage')
def baseImage():
    key_value = request.args.get('number')
    print(key_value)
    return jsonify(images=Functions.get_baseimage(key_value))


@app.route('/Validate', methods=['GET'])
def Validate():
    return render_template('Validate.html', the_title='Phantomzeichner')


@app.route('/trigger_route', methods=['POST'])
def trigger_route():

    # Assuming the request content type is set to 'application/json'
    data = request.get_json()

    # Access the value using the key
    key_value = data.get('key')

    Session = sessionmaker(bind=db.engine)
    session = Session()
    # Insert a new User
    new_user = User(username='JohnDoe')
    session.add(new_user)
    session.commit()

    # Insert a new ImageSet
    new_imageset = ImageSet(imageset_name=key_value)
    session.add(new_imageset)
    session.commit()

    # Insert a new Test associated with the User and ImageSet
    new_test = Test(
        time=datetime.now(),
        highscore_percentage=90.5,
        user=new_user,
        imageset=new_imageset
    )
    session.add(new_test)
    session.commit()

    return "Route triggered successfully!"

if __name__ == '__main__':
    app.run(debug=True)
