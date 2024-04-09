from flask import Flask, request, jsonify
from flask_cors import CORS

from main import main, main_mensal
from datetime import datetime

app = Flask(__name__)

def make_response(success):
    response = jsonify({'success': success})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')  # Permitir apenas de localhost:3000
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route("/bot")
def bot():
    dataStr = request.args.get('data')
    data = datetime.strptime(dataStr, "%d/%m/%Y")
    success = main(data)
    return make_response(success)



@app.route("/bot/mensal")
def bot_mensal():
    ano = int(request.args.get('ano'))
    mes = int(request.args.get('mes'))
    success = main_mensal(ano,mes)
    return make_response(success)

if __name__ == "__main__":
    app.run()
    cors = CORS(app, resources={r"/bot": {"origins": "http://localhost:3000"}})