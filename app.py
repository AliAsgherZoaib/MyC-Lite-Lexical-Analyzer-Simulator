from flask import Flask
from routes import init_routes

app = Flask(__name__)
init_routes(app)

if __name__ == '__main__':
    # Running in debug mode for development flexibility
    app.run(debug=True, port=5000)