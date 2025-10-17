import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import json
import os


from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# -----------------------------
# Configurações
# -----------------------------
ARQUIVO = "caixa.csv"
ARQUIVO_ABERTO = "pedidos_abertos.json"

produtos = {
    1: ("Clássico da Casa", 17.00),
    2: ("Burger Bacon", 20.00),
    3: ("Burger Calabresa", 20.00),
    4: ("X-Tudo", 25.00),
    5: ("Guaraná Tropical 200ml", 3.00),
    6: ("Coca-Cola 350ml", 5.00),
    7: ("Sprite 350ml", 5.00),
    8: ("Coca-Cola 1L", 10.00),
    9: ("Guaraná Kuat 1L", 10.00),
    10: ("Fanta Laranja 1L", 10.00),
    11: ("Guaraná Jesus 1L", 10.00),
    12: ("Coca-Cola 2L", 15.00),
    13: ("Coca-Cola Zero 2L", 15.00),
    14: ("Guaraná Jesus 2L", 15.00),
    15: ("Psiu Guaraná 2L", 9.00),
    16: ("Psiu Cola 2L", 9.00),
    17: ("Psiu Guaraná Jesus 2L", 9.00),
}

formas_pagamento = ["PIX", "Cartão", "Dinheiro"]
status_opcoes = ["Pendente", "Em andamento", "Finalizado", "Entregue"]


# Ficha Técnica (ingredientes por lanche)
ficha_tecnica = {
    "Clássico da Casa": {
        "Pão":   ("un", 1),
        "Hambúrguer artesanal": ("g", 100),
        "Maionese caseira":     ("g", 30),
        "Queijo":               ("g", 20),
        "Presunto":             ("g", 20),
        "Salsicha":             ("un", 1),
        "Ovo":                  ("un", 1),
        "Tomate":               ("g", 30),
        "Milho":                ("g", 20),
        "Ervilha":              ("g", 20),
        "Batata palha":         ("g", 15),
    },
    "Burger Bacon": {
        "Pão":   ("un", 1),
        "Hambúrguer artesanal": ("g", 100),
        "Maionese caseira":     ("g", 30),
        "Bacon":                ("g", 30),
        "Queijo":               ("g", 20),
        "Presunto":             ("g", 20),
        "Salsicha":             ("un", 1),
        "Ovo":                  ("un", 1),
        "Tomate":               ("g", 30),
        "Milho":                ("g", 20),
        "Ervilha":              ("g", 20),
        "Batata palha":         ("g", 15),
    },
    "Burger Calabresa": {
        "Pão":   ("un", 1),
        "Hambúrguer artesanal": ("g", 100),
        "Maionese caseira":     ("g", 30),
        "Calabresa":            ("g", 40),
        "Queijo":               ("g", 20),
        "Presunto":             ("g", 20),
        "Salsicha":             ("un", 1),
        "Ovo":                  ("un", 1),
        "Tomate":               ("g", 30),
        "Milho":                ("g", 20),
        "Ervilha":              ("g", 20),
        "Batata palha":         ("g", 15),
    },
    "X-Tudo": {
        "Pão":   ("un", 1),
        "Hambúrguer artesanal": ("g", 100),
        "Maionese caseira":     ("g", 30),
        "Bacon":                ("g", 30),
        "Calabresa":            ("g", 40),
        "Queijo":               ("g", 20),
        "Presunto":             ("g", 20),
        "Salsicha":             ("un", 1),
        "Ovo":                  ("un", 1),
        "Tomate":               ("g", 30),
        "Milho":                ("g", 20),
        "Ervilha":              ("g", 20),
        "Batata palha":         ("g", 15),
    },
}

precos_ingredientes = {
    "Pão": { "preco_unitario": 1.6},
    "Hambúrguer artesanal": { "preco_unitario": 0.03},
    "Maionese caseira": { "preco_unitario": 0.01},
    "Queijo": { "preco_unitario": 0.04},
    "Presunto": { "preco_unitario": 0.02},
    "Salsicha": { "preco_unitario": 0.4},
    "Ovo": { "preco_unitario": 0.5},
    "Tomate": { "preco_unitario": 0.01},
    "Milho": { "preco_unitario": 0.025},
    "Ervilha": { "preco_unitario": 0.025},
    "Batata palha": { "preco_unitario": 0.0375},
    "Bacon": { "preco_unitario": 0.03},
    "Calabresa": { "preco_unitario": 0.03},
    # Bebidas e outros produtos podem ser adicionados aqui
    "Coca-Cola 350ml" : { "preco_unitario": 3.70},
    "Coca-Cola 1L" : { "preco_unitario": 7.0},
    "Coca-Cola 2L" : { "preco_unitario": 10.0},
    "Coca-Cola Zero 2L" : { "preco_unitario": 10.0},
    "Guaraná Kuat 1L" : { "preco_unitario": 7.0},
    "Guaraná Jesus 1L" : { "preco_unitario": 7.0},
    "Guaraná Jesus 2L" : { "preco_unitario": 10.0},
    "Psiu Guaraná 2L" : { "preco_unitario": 6.0},
    "Psiu Cola 2L" : { "preco_unitario": 6.0},
    "Psiu Guaraná Jesus 2L" : { "preco_unitario": 6.0},
    "Guaraná Tropical 200ml" : { "preco_unitario": 2.0},
    "Sprite 350ml" : { "preco_unitario": 3.70},
    "Fanta Laranja 1L" : { "preco_unitario": 7.0},

}

def calcular_custo_hamburguer(nome_produto, qtd=1):
    if nome_produto in ficha_tecnica:
        custo = 0.0
        for ingrediente, (unidade, quantidade) in ficha_tecnica[nome_produto].items():
            preco_info = precos_ingredientes.get(ingrediente)
            if preco_info and preco_info["preco_unitario"] > 0:
                custo += preco_info["preco_unitario"] * quantidade * qtd
        return custo
    preco_info = precos_ingredientes.get(nome_produto)
    if preco_info and preco_info["preco_unitario"] > 0:
        return preco_info["preco_unitario"] * qtd
    return 0.0

def calcular_lucros():
    vendas_por_produto = {}
    qtd_por_produto = {}
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8-sig") as f:
            leitor = csv.DictReader(f, delimiter=";")
            for linha in leitor:
                nome = linha.get("Produto", "")
                total_item = float(linha.get("Total Item", "0").replace(',', '.'))
                qtd = int(linha.get("Qtd", "1"))
                vendas_por_produto[nome] = vendas_por_produto.get(nome, 0) + total_item
                qtd_por_produto[nome] = qtd_por_produto.get(nome, 0) + qtd

    # Calcula custo total por produto
    custos_por_produto = {}
    for nome, qtd in qtd_por_produto.items():
        custos_por_produto[nome] = calcular_custo_hamburguer(nome, qtd)

    # Calcula lucro por produto
    lucros_por_produto = {}
    for nome in vendas_por_produto:
        lucro = vendas_por_produto[nome] - custos_por_produto.get(nome, 0)
        lucros_por_produto[nome] = lucro

    # Lucro total
    lucro_total = sum(lucros_por_produto.values())
    lbl_lucro.config(text=f"Lucro Total: R$ {lucro_total:.2f}")

    # Salva para gráfico
    root.lucros_por_produto = lucros_por_produto
    gerar_grafico_lucros()

def gerar_grafico_lucros():
    # Limpa gráficos anteriores
    for widget in frame_grafico_lucros.winfo_children():
        widget.destroy()

    lucros_por_produto = getattr(root, "lucros_por_produto", {})
    if not lucros_por_produto:
        tk.Label(frame_grafico_lucros, text="Nenhum dado para mostrar.").pack()
        return

    # --- Gráfico 1: Lucro por Produto (Top 10) ---
    itens = sorted(lucros_por_produto.items(), key=lambda x: x[1], reverse=True)[:10]
    nomes = [i[0] for i in itens][::-1]
    lucros = [i[1] for i in itens][::-1]

    fig = Figure(figsize=(12, 8))
    ax1 = fig.add_subplot(211)
    bars = ax1.barh(nomes, lucros, color="green")
    ax1.set_title("Lucro por Produto (Top 10)")
    ax1.set_xlabel("R$ Lucro")

    max_lucro = max(lucros) if lucros else 1
    for bar, lucro in zip(bars, lucros):
        width = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2
        if width >= max(1, max_lucro * 0.50):
            x_text = width - (max_lucro * 0.02)
            ha = "right"
            color = "white"
        else:
            x_text = width + (max_lucro * 0.02)
            ha = "left"
            color = "black"
        ax1.text(x_text, y, f"R$ {lucro:.2f}", va="center", ha=ha, color=color, fontsize=10, fontweight="bold")

    # --- Gráfico 2: Lucro por Dia ---
    # Calcula lucros por dia
    lucros_por_dia = {}
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8-sig") as f:
            leitor = csv.DictReader(f, delimiter=";")
            for linha in leitor:
                data_full = linha.get("Data", "")
                data_only = data_full.split(" ")[0] if data_full else ""
                nome = linha.get("Produto", "")
                total_item = float(linha.get("Total Item", "0").replace(',', '.'))
                qtd = int(linha.get("Qtd", "1"))
                custo = calcular_custo_hamburguer(nome, qtd)
                lucro = total_item - custo
                lucros_por_dia[data_only] = lucros_por_dia.get(data_only, 0) + lucro

    # Ordena por data
    dias_ordenados = sorted(lucros_por_dia.items(), key=lambda x: x[0])
    datas = [d[0] for d in dias_ordenados]
    lucros_dia = [d[1] for d in dias_ordenados]
    x_pos = list(range(len(datas)))

    ax2 = fig.add_subplot(212)
    if datas:
        ax2.plot(x_pos, lucros_dia, marker="o", color="blue")
        ax2.set_title("Lucro por Dia")
        ax2.set_ylabel("R$ Lucro")
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(datas, rotation=45)
        for i, data in enumerate(datas):
            val = lucros_dia[i]
            vmin = min(lucros_dia) if lucros_dia else 0
            vmax = max(lucros_dia) if lucros_dia else 0
            gap = max(5.0, (vmax - vmin) * 0.03) if vmax != vmin else 5.0
            ax2.text(i, val - gap, f"R$ {val:.2f}", ha="center", va="top",
                     fontsize=9, fontweight="bold", bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"))
    else:
        ax2.text(0.5, 0.5, "Sem dados", ha='center', va='center')
        ax2.axis('off')

    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico_lucros)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# -----------------------------
# Funções
# -----------------------------
def inicializar():
    # cria CSV com cabeçalho caso não exista
    try:
        with open(ARQUIVO, "x", newline="", encoding="utf-8-sig") as f:
            escritor = csv.writer(f, delimiter=";")
            escritor.writerow([
                "ID", "Data", "Cliente", "Telefone", "Endereço",
                "Produto", "Qtd", "Valor Unitário", "Total Item",
                "Total Pedido", "Forma Pagamento", "Troco",
                "Entrega", "Status", "Observacao"
            ])
    except FileExistsError:
        pass

    # cria JSON de pedidos em andamento caso não exista
    if not os.path.exists(ARQUIVO_ABERTO):
        with open(ARQUIVO_ABERTO, "w", encoding="utf-8-sig") as f:
            json.dump([], f)

def gerar_id():
    # ID = ano + sequência (ex: 20250001)
    ano = datetime.now().strftime("%Y")
    ultimo_id = int(ano + "0000")
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8-sig") as f:
            leitor = csv.DictReader(f, delimiter=";")
            for linha in leitor:
                val = linha.get("ID", "").strip()
                if val.startswith(ano) and val.isdigit():
                    ultimo_id = max(ultimo_id, int(val))
    return str(ultimo_id + 1)

def adicionar_item():
    selecao = combo_produto.get()
    qtd = qtd_var.get()
    if not selecao or qtd <= 0:
        messagebox.showerror("Erro", "Selecione um produto e quantidade válida!")
        return
    for codigo, (nome, preco) in produtos.items():
        if selecao.startswith(nome):
            total_item = preco * qtd
            itens_pedido.append({"nome": nome, "qtd": qtd, "preco": preco, "total_item": total_item})
            break
    atualizar_lista()

def remover_item():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um item para remover!")
        return
    idx = tree.index(selecionado)
    try:
        del itens_pedido[idx]
    except IndexError:
        pass
    atualizar_lista()

def atualizar_lista():
    for row in tree.get_children():
        tree.delete(row)
    total = 0
    for item in itens_pedido:
        tree.insert("", tk.END, values=(item["nome"], item["qtd"], f"R$ {item['preco']:.2f}", f"R$ {item['total_item']:.2f}"))
        total += item["total_item"]
    if entrega_var.get():
        total += 3
    lbl_total.config(text=f"Total: R$ {total:.2f}")

def salvar_em_andamento():
    nome = nome_var.get().strip()
    telefone = tel_var.get().strip()
    endereco = end_var.get().strip()
    forma = forma_var.get()
    if not nome or not telefone:
        messagebox.showerror("Erro", "Nome e telefone são obrigatórios!")
        return
    if not itens_pedido:
        messagebox.showerror("Erro", "Adicione ao menos 1 item ao pedido!")
        return
    total = sum([item["total_item"] for item in itens_pedido]) + (3 if entrega_var.get() else 0)
    pedido = {
        "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "cliente": nome,
        "telefone": telefone,
        "endereco": endereco,
        "itens": itens_pedido.copy(),
        "total": total,
        "forma": forma,
        "troco": 0,
        "entrega": entrega_var.get(),
        "status": "Em Andamento",
        "observacao": obs_var.get().strip()
    }
    with open(ARQUIVO_ABERTO, "r", encoding="utf-8-sig") as f:
        pedidos_abertos = json.load(f)
    if pedido_editando is not None:
        for i, p in enumerate(pedidos_abertos):
            if p["data_criacao"] == pedido_editando:
                pedidos_abertos[i] = pedido
                break
    else:
        pedidos_abertos.append(pedido)
    with open(ARQUIVO_ABERTO, "w", encoding="utf-8-sig") as f:
        json.dump(pedidos_abertos, f, indent=4, ensure_ascii=False)
    messagebox.showinfo("Salvo", "Pedido salvo como 'Em andamento'. Você pode continuar depois.")
    limpar_pedido()
    carregar_pedidos_abertos()

def carregar_pedidos_abertos():
    for row in tree_andamento.get_children():
        tree_andamento.delete(row)
    if not os.path.exists(ARQUIVO_ABERTO):
        return
    with open(ARQUIVO_ABERTO, "r", encoding="utf-8-sig") as f:
        pedidos_abertos = json.load(f)
    for pedido in pedidos_abertos:
        tree_andamento.insert("", tk.END, values=(
            pedido["data_criacao"],
            pedido["cliente"],
            pedido["telefone"],
            f"R$ {pedido['total']:.2f}",
            pedido["forma"],
            pedido["status"]
        ))

def carregar_pedido_para_editar():
    global pedido_editando
    selecionado = tree_andamento.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um pedido em andamento para editar!")
        return
    item = tree_andamento.item(selecionado)
    data_criacao = item["values"][0]
    with open(ARQUIVO_ABERTO, "r", encoding="utf-8-sig") as f:
        pedidos_abertos = json.load(f)
    pedido = next((p for p in pedidos_abertos if p["data_criacao"] == data_criacao), None)
    if not pedido:
        messagebox.showerror("Erro", "Pedido não encontrado!")
        return
    # Carrega dados na interface
    nome_var.set(pedido["cliente"])
    tel_var.set(pedido["telefone"])
    end_var.set(pedido["endereco"])
    forma_var.set(pedido["forma"])
    entrega_var.set(pedido["entrega"])
    obs_var.set(pedido.get("observacao", ""))
    entry_recebido.delete(0, tk.END)
    itens_pedido.clear()
    itens_pedido.extend(pedido["itens"])
    atualizar_lista()
    pedido_editando = pedido["data_criacao"]
    notebook.select(frame_pedido)

def finalizar_pedido():
    global pedido_editando
    nome = nome_var.get().strip()
    telefone = tel_var.get().strip()
    endereco = end_var.get().strip()
    forma = forma_var.get()
    if not nome or not telefone:
        messagebox.showerror("Erro", "Nome e telefone são obrigatórios!")
        return
    if not itens_pedido:
        messagebox.showerror("Erro", "Adicione ao menos 1 item ao pedido!")
        return
    total = sum([item["total_item"] for item in itens_pedido]) + (3 if entrega_var.get() else 0)
    troco = 0
    if forma == "Dinheiro":
        try:
            recebido = float(entry_recebido.get().replace(',', '.'))
            if recebido < total:
                messagebox.showerror("Erro", "Valor recebido insuficiente!")
                return
            troco = recebido - total
        except ValueError:
            messagebox.showerror("Erro", "Informe o valor recebido!")
            return
    pedido_id = gerar_id()
    obs = obs_var.get().strip()
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(ARQUIVO, "a", newline="", encoding="utf-8-sig") as f:
        escritor = csv.writer(f, delimiter=";")
        for item in itens_pedido:
            escritor.writerow([
                pedido_id, data, nome, telefone, endereco,
                item["nome"], item["qtd"],
                f"{item['preco']:.2f}".replace('.', ','),
                f"{item['total_item']:.2f}".replace('.', ','),
                f"{total:.2f}".replace('.', ','),
                forma, f"{troco:.2f}".replace('.', ','),
                "Sim" if entrega_var.get() else "Não",
                "Pendente", obs
            ])
    # remove pedido em andamento se estava editando
    if pedido_editando is not None:
        if os.path.exists(ARQUIVO_ABERTO):
            with open(ARQUIVO_ABERTO, "r", encoding="utf-8-sig") as f:
                pedidos_abertos = json.load(f)
            pedidos_abertos = [p for p in pedidos_abertos if p["data_criacao"] != pedido_editando]
            with open(ARQUIVO_ABERTO, "w", encoding="utf-8-sig") as f:
                json.dump(pedidos_abertos, f, indent=4, ensure_ascii=False)
    messagebox.showinfo("Pedido Registrado", f"Pedido {pedido_id} registrado!\nTotal: R${total:.2f}\nTroco: R${troco:.2f}")
    limpar_pedido()
    carregar_pedidos()
    carregar_pedidos_abertos()
    pedido_editando = None

def limpar_pedido():
    global pedido_editando
    nome_var.set("")
    tel_var.set("")
    end_var.set("")
    forma_var.set(formas_pagamento[0])
    entry_recebido.delete(0, tk.END)
    entrega_var.set(False)
    obs_var.set("")
    itens_pedido.clear()
    atualizar_lista()
    pedido_editando = None

def carregar_pedidos(filtro=""):
    for row in tree_hist.get_children():
        tree_hist.delete(row)
    if not os.path.exists(ARQUIVO):
        # atualiza labels mesmo sem arquivo
        lbl_pix.config(text=f"Valor em PIX: R${0:.2f}")
        lbl_cartao.config(text=f"Valor em Cartão: R${0:.2f}")
        lbl_dinheiro.config(text=f"Valor em Dinheiro: R${0:.2f}")
        lbl_total_dia.config(text=f"Total Geral: R${0:.2f}")
        return
    with open(ARQUIVO, "r", encoding="utf-8-sig") as f:
        leitor = csv.DictReader(f, delimiter=";")
        pedidos = {}
        for linha in leitor:
            if not linha:
                continue
            idv = linha.get("ID", "").strip()
            data = linha.get("Data", "").strip()
            cliente = linha.get("Cliente", "").strip()
            telefone = linha.get("Telefone", "").strip()
            total_str = linha.get("Total Pedido", "0").replace(',', '.')
            try:
                total = float(total_str)
            except Exception:
                total = 0.0
            chave = (idv, data, cliente, telefone)
            if chave not in pedidos:
                pedidos[chave] = {
                    "ID": idv,
                    "Data": data,
                    "Cliente": cliente,
                    "Telefone": telefone,
                    "Total": total,
                    "Forma": linha.get("Forma Pagamento", ""),
                    "Status": linha.get("Status", "")
                }
        # aplicar filtro
        termo = filtro.strip().lower()
        soma_pix = soma_cartao = soma_dinheiro = soma_total = 0
        for p in pedidos.values():
            row_vals = (p["ID"], p["Data"], p["Cliente"], p["Telefone"], f"R${p['Total']:.2f}", p["Forma"], p["Status"])
            if termo == "" or any(termo in str(v).lower() for v in row_vals):
                tree_hist.insert("", tk.END, values=row_vals)
                # soma por forma
                if p["Forma"].lower() == "pix":
                    soma_pix += p["Total"]
                elif p["Forma"].lower() == "cartão" or p["Forma"].lower() == "cartao":
                    soma_cartao += p["Total"]
                elif p["Forma"].lower() == "dinheiro":
                    soma_dinheiro += p["Total"]
                soma_total += p["Total"]

    # atualiza labels de totais
    lbl_pix.config(text=f"Valor em PIX: R${soma_pix:.2f}")
    lbl_cartao.config(text=f"Valor em Cartão: R${soma_cartao:.2f}")
    lbl_dinheiro.config(text=f"Valor em Dinheiro: R${soma_dinheiro:.2f}")
    lbl_total_dia.config(text=f"Total Geral: R${soma_total:.2f}")

def atualizar_status():
    selecionado = tree_hist.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um pedido para atualizar!")
        return
    novo_status = combo_status.get()
    valores = tree_hist.item(selecionado, "values")
    pedido_id = valores[0]
    linhas = []
    if not os.path.exists(ARQUIVO):
        messagebox.showerror("Erro", "Arquivo de pedidos não encontrado!")
        return
    with open(ARQUIVO, "r", encoding="utf-8-sig") as f:
        leitor = csv.DictReader(f, delimiter=";")
        for linha in leitor:
            if linha.get("ID", "") == pedido_id:
                linha["Status"] = novo_status
            linhas.append(linha)
    if linhas:
        with open(ARQUIVO, "w", newline="", encoding="utf-8-sig") as f:
            # usa os mesmos fieldnames do arquivo original (preserva ordem)
            fieldnames = ["ID", "Data", "Cliente", "Telefone", "Endereço",
                          "Produto", "Qtd", "Valor Unitário", "Total Item",
                          "Total Pedido", "Forma Pagamento", "Troco",
                          "Entrega", "Status", "Observacao"]
            escritor = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            escritor.writeheader()
            escritor.writerows(linhas)
    carregar_pedidos()

def on_editar_pedido_dia():
    selecionado = tree_hist.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um pedido para editar!")
        return
    # Solicita senha
    def verificar_senha():
        senha = entry_senha.get()
        if senha == "123":
            janela.destroy()
            editar_pedido_dia(selecionado)
        else:
            messagebox.showerror("Erro", "Senha incorreta!")
            janela.lift()
    janela = tk.Toplevel(root)
    janela.title("Autenticação")
    janela.geometry("300x120")
    tk.Label(janela, text="Digite a senha para editar:").pack(pady=10)
    entry_senha = tk.Entry(janela, show="*", width=20)
    entry_senha.pack(pady=5)
    tk.Button(janela, text="Confirmar", command=verificar_senha, bg="green", fg="white").pack(pady=5)
    entry_senha.focus_set()

def editar_pedido_dia(selecionado):
    item = tree_hist.item(selecionado)
    valores = item["values"]
    pedido_id = valores[0]
    # Busca o pedido no arquivo CSV
    linhas = []
    with open(ARQUIVO, "r", encoding="utf-8-sig") as f:
        leitor = csv.DictReader(f, delimiter=";")
        for linha in leitor:
            linhas.append(linha)
    # Filtra linhas do pedido
    pedido_linhas = [l for l in linhas if l.get("ID", "") == str(pedido_id)]
    if not pedido_linhas:
        pedido_linhas = [l for l in linhas if l.get("ID", "") == str(int(pedido_id))]
    if not pedido_linhas:
        messagebox.showerror("Erro", f"Pedido {pedido_id} não encontrado!\nVerifique se o pedido possui múltiplos produtos.")
        return

    janela = tk.Toplevel(root)
    janela.title(f"Editar Pedido {pedido_id}")
    janela.geometry("800x520")

    campos = ["Cliente", "Telefone", "Endereço", "Forma Pagamento", "Status", "Observacao"]
    vars = {c: tk.StringVar(value=pedido_linhas[0].get(c, "")) for c in campos}
    for i, c in enumerate(campos):
        tk.Label(janela, text=c+":").grid(row=i, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(janela, textvariable=vars[c], width=40).grid(row=i, column=1, padx=5, pady=5)

    # Produtos do pedido
    frame_prod = tk.LabelFrame(janela, text="Produtos do Pedido")
    frame_prod.grid(row=0, column=2, rowspan=len(campos), padx=10, pady=10, sticky="ns")

    tree_prod = ttk.Treeview(frame_prod, columns=("Produto", "Qtd", "Unit", "Total"), show="headings", height=8)
    for col in ("Produto", "Qtd", "Unit", "Total"):
        tree_prod.heading(col, text=col)
    tree_prod.pack(fill="both", expand=True)

    # Carrega produtos
    itens_editaveis = []
    for l in pedido_linhas:
        nome = l.get("Produto", "")
        qtd = int(l.get("Qtd", "1"))
        preco = float(l.get("Valor Unitário", "0").replace(",", "."))
        total_item = float(l.get("Total Item", "0").replace(",", "."))
        itens_editaveis.append({"nome": nome, "qtd": qtd, "preco": preco, "total_item": total_item})

    def atualizar_tree_prod():
        for row in tree_prod.get_children():
            tree_prod.delete(row)
        for item in itens_editaveis:
            tree_prod.insert("", tk.END, values=(item["nome"], item["qtd"], f"R$ {item['preco']:.2f}", f"R$ {item['total_item']:.2f}"))

    atualizar_tree_prod()

    # Funções para editar/remover/adicionar produto
    def editar_produto():
        selecionado = tree_prod.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um produto para editar!")
            return
        idx = tree_prod.index(selecionado)
        item = itens_editaveis[idx]
        edit_win = tk.Toplevel(janela)
        edit_win.title("Editar Produto")
        tk.Label(edit_win, text="Produto:").grid(row=0, column=0, padx=5, pady=5)
        prod_var = tk.StringVar(value=item["nome"])
        ttk.Combobox(edit_win, values=[p[0] for p in produtos.values()], textvariable=prod_var, state="readonly").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(edit_win, text="Qtd:").grid(row=1, column=0, padx=5, pady=5)
        qtd_var = tk.IntVar(value=item["qtd"])
        tk.Entry(edit_win, textvariable=qtd_var, width=5).grid(row=1, column=1, padx=5, pady=5)
        def salvar_prod():
            nome = prod_var.get()
            qtd = qtd_var.get()
            preco = next((p[1] for p in produtos.values() if p[0] == nome), item["preco"])
            total_item = preco * qtd
            itens_editaveis[idx] = {"nome": nome, "qtd": qtd, "preco": preco, "total_item": total_item}
            atualizar_tree_prod()
            edit_win.destroy()
        tk.Button(edit_win, text="Salvar", command=salvar_prod, bg="green", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

    def remover_produto():
        selecionado = tree_prod.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um produto para remover!")
            return
        idx = tree_prod.index(selecionado)
        del itens_editaveis[idx]
        atualizar_tree_prod()

    def adicionar_produto():
        add_win = tk.Toplevel(janela)
        add_win.title("Adicionar Produto")
        tk.Label(add_win, text="Produto:").grid(row=0, column=0, padx=5, pady=5)
        prod_var = tk.StringVar()
        ttk.Combobox(add_win, values=[p[0] for p in produtos.values()], textvariable=prod_var, state="readonly").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(add_win, text="Qtd:").grid(row=1, column=0, padx=5, pady=5)
        qtd_var = tk.IntVar(value=1)
        tk.Entry(add_win, textvariable=qtd_var, width=5).grid(row=1, column=1, padx=5, pady=5)
        def salvar_novo():
            nome = prod_var.get()
            qtd = qtd_var.get()
            preco = next((p[1] for p in produtos.values() if p[0] == nome), 0.0)
            total_item = preco * qtd
            itens_editaveis.append({"nome": nome, "qtd": qtd, "preco": preco, "total_item": total_item})
            atualizar_tree_prod()
            add_win.destroy()
        tk.Button(add_win, text="Adicionar", command=salvar_novo, bg="blue", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

    btn_frame = tk.Frame(frame_prod)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Editar Produto", command=editar_produto, bg="orange", fg="black").pack(side="left", padx=5)
    tk.Button(btn_frame, text="Remover Produto", command=remover_produto, bg="red", fg="white").pack(side="left", padx=5)
    tk.Button(btn_frame, text="Adicionar Produto", command=adicionar_produto, bg="blue", fg="white").pack(side="left", padx=5)

    def salvar_edicao():
        try:
            # Atualiza campos principais
            for l in linhas:
                if l.get("ID", "") == str(pedido_id) or l.get("ID", "") == str(int(pedido_id)):
                    for c in campos:
                        l[c] = vars[c].get()
            # Remove todas as linhas do pedido
            linhas_filtradas = [l for l in linhas if l.get("ID", "") != str(pedido_id) and l.get("ID", "") != str(int(pedido_id))]
            # Adiciona linhas atualizadas dos produtos
            total_pedido = sum([item["total_item"] for item in itens_editaveis])
            data = pedido_linhas[0].get("Data", "")
            cliente = vars["Cliente"].get()
            telefone = vars["Telefone"].get()
            endereco = vars["Endereço"].get()
            forma = vars["Forma Pagamento"].get()
            status = vars["Status"].get()
            obs = vars["Observacao"].get()
            entrega = pedido_linhas[0].get("Entrega", "")
            troco = pedido_linhas[0].get("Troco", "")
            for item in itens_editaveis:
                linhas_filtradas.append({
                    "ID": str(pedido_id),
                    "Data": data,
                    "Cliente": cliente,
                    "Telefone": telefone,
                    "Endereço": endereco,
                    "Produto": item["nome"],
                    "Qtd": str(item["qtd"]),
                    "Valor Unitário": f"{item['preco']:.2f}".replace('.', ','),
                    "Total Item": f"{item['total_item']:.2f}".replace('.', ','),
                    "Total Pedido": f"{total_pedido:.2f}".replace('.', ','),
                    "Forma Pagamento": forma,
                    "Troco": troco,
                    "Entrega": entrega,
                    "Status": status,
                    "Observacao": obs
                })
            with open(ARQUIVO, "w", newline="", encoding="utf-8-sig") as f:
                fieldnames = ["ID", "Data", "Cliente", "Telefone", "Endereço",
                            "Produto", "Qtd", "Valor Unitário", "Total Item",
                            "Total Pedido", "Forma Pagamento", "Troco",
                            "Entrega", "Status", "Observacao"]
                escritor = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
                escritor.writeheader()
                escritor.writerows(linhas_filtradas)
            messagebox.showinfo("Sucesso", "Pedido editado com sucesso!")
            janela.destroy()
            carregar_pedidos()
        except Exception as e:
            messagebox.showerror("Erro ao salvar", str(e))

    btn_salvar = tk.Button(janela, text="Salvar", command=salvar_edicao, bg="green", fg="white")
    btn_salvar.grid(row=len(campos)+2, column=0, columnspan=2, pady=15)

def gerar_recibo_txt(pedido_id):
    # Busca o pedido no arquivo CSV
    if not os.path.exists(ARQUIVO):
        messagebox.showerror("Erro", "Arquivo de pedidos não encontrado!")
        return
    pedido_info = None
    itens = []
    entrega_valor = 0.0
    observacao = ""
    with open(ARQUIVO, "r", encoding="utf-8-sig") as f:
        leitor = csv.DictReader(f, delimiter=";")
        for linha in leitor:
            if linha.get("ID", "") == pedido_id:
                if not pedido_info:
                    pedido_info = {
                        "ID": linha.get("ID", ""),
                        "Data": linha.get("Data", ""),
                        "Cliente": linha.get("Cliente", ""),
                        "Telefone": linha.get("Telefone", ""),
                        "Endereco": linha.get("Endereço", ""),
                        "Forma": linha.get("Forma Pagamento", ""),
                        "Total": linha.get("Total Pedido", ""),
                        "Entrega": linha.get("Entrega", ""),
                        "Observacao": linha.get("Observacao", ""),
                    }
                    # verifica valor da entrega
                    if linha.get("Entrega", "").strip().lower() in ["sim", "true", "1"]:
                        entrega_valor = 3.0
                    observacao = linha.get("Observacao", "")
                itens.append({
                    "Produto": linha.get("Produto", ""),
                    "Qtd": linha.get("Qtd", ""),
                    "Total Item": linha.get("Total Item", ""),
                })
    if not pedido_info:
        messagebox.showerror("Erro", "Pedido não encontrado!")
        return

    # Monta o recibo
    recibo = []
    recibo.append(" " * 25 + "RECIBO DE VENDA\n")
    recibo.append("-" * 60)
    recibo.append(f"ID do Pedido:      {pedido_info['ID']}")
    recibo.append(f"Cliente:           {pedido_info['Cliente']}")
    recibo.append(f"Telefone:          {pedido_info['Telefone']}")
    recibo.append(f"Endereço da entrega: {pedido_info['Endereco']}")
    recibo.append(f"Data:              {pedido_info['Data']}")
    recibo.append("-" * 60)
    recibo.append("Itens:")
    for item in itens:
        recibo.append(f"  {item['Produto']} x{item['Qtd']}  -  R$ {item['Total Item']}")
    if entrega_valor > 0:
        recibo.append(f"\nEntrega:           R$ {entrega_valor:.2f}")
    recibo.append("-" * 60)
    recibo.append(f"Valor Total:       R$ {pedido_info['Total']}")
    recibo.append(f"Forma de Pagamento: {pedido_info['Forma']}")
    if observacao:
        recibo.append("-" * 60)
        recibo.append(f"Observações: {observacao}")
    recibo.append("-" * 60)
    recibo.append("\nHamburgueria do Gaúcho")
    recibo.append("Endereço: Rua da Rocinha, Tasso Fragoso - MA")
    recibo.append("Telefone: +55 99 8467-1941")
    recibo.append("\nAgradecemos a preferência!\n")

    recibo_texto = "\n".join(recibo)

    # Exibe em uma janela para copiar/colar e opção de salvar
    def salvar_recibo():
        nome_arquivo = f"recibo_{pedido_id}.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(recibo_texto)
        messagebox.showinfo("Recibo Salvo", f"Recibo salvo como {nome_arquivo}")

    janela = tk.Toplevel(root)
    janela.title(f"Recibo do Pedido {pedido_id}")
    janela.geometry("600x500")
    txt = tk.Text(janela, font=("Consolas", 12))
    txt.pack(fill="both", expand=True, padx=10, pady=10)
    txt.insert("1.0", recibo_texto)
    txt.config(state="normal")
    # Botão para salvar
    btn_salvar = tk.Button(janela, text="Salvar como TXT", command=salvar_recibo, bg="green", fg="white")
    btn_salvar.pack(pady=5)
    # Botão para fechar
    btn_fechar = tk.Button(janela, text="Fechar", command=janela.destroy)
    btn_fechar.pack(pady=5)

def on_gerar_recibo():
    selecionado = tree_hist.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um pedido para gerar o recibo!")
        return
    valores = tree_hist.item(selecionado, "values")
    pedido_id = valores[0]
    gerar_recibo_txt(pedido_id)
    
# ----- Função para gerar gráficos -----
def gerar_graficos(container, filtro=""):
    for widget in container.winfo_children():
        widget.destroy()

    if not os.path.exists(ARQUIVO):
        tk.Label(container, text="Nenhum dado para gerar relatórios.").pack()
        return

    # estruturas para agregação corretas
    produtos_qtd = {}     # nome -> total quantidade
    produtos_val = {}     # nome -> total valor (soma Total Item)
    orders = {}           # order_id -> (data_only, total_pedido) para evitar soma duplicada
    forma_por_pedido = {} # order_id -> forma
    pedidos_por_dia = {}  # data_only -> set(order_id)

    # primeira passagem: lê linhas e agrega qtd/val por produto, e registra orders (ID -> total)
    with open(ARQUIVO, "r", encoding="utf-8-sig") as f:
        leitor = csv.DictReader(f, delimiter=";")
        for linha in leitor:
            if not linha:
                continue

            # aplicar filtro simples: busca no cliente/produto/data (checagem por linha)
            linha_str = " ".join([str(v) for v in linha.values()]).lower()
            if filtro and filtro not in linha_str:
                continue

            # produto
            nome = linha.get("Produto", "").strip()
            qtd_str = linha.get("Qtd", "0").strip()
            try:
                qtd = int(qtd_str)
            except Exception:
                try:
                    qtd = int(float(qtd_str))
                except Exception:
                    qtd = 0

            # total do item (valor do produto * qtd) - coluna "Total Item"
            total_item = 0.0
            try:
                total_item = float(linha.get("Total Item", "0").replace(",", "."))
            except Exception:
                # fallback: tenta multiplicar preço unitário por qtd
                try:
                    unit = float(linha.get("Valor Unitário", "0").replace(",", "."))
                    total_item = unit * qtd
                except Exception:
                    total_item = 0.0

            if nome:
                produtos_qtd[nome] = produtos_qtd.get(nome, 0) + qtd
                produtos_val[nome] = produtos_val.get(nome, 0.0) + total_item

            # orders: para faturamento diário e formas não somarmos o mesmo pedido várias vezes,
            # guardamos por ID
            order_id = linha.get("ID", "").strip()
            data_full = linha.get("Data", "")
            data_only = data_full.split(" ")[0] if data_full else ""
            if order_id:
                if order_id not in orders:
                    # tento obter total do pedido (valor que aparece na linha "Total Pedido")
                    try:
                        orders[order_id] = (data_only, float(linha.get("Total Pedido", "0").replace(",", ".")))
                    except Exception:
                        orders[order_id] = (data_only, 0.0)
                if data_only:
                    pedidos_por_dia.setdefault(data_only, set()).add(order_id)
                # registra forma por pedido (primeira ocorrência)
                forma = linha.get("Forma Pagamento", "").strip()
                if order_id not in forma_por_pedido and forma:
                    forma_por_pedido[order_id] = forma

    # soma valores por forma (somando cada pedido apenas uma vez)
    formas_agg = {}
    for order_id, (data_only, total_val) in orders.items():
        # se filtro foi aplicado, precisamos garantir que este order_id foi incluído (cheque forma_por_pedido ou pedidos_por_dia)
        if filtro:
            # se nenhum dado do pedido passou no filtro, pular
            found = False
            # quick heuristic: if order_id in forma_por_pedido then it had at least one line matched earlier
            if order_id in forma_por_pedido:
                found = True
            else:
                # also check if order_id in any pedidos_por_dia set
                for s in pedidos_por_dia.values():
                    if order_id in s:
                        found = True
                        break
            if not found:
                continue
        forma = forma_por_pedido.get(order_id, "Outro")
        formas_agg[forma] = formas_agg.get(forma, 0.0) + total_val

    # Agrupa faturamento por dia somando cada pedido uma vez
    dias = {}
    pedidos_count = {}
    for order_id, (data_only, total_val) in orders.items():
        if filtro:
            # garantir que order_id foi considerado
            if order_id not in forma_por_pedido and not any(order_id in s for s in pedidos_por_dia.values()):
                continue
        if not data_only:
            continue
        dias[data_only] = dias.get(data_only, 0.0) + total_val
        pedidos_count[data_only] = pedidos_count.get(data_only, 0) + 1

    # cria figura com 3 gráficos
    fig = Figure(figsize=(12, 5))

    # Produtos mais vendidos (top 10)
    ax1 = fig.add_subplot(131)
    if produtos_qtd:
        itens = sorted(produtos_qtd.items(), key=lambda x: x[1], reverse=True)[:10]
        nomes_desc = [i[0] for i in itens][::-1]  # reverter pra barra horizontal mais legível
        qtds = [i[1] for i in itens][::-1]
        vals = [produtos_val.get(name, 0.0) for name in [i[0] for i in itens]][::-1]
        bars = ax1.barh(nomes_desc, qtds)
        ax1.set_title("Produtos mais vendidos (Top 10)")
        ax1.set_xlabel("Quantidade")

        # Determina referência para deslocamento de texto
        max_q = max(qtds) if qtds else 1
        for bar, q, v in zip(bars, qtds, vals):
            width = bar.get_width()
            y = bar.get_y() + bar.get_height() / 2
            # Se a barra for suficientemente larga, coloca texto dentro (alinhado à direita).
            # Caso contrário, posiciona do lado direito da barra.
            if width >= max(1, max_q * 0.50):
                x_text = width - (max_q * 0.02)  # pequeno recuo dentro da barra
                ha = "right"
                color = "white"
            else:
                x_text = width + (max_q * 0.02)
                ha = "left"
                color = "black"
            ax1.text(x_text, y, f"Qtd: {q}  |  R$ {v:.2f}", va="center", ha=ha, color=color, fontsize=9, fontweight="bold")
    else:
        ax1.text(0.5, 0.5, "Sem dados", ha='center', va='center')
        ax1.axis('off')

    # Formas de pagamento (pie) - mostra % e R$
    ax2 = fig.add_subplot(132)
    if formas_agg and sum(formas_agg.values()) > 0:
        labels = list(formas_agg.keys())
        valores = [formas_agg[k] for k in labels]
        total_forms = sum(valores)
        def autopct_fn(pct):
            val = total_forms * pct / 100.0
            return f"{pct:.1f}%\nR$ {val:.2f}"
        wedges, texts, autotexts = ax2.pie(
            valores,
            labels=labels,
            autopct=autopct_fn,
            startangle=90
        )
        ax2.set_title("Distribuição por Forma de Pagamento")
        for txt in autotexts:
            txt.set_fontsize(8)
    else:
        ax2.text(0.5, 0.5, "Sem dados", ha='center', va='center')
        ax2.axis('off')

    # Faturamento por dia (linha) com rótulos de Qtd e R$ abaixo do ponto
    ax3 = fig.add_subplot(133)
    if dias:
        dias_ordenados = sorted(dias.items(), key=lambda x: x[0])
        datas = [d[0] for d in dias_ordenados]
        vals = [d[1] for d in dias_ordenados]
        x_pos = list(range(len(datas)))
        ax3.plot(x_pos, vals, marker="o")
        ax3.set_title("Faturamento por Dia")
        ax3.tick_params(axis="x", rotation=45)
        ax3.set_ylabel("R$")
        # coloca labels do eixo x com as datas
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels(datas)
        # adiciona rótulos embaixo do ponto com fundo branco semitransparente
        for i, data in enumerate(datas):
            qtd_ped = pedidos_count.get(data, 0)
            val = vals[i]
            # calcula deslocamento vertical para ficar abaixo - usa 5% do valor máximo como gap
            vmin = min(vals) if vals else 0
            vmax = max(vals) if vals else 0
            gap = max(5.0, (vmax - vmin) * 0.03) if vmax != vmin else 5.0
            ax3.text(i, val - gap, f"Qtd: {qtd_ped}\nR$ {val:.2f}", ha="center", va="top",
                     fontsize=8, fontweight="bold", bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"))
    else:
        ax3.text(0.5, 0.5, "Sem dados", ha='center', va='center')
        ax3.axis('off')

    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# -----------------------------
# Interface Principal
# -----------------------------
inicializar()
itens_pedido = []
pedido_editando = None

root = tk.Tk()
root.title("Sistema de Caixa - Hambúrgueria do Gaúcho")
root.geometry("1100x750")

# estilo (aumenta fonte do Treeview)
style = ttk.Style()
style.configure("Treeview", font=("Arial", 12))
style.configure("Treeview.Heading", font=("Arial", 14, "bold"))

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# -----------------------------
# Aba Novo Pedido
# -----------------------------
frame_pedido = ttk.Frame(notebook)
notebook.add(frame_pedido, text="Novo Pedido")

frame_cliente = tk.LabelFrame(frame_pedido, text="Dados do Cliente")
frame_cliente.pack(fill="x", padx=10, pady=5)

nome_var = tk.StringVar()
tel_var = tk.StringVar()
end_var = tk.StringVar()

tk.Label(frame_cliente, text="Nome:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
tk.Entry(frame_cliente, textvariable=nome_var, width=40).grid(row=0, column=1, padx=5, pady=2)
tk.Label(frame_cliente, text="Telefone:").grid(row=1, column=0, padx=5, pady=2, sticky="e")
tk.Entry(frame_cliente, textvariable=tel_var, width=20).grid(row=1, column=1, padx=5, pady=2, sticky="w")
tk.Label(frame_cliente, text="Endereço:").grid(row=2, column=0, padx=5, pady=2, sticky="e")
tk.Entry(frame_cliente, textvariable=end_var, width=40).grid(row=2, column=1, padx=5, pady=2)

frame_produto = tk.LabelFrame(frame_pedido, text="Adicionar Produto")
frame_produto.pack(fill="x", padx=10, pady=5)

produto_var = tk.StringVar()
qtd_var = tk.IntVar(value=1)

tk.Label(frame_produto, text="Produto:").grid(row=0, column=0, padx=5, pady=2)
combo_produto = ttk.Combobox(frame_produto,
    values=[f"{p[0]} (R${p[1]:.2f})" for p in produtos.values()],
    state="readonly", width=40)
combo_produto.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_produto, text="Quantidade:").grid(row=0, column=2, padx=5, pady=2)
tk.Entry(frame_produto, textvariable=qtd_var, width=5).grid(row=0, column=3, padx=5, pady=2)

tk.Button(frame_produto, text="Adicionar", command=adicionar_item).grid(row=0, column=4, padx=5, pady=2)

frame_lista = tk.LabelFrame(frame_pedido, text="Itens do Pedido")
frame_lista.pack(fill="both", padx=10, pady=5, expand=True)

tree = ttk.Treeview(frame_lista, columns=("Produto", "Qtd", "Unit", "Total"), show="headings")
for col in ("Produto", "Qtd", "Unit", "Total"):
    tree.heading(col, text=col)
tree.pack(fill="both", expand=True)

tk.Button(frame_lista, text="Remover Selecionado", command=remover_item, bg="red", fg="white").pack(pady=5)

lbl_total = tk.Label(frame_pedido, text="Total: R$ 0.00", font=("Arial", 14, "bold"))
lbl_total.pack(pady=5)

frame_obs = tk.LabelFrame(frame_pedido, text="Observações")
frame_obs.pack(fill="x", padx=10, pady=5)
obs_var = tk.StringVar()
tk.Entry(frame_obs, textvariable=obs_var, width=70).pack(padx=5, pady=5)

frame_pag = tk.LabelFrame(frame_pedido, text="Pagamento")
frame_pag.pack(fill="x", padx=10, pady=5)

forma_var = tk.StringVar(value=formas_pagamento[0])
ttk.Combobox(frame_pag, values=formas_pagamento, state="readonly", textvariable=forma_var).grid(row=0, column=0, padx=5, pady=2)

tk.Label(frame_pag, text="Valor Recebido (Dinheiro):").grid(row=0, column=1, padx=5, pady=2)
entry_recebido = tk.Entry(frame_pag, width=10)
entry_recebido.grid(row=0, column=2, padx=5, pady=2)

entrega_var = tk.BooleanVar()
tk.Checkbutton(frame_pag, text="Entrega (+R$3,00)", variable=entrega_var, command=atualizar_lista).grid(row=0, column=3, padx=5, pady=2)

frame_botoes = tk.Frame(frame_pedido)
frame_botoes.pack(fill="x", padx=10, pady=10)

tk.Button(frame_botoes, text="Salvar Pedido em Andamento", command=salvar_em_andamento, bg="orange", fg="black").pack(side="left", expand=True, padx=5)
tk.Button(frame_botoes, text="Finalizar Pedido", command=finalizar_pedido, bg="green", fg="white").pack(side="left", expand=True, padx=5)
tk.Button(frame_botoes, text="Novo Pedido", command=limpar_pedido, bg="blue", fg="white").pack(side="left", expand=True, padx=5)

# -----------------------------
# Aba Pedidos do Dia
# -----------------------------
frame_hist = ttk.Frame(notebook)
notebook.add(frame_hist, text="Pedidos do Dia")

# filtro / pesquisa
frame_filtro = tk.Frame(frame_hist)
frame_filtro.pack(fill="x", padx=10, pady=5)
filtro_var = tk.StringVar()
tk.Label(frame_filtro, text="Pesquisar:").pack(side="left", padx=5)
entry_filtro = tk.Entry(frame_filtro, textvariable=filtro_var, width=30)
entry_filtro.pack(side="left", padx=5)

def on_pesquisar():
    carregar_pedidos(filtro_var.get())

def on_limpar():
    filtro_var.set("")
    carregar_pedidos("")

tk.Button(frame_filtro, text="Pesquisar", command=on_pesquisar).pack(side="left", padx=5)
tk.Button(frame_filtro, text="Limpar", command=on_limpar).pack(side="left", padx=5)

tree_hist = ttk.Treeview(frame_hist, columns=("ID", "Data", "Cliente", "Telefone", "Total", "Forma", "Status"), show="headings")
for col in ("ID", "Data", "Cliente", "Telefone", "Total", "Forma", "Status"):
    tree_hist.heading(col, text=col)
tree_hist.pack(fill="both", expand=True, padx=10, pady=10)

# ---- Alterar Status ----
frame_status = tk.Frame(frame_hist)
frame_status.pack(fill="x", padx=10, pady=5)

tk.Label(frame_status, text="Novo Status:").pack(side="left", padx=5)
combo_status = ttk.Combobox(frame_status, values=status_opcoes, state="readonly", width=20)
combo_status.current(0)
combo_status.pack(side="left", padx=5)
tk.Button(frame_status, text="Atualizar Status", command=atualizar_status, bg="orange", fg="black").pack(side="left", padx=10)
tk.Button(frame_status, text="Gerar Recibo", command=on_gerar_recibo, bg="gray", fg="white").pack(side="left", padx=10)
tk.Button(frame_status, text="Editar Pedido Selecionado", command=on_editar_pedido_dia, bg="purple", fg="white").pack(side="left", padx=10)
# ---- Rodapé com totais coloridos ----
frame_totais = tk.Frame(frame_hist)
frame_totais.pack(fill="x", padx=10, pady=5)

lbl_pix = tk.Label(frame_totais, text="Valor em PIX: R$0.00", font=("Arial", 12, "bold"), fg="green")
lbl_pix.pack(side="left", padx=15)

lbl_cartao = tk.Label(frame_totais, text="Valor em Cartão: R$0.00", font=("Arial", 12, "bold"), fg="blue")
lbl_cartao.pack(side="left", padx=15)

lbl_dinheiro = tk.Label(frame_totais, text="Valor em Dinheiro: R$0.00", font=("Arial", 12, "bold"), fg="brown")
lbl_dinheiro.pack(side="left", padx=15)

lbl_total_dia = tk.Label(frame_totais, text="Total Geral: R$0.00", font=("Arial", 12, "bold"), fg="black")
lbl_total_dia.pack(side="left", padx=15)

# -----------------------------
# Aba Pedidos em Andamento
# -----------------------------
frame_andamento = ttk.Frame(notebook)
notebook.add(frame_andamento, text="Pedidos em Andamento")

tree_andamento = ttk.Treeview(frame_andamento, columns=("Data", "Cliente", "Telefone", "Total", "Forma", "Status"), show="headings")
for col in ("Data", "Cliente", "Telefone", "Total", "Forma", "Status"):
    tree_andamento.heading(col, text=col)
tree_andamento.pack(fill="both", expand=True, padx=10, pady=10)

frame_botoes_andamento = tk.Frame(frame_andamento)
frame_botoes_andamento.pack(fill="x", padx=10, pady=5)
tk.Button(frame_botoes_andamento, text="Editar Pedido Selecionado", command=carregar_pedido_para_editar, bg="purple", fg="white").pack(side="left", padx=5)

# -----------------------------
# Aba Relatórios
# -----------------------------
frame_relatorios = ttk.Frame(notebook)
notebook.add(frame_relatorios, text="Relatórios")

frame_filtros_rel = tk.Frame(frame_relatorios)
frame_filtros_rel.pack(fill="x", padx=10, pady=5)

tk.Label(frame_filtros_rel, text="Filtro (cliente/produto/data):").pack(side="left", padx=5)
filtro_rel_var = tk.StringVar()
entry_rel = tk.Entry(frame_filtros_rel, textvariable=filtro_rel_var, width=40)
entry_rel.pack(side="left", padx=5)

def gerar_relatorios():
    filtro = filtro_rel_var.get().lower().strip()
    gerar_graficos(frame_graficos, filtro)

tk.Button(frame_filtros_rel, text="Gerar Relatórios", command=gerar_relatorios, bg="green", fg="white").pack(side="left", padx=10)

frame_graficos = tk.Frame(frame_relatorios)
frame_graficos.pack(fill="both", expand=True, padx=10, pady=10)

# Aba Lucros
# -----------------------------
frame_lucros = ttk.Frame(notebook)
notebook.add(frame_lucros, text="Lucros")

frame_filtros_lucros = tk.Frame(frame_lucros)
frame_filtros_lucros.pack(fill="x", padx=10, pady=5)

tk.Label(frame_filtros_lucros, text="Filtro (cliente/produto/data):").pack(side="left", padx=5)
filtro_lucros_var = tk.StringVar()
entry_lucros = tk.Entry(frame_filtros_lucros, textvariable=filtro_lucros_var, width=40)
entry_lucros.pack(side="left", padx=5)

lbl_lucro = tk.Label(frame_lucros, text="Lucro Total: R$ 0.00", font=("Arial", 14, "bold"))
lbl_lucro.pack(pady=5)

frame_grafico_lucros = tk.Frame(frame_lucros)
frame_grafico_lucros.pack(fill="both", expand=True, padx=10, pady=10)

def calcular_lucros_com_filtro():
    filtro = filtro_lucros_var.get().lower().strip()
    calcular_lucros(filtro)

tk.Button(frame_filtros_lucros, text="Gerar Lucros", command=calcular_lucros_com_filtro, bg="green", fg="white").pack(side="left", padx=10)

# Atualize a função calcular_lucros para aceitar filtro:
def calcular_lucros(filtro=""):
    vendas_por_produto = {}
    qtd_por_produto = {}
    # Calcula vendas e quantidade vendida por produto
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8-sig") as f:
            leitor = csv.DictReader(f, delimiter=";")
            for linha in leitor:
                linha_str = " ".join([str(v) for v in linha.values()]).lower()
                if filtro and filtro not in linha_str:
                    continue
                nome = linha.get("Produto", "")
                total_item = float(linha.get("Total Item", "0").replace(',', '.'))
                qtd = int(linha.get("Qtd", "1"))
                vendas_por_produto[nome] = vendas_por_produto.get(nome, 0) + total_item
                qtd_por_produto[nome] = qtd_por_produto.get(nome, 0) + qtd

    # Calcula custo total por produto
    custos_por_produto = {}
    for nome, qtd in qtd_por_produto.items():
        custos_por_produto[nome] = calcular_custo_hamburguer(nome, qtd)

    # Calcula lucro por produto
    lucros_por_produto = {}
    for nome in vendas_por_produto:
        lucro = vendas_por_produto[nome] - custos_por_produto.get(nome, 0)
        lucros_por_produto[nome] = lucro

    # Lucro total
    lucro_total = sum(lucros_por_produto.values())
    lbl_lucro.config(text=f"Lucro Total: R$ {lucro_total:.2f}")

    # Salva para gráfico
    root.lucros_por_produto = lucros_por_produto
    gerar_grafico_lucros(filtro)

# Atualize a função gerar_grafico_lucros para aceitar filtro:
def gerar_grafico_lucros(filtro=""):
    # Limpa gráficos anteriores
    for widget in frame_grafico_lucros.winfo_children():
        widget.destroy()

    lucros_por_produto = getattr(root, "lucros_por_produto", {})
    if not lucros_por_produto:
        tk.Label(frame_grafico_lucros, text="Nenhum dado para mostrar.").pack()
        return

    # --- Gráfico 1: Lucro por Produto (Top 10) ---
    itens = sorted(lucros_por_produto.items(), key=lambda x: x[1], reverse=True)[:10]
    nomes = [i[0] for i in itens][::-1]
    lucros = [i[1] for i in itens][::-1]

    fig = Figure(figsize=(12, 8))
    ax1 = fig.add_subplot(211)
    bars = ax1.barh(nomes, lucros, color="green")
    ax1.set_title("Lucro por Produto (Top 10)")
    ax1.set_xlabel("R$ Lucro")

    max_lucro = max(lucros) if lucros else 1
    for bar, lucro in zip(bars, lucros):
        width = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2
        if width >= max(1, max_lucro * 0.50):
            x_text = width - (max_lucro * 0.02)
            ha = "right"
            color = "white"
        else:
            x_text = width + (max_lucro * 0.02)
            ha = "left"
            color = "black"
        ax1.text(x_text, y, f"R$ {lucro:.2f}", va="center", ha=ha, color=color, fontsize=10, fontweight="bold")

    # --- Gráfico 2: Lucro por Dia ---
    lucros_por_dia = {}
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8-sig") as f:
            leitor = csv.DictReader(f, delimiter=";")
            for linha in leitor:
                linha_str = " ".join([str(v) for v in linha.values()]).lower()
                if filtro and filtro not in linha_str:
                    continue
                data_full = linha.get("Data", "")
                data_only = data_full.split(" ")[0] if data_full else ""
                nome = linha.get("Produto", "")
                total_item = float(linha.get("Total Item", "0").replace(',', '.'))
                qtd = int(linha.get("Qtd", "1"))
                custo = calcular_custo_hamburguer(nome, qtd)
                lucro = total_item - custo
                lucros_por_dia[data_only] = lucros_por_dia.get(data_only, 0) + lucro

    dias_ordenados = sorted(lucros_por_dia.items(), key=lambda x: x[0])
    datas = [d[0] for d in dias_ordenados]
    lucros_dia = [d[1] for d in dias_ordenados]
    x_pos = list(range(len(datas)))

    ax2 = fig.add_subplot(212)
    if datas:
        ax2.plot(x_pos, lucros_dia, marker="o", color="blue")
        ax2.set_title("Lucro por Dia")
        ax2.set_ylabel("R$ Lucro")
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(datas, rotation=45)
        for i, data in enumerate(datas):
            val = lucros_dia[i]
            vmin = min(lucros_dia) if lucros_dia else 0
            vmax = max(lucros_dia) if lucros_dia else 0
            gap = max(5.0, (vmax - vmin) * 0.03) if vmax != vmin else 5.0
            ax2.text(i, val - gap, f"R$ {val:.2f}", ha="center", va="top",
                     fontsize=9, fontweight="bold", bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"))
    else:
        ax2.text(0.5, 0.5, "Sem dados", ha='center', va='center')
        ax2.axis('off')

    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico_lucros)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# carrega dados iniciaiss
carregar_pedidos()
carregar_pedidos_abertos()


root.mainloop()
