import os
import tkinter as tk
from tkinter import messagebox

# ==========================================
# CONFIGURAÇÃO (3 PASTAS)
# ==========================================
PASTAS = [
    r"\\10.19.3.19\IbaData\Raw\403-SL4\Reports",
    r"\\10.19.3.19\IbaData\Raw\402-SL3\Reports",
    r"\\10.19.3.19\IbaData\Raw\401-SL2\reports"
]

resultados_map = []

# ==========================================
# BUSCA
# ==========================================
def buscar():

    lote = entrada_lote.get().strip().lower()

    lista_resultados.delete(0, tk.END)

    if not lote:
        messagebox.showwarning("Atenção", "Digite um lote.")
        return

    status_var.set("🔄 Aguarde, estou Procurando seu Arquivo...")
    janela.update()

    encontrados = []

    # percorre TODAS as pastas
    for pasta in PASTAS:
        for root, dirs, files in os.walk(pasta):
            try:
                for file in files:
                    if lote in file.lower():
                        caminho = os.path.join(root, file)
                        encontrados.append((caminho, pasta))
            except:
                pass

    global resultados_map
    resultados_map = [item[0] for item in encontrados]

    lista_resultados.delete(0, tk.END)

    if encontrados:

        for caminho, pasta in encontrados:

            nome = os.path.basename(caminho)

            if "TEAS" in pasta:
                origem = "TEAS"
            elif "FEAS" in pasta:
                origem = "FEAS"
            else:
                origem = "EXTRA"

            lista_resultados.insert(
                tk.END,
                f"[{origem}] 📄 {nome}"
            )

        contador.config(text=f"{len(encontrados)} resultado(s)")
        status_var.set(f"✅ {len(encontrados)} arquivo(s) encontrado(s)")

    else:
        lista_resultados.insert(tk.END, "❌ Nenhum arquivo localizado")
        contador.config(text="0 resultados")
        status_var.set("❌ Nenhum resultado encontrado")


# ==========================================
# ABRIR ARQUIVO
# ==========================================
def abrir_arquivo(event):

    if not lista_resultados.curselection():
        return

    idx = lista_resultados.curselection()[0]

    if idx >= len(resultados_map):
        return

    caminho = resultados_map[idx]

    if os.path.exists(caminho):
        os.startfile(caminho)


# ==========================================
# JANELA PRINCIPAL
# ==========================================
janela = tk.Tk()

largura = 900
altura = 700

x = (janela.winfo_screenwidth() // 2) - (largura // 2)
y = (janela.winfo_screenheight() // 2) - (altura // 2)

janela.geometry(f"{largura}x{altura}+{x}+{y}")
janela.title("Buscador IBA-Espessura")
janela.configure(bg="#0f172a")

# ==========================================
# CABEÇALHO
# ==========================================
header = tk.Frame(janela, bg="#1e293b", height=90)
header.pack(fill="x")

tk.Label(
    header,
    text="🔍 BUSCADOR IBA - TEAS & FEAS",
    bg="#1e293b",
    fg="white",
    font=("Segoe UI", 20, "bold")
).pack(pady=(15, 0))

tk.Label(
    header,
    text="Pesquisa de Dados de Espessura das Refiladeiras",
    bg="#1e293b",
    fg="#94a3b8",
    font=("Segoe UI", 10)
).pack()

# ==========================================
# CARD PRINCIPAL
# ==========================================
card = tk.Frame(janela, bg="#1e293b")
card.pack(fill="both", expand=True, padx=20, pady=20)

# ==========================================
# ÁREA DE BUSCA (1 CAMPO)
# ==========================================
frame_busca = tk.Frame(card, bg="#1e293b")
frame_busca.pack(pady=20)

tk.Label(
    frame_busca,
    text="Digite o número do lote desejado:",
    bg="#1e293b",
    fg="white",
    font=("Segoe UI", 11)
).pack(pady=(0, 8))

entrada_lote = tk.Entry(
    frame_busca,
    width=45,
    justify="center",
    font=("Segoe UI", 13),
    bg="#334155",
    fg="white",
    relief="flat",
    insertbackground="white"
)

entrada_lote.pack(ipady=8)

tk.Button(
    frame_busca,
    text="🔎 Buscar",
    command=buscar,
    bg="#2563eb",
    fg="white",
    relief="flat",
    font=("Segoe UI", 11, "bold"),
    cursor="hand2"
).pack(pady=15, ipadx=15, ipady=6)

# ==========================================
# CONTADOR
# ==========================================
contador = tk.Label(
    card,
    text="0 resultados",
    bg="#1e293b",
    fg="#38bdf8",
    font=("Segoe UI", 11, "bold")
)

contador.pack(anchor="w", padx=10)

# ==========================================
# LISTA
# ==========================================
frame_lista = tk.Frame(card, bg="#334155")
frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

scroll = tk.Scrollbar(frame_lista)
scroll.pack(side="right", fill="y")

lista_resultados = tk.Listbox(
    frame_lista,
    bg="#334155",
    fg="white",
    font=("Segoe UI", 11),
    borderwidth=0,
    activestyle="none",
    selectbackground="#2563eb",
    yscrollcommand=scroll.set
)

lista_resultados.pack(fill="both", expand=True)
scroll.config(command=lista_resultados.yview)

# ==========================================
# STATUS
# ==========================================
status_var = tk.StringVar(value="Pronto")

tk.Label(
    janela,
    textvariable=status_var,
    bg="#111827",
    fg="#94a3b8",
    anchor="w",
    padx=15,
    font=("Segoe UI", 10)
).pack(fill="x")

# ==========================================
# EVENTOS
# ==========================================
lista_resultados.bind("<Double-Button-1>", abrir_arquivo)
janela.bind("<Return>", lambda e: buscar())

entrada_lote.focus()

# ==========================================
# INICIAR
# ==========================================
janela.mainloop()