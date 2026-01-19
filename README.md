# SGHSS - VidaPlus | Back-end & Segurança

🏥 Sobre o Projeto

Este repositório contém a infraestrutura de Back-end do VidaPlus, um Sistema de Gestão Hospitalar desenvolvido para modernizar o atendimento clínico e a telemedicina. O foco central deste desenvolvimento foi a criação de uma API robusta, capaz de gerenciar dados sensíveis com alta integridade e em total conformidade com a LGPD.

🛠️ Tecnologias Utilizadas

    Linguagem: Python 3.12.

    Framework: Flask (API RESTful).

    Persistência: SQLAlchemy ORM.

    Segurança: Werkzeug (Hashing de senhas) e JWT (Autenticação).

🌟 Funcionalidades Principais

    Gestão de Pacientes: Cadastro estruturado de dados pessoais e clínicos.

    Agendamento Inteligente: API para listagem e controle de agendas médicas.

    Prontuário Digital: Registro de históricos e emissão de receitas digitais.

    Auditoria (LGPD): Sistema automatizado de Logs de Auditoria que registra cada ação crítica dos usuários, garantindo a rastreabilidade completa dos dados.

🚀 Como executar

    Clone o repositório: git clone https://github.com/seu-usuario/SGHSS-VidaPlus.git

    Instale as dependências: pip install -r requirements.txt

    Inicie o servidor: python src/routes.py
