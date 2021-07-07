class Config:
	pass

class DevelopmentConfig(Config):
	DEBUG = True
	# Ingresamos credenciales para conexión a base de datos
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:2453@localhost:5432/Tarea2'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
	'development': DevelopmentConfig,
}
