from flask import Flask, request, jsonify
from main import main
from datetime import datetime

app = Flask(__name__)

@app.route("/bot")
def bot():
    dataStr = request.args.get('data')
    data = datetime.strptime(dataStr, "%d/%m/%Y")
    success = main(data)
    return jsonify({"sucess": success}), 200

if __name__ == "__main__":
    app.run()