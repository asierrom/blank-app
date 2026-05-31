import streamlit as st
import numpy as np
import M3_ProtocolBB84_Introducció as IntroBB84
import M3_ProtocolBB84_SimulacióBB84 as BB84
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector

# Diccionari de configuració dels estats BB84 (Definit internament al mòdul)
ESTATS = {
    (0, "Z"): {"nom": "|0⟩", "color": "#4A90D9", "color_suau": "#EFF6FF", "descripcio": "Estat de la base rectilínia (Z) que representa el bit 0 clàssic."},
    (1, "Z"): {"nom": "|1⟩", "color": "#E8534A", "color_suau": "#FEF2F2", "descripcio": "Estat de la base rectilínia (Z) que representa el bit 1 clàssic."},
    (0, "X"): {"nom": "|+⟩", "color": "#27AE60", "color_suau": "#F0FDF4", "descripcio": "Estat de superposició diagonal (X). Al mesurar en base Z té un 50% de donar 0 o 1."},
    (1, "X"): {"nom": "|−⟩", "color": "#F39C12", "color_suau": "#FFFBEB", "descripcio": "Estat de superposició diagonal (X) amb fase invertida. Superposició màxima equitativa."}
}

def mostrar_introduccio_BB84():
    # Genera la pestanya de teoria de conceptes quàntics
    st.write("### Conceptes clau")
    
    # EXPANDER 1- SUPERPOSICIÓ
    with st.expander("Superposició: Bit vs Qubit", expanded=True):
        st.markdown("#### Del bit clàssic al Qubit")
        st.markdown("""
            **Un bit clàssic** sempre és **0** o **1**, com un interruptor de llum o bé està obert o bé tancat.
            
            En canvi, **un qubit** pot estar en **superposició**: una combinació d'ambdós estats alhora, 
            fins que el *mesurem* i "col·lapsa" a un resultat definitiu.
            
            La superposició és una propietat fonamental de la mecànica quàntica, 
            descrita matemàticament per l'**equació d'estat**:
            """)
        st.latex(r"|\psi\rangle = \alpha\,|0\rangle + \beta\,|1\rangle")
        col1, col2 = st.columns([1,1])
        with col1:
            st.markdown("""
                On **α** i **β** són amplituds complexes que compleixen:
                
                $$|\\alpha|^2 + |\\beta|^2 = 1$$

                - $|\\alpha|^2$ → probabilitat de mesurar **0**  
                - $|\\beta|^2$ → probabilitat de mesurar **1**  
                
                Quan mesurem, el qubit **col·lapsa irreversiblement** a un dels dos estats. Però, fins que no es fa aquesta mesura, el qubit pot ser 0 i 1 alhora.
                """)
        
        with col2:
            st.image("QubySuperposició.png", use_container_width=True)
        
        st.divider()
        st.markdown("#### Experiment: Construeix i visualitza el teu Qubit")
        st.markdown("Ajusta les probabilitats i veu com canvia l'estat quàntic.")
        
        st.markdown("##### Ajusta la superposició")
        prob_1 = st.slider("Probabilitat de mesurar $|1\\rangle$, és a dir, $|\\beta|^2$",
                           0.0, 1.0, 0.1, 0.01, 
                           help="Mou el lliscador per canviar la probablitat que aparegui cada estat. Al 50% tens superposició màxima.")
        prob_0 = 1 - prob_1
        beta = np.sqrt(prob_1)
        alpha = np.sqrt(prob_0)
        
        if prob_1 == 0.50:
            st.success("**Superposició màxima!** El qubit té exactament un 50% de probabilitat per a cada estat. "
                    "Això correspon a l'estat $|+\\rangle$ de la base de Hadamard, fonamental al BB84.")
        elif prob_1 == 0.0:
            st.info("**Estat $|0\\rangle$ pur.** No hi ha superposició, és un bit clàssic 0.")
        elif prob_1 == 1.0:
            st.info("**Estat $|1\\rangle$ pur.** No hi ha superposició, és un bit clàssic 1.")
            
        st.latex(rf"|\psi\rangle = {alpha:.2f}\,|0\rangle + {beta:.2f}\,|1\rangle")
        
        col_bloch, col_probs = st.columns([0.8, 0.9])
        with col_bloch:
            st.markdown("**Esfera de Bloch** - representació gràfica del qubit")
            qc = QuantumCircuit(1)
            qc.initialize([alpha, beta], 0)
            state = Statevector.from_instruction(qc)
            fig_bloch = IntroBB84.bloch_fig(state, title="", figsize=(2.5, 2.5))
            st.pyplot(fig_bloch, use_container_width=False )
            st.caption("La fletxa rosa indica l'estat del qubit. Al pol nord = $|0\\rangle$, pol sud = $|1\\rangle$.")
            
        with col_probs:
            st.markdown("**Probabilitats de mesura**")
            st.pyplot(IntroBB84.prob_bar_fig(prob_0, prob_1), use_container_width=False)
            
            st.markdown("**Simulació de 100 mesures**")
            if st.button("Simular 100 mesures d'aquest qubit"):
                fig_sim, _, _ = IntroBB84.simular_100_mesures(prob_0, prob_1)
                st.pyplot(fig_sim, use_container_width=False)
                st.caption(f"Teòricament hauríem d'obtenir: {prob_0*100:.0f}% $|0\\rangle$ i {prob_1*100:.0f}% $|1\\rangle$")


    # EXPANDER 2- ESTATS DEL BB84
    with st.expander("Els 4 estats del protocol BB84", expanded=True):
        st.markdown("#### Com codifica Alice la informació?")
        st.markdown("""
                    Al protocol BB84, Alice vol enviar bits a Bob de forma segura. Per fer-ho, converteix cada bit en un qubit escollint:

                    1. Quin bit vol enviar → **0** o **1** 
                    2. Quina base de codificació fa servir → **Z** (rectilínia) o **X** (diagonal)

                    Combinant-los, té **4 estats possibles** per enviar. La gràcia és que Eve, si intercepta, no sap quina base ha usat l'Alice i això la delata estadísticament.
                    """)
        
        st.markdown("#### Els 4 estats:")
        cols = st.columns(4)
        # Columna 1, estat |0⟩
        estat1 = ESTATS[(0, "Z")]
        html_col1 = f"""
        <div style="background:{estat1['color_suau']}; border:2.5px solid {estat1['color']}; border-radius:14px; padding:14px 10px; text-align:center;">
            <div style="font-size:2rem; font-weight:900; color:{estat1['color']};">{estat1['nom']}</div>
            <div style="font-size:0.82rem; color:#555;">Bit <b>0</b> · Base <b>Z</b></div>
        </div>
        """
        cols[0].markdown(html_col1, unsafe_allow_html=True)

        # Columna 2, estat |1⟩
        estat2 = ESTATS[(1, "Z")]
        html_col2 = f"""
        <div style="background:{estat2['color_suau']}; border:2.5px solid {estat2['color']}; border-radius:14px; padding:14px 10px; text-align:center;">
            <div style="font-size:2rem; font-weight:900; color:{estat2['color']};">{estat2['nom']}</div>
            <div style="font-size:0.82rem; color:#555;">Bit <b>1</b> · Base <b>Z</b></div>
        </div>
        """
        cols[1].markdown(html_col2, unsafe_allow_html=True)

        # Columna 3, estat |+⟩
        estat3 = ESTATS[(0, "X")]
        html_col3 = f"""
        <div style="background:{estat3['color_suau']}; border:2.5px solid {estat3['color']}; border-radius:14px; padding:14px 10px; text-align:center;">
            <div style="font-size:2rem; font-weight:900; color:{estat3['color']};">{estat3['nom']}</div>
            <div style="font-size:0.82rem; color:#555;">Bit <b>0</b> · Base <b>X</b></div>
        </div>
        """
        cols[2].markdown(html_col3, unsafe_allow_html=True)

        # Columna 4, estat |-⟩
        estat4 = ESTATS[(1, "X")]
        html_col4 = f"""
        <div style="background:{estat4['color_suau']}; width: 100%; border:2.5px solid {estat4['color']}; border-radius:14px; padding:14px 10px; text-align:center;">
            <div style="font-size:2rem; font-weight:900; color:{estat4['color']};">{estat4['nom']}</div>
            <div style="font-size:0.82rem; color:#555;">Bit <b>1</b> · Base <b>X</b></div>
        </div>
        """
        cols[3].markdown(html_col4, unsafe_allow_html=True)
        st.divider()

        st.markdown("#### Per què dues bases i no una?")
        st.markdown("""
                    Imagina que l'Alice i l'Eve (l'espia) parlen idiomes secrets. Imaginem que...

                    - **Base Z** és com parlar en **català**.
                    - **Base X** és com parlar en **japonès**.

                    Si l'Alice envia un missatge en català (base Z) i Eva l'intercepta sense saber quin idioma és, té un 50% de probabilitat d'interpretar-lo malament.

                    **Quan Eva mesura en la base incorrecta:**
                    - Destrueix l'estat original del qubit
                    - Obté un resultat completament aleatori
                    - Quan reenvía el qubit a Bob, ho fa malament
                    - Bob i Alice detecten l'error comparant una mostra de bits

                    Sense conèixer les bases prèviament, Eva no pot llegir ni copiar els qubits sense ser detectada. Això és el que fa que el BB84 sigui **sempre segur**.
                    """)
        st.divider()

        st.markdown("#### Experiment: Explora cada estat en detall")
        
        # Selectors d'estat interactius
        col_sel = st.columns(4)
        if "estat_selec" not in st.session_state:
            st.session_state.estat_selec = (0, "Z")
            
        # Estat |0⟩
        if col_sel[0].button("|0⟩\nBit 0 · Base Z", use_container_width=True):
            st.session_state.estat_selec = (0, "Z")
            st.rerun()

        # Estat |1⟩
        if col_sel[1].button("|1⟩\nBit 1 · Base Z", use_container_width=True):
            st.session_state.estat_selec = (1, "Z")
            st.rerun()

        # Estat |+⟩
        if col_sel[2].button("|+⟩\nBit 0 · Base X", use_container_width=True):
            st.session_state.estat_selec = (0, "X")
            st.rerun()

        # Estat |-⟩
        if col_sel[3].button("|−⟩\nBit 1 · Base X", use_container_width=True):
            st.session_state.estat_selec = (1, "X")
            st.rerun()
                
        bit_s, base_s = st.session_state.estat_selec
        info_s = ESTATS[(bit_s, base_s)]

        # NOTA D'AUTORIA: L'estructura HTML/CSS d'aquest contenidor adaptatiu 
        # per cada estat s'ha generat amb el suport de ChatGPT (OpenAI).            
        st.markdown(f'<div style="background:{info_s["color_suau"]}; border-left:5px solid {info_s["color"]}; border-radius:10px; padding:16px 20px;">'
                    f'<div style="color:{info_s["color"]}; font-size:1.5rem; font-weight:700;">{info_s["nom"]} — Bit {bit_s} en Base {base_s}</div>'
                    f'<p style="margin:0; font-size:1.05rem; color:#333;">{info_s["descripcio"]}</p></div>', unsafe_allow_html=True)
                    
        col_bl, col_inf = st.columns([1, 1.4])
        with col_bl:
            fig_sel, _ = IntroBB84.bloch_compacte(bit_s, base_s)
            st.pyplot(fig_sel, use_container_width=False)
            st.caption(
                    "L'esfera de Bloch és una manera de representar geomètricament qualsevol estat d'un qubit. "
                    "Cada punt de la superfície és un estat quàntic possible."
                    )
        with col_inf:
            st.markdown("**Equació d'estat:**")
            if base_s == "Z":
                st.latex(r"|\psi\rangle = |0\rangle" if bit_s == 0 else r"|\psi\rangle = |1\rangle")
            else:
                st.latex(r"|\psi\rangle = |{+}\rangle" if bit_s == 0 else r"|\psi\rangle = |{-}\rangle")
                
            st.divider()
            st.markdown("**Què passa quan en Bob mesura?**")
            st.pyplot(IntroBB84.mostrar_resultat_mesura(1.0 if bit_s == 0 else 0.0, 0.0 if bit_s == 0 else 1.0, info_s['color'], info_s["color_suau"]), use_container_width=False)

    # EXPANDER 3 - EXPERIMENT MESURAR QUBITS
    with st.expander("Experiment: Mesura Qubits", expanded=True):
        st.markdown("#### Experiment: Mesura Qubits")
        st.markdown("""
                    Aquí pots simular exactament el que passa quan Bob (o Eva) intenta mesurar un qubit de BB84.
                    Escull quin qubit ha enviat Alice i quina base usa Bob per mesurar.
                    """)

        col_alice, col_bob = st.columns(2)
        with col_alice:
            st.markdown("##### 👩 Alice prepara:")
            bit_alice = st.radio("Bit d'Alice:", [0, 1], horizontal=True, format_func=lambda x: f"Bit {x}", key="bit_alice_mes")
            base_alice = st.radio("Base d'Alice:", ["Z", "X"], horizontal=True, format_func=lambda b: f"Base {b}", key="base_alice_mes")
            info_a = ESTATS[(bit_alice, base_alice)]

            # NOTA D'AUTORIA: L'estructura HTML/CSS d'aquest contenidor adaptatiu 
            # per cada estat s'ha generat amb el suport de ChatGPT (OpenAI). 
            st.markdown(f"""
                        <div style="background:{info_a["color_suau"]}; border:2px solid {info_a["color"]}; border-radius:10px; padding:12px; text-align:center;">
                        <span style="font-size:1.8rem; font-weight:900; color:{info_a["color"]};">{info_a["nom"]}</span><br>
                        <span style="font-size:0.85rem;color:#555;">Bit {bit_alice} · Base {base_alice}</span>
                        </div>'""", unsafe_allow_html=True)
            fig_a, _ = IntroBB84.bloch_compacte(bit_alice, base_alice)
            st.pyplot(fig_a, use_container_width=False)
            
        with col_bob:
            st.markdown("##### 👨 Bob mesura amb:")
            base_bob = st.radio("Base de Bob:", ["Z", "X"], horizontal=True, format_func=lambda b: f"Base {b}", key="base_bob_mes")
            
            if base_alice == base_bob:
                st.success(f"✅ Bases iguals! Bob obté sempre el bit **{bit_alice}** correctament.")
            else:
                st.error("❌ Bases diferents! El resultat és completament aleatori.")
            
            st.markdown("**Probabilitats de mesura de Bob:**")
            p0_m, p1_m = IntroBB84.calcular_probabilitats_mesura(bit_alice, base_alice, base_bob)
            st.pyplot(IntroBB84.barra_probabilitat(p0_m, p1_m, info_a["color"], info_a["color_suau"], "|0⟩", "|1⟩"), use_container_width=False)
            
            st.markdown("**Simula les mesures de Bob:**")
            n_mesures = st.slider("Nombre de mesures:", 10, 500, 100, 10, key="n_mes")
            if st.button("Simular", key="btn_sim_mes"):
                fig_h, n0, n1 = IntroBB84.simular_historial_bob(n_mesures, p0_m, p1_m, info_a["color"], info_a["color_suau"])
                st.pyplot(fig_h, use_container_width=True)
                
                if not base_alice == base_bob:
                    st.warning(f"De {n_mesures} mesures, **{n0}** han donat 0, i **{n1}** han donat 1. És aleatori, i en Bob no pot saber quin bit va enviar Alice!")
                else:
                    st.success(f"Les {n_mesures} mesures han donat **{n0 if bit_alice == 0 else n1}** cops el bit {bit_alice}.")
    
        col_c1, col_c2, col3 = st.columns(3)
        with col_c1:
            st.markdown("""
                    **Quan les bases coincideixen:**
                    - Bob sempre obté el bit correcte
                    - La mesura és determinista (100% segura)
                    - Aquesta mesura forma part de la **clau final**
                    """)
        with col_c2:
            st.markdown("""
                    **Quan les bases no coincideixen:**
                    - Bob obté un resultat completament aleatori
                    - La mesura es **descarta** (Alice i Bob ho saben perquè comparen bases públicament)
                    - Eva tampoc no pot aprofitar res d'útil
                    """)
        
        with col3:
            st.image("QubyEstudiant.png", use_container_width=True)


# -------------------------------
# ----SIMULACIÓ PROTOCOL BB84----
# -------------------------------

# Funcions que indiquen si és canal públic o quàntic
def banner_canal(tipus):
    if tipus == "quantic":
        # NOTA D'AUTORIA: L'estructura HTML/CSS d'aquest contenidor adaptatiu 
        # per cada canal (públic/quàntic) s'ha generat amb el suport de ChatGPT (OpenAI).
        st.markdown("""
        <div style="background-color:#E6F2FF; border-left: 5px solid #007BFF; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
            🔵 <b>Canal quàntic</b> — La informació no pot ser interceptada sense pertorbar-la.
        </div>
        """, unsafe_allow_html=True)
    elif tipus == "public":
        st.markdown("""
        <div style="background-color:#FFF3CD; border-left: 5px solid #FFC107; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
            🟠 <b>Canal públic clàssic</b> — Tothom el pot escoltar (el Bob i l'Alice revelen quines bases han usat per mesurar els qubits, però no revelen els resultats de les mesures: els bits).
        </div>
        """, unsafe_allow_html=True)


def dibuixar_qubit(bit, base, estat, ocultar_tot=False, ocultar_base=False):
    b_text   = "?" if ocultar_base or ocultar_tot else base
    bit_text = "?" if ocultar_tot else bit

    if ocultar_tot:
        nom_estat   = "?"
        color       = "#6c757d"
        color_suau  = "#f8f9fa"
    else:
        nom_estat   = estat['nom']
        color       = estat['color']
        color_suau  = estat['color_suau']
    # NOTA D'AUTORIA: L'estructura HTML/CSS d'aquest contenidor adaptatiu 
    # per cada estat s'ha generat amb el suport de ChatGPT (OpenAI).
    html = f"""
        <div style="
            background: {color_suau};
            border: 2.5px solid {color};
            border-radius: 14px;
            padding: 14px 10px;
            text-align: center;
            margin-bottom: 6px;
        ">
        <div style="font-size:2rem; font-weight:900; color:{color};">{nom_estat}</div>
        <div style="font-size:0.82rem; color:#555; margin-top:4px;">
            Bit <b>{bit_text}</b> · Base <b>{b_text}</b>
        </div>
        </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def inicialitzar_sessio():
    if 'pas' not in st.session_state:
        st.session_state.pas = 0

def avançar(pas_desti):
    st.session_state.pas = pas_desti

# Fase 0
def mostrar_fase0():
    with st.expander("Fase 0: Configuració del protocol BB84", expanded=(st.session_state.pas == 0)):
        st.markdown("### Paràmetres Inicials:")
        col1, col2 = st.columns([2, 1.5])
        with col1:
            st.write("Abans de començar la transmissió, quants bits vol enviar l'Alice? Hi haurà una espia (l'Eve)?")
            n_bits     = st.slider("Nombre de bits a enviar", min_value=60, max_value=100, value=60)
            eve_activa = st.toggle("Activar Eve (espia)", value=False)
        with col2:
            st.image("QubyMilions.png", use_container_width=True)

        if eve_activa:
            st.info("**Eve interceptarà el canal quàntic.** Llegirà els qubits d'Alice (triant una base a l'atzar) i generarà nous qubits per enviar a Bob segons el que ella hagi mesurat. Com que no coneix les bases d'Alice, introduirà errors.")

        if st.button("Iniciar Protocol", type="primary"):
            # Generar dades Alice
            st.session_state.n_bits = n_bits
            st.session_state.eve_activa = eve_activa
            st.session_state.alice_bits, st.session_state.alice_bases = BB84.generar_dades_alice(n_bits)

            # Generar dades Eve, si s'ha escollit
            if eve_activa:
                st.session_state.eve_bases, st.session_state.eve_bits = BB84.generar_dades_eve(
                    n_bits,
                    st.session_state.alice_bits,
                    st.session_state.alice_bases,)

            # Generar dades Bob
            st.session_state.bob_bases, st.session_state.bob_bits = BB84.generar_dades_bob(
                n_bits,
                st.session_state.alice_bits,
                st.session_state.alice_bases,
                eve_activa,
                st.session_state.get('eve_bases', []),
                st.session_state.get('eve_bits',  []),)

            # Selecció aleatòria per al QBER (pas 3)
            st.session_state.qber_sample_indices = None
            avançar(1)
            st.rerun()

# Fase 1
def mostrar_fase1():
    if st.session_state.pas >= 1:
        with st.expander("Fase 1: Alice prepara i envia els qubits", expanded=(st.session_state.pas == 1)):
            banner_canal("quantic")
            st.write("Alice genera seqüències aleatòries de bits i tria una base (Rectilínia Z o Diagonal X) a l'atzar per codificar-los en qubits.")

            n_mostrar = min(24, st.session_state.n_bits) # Limitem a 24
            cols = st.columns(6)
            for i in range(n_mostrar):
                bit   = st.session_state.alice_bits[i]
                base  = st.session_state.alice_bases[i]
                estat = ESTATS[(bit, base)]
                with cols[i % 6]:
                    st.caption(f"Qubit {i+1}")
                    dibuixar_qubit(bit, base, estat, ocultar_base=False)
            
            if st.session_state.n_bits > 24:
                st.info(f"👀 S'han ocultat {st.session_state.n_bits - 24} qubits addicionals per comoditat visual.")

            if st.session_state.pas == 1:
                següent_pas = 1.5 if st.session_state.eve_activa else 2
                if st.button("Enviar pel canal quàntic →", on_click=avançar, args=(següent_pas,)):
                    pass

# Fase 1.5 (Eve)
def mostrar_fase1_5():
    if st.session_state.pas >= 1.5 and st.session_state.eve_activa:
        with st.expander("Fase 1.5: Eve intercepta els qubits de l'Alice", expanded=(st.session_state.pas == 1.5)):
            banner_canal("quantic")
            st.write("L'espia captura els qubits al vol. Com que la mecànica quàntica prohibeix clonar estats desconeguts, es veu obligada a mesurar-los triant bases a l'atzar, i enviar allò que ha mesurat a Bob.")

            encerts, pertorbats = BB84.resum_eve(
                st.session_state.n_bits,
                st.session_state.alice_bases,
                st.session_state.eve_bases,
            )

            col1, col2, col3 = st.columns([1, 1, 1.5])
            col1.metric("Bases encertades per Eve", f"{encerts} de {st.session_state.n_bits}")
            col2.metric("Qubits potencialment pertorbats", f"{pertorbats}")
            with col3:
                st.image("QubyDetectiu.png", use_container_width=True)

            st.divider()
            n_mostrar = min(24, st.session_state.n_bits) # Limitem a 24
            for i in range(n_mostrar):
                col1, col2, col3 = st.columns([1, 1.5, 1])
                base_alice = st.session_state.alice_bases[i]
                base_eve   = st.session_state.eve_bases[i]

                with col1:
                    if i == 0: st.markdown("**D'Alice**")
                    estat_a = ESTATS[(st.session_state.alice_bits[i], base_alice)]
                    dibuixar_qubit(st.session_state.alice_bits[i], "?", estat_a)

                with col2:
                    if i == 0: st.markdown("**Eve Mesura / Genera**")
                    color_text = "green" if base_alice == base_eve else "red"
                    icona      = "✅" if base_alice == base_eve else "❌ Pertorbat"
                    # NOTA D'AUTORIA: L'estructura HTML/CSS d'aquest contenidor adaptatiu 
                    # per cada estat s'ha generat amb el suport de ChatGPT (OpenAI).
                    st.markdown(
                        f"<div style='text-align:center; padding-top:20px; color:{color_text};'>"
                        f"<b>Eve tria: {base_eve}</b><br>{icona}</div>",
                        unsafe_allow_html=True,
                    )

                with col3:
                    if i == 0: st.markdown("**Cap a Bob**")
                    estat_e = ESTATS[(st.session_state.eve_bits[i], base_eve)]
                    dibuixar_qubit(st.session_state.eve_bits[i], "?", estat_e)
            if st.session_state.n_bits > 24:
                st.info(f"👀 Eve també ha interceptat {st.session_state.n_bits - 24} qubits més en segon pla.")

            if st.session_state.pas == 1.5:
                if st.button("Bob rep els qubits (pertorbats) →", on_click=avançar, args=(2,)):
                    pass
                
# Fase 2
def mostrar_fase2():
    if st.session_state.pas >= 2:
        with st.expander("Fase 2: Bob rep i mesura els qubits", expanded=(st.session_state.pas == 2)):
            col1, col2 = st.columns([1.5,1])
            with col1:
                banner_canal("quantic")
                st.write("Bob rep la seqüència de qubits. Com que no sap les bases d'Alice, ha de triar-ne a l'atzar per mesurar. A vegades coincidirà amb Alice i d'altres no. Si les bases no coincideixen, el Bob mesurarà un resultat alteatori.")

            with col2:
                st.image("QubyPlatja.png", use_container_width=True)

            if 'bob_mesurat' not in st.session_state:
                st.session_state.bob_mesurat = False

            n_mostrar = min(24, st.session_state.n_bits) # Limitem a 24
            cols = st.columns(6)
            for i in range(n_mostrar):
                with cols[i % 6]:
                    st.caption(f"Recepció {i+1}")
                    if not st.session_state.bob_mesurat and st.session_state.pas == 2:
                        dibuixar_qubit("?", "?", None, ocultar_tot=True)
                    else:
                        bit_b   = st.session_state.bob_bits[i]
                        base_b  = st.session_state.bob_bases[i]
                        estat_b = ESTATS[(bit_b, base_b)]
                        dibuixar_qubit(bit_b, base_b, estat_b)

            if st.session_state.n_bits > 24:
                st.info(f"👀 Bob ha rebut {st.session_state.n_bits - 24} qubits més en segon pla.")

            if st.session_state.pas == 2:
                if not st.session_state.bob_mesurat:
                    if st.button("Bob mesura els qubits"):
                        st.session_state.bob_mesurat = True
                        st.rerun()
                else:
                    if st.button("Anar al Canal Públic (Comparar Bases) →", type="primary", on_click=avançar, args=(3,)):
                        pass

# Fase 3
def mostrar_fase3():
    if st.session_state.pas >= 3:
        with st.expander("Fase 3: Cribatge (Sifting) i clau final", expanded=(st.session_state.pas == 3)):
            banner_canal("public")

            # Comparació de bases
            st.markdown("#### 1. Comparació de Bases")
            st.write("Alice i Bob publiquen **només les seves bases** en un canal públic. Si les bases no coincideixen, descarten els qubits perquè els resultats són aleatoris.")

            indexos_valids, clau_bruta_alice, clau_bruta_bob = BB84.calcular_clau_bruta(
                st.session_state.n_bits,
                st.session_state.alice_bits,
                st.session_state.alice_bases,
                st.session_state.bob_bits,
                st.session_state.bob_bases,
            )

            n_mostrar = min(24, st.session_state.n_bits) # Es limita a 24 perquè no hi càpiga
            cols = st.columns(n_mostrar) 
    
            for i in range(n_mostrar):
                a_base    = st.session_state.alice_bases[i]
                b_base    = st.session_state.bob_bases[i]
                coincideix = (a_base == b_base)
                with cols[i]:
                    # NOTA D'AUTORIA: L'estructura HTML/CSS d'aquest contenidor adaptatiu 
                    # per cada bit s'ha generat amb el suport de ChatGPT (OpenAI).
                    st.markdown(
                        f"<div style='text-align:center; font-size:12px;'>"
                        f"<b>A:</b> {a_base}<br><b>B:</b> {b_base}</div>",
                        unsafe_allow_html=True,)
                    if coincideix:
                        st.markdown("<div style='text-align:center;'>✅</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='text-align:center; opacity:0.3;'>❌</div>", unsafe_allow_html=True)
            if st.session_state.n_bits > 24:
                st.info(f"👀 S'han comparat {st.session_state.n_bits - 24} bases més en segon pla.")

            st.divider()
            
            # Clau bruta
            st.markdown("#### 2. Clau bruta (Sifted Key)")
            
            # NOTA D'AUTORIA: L'estructura HTML/CSS d'aquest contenidor adaptatiu 
            # per cada estat s'ha generat amb el suport de ChatGPT (OpenAI).
            html_alice = ""
            for b in clau_bruta_alice:
                if b == 0:
                    color = '#007BFF'
                else:
                    color = '#DC3545'
                
                bloc_html = f"<span style='display:inline-block; width:25px; height:25px; background:{color}; color:white; text-align:center; border-radius:3px; margin:2px;'>{b}</span>"
                html_alice = html_alice + bloc_html 

            html_bob = ""
            for b in clau_bruta_bob:
                if b == 0:
                    color = '#007BFF'
                else:
                    color = '#DC3545'
                
                bloc_html = f"<span style='display:inline-block; width:25px; height:25px; background:{color}; color:white; text-align:center; border-radius:3px; margin:2px;'>{b}</span>"
                html_bob = html_bob + bloc_html 

           
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Bits d'Alice:**<br> {html_alice}", unsafe_allow_html=True)
                st.markdown(f"**Bits de Bob:**<br> {html_bob}", unsafe_allow_html=True)
            with col2:
                st.image("QubyEstrelles.png", use_container_width=True)
            st.divider()

            # Verificació QBER
            st.markdown("#### 3. Verificació d'Intercepció (QBER) i Sacrifici de Bits")
            st.write("Per assegurar-se que no hi ha actuat cap espia, l'Alice i el Bob escullen un tros de la seva clau i comproven que no estigui alterada. Si veuem que un dels resultats no els coincideix, significa que algú els ha intentat robar la clau.")

            if len(indexos_valids) > 0:
                if st.session_state.qber_sample_indices is None:
                    st.session_state.qber_sample_indices = BB84.seleccionar_mostra_qber(len(indexos_valids))

                mostra_idx = st.session_state.qber_sample_indices
                errors, qber = BB84.calcular_qber(clau_bruta_alice, clau_bruta_bob, mostra_idx)

                col_mostra, col_restants = st.columns(2)

                with col_mostra:
                    st.markdown("**Mostra Comparada (es descarta):**")
                    html_mostra = ""
                    for idx_local in mostra_idx:
                        b_alice = clau_bruta_alice[idx_local]
                        b_bob   = clau_bruta_bob[idx_local]
                        # NOTA D'AUTORIA: L'estructura HTML/CSS d'aquest contenidor adaptatiu 
                        # per cada bit s'ha generat amb el suport de ChatGPT (OpenAI).
                        if b_alice != b_bob:
                            html_mostra += f"<span style='padding:4px; background:#FDEEEA; border:1px solid #DC3545; color:#DC3545; font-weight:bold; margin:2px; border-radius:4px;'>A:{b_alice} ≠ B:{b_bob}</span> "
                        else:
                            html_mostra += f"<span style='padding:4px; background:#E9F7EF; border:1px solid #28A745; color:#28A745; font-weight:bold; margin:2px; border-radius:4px;'>A:{b_alice} = B:{b_bob}</span> "
                    st.markdown(html_mostra, unsafe_allow_html=True)

                with col_restants:
                    st.markdown("**Bits Restant (se'ls queden en secret):**")
                    html_restants = ""
                    for i in range(len(clau_bruta_bob)):
                        # Es mira si la posició 'i' no està a la mostra 
                        if i not in mostra_idx:
                            bit = clau_bruta_bob[i]
                            bloc = f"<span style='display:inline-block; width:25px; height:25px; background:#6c757d; color:white; text-align:center; border-radius:3px; margin:2px;'>{bit}</span>"
                            html_restants = html_restants + bloc
                    st.markdown(html_restants, unsafe_allow_html=True)

                st.divider()

                # Indicador de QBER
                col1, col2, col3 = st.columns([2, 1, 2])
                with col1:
                    if qber == 0:
                        st.success(f"✅ **Canal Segur (QBER = {qber:.1f}%)**: No hi ha espies. Els bits restants són vàlids!")
                    else:
                        st.error(f"🚨 **EVE DETECTADA (QBER = {qber:.1f}%)**: L'espia ha pertorbat massa bits en mesurar-los. **S'abandona el protocol!**")
                with col2:
                    st.metric("Taxa d'error (QBER)", f"{qber:.1f}%")
                with col3:
                    if qber == 0:
                        st.image("QubyFinal1.png", use_container_width=True)
                    else:
                        st.image("QubyFinal2.png", use_container_width=True)

                # 3d — Clau Final
                if qber == 0:
                    clau_final = BB84.obtenir_clau_final(clau_bruta_alice, mostra_idx)
                    st.markdown("#### 4. Clau Final Secreta")
                    st.write("Aquesta és la clau neta, lliure de la mostra pública i llista per encriptar:")
                    # NOTA D'AUTORIA: L'estructura HTML/CSS d'aquest contenidor adaptatiu 
                    # per cada nombre de la clau s'ha generat amb el suport de ChatGPT (OpenAI).
                    html_final = ""
                    for b in clau_final:
                        bloc = f"<span style='display:inline-block; font-size:22px; font-weight:bold; padding:6px 12px; background:#E6F2FF; border:2px solid #007BFF; color:#007BFF; border-radius:8px; margin:3px;'>{b}</span>"
                        html_final = html_final + bloc
                    st.markdown(f"<div style='text-align:center; padding:10px;'>{html_final}</div>", unsafe_allow_html=True)

            if st.button("Reiniciar Simulació"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

# Execució del programa
def mostrar_simulacio_bb84():
    inicialitzar_sessio()
    mostrar_fase0()
    mostrar_fase1()
    mostrar_fase1_5()
    mostrar_fase2()
    mostrar_fase3()