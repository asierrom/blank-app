#Mòdul 1: Criptografia clàssica i vulnerabilitat (xifratge Cèsar)
import time # Mòdul per cronometrar el temps en què un programa s'executa
import random

def xifrar_cesar(missatge_a_codificar, clau):
    # Es converteix el missatge a majúscules
    missatge_a_codificar = missatge_a_codificar.upper()
    
    # Es defineix l'abecedari per comparar caràcters
    abecedari = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
    
    missatge_xifrat = ""
    
    # Es recorre caràcter per caràcter
    for caracter in missatge_a_codificar:
        
        # Es mira si el caràcter forma part de l'abecedari
        if caracter in abecedari:
            # Es troba la posició de la leltra (P)
            P = abecedari.find(caracter)
            
            # S'Aplica la fórmula: C = (P + clau) mod26
            C = (P + clau) % 26
            
            # S'afegeix el nou caràcter xifrat
            missatge_xifrat += abecedari[C]
        else:
            # Si no és un caràcter de l'abecedari, s'afegeix directament
            missatge_xifrat += caracter
            
    return missatge_xifrat

def desxiframent_cesar(missatge_xifrat, missatge_original):
    # Es guarda el moment exacte en què comença el programa
    inici_temps = time.time() 
    
    # Es defineix l'abecedari i es passa el missatge a majúscules.
    abecedari = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    missatge_original = missatge_original.upper() 
    
    #La clau amb què comença el programa és 0 (no canvia el missatge original versus el xifrat)
    clau_actual = 0
    trobat = False
    
    # Bucle principal: aplica la clau i comprova si és la correcta
    while not trobat and clau_actual < 26:
        intent_desxifrat = ""
        
        # Es selecciona el següent caràcter, s'aplica fórmula o afegeix directament
        for caracter in missatge_xifrat:
            if caracter in abecedari:
                C = abecedari.find(caracter)
                #Fórmula de desxifrat: P = (C - clau) mod 26
                P = (C - clau_actual) % 26
                intent_desxifrat += abecedari[P]
            else:
                intent_desxifrat += caracter
        
        # Si coincideixen, el programa ja ha desxifrat el missatge
        if intent_desxifrat == missatge_original:
            trobat = True
        else:
            clau_actual += 1

    # Es guarda el temps que ha trigat el programa en desxifrar el missatge       
    final_temps = time.time()
    return intent_desxifrat, (final_temps - inici_temps)

def generar_joc_cesar():
    frases = [
            "CLAU INCORRECTA, TORNA A INTENTAR-HO",
            "EL PROTOCOL QUANTIC ES EL FUTUR",
            "AQUESTA WEB ES INCREIBLE PER ENTENDRE CRIPTOGRAFIA",
            "LA CONTRASENYA ES #C0NTRA$3NYA",
            "DEMA A L'ALBA FAREM L'INTERCANVI",
            "AQUEST MISSATGE VA SER ESCRIT EL SET D'ABRIL DE 2026"
        ]
    frase = random.choice(frases)
    clau = random.randint(1, 25)
    # Es retorna la frase ja xifrada, la frase escollida i la clau original
    return xifrar_cesar(frase, clau), frase, clau

# NOTA: El programa agafa l'abecedari sense lletres especials de llengües específiques (com ho són la Ç o la Ñ).
# Per tant, si s'usen aquestes lletres, el programa no les codifica i les deixa tal com hi són. 
# Però en cap cas el programa dona error en usar-se altres caràcters.