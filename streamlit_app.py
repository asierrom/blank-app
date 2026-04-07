import streamlit as st
import M1_CriptoClàssica as CCl
import base64
from streamlit_option_menu import option_menu
import pandas as pd

# Guarda les imatges al caché de la web.
@st.cache_data
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
img_cesar_gran = get_base64("Cesar_gran.png")
img_cesar_petita = get_base64("Cesar_petita.png")
abecedari = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Treu icones d'enllaç de la web
st.markdown("""
    <style>
    .stApp a.element-container:hover, 
    .stApp a.header-anchor {
        display: none !important;
    }
    [data-testid="stHeaderActionElements"] {
        display: none !important;
    }
    .header-anchor {
        display: none !important;
    }
   
    </style>
    """, unsafe_allow_html=True)
# Tipografia de la web
st.markdown("""
    <style>
    /* Importació de Poppins des de Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    /* Aplicació de Poppins a tota la web */
    html, body, [class*="css"], .stApp, p, span, div, h1, h2, h3, h4, h5, h6, label, input, button {
        font-family: 'Poppins', sans-serif !important;
    }

    /* Títol i negretes dels títols  */
    h1, h2, h3, h4, h5 {
        color: #2f3d92 !important;
    }
    h1 { font-weight: 700 !important; } /* st.title */
    h2, h3, h4, h5 { font-weight: 500 !important; } /* st.header, st.subheader, ###, ####, ##### */

    
    /* Restauració font predeterminada per icones de Streamlit */
    .material-symbols-rounded, 
    .material-icons, 
    [class*="material-symbols"],
    [data-testid="stIconMaterial"], 
    [data-baseweb="icon"], 
    [data-baseweb="icon"] * {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        /* Assegurem que el text 'arrow_down' es converteixi en dibuix */
        font-feature-settings: 'liga' !important; 
    }

    /* Restauració de les icones de Bootstrapdel menú */
    .bi, [class^="bi-"], [class*=" bi-"], .nav-link i {
        font-family: "bootstrap-icons" !important;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    </style>
    """, unsafe_allow_html=True)



# Configuració inicial de la pàgina
st.set_page_config(page_title="Desxifra'm!", page_icon="Logo_desxifram.png", layout="wide")
 
col_logo, col_titol = st.columns([0.9,9], vertical_alignment="center")
with col_logo:
    st.image("Logo_desxifram.png", width=500) 
with col_titol:
    st.title("Desxifra'm!")
st.subheader("Simulador de Protocols Criptogràfics")

# Menú horitzontal
pestanya = option_menu(
    menu_title=None, 
    options=["Inici", "Criptografia Cèsar", "Algorisme RSA", "Protocol Quàntic BB84"], # Noms dels apartats
    icons=["house-door-fill", "alphabet-uppercase", "key-fill", "cpu-fill"], # Icones
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0!important", 
            "background-color": "#ddeaf7", 
            "border-radius": "15px",        
            "border": "1px solid #c5d5e5",
        },
        "icon": {
            "color": "#2f3d92",            
            "font-size": "17px"
        }, 
        "nav-link": {                        # Quan passa el punter per sobre
            "font-size": "16px", 
            "text-align": "center", 
            "margin": "0px", 
            "color": "#2f3d92",            
            "font-weight": "400",
            "--hover-color": "#c9d9e9",
            "border-radius": "15px"       
        },
        "nav-link-selected": {               # Quan es selecciona un apartat
            "background-color": "#c9d9e9", 
            "color": "#2f3d92",     
            "border-radius": "15px",       
            "border-bottom": "3px solid #2f3d92", # Línia decorativa inferior
            "font-weight": "bold"
        }
    }
)

# --- PESTANYA INICI ---
if pestanya == "Inici":
    st.info("**Estat del projecte:** En desenvolupament.")
   
    st.write("### Benvingut al simulador")
    st.write("""Aquesta web t'ajudarà a entendre l'evolució de la criptografia des dels mètodes més antics fins a la física quàntica.""")
   
    with st.expander("Principi d'Incertesa"):
        st.write("""Si no veus la web encara no és perquè no estigui acabada sinó perquè segons el principi d'incertesa no es pot veure el seu contingut i estar dins d'aquesta alhora.""")
        st.write("Progrés de la web:")
        st.progress(30)


# --- PESTANYA CÈSAR ---
elif pestanya == "Criptografia Cèsar":
    st.write("### Mètode de Substitució: Cèsar")

    # --- APARTAT TEÒRIC (DESPLEGABLE) ---
    with st.expander("Com funciona la roda del Cèsar?"):
        st.write("""
        El xifratge Cèsar és un mètode de substitució on cada lletra del text original es reemplaça 
        per una altra que es troba un nombre fix de posicions (clau) més endavant en l'alfabet.
        
        **Fes girar la roda interior** per veure com canvien les correspondències segons la clau triada:
        """)
        
        # Columna de control i columna de visió de la roda
        col_roda_ctrl, col_roda_img = st.columns([1, 1.5], vertical_alignment="center")
        
        with col_roda_ctrl:
            clau_teoria = st.slider("Tria la clau per fer girar la roda:", 0, 25, 0, key="slider_roda_teoria")
            angle = (360 / 26) * clau_teoria
            if clau_teoria == 0:
                st.info("La roda està alineada: **A** es manté com a **A**.")
            else:
                st.info(f"Amb la clau **{clau_teoria}**, la **A** es converteix en la **{abecedari[clau_teoria]}**.")

        with col_roda_img:            
            st.markdown(f"""
                <div style="position: relative; width: 320px; height: 320px; margin: 0 auto; display: flex; justify-content: center; align-items: center;">
                    <img src="data:image/png;base64,{img_cesar_gran}" style="position: absolute; width: 320px; z-index: 1;">
                    <img src="data:image/png;base64,{img_cesar_petita}" style="position: absolute; width: 320px; z-index: 2; 
                         transform: rotate(-{angle}deg); transition: transform 0.6s ease-out;">
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    # --- SIMULADOR DE XIFRATGE I ATAC ---
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
        else:
            st.warning("Primer xifra un missatge.")
    
    st.divider()

    # --- JOC INTERACTIU ---
    st.write("### 🕵️‍♀️ Missió: Desxifra el Missatge Interceptat")
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
        if st.button("⬅️ Girar Roda -1", disabled=st.session_state.clau_intent == 0):
            st.session_state.clau_intent -= 1
            st.rerun() 
        

    with col_clau:
        st.metric("Clau aplicada", f"n = {st.session_state.clau_intent}")

    with col_bt2:
        if st.button("Girar Roda +1 ➡️", disabled=st.session_state.clau_intent == 25):
            st.session_state.clau_intent += 1
            st.rerun()

    # Descodificador
    # Important: Per desxifrar, s'aplica el desplaçament invers (26 - n)
    text_provisional = CCl.xifrar_cesar(st.session_state.msg_xifrat, 26 - st.session_state.clau_intent)

    st.write(f"#### 🔍 Visualització del desxiframent amb clau n = {st.session_state.clau_intent}:")
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
        if st.button("🔄 Generar nova missió"):
            del st.session_state.joc_actiu
            st.rerun()
    else:
        with st.expander("❓ Necessites ajuda? Com funciona aquest descodificador?"):
            st.write(f"""
            Actualment estàs provant de moure tot l'alfabet **{st.session_state.clau_intent}** posicions enrere.
            Per exemple, si la clau fos 1, una **B** es convertiria en una **A**.
            Procura moure la roda fins que les paraules semblin català!
            """)






# --- PESTANYA RSA ---
elif pestanya == "Algorisme RSA":
    st.header("Criptografia Asimètrica (RSA)")
    st.write("Per desenvolupar encara")
   
    contra = st.text_input("Prova una contrasenya:", type="password")
    if contra:
        st.write("La idea és comparar la vulnerabilitat del RSA envers l'algorisme de Shor")
        st.warning("Pàgina en construcció.")
 
# --- PESTANYA BB84 ---
elif pestanya == "Protocol Quàntic BB84":
    st.header("Simulador Quàntic BB84")
   
    st.write("*(Aquí anirà una mica de teoria)*")
   
    if st.button("Simular enviament de fotons"):
        st.write("Per desenvolupar")
 
# Peu de pàgina
st.divider()
st.caption("Treball de Recerca 2025-2026, Asier Romero | Desenvolupat amb Python i Streamlit")