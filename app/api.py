from flask import Blueprint, request

from app import db
from app.models import Location, Meal, Item, Nutrition
from app.util import to_json

import os
import datetime


DATE_FMT = '%Y-%m-%d'

api_bp = Blueprint('api', __name__)

STATUS = to_json({
    'message': os.environ.get('STATUS_MESSAGE'),
    'min_version_ios': int(os.environ.get('STATUS_MIN_VERSION_IOS', 0)),
    'min_version_android': int(os.environ.get('STATUS_MIN_VERSION_ANDROID', 0)),
})


@api_bp.route('/status')
def api_status():
    return STATUS


@api_bp.route('/halls')
def api_halls():
    halls = Hall.query.order_by(Hall.nickname).all()
    return to_json(halls)


@api_bp.route('/halls/<hall_id>')
def api_hall(hall_id):
    hall = Hall.query.get_or_404(hall_id)
    return to_json(hall)


@api_bp.route('/halls/<hall_id>/managers')
def api_managers(hall_id):
    hall = Hall.query.get_or_404(hall_id)
    managers = hall.managers
    return to_json(managers)


@api_bp.route('/halls/<hall_id>/meals')
def api_hall_meals(hall_id):
    # TODO: use this later on, right now it's mostly a 404 check
    hall = Hall.query.get_or_404(hall_id)
    meals = Meal.query.filter_by(hall_id=hall_id)
    date = request.args.get('date')
    if date is not None:
        meals = meals.filter(Meal.date == date)
    else:
        start_date = request.args.get('start_date')
        if start_date is None:
            start_date = datetime.date.today()
        else:
            start_date = datetime.datetime.strptime(start_date, DATE_FMT)
        meals = meals.filter(start_date <= Meal.date)
        end_date = request.args.get('end_date')
        if end_date is not None:
            meals = meals.filter(Meal.date <= end_date)
    meals = meals.order_by(Meal.date, Meal.start_time)
    meals = meals.all()
    return to_json(meals)


@api_bp.route('/meals')
def api_meals():
    meals = Meal.query.all()
    return to_json(meals)


@api_bp.route('/meals/<meal_id>')
def api_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    return to_json(meal)


@api_bp.route('/meals/<meal_id>/recipes')
def api_meal_recipes(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    recipes = meal.recipes
    return to_json(recipes)


@api_bp.route('/recipes')
def api_recipes():
    recipes = Item.query.all()
    return to_json(recipes)


@api_bp.route('/recipes/<recipe_id>')
def api_recipe(recipe_id):
    recipe = Item.query.get_or_404(recipe_id)
    return to_json(recipe)


@api_bp.route('/recipes/<recipe_id>/nutrition')
def api_recipe_nutrition(recipe_id):
    recipe = Item.query.get_or_404(recipe_id)
    nutrition = recipe.nutrition
    return to_json(nutrition)
