import os
from flask import Flask, redirect, url_for
from database.models import db, UserAccount

def build_application():
    
    # Configures SQLAlchemy, registers controller Blueprints, and establishes root navigation.
    
    app = Flask(__name__, template_folder='templates', static_folder='static')

    base_directory = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(base_directory, 'epsilon_system.sqlite3')}"
    app.config['SECRET_KEY'] = 'epsilon_alpine_secret_key_2026'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from controllers.client_controller import client_controller
    from controllers.guide_controller import guide_controller
    from controllers.manager_controller import manager_controller

    # imports routes from controllers files 

    app.register_blueprint(client_controller)
    app.register_blueprint(guide_controller)
    app.register_blueprint(manager_controller)

    @app.route('/')
    def default_redirect():
        return redirect('/portal/login')

    # Convenience compatibility redirects for users familiar with earlier versions

    @app.route('/client/login')
    def compat_login():
        return redirect('/portal/login')

    @app.route('/guide/dash')
    def compat_guide():
        return redirect('/staff/dashboard')

    @app.route('/manager/dash')
    def compat_manager():
        return redirect('/admin/dashboard')

    return app


if __name__ == '__main__':
    app = build_application()
    with app.app_context():
         
        db.create_all()   #inititates the database 

        # Ensure default manager/admin superuser exists
        if not UserAccount.query.filter_by(username='manager').first():
            default_mgr = UserAccount(
                username='manager',
                user_role='manager',
                is_verified=True,
                is_enabled=True
            )
            default_mgr.set_password('manager')
            db.session.add(default_mgr)
            db.session.commit()

    print("==========================================================")
    print("  PROJECT EPSILON 3 — TREKKING & EXPEDITION PLATFORM      ")
    print("  Active on http://127.0.0.1:8113                         ")
    print("==========================================================")
    app.run(debug=True, port=8113)
