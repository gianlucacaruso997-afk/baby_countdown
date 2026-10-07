import streamlit as st
from datetime import datetime, timedelta
import json
import os
from PIL import Image, ImageDraw, ImageFont

# 1. Configurazione della pagina ed estetica della scheda del browser
st.set_page_config(
    page_title="Nascita Premium - Il Tuo Diario di Gravidanza Intelligente",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Funzione per calcolare il segno zodiacale basandosi sulla Data Parto
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

# Database locale JSON per rendere persistente la sessione utente
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

# Scelta del gradiente Premium Dinamico (Morbido, Elegante, Contrasto Altissimo)
sesso_scelto = dati_salvati.get("sesso", "N")
if sesso_scelto == "F":
    gradient = "linear-gradient(135deg, #FFF0F5 0%, #FFD1DC 100%)"
    primary_color = "#E91E63"
    accent_box = "#FFF5F8"
    shadow_color = "rgba(233, 30, 99, 0.15)"
elif sesso_scelto == "M":
    gradient = "linear-gradient(135deg, #F0F8FF 0%, #B0C4DE 100%)"
    primary_color = "#1E88E5"
    accent_box = "#F4F9FF"
    shadow_color = "rgba(30, 136, 229, 0.15)"
else:
    gradient = "linear-gradient(135deg, #F9F9FB 0%, #E2E4E9 100%)"
    primary_color = "#4F46E5"
    accent_box = "#F3F4F6"
    shadow_color = "rgba(79, 70, 229, 0.1)"

# Iniezione del Foglio di Stile CSS da Agenzia Digitale (Look da 10k)
st.markdown(f"""
    <style>
    .stApp {{ background: {gradient} !important; }}
    
    /* Reset Forzato Font e Colori per abbattere lo stile grezzo di Streamlit */
    h1, h2, h3, h4, h5, h6, p, span, label, div {{
        font-family: '-apple-system', BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        color: #1E293B !important;
    }}
    
    /* Card Madre con Micro-Ombreggiatura Neutra ed Effetto di Elevazione Spaziale */
    .agency-card {{
        background: #FFFFFF !important;
        border-radius: 32px !important;
        padding: 45px !important;
        box-shadow: 0 25px 50px -12px {shadow_color}, 0 0 1px rgba(0,0,0,0.1) !important;
        border: 1px solid rgba(255,255,255,0.8) !important;
        margin-top: 30px !important;
        margin-bottom: 40px !important;
    }}
    /* Titolo dell'applicazione con Gradiente e spaziatura Kerning */
    .agency-title {{
        background: linear-gradient(90deg, {primary_color}, #0F172A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center !important;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        margin-bottom: 10px !important;
        letter-spacing: -1px;
    }}
    .agency-subtitle {{
        text-align: center !important;
        color: #64748B !important;
        font-size: 1.1rem !important;
        margin-bottom: 40px !important;
    }}
    
    /* Griglia Dashboard di Alto Livello */
    .metric-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 20px;
        margin-top: 30px;
    }}
    .metric-box {{
        background: {accent_box} !important;
        border-radius: 20px !important;
        padding: 24px !important;
        text-align: center !important;
        border: 1px solid rgba(0,0,0,0.02) !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.01) !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .metric-box:hover {{
        transform: translateY(-6px);
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.05) !important;
    }}
    .metric-label {{
        font-size: 0.85rem !important;
        color: #64748B !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        margin-bottom: 8px !important;
    }}
    .metric-value {{
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        color: #0F172A !important;
    }}
    
    /* Barra di Avanzamento Minimal e Moderna con Micro-Bagliore */
    .progress-wrapper {{
        width: 100%;
        background-color: #F1F5F9;
        border-radius: 30px;
        padding: 5px;
        margin: 35px 0 15px 0;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.03);
    }}
    .progress-core {{
        background: linear-gradient(90deg, {primary_color}, #0F172A) !important;
        height: 24px;
        border-radius: 20px;
        text-align: right;
        padding-right: 15px;
        line-height: 24px;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.85rem;
        box-shadow: 0 4px 12px {shadow_color};
        transition: width 1s ease-in-out;
    }}
    
    /* Stile Banner Pubblicitari Spazi ADV */
    .adv-banner {{
        background: #F8FAFC !important;
        border: 2px dashed #CBD5E1 !important;
        border-radius: 16px !important;
        padding: 25px !important;
        text-align: center !important;
        margin: 30px 0 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Inizio Container ad Elevazione Agenzia
st.markdown('<div class="agency-card">', unsafe_allow_html=True)

st.markdown('<h1 class="agency-title">Nascita Premium</h1>', unsafe_allow_html=True)
st.markdown('<p class="agency-subtitle">La piattaforma medica intelligente per il tracciamento gestazionale</p>', unsafe_allow_html=True)

# Layout Input Dati Professionale
col1, col2 = st.columns(2)

with col1:
    nome = st.text_input("Nome del nascituro", value=dati_salvati.get("nome", ""), placeholder="Es. Leonardo o Sofia...")
    sesso_mappa = {"👧 Fiocco Rosa": "F", "👦 Fiocco Azzurro": "M", "🤍 Custodisci il Segreto": "N"}
    sesso_lista = list(sesso_mappa.keys())
    sesso_saved_index = list(sesso_mappa.values()).index(dati_salvati.get("sesso", "N"))
    sesso_sel = st.radio("Seleziona Configurazione", sesso_lista, index=sesso_saved_index)
    sesso_codice = sesso_mappa[sesso_sel]
with col2:
    duc_default = datetime.today()
    if dati_salvati.get("duc"):
        try: duc_default = datetime.strptime(dati_salvati.get("duc"), "%d/%m/%Y")
        except: pass
    ultimo_ciclo = st.date_input("Data dell'ultimo ciclo (U.M.C.)", value=duc_default)
    dpp_modificata = st.checkbox("Ricalcolo Clinico (DPP fornito dal Ginecologo)", value=dati_salvati.get("dpp_modificata", False))
    dpp_default = ultimo_ciclo + timedelta(days=280)
    if dati_salvati.get("dpp") and dpp_modificata:
        try: dpp_default = datetime.strptime(dati_salvati.get("dpp"), "%d/%m/%Y")
        except: pass
    entry_dpp = st.date_input("Data Presunta Parto Modificata", value=dpp_default, disabled=not dpp_modificata)

# Sezione Pulsantiera Flat minimalista
st.markdown("<br>", unsafe_allow_html=True)
btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col1: esegui_calcolo = st.button("📊 Elabora Dati Clinici", use_container_width=True)
with btn_col2: resetta = st.button("🔄 Resetta Sistema", use_container_width=True)

if ultimo_ciclo > datetime.today().date():
    st.error("Errore di validazione: La data inserita non può essere futura.")
    esegui_calcolo = False

if resetta:
    if os.path.exists(FILE_DATI): os.remove(FILE_DATI)
    st.rerun()

# Motore di Calcolo e Generazione Metriche della Dashboard
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
    trimestre = "1° Trimestre 🍉" if settimane < 13 else "2° Trimestre ⌛" if settimane < 28 else "3° Trimestre 🍼"

    # Barra di avanzamento Custom con Bagliore Lineare
    st.markdown(f'<div class="progress-wrapper"><div class="progress-core" style="width: {percentuale:.1f}%;">{percentuale:.2f}%</div></div>', unsafe_allow_html=True)
    
    # Rendering Dashboard Metriche Premium
    st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-box"><div class="metric-label">📅 Data Presunta Parto</div><div class="metric-value" style="color:{primary_color} !important;">{dpp_finale.strftime("%d/%m/%Y")}</div></div>
            <div class="metric-box"><div class="metric-label">⏱️ Epoca Gestazionale</div><div class="metric-value">{settimane} sett + {giorni_extra} gg</div></div>
            <div class="metric-box"><div class="metric-label">📈 Giorni Trascorsi</div><div class="metric-value">{giorni_trascorsi} giorni</div></div>
            <div class="metric-box"><div class="metric-label">⏳ Giorni Mancanti</div><div class="metric-value">{giorni_mancanti} giorni</div></div>
            <div class="metric-box"><div class="metric-label">🧬 Trimestre Attuale</div><div class="metric-value">{trimestre}</div></div>
            <div class="metric-box"><div class="metric-label">✨ Segno Nascituro</div><div class="metric-value">{segno_zodiacale}</div></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Generazione Immagine Condivisione (Memoria Virtuale Cloud)
    if nome:
        img = Image.new("RGB", (1080, 1080), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        draw.text((100, 100), f"Aspettando {nome}", fill="#0F172A", font=ImageFont.load_default())
        img.save("condivisione.png")
        with open("condivisione.png", "rb") as file_img:
            with btn_col3: st.download_button(label="📸 Esporta Report PNG", data=file_img, file_name=f"Report_{nome}.png", mime="image/png", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True) # Fine card principale
# ================= AREA STRATEGICA ADV / GOOGLE ADSENSE =================
st.markdown("""
    <div class="adv-banner">
        <p style="color: #94A3B8 !important; font-size: 0.75rem !important; text-transform: uppercase; font-weight:700; letter-spacing:1px; margin-bottom:5px;">Spazio Sponsorizzato / Google AdSense</p>
        <p style="color: #475569 !important; font-size: 0.95rem !important; font-weight: 500;">Vuoi promuovere la tua attività qui? Contattaci a: sponsor@nascitapremium.it</p>
    </div>
""", unsafe_allow_html=True)

# ================= SEZIONE INFORMATIVA DI VALORE PREMIUM =================
st.markdown("### 📚 Approfondimenti Clinici Gestazionali")
faq1, faq2 = st.columns(2)

with faq1:
    with st.expander("🔬 Cosa succede nel trimestre corrente?"):
        st.write("Ogni trimestre comporta cambiamenti biologici precisi. Monitorare costantemente l'epoca gestazionale aiuta il ginecologo a programmare ecografie morfologiche e screening mirati.")
with faq2:
    with st.expander("🍏 Consigli nutrizionali per la mamma"):
        st.write("Un'alimentazione ricca di acido folico, ferro e DHA supporta attivamente lo sviluppo cerebrale e cardiaco del feto fin dalle prime settimane gestazionali.")

# ================= AREA AFFILIAZIONE COMMERCIALE AUTOMATICA =================
st.markdown("<br><h3 style='text-align:center; font-weight: 800; color:#0F172A;'>🛒 Gli Essenziali Consigliati dai Professionisti</h3>", unsafe_allow_html=True)
prod_col1, prod_col2, prod_col3 = st.columns(3)

with prod_col1:
    st.markdown('<div class="product-card"><span style="font-size:3rem;">🤰</span><h4 style="margin:10px 0;">Cuscino Supporto XXL</h4><p style="font-size:0.85rem; color:#64748B;">Ergonomico, ideale per agevolare il sonno della mamma.</p><a class="product-btn" href="https://amazon.it" target="_blank">Acquista su Amazon</a></div>', unsafe_allow_html=True)
with prod_col2:
    st.markdown('<div class="product-card"><span style="font-size:3rem;">🧴</span><h4 style="margin:10px 0;">Olio Elasticizzante Bio</h4><p style="font-size:0.85rem; color:#64748B;">Previene attivamente lo sviluppo delle smagliature della pancia.</p><a class="product-btn" href="https://amazon.it" target="_blank">Acquista su Amazon</a></div>', unsafe_allow_html=True)
with prod_col3:
    st.markdown('<div class="product-card"><span style="font-size:3rem;">📔</span><h4 style="margin:10px 0;">Diario Clinico dei 9 Mesi</h4><p style="font-size:0.85rem; color:#64748B;">Un album raffinato per conservare esami, note ed emozioni.</p><a class="product-btn" href="https://amazon.it" target="_blank">Acquista su Amazon</a></div>', unsafe_allow_html=True)
