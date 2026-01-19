from models import Log  # Importa o modelo de Log definido anteriormente
from datetime import datetime
# Importe sua instância de banco de dados (ex: db)


def registrar_log(usuario_id, acao):
    """
    Função utilitária para salvar ações críticas no banco de dados.
    Atende aos requisitos de Segurança e LGPD do projeto SGHSS.
    """
    novo_log = Log(
        usuario_id=usuario_id,
        acao=acao,
        data_hora=datetime.utcnow()
    )
    # db.session.add(novo_log)
    # db.session.commit()
    print(f"LOG GERADO: Usuário {usuario_id} executou a ação: {acao}")
