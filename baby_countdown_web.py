import streamlit as st
from datetime import datetime, timedelta
import json
import os
import time
from PIL import Image, ImageDraw, ImageFont

# 1. Configurazione Iniziale e SEO della Piattaforma Ultimate con Area Riservata
st.set_page_config(
    page_title="Nascita Premium Suite - Area Riservata",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Database sicuro degli utenti per l'accesso (Verifica diretta delle credenziali)
UTENTI_DB = {
    "dottoressa": "password123",
    "mamma": "mamma2026"
}

# Funzione per gestire il database dei dati clinici degli utenti loggati
def carica_dati_utente(username):
    file_nome = f"dati_{username}.json"
    if os.path.exists(file_nome):
        try:
            with open(file_nome, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}

def salva_dati_utente(username, dati):
    file_nome = f"dati_{username}.json"
    with open(file_nome, "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False, indent=4)

# Funzione per determinare la dimensione del feto in base alle settimane
def ottieni_dimensione_frutto(settimane):
    if settimane <= 4: return "un semino di papavero 🌾 (0.5 mm)"
    elif settimane <= 8: return "un mirtillo 🫐 (1.3 cm)"
    elif settimane <= 12: return "un lime 🍋 (5.4 cm)"
    elif settimane <= 16: return "un avocado 🥑 (11.6 cm)"
    elif settimane <= 20: return "un mango 🥭 (25.6 cm)"
    elif settimane <= 24: return "una spiga di mais 🌽 (30 cm)"
    elif settimane <= 28: return "una melanzana 🍆 (37.6 cm)"
    elif settimane <= 32: return "una zucca gialla 🎃 (42.4 cm)"
    elif settimane <= 36: return "un melone 🍈 (47.4 cm)"
    else: return "una anguria 🍉 (51.2 cm)"

# Calcolo automatico del segno zodiacale predittivo
def ottieni_zodiaco(data):
    giorno = data.day
    mese = data.month
    if (mese == 3 and giorno >= 21) or (mese == 4 and giorno <= 19): return "Ariete ♈"
    elif (mese == 4 and giorno >= 20) or (mese == 5 and giorno <= 20): return "Toro ♉"
    elif (mese == 5 and giorno >= 21) or (mese == 6 and giorno <= 20): return "Gemelli ♊"
    elif (mese == 6 and giorno >= 21) or (mese == 7 and giorno <= 22): return "Cancro ♋"
    elif (mese == 7 and giorno >= 23) or (mese == 8 and giorno <= 22): return "Leone ♌"
    elif (mese == 8 and giorno >= 23) or (mese == 9 and giorno <= 22): return "Vergine ♍"
    elif (mese == 9 and giorno >= 23) or (mese == 10 and giorno <= 22): return "Bilancia ♎"
    elif (mese == 10 and giorno >= 23) or (mese == 11 and giorno <= 21): return "Scorpione ♏"
    elif (mese == 11 and giorno >= 22) or (mese == 12 and giorno <= 21): return "Sagittario ♐"
    elif (mese == 12 and giorno >= 22) or (mese == 1 and giorno <= 19): return "Capricorno ♑"
    elif (mese == 1 and giorno >= 20) or (mese == 2 and giorno <= 18): return "Acquario ♒"
    else: return "Pesci ♓"
# Gestione dello stato di Login nella sessione web
if 'autenticato' not in st.session_state:
    st.session_state.autenticato = False
    st.session_state.username = ""

# Styling CSS Avanzato per la Login Page e la Dashboard di Lusso
gradient = "linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%)"
primary_color = "#6366F1"
accent_box = "#F1F3F5"

st.markdown(f"""
    <style>
    .stApp {{ background: {gradient} !important; }}
    h1, h2, h3, h4, h5, h6, p, label, span {{ font-family: '-apple-system', BlinkMacSystemFont, 'Inter', sans-serif !important; }}
    
    .ultimate-card {{
        background: #FFFFFF !important;
        border-radius: 40px !important;
        padding: 50px !important;
        box-shadow: 0 40px 80px -15px rgba(0,0,0,0.06) !important;
        border: 1px solid rgba(255,255,255,0.7) !important;
        margin-top: 20px !important;
    }}
    .login-box {{
        background: #FFFFFF !important;
        padding: 40px !important;
        border-radius: 24px !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
        border: 1px solid #E2E8F0 !important;
        margin-top: 50px !important;
    }}
    .dashboard-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 20px;
        margin-top: 30px;
    }}
    .dashboard-box {{
        background: {accent_box} !important;
        border-radius: 24px !important;
        padding: 25px !important;
        text-align: center !important;
        transition: all 0.35s ease;
    }}
    .dashboard-box:hover {{ transform: translateY(-6px); box-shadow: 0 20px 30px rgba(0,0,0,0.04) !important; }}
    .box-lbl {{ font-size: 0.85rem !important; color: #868E96 !important; text-transform: uppercase; font-weight: 700; margin-bottom: 6px !important; }}
    .box-val {{ font-size: 1.55rem !important; font-weight: 800 !important; color: #212529 !important; }}
    
    .ultimate-progress-wrap {{ width: 100%; background-color: #F8F9FA; border-radius: 40px; padding: 6px; margin: 35px 0; border: 1px solid #E9ECEF; }}
    .ultimate-progress-core {{
        background: linear-gradient(90deg, {primary_color}, #1E1B4B) !important;
        height: 24px; border-radius: 30px; text-align: right; padding-right: 20px; line-height: 24px; color: white !important; font-weight: 700 !important;
    }}
    .eco-frame {{ border: 2px solid #E9ECEF; border-radius: 24px; padding: 20px; text-align: center; background: #FAFAFA; margin-top: 30px; }}
    .adv-banner-premium {{
        background: #F8FAFC !important; border: 2px dashed {primary_color} !important; border-radius: 20px !important;
        padding: 25px !important; text-align: center; margin: 40px 0 20px 0 !important;
    }}
    .premium-product {{ background: #FFFFFF !important; border-radius: 20px !important; padding: 25px !important; text-align: center; border: 1px solid #E9ECEF !important; }}
    .buy-btn {{ background-color: #FF9900 !important; color: white !important; border-radius: 10px !important; padding: 12px 24px !important; font-weight: 700 !important; display: inline-block !important; text-decoration: none !important; }}
    </style>
""", unsafe_allow_html=True)

# SCHERMATA DI LOGIN DI LUSSO (Se l'utente non è connesso)
if not st.session_state.autenticato:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; font-weight:900; color:#1E1B4B;'>🔐 Accesso Piattaforma Premium</h2>", unsafe_allow_html=True)
    st.write("<p style='text-align:center; color:#64748B;'>Inserisci le deine credenziali per accedere al diario cloud</p>", unsafe_allow_html=True)
    
    username_input = st.text_input("Username o Email")
    password_input = st.text_input("Password", type="password")
    
    if st.button("Accedi in Sicurezza", use_container_width=True):
        if username_input in UTENTI_DB and UTENTI_DB[username_input] == password_input:
            st.session_state.autenticato = True
            st.session_state.username = username_input
            st.success("Accesso effettuato!")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("Credenziali errate. Riprova o contatta l'assistenza.")
    st.markdown("<p style='text-align:center; font-size:0.85rem; color:#94A3B8; margin-top:15px;'>Credenziali demo -> user: dottoressa / pass: password123</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # SEZIONE UTENTE AUTENTICATO - CARICAMENTO DIARIO DI LUSSO
    dati_salvati = carica_dati_utente(st.session_state.username)
    
    # Data check preventivo sugli indici
    sesso_mappa = {"🌸 Fiocco Rosa (Femmina)": "F", "💎 Fiocco Azzurro (Maschio)": "M", "✨ Custodisci il Segreto": "N"}
    sesso_lista = list(sesso_mappa.keys())
    
    sesso_saved_index = 2
    if dati_salvati.get("sesso") in ["F", "M", "N"]:
        sesso_saved_index = list(sesso_mappa.values()).index(dati_salvati.get("sesso"))

    # Aggiornamento dinamico del colore in base al sesso dell'utente loggato
    if dati_salvati.get("sesso") == "F":
        primary_color = "#FF2A7A"
        accent_box = "#FFF0F5"
    elif dati_salvati.get("sesso") == "M":
        primary_color = "#0084FF"
        accent_box = "#ECF5FF"

    # Barra di navigazione utente superiore
    log_col1, log_col2 = st.columns(2)
    with log_col1:
        st.markdown(f"##### 👤 Account: **{st.session_state.username.capitalize()}** | Stato: Premium ✨")
    with log_col2:
        if st.button("🚪 Esci", use_container_width=True):
            st.session_state.autenticato = False
            st.session_state.username = ""
            st.rerun()

    # Apertura Card Madre Bianca
    st.markdown('<div class="ultimate-card">', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center; font-weight:900; color:#1E1B4B; font-size:2.8rem; margin-bottom:5px;">Suite Nascita Premium</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#6C757D; margin-bottom:40px;">Archivio crittografato e tracciamento gestazionale cloud</p>', unsafe_allow_html=True)

    # Input Dati Clinici
    col1, col2 = st.columns(2)
    
    with col1:
        nome = st.text_input("Identificativo Nascituro / Nome", value=dati_salvati.get("nome", ""), placeholder="Inserisci il nome scelto...")
        sesso_sel = st.radio("Configurazione Cromatica", sesso_lista, index=sesso_saved_index)
        sesso_codice = sesso_mappa[sesso_sel]

    with col2:
        duc_default = datetime.today()
        if dati_salvati.get("duc"):
            try: duc_default = datetime.strptime(dati_salvati.get("duc"), "%d/%m/%Y")
            except: pass
        ultimo_ciclo = st.date_input("Data Ultima Mestruazione (U.M.C.)", value=duc_default)
        dpp_modificata = st.checkbox("Correzione Clinica della DPP (Fornita dal Medico)", value=dati_salvati.get("dpp_modificata", False))
        dpp_default = ultimo_ciclo + timedelta(days=280)
        if dati_salvati.get("dpp") and dpp_modificata:
            try: dpp_default = datetime.strptime(dati_salvati.get("dpp"), "%d/%m/%Y")
            except: pass
        entry_dpp = st.date_input("Data Presunta Parto Ricalcolata", value=dpp_default, disabled=not dpp_modificata)
    st.markdown("<br>", unsafe_allow_html=True)
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1: esegui_calcolo = st.button("📊 Salva e Sincronizza Cloud", use_container_width=True)
    with btn_col2: resetta = st.button("🔄 Resetta Scheda", use_container_width=True)

    if ultimo_ciclo > datetime.today().date():
        st.error("Errore di validazione: Inserita una data futura non ammessa.")
        esegui_calcolo = False

    if resetta:
        salva_dati_utente(st.session_state.username, {})
        st.rerun()

    # Motore di calcolo ed elaborazione dati utente connesso
    if esegui_calcolo or dati_salvati:
        dati_da_salvare = {"nome": nome, "sesso": sesso_codice, "duc": ultimo_ciclo.strftime("%d/%m/%Y"), "dpp_modificata": dpp_modificata, "dpp": entry_dpp.strftime("%d/%m/%Y")}
        salva_dati_utente(st.session_state.username, dati_da_salvare)
        
        if dpp_modificata:
            giorni_totali = (entry_dpp - ultimo_ciclo).days
            dpp_finale = entry_dpp
        else:
            giorni_totali = 280
            dpp_finale = ultimo_ciclo + timedelta(days=280)
            
        giorni_trascorsi = (datetime.today().date() - ultimo_ciclo).days
        giorni_mancanti = giorni_totali - giorni_trascorsi
        settimane = giorni_trascorsi // 7
        giorni_extra = giorni_trascorsi % 7
        percentuale = max(0, min((giorni_trascorsi / giorni_totali) * 100, 100))
        segno_zodiacale = ottieni_zodiaco(dpp_finale)
        trimestre = "1° Trimestre 🍉" if settimane < 13 else "2° Trimestre ⌛" if settimane < 28 else "3° Trimestre 🍼"
        dimensione_bambino = ottieni_dimensione_frutto(settimane)

        st.markdown(f'<div class="ultimate-progress-wrap"><div class="ultimate-progress-core" style="width: {percentuale:.1f}%;">{percentuale:.2f}%</div></div>', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="dashboard-grid">
                <div class="dashboard-box"><div class="box-lbl">📅 Data Presunta Parto</div><div class="box-val" style="color:#6366F1 !important;">{dpp_finale.strftime("%d/%m/%Y")}</div></div>
                <div class="dashboard-box"><div class="box-lbl">⏱️ Sviluppo Attuale</div><div class="box-val">{settimane} sett + {giorni_extra} gg</div></div>
                <div class="dashboard-box"><div class="box-lbl">🌱 Giorni Completati</div><div class="box-val">{giorni_trascorsi} giorni</div></div>
                <div class="dashboard-box"><div class="box-lbl">⏳ Giorni al Parto</div><div class="box-val">{giorni_mancanti} giorni</div></div>
                <div class="dashboard-box"><div class="box-lbl">🔬 Fase Trimestrale</div><div class="box-val">{trimestre}</div></div>
                <div class="dashboard-box"><div class="box-lbl">✨ Costellazione Astrale</div><div class="box-val">{segno_zodiacale}</div></div>
            </div>
            <div class="dashboard-box" style="margin-top:20px; width:100%;"><div class="box-lbl">📏 Dimensions Stimate del Bambino</div><div class="box-val" style="color:#6366F1 !important;">Attualmente ha le dimensioni di {dimensione_bambino}</div></div>
        """, unsafe_allow_html=True)

        # Caricamento Ecografia Protetta
        st.markdown('<div class="eco-frame">', unsafe_allow_html=True)
        st.markdown("#### 👁️ Centro Ecografico Cloud")
        file_eco = st.file_uploader("Carica lo screening per salvarlo nella tua area privata", type=["jpg", "png", "jpeg"])
        if file_eco:
            st.image(Image.open(file_eco), caption=f"Ecografia salvata nel cloud di {nome}", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Registro medico contrazioni privato
        st.markdown("<br>#### ⏱️ Registro Clinico delle Contrazioni")
        with st.expander("Apri Cronometro Contrazioni"):
            if 'contrazioni' not in st.session_state: st.session_state.contrazioni = []
            if st.button("🚨 Registra Picco Contrazione Ora"):
                st.session_state.contrazioni.append(datetime.now().strftime("%H:%M:%S"))
            if st.session_state.contrazioni:
                for idx, c in enumerate(st.session_state.contrazioni):
                    st.write(f"Rilevazione #{idx+1}: **{c}**")

        if nome:
            img = Image.new("RGB", (1080, 1080), "#FFFFFF")
            draw = ImageDraw.Draw(img)
            draw.text((100, 100), f"Report Cloud {nome}", fill="#0F172A", font=ImageFont.load_default())
            img.save("condivisione.png")
            with open("condivisione.png", "rb") as file_img:
                with btn_col3: st.download_button(label="📸 Esporta Report PNG", data=file_img, file_name=f"Cloud_Report_{nome}.png", mime="image/png", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True) # Fine card principale bianca

    # ================= BANNER E MONETIZZAZIONE SOTTO L'AREA RISERVATA =================
    st.markdown("""
        <div class="adv-banner-premium">
            <p style="color: #6366F1 !important; font-size: 0.8rem !important; text-transform: uppercase; font-weight:800; letter-spacing:1.5px; margin-bottom:5px;">⭐ Baby Countdown Spazio Partner ⭐</p>
            <p style="color: #1E293B !important; font-size: 1.05rem !important; font-weight: 600; margin-bottom:5px;">Vuoi inserire la tua clinica o prodotto qui? Spazio pubblicitario ad alto rendimento.</p>
            <p style="color: #64748B !important; font-size: 0.85rem !important;">Contattaci subito a: commercial@babycountdown.it</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><h3 style='text-align:center; font-weight:900; color:#1E1B4B;'>🛍️ La Vetrina delle Mamme - Consigliati dagli Specialisti</h3>", unsafe_allow_html=True)
    prod_col1, prod_col2, prod_col3 = st.columns(3)
    with prod_col1: st.markdown('<div class="premium-product"><span style="font-size:3.5rem;">🤰</span><h4>Cuscino Medico XXL</h4><p style="font-size:0.85rem; color:#6C757D;">Supporto posturale raccomandato.</p><a class="buy-btn" href="https://amazon.it" target="_blank">Acquista 🛒</a></div>', unsafe_allow_html=True)
    with prod_col2: st.markdown('<div class="premium-product"><span style="font-size:3.5rem;">🧴</span><h4>Olio Elastina Bio</h4><p style="font-size:0.85rem; color:#6C757D;">Trattamento smagliature dermatologico.</p><a class="buy-btn" href="https://amazon.it" target="_blank">Acquista 🛒</a></div>', unsafe_allow_html=True)
    with prod_col3: st.markdown('<div class="premium-product"><span style="font-size:3.5rem;">📔</span><h4>Diario d\'Elite dei 9 Mesi</h4><p style="font-size:0.85rem; color:#6C757D;">Album speciale per esami e ricordi.</p><a class="buy-btn" href="https://amazon.it" target="_blank">Acquista 🛒</a></div>', unsafe_allow_html=True)
