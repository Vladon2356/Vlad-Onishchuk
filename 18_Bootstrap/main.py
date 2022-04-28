import os
import requests
from flask import Flask, render_template, url_for, request, session, redirect
from config import Config, TestingConfig
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
app.debug = True


@app.route('/home/', methods=['GET'])
def home():
    return render_template('app/home.html')


@app.route('/calculator/', methods=['GET', 'POST'])
def daily_calorie_calculator():
    if request.method == 'GET':
        return render_template('app/daily_calorie_calculator.html')
    if not request.form:
        return render_template('app/calculator_error.html',
                               message='Please, specify "mass", "age", "sex" and "height".')

    sex = request.form.get('sex')
    mass = float(request.form.get('mass'))
    height = float(request.form.get('height'))
    age = int(request.form.get('age'))

    if sex == 'Female':
        res = int((9.277 * mass) + (3.098 * height) - (4.33 * age) + 447.593)
    else:
        res = int((13.397 * mass) + (4.799 * height) - (5.677 * age) + 88.362)
    session['count_calorie_norm'] = res
    return render_template('app/view_daily_calorie_norm.html', result=res)


@app.route('/menu/create/', methods=['GET','POST'])
def create_menu():
    if request.method == 'GET':
        session['menu'] == []

        return render_template('app/create_menu.html')
    if 'count_calorie_norm' not in session:
        return redirect(url_for('daily_calorie_calculator'))
    session['menu'] = []
    session['count_calorie'] = 0
    return redirect(url_for('show_menu'))

@app.route('/menu/', methods = ['GET'])
def show_menu():
    if 'menu' not in session:
        return redirect(url_for('create_menu'))
    return render_template('app/menu_show.html',
                           menu=session['menu'],
                           count_calorie=session['count_calorie'],
                           count_calorie_norm= session['count_calorie_norm'])

@app.route('/menu/add_product/', methods=['POST', 'GET'])
def add_product_to_menu():
    if 'menu' not in session:
        return redirect(url_for('create_menu'))
    if request.method == 'GET':
        return render_template('app/menu_add_product.html')
    if request.method == 'POST':
        product = request.form.get('product')
        if product == '':
            return render_template('app/menu_error.html', message='Plese enter product')
        else:
            try :
                kcal_on_100g = edamam_search(product)
            except Exception:
                return render_template('app/menu_error.html', message=f'Product - {product} not found')
            mass = int(request.form.get('mass'))
            product_calorie = int(kcal_on_100g * mass / 100)
            session['count_calorie'] += product_calorie
            session['menu'].append({'product': product, 'calorie': product_calorie, "mass": mass})

            return redirect(url_for('show_menu'))
@app.route('/menu/delete_product/', methods=['POST','GET'])
def delete_product_from_menu():
    if request.method == 'GET':
        return render_template('app/menu_delete_product.html',
                               menu=session['menu'],
                               count_calorie=session['count_calorie']
                               )
    if 'menu' not in session:
        return render_template('app/create_menu.html')
    if not session['menu']:
        return redirect(url_for('add_product_to_menu'))
    product = request.form.get('product')
    for index, item in enumerate(session['menu']):
        if item['product'] == product:
            session['count_calorie'] -= int(item['calorie'])
            session['menu'].pop(index)
    return redirect(url_for('show_menu'))

def edamam_search(product:str):
    app_id = os.environ['APP_ID']
    app_key = os.environ['APP_KEY']

    curl = f"https://api.edamam.com/api/food-database/v2/parser?app_id={app_id}&app_key={app_key}&" \
           f"ingr={product.lower()}"
    response = requests.get(curl)
    res = response.json()['hints'][0]['food']['nutrients']['ENERC_KCAL']


    return res
