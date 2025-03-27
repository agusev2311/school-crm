from flask import app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from celery import Celery

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
mail = Mail()
limiter = Limiter(
    get_remote_address,
    storage_uri="memory://",
)
celery = Celery(
    "school_crm_app",
    result_expires=600,
    include=["application.tasks"]  # Модуль с задачами
)
