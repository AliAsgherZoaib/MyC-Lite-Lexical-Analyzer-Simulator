from flask import render_template, request, jsonify
from lexer import MyCLiteLexer

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/analyze', methods=['POST'])
    def analyze_code():
        data = request.get_json() or {}
        code = data.get("code", "")
        
        lexer = MyCLiteLexer(code)
        results = lexer.analyze()
        
        return jsonify(results)