from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt  # PyJWT
import datetime
# Importa seus modelos do arquivo anterior
from models import Usuario, Log, Base

# Configuração simples para exemplo de Back-end
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'  # Essencial para JWT

#  SIGN-UP (Cadastro com Criptografia)


@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        # Validação de campos obrigatórios
        if not data or not data.get('email') or not data.get('senha'):
            return jsonify({"mensagem": "Email e senha são obrigatórios"}), 400

        # Criptografia de senha obrigatória para LGPD
        hashed_password = generate_password_hash(
            data['senha'], method='pbkdf2:sha256')

        novo_usuario = Usuario(
            email=data['email'],
            senha_hash=hashed_password,
            perfil=data.get('perfil', 'Paciente')
        )

        # Aqui entraria a lógica de salvar no banco (ex: db.session.add(novo_usuario))

        return jsonify({"mensagem": "Usuário criado com sucesso e senha criptografada!"}), 201
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao criar usuário: {str(e)}"}), 500

#  LOGIN (Autenticação e Geração de Token)


@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        auth = request.get_json()

        if not auth or not auth.get('email') or not auth.get('senha'):
            return jsonify({"mensagem": "Credenciais ausentes"}), 401

        # Simulação de busca no banco pelo email
        # usuario = Usuario.query.filter_by(email=auth.get('email')).first()

        # Exemplo de verificação de senha criptografada
        # if check_password_hash(usuario.senha_hash, auth.get('senha')):

        # Se válido, gera o Token JWT conforme o FAQ
        token = jwt.encode({
            'user_id': "id_do_usuario",
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token}), 200
    except Exception as e:
        return jsonify({"mensagem": f"Erro na autenticação: {str(e)}"}), 500
