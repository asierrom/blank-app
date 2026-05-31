"""
=============================================================================
PROJECTE: Desxifra'm! - Plataforma de Simulació de Protocols Criptogràfics
FITXER: desxifram_app.py
AUTOR: Asier Romero
CURS: 2n de Batxillerat (Maristes Rubí)
DATA DE CREACIÓ: Març 2026
ÚLTIMA MODIFICACIÓ: Maig 2026
VERSIÓ: 1.0
DESCRIPCIÓ: Programa principal i punt d'entrada de la plataforma web. 
            Gestiona la configuració global de la interfície (estils CSS,
            tipografies), el menú d'enrutament horitzontal i
            les diferents pestanyes i mòduls.
=============================================================================
"""
import streamlit as st
from streamlit_option_menu import option_menu
from pestanyes import pestanya_CriptoClàssica as CESAR
from pestanyes import pestanya_RSA as RSA
from pestanyes import pestanya_ProtocolBB84 as BB84

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
st.set_page_config(page_title="Desxifra'm!", page_icon="Logo_Desxifram.png", layout="wide")
 
col_logo, col_titol = st.columns([0.9,9], vertical_alignment="center")
with col_logo:
    st.image("Logo_Desxifram.png", width=500) 
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


# PESTANYA INICI
if pestanya == "Inici":
    # Inicialització de variable per comprovar si en Quby està despert
    if "quby_despert" not in st.session_state:
        st.session_state.quby_despert = False

    col1, col2 = st.columns([1, 2])

    if not st.session_state.quby_despert: # Si en Quby dorm
        with col1:
            st.image("QubyDormint.png", use_container_width=True)
            
        with col2:
            st.write("#### Shht... En Quby està en superposició.")
            st.write("""
                    Ara mateix, està adormit. O despert? En el món quàntic, fins que no el mesuris, 
                    està tècnicament en els dos estats alhora!
                    """)
            st.write("Necessitem el teu ajut per començar la missió. Què vols fer?")
            
            # Botó per despertar-lo
            if st.button("Fes col·lapsar en Quby (Desperta'l!)"):
                st.session_state.quby_despert = True
                st.rerun() # Recarrega la pàgina per mostrar els canvis

    else: # Si en Quby està despert
            
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image("QubySalutació.png", use_container_width=True)
            
        with col2:
            st.info("**QUBY DESPERTAT!**")
            st.caption("Navega pel menú superior per començar la primera missió.")
            
            if st.button("Tornar a adormir"):
                st.session_state.quby_despert = False
                st.rerun()

# PESTANYA CÈSAR
elif pestanya == "Criptografia Cèsar":
    CESAR.mostrar_pagina_cesar()

# PESTANYA RSA
elif pestanya == "Algorisme RSA":
    RSA.mostrar_pagina_RSA()

# PESTNYA BB84
elif pestanya == "Protocol Quàntic BB84":
    menu = st.tabs(["Conceptes Quàntics", "Simulador BB84"])

    with menu[0]:
        BB84.mostrar_introduccio_BB84()

    with menu[1]:
        BB84.mostrar_simulacio_bb84()

# Peu de pàgina
st.divider()
st.caption("Treball de Recerca 2025-2026, Asier Romero | Desenvolupat amb Python i Streamlit")