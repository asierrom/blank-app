import numpy as np
import random
# Diccionari dels estats i els seus respectius colors
ESTATS = {
    (0, 'Z'): {'nom': '|0⟩', 'color': '#1a73e8', 'color_suau': '#e8f0fe'},
    (1, 'Z'): {'nom': '|1⟩', 'color': '#d93025', 'color_suau': '#fce8e6'},
    (0, 'X'): {'nom': '|+⟩', 'color': '#188038', 'color_suau': '#e6f4ea'},
    (1, 'X'): {'nom': '|−⟩', 'color': '#e37400', 'color_suau': '#fef7e0'},
}

def generar_dades_alice(n_bits):
    # Genera els bits i bases aleatoris d'Alice
    alice_bits = np.random.randint(2, size=n_bits).tolist()
    alice_bases = np.random.choice(['Z', 'X'], size=n_bits).tolist()
    return alice_bits, alice_bases


def generar_dades_eve(n_bits, alice_bits, alice_bases):
    # Genera les bases i bits d'Eve (espia), simulant la seva mesura
    eve_bases = np.random.choice(['Z', 'X'], size=n_bits).tolist()
    eve_bits = []
    for i in range(n_bits):
        if eve_bases[i] == alice_bases[i]:
            eve_bits.append(alice_bits[i])       # Encerta la base, mesura correctament
        else:
            eve_bits.append(random.choice([0, 1]))  # Falla la base, resultat aleatori 50%-50%
    return eve_bases, eve_bits


def generar_dades_bob(n_bits, alice_bits, alice_bases, eve_activa, eve_bases, eve_bits):
    # Genera les bases i bits de Bob, tenint en compte si Eve ha interceptat
    bob_bases = np.random.choice(['Z', 'X'], size=n_bits).tolist()
    bob_bits = []
    for i in range(n_bits):
        base_rebuda = eve_bases[i] if eve_activa else alice_bases[i]
        bit_rebut   = eve_bits[i]  if eve_activa else alice_bits[i]

        if bob_bases[i] == base_rebuda:
            bob_bits.append(bit_rebut)
        else:
            bob_bits.append(random.choice([0, 1]))
    return bob_bases, bob_bits

def calcular_clau_bruta(n_bits, alice_bits, alice_bases, bob_bits, bob_bases):
    # Compara les bases d'Alice i Bob i retorna els índexs on les bases coincideien, els bits d'Alice en les posicions vàlides i els bits del Bob en les posicions vàlides.
    indexos_valids   = []
    clau_bruta_alice = []
    clau_bruta_bob   = []

    for i in range(n_bits):
        if alice_bases[i] == bob_bases[i]:
            indexos_valids.append(i)
            clau_bruta_alice.append(alice_bits[i])
            clau_bruta_bob.append(bob_bits[i])

    return indexos_valids, clau_bruta_alice, clau_bruta_bob


def seleccionar_mostra_qber(n_valids):
    # Tria aleatòriament un 50 % dels índexos locals de la clau bruta per usar-los com a mostra del QBER.
    mida_mostra = max(1, int(n_valids * 0.75))
    return random.sample(range(n_valids), mida_mostra)


def calcular_qber(clau_bruta_alice, clau_bruta_bob, mostra_idx):
    # Calcula la Taxa d'Error de Bit Quàntic (QBER) sobre la mostra indicada i retorna el nombre d'errors trobats i el QBER
    errors = sum(
        1 for idx in mostra_idx
        if clau_bruta_alice[idx] != clau_bruta_bob[idx]
    )
    qber = (errors / len(mostra_idx)) * 100
    return errors, qber


def obtenir_clau_final(clau_bruta_alice, mostra_idx):
    # Retorna els bits que queden un cop descartada la mostra del QBER. 
    return [
        clau_bruta_alice[i]
        for i in range(len(clau_bruta_alice))
        if i not in mostra_idx
    ]


def resum_eve(n_bits, alice_bases, eve_bases):
    # Retorna el nombre de bases encertades per Eve i les pertorbades
    encerts = sum(1 for i in range(n_bits) if eve_bases[i] == alice_bases[i])
    pertorbats = n_bits - encerts
    return encerts, pertorbats