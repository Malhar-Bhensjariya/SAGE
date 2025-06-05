from flask import Flask
from flask_cors import CORS
from config.settings import Config
from db.db_init import init_db

# Import Blueprints
from core.routes.user_routes import user_bp
from core.routes.task_routes import task_bp
from core.routes.document_routes import document_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Initialize DB
    init_db(app)

    # Register Blueprints
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(task_bp, url_prefix='/api/task')
    app.register_blueprint(document_bp, url_prefix='/api/document')

    @app.route('/ping')
    def ping():
        return {'status': 'pong'}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
