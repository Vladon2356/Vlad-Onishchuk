from flask import jsonify, request, Blueprint
from constants import LIMIT, OFFSET
const_limit = LIMIT
const_offset = OFFSET
from ..models.owner import OwnerModel

owners_bp = Blueprint('owners', __name__)


@owners_bp.route("/owners/", methods=["GET"])
def get_owners():
    find_by_name = request.args.get('name')
    find_by_age = request.args.get('age')
    offset = request.args.get("offset", const_offset)
    limit = request.args.get("limit", const_limit)

    if find_by_name:
        owners = OwnerModel.find_by_name(find_by_name,offset, limit)
    if find_by_age:
        owners = OwnerModel.find_by_age(find_by_age,offset, limit)
    if not owners :
        owners = OwnerModel.return_all(offset, limit)
    return jsonify(owners)


@owners_bp.route("/owners/<int:id>", methods=["GET"])
def get_owner(id):
    owner = OwnerModel.find_by_id(id)
    if not owner:
        return jsonify({"message": "owner not found."}), 404

    return jsonify(owner)


@owners_bp.route("/owners", methods=["POST"])
def create_owner():
    if not request.json:
        return jsonify({"message": 'Please, specify "name" and "age".'}), 400

    age = request.json.get("age")
    name = request.json.get("name")

    if not age or not name:
        return jsonify({"message": 'Please, specify "name" and "age".'}), 400

    owner = OwnerModel(name=name, age=age)
    owner.save_to_db()

    return jsonify({"id": owner.id}), 201


@owners_bp.route("/owners/<int:id>", methods=["PATCH"])
def update_owner(id):
    age = request.json.get("age")
    name = request.json.get("name")

    owner = OwnerModel.find_by_id(id, to_dict=False)
    if not owner:
        return jsonify({"message": "owner not found."}), 404

    if age:
        owner.age = age
    if name:
        owner.name = name
    owner.save_to_db()
    return jsonify({"message": "Updated"})


@owners_bp.route("/owners/<int:id>", methods=["DELETE"])
def delete_owner(id):
    code = OwnerModel.delete_by_id(id)
    if code == 404:
        return jsonify({"message": "owner not found."}), 404

    return jsonify({"message": "Deleted"})
