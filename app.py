from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

# Przykładowe dane firm (Mock Data) do testowania swipowania
MOCK_COMPANIES = [
    {"id": 1, "name": "CodeWizards SH", "desc": "Specjaliści od Python & AI.", "img": "https://source.unsplash.com/random/400x500/?developer"},
    {"id": 2, "name": "Creative Studio", "desc": "Branding i UI/UX na najwyższym poziomie.", "img": "https://source.unsplash.com/random/400x500/?design"},
    {"id": 3, "name": "Marketing Ninjas", "desc": "Zwiększymy Twoją sprzedaż B2B o 200%.", "img": "https://source.unsplash.com/random/400x500/?office"},
    {"id": 4, "name": "Cloud Solutions", "desc": "Migracja do chmury i DevOps.", "img": "https://source.unsplash.com/random/400x500/?server"},
    {"id": 5, "name": "Legal Eagles", "desc": "Obsługa prawna startupów.", "img": "https://source.unsplash.com/random/400x500/?lawyer"},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == 'admin' and data.get('password') == 'admin':
        return jsonify({'success': True, 'redirect': url_for('dashboard')})
    return jsonify({'success': False, 'message': 'Błędne dane'})

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/companies')
def get_companies():
    # Zwraca listę firm do swipowania
    return jsonify(MOCK_COMPANIES)

if __name__ == '__main__':
    app.run(debug=True, port=5000)