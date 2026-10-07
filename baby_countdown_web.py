import streamlit as st
from datetime import datetime, timedelta
import json
import os
import time
from PIL import Image, ImageDraw, ImageFont

# 1. Configurazione Iniziale e SEO della Piattaforma Ultimate
st.set_page_config(
    page_title="Nascita Premium Suite - Gestione Gestazionale di Lusso",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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

FILE_DATI = "gravidanza_web.json"

def carica_sessione():
    if os.path.exists(FILE_DATI):
        try:
            with open(FILE_DATI, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}

def salva_sessione(dati):
    with open(FILE_DATI, "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False, indent=4)

dati_salvati = carica_sessione()

# Color Palette High-End con sfumature al neon e contrasti definiti
sesso_scelto = dati_salvati.get("sesso", "N")
if sesso_scelto == "F":
    gradient = "linear-gradient(135deg, #FFFBFC 0%, #FFE4EC 100%)"
    primary_color = "#FF2A7A"
    text_gradient = "linear-gradient(90deg, #FF2A7A, #4A001F)"
    accent_box = "#FFF0F5"
elif sesso_scelto == "M":
    gradient = "linear-gradient(135deg, #F5FAFF 0%, #D4E9FF 100%)"
    primary_color = "#0084FF"
    text_gradient = "linear-gradient(90deg, #0084FF, #002D59)"
    accent_box = "#ECF5FF"
else:
    gradient = "linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%)"
    primary_color = "#6366F1"
    text_gradient = "linear-gradient(90deg, #6366F1, #1E1B4B)"
    accent_box = "#F1F3F5"

# Iniezione di CSS Custom da Agenzia Digitale d'Elite (Valore percepito altissimo)
st.markdown(f"""
    <style>
    .stApp {{ background: {gradient} !important; }}
    
    h1, h2, h3, h4, h5, h6, p, label, span {{
        font-family: '-apple-system', BlinkMacSystemFont, 'Inter', sans-serif !important;
    }}
    
    .ultimate-card {{
        background: #FFFFFF !important;
        border-radius: 40px !important;
        padding: 50px !important;
        box-shadow: 0 40px 80px -15px rgba(0,0,0,0.06), 0 0 1px rgba(0,0,0,0.04) !important;
        border: 1px solid rgba(255,255,255,0.7) !important;
        margin-top: 20px !important;
    }}
    .ultimate-title {{
        background: {text_gradient};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center !important;
        font-size: 3.2rem !important;
        font-weight: 900 !important;
        letter-spacing: -1.5px;
        margin-bottom: 5px !important;
    }}
    .ultimate-subtitle {{
        text-align: center !important;
        color: #6C757D !important;
        font-size: 1.15rem !important;
        margin-bottom: 45px !important;
        font-weight: 400;
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
        border: 1px solid rgba(0,0,0,0.01) !important;
        transition: all 0.35s cubic-bezier(0.2, 0.8, 0.2, 1);
    }}
    .dashboard-box:hover {{
        transform: translateY(-8px);
        box-shadow: 0 24px 36px rgba(0,0,0,0.04) !important;
    }}
    .box-lbl {{
        font-size: 0.85rem !important;
        color: #868E96 !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 700;
        margin-bottom: 6px !important;
    }}
    .box-val {{
        font-size: 1.55rem !important;
        font-weight: 800 !important;
        color: #212529 !important;
    }}
    
    .ultimate-progress-wrap {{
        width: 100%;
        background-color: #F8F9FA;
        border-radius: 40px;
        padding: 6px;
        margin: 35px 0;
        box-shadow: inset 0 2px 6px rgba(0,0,0,0.02);
        border: 1px solid #E9ECEF;
    }}
    .ultimate-progress-core {{
        background: linear-gradient(90deg, {primary_color}, #1E1B4B) !important;
        height: 28px;
        border-radius: 30px;
        text-align: right;
        padding-right: 20px;
        line-height: 28px;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.9rem;
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    }}
    
    .eco-frame {{
        border: 2px solid #E9ECEF;
        border-radius: 24px;
        padding: 20px;
        text-align: center;
        background: #FAFAFA;
        margin-top: 30px;
    }}
    
    .premium-product {{
        background: #FFFFFF !important;
        border-radius: 20px !important;
        padding: 25px !important;
        text-align: center !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.03) !important;
        border: 1px solid #E9ECEF !important;
        transition: all 0.3s ease;
    }}
    .premium-product:hover {{
        box-shadow: 0 20px 40px rgba(0,0,0,0.07) !important;
    }}
    .buy-btn {{
        background-color: #FF9900 !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        text-decoration: none !important;
        display: inline-block !important;
        font-weight: 700 !important;
        margin-top: 15px !important;
        box-shadow: 0 4px 10px rgba(255, 153, 0, 0.2);
    }}
    </style>
""", unsafe_allow_html=True)

# Apertura Card Madre
st.markdown('<div class="ultimate-card">', unsafe_allow_html=True)

st.markdown('<h1 class="ultimate-title">Suite Nascita Premium</h1>', unsafe_allow_html=True)
st.markdown('<p class="ultimate-subtitle">Sistemi digitali integrati per cliniche private e futuri genitori</p>', unsafe_allow_html=True)

# Input Dati Avanzato
col1, col2 = st.columns(2)
with col1:
    nome = st.text_input("Identificativo Nascituro / Nome", value=dati_salvati.get("nome", ""), placeholder="Inserisci il nome scelto...")
    sesso_mappa = {"🌸 Fiocco Rosa (Femmina)": "F", "💎 Fiocco Azzurro (Maschio)": "M", "✨ Custodisci il Segreto": "N"}
    sesso_lista = list(sesso_mappa.keys())
    sesso_saved_index = list(sesso_mappa.values()).index(dati_salvati.get("sesso", "N"))
    sesso_sel = st.radio("Configurazione Cromatica", sesso_lista, index=sesso_saved_index)
    sesso_codice = sesso_mappa[sesso_sel]

with col2:
    duc_default = datetime.today()
    if dati_salvati.get("duc"):
        try: duc_default = datetime.strptime(dati_salvati.get("duc"), "%d/%m/%Y")
        except: pass
    ultimo_ciclo = st.date_input("Data Ultima Mestruazione (U.M.C.)", value=duc_default)
    dpp_modificata = st.checkbox("Correzione Clinica della DPP (Data fornita dal Medico)", value=dati_salvati.get("dpp_modificata", False))
    dpp_default = ultimo_ciclo + timedelta(days=280)
    if dati_salvati.get("dpp") and dpp_modificata:
        try: dpp_default = datetime.strptime(dati_salvati.get("dpp"), "%d/%m/%Y")
        except: pass
    entry_dpp = st.date_input("Data Presunta Parto Ricalcolata", value=dpp_default, disabled=not dpp_modificata)

st.markdown("<br>", unsafe_allow_html=True)
btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col1: esegui_calcolo = st.button("📊 Genera Report Clinico", use_container_width=True)
with btn_col2: resetta = st.button("🔄 Resetta Database", use_container_width=True)

if ultimo_ciclo > datetime.today().date():
    st.error("Errore di validazione: Inserita una data futura non ammessa dal sistema.")
    esegui_calcolo = False

if resetta:
    if os.path.exists(FILE_DATI): os.remove(FILE_DATI)
    st.rerun()

# Motore di Calcolo della Piattaforma Ultimate
if esegui_calcolo or dati_salvati:
    dati_da_salvare = {"nome": nome, "sesso": sesso_codice, "duc": ultimo_ciclo.strftime("%d/%m/%Y"), "dpp_modificata": dpp_modificata, "dpp": entry_dpp.strftime("%d/%m/%Y")}
    salva_sessione(dati_da_salvare)
    
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
    trimestre = "1° Trimestre Gestazionale 🍉" if settimane < 13 else "2° Trimestre Gestazionale ⌛" if settimane < 28 else "3° Trimestre Gestazionale 🍼"
    dimensione_bambino = ottieni_dimensione_frutto(settimane)

    # Barra di avanzamento Premium ad alta risoluzione
    st.markdown(f'<div class="ultimate-progress-wrap"><div class="ultimate-progress-core" style="width: {percentuale:.1f}%;">{percentuale:.2f}%</div></div>', unsafe_allow_html=True)
    
    # Rendering della Dashboard dei Risultati Ultimate
    st.markdown(f"""
        <div class="dashboard-grid">
            <div class="dashboard-box"><div class="box-lbl">📅 Data Presunta Parto</div><div class="box-val" style="color:{primary_color} !important;">{dpp_finale.strftime("%d/%m/%Y")}</div></div>
            <div class="dashboard-box"><div class="box-lbl">⏱️ Sviluppo Attuale</div><div class="box-val">{settimane} sett + {giorni_extra} gg</div></div>
            <div class="dashboard-box"><div class="box-lbl">🌱 Giorni Completati</div><div class="box-val">{giorni_trascorsi} giorni</div></div>
            <div class="dashboard-box"><div class="box-lbl">⏳ Giorni al Parto</div><div class="box-val">{giorni_mancanti} giorni</div></div>
            <div class="dashboard-box"><div class="box-lbl">🔬 Fase Trimestrale</div><div class="box-val" style="font-size:1.15rem; padding-top:4px;">{trimestre}</div></div>
            <div class="dashboard-box"><div class="box-lbl">✨ Costellazione Astrale</div><div class="box-val">{segno_zodiacale}</div></div>
        </div>
        <div class="dashboard-box" style="margin-top:20px; width:100%;"><div class="box-lbl">📏 Dimensioni Stimate del Bambino</div><div class="box-val" style="color:{primary_color} !important;">Attualmente ha le dimensioni di {dimensione_bambino}</div></div>
    """, unsafe_allow_html=True)
    # FUNZIONALITÀ ULTIMATE: Caricamento Ecografia Real-Time
    st.markdown('<div class="eco-frame">', unsafe_allow_html=True)
    st.markdown("#### 👁️ Centro Ecografico Digitale")
    file_eco = st.file_uploader("Carica lo screening o l'ecografia del mese per integrarla nel diario grafico", type=["jpg", "png", "jpeg"])
    if file_eco:
        immagine_caricata = Image.open(file_eco)
        st.image(immagine_caricata, caption=f"Ecografia di {nome if nome else 'Bimbo/a'} - Sviluppo a {settimane} settimane", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # FUNZIONALITÀ ULTIMATE: Monitor Medico delle Contrazioni
    st.markdown("<br>#### ⏱️ Strumento Clinico: Registro Contrazioni")
    with st.expander("Apri Cronometro Contrazioni Privato"):
        st.write("Usa questo strumento per monitorare la frequenza delle contrazioni da riferire alla dottoressa.")
        if 'contrazioni' not in st.session_state: st.session_state.contrazioni = []
        if st.button("🚨 Registra Picco Contrazione Ora"):
            st.session_state.contrazioni.append(datetime.now().strftime("%H:%M:%S"))
        if st.session_state.contractions:
            for idx, c in enumerate(st.session_state.contrazioni):
                st.write(f"Contrazione #{idx+1}: Rilevata alle ore **{c}**")

    if nome:
        img = Image.new("RGB", (1080, 1080), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        draw.text((100, 100), f"Suite Premium {nome}", fill="#0F172A", font=ImageFont.load_default())
        img.save("condivisione.png")
        with open("condivisione.png", "rb") as file_img:
            with btn_col3: st.download_button(label="📸 Esporta Report PNG", data=file_img, file_name=f"Report_{nome}.png", mime="image/png", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True) # Fine card principale

# ================= RIGIDA MONETIZZAZIONE AD RENDIMENTO HIGH-END =================
st.markdown("<br><h3 style='text-align:center; font-weight:900; color:#1E1B4B;'>🛍️ La Vetrina delle Mamme - Consigliati dagli Specialisti</h3>", unsafe_allow_html=True)
prod_col1, prod_col2, prod_col3 = st.columns(3)

with prod_col1:
    st.markdown('<div class="premium-product"><span style="font-size:3.5rem;">🤰</span><h4>Cuscino Medico XXL</h4><p style="font-size:0.85rem; color:#6C757D; min-height:50px;">Supporto posturale raccomandato per alleviare il peso sulla colonna.</p><a class="buy-btn" href="https://amazon.it" target="_blank">Ordina su Amazon</a></div>', unsafe_allow_html=True)
with prod_col2:
    st.markdown('<div class="premium-product"><span style="font-size:3.5rem;">🧴</span><h4>Olio Elastina Bio</h4><p style="font-size:0.85rem; color:#6C757D; min-height:50px;">Trattamento clinico preventivo dermatologicamente testato.</p><a class="buy-btn" href="https://amazon.it" target="_blank">Ordina su Amazon</a></div>', unsafe_allow_html=True)
with prod_col3:
    st.markdown('<div class="premium-product"><span style="font-size:3.5rem;">📔</span><h4>Diario d\'Elite dei 9 Mesi</h4><p style="font-size:0.85rem; color:#6C757D; min-height:50px;">Custodia di lusso in pelle per conservare ricordi ed ecografie.</p><a class="buy-btn" href="https://amazon.it" target="_blank">Ordina su Amazon</a></div>', unsafe_allow_html=True)
