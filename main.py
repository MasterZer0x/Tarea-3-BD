
from flask import Flask
from flask import jsonify
from sqlalchemy.orm import session
from config import config
from models import CuentaBancaria, PrecioMoneda, UsuarioTieneMoneda, db
from models import Pais
from models import Usuario
from models import Moneda
from flask import request

app = Flask(__name__)
enviroment = config['development']
app.config.from_object(enviroment)
#   app = create_app(enviroment)
db.init_app(app)


@app.route('/')
def index():
    print("entro")
    return 'Hola mundo!'

# -------------------------------------- USUARIO --------------------------------------------


# CREATE
@app.route('/api/usuario', methods=['POST'])
def create_user():
    json = request.get_json(force=True)
    
    if None in (json.get('nombre'), json.get('correo'), json.get('contrasena'), json.get('pais')):
        return jsonify({'message': 'El formato está mal'}), 400


    usuario = Usuario.create(json['nombre'], json['apellido'], json['correo'], json['contrasena'], json['pais'])
    return jsonify({usuario.id:usuario.json()})


# READ
@app.route('/api/usuario', methods=['GET'])
def get_users():
    users = [ user.json() for user in Usuario.query.all() ] 
    users_return = dict()
    for user in users:
        users_return[user['id']] = user
    return jsonify(users_return)
    
# READ 1 USER
@app.route('/api/usuario/<id>', methods=['GET'])
def get_user(id):
    usuario = Usuario.query.filter_by(id=id).first()
    if usuario is None:
        return jsonify({'mensaje': 'El usuario no existe'}), 404
    return usuario.json()



# UPDATE
@app.route('/api/usuario/<id>', methods=['PUT'])
def update_user(id):
    usuario = Usuario.query.filter_by(id=id).first()
    if usuario is None:
        return jsonify({'mensaje': 'El usuario no existe'}), 404

    json = request.get_json(force=True)
    if None in (json.get('nombre'),json.get('correo'),json.get('contrasena'),json.get('pais')):
        return jsonify({'message': 'Solicitud Incorrecta'}), 400

    usuario.nombre = json["nombre"]
    usuario.apellido = json["apellido"]
    usuario.correo = json["correo"]
    usuario.contraseña = json["contrasena"]
    usuario.pais = json["pais"]
    usuario.update()

    # TODO: Solo se considerarán updates con estos datos concretos, en una posterior iteracion se mejorará.


    return jsonify({'usuario': usuario.json() })


# TODO: AÑADIR ELIMINADA EN CASCADA

# DELETE
@app.route('/api/usuario/<id>', methods=['DELETE'])
def delete_user(id):
	usuario = Usuario.query.filter_by(id=id).first()
	if usuario is None:
		return jsonify({'mensaje': 'El usuario no existe'}), 404

	usuario.delete()

	return jsonify({'usuario': usuario.json() })


# --------------------------------------- PAIS -----------------------------------------------

# CREATE
@app.route('/api/pais', methods=['POST'])
def create_pais():
    json = request.get_json(force=True)

    # TODO: No permitir que se asigne id_pais mediante API, erlo automaticamente
    # SOLO se puede crear si la id ya no está ocupada
    if None in (json.get('cod_pais'), json.get('nombre')):
        return jsonify({'message': 'El formato está mal'}), 400


    pais = Pais.create(json['cod_pais'], json['nombre'])
    return jsonify({'pais': pais.json() })


# READ
@app.route('/api/pais', methods=['GET'])
def get_pais():
    paises = [ pais.json() for pais in Pais.query.all() ] 
    return jsonify({'paises': paises })


# UPDATE
@app.route('/api/pais/<id>', methods=['PUT'])
def uptade_pais(id):
    pais = Pais.query.filter_by(id=id).first()
    if pais is None:
        return jsonify({'mensaje': 'El pais no existe'}), 404

    json = request.get_json(force=True)
    if None in (json.get('nombre')):
        return jsonify({'mensaje': 'Solicitud Incorrecta'}), 400

    pais.nombre = json["nombre"]
    pais.update()

    return jsonify({'pais': pais.json() })



# TODO: ELIMINACION EN CASCADA

# DELETE
@app.route('/api/pais/<id>', methods=['DELETE'])
def delete_pais(cod_pais):
	pais = Pais.query.filter_by(cod_pais=cod_pais).first()
	if pais is None:
		return jsonify({'mensaje': 'El pais no existe'}), 404

	pais.delete()

	return jsonify({'pais': pais.json() })


# ---------------------------------------- MONEDA --------------------------------------------


