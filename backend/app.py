from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.get_json()

    # pega os dados enviados
    peso = float(dados.get("peso", 0))
    idade = int(dados.get("idade", 0))
    atividade = dados.get("atividade")
    clima = dados.get("clima")

    # --- Aqui entram as regras de cálculo ---
    quantidade_agua = 0

    # Exemplo: fator por idade
    if idade <= 17:
        fator = 0.040
    elif 18 <= idade <= 55:
        fator = 0.035
    else:  # acima de 55
        fator = 0.030

    # Atividade (usar o fator base ou aumentar)
    if atividade == "sedentario":
        quantidade_agua = peso * fator
    elif atividade == "ativo":
        quantidade_agua = peso * fator + 0.5
    else:
        return jsonify({"erro": "Atividade inválida"}), 400

    # Ajuste pelo clima
    if clima == "quente":
        quantidade_agua += 0.5
    elif clima == "frio":
        quantidade_agua -= 0.2

    return jsonify({"agua_recomendada": round(quantidade_agua, 2)})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
