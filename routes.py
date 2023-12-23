from flask import Flask, render_template ,request, jsonify
import requests
import base64
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, DECIMAL, BigInteger
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.orm import declarative_base, relationship, sessionmaker


from functions import Functions
import os
from flask import Flask


app = Flask(__name__)

#Configure Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"

db = SQLAlchemy(app)

app.app_context().push()


class User(db.Model):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)  # Ensure unique usernames
    tests = relationship('Test', back_populates='user')

    @classmethod
    def create_user(cls, session, username):
        try:
            # Try to get a user with the given username
            existing_user = session.query(cls).filter(cls.username == username).one()
            return existing_user  # User with the same username already exists
        except NoResultFound:
            # If no user with the given username is found, create a new user
            new_user = cls(username=username)
            session.add(new_user)
            return new_user

class Test(db.Model):
    __tablename__ = 'Test'

    imageset_id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(BigInteger)  # Use BigInteger for non-countable integers
    time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('User.user_id'))



with app.app_context():
    db.create_all()
	



# two decorators, same function
@app.route('/')
@app.route('/Index')
def Index():
    return render_template('Index.html', the_title='Phantomzeichner')





# two decorators, same function
@app.route('/Imageset', methods=['GET'])
def Imageset():
    return render_template('Imageset.html', the_title='Phantomzeichner')



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
    name_value = data.get('user')
    number_value = data.get('number')

    Session = sessionmaker(bind=db.engine)
    session = Session()
    # Insert a new User
    new_user = new_user = User.create_user(session, name_value)
    session.add(new_user)
    session.commit()

    # Insert a new ImageSet
    new_imageset = Test(selected_image=key_value, image_id=number_value, time=datetime.now(), user=new_user)
    session.add(new_imageset)
    session.commit()


    return "Route triggered successfully!"

if __name__ == '__main__':
    app.run(debug=True)