# CREATE
@app.route('/api/moneda', methods=['POST'])
def create_moneda():
    json = request.get_json(force=True)

    # TODO: No permitir que se asigne id_moneda mediante API, si no hacerlo automaticamente
    if None in (json.get('sigla'), json.get('nombre')):
        return jsonify({'message': 'El formato está mal'}), 400


    moneda = Moneda.create(json['sigla'], json['nombre'])
    return jsonify({moneda.id:moneda.json()})




# READ
@app.route('/api/moneda', methods=['GET'])
def get_monedas():
    monedas = [ moneda.json() for moneda in Moneda.query.all() ] 
    return jsonify({'monedas': monedas })

# READ 1 USER
@app.route('/api/moneda/<id>', methods=['GET'])
def get_moneda(id):
    moneda = Moneda.query.filter_by(id=id).first()
    if moneda is None:
        return jsonify({'mensaje': 'El usuario no existe'}), 404
    return moneda.json()

# UPDATE
@app.route('/api/moneda/<id>', methods=['PUT'])
def update_moneda(id):
    moneda = Moneda.query.filter_by(id=id).first()
    if moneda is None:
        return jsonify({'mensaje': 'La moneda no existe'}), 404

    json = request.get_json(force=True)
    if None in (json.get('sigla'),json.get('nombre')):
        return jsonify({'mensaje': 'Solicitud Incorrecta'}), 400

    # TODO: en caso de una de las 2 entradas vacias dejarlo como estaba antes.

    print(json)

    moneda.sigla = json["sigla"]
    moneda.nombre = json["nombre"]
    moneda.update()

    return jsonify({'moneda': moneda.json() })




# TODO: ELIMINACION EN CASCADA

# DELETE
@app.route('/api/moneda/<id>', methods=['DELETE'])
def delete_moneda(id):
	moneda = Moneda.query.filter_by(id=id).first()
	if moneda is None:
		return jsonify({'mensaje': 'La moneda no existe'}), 404

	moneda.delete()

	return jsonify({'moneda': moneda.json() })

# ------------------------------------ CUENTA BANCARIA ---------------------------------------



# CREATE
@app.route('/api/cuenta_bancaria', methods=['POST'])
def create_cuenta_bancaria():
    json = request.get_json(force=True)

    # TODO: No permitir que se asigne id_moneda mediante API, si no hacerlo automaticamente
    if None in (json.get('numero_cuenta'), json.get('id_usuario'), json.get('balance')):
        return jsonify({'message': 'El formato está mal'}), 400


    cuenta_bancaria = CuentaBancaria.create(json['numero_cuenta'], json['id_usuario'], json['balance'])
    return jsonify({'cuenta_bancaria': cuenta_bancaria.json() })




# READ
@app.route('/api/cuenta_bancaria', methods=['GET'])
def get_cuenta_bancaria():
    cuentas_bancarias = [ cuenta_bancaria.json() for cuenta_bancaria in CuentaBancaria.query.all() ] 
    return jsonify({'cuentas_bancarias': cuentas_bancarias })



# UPDATE
@app.route('/api/cuenta_bancaria/<id>', methods=['PUT'])
def update_cuenta(numero_cuenta):
    cuenta_bancaria = CuentaBancaria.query.filter_by(numero_cuenta=numero_cuenta).first()
    if cuenta_bancaria is None:
        return jsonify({'mensaje': 'La cuenta bancaria no existe'}), 404

    json = request.get_json(force=True)
    # Se considera que lo unico cambiable en una cuenta es el balance.
    if None in (json.get('balance')):
        return jsonify({'mensaje': 'Solicitud Incorrecta'}), 400

    cuenta_bancaria.balance = json["balance"]
    cuenta_bancaria.update()

    return jsonify({'cuenta_bancaria': cuenta_bancaria.json() })




# DELETE
@app.route('/api/cuenta_bancaria/<id>', methods=['DELETE'])
def delete_cuenta_bancaria(id):
	cuenta_bancaria = CuentaBancaria.query.filter_by(id=id).first()
	if cuenta_bancaria is None:
		return jsonify({'mensaje': 'La cuenta bancaria no existe'}), 404

	cuenta_bancaria.delete()

	return jsonify({'cuenta_bancaria': cuenta_bancaria.json() })

# ------------------------------------- PRECIO MONEDA ----------------------------------------



# CREATE
@app.route('/api/precio_moneda', methods=['POST'])
def create_precio_moneda():
    json = request.get_json(force=True)

    if None in (json.get('id_moneda'), json.get('fecha'), json.get('valor')):
        return jsonify({'message': 'El formato está mal'}), 400


    precio_moneda = PrecioMoneda.create(json['id_moneda'], json['fecha'], json['valor'])
    return jsonify({'precio_moneda': precio_moneda.json() })


# READ
@app.route('/api/precio_moneda', methods=['GET'])
def get_precio_moneda():
    precios_monedas = [ precio_moneda.json() for precio_moneda in PrecioMoneda.query.all() ] 
    return jsonify({'precios_monedas': precios_monedas })


# UPDATE
@app.route('/api/precio_moneda/<id>', methods=['PUT'])
def update_precio_moneda(id_moneda):
    precio_moneda = PrecioMoneda.query.filter_by(id_moneda=id_moneda).first()
    if precio_moneda is None:
        return jsonify({'mensaje': 'El historial del precio de la moneda no existe'}), 404

    json = request.get_json(force=True)
    if None in (json.get('id_moneda'),json.get('fecha'),json.get('valor')):
        return jsonify({'mensaje': 'Solicitud Incorrecta'}), 400

    # Se considera el par id_moneda-fecha como el identificador efectivo de un registro, por lo que solo tiene sentido actualizar el valor de este.
    precio_moneda.valor = json["valor"]
    precio_moneda.update()

    return jsonify({'precio_moneda': precio_moneda.json() })



# DELETE
@app.route('/api/precio_moneda/<id>', methods=['DELETE'])
def delete_precio_moneda(id):
	precio_moneda = PrecioMoneda.query.filter_by(id=id).first()
	if precio_moneda is None:
		return jsonify({'mensaje': 'El precio de la moneda no existe'}), 404

	precio_moneda.delete()

	return jsonify({'precio_moneda': precio_moneda.json() })


# ------------------------------- USUARIO TIENE MONEDA ---------------------------------------





# CREATE
@app.route('/api/usuario_tiene_moneda', methods=['POST'])
def create_usuario_tiene_moneda():
    # solo se pueden agregar usuarios a una moneda solo si ya no tienen la misma moneda asociada.
    json = request.get_json(force=True)

    if None in (json.get('id_usuario'), json.get('id_moneda'), json.get('balance')):
        return jsonify({'message': 'El formato está mal'}), 400

    usuario_tiene_moneda = UsuarioTieneMoneda.create(json['id_usuario'], json['id_moneda'], json['balance'])
    return jsonify({'usuario_tiene_moneda': usuario_tiene_moneda.json() })



# READ
@app.route('/api/usuario_tiene_moneda', methods=['GET'])
def get_usuario_tiene_monedas():
    usuario_tiene_monedas = [ usuario_tiene_moneda.json() for usuario_tiene_moneda in UsuarioTieneMoneda.query.all() ] 
    return jsonify({'usuario_tiene_monedas': usuario_tiene_monedas })

@app.route('/api/usuario_tiene_moneda/<id>&<id2>', methods=['GET'])
def get_usuario_tiene_moneda(id, id2):
    utm = UsuarioTieneMoneda.query.filter_by(id_usuario=id,id_moneda=id2).first()
    if utm is None:
        return jsonify({'mensaje': 'El usuario no existe'}), 404
    return utm.json()


# UPDATE
@app.route('/api/usuario_tiene_moneda/<id>', methods=['PUT'])
def update_usuario_tiene_moneda(id_usuario):
    usuario_tiene_moneda = UsuarioTieneMoneda.query.filter_by(id_usuario=id_usuario).first()
    if usuario_tiene_moneda is None:
        return jsonify({'mensaje': 'El historial del precio de la moneda no existe'}), 404

    json = request.get_json(force=True)
    if None in (json.get('id_usuario'),json.get('id_moneda'),json.get('balance')):
        return jsonify({'mensaje': 'Solicitud Incorrecta'}), 400

    # Se considera el par id_usuario-id_moneda como el identificador efectivo de un registro, por lo que solo tiene sentido actualizar el balance de este.
    usuario_tiene_moneda.balance = json["balance"]
    usuario_tiene_moneda.update()

    return jsonify({'usuario_tiene_moneda': usuario_tiene_moneda.json() })


# DELETE
@app.route('/api/usuario_tiene_moneda/<id>', methods=['DELETE'])
def delete_usuario_tiene_moneda(id):
	usuario_tiene_moneda = UsuarioTieneMoneda.query.filter_by(id=id).first()
	if usuario_tiene_moneda is None:
		return jsonify({'mensaje': 'El usuario no existe'}), 404

	usuario_tiene_moneda.delete()

	return jsonify({'usuario_tiene_moneda': usuario_tiene_moneda.json() })
# --------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(port=4996)
