
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from markupsafe import re
from sqlalchemy_utils.types.choice import ChoiceType
import datetime
import json
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token)
app = Flask(__name__)


DATABASE_URI = "sqlite:///posts.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI



db = SQLAlchemy(app)
app.config['JWT_SECRET_KEY'] = "secret-key"
jwt = JWTManager(app)

USERNAME = 'esraa1'
PASSWORD = '123456'
access=[]
 
class Posts(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


#--------------------- get all posts ---------------------------#

@app.route('/post', methods=['GET'])

def get_posts():
    posts = Posts.query.all()
    data_result = []
    for post in posts:
        p = {}
        p["id"] = post.id
        p["title"] = post.title
        p["description"] = post.description

        data_result.append(p)
        
    return jsonify({
        "result": "success",
        "data": data_result
    })



#--------------------- add new post ---------------------------#

@app.route('/post', methods=['POST'])
def add_post():
    
    if access:
            data = json.loads(request.data)
            title = data["title"]
            description = data["description"]
            try:
                post = Posts(title=title, description=description)
                db.session.add(post)
                db.session.commit()
            except ValueError as e:
                return jsonify({
                        "result": "Failed",
                        "data": "failed to add post "
                    })

            return jsonify({
                        "result": "success",
                        "data": "post added successfully"
                    })
    else:
        return {
          'status': 'failed',
          'data': 'you do not have a valid token',
            }
    


  



#--------------------- update a post ---------------------------#

@app.route('/post/<int:id>', methods=['PUT'])
def update_post(id):
    if access:
        try:
            post = Posts.query.get(id)
            data = json.loads(request.data)
            title = data["title"]
            description=data["description"]
            post.title = title
            post.description = description
            db.session.commit()

            return jsonify({
                "result": "success",
                "data": "Post updated successfully"
            })
        except:
                return jsonify({
                "result": "faild",
                "data": "faild to update post "
            })
    else:
        return {
          'status': 'failed',
          'data': 'you do not have a valid token',
            }    
#--------------------- Delete a post ---------------------------#
@app.route('/post/<int:id>', methods=['DELETE'])
def delete_post(id):
    if access: 
        try:       
            post = Posts.query.filter_by(id=id).first()
            db.session.delete(post)
            db.session.commit()

            return jsonify({
                "result": "success",
                "data": "post deleted successfully"
            })
        except:
             return jsonify({
                "result": "faild",
                "data": "faild to delete post"
            })

        else:
            return {
          'status': 'failed',
          'data': 'you do not have a valid token',
            }   
#--------------------- get spesific post by id ---------------------------#

@app.route('/post/<int:id>', methods=['GET'])
def get_post_by_id(id):
    post = Posts.query.filter_by(id=id).first()
    p = {}
    p["id"] = post.id
    p["title"] = post.title
    p["description"] = post.description

    return jsonify({
        "result": "success",
        "data": p
    })

#################################################

@app.route('/home')
def home():
    return jsonify({
        "result": "success",
        "data": "Welcome Home Page"
    })
    
    
    
    
    
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username == USERNAME and password == PASSWORD:
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        access.append(access_token) 
        return {
            'status': 'success',
            'data': {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }
    return {
            'status': 'failed',
            'data': 'Bad username or password'
        }
@app.route('/logout', methods=['GET'])
def logout():
    access.clear()
    return redirect(url_for('login'))    

db.create_all()
app.run(debug=True)
