import streamlit as st
import time
import M1_CriptoClàssica as CCl

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
        st.write("""
        Si no veus la web encara no és perquè no estigui acabada sinó perquè segons el principi d'incertesa no es pot veure el seu contingut i estar dins d'aquesta alhora.""")
        st.write("Progrés de la web:")
        st.progress(45)
 
# --- PESTANYA CÈSAR ---
with pestanya_cesar:
    st.header("Mètode de Substitució: Cèsar")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Configuració")
        missatge_original = st.text_input("Missatge per a l'Alice:", "HOLA")
        clau_xifrar = st.slider("Clau de desplaçament (n):", 1, 25, 1, key="slider_xifrar")
        
        if st.button("Xifrar missatge"):
            missatge_xifrat = CCl.xifrar_cesar(missatge_original, clau_xifrar)
            st.session_state['xifrat'] = missatge_xifrat
            st.success(f"Missatge xifrat: {missatge_xifrat}")

    with col2:
        st.subheader("Atac de Força Bruta (Eve)")
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
        st.write("Aquí anirà el càlcul de combinatòria per demostrar la seguretat matemàtica.")
        st.warning("Pàgina en construcció.")
 
# --- PESTANYA BB84 ---
with pestanya_bb84:
    st.header("Simulador Quàntic BB84")
    st.write("Aquí simularem l'enviament de fotons.")
   
    # Espai per a les teves imatges de qubits
    st.write("*(Aquí aniran les teves imatges de l'esfera de Bloch)*")
   
    if st.button("Simular enviament de fotons"):
        st.write("Simulant bases i polarització...")
 
# Peu de pàgina
st.divider()
st.caption("Treball de Recerca 2025-2026, Asier Romero | Desenvolupat amb Python i Streamlit")