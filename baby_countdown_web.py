import streamlit as st
from datetime import datetime, timedelta
import json
import os
from PIL import Image, ImageDraw, ImageFont

# 1. Configurazione iniziale della pagina
st.set_page_config(
    page_title="Aspettando Te - Premium Tracker",
    page_icon="👶",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Calcolo automatico del segno zodiacale
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

# Database locale JSON per i dati della sessione
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

# Gestione dinamica dei colori ad altissimo contrasto basata sul sesso scelto
sesso_scelto = dati_salvati.get("sesso", "N")
if sesso_scelto == "F":
    gradient = "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)"
    primary_color = "#d63384"
    text_color = "#4a0e2e"
    accent_box = "#fff0f7"
elif sesso_scelto == "M":
    gradient = "linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)"
    primary_color = "#1976d2"
    text_color = "#0a2540"
    accent_box = "#f0f8ff"
else:
    gradient = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
    primary_color = "#5d6d7e"
    text_color = "#2c3e50"
    accent_box = "#f8f9f9"

# Iniezione CSS Forzata per bloccare i testi bianchi invisibili e rendere tutto bellissimo
st.markdown(f"""
    <style>
    /* Sfondo generale della pagina */
    .stApp {{ 
        background: {gradient} !important; 
    }}
    
    /* Disattivazione stili nativi distruttivi di Streamlit */
    h1, h2, h3, h4, h5, h6, p, span, label {{
        color: #2c3e50 !important;
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
    }}
    
    /* La Card Bianca principale */
    .main-card {{
        background: #ffffff !important;
        border-radius: 20px !important;
        padding: 40px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
        margin-top: 20px !important;
        margin-bottom: 30px !important;
    }}
    /* Il Titolo Principale della App */
    .main-title {{
        color: {primary_color} !important;
        text-align: center !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 25px !important;
        letter-spacing: -0.5px;
    }}
    
    /* Griglia dei Risultati del Calcolo */
    .grid-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin-top: 25px;
    }}
    
    /* Singoli Box dei Risultati */
    .grid-box {{
        background: {accent_box} !important;
        border-radius: 12px !important;
        padding: 20px !important;
        text-align: center !important;
        border: 1px solid rgba(0,0,0,0.04) !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
    }}
    .box-title {{
        font-size: 0.85rem !important;
        color: #7f8c8d !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px !important;
        font-weight: bold;
    }}
    .box-value {{
        font-size: 1.35rem !important;
        font-weight: bold !important;
        color: {text_color} !important;
    }}
    
    /* Personalizzazione della Barra di Progresso Real-Time */
    .custom-progress-container {{
        width: 100%;
        background-color: #eaeded;
        border-radius: 20px;
        padding: 4px;
        margin: 25px 0;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.06);
    }}
    .custom-progress-bar {{
        background-color: {primary_color} !important;
        height: 24px;
        border-radius: 15px;
        text-align: center;
        line-height: 24px;
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 0.9rem;
    }}
    
    /* Card per i Prodotti Amazon Consigliati */
    .product-card {{
        background: #ffffff !important;
        border-radius: 14px !important;
        padding: 20px !important;
        text-align: center !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04) !important;
        border: 1px solid #eef2f3 !important;
        height: 100%;
    }}
    .product-card h4 {{
        color: #34495e !important;
        font-weight: bold !important;
        margin-top: 10px !important;
    }}
    .product-btn {{
        background-color: #ff9900 !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        text-decoration: none !important;
        display: inline-block !important;
        font-weight: bold !important;
        margin-top: 15px !important;
        font-size: 0.9rem !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }}
    </style>
""", unsafe_allow_html=True)

# Apertura blocco grafico Card Principale Bianca
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.markdown(f'<h1 class="main-title">👶 Aspettando Te Premium</h1>', unsafe_allow_html=True)

# Colonne per l'inserimento dei dati
col1, col2 = st.columns(2)
with col1:
    nome = st.text_input("Nome del bambino/a", value=dati_salvati.get("nome", ""), placeholder="Scrivi qui il nome...")
    sesso_mappa = {"👧 Femmina": "F", "👦 Maschio": "M", "🤍 Non definito": "N"}
    sesso_lista = list(sesso_mappa.keys())
    sesso_saved_index = list(sesso_mappa.values()).index(dati_salvati.get("sesso", "N"))
    sesso_sel = st.radio("Sesso", sesso_lista, index=sesso_saved_index)
    sesso_codice = sesso_mappa[sesso_sel]

with col2:
    duc_default = datetime.today()
    if dati_salvati.get("duc"):
        try: duc_default = datetime.strptime(dati_salvati.get("duc"), "%d/%m/%Y")
        except: pass
    ultimo_ciclo = st.date_input("Data ultimo ciclo (U.M.C.)", value=duc_default)
    dpp_modificata = st.checkbox("DPP modificata dal ginecologo", value=dati_salvati.get("dpp_modificata", False))
    dpp_default = ultimo_ciclo + timedelta(days=280)
    if dati_salvati.get("dpp") and dpp_modificata:
        try: dpp_default = datetime.strptime(dati_salvati.get("dpp"), "%d/%m/%Y")
        except: pass
    entry_dpp = st.date_input("DPP personalizzata", value=dpp_default, disabled=not dpp_modificata)

# Organizzazione orizzontale dei Pulsanti
btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col1: esegui_calcolo = st.button("✨ Calcola Stato", use_container_width=True)
with btn_col2: resetta = st.button("🔄 Reset Dati", use_container_width=True)

if ultimo_ciclo > datetime.today().date():
    st.error("Errore: La data dell'ultimo ciclo non può essere futura rispetto a oggi!")
    esegui_calcolo = False

if resetta:
    if os.path.exists(FILE_DATI): os.remove(FILE_DATI)
    st.rerun()

# Motore di Hospital ed elaborazione gravidanza
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

    # Rendering della barra di avanzamento e dei box informativi fissati ad alto contrasto
    st.markdown(f'<div class="custom-progress-container"><div class="custom-progress-bar" style="width: {percentuale:.1f}%;">{percentuale:.2f}%</div></div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="grid-container">
            <div class="grid-box"><div class="box-title">🌸 Data Presunta Parto</div><div class="box-value">{dpp_finale.strftime("%d/%m/%Y")}</div></div>
            <div class="grid-box"><div class="box-title">💗 Epoca Gestazionale</div><div class="box-value">{settimane} + {giorni_extra} gg</div></div>
            <div class="grid-box"><div class="box-title">🌼 Giorni Trascorsi</div><div class="box-value">{giorni_trascorsi} gg</div></div>
            <div class="grid-box"><div class="box-title">🚀 Giorni Mancanti</div><div class="box-value">{giorni_mancanti} gg</div></div>
            <div class="grid-box"><div class="box-title">✨ Trimestre Attuale</div><div class="box-value">{trimestre}</div></div>
            <div class="grid-box"><div class="box-title">⭐ Segno Zodiacale</div><div class="box-value">{segno_zodiacale}</div></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Generazione in background dell'immagine di condivisione PNG
    if nome:
        img = Image.new("RGB", (1080, 1080), "#fff0f7" if sesso_codice=="F" else "#f0f8ff" if sesso_codice=="M" else "#fffef0")
        draw = ImageDraw.Draw(img)
        draw.text((120, 120), f"Aspettando {nome}", fill="#d63384" if sesso_codice=="F" else "#1976d2", font=ImageFont.load_default())
        draw.text((120, 280), f"Data Parto: {dpp_finale.strftime('%d/%m/%Y')}\nSettimana: {settimane}+{giorni_extra}gg", fill="black", font=ImageFont.load_default())
        img.save("condivisione.png")
        with open("condivisione.png", "rb") as file_img:
            with btn_col3: st.download_button(label="📸 Scarica Immagine", data=file_img, file_name=f"{nome}_countdown.png", mime="image/png", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True) # Fine card principale bianca

# ================= VETRINA PRODOTTI AMAZON AFFILIAZIONI =================
st.markdown("<br><h3 style='text-align:center; color:#2c3e50; font-weight: bold;'>🛍️ Prodotti Consigliati per la Mamma</h3>", unsafe_allow_html=True)
prod_col1, prod_col2, prod_col3 = st.columns(3)

with prod_col1:
    st.markdown('<div class="product-card"><span style="font-size:3rem;">🤰</span><h4>Cuscino Gravidanza</h4><p style="font-size:0.85rem; color:#666;">Supporto ergonomico XXL per il riposo e la schiena.</p><a class="product-btn" href="https://amazon.it" target="_blank">Vedi su Amazon 🛒</a></div>', unsafe_allow_html=True)
with prod_col2:
    st.markdown('<div class="product-card"><span style="font-size:3rem;">🧴</span><h4>Olio Smagliature Bio</h4><p style="font-size:0.85rem; color:#666;">Idratante naturale elasticizzante ad assorbimento rapido.</p><a class="product-btn" href="https://amazon.it" target="_blank">Vedi su Amazon 🛒</a></div>', unsafe_allow_html=True)
with prod_col3:
    st.markdown('<div class="product-card"><span style="font-size:3rem;">📔</span><h4>Diario dei Ricordi</h4><p style="font-size:0.85rem; color:#666;">Bellissimo album speciale per raccogliere le emozioni dei 9 mesi.</p><a class="product-btn" href="https://amazon.it" target="_blank">Vedi su Amazon 🛒</a></div>', unsafe_allow_html=True)
