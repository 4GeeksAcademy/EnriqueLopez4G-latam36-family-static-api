"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# diccionario global para almacenar las familias
families = {}

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }
    return jsonify(response_body), 200

#Este decorador con su funcion es para crear una nueva familia, y no estar limitado solo a la familia jackson
@app.route('/family', methods=['POST'])
def create_family():
    # Obtener el apellido de la familia del cuerpo de la solicitud
    data = request.get_json()
    last_name = data.get('last_name')  # El apellido es un parámetro en el cuerpo de la solicitud
    
    if not last_name:
        return jsonify({"error": "El apellido de la familia es obligatorio"}), 400

    # Crear una nueva instancia de FamilyStructure con el apellido recibido
    #osea usando la estructura que nos da familyStructura la usamos en families de esa nueva familia
    if last_name not in families:
        families[last_name] = FamilyStructure(last_name)
    
    return jsonify({"message": f"Familia {last_name} creada exitosamente."}), 200

#---------------------------------------------------------------------------------------
#una vez que ya tengams una familia nueva, podremos agregar mimebros a esta nueva familia
#hice un pequeño cambio, agrego a la url /family el apellido de la familia para luego meter mi miembro en esa familia
@app.route('/family/<last_name>/member', methods=['POST'])
def add_member(last_name):
    # Verificar si la familia existe #puede que aun el user no la haya creado
    if last_name not in families:
        return jsonify({"error": f"La familia {last_name} no existe."}), 404
    
    # Obtener los datos del miembro #oby ya tuvo que haberla creado ahora sacamos los datos del miembro
    data = request.get_json()
    member = {
        "first_name": data.get('first_name'),
        "age": data.get('age'),
        "lucky_numbers": data.get('lucky_numbers')
    }
    
    # Agregar el miembro a la familia correspondiente
    families[last_name].add_member(member)
    
    return jsonify({"message": f"Miembro {member['first_name']} {last_name} agregado exitosamente."}), 200

#------------------------------------------------------------------
#OBTENER TODOS LOS MEMBERS DE LA FAMILIA FULANA DE TAL "last_name"
@app.route('/family/<last_name>/members', methods=['GET'])
def get_members(last_name):
    # Verificar si la familia existe
    if last_name not in families:
        return jsonify({"error": f"La familia {last_name} no existe."}), 404
    
    # Obtener los miembros de la familia
    members = families[last_name].get_all_members()
    
    return jsonify(members), 200

#------------------------------------------------------------------------------
#ELIMINAR UN MIEMBRO DE LA FAMILIA fulana de tal "last_name"
@app.route('/family/<last_name>/member/<int:member_id>', methods=['DELETE'])
def delete_some_member(last_name, member_id):
    if last_name not in families:
        return jsonify({"error": f"La familia {last_name} no existe."}), 404
    
    # Obtener la familia correspondiente
    family = families[last_name]
    
    # Intentar eliminar el miembro
    try:
        family.delete_member(member_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    
    return jsonify({"message": f"Miembro con ID {member_id} de la familia {last_name} eliminado."}), 200

#-----------------------------------------------
#TRAE UN MIEMBRO DE LA FAMILIA fulana de tal "last_name" QUE TENGA EL ID ESPECIFICADO
@app.route('/family/<last_name>/member/<int:member_id>', methods=['GET'])
def get_member_by_id(last_name, member_id):
    if last_name not in families:
        return jsonify({"error": f"La familia {last_name} no existe."}), 404
    
    # Obtener la familia correspondiente
    family = families[last_name]
    
    member_getted = family.get_member(member_id)
    
    return jsonify(member_getted), 200
#----------------------------------------------




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
