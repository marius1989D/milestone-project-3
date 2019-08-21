import os
import datetime
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId




app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'cooking_recipes'
app.config["MONGO_URI"] = os.getenv("MONGO_URI")


mongo = PyMongo(app)


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
    #datetime_now = datetime.datetime.utcnow()
    #current_date = datetime.datetime.strftime(datetime_now, '%b %d, %Y')
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
    datetime_now = datetime.datetime.utcnow()
    current_date = datetime.datetime.strftime(datetime_now, '%b %d, %Y')
    

    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        'recipe_category' : request.form.get('recipe_category'),
        'recipe_name' : request.form.get('recipe_name'),
        'recipe_ingredients' : request.form.get('recipe_ingredients'),
        'recipe_method' : request.form.get('recipe_method'),
        'recipe_time' : request.form.get('recipe_time'),
        'recipe_photo': request.form.get('recipe_photo'),
        'last_updated': current_date
    })
    return redirect(url_for('get_recipe'))
    
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipe'))
    
@app.route('/search_recipe')
def search_recipe():
    return render_template("search.html", categories=mongo.db.recipes.find())
    
@app.route('/get_results', methods = ['POST', 'GET'])
def get_results():
    recipes = mongo.db.recipes
    recipe_category = request.form.get('recipe_category')
    results = recipes.find({'recipe_category': recipe_category})
    return render_template('results.html', results=results)
    
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=False)
        
