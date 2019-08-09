import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_mongoengine import MongoEngine, Document
from werkzeug.urls import url_parse
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FieldList, FormField
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_bcrypt import Bcrypt





app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'cooking_recipes'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@myfirstcluster-rffnv.mongodb.net/cooking_recipes?retryWrites=true&w=majority'
app.config["SECRET_KEY"] = '4f1421d2299968b6e9ce128fa0ec1048'


mongo = PyMongo(app)
db = MongoEngine(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Document):
    meta = {'collection': 'users'}
    username = db.StringField(max_length=15)
    email = db.StringField(max_length=30)
    password = db.StringField()
    
    def add_user(self, username, email, password):
        user = mongo.db.users
        extisting_user = user.find_one({"username": username, 'email': email})
        
        if extisting_user is None:
            hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user.insert(
                {
                    "username": username,
                    "email": email,
                    "password": hashpass
                }
            )
            
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()
    
    
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('get_recipe'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        user.insert_one(request.form.to_dict())
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('get_recipe'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(email=form.email.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('get_recipe'))
    return render_template('login.html', form=form)


@app.route('/')
@app.route('/get_recipe')
def get_recipe():
    return render_template('recipes.html', recipes=mongo.db.recipes.find())
    
@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('viewrecipe.html', recipe=recipe)
    
@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html',
                           recipes=mongo.db.recipes.find())
                           
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes =  mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipe'))
    
@app.route('/edit_recipe/<recipe_id>', methods=['POST', 'GET'])
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('editrecipe.html', recipe=the_recipe, categories=all_categories)
    
@app.route('/update_recipe/<recipe_id>', methods = ["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        'recipe_category' : request.form.get('recipe_category'),
        'recipe_name' : request.form.get('recipe_name'),
        'recipe_ingredients' : request.form.get('recipe_ingredients'),
        'recipe_method' : request.form.get('recipe_method'),
        'recipe_time' : request.form.get('recipe_time')
    })
    return redirect(url_for('get_recipe'))
    
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipe'))
    

    


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


    



    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
        
