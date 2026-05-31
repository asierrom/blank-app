import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector

def construir_circuit(bit, base):
    # Genera el qubit quàntic a partir del bit i la base
    qc = QuantumCircuit(1)
    if bit == 1:
        qc.x(0)
    if base == "X":
        qc.h(0)
    return qc

def bloch_fig(state, title="", figsize=(3, 3)):
    # Retorna la figura de l'Esfera de Bloch amb fons transparent
    fig = plot_bloch_multivector(state, title=title, figsize=figsize)
    fig.patch.set_facecolor("none")
    return fig

def bloch_compacte(bit, base, figsize=(2.6, 2.6)):
    # Construeix el circuit i també fa el grafic de Bloch
    qc = construir_circuit(bit, base)
    state = Statevector.from_instruction(qc)
    fig = plot_bloch_multivector(state, figsize=figsize)
    fig.patch.set_facecolor("none")
    for ax in fig.axes:
        ax.set_title("")
    return fig, state

def prob_bar_fig(prob_0, prob_1):
    # Gràfic de barres horitzontals a partir de dues probabilitats
    fig, ax = plt.subplots(figsize=(3.5, 1.6))
    labels = ["$|1\\rangle$", "$|0\\rangle$"]
    colors = ["#c9d9e9", "#2f3d92"]
    
    ax.barh(labels, [prob_1, prob_0], color=colors, height=0.5, edgecolor="white", linewidth=1.2)
    ax.text(prob_1 + 0.01, labels[0], f"{prob_1*100:.0f}%", va="center", fontsize=11, fontweight="bold")
    ax.text(prob_0 + 0.01, labels[1], f"{prob_0*100:.0f}%", va="center", fontsize=11, fontweight="bold")
    
    ax.set_xlim(0, 1.15)
    ax.set_xlabel("Probabilitat de mesura", fontsize=9)
    ax.spines["top"].set_visible(False) # Oculta el marc superior i dret
    ax.spines["right"].set_visible(False)
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")
    plt.tight_layout()
    return fig

def simular_100_mesures(prob_0, prob_1):
    # Simula de forma aleatòria 100 mesures d'un qubit i retorna el gràfic de barres vertical
    results = np.random.choice([0, 1], size=100, p=[prob_0, prob_1]) # Genera 100 valors aleatoris segons les probabilitats
    n0, n1 = np.sum(results == 0), np.sum(results == 1) # Recull les dades obtingudes aleatòriament
    
    fig, ax = plt.subplots(figsize=(3.5, 1.8))
    ax.bar(["$|0\\rangle$", "$|1\\rangle$"], [n0, n1], color=["#2f3d92", "#c9d9e9"], edgecolor="white", linewidth=1.2)
    ax.set_ylabel("Vegades mesurat", fontsize=9)
    for i, v in enumerate([n0, n1]):
        ax.text(i, v + 0.5, str(v), ha="center", fontsize=11, fontweight="bold")
    ax.set_ylim(0, 110)
    ax.spines[["top", "right"]].set_visible(False) # Oculta el marc superior i dret
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")
    plt.tight_layout()
    return fig, n0, n1

def barra_probabilitat(p0, p1, color0, color1, etiqueta0, etiqueta1):
    # Barra horitzontal combinada amb missatges
    fig, ax = plt.subplots(figsize=(4, 1.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.05, 1)
    ax.axis("off")

    es_determinista = (p0 >= 0.999 or p1 >= 0.999)

    if p0 > 0: # Crear un rectangle amb cantonades arrodonides
        rect0 = mpatches.FancyBboxPatch((0, 0.3), p0 - 0.005 if p1 > 0 else p0, 0.4, boxstyle="round,pad=0.01", facecolor=color0, edgecolor="white", linewidth=1.5)
        ax.add_patch(rect0)
        ax.text(p0 / 2, 0.5, f"{etiqueta0}\n{p0*100:.0f}%", ha="center", va="center", fontsize=9.5, color=color1, fontweight="bold", linespacing=1.3)

    if p1 > 0:
        left = p0 + 0.005 if p0 > 0 else 0  # Es deixa una petita separació visual
        rect1 = mpatches.FancyBboxPatch((left, 0.3), 1 - left, 0.4, boxstyle="round,pad=0.01", facecolor=color1, edgecolor="white", linewidth=1.5)
        ax.add_patch(rect1)
        ax.text(left + (1 - left) / 2, 0.5, f"{etiqueta1}\n{p1*100:.0f}%", ha="center", va="center", fontsize=9.5, color=color0, fontweight="bold", linespacing=1.3)

    if es_determinista:
        guanyador = etiqueta0 if p0 >= 0.999 else etiqueta1
        ax.text(0.5, 0.05, f"✔️ Resultat garantit: sempre {guanyador}", ha="center", va="bottom", fontsize=8.5, color="#166534", fontstyle="italic")
    else:
        ax.text(0.5, 0.05, "⚠️ Resultat aleatori: 50% per a cada opció!", ha="center", va="bottom", fontsize=8.5, color="#92400E", fontstyle="italic")

    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")
    plt.tight_layout(pad=0.2)
    return fig

def mostrar_resultat_mesura(p0, p1, color, color_suau):
    # Crear dos gràfics, el de la base correcta i base incorrecta
    fig, axes = plt.subplots(1, 2, figsize=(5, 2.2))

    # Gràfic de base correcta
    ax = axes[0]

    if p1 > p0: # Ressaltar el bit més probable
        colors = [color, "#D1D5DB"]
    else:
        colors = ["#D1D5DB", color]

    ax.barh(
        ["Bit 1", "Bit 0"],
        [p1, p0],
        color=colors,
        height=0.5,
        edgecolor="none"
    )

    ax.text(p1 + 0.02, 0, f"{p1*100:.0f}%", va="center",
            fontsize=11, fontweight="bold")
    ax.text(p0 + 0.02, 1, f"{p0*100:.0f}%", va="center",
            fontsize=11, fontweight="bold")

    ax.set_xlim(0, 1.25)
    ax.set_title("Base correcta", fontsize=10,
                 fontweight="bold", color=color)
    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
    ax.tick_params(left=False, bottom=False)
    ax.set_xticklabels([])
    ax.set_xlabel(
        "Resultat segur",
        fontsize=9,
        color=color,
        fontstyle="italic"
    )

    # Base incorrecta
    ax = axes[1]
    ax.barh(
        ["Bit 1", "Bit 0"],
        [0.5, 0.5], # El percentatge serà 50%-50%
        color=color_suau,
        height=0.5,
        edgecolor="none"
    )
    ax.text(0.52, 0, "50%", va="center",
            fontsize=11, fontweight="bold")
    ax.text(0.52, 1, "50%", va="center",
            fontsize=11, fontweight="bold")

    ax.set_xlim(0, 1.25)
    ax.set_title("Base incorrecta", fontsize=10,
                 fontweight="bold", color=color)
    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
    ax.tick_params(left=False, bottom=False)
    ax.set_xticklabels([])
    ax.set_xlabel(
        "Resultat aleatori",
        fontsize=9,
        color=color,
        fontstyle="italic"
    )
    fig.patch.set_facecolor("none")
    plt.tight_layout(pad=1.0)
    return fig

def calcular_probabilitats_mesura(bit_alice, base_alice, base_bob):
    # Calcula les probabilitats de col·lapse segons les bases escollides
    qc_mes = construir_circuit(bit_alice, base_alice)
    if base_bob == "X":
        qc_mes.h(0) # L'ordinador mesura per defecte en base Z, si està en base X cal aplicar porta Hadamard
    sv_mes = Statevector.from_instruction(qc_mes).data
    p0_mes = float(np.abs(sv_mes[0])**2) # Probabilitats mesura
    p1_mes = float(np.abs(sv_mes[1])**2)
    return p0_mes, p1_mes

def simular_historial_bob(n_mesures, p0_mes, p1_mes, color, color_suau):
    resultats = np.random.choice([0, 1], size=n_mesures, p=[p0_mes, p1_mes])
    n0 = np.sum(resultats == 0)
    n1 = np.sum(resultats == 1)

    fig, ax = plt.subplots(figsize=(4, 2.2))
    bars = ax.bar(["Bit 0", "Bit 1"], [n0, n1], color=[color, color_suau], edgecolor="white", linewidth=1.5, width=0.5)
    ax.text(0, n0 + 1, f"{n0}\n({n0/n_mesures*100:.1f}%)", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.text(1, n1 + 1, f"{n1}\n({n1/n_mesures*100:.1f}%)", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_ylim(0, n_mesures * 1.2)
    ax.set_ylabel("Nº mesures")
    ax.spines[["top", "right"]].set_visible(False)
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")
    plt.tight_layout()
    return fig, n0, n1