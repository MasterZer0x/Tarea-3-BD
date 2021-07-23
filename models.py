from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.sql.schema import ForeignKey

db = SQLAlchemy()




# -------------------------------------- USUARIOS --------------------------------------------



class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50))
    correo = db.Column(db.String(50), nullable=False)
    contraseña = db.Column(db.String(150), nullable=False)
    pais = db.Column(db.Integer, db.ForeignKey("pais.cod_pais"), nullable=False) # TODO: relacionar con la tabla pais
    fecha_registro = db.Column(db.DateTime(), nullable=False)
    
    cuentas_bancarias = db.relationship('CuentaBancaria', cascade="delete", lazy='dynamic')
    usuario_monedas = db.relationship('UsuarioTieneMoneda', cascade="delete", lazy='dynamic')

    @classmethod
    def create(cls, nombre, apellido, correo, contraseña, pais):
        res = db.session.query(func.max(Usuario.id).label('id')).one()
        nid=res[0]+1
        now = datetime.now()
        fecha = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

        user = Usuario(id=nid,nombre=nombre,apellido=apellido,correo=correo,contraseña=contraseña,pais=pais,fecha_registro=fecha)
        temp = user.save()
        print(temp)
        return user

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False

    def json(self):
        return {
        'id': self.id,
	    'nombre': self.nombre,
	    'apellido': self.apellido,
        'correo': self.correo,
        'contrasena': self.contraseña,
        'pais': self.pais,
        'fecha_registro': self.fecha_registro
		}


    def update(self):
	    self.save()

    def delete(self):
	    try:
	        db.session.delete(self)
	        db.session.commit()

	        return True
	    except:
	        return False





# --------------------------------------- PAIS -----------------------------------------------


# Se considera que la inexistencia de un pais no provocará la eliminacion de una cuenta, si no, estas simplemente se quedaran con un parametro "invalido"
class Pais(db.Model):
    __tablename__ = 'pais'
    cod_pais = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)

    @classmethod
    def create(cls, cod_pais, nombre):
        pais = Pais(cod_pais=cod_pais, nombre=nombre)
        return pais.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False

    def json(self):
        return {
            'cod_pais': self.cod_pais,
            'nombre': self.nombre
		}

    def update(self):
        self.save()
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()

            return True
        except:
            return False


# ---------------------------------------- MONEDA --------------------------------------------

class Moneda(db.Model):
    __tablename__ = "moneda"
    id = db.Column(db.Integer, primary_key=True)
    sigla = db.Column(db.String(10), nullable=False)
    nombre = db.Column(db.String(80), nullable=False)

    precio_relation = db.relationship('PrecioMoneda', cascade="all,delete", lazy='dynamic')
    usuario_monedas = db.relationship('UsuarioTieneMoneda', cascade="all,delete", lazy='dynamic')

    @classmethod
    def create(cls, id, sigla, nombre):
        res = db.session.query(func.max(Moneda.id).label('id')).one()
        nid=res[0]+1
        moneda = Moneda(id=nid, sigla=sigla, nombre=nombre)
        temp = moneda.save()
        print(temp)
        return moneda

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False

    def json(self):
        return {
        'id': self.id,
	    'sigla': self.sigla,
	    'nombre': self.nombre
		}


    def update(self):
	    self.save()

    def delete(self):
	    try:
	        db.session.delete(self)
	        db.session.commit()

	        return True
	    except:
	        return False




# ------------------------------------ CUENTA BANCARIA ---------------------------------------


class CuentaBancaria(db.Model):
    __tablename__ = "cuenta_bancaria"
    numero_cuenta = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer,  db.ForeignKey("usuario.id"), nullable=False) # TODO: Relacionar con tabla Usuario
    balance = db.Column(db.Float, nullable=False)



    @classmethod
    def create(cls, numero_cuenta, id_usuario, balance):
        cuentabancaria = CuentaBancaria(numero_cuenta=numero_cuenta, id_usuario=id_usuario , balance=balance)
        return cuentabancaria.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False

    def json(self):
        return {
        'numero_cuenta': self.numero_cuenta,
	    'id_usuario': self.id_usuario,
	    'balance': self.balance
		}


    def update(self):
	    self.save()

    def delete(self):
	    try:
	        db.session.delete(self)
	        db.session.commit()

	        return True
	    except:
	        return False



# ------------------------------------- PRECIO MONEDA ----------------------------------------


class PrecioMoneda(db.Model):
    __tablename__ = "precio_moneda"
    id_moneda = db.Column(db.Integer, db.ForeignKey("moneda.id"), primary_key=True, nullable=False)
    fecha = db.Column(db.DateTime(), primary_key=True, nullable=False)
    valor = db.Column(db.Float, nullable=False)

    @classmethod
    def create(cls, id_moneda, fecha, valor):
        preciomoneda = PrecioMoneda(id_moneda=id_moneda, fecha=fecha, valor=valor)
        return preciomoneda.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False

    def json(self):
        return {
        'id_moneda': self.id_moneda,
	    'fecha': self.fecha,
	    'valor': self.valor
		}


    def update(self):
	    self.save()

    def delete(self):
	    try:
	        db.session.delete(self)
	        db.session.commit()

	        return True
	    except:
	        return False




# ------------------------------- USUARIO TIENE MONEDA ---------------------------------------



class UsuarioTieneMoneda(db.Model):
    __tablename__ = "usuario_tiene_moneda"
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), primary_key=True, nullable=False) # TODO: relacionar con tabla USUARIO
    id_moneda = db.Column(db.Integer, db.ForeignKey("moneda.id"), primary_key=True, nullable=False) # TODO: relacionar con tabla MONEDA
    balance = db.Column(db.Float, nullable=False)

    @classmethod
    def create(cls, id_usuario, id_moneda, balance):
        usuariotienemoneda = UsuarioTieneMoneda(id_usuario=id_usuario, id_moneda=id_moneda, balance=balance)
        return usuariotienemoneda.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False

    def json(self):
        return {
	    'id_usuario': self.id_usuario,
        'id_moneda': self.id_moneda,
	    'balance': self.balance
		}


    def update(self):
	    self.save()

    def delete(self):
	    try:
	        db.session.delete(self)
	        db.session.commit()

	        return True
	    except:
	        return False











