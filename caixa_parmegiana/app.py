from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3

from database import criar_tabela
from precos import PRECO_BASE, PRECO_REFRIGERANTE, PRECO_ENTREGA

app = Flask(__name__)
criar_tabela()

def calcular_valor(tipo, proteina, refrigerante, entrega):
    valor = PRECO_BASE[tipo][proteina]

    if refrigerante:
        valor += PRECO_REFRIGERANTE
    if entrega:
        valor += PRECO_ENTREGA

    return valor

@app.route("/", methods=["GET", "POST"])
def novo_pedido():
    if request.method == "POST":
        cliente = request.form["cliente"]
        tipo = request.form["tipo"]
        proteina = request.form["proteina"]
        refrigerante = 1 if request.form.get("refrigerante") else 0
        entrega = 1 if request.form.get("entrega") else 0
        origem = request.form["origem"]
        pagamento = request.form["pagamento"]

        valor = calcular_valor(tipo, proteina, refrigerante, entrega)
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

        conn = sqlite3.connect("caixa.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pedidos
            (cliente, tipo, proteina, refrigerante, entrega, origem, pagamento, valor, data_hora)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (cliente, tipo, proteina, refrigerante, entrega, origem, pagamento, valor, data_hora))
        conn.commit()
        conn.close()

        return redirect("/caixa")

    return render_template("novo_pedido.html")

@app.route("/caixa")
def caixa():
    conn = sqlite3.connect("caixa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedidos")
    pedidos = cursor.fetchall()

    total = sum(p[8] for p in pedidos)
    conn.close()

    return render_template("caixa.html", pedidos=pedidos, total=total)

app.run(debug=True)
