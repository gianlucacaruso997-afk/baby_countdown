import streamlit as st
from datetime import datetime, timedelta
import json
import os
from PIL import Image, ImageDraw, ImageFont

# 1. Configurazione della pagina Streamlit
st.set_page_config(
    page_title="Aspettando Te - Premium Pregnancy Tracker",
    page_icon="👶",
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

# Gestione del database locale JSON per memorizzare i dati
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

# Scelta dinamica dello sfondo basata sul sesso del nascituro
sesso_scelto = dati_salvati.get("sesso", "N")
if sesso_scelto == "F":
    gradient = "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)"
    card_bg = "rgba(255, 240, 247, 0.90)"
    primary_color = "#d63384"
    text_color = "#880e4f"
elif sesso_scelto == "M":
    gradient = "linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)"
    card_bg = "rgba(240, 248, 255, 0.90)"
    primary_color = "#1976d2"
    text_color = "#0d47a1"
else:
    gradient = "linear-gradient(135deg, #fff8dc 0%, #fffef0 100%)"
    card_bg = "rgba(255, 254, 240, 0.90)"
    primary_color = "#b7950b"
    text_color = "#7d6608"

# Grafica HTML5/CSS3 Premium per trasformare l'app in un vero sito web
st.markdown(f"""
    <style>
    .stApp {{ background: {gradient}; }}
    .main-card {{
        background: {card_bg}; border-radius: 24px; padding: 35px;
        box-shadow: 0 12px 32px rgba(0,0,0,0.08); backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.4); margin-bottom: 25px; color: #333333;
    }}
    .main-title {{
        color: {primary_color}; text-align: center; font-family: 'Comic Sans MS', cursive, sans-serif;
        font-size: 2.8rem !important; font-weight: bold; margin-bottom: 30px;
    }}
    .grid-container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; margin-top: 20px; }}
    .grid-box {{
        background: rgba(255,255,255,0.75); border-radius: 16px; padding: 18px; text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02); border: 1px solid rgba(255,255,255,0.6); transition: transform 0.3s ease;
    }}
    .grid-box:hover {{ transform: translateY(-4px); }}
    .box-title {{ font-size: 0.95rem; color: #555555; font-weight: bold; margin-bottom: 6px; }}
    .box-value {{ font-size: 1.4rem; font-weight: bold; color: {text_color}; }}
    .custom-progress-container {{ width: 100%; background-color: rgba(220, 220, 220, 0.6); border-radius: 25px; padding: 3px; margin: 25px 0; }}
    .custom-progress-bar {{
        background-color: {primary_color}; height: 28px; border-radius: 20px; text-align: center;
        line-height: 28px; color: white; font-weight: bold; transition: width 0.8s ease-in-out;
    }}
    .product-card {{ background: white; border-radius: 16px; padding: 20px; text-align: center; box-shadow: 0 6px 18px rgba(0,0,0,0.04); border: 1px solid #eee; height: 100%; }}
    .product-btn {{ background-color: #ff9900; color: white !important; border-radius: 8px; padding: 8px 18px; text-decoration: none; display: inline-block; font-weight: bold; margin-top: 15px; }}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown(f'<h1 class="main-title">💖 Aspettando Te Premium 💖</h1>', unsafe_allow_html=True)
# Inizio Sezione Input Dati
col1, col2 = st.columns(2)

with col1:
    nome = st.text_input("Nome del bambino/a", value=dati_salvati.get("nome", ""), placeholder="Scrivi qui il nome...")
    sesso_mappa = {"👧 Femmina": "F", "👦 Maschio": "M", "🤍 Non lo sappiamo ancora": "N"}
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

btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col1: esegui_calcolo = st.button("✨ Calcola Stato", use_container_width=True)
with btn_col2: resetta = st.button("🔄 Reset Dati", use_container_width=True)

if ultimo_ciclo > datetime.today().date():
    st.error("Attenzione: La data dell'ultimo ciclo non può essere futura!")
    esegui_calcolo = False

if resetta:
    if os.path.exists(FILE_DATI): os.remove(FILE_DATI)
    st.rerun()

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
    
    if nome:
        img = Image.new("RGB", (1080, 1080), "#fff0f7" if sesso_codice=="F" else "#f0f8ff" if sesso_codice=="M" else "#fffef0")
        draw = ImageDraw.Draw(img)
        draw.text((120, 120), f"Aspettando {nome}", fill="#d63384" if sesso_codice=="F" else "#1976d2", font=ImageFont.load_default())
        draw.text((120, 280), f"Data Parto: {dpp_finale.strftime('%d/%m/%Y')}\nSettimana: {settimane}+{giorni_extra}gg", fill="black", font=ImageFont.load_default())
        img.save("condivisione.png")
        with open("condivisione.png", "rb") as file_img:
            with btn_col3: st.download_button(label="📸 Scarica Immagine", data=file_img, file_name=f"{nome}_countdown.png", mime="image/png", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Sezione Vetrine Affiliazione Amazon
st.markdown("<br><h3 style='text-align:center; color:#444;'>🛍️ Prodotti Consigliati per la Mamma</h3>", unsafe_allow_html=True)
prod_col1, prod_col2, prod_col3 = st.columns(3)

with prod_col1:
    st.markdown('<div class="product-card"><span style="font-size:3rem;">🤰</span><h4>Cuscino Gravidanza</h4><p style="font-size:0.85rem; color:#666;">Supporto ergonomico XXL per il riposo.</p><a class="product-btn" href="https://amazon.it" target="_blank">Vedi su Amazon 🛒</a></div>', unsafe_allow_html=True)
with prod_col2:
    st.markdown('<div class="product-card"><span style="font-size:3rem;">🧴</span><h4>Olio Smagliature Bio</h4><p style="font-size:0.85rem; color:#666;">Idratante naturale elasticizzante.</p><a class="product-btn" href="https://amazon.it" target="_blank">Vedi su Amazon 🛒</a></div>', unsafe_allow_html=True)
with prod_col3:
    st.markdown('<div class="product-card"><span style="font-size:3rem;">📔</span><h4>Diario dei Ricordi</h4><p style="font-size:0.85rem; color:#666;">Per annotare le emozioni dei 9 mesi.</p><a class="product-btn" href="https://amazon.it" target="_blank">Vedi su Amazon 🛒</a></div>', unsafe_allow_html=True)
