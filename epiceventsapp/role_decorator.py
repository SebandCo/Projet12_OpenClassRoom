from functools import wraps
from flask import session, render_template, redirect, url_for


# Decorateur pour bloquer completement une page aux roles définies
def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if session.get('user_role') not in roles:
                message = "No Authorisation : Vous n'avez pas les droits nécessaires pour accéder à cette page."
                return render_template("home.html", message=message)
            return f(*args, **kwargs)
        return wrapped
    return wrapper


# Redirige l'utilisateur vers la page de connexion si il n'est pas connecté
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_role' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
