from flask import Flask, request, jsonify
from datetime import datetime
from models import Paciente, Consulta, Prontuario, Log, Usuario, Medico
# from database import db  # sua sessão SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

# =========================================================
# FUNÇÃO AUXILIAR DE LOG (LGPD)
# =========================================================

def registrar_log(usuario_id, acao):
    novo_log = Log(
        usuario_id=usuario_id,
        acao=acao,
        data_hora=datetime.now(timezone.utc)
    )
    print(f"LOG: Usuário {usuario_id} - Ação: {acao}")
    # db.session.add(novo_log)
    # db.session.commit()

# =========================================================
# POST /api/pacientes
# Cadastro de paciente
# =========================================================

@app.route('/api/pacientes', methods=['POST'])
def cadastrar_paciente():
    data = request.get_json()

    nome = data.get('nome')
    cpf = data.get('cpf')
    usuario_id = data.get('usuario_id')  # quem está executando a ação

    if not nome or not cpf or not usuario_id:
        return jsonify({"erro": "Nome, CPF e usuário são obrigatórios"}), 400

    # Verifica CPF duplicado
    # if Paciente.query.filter_by(cpf=cpf).first():
    #    return jsonify({"erro": "CPF já cadastrado"}), 409

    novo_paciente = Paciente(
        nome=nome,
        cpf=cpf
    )

    # db.session.add(novo_paciente)
    # db.session.commit()

    registrar_log(
        usuario_id=usuario_id,
        acao=f"Cadastrou paciente CPF {cpf}"
    )

    return jsonify({
        "mensagem": "Paciente cadastrado com sucesso"
    }), 201

# =========================================================
# GET /api/consultas
# Listagem de consultas
# =========================================================

@app.route('/api/consultas', methods=['GET'])
def listar_consultas():
    
    exemplo_consultas = [
        {"id": 1, "paciente": "João Silva", "data": "2025-10-20 14:00", "tipo": "Telemedicina"},
        {"id": 2, "paciente": "Maria Souza", "data": "2025-10-20 15:30", "tipo": "Presencial"}
    ]
    return jsonify(exemplo_consultas), 200


# =========================================================
# POST /api/consultas
# Criar consulta
# =========================================================

@app.route('/api/consultas', methods=['POST'])
def criar_consulta():
    data = request.get_json()

    paciente_id = data.get('paciente_id')
    medico_id = data.get('medico_id')
    data_hora = data.get('data_hora')
    usuario_id = data.get('usuario_id')

    if not paciente_id or not medico_id or not data_hora or not usuario_id:
        return jsonify({"erro": "Dados incompletos"}), 400

    # Verifica integridade
    if not Paciente.query.get(paciente_id):
        return jsonify({"erro": "Paciente não encontrado"}), 404

    if not Medico.query.get(medico_id):
        return jsonify({"erro": "Médico não encontrado"}), 404

    nova_consulta = Consulta(
        paciente_id=paciente_id,
        medico_id=medico_id,
        data_hora=datetime.fromisoformat(data_hora)
    )

    # db.session.add(nova_consulta)
    # db.session.commit()

    registrar_log(
        usuario_id=usuario_id,
        acao=f"Criou consulta para paciente {paciente_id} com médico {medico_id}"
    )

    return jsonify({"mensagem": "Consulta criada com sucesso"}), 201

# =========================================================
# POST /api/prontuarios
# Registro de prontuário
# =========================================================

@app.route('/api/prontuarios', methods=['POST'])
def registrar_prontuario():
    data = request.get_json()

    consulta_id = data.get('consulta_id')
    descricao = data.get('descricao')
    prescricao = data.get('prescricao')
    usuario_id = data.get('usuario_id')  # médico logado

    if not consulta_id or not descricao or not usuario_id:
        return jsonify({"erro": "Dados obrigatórios ausentes"}), 400

    consulta = Consulta.query.get(consulta_id)
    if not consulta:
        return jsonify({"erro": "Consulta não encontrada"}), 404

    # Relação 1:1 — impede duplicação
    if Prontuario.query.filter_by(consulta_id=consulta_id).first():
        return jsonify({"erro": "Prontuário já registrado para esta consulta"}), 409

    novo_prontuario = Prontuario(
        consulta_id=consulta_id,
        descricao=descricao,
        prescricao=prescricao
    )

    # db.session.add(novo_prontuario)
    # db.session.commit()

    registrar_log(
        usuario_id=usuario_id,
        acao=f"Registrou prontuário da consulta {consulta_id}"
    )

    return jsonify({"mensagem": "Prontuário registrado com sucesso"}), 201

# =========================================================

if __name__ == "__main__":
    app.run(debug=True)
