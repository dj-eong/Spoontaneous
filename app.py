from flask import Flask, render_template, redirect, session, jsonify, flash
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, SavedRecipe
from forms import RegisterForm, LoginForm
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///spoontaneous'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = 'abc123'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)


@app.route('/')
def homepage():
    if 'username' in session:
        user = db.session.query(User).filter_by(username=session['username']).first()
        return render_template('index.html', user=user)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data

            new_user = User.register(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

            session['username'] = new_user.username
            return redirect('/')
        except:
            flash('Username is taken!')
            return render_template('register-form.html', form=form)

    return render_template('register-form.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect('/')
        else:
            form.password.errors = ['Invalid username/password.']

    return render_template('login-form.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

@app.route('/saved-recipes/<int:recipe_id>', methods=["POST"])
def save_recipe(recipe_id):
    """Creates user + saved recipe row in database"""
    user = db.session.query(User).filter_by(username=session['username']).first()
    data = get_recipe(recipe_id)
    name = data['meals'][0]['strMeal']
    saved_recipe = SavedRecipe(user_id=user.id, recipe_id=recipe_id, name=name)
    db.session.add(saved_recipe)
    db.session.commit()
    return jsonify(message='saved')

@app.route('/saved-recipes/<int:recipe_id>', methods=["DELETE"])
def unsave_recipe(recipe_id):
    """Removes user + saved recipe row in database"""
    user = db.session.query(User).filter_by(username=session['username']).first()
    saved_recipe = db.session.query(SavedRecipe).filter(SavedRecipe.user_id == user.id, SavedRecipe.recipe_id == recipe_id).first()
    
    db.session.delete(saved_recipe)
    db.session.commit()
    return jsonify(message='deleted')

@app.route('/saved-recipes')
def list_saved_recipes():
    user = db.session.query(User).filter_by(username=session['username']).first()
    return render_template('saved-recipes.html', user=user)

@app.route('/api/saved-recipes')
def get_saved_recipes():
    user = db.session.query(User).filter_by(username=session['username']).first()
    lst = []
    for recipe in user.recipes:
        lst.append(recipe.recipe_id)
    return jsonify(lst)

@app.route('/recipe/<int:recipe_id>')
def show_recipe(recipe_id):
    if 'username' not in session:
        return redirect('/')
    user = db.session.query(User).filter_by(username=session['username']).first()
    data = get_recipe(recipe_id)
    recipe = data['meals'][0]
    return render_template('recipe.html', recipe=recipe, user=user)

def get_recipe(recipe_id):
    API_BASE_URL = 'https://www.themealdb.com/api/json/v1/1/lookup.php?i='
    res = requests.get(f'{API_BASE_URL}{recipe_id}')
    return res.json()
