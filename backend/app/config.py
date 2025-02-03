import os

class Config:
    SECRET_KEY = 'superclaveultrasecreta'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'claveultrasecreta_jwt'  # Llave para firmar los tokens

