import os
from flask import Flask, request, jsonify, url_for, render_template  # Importa render_template
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# diccionario global para almacenar las familias
families = {}


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Ruta para mostrar la página de bienvenida
# @app.route('/')
# def home():
    # Obtener el apellido de la familia seleccionada del parámetro de la consulta
    # selected_family = request.args.get('family', None)
    
# @app.route('/members', methods=['GET'])

# def handle_hello():
#     members = jackson_family.get_all_members()
#     response_body = {
#         "hello": "world",
#         "family": members
#     }
#     return jsonify(response_body), 200

# Este decorador con su función es para crear una nueva familia
@app.route('/family', methods=['POST'])
def create_family():
    data = request.get_json()
    last_name = data.get('last_name')
    
    if not last_name:
        return jsonify({"error": "El apellido de la familia es obligatorio"}), 400

    if last_name not in families:
        families[last_name] = FamilyStructure(last_name)
    
    return jsonify({"message": f"Familia {last_name} creada exitosamente."}), 200
#------------------------------------------------------------------
# Endpoint para obtener todos los apellidos de las familias
@app.route('/families', methods=['GET'])
def get_all_families():
    # Obtener todos los apellidos de las familias almacenadas en el diccionario 'families'
    all_families = list(families.keys())

    # Devolver la lista de apellidos como respuesta JSON
    return jsonify(all_families), 200



# Ruta para agregar un miembro a la familia
@app.route('/family/<last_name>/member', methods=['POST'])
def add_member(last_name):
    if last_name not in families:
        return jsonify({"error": f"La familia {last_name} no existe."}), 404
    
    data = request.get_json()
    member = {
        "first_name": data.get('first_name'),
        "age": data.get('age'),
        "lucky_numbers": data.get('lucky_numbers')
    }
    
    families[last_name].add_member(member)
    
    return jsonify({"message": f"Miembro {member['first_name']} {last_name} agregado exitosamente."}), 200

# Obtener todos los miembros de la familia
@app.route('/family/<last_name>/members', methods=['GET'])
def get_members(last_name):
    if last_name not in families:
        return jsonify({"error": f"La familia {last_name} no existe."}), 404
    
    members = families[last_name].get_all_members()
    
    return jsonify(members), 200

# Eliminar un miembro de la familia
@app.route('/family/<last_name>/member/<int:member_id>', methods=['DELETE'])
def delete_some_member(last_name, member_id):
    if last_name not in families:
        return jsonify({"error": f"La familia {last_name} no existe."}), 404
    
    family = families[last_name]
    
    try:
        family.delete_member(member_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    
    return jsonify({"message": f"Miembro con ID {member_id} de la familia {last_name} eliminado."}), 200

# Obtener un miembro de la familia por ID
@app.route('/family/<last_name>/member/<int:member_id>', methods=['GET'])
def get_member_by_id(last_name, member_id):
    if last_name not in families:
        return jsonify({"error": f"La familia {last_name} no existe."}), 404
    
    family = families[last_name]
    
    member_getted = family.get_member(member_id)
    
    return jsonify(member_getted), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
