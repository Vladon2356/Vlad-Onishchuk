from flask import jsonify, request, Blueprint
from constants import LIMIT, OFFSET
const_limit = LIMIT
const_offset = OFFSET
from ..models.car import CarModel

cars_bp = Blueprint('cars', __name__)


@cars_bp.route("/cars", methods=["GET"])
def get_cars():
    find_by_brand = request.args.get('brand')
    find_by_price = request.args.get('price')
    find_by_model = request.args.get('model')
    find_by_owner_id = request.args.get('owner_id')

    cars = False
    offset = request.args.get("offset", const_offset)
    limit = request.args.get("limit", const_limit)
    if find_by_brand:
        cars = CarModel.find_by_brand(find_by_brand,offset, limit)
    if find_by_model:
        cars = CarModel.find_by_model(find_by_model,offset, limit)
    if find_by_price:
        cars = CarModel.find_by_price(find_by_price,offset, limit)
    if find_by_owner_id:
        cars = CarModel.find_by_owner_id(find_by_owner_id,offset,limit)
    if not cars:
        cars = CarModel.return_all(offset, limit)
    return jsonify(cars)


@cars_bp.route("/cars/<int:id>", methods=["GET"])
def get_car(id):
    car = CarModel.find_by_id(id)
    if not car:
        return jsonify({"message": "car not found."}), 404

    return jsonify(car)


@cars_bp.route("/cars", methods=["POST"])
def create_car():
    if not request.json:
        return jsonify({"message": 'Please, specify "model" and "brand" and "price".'}), 400

    model = request.json.get("model")
    brand = request.json.get("brand")
    price = request.json.get("price")
    car_owner_id = request.json.get('owner_id')

    if not model or not brand or not price:
        return jsonify({"message": 'Please, specify "model" and "brand" and "price"2.'}), 400

    car = CarModel(model=model, brand=brand, price=price,owner_id=car_owner_id)
    car.save_to_db()

    return jsonify({"id": car.id}), 201


@cars_bp.route("/cars/<int:id>", methods=["PATCH"])
def update_car(id):
    model = request.json.get("model")
    brand = request.json.get("brande")
    price = request.json.get("price")
    car_owner_id = request.json.get('owner_id')

    car = CarModel.find_by_id(id, to_dict=False)
    if not car:
        return jsonify({"message": "car not found."}), 404

    if brand:
        car.brand = brand
    if model:
        car.model = model
    if price:
        car.price = price
    if car_owner_id:
        car.owner_id = car_owner_id

    car.save_to_db()
    return jsonify({"message": "Updated"})


@cars_bp.route("/cars/<int:id>", methods=["DELETE"])
def delete_car(id):
    code = CarModel.delete_by_id(id)
    if code == 404:
        return jsonify({"message": "car not found."}), 404

    return jsonify({"message": "Deleted"})
