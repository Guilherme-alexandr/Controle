from flask import Flask, redirect, url_for
from produtos import produtos_bp
from usuarios import usuarios_bp
from cliente import cliente_bp

app = Flask(__name__)

app.register_blueprint(produtos_bp, url_prefix='/produtos')
app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
app.register_blueprint(cliente_bp, url_prefix='/cliente')
app.secret_key = 'cyber_key_segurity'

@app.route('/')
def index():
    return redirect(url_for('usuarios.index'))

if __name__ == '__main__':
    app.run(debug=True)
