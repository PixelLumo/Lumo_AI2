def create_app():
    try:
        from flask import Flask
    except Exception as e:  # pragma: no cover - runtime env issue
        raise ImportError(
            "Flask is required to create the app. Activate the virtualenv or install dependencies: `pip install -r requirements.txt`"
        ) from e

    app = Flask(__name__)

    # Import and register routes
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
