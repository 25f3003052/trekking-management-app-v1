class DevelopmentConfig():
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Treck.db'
    SECRET_KEY="secret123"
    SECURITY_PASSWORD_HASH='bcrypt'
    SECURITY_PASSWORD_SALT='tree'