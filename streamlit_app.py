import streamlit as st

st.set_page_config(page_title="Desxifra'm!", page_icon="🔐")

st.title("🔐 Desxifra'm!")
st.subheader("Simulador de Protocols Criptogràfics")

# Missatge d'estat
st.info(" **Estat del projecte:** En desenvolupament .")

# Contingut provisional
st.markdown("""
### PÀGINA EN DESENVOLUPAMENT

---
""")

with st.expander("Missatge"):
    st.write("""
    Si no veus la web encara no és perquè no estigui acabada sinó perquè segons el principi d'incertesa no es pot veure el seu contingut i estar dins d'aquesta alhora.
    """)

st.write("Progrés de la web:")
st.progress(35)

st.caption("Treball de Recerca 2025-2026, Asier Romero | Desenvolupat amb Python i Streamlit")
