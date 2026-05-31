"""
=============================================================================
PROJECTE: Desxifra'm! - Plataforma de Simulació de Protocols Criptogràfics
FITXER: pestanya_RSA.py
AUTOR: Asier Romero
CURS: 2n de Batxillerat (Maristes Rubí)
DATA DE CREACIÓ: Abril 2026
ÚLTIMA MODIFICACIÓ: Maig 2026
VERSIÓ: 1.0
DESCRIPCIÓ: Interfície d'usuari per al Mòdul 2 (Algorisme RSA).
=============================================================================
"""
import streamlit as st
import numpy as np
import M2_RSA as RSA   # Importem el nostre mòdul lliure d'Streamlit

def mostrar_pagina_RSA():
    seccio_teoria_RSA()
    st.divider()
    num_digits, N = seccio_seleccio_N()
    seccio_grafic_RSA_Shor(num_digits, N)
    st.divider()
    seccio_experiment_imatges()


def seccio_teoria_RSA():
    st.write("### Criptografia Asimètrica (RSA)")
    with st.expander("Els ordinadors quàntics: el futur o la fi de la seguretat?"):
        st.markdown("""
        #### Què és l'RSA?
        Per crear una clau RSA, es trien nombres primers grans ($p$ i $q$) i es multipliquen per obtenir $N$.
        * **La clau pública ($N$):** És el producte de la multiplicació i qualsevol persona pot veure-la.
        * **La clau privada:** Són els dos nombres originals ($p$ i $q$). 
        
        Per a un ordinador clàssic, multiplicar és fàcil, però factoritzar $N$ en els seus dos nombres primers és gairebé impossible si el número és gran. Trigaria milers d'anys!
        """)
        
        st.markdown("""
        #### L'algorisme de Shor
        Aquí entra la computació quàntica. L'algorisme de Shor no intenta endevinar els números per força bruta.
        Amb ordinadors quàntics, encara que actualment són massa petits per fer-ho amb números grans, es podria descobrir la clau en un període de temps ràpid, i **totes les claus mundials esdevindrien insegures**!
        """)

def seccio_seleccio_N():
    st.write("### Experiment: El teu número vs l'Algorisme de Shor")
    st.markdown("Aquesta eina et permet visualitzar on se situa el teu propi número **$N$** (producte de dos nombres primers) en la corba de complexitat de factorització.")

    # Introducció de p i q per part de l'usuari
    usar_rsa2048 = st.checkbox("Usar estàndard RSA-2048 (620 dígits)")

    if usar_rsa2048:
        num_digits = 620
        N = 10**620
        st.info("💡 **RSA-2048** *(com les contrasenyes dels bancs)* utilitza un nombre compost amb uns 620 dígits decimals.")
        st.latex(r"N = 10^{620}")
    else:
        col1, col2 = st.columns(2)
        with col1:
            exp_p = st.slider("Exponent per al primer $p$ ($10^p$)", min_value=1, max_value=400, value=30)    
        with col2:
            exp_q = st.slider("Exponent per al primer $q$ ($10^q$)", min_value=1, max_value=400, value=30)
        N = 10**exp_p * 10**exp_q
        num_digits = exp_p + exp_q
        st.latex(rf"N = 10^{{{exp_p}}} \cdot 10^{{{exp_q}}} = 10^{{{num_digits}}}")
        st.info(f"El teu número $N$ té **{num_digits}** dígits.")
    
    return num_digits, N

def seccio_grafic_RSA_Shor(num_digits, N):
    if st.button("Calcula i Visualitza"):
        if num_digits < 5:
            st.warning("Per observar l'efecte correctament, és recomanable introduir nombres primers molt més grans.")
                
        # Crida als mòduls
        digits_array, gnfs_array, shor_array = RSA.calcular_dades_grafic(num_digits)
        gnfs_N, shor_N, ratio = RSA.calcular_punt_N(num_digits, N)
        fig = RSA.crear_grafic_comparacio(num_digits, gnfs_N, shor_N, digits_array, gnfs_array, shor_array)
        
        # Mostra del gràfic de matplotlib 
        col_grafic, col_missatge = st.columns([2,1])
        with col_grafic:
            st.pyplot(fig)
        
        # Anàlisi dels resultats
        with col_missatge:
            if ratio > 1:
                exponent = int(np.floor(np.log10(ratio)))
                base = ratio / (10 ** exponent)
                st.metric(label="Factor d'eficiència de Shor", value=f"{base:.2f} × $10^{{{exponent}}}$")
                
                st.error(f"⚠️ El sistema és vulnerable a la computació quàntica. L'algorisme de Shor és {base:.2f} × $10^{{{exponent}}}$ vegades més eficient que el clàssic.")
                st.image("QubyShor.png", use_container_width=True)

            else:
                st.write("Per a aquest número, l'ordinador clàssic és més eficaç que el quàntic.")
                st.success("✅ És més eficient usar un ordinador convencional per desencriptar la clau.")


# Apartat d'experiment amb imatges:
def seccio_experiment_imatges():
    st.write("### Experiment: El perill de reutilitzar la clau")
    
    # Selecció de les imatges
    diccionari_imatges = {
        "Quby": "Quby.png",
        "Cadenat" : "Cadenat.png",
        "Jeroglífic Egipci" :"Jeroglífic.jpg",
        "Àtom": "Àtom.png",
        "Màquina Enigma": "MàquinaEnigma.jpg",
        "Puja la teva pròpia...": ""
    }
    opcions = list(diccionari_imatges.keys())

    col_sel1, col_sel2, col3 = st.columns(3)
    with col_sel1:
        seleccio_a = st.selectbox("Escull la Imatge A:", opcions, key="sel_img_a")
        if seleccio_a == "Puja la teva pròpia...":
            imatge_a = st.file_uploader("Puja Imatge A", type=["png", "jpg", "jpeg"], key="upload_a")
        else:
            imatge_a = diccionari_imatges[seleccio_a]

    with col_sel2:
        seleccio_b = st.selectbox("Escull la Imatge B:", opcions, index=1, key="sel_img_b")
        if seleccio_b == "Puja la teva pròpia...":
            imatge_b = st.file_uploader("Puja Imatge B", type=["png", "jpg", "jpeg"], key="upload_b")
        else:
            imatge_b = diccionari_imatges[seleccio_b]

    with col3:
        st.image("QubyXifrar.png", use_container_width=True)

    # Tractament de les imatges
    if imatge_a and imatge_b:
        try:
            # Preparació 
            matriu_a = RSA.preparar_img(imatge_a)
            matriu_b = RSA.preparar_img(imatge_b)

            # Gestió de la clau a session state
            if 'clau_experiment' not in st.session_state:
                st.session_state.clau_experiment = RSA.generar_clau_aleatoria(matriu_a.shape)
            
            clau = st.session_state.clau_experiment

            # Xifratge de les imatges
            xifrat1 = RSA.xifrar_imatges_xor(matriu_a, clau)
            xifrat2 = RSA.xifrar_imatges_xor(matriu_b, clau)
            revelat = RSA.superposicio_imatges_xor(xifrat1, xifrat2)

            # Mostra de resultats a l'usuari
            with st.expander("Per què és important que la clau sigui única?"):
                st.write("""
                Basat amb el mètode *one-time pad*, on s'usa una clau totalment aleatòria per encriptar un missatge, xifrarem dues imatges amb XOR.        
                **XOR** és una operació que gira els píxels. Si s'aplica dues vegades la mateixa clau, el segon gir desfà el primer ($X \oplus X = 0$).
                Quan xifrem dues imatges amb la mateixa clau i les superposem, la clau s'anul·la i revela els dos secrets barrejats.
                """)
                st.markdown("#### Procés de xifratge pas a pas:")
                
                st.write("##### Imatge A")
                c1, c2, c3 = st.columns(3)
                c1.image(matriu_a, caption="1. Imatge Original A", use_container_width=True)
                c2.image(clau, caption="2. Clau Aleatòria", use_container_width=True)
                c3.image(xifrat1, caption="3. Imatge A Xifrada", use_container_width=True)

                st.write("##### Imatge B")
                c4, c5, c6 = st.columns(3)
                c4.image(matriu_b, caption="1. Imatge original B", use_container_width=True )
                c5.image(clau, caption="2. MATEIXA Clau", use_container_width=True)
                c6.image(xifrat2, caption="3. Imatge B Xifrada", use_container_width=True)

                st.markdown("##### Resultat de l'Atac (Superposició)")
                cf1, cf2 = st.columns([2, 1.7])
                cf1.write("En ajuntar els dos sorolls, la clau desapareix:")
                cf1.write("$$(A \oplus Clau) \oplus (B \oplus Clau) = A \oplus B$$")
                cf2.image(revelat, caption="Imatges xifrades superposades", width=400)
            
            # Resum final
            res1, res2, res3 = st.columns(3)
            res1.image(xifrat1, caption="Xifrat A", use_container_width=True)
            res2.image(xifrat2, caption="Xifrat B", use_container_width=True)
            res3.image(revelat, caption="Superposició (A XOR B)", use_container_width=True)

        except Exception as e:
            st.error(f"Error en les imatges: {e}") # Si dona error informa a l'usuari del tipus d'error