from flask import Flask, jsonify, request

app = Flask(__name__)

# Przykładowe API do logowania
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == 'admin' and data.get('password') == 'admin':
        # W prawdziwej apce tutaj zwracałbyś token JWT
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Błędne dane'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)