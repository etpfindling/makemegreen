""" credentials """
from flask_login import login_user

from models.api_errors import ApiErrors
from models.base_object import BaseObject
from models.user import User

from flask import current_app as app


def get_user_with_credentials(identifier, password):
    errors = ApiErrors()
    errors.status_code = 401

    if identifier is None:
        errors.addError('identifier', 'Identifiant manquant')
    if password is None:
        errors.addError('password', 'Mot de passe manquant')
    errors.maybeRaise()

    user = User.query.filter_by(email=identifier).first()

    if not user:
        errors.addError('identifier', 'Identifiant incorrect')
        raise errors
    if not user.checkPassword(password):
        errors.addError('password', 'Mot de passe incorrect')
        raise errors

    login_user(user, remember=True)
    return user


def change_password(user, password):
    if type(user) != User:
        user = User.query.filter_by(email=user).one()
    user.setPassword(password)
    user = session.merge(user)
    BaseObject.check_and_save(user)
