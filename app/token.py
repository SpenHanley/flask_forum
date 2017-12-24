from itsdangerous import URLSafeTimedSerializer
from . import app
from .logger import logger

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    logger.info(app.config.get('SECURITY_PASSWORD_SALT'))
    return serializer.dumps(email, salt=app.config.get('SECURITY_PASSWORD_SALT'))

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False

    return email