import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.urls import url_parse
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms import StringField, PasswordField, SubmitField, BooleanField




app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'cooking_recipes'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@myfirstcluster-rffnv.mongodb.net/cooking_recipes?retryWrites=true&w=majority'
app.config["SECRET_KEY"] = '4f1421d2299968b6e9ce128fa0ec1048'


mongo = PyMongo(app)
db = 'mongodb+srv://root:r00tUser@myfirstcluster-rffnv.mongodb.net/cooking_recipes?retryWrites=true&w=majority'
login_manager = LoginManager(app)



#+++++++++++++++++++++++++


class RegistrationForm(FlaskForm):
    username = db.StringField('Username', validators=[DataRequired()])
    email = db.StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
    
class LoginForm(FlaskForm):
    username = db.StringField('Username', validators=[DataRequired()])
    email = db.StringField('Email address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_username(self, username):
        form = LoginForm()
        user = User.objects(username=username.data).first()
        if user is None or not user.check_password(form.password.data):
            raise ValidationError('Invalid username or password')
            
            
class User(UserMixin):
    username = mongo.StringField(max_length=64)
    email = mongo.StringField(max_length=120)
    password_hash = mongo.StringField(max_length=128)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


#++++++++++++++++++++++++++


@app.route('/')
@app.route('/get_recipe')
def get_recipe():
    return render_template('recipes.html', recipes=mongo.db.recipes.find())
    
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
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


    
    


    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)