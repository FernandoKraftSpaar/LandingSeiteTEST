from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from datetime import datetime

equipamentos_bp = Blueprint('equipamentos', __name__)

db = SQLAlchemy()

class Equipamento(db.Model):
    __tablename__ = 'equipamentos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    potencia = db.Column(db.Float, nullable=False)
    horas_uso = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50))
    observacoes = db.Column(db.String(255))
    idade = db.Column(db.Integer)
    etiqueta_eficiencia = db.Column(db.String(10))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

@equipamentos_bp.route('/api/equipamentos', methods=['GET'])
def listar_equipamentos():
    # Só permite admin (ajuste conforme seu método de autenticação)
    if not hasattr(current_user, "role") or current_user.role != 'admin':
        return jsonify({"error": "Acesso restrito"}), 403
    equipamentos = Equipamento.query.all()
    qtd = len(equipamentos)
    potencia_total = sum(e.potencia for e in equipamentos)
    uso_medio_diario = round(sum(e.horas_uso for e in equipamentos) / qtd, 2) if qtd else 0
    consumo_mensal_estimado = round(sum(e.potencia * e.horas_uso * 30 for e in equipamentos), 2)
    return jsonify({
        "qtd": qtd,
        "potencia_total": round(potencia_total, 2),
        "uso_medio_diario": uso_medio_diario,
        "consumo_mensal_estimado": consumo_mensal_estimado,
        "equipamentos": [
            {
                "nome": e.nome,
                "potencia": e.potencia,
                "horas_uso": e.horas_uso,
                "categoria": e.categoria,
                "idade": e.idade,
                "etiqueta_eficiencia": e.etiqueta_eficiencia,
                "observacoes": e.observacoes,
                "updated_at": e.updated_at.strftime("%d/%m/%Y %H:%M") if e.updated_at else ""
            } for e in equipamentos
        ]
    })

@equipamentos_bp.route('/api/equipamentos', methods=['POST'])
def adicionar_equipamento():
    if not hasattr(current_user, "role") or current_user.role != 'admin':
        return jsonify({"error": "Acesso restrito"}), 403
    data = request.json
    eq = Equipamento(
        nome = data['nome'],
        potencia = data['potencia'],
        horas_uso = data['horas_uso'],
        categoria = data.get('categoria'),
        idade = data.get('idade'),
        etiqueta_eficiencia = data.get('etiqueta_eficiencia'),
        observacoes = data.get('observacoes'),
        updated_at = datetime.utcnow()
    )
    db.session.add(eq)
    db.session.commit()
    return jsonify({"msg": "Equipamento adicionado"}), 201
