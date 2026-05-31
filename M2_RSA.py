"""
=============================================================================
PROJECTE: Desxifra'm! - Plataforma de Simulació de Protocols Criptogràfics
FITXER: M2_RSA.py
AUTOR: Asier Romero
CURS: 2n de Batxillerat (Maristes Rubí)
DATA DE CREACIÓ: Abril 2026
ÚLTIMA MODIFICACIÓ: Maig 2026
VERSIÓ: 1.0
DESCRIPCIÓ: Mòdul de lògica algorísmica per a l'estudi de l'RSA.
            Conté les funcions matemàtiques de complexitat per a la corba
            GNFS i l'algorisme de Shor, la generació del gràfic comparatiu
            amb Matplotlib i el xifratge/superposició XOR de matrius
            d'imatges per a l'experiment de seguretat.
=============================================================================
"""
import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def calcular_dades_grafic(num_digits):
    c = (64/9)**(1/3) # Constant de la fórmula de l'eficiència

    # Adaptació de funcions de complexitat per evitar que el programa se saturi
    # ln(n) = ln(10^digits) = digits * ln(10)
    max_digits = max(200, num_digits + 50)
    digits_array = np.linspace(2, max_digits, 500)
    
    ln_n_array = digits_array * np.log(10)
    ln_ln_n_array = np.log(ln_n_array)
    
    # Les funcions de cada corba
    gnfs_array = np.exp(c * (ln_n_array**(1/3)) * (ln_ln_n_array**(2/3)))
    shor_array = ln_n_array**3
    
    return digits_array, gnfs_array, shor_array

def calcular_punt_N(num_digits, N):
    c = (64/9)**(1/3) # Constant de la fórmula de l'eficiència
    
    # Si N > 10^308 fa una aproximació 
    try:
        ln_N = math.log(N)
    except OverflowError: 
        ln_N = num_digits * math.log(10) 
            
    ln_ln_N = math.log(ln_N)
    
    # Càlcul de quantes vegades és més eficient un algorisme que l'altre
    gnfs_N = math.exp(c * (ln_N**(1/3)) * (ln_ln_N**(2/3)))        
    shor_N = ln_N**3
    ratio = gnfs_N / shor_N
    
    return gnfs_N, shor_N, ratio

def crear_grafic_comparacio(num_digits, gnfs_N, shor_N, digits_array, gnfs_array, shor_array):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(digits_array, gnfs_array, label="GNFS (Clàssic)", linewidth=2, color="#2f3d92")
    ax.plot(digits_array, shor_array, label="Shor (Quàntic)", linewidth=2, color="#c9d9e9")
    
    # Afegir els punts N
    ax.scatter([num_digits, num_digits], [gnfs_N, shor_N], color="#B22222", zorder=5, s=60, label=f"El teu $N$ ({num_digits} dígits)")
    ax.vlines(num_digits, shor_N, gnfs_N, linestyles="dashed", colors="#B22222", alpha=0.7)
    
    # Configuració dels eixos
    ax.set_yscale('log') # Només l'eix Y requereix escala logarítmica perquè l'eix X ja són dígits
    
    ax.set_title("Comparació de l'algorisme GNFS amb l'algorisme de Shor", fontsize=14)
    ax.set_xlabel("Longitud del nombre $N$ (Nombre de dígits)", fontsize=12)
    ax.set_ylabel("Passos de Computació", fontsize=12)
    
    ax.grid(True, which="both", ls="--", alpha=0.5)
    ax.legend()
    
    return fig

# Apartat d'experiment amb imatges:
def preparar_img(imatge_entrada):
    # Passa la imatge a escala de grisos i la redimensiona a 400x400
    imatge_tractada = Image.open(imatge_entrada).convert("L")
    imatge_tractada = imatge_tractada.resize((400, 400))
    return np.array(imatge_tractada)

def generar_clau_aleatoria(shape):
    return np.random.randint(0, 256, shape, dtype=np.uint8)

def xifrar_imatges_xor(matriu_img, matriu_clau):
    return np.bitwise_xor(matriu_img, matriu_clau)

def superposicio_imatges_xor(xifrat1, xifrat2):
    return np.bitwise_xor(xifrat1, xifrat2)