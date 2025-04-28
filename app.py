from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=True)

@app.route('/')
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

@app.route('/recipe/<int:id>')
def view_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('view_recipe.html', recipe=recipe)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        image = request.form['image']
        new_recipe = Recipe(title=title, category=category, ingredients=ingredients, instructions=instructions, image=image)
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_recipe.html')

@app.route('/delete/<int:id>')
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if Recipe.query.count() == 0:
            samples = [
                Recipe(
                    title="Jollof Rice",
                    category="Nigerian",
                    ingredients="Rice, Tomatoes, Onion, Pepper, Oil, Seasoning",
                    instructions="1. Blend tomato, pepper and onions. 2. Fry in oil. 3. Add rice and cook till soft.",
                    image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Nigerian_Jollof_Rice.jpg/640px-Nigerian_Jollof_Rice.jpg"
                ),
                Recipe(
                    title="Egusi Soup",
                    category="Nigerian",
                    ingredients="Egusi, Palm oil, Meat, Stockfish, Crayfish, Seasoning",
                    instructions="1. Add your palm oil into a pot. 2. Add your mixed grounded egusi . 3. Allow to cook for 3 minutes. 4. Add your meat, fish and ponmo into the the egusi on fire 5.leaves into the egusi and then allow to cook for a minute 6. Serve with hot pounded Yam",
                    image="https://upload.wikimedia.org/wikipedia/commons/4/4e/Egusi_soup.jpg" 
                ),
                Recipe(
                    title="Jollof Spaghetti",
                    category="Foreign",
                    ingredients="Spaghetti, Eggs, Cheese, Bacon, Pepper",
                    instructions="1. Boil spaghetti. 2. Fry bacon. 3. Boil your egg inside the spaghetti. 4. Filter the water out, then rinse the pot and put on fire then add oil, and fry your bacon and remove, add your onions and tin-tomato, stir fry and add your grounded pepper and cover for 1minute to allow it cook, stir and add your spaghetti then mix and leave it for 30seconds then add your egg..  ",
                    image="https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Spaghetti_alla_Carbonara.jpg/640px-Spaghetti_alla_Carbonara.jpg"
                ),
                Recipe(
                    title="Sushi",
                    category="Foreign",
                    ingredients="Rice, Nori, Fish, Vegetables, Vinegar",
                    instructions="1. Cook rice with vinegar. 2. Roll with nori and fillings. 3. Slice and serve.",
                    image="https://upload.wikimedia.org/wikipedia/commons/6/60/Sushi_platter.jpg"
                )
            ]
            db.session.bulk_save_objects(samples)
            db.session.commit()
    app.run(debug=True)