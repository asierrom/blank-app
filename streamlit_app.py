import streamlit as st
import time
import M1_CriptoClàssica as CCl
import os
import base64

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

# Configuració inicial de la pàgina
st.set_page_config(page_title="Desxifra'm!", page_icon="Logo_desxifram.png", layout="wide")
 
col_logo, col_titol = st.columns([0.9,9], vertical_alignment="center")
with col_logo:
    st.image("Logo_desxifram.png", width=500) 
with col_titol:
    st.title("Desxifra'm!")
st.subheader("Simulador de Protocols Criptogràfics")
 
pestanya_inici, pestanya_cesar, pestanya_rsa, pestanya_bb84 = st.tabs([
    "🏠 Inici",
    "📜 Criptografia Cèsar",
    "🔢 Algorisme RSA",
    "⚛️ Protocol BB84 (Quàntic)"
])
 
# --- PESTANYA INICI ---
with pestanya_inici:
    st.info("**Estat del projecte:** En desenvolupament.")
   
    st.write("### Benvingut al simulador")
    st.write("""Aquesta web t'ajudarà a entendre l'evolució de la criptografia des dels mètodes més antics fins a la física quàntica.""")
   
    with st.expander("Principi d'Incertesa"):
        st.write("""Si no veus la web encara no és perquè no estigui acabada sinó perquè segons el principi d'incertesa no es pot veure el seu contingut i estar dins d'aquesta alhora.""")
        st.write("Progrés de la web:")
        st.progress(30)

 # --- PESTANYA CÈSAR ---
@st.cache_data
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
img_cesar_gran = get_base64("Cesar_gran.png")
img_cesar_petita = get_base64("Cesar_petita.png")

with pestanya_cesar:
    st.header("Mètode de Substitució: Cèsar", anchor=False)

    # --- APARTAT TEÒRIC INTERACTIU (DESPLEGABLE) ---
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
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Configuració", anchor=False)
        missatge_original = st.text_input("Missatge per a l'Alice:", "Introdueix el missatge a codificar")
        clau_xifrar = st.slider("Clau de desplaçament (n):", 1, 25, 1, key="slider_xifrar")
        
        if st.button("Xifrar missatge"):
            missatge_xifrat = CCl.xifrar_cesar(missatge_original, clau_xifrar)
            st.session_state['xifrat'] = missatge_xifrat
            st.success(f"Missatge xifrat: {missatge_xifrat}")

    with col2:
        st.subheader("Atac de Força Bruta (Eve)", anchor=False)
        if 'xifrat' in st.session_state:
            if st.button("🚀 Iniciar Atac"):
                intent, temps = CCl.desxiframent_cesar(st.session_state['xifrat'], missatge_original)
                st.metric("Temps de desxiframent", f"{temps:.6f} s")
                st.write(f"L'espia ha desxifrat: **{intent}**")
        else:
            st.warning("Primer xifra un missatge.")

# --- PESTANYA RSA ---
with pestanya_rsa:
    st.header("Criptografia Asimètrica (RSA)")
    st.write("Per desenvolupar encara")
   
    contra = st.text_input("Prova una contrasenya:", type="password")
    if contra:
        st.write("La idea és comparar la vulnerabilitat del RSA envers l'algorisme de Shor")
        st.warning("Pàgina en construcció.")
 
# --- PESTANYA BB84 ---
with pestanya_bb84:
    st.header("Simulador Quàntic BB84")
   
    # Espai per a les teves imatges de qubits
    st.write("*(Aquí anirà una mica de teoria)*")
   
    if st.button("Simular enviament de fotons"):
        st.write("Per desenvolupar")
 
# Peu de pàgina
st.divider()
st.caption("Treball de Recerca 2025-2026, Asier Romero | Desenvolupat amb Python i Streamlit")