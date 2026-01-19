from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    # UNIQUE conforme o diagrama para garantir login único [cite: 344]
    email = Column(String(100), unique=True, nullable=False)
    # Armazenamento de hash para segurança LGPD [cite: 38, 320]
    senha_hash = Column(String(255), nullable=False)
    perfil = Column(String(20)) # Paciente, Medico ou Admin

    # Relacionamentos 1:1 e 1:N conforme o DER
    paciente = relationship("Paciente", back_populates="usuario", uselist=False)
    medico = relationship("Medico", back_populates="usuario", uselist=False)
    logs = relationship("Log", back_populates="usuario")

class Paciente(Base):
    __tablename__ = 'pacientes'
    
    id = Column(Integer, primary_key=True)
    # FK ligada à PK de Usuarios (1:1 no DER)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), unique=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), nullable=False, unique=True)
    
    usuario = relationship("Usuario", back_populates="paciente")
    consultas = relationship("Consulta", back_populates="paciente")

class Medico(Base):
    __tablename__ = 'medicos'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), unique=True)
    crm = Column(String(20), nullable=False)
    
    usuario = relationship("Usuario", back_populates="medico")
    consultas = relationship("Consulta", back_populates="medico")

class Consulta(Base):
    __tablename__ = 'consultas'
    
    id = Column(Integer, primary_key=True)
    # FKs que representam o relacionamento (1:N) do diagrama
    paciente_id = Column(Integer, ForeignKey('pacientes.id'))
    medico_id = Column(Integer, ForeignKey('medicos.id'))
    data_hora = Column(DateTime, nullable=False)
    
    paciente = relationship("Paciente", back_populates="consultas")
    medico = relationship("Medico", back_populates="consultas")
    prontuario = relationship("Prontuario", back_populates="consulta", uselist=False)

class Prontuario(Base):
    __tablename__ = 'prontuarios'
    
    id = Column(Integer, primary_key=True)
    consulta_id = Column(Integer, ForeignKey('consultas.id'), unique=True)
    descricao = Column(Text)
    # Atende o requisito de Receita Digital [cite: 32, 36]
    prescricao = Column(Text)
    
    consulta = relationship("Consulta", back_populates="prontuario")

class Log(Base):
    __tablename__ = 'logs'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    acao = Column(String(255), nullable=False)
    # Timestamp automático para auditoria LGPD [cite: 33, 38]
    data_hora = Column(DateTime, default=datetime.datetime.utcnow)
    
    usuario = relationship("Usuario", back_populates="logs")