"""
=============================================================================
PROJECTE: Desxifra'm! - Plataforma de Simulació de Protocols Criptogràfics
FITXER: pestanya_CriptoClàssica.py
AUTOR: Asier Romero
CURS: 2n de Batxillerat (Maristes Rubí)
DATA DE CREACIÓ: Març 2026
ÚLTIMA MODIFICACIÓ: Maig 2026
VERSIÓ: 1.0
DESCRIPCIÓ: Interfície d'usuari per al Mòdul 1 (Criptografia
            Clàssica).
=============================================================================
"""

import streamlit as st
import base64
import M1_CriptoClàssica as CCl

# Guarda les imatges al caché de la web.
@st.cache_data
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
img_cesar_gran = get_base64("Cesar_gran.png")
img_cesar_petita = get_base64("Cesar_petita.png")
abecedari = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def mostrar_pagina_cesar():
    st.write("### Mètode de Substitució Cèsar")
    seccio_teoria() 
    st.divider()
    seccio_xifratge()
    st.divider()
    seccio_joc()

def seccio_teoria():
    with st.expander("Com funciona la roda del Cèsar?"):
        st.write("""
            El xifratge Cèsar és un mètode de substitució on cada lletra del text original es reemplaça 
            per una altra que es troba un nombre fix de posicions (clau) més endavant en l'alfabet.
            
            **Fes girar la roda interior** per veure com canvien les correspondències segons la clau triada:
            """)
        
        col_roda_ctrl, col_roda_img = st.columns([1, 1.5], vertical_alignment="center")
        
        with col_roda_ctrl:
            clau_teoria = st.slider("Tria la clau per fer girar la roda:", 0, 25, 0, key="slider_roda_teoria")
            angle = (360 / 26) * clau_teoria # Com la roda Cèsar té 26 lletres, l'angle d'una es calcula dividint l'angle total d'un cercle entre 26
            if clau_teoria == 0:
                st.info("La roda està alineada: **A** es manté com a **A**.")
            else:
                st.info(f"Amb la clau **{clau_teoria}**, la **A** es converteix en la **{abecedari[clau_teoria]}**.")

        with col_roda_img:
            # NOTA D'AUTORIA: L'estructura HTML/CSS d'aquest contenidor adaptatiu 
            # i la transició de rotació s'han generat amb el suport de ChatGPT (OpenAI).            
            st.markdown(f"""
                <div style="position: relative; width: 320px; height: 320px; margin: 0 auto; display: flex; justify-content: center; align-items: center;">
                    <img src="data:image/png;base64,{img_cesar_gran}" style="position: absolute; width: 320px; z-index: 1;">
                    <img src="data:image/png;base64,{img_cesar_petita}" style="position: absolute; width: 320px; z-index: 2; 
                         transform: rotate(-{angle}deg); transition: transform 0.6s ease-out;">
                </div>
                """, unsafe_allow_html=True)
        


def seccio_xifratge():
    st.write("### Prova-ho tu mateix!")
    st.write("Escriu un missatge, escull quina clau vols usar i descobreix quant temps trigaria un ordinador estàndar en descobrir el teu missatge secret!")

    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Configuració")
        missatge_original = st.text_input("Missatge:", "Introdueix el missatge a codificar")
        clau_xifrar = st.slider("Clau de desplaçament (n):", 1, 25, 1, key="slider_xifrar")
        
        if st.button("Xifrar missatge"):
            missatge_xifrat = CCl.xifrar_cesar(missatge_original, clau_xifrar)
            st.session_state['xifrat'] = missatge_xifrat
            st.success(f"Missatge xifrat: {missatge_xifrat}")

    with col2:
        st.write("#### Atac per Força Bruta")
        if 'xifrat' in st.session_state:
            if st.button("🚀 Iniciar Atac"):
                intent, temps = CCl.desxiframent_cesar(st.session_state['xifrat'], missatge_original)
                st.metric("L'ordinador només ha trigat en descobrir el missatge", f"{temps:.6f} segons")
                st.write(f"L'ordinador ha desxifrat: **{intent}**")
                
                with st.expander("Veure tots els intents de l'ordinador"):
                    
                    intents_llista = []
                    # Bucle per cada clau
                    for n in range(26):
                        provisional = CCl.xifrar_cesar(st.session_state['xifrat'], 26 - n)
                        
                        # Si és la clau correcta, es marca en negreta
                        if provisional == missatge_original.upper():
                            intents_llista.append(f"**Clau {n:02d}: {provisional} ✅**")
                        else:
                            intents_llista.append(f"Clau {n:02d}: {provisional}")
                    
                    # Mostra de totes les combinacions
                    for x in range(len(intents_llista)):
                        st.markdown(intents_llista[x])
        else:
            st.warning("Primer xifra un missatge.")
            st.image("QubyCèsar1.png", use_container_width=True)
        
        
        

def seccio_joc():
    st.write("### Missió: Desxifra el Missatge Interceptat")
    st.write("**Vols jugar a desxifrar el missatge tu mateix?**")
    st.write("Has interceptat una comunicació enemiga. Canvia la clau manualment per intentar que el text tingui sentit.")

    # Inicialització del Repte (comprova si ja hi ha un joc en partida)
    if 'joc_actiu' not in st.session_state:
        # Cridar al mòdul per generar les dades inicials
        msg_xifrat, original, clau_real = CCl.generar_joc_cesar()
        st.session_state.msg_xifrat = msg_xifrat
        st.session_state.solucio = original
        st.session_state.clau_intent = 0
        st.session_state.joc_actiu = True

    # Es mostra el missatge que l'usuari ha de adivinar
    st.warning(f"**MISSATGE INTERCEPTAT:**   {st.session_state.msg_xifrat}")

    # Controls de la Roda
    col_bt1, col_clau, col_bt2 = st.columns([1, 1, 1])

    with col_bt1:
        if st.button("⬅️ Girar Roda -1", disabled=st.session_state.clau_intent == 0): # Es deshabilita el botó si la clau es 0 per evitar claus negatives
            st.session_state.clau_intent -= 1
            st.rerun() 
        

    with col_clau:
        st.metric("Clau aplicada", f"n = {st.session_state.clau_intent}")

    with col_bt2:
        if st.button("Girar Roda +1 ➡️", disabled=st.session_state.clau_intent == 25): # Es deshabilita el botó si la clau és 25 per evitar claus més grans que 25
            st.session_state.clau_intent += 1
            st.rerun()

    # Descodificador
    # Important: Per desxifrar, s'aplica el desplaçament invers (26 - n)
    text_provisional = CCl.xifrar_cesar(st.session_state.msg_xifrat, 26 - st.session_state.clau_intent)

    st.write(f"#### Visualització del desxiframent amb clau n = {st.session_state.clau_intent}:")
    st.code(text_provisional, language=None)
    # Taula de xifratge
    abecedari_xifrat = CCl.xifrar_cesar(abecedari, st.session_state.clau_intent)
    capçalera = "| **ORIGINAL** | " + " | ".join(list(abecedari)) + " |"
    separador = "|:---:|" + "|".join([":---:"] * 26) + "|" 
    fila_xifrada = f"| **DESXIFRAT *n = {st.session_state.clau_intent}*** | " + " | ".join(list(abecedari_xifrat)) + " |"

    taula = f"{capçalera}\n{separador}\n{fila_xifrada}"
    st.markdown(taula)

    # Verificació de la clau que l'usuari tria
    if text_provisional == st.session_state.solucio:
        st.success(f"**EXCEL·LENT!** Has trobat la clau correcta: **{st.session_state.clau_intent}**.")
        st.balloons()
        if st.button("Generar nova missió"):
            del st.session_state.joc_actiu
            st.rerun()
    else:
        col1, col2 = st.columns([1,1])
        with col1:
            with st.expander("Necessites ajuda? Com funciona aquest descodificador?"):
                st.write(f"""
                Actualment estàs provant de moure tot l'alfabet **{st.session_state.clau_intent}** posicions enrere.
                Per exemple, si la clau fos 1, una **B** es convertiria en una **A**.
                Procura moure la roda fins que les paraules semblin català!
                """)
        
        with col2:
            st.image("QubyCèsar2.png", use_container_width=True)
