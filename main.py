
from flask import Flask
from flask import jsonify
from sqlalchemy.orm import session
from sqlalchemy import func
from sqlalchemy import extract
from sqlalchemy import desc
from config import config
from models import CuentaBancaria, PrecioMoneda, UsuarioTieneMoneda, db
from models import Pais
from models import Usuario
from models import Moneda
from flask import request
from datetime import datetime
from datetime import timedelta
import re

# -------------------------------------- UTILES --------------------------------------------

pat = re.compile(r'\w{3}, \d{2} (\w{3}) \d{4} \d{2}:\d{2}:\d{2} GMT', re.MULTILINE)

# -------------------------------------- APP --------------------------------------------

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

    # SOLO se puede crear si la id ya no está ocupada
    if '' == json.get('nombre'):
        return jsonify({'message': 'El formato está mal'}), 400


    pais = Pais.create(json['nombre'])
    return jsonify({'pais': pais.json() })

# READ
@app.route('/api/pais', methods=['GET'])
def get_paises():
    paises = [ pais.json() for pais in Pais.query.all() ] 
    paises_return = dict()
    for pais in paises:
        paises_return[pais['cod_pais']] = pais
    return jsonify(paises_return)

    
# READ 1 PAIS
@app.route('/api/pais/<id>', methods=['GET'])
def get_pais(id):
    pais = Pais.query.filter_by(cod_pais=id).first()
    if pais is None:
        return jsonify({'mensaje': 'El pais no existe'}), 404
    return pais.json()

# UPDATE
@app.route('/api/pais/<cod_pais>', methods=['PUT'])
def uptade_pais(cod_pais):
    pais = Pais.query.filter_by(cod_pais=cod_pais).first()
    if pais is None:
        return jsonify({'mensaje': 'El pais no existe'}), 404

    json = request.get_json(force=True)
    if '' == json.get('nombre'):
        return jsonify({'mensaje': 'Solicitud Incorrecta'}), 400

    pais.nombre = json["nombre"]
    pais.update()

    return jsonify({'pais': pais.json() })



# DELETE
@app.route('/api/pais/<cod_pais>', methods=['DELETE'])
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
    if None in (json.get('sigla'), json.get('nombre')):
        return jsonify({'message': 'El formato está mal'}), 400


    moneda = Moneda.create(json['sigla'], json['nombre'])
    return jsonify({moneda.id: moneda.json() })




# READ
@app.route('/api/moneda', methods=['GET'])
def get_monedas():
    monedas = [ moneda.json() for moneda in Moneda.query.all() ] 
    monedas_return = dict()
    for moneda in monedas:
        monedas_return[moneda['id']] = moneda
    return jsonify(monedas_return)


# READ 1 MONEDA
@app.route('/api/moneda/<id>', methods=['GET'])
def get_moneda(id):
    moneda = Moneda.query.filter_by(id=id).first()
    if moneda is None:
        return jsonify({'mensaje': 'La moneda no existe'}), 404
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

    moneda.sigla = json["sigla"]
    moneda.nombre = json["nombre"]
    moneda.update()

    return jsonify({'moneda': moneda.json() })




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
    cuenta_bancaria = CuentaBancaria.create( json['id_usuario'], json['balance'])
    return jsonify({cuenta_bancaria.numero_cuenta: cuenta_bancaria.json() })




# READ
@app.route('/api/cuenta_bancaria', methods=['GET'])
def get_cuenta_bancarias():
    cuentas_bancarias = [ cuenta_bancaria.json() for cuenta_bancaria in CuentaBancaria.query.all() ] 
    cuentas_bancarias_return = dict()
    for cuenta_bancaria in cuentas_bancarias:
        cuentas_bancarias_return[cuenta_bancaria['numero_cuenta']] = cuenta_bancaria
    return jsonify(cuentas_bancarias_return)


# READ 1 Cuenta
@app.route('/api/cuenta_bancaria/<id>', methods=['GET'])
def get_cuenta_bancaria(id):
    cuenta_bancaria = CuentaBancaria.query.filter_by(numero_cuenta=id).first()
    if cuenta_bancaria is None:
        return jsonify({'mensaje': 'La cuenta bancaria no existe'}), 404
    return cuenta_bancaria.json()


# UPDATE
@app.route('/api/cuenta_bancaria/<numero_cuenta>', methods=['PUT'])
def update_cuenta(numero_cuenta):
    cuenta_bancaria = CuentaBancaria.query.filter_by(numero_cuenta=numero_cuenta).first()
    if cuenta_bancaria is None:
        return jsonify({'mensaje': 'La cuenta bancaria no existe'}), 404

    json = request.get_json(force=True)
    cuenta_bancaria.balance = json["balance"]
    cuenta_bancaria.update()

    return jsonify({'cuenta_bancaria': cuenta_bancaria.json() })




# DELETE
@app.route('/api/cuenta_bancaria/<numero_cuenta>', methods=['DELETE'])
def delete_cuenta_bancaria(numero_cuenta):
	cuenta_bancaria = CuentaBancaria.query.filter_by(numero_cuenta=numero_cuenta).first()
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
def get_precios_monedas():
    precios_monedas = [ precio_moneda.json() for precio_moneda in PrecioMoneda.query.all() ] 
    return jsonify({'precios_monedas': precios_monedas })

# READ valor asociado a fecha y moneda
@app.route('/api/precio_moneda/<fecha>/<id>', methods=['GET'])
def get_precio_moneda(fecha,id):
    # fecha_raw en formato "%a, %d %b %Y %H:%M:%S GMT"
    date_time_obj = datetime.strptime(fecha, '%a, %d %b %Y %H:%M:%S %Z')
    fecha_down = date_time_obj.strftime("%Y-%m-%d %H:%M:%S")
    fecha_up = date_time_obj + timedelta(0,1)
    fecha_up = fecha_up.strftime("%Y-%m-%d %H:%M:%S")
    precio_moneda = PrecioMoneda.query.filter(PrecioMoneda.id_moneda == id, PrecioMoneda.fecha >= fecha_down, PrecioMoneda.fecha < fecha_up ).first()
    if precio_moneda is None:
        return jsonify({'mensaje': 'La fecha de moneda no existe'}), 404
    return precio_moneda.json()

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
@app.route('/api/precio_moneda/<fecha>/<id>', methods=['DELETE'])
def delete_precio_moneda(fecha,id):
    # fecha_raw en formato "%a, %d %b %Y %H:%M:%S GMT"
    date_time_obj = datetime.strptime(fecha, '%a, %d %b %Y %H:%M:%S %Z')
    fecha_down = date_time_obj.strftime("%Y-%m-%d %H:%M:%S")
    fecha_up = date_time_obj + timedelta(0,1)
    fecha_up = fecha_up.strftime("%Y-%m-%d %H:%M:%S")
    precio_moneda = PrecioMoneda.query.filter(PrecioMoneda.id_moneda == id, PrecioMoneda.fecha >= fecha_down, PrecioMoneda.fecha < fecha_up ).first()
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
    if not usuario_tiene_moneda:
        return jsonify({'message': 'Esta creado'}), 400
    
    return jsonify({'usuario_tiene_moneda': usuario_tiene_moneda.json() })



# READ
@app.route('/api/usuario_tiene_moneda', methods=['GET'])
def get_usuarios_tiene_monedas():
    usuario_tiene_monedas = [ usuario_tiene_moneda.json() for usuario_tiene_moneda in UsuarioTieneMoneda.query.all() ] 
    return jsonify({'usuario_tiene_monedas': usuario_tiene_monedas })


# READ valor asociado a id_usuario e id_moneda
@app.route('/api/usuario_tiene_moneda/<id_user>/<id_moneda>', methods=['GET'])
def get_usuario_tiene_moneda(id_user,id_moneda):

    usuario_tiene_moneda = UsuarioTieneMoneda.query.filter_by(id_usuario = id_user, id_moneda = id_moneda).first()
    if usuario_tiene_moneda is None:
        return jsonify({'mensaje': 'No existe un usuario asociado a tal cuenta'}), 404
    return usuario_tiene_moneda.json()


"""@app.route('/api/moneda/<id>', methods=['PUT'])
def update_moneda(id):
    moneda = Moneda.query.filter_by(id=id).first()
    if moneda is None:
        return jsonify({'mensaje': 'La moneda no existe'}), 404

    json = request.get_json(force=True)
    if None in (json.get('sigla'),json.get('nombre')):
        return jsonify({'mensaje': 'Solicitud Incorrecta'}), 400

    moneda.sigla = json["sigla"]
    moneda.nombre = json["nombre"]
    moneda.update()

    return jsonify({'moneda': moneda.json() })"""

# UPDATE
@app.route('/api/usuario_tiene_moneda/<id_user>/<id_moneda>', methods=['PUT'])
def update_usuario_tiene_moneda(id_user,id_moneda):
    
    usuario_tiene_moneda = UsuarioTieneMoneda.query.filter_by(id_usuario=id_user, id_moneda=id_moneda).first()
    if usuario_tiene_moneda is None:
        return jsonify({'mensaje': 'El historial del precio de la moneda no existe'}), 404

    json = request.get_json(force=True)
    
    # Se considera el par id_usuario-id_moneda como el identificador efectivo de un registro, por lo que solo tiene sentido actualizar el balance de este.
    usuario_tiene_moneda.balance = json["balance"]
    usuario_tiene_moneda.update()

    return jsonify({usuario_tiene_moneda.id_usuario: usuario_tiene_moneda.json() })


# DELETE
@app.route('/api/usuario_tiene_moneda/<id_user>/<id_moneda>', methods=['DELETE'])
def delete_usuario_tiene_moneda(id_user,id_moneda):
	usuario_tiene_moneda = UsuarioTieneMoneda.query.filter_by(id_usuario=id_user,id_moneda=id_moneda).first()
	if usuario_tiene_moneda is None:
		return jsonify({'mensaje': 'El usuario no existe'}), 404

	usuario_tiene_moneda.delete()

	return jsonify({'usuario_tiene_moneda': usuario_tiene_moneda.json() })

# --------------------------------------------------------------------------------------------

#                                IMPLEMENTACION CONSULTAS SOLICITADAS

# --------------------------------------------------------------------------------------------

base_cons_dir = '/api/consultas/'

@app.route(base_cons_dir+'1/<year>', methods=['GET'])
def get_user_by_year(year):
    # Año en formato %Y (4 digitos)
    date_time_obj = datetime.strptime(year.zfill(4), '%Y') # String to datetime object
    base_year_string = date_time_obj.strftime("%Y-%m-%d %H:%M:%S") # Formatear como año-00-00 00:00:00
    next_year_obj = date_time_obj + timedelta(365) # Sumar 1 año al año dado
    next_year_string = next_year_obj.strftime("%Y-%m-%d %H:%M:%S") # Formatear como año+1-00-00 00:00:00

    users_filtered = Usuario.query.filter(Usuario.fecha_registro >= base_year_string, Usuario.fecha_registro < next_year_string)

    usuarios = [ usuario.json() for usuario in users_filtered ] 

    if len(usuarios) == 0:
        return jsonify({'message': 'No se han encontrado usuarios para el año ingresado'}), 400

    return jsonify(usuarios), 200

    
@app.route(base_cons_dir+'2/<balance>', methods=['GET'])
def get_accounts_by_balance(balance):

    accounts_filtered = CuentaBancaria.query.filter(CuentaBancaria.balance >= float(balance))

    cuentabancaria = [ CuentaBancaria.json() for CuentaBancaria in accounts_filtered ] 
    if len(cuentabancaria) == 0:
        return jsonify({'message': 'No se han encontrado cuentas a ingresar.'}), 400

    return jsonify(cuentabancaria), 200


@app.route(base_cons_dir+'3/<country>', methods=['GET'])
def get_user_by_country(country):
    users_filtered = Usuario.query.filter(Usuario.pais == int(country))
    pais = Pais.query.filter(Pais.cod_pais == int(country)).first()

    respuesta = {"usuarios":[ usuario.json() for usuario in users_filtered ], "pais":pais.nombre}
    if len(respuesta["usuarios"]) == 0:
        return jsonify({'message': 'No se han encontrado usuarios para el año ingresado.'}), 400
    if len(respuesta["pais"]) == 0:
        return jsonify({'message': 'No se ha encontrado el nombre del pais solicitado.'}), 400

    return jsonify(respuesta)



@app.route(base_cons_dir+'4/<id_moneda>', methods=['GET'])
def get_max_by_coin(id_moneda):
    result = PrecioMoneda.query.filter(PrecioMoneda.id_moneda == id_moneda).order_by(desc(PrecioMoneda.valor)).limit(1)
    resultados = [ preciomoneda.json() for preciomoneda in result ] 

    if len(resultados) == 0:
        return jsonify({'message': 'No se han encontrado valores para la id_moneda dado.'}), 400

    return jsonify(resultados), 200


@app.route(base_cons_dir+'5/<id>', methods=['GET'])
def get_total_moneda(id):
    resultados = UsuarioTieneMoneda.query.with_entities(
             func.sum(UsuarioTieneMoneda.balance).label("Suma")
         ).filter_by(
             id_moneda=id
         ).first()
    print(resultados[0])
    if (resultados[0] == None) :
        return {'message': 'No hay monedas que sumar.'}
    return {'Suma': resultados[0]},200



@app.route(base_cons_dir+'6/', methods=['GET'])
def get_monedas_top():

    monedas = [moneda.json() for moneda in Moneda.query.all()]
    contados = []
    for m in monedas:
        contados.append((UsuarioTieneMoneda.query.filter(UsuarioTieneMoneda.id_moneda == m["id"]).count(),m["nombre"],m["sigla"],m["id"]))
    contados.sort(reverse=True)

    if len(contados) == 0:
        return jsonify({'message': 'No se han encontrado monedas a ingresar.'}), 400

    return jsonify(contados[:3]), 200
    

@app.route(base_cons_dir+'7/<mes>', methods=['GET'])
def get_monedas_change_top(mes):
    monedas = [moneda.json() for moneda in Moneda.query.all()]
    contados = []
    for m in monedas:
        cambios = PrecioMoneda.query.filter(PrecioMoneda.id_moneda == m["id"], extract('month', PrecioMoneda.fecha) == datetime(year=1999,month=int(mes), day=12).month).count()
        contados.append((cambios,m["id"],m["nombre"],m["sigla"]))
    if len(contados) == 0:
        return jsonify({'message': 'No se han encontrado monedas a ingresar.'}), 400
    contados.sort(reverse=True)
    return jsonify(contados[0]), 200


@app.route(base_cons_dir+'8/<user_id>', methods=['GET'])
def get_max_money_by_user(user_id):
    
    users_filtered = UsuarioTieneMoneda.query.filter(UsuarioTieneMoneda.id_usuario == user_id).order_by(desc(UsuarioTieneMoneda.balance)).limit(1)

    valores = [ usuario.json() for usuario in users_filtered ] 

    if len(valores) == 0:
        return jsonify({'message': 'No se han encontrado monedas par el usuario dado.'}), 400

    return jsonify(valores), 200










    




if __name__ == '__main__':
    app.run(port=4996)
