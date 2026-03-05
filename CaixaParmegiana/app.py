import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime


# ---------------- PREÇOS ----------------

preco_base = {
    "individual": {"carne": 29.99, "frango": 27.99},
    "duplo": {"carne": 54.99, "frango": 49.99},
    "triplo": {"carne": 83.99, "frango": 73.99},
}

arquivo = "pedidos.json"

# ---------------- FUNÇÕES ----------------

def calcular_valor():
    quantidade = var_quantidade.get()
    proteina = var_proteina.get()
    valor = preco_base[quantidade][proteina]

    if var_refrigerante.get():

        tipo = var_tipo_refri.get()
        marca = var_marca_refri.get()

        tabela_refri = {"coca": {"litro": 10, "lata": 6, "caculinha": 4},
                        "guarana": {"litro": 9, "lata": 6, "caculinha": 3}
        }

        if marca in tabela_refri and tipo in tabela_refri[marca]:
            valor += tabela_refri[marca][tipo]
        else:
            messagebox.showwarning("Erro", "Selecione marca e tamanho do refrigerante")

    # -------- ENTREGA --------
    if var_entrega.get():
        try:
            valor += float(var_valor_entrega.get())
        except:
            messagebox.showwarning("Erro", "Valor de entrega inválido")

    return valor


def salvar_pedido():
    cliente = entry_cliente.get()

    if not cliente:
        messagebox.showwarning("Erro", "Digite o nome do cliente")
        return

    pedido = {
        "cliente": cliente,
        "valor": calcular_valor(),
        "pagamento": var_pagamento.get(),
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }

    pedidos.append(pedido)
    salvar_arquivo()
    atualizar_lista()
    entry_cliente.delete(0, tk.END)


def salvar_arquivo():
    with open(arquivo, "w") as f:
        json.dump(pedidos, f, indent=4)


def carregar_arquivo():
    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            return json.load(f)
    return []


def atualizar_lista():
    lista.delete(0, tk.END)
    total = 0
    for pedido in pedidos:
        lista.insert(tk.END, f"{pedido['cliente']} - R$ {pedido['valor']:.2f} - {pedido['pagamento']}")
        total += pedido["valor"]

    label_total.config(text=f"Total do dia: R$ {total:.2f}")

# -------- INTERFACE --------

pedidos = carregar_arquivo()

janela = tk.Tk()
janela.title("Caixa Parmegiana")
janela.geometry("900x650")


frame_esquerda = tk.Frame(janela)
frame_esquerda.pack(side="left", padx=20, pady=20)


frame_direita = tk.Frame(janela)
frame_direita.pack(side="right", padx=20, pady=20)


tk.Label(frame_esquerda, text="Nome do Cliente").pack()
entry_cliente = tk.Entry(frame_esquerda)
entry_cliente.pack()


tk.Label(frame_esquerda, text="Quantidade").pack()
var_quantidade = tk.StringVar(value="individual")

tk.Radiobutton(frame_esquerda, text="Individual", variable=var_quantidade, value="individual").pack(anchor="w")
tk.Radiobutton(frame_esquerda, text="Duplo", variable=var_quantidade, value="duplo").pack(anchor="w")
tk.Radiobutton(frame_esquerda, text="Triplo", variable=var_quantidade, value="triplo").pack(anchor="w")


tk.Label(frame_esquerda, text="Proteína").pack()
var_proteina = tk.StringVar(value="carne")

tk.Radiobutton(frame_esquerda, text="Carne", variable=var_proteina, value="carne").pack(anchor="w")
tk.Radiobutton(frame_esquerda, text="Frango", variable=var_proteina, value="frango").pack(anchor="w")


tk.Label(frame_esquerda, text="Refrigerante").pack()
var_refrigerante = tk.BooleanVar()
tk.Checkbutton(frame_esquerda, text="Adicionar Refrigerante", variable=var_refrigerante).pack(anchor="w")

var_tipo_refri = tk.StringVar()
tk.Radiobutton(frame_esquerda, text="Caçulinha", variable=var_tipo_refri, value="caculinha").pack(anchor="w")
tk.Radiobutton(frame_esquerda, text="Lata", variable=var_tipo_refri, value="lata").pack(anchor="w")
tk.Radiobutton(frame_esquerda, text="Litro", variable=var_tipo_refri, value="litro").pack(anchor="w")

var_marca_refri = tk.StringVar()
tk.Radiobutton(frame_esquerda, text="Coca", variable=var_marca_refri, value="coca").pack(anchor="w")
tk.Radiobutton(frame_esquerda, text="Guaraná", variable=var_marca_refri, value="guarana").pack(anchor="w")


tk.Label(frame_esquerda, text="Entrega").pack()
var_entrega = tk.BooleanVar()
tk.Checkbutton(frame_esquerda, text="Adicionar Entrega", variable=var_entrega).pack(anchor="w")

var_valor_entrega = tk.StringVar(value="0")
tk.Entry(frame_esquerda, textvariable=var_valor_entrega).pack()


tk.Label(frame_esquerda, text="Forma de Pagamento").pack()
var_pagamento = tk.StringVar(value="Dinheiro")

tk.Radiobutton(frame_esquerda, text="Dinheiro", variable=var_pagamento, value="Dinheiro").pack(anchor="w")
tk.Radiobutton(frame_esquerda, text="Pix", variable=var_pagamento, value="Pix").pack(anchor="w")
tk.Radiobutton(frame_esquerda, text="Cartão", variable=var_pagamento, value="Cartão").pack(anchor="w")

tk.Button(frame_esquerda, text="Salvar Pedido", command=salvar_pedido, bg="green", fg="white").pack(pady=10)


tk.Label(frame_direita, text="Pedidos do Dia").pack()

lista = tk.Listbox(frame_direita, width=40, height=25)
lista.pack()

label_total = tk.Label(frame_direita, text="")
label_total.pack(pady=10)

atualizar_lista()
janela.mainloop()