from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from myMail import recipent

from fixed_bills import bills_bp
from flask_cors import CORS


app = Flask(__name__)


CORS(app)

app.config['SECRET_KEY'] = 'SUPER-SECRET-KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:aarna2002$@localhost:5433/projectdb'

db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()


class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        email = data.get('email')
        password = data['password']

        if not username or not password:
            return {'message': 'Missing username or password'}, 400
        if User.query.filter_by(username=username).first():
            return {'message':'Username already taken'}, 400
        
        if User.query.filter_by(email=email).first():
            return {'message': 'Email already registered'}, 400
        
        self.register_user(username, email, password)           ## Call helper method to handle user creation
        return {'message':'User created successfully'}, 200
    
    def register_user(self, username, email, password):
        new_user = User(username=username, email=email, password = password)
        db.session.add(new_user)
        db.session.commit() 
        recipent(email)


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        identifier = data['username']   # could be username or email
        password = data['password']

        if not identifier or not password:
            return {'message': 'Missing username/email or password'}, 400

        user = User.query.filter((User.username==identifier) | (User.email==identifier)).first()

        if user and user.password==password:
            access_token=create_access_token(identity=str(user.id))

            return {'access_token': access_token}, 200
        
        return {'message':'invalid credentials'}, 401



class ProtectedResource(Resource):
    @jwt_required()      #dekhe ga  ki jwt token hai kya
    def get(self):
        current_user_id=get_jwt_identity()
        return {'message':f"hello user {current_user_id}, you accessed the protected resource"}, 200 
        

app.register_blueprint(bills_bp)

api.add_resource()
api.add_resource(UserRegistration,'/register')
api.add_resource(UserLogin, '/login')
api.add_resource(ProtectedResource, '/secure')



if __name__=="__main__":
    app.run(debug=True)

