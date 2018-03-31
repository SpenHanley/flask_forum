from flask import current_app
from flask_login import current_user
from flask_nav import Nav
from flask_nav.elements import Navbar, View

def global_nav():
    return Navbar(
        current_app.config.get('SITE_NAME'),
        View('Home', 'home.homepage')
    )

def unauthenticated_nav():
    nav = list(global_nav().items)

    if current_user.is_anonymous:
        nav.extend([
            View('Login', 'security.login'),
            View('Register', 'security.register')
        ])
    
    return Navbar(current_app.config.get('SITE_NAME'), *nav)

def authenticated_nav():
    nav = list(global_nav().items)

    if current_user.is_authenticated and not current_user.has_role('admin'):
        nav.extend([
            View('Account', 'home.account'),
            View('Logout', 'security.logout')
        ])

    if current_user.has_role('admin'):
        nav.extend([
            View('Account', 'home.account'),
            View('Dashboard', 'admin.homepage'),
            View('Tickets', 'admin.tickets')
        ])

    return Navbar(current_app.config.get('SITE_NAME'), *nav)

def configure_nav(app):
    nav = Nav()
    nav.register_element('global_nav', global_nav)
    nav.register_element('authenticated_nav', authenticated_nav)
    nav.register_element('unauthenticated_nav', unauthenticated_nav)
    nav.init_app(app)
