import streamlit as st
import random

# ─────────────────────────────────────────────
#  TESTS.PY DAN IMPORT
# ─────────────────────────────────────────────
from tests import UMUMIY_PEDAGOGIKA, TEXNOLOGIYA, TABIY_FAN, ONA_TILI, MATEMATIKA

# ─────────────────────────────────────────────
#  MA'LUMOTLARNI NORMALLASHTIRISH
#  (turli xil kalit nomlarini bir xilga keltirish)
# ─────────────────────────────────────────────
def normalize_savol(savol_dict):
    """
    Har xil formatdagi savol dict'larini bir xil formatga keltiradi:
    - variantlar kalitlarini katta harfga o'tkazadi (a→A, b→B ...)
    - 'S' kalitini 'C' ga o'zgartiradi
    - javob None bo'lsa 'A' deb belgilaydi
    - javobni ham katta harfga o'tkazadi
    """
    v = savol_dict.get("variantlar", {})

    # Kalitlarni normallashtirish: kichik harf → katta harf, S → C
    yangi_v = {}
    kalit_map = {}  # eski_kalit → yangi_kalit
    for k, qiymat in v.items():
        if k == "S":
            yangi_k = "C"
        else:
            yangi_k = k.upper()
        yangi_v[yangi_k] = qiymat
        kalit_map[k] = yangi_k

    # Javobni normallashtirish
    javob = savol_dict.get("javob")
    if javob is None:
        javob = list(yangi_v.keys())[0] if yangi_v else "A"
    elif javob == "S":
        javob = "C"
    else:
        javob = javob.upper()

    return {
        "id": savol_dict.get("id"),
        "savol": savol_dict.get("savol", ""),
        "variantlar": yangi_v,
        "javob": javob,
    }


def dict_dan_savollar(fan_dict):
    """
    {"fan": "...", "tests": [...]} formatidagi dict'dan
    normalashtirilgan savollar ro'yxatini qaytaradi.
    """
    raw = fan_dict.get("tests", [])
    return [normalize_savol(s) for s in raw]


# ─────────────────────────────────────────────
#  BARCHA FANLAR
# ─────────────────────────────────────────────
FANLAR_RAW = {
    UMUMIY_PEDAGOGIKA["fan"]: UMUMIY_PEDAGOGIKA,
    TEXNOLOGIYA["fan"]:       TEXNOLOGIYA,
    TABIY_FAN["fan"]:         TABIY_FAN,
    ONA_TILI["fan"]:          ONA_TILI,
    MATEMATIKA["fan"]:        MATEMATIKA,
}

# Fan nomi → normalashtirilgan savollar ro'yxati
tests = {fan_nomi: dict_dan_savollar(fan_dict)
         for fan_nomi, fan_dict in FANLAR_RAW.items()}

FAN_NOMLARI = list(tests.keys())
RANDOM_LABEL = "🎲 Random (Barcha fanlar)"

# ─────────────────────────────────────────────
#  SAHIFA KONFIGURATSIYASI
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="XUSNURA | Test Platformasi",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS USLUBLAR
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── ASOSIY FON ── */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    min-height: 100vh;
    font-family: 'DM Sans', sans-serif;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
    border-right: 1px solid rgba(255,215,0,0.15);
}
[data-testid="stSidebar"] * {
    color: #e0e0ff !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    padding: 6px 0;
    cursor: pointer;
    transition: color 0.2s;
}
[data-testid="stSidebar"] .stRadio label:hover {
    color: #ffd700 !important;
}

/* ── SARLAVHA ── */
.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 4rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #ffd700, #ff8c00, #ffd700);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shine 3s linear infinite;
    letter-spacing: 6px;
    margin: 10px 0 4px;
    text-shadow: none;
}
@keyframes shine {
    to { background-position: 200% center; }
}
.subtitle {
    text-align: center;
    color: rgba(255,255,255,0.45);
    font-size: 0.9rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 30px;
    font-family: 'DM Sans', sans-serif;
}

/* ── SAVOL KARTASI ── */
.question-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,215,0,0.2);
    border-radius: 16px;
    padding: 24px 28px;
    margin: 10px 0 18px;
    backdrop-filter: blur(8px);
    transition: border-color 0.3s;
}
.question-card:hover {
    border-color: rgba(255,215,0,0.45);
}
.q-number {
    font-size: 0.75rem;
    color: #ffd700;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 8px;
    font-weight: 600;
}
.q-text {
    font-size: 1.05rem;
    color: #f0f0ff;
    font-weight: 500;
    line-height: 1.6;
}

/* ── TUGMALAR ── */
div.stButton > button {
    background: linear-gradient(135deg, #ffd700, #ff8c00);
    color: #1a1a2e;
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    border: none;
    border-radius: 12px;
    padding: 12px 36px;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 4px 20px rgba(255,215,0,0.3);
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(255,215,0,0.45);
}

/* ── NATIJA KARTASI ── */
.result-box {
    background: linear-gradient(135deg, rgba(255,215,0,0.08), rgba(255,140,0,0.08));
    border: 2px solid rgba(255,215,0,0.4);
    border-radius: 20px;
    padding: 36px;
    text-align: center;
    margin: 20px 0;
}
.result-score {
    font-family: 'Playfair Display', serif;
    font-size: 4rem;
    font-weight: 900;
    color: #ffd700;
}
.result-label {
    font-size: 1.2rem;
    color: rgba(255,255,255,0.75);
    margin-top: 8px;
}
.result-emoji {
    font-size: 3.5rem;
    margin-bottom: 10px;
}

/* ── DIVIDER ── */
hr { border-color: rgba(255,215,0,0.15) !important; }

/* ── RADIO OPTIONS ── */
div[role="radiogroup"] label {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    margin: 4px 0 !important;
    color: #e0e0ff !important;
    transition: background 0.2s, border-color 0.2s;
    cursor: pointer;
}
div[role="radiogroup"] label:hover {
    background: rgba(255,215,0,0.08) !important;
    border-color: rgba(255,215,0,0.4) !important;
}

/* ── NUMBER INPUT ── */
.stNumberInput input {
    background: rgba(255,255,255,0.05) !important;
    color: #fff !important;
    border: 1px solid rgba(255,215,0,0.3) !important;
    border-radius: 8px !important;
}

/* ── INFO / WARNING ── */
.stAlert { border-radius: 12px !important; }

/* ── PROGRESS BAR ── */
.stProgress > div > div > div { background: linear-gradient(90deg,#ffd700,#ff8c00) !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SESSION STATE INITSIALIZATSIYA
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "sahifa": "menu",
        "tanlangan_fan": None,
        "test_soni": 10,
        "savollar": [],
        "javoblar": {},
        "joriy_savol": 0,
        "natija_korsatildi": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────
#  SARLAVHA
# ─────────────────────────────────────────────
st.markdown('<div class="main-title">✦ XUSNURA ✦</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bilim Platformasi · Test Markazi</div>', unsafe_allow_html=True)
st.divider()

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📚 Fanlar")
    st.markdown("---")
    sidebar_options = FAN_NOMLARI + [RANDOM_LABEL]
    tanlangan = st.radio(
        "Fan tanlang:",
        sidebar_options,
        index=sidebar_options.index(st.session_state.tanlangan_fan)
              if st.session_state.tanlangan_fan in sidebar_options else 0,
        key="sidebar_fan"
    )
    st.markdown("---")
    st.markdown("#### ℹ️ Ma'lumot")
    for fan in FAN_NOMLARI:
        st.markdown(f"**{fan}**: {len(tests[fan])} ta savol")
    st.markdown(f"**Jami**: {sum(len(v) for v in tests.values())} ta savol")

# ─────────────────────────────────────────────
#  FAN O'ZGARGANDA MENU GA QAYTISH
# ─────────────────────────────────────────────
if tanlangan != st.session_state.tanlangan_fan:
    st.session_state.tanlangan_fan = tanlangan
    st.session_state.sahifa = "menu"
    st.session_state.savollar = []
    st.session_state.javoblar = {}
    st.session_state.joriy_savol = 0
    st.session_state.natija_korsatildi = False
    st.rerun()

# ─────────────────────────────────────────────
#  SAHIFALAR
# ─────────────────────────────────────────────

# ══════════════════════════════════
# MENU SAHIFASI
# ══════════════════════════════════
if st.session_state.sahifa == "menu":
    fan = st.session_state.tanlangan_fan or FAN_NOMLARI[0]

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"## {fan}")

        if fan == RANDOM_LABEL:
            st.info("🎲 **Random rejim**: Barcha 5 ta fandan aralash holda **50 ta** savol beriladi.")
            if st.button("🚀 Testni Boshlash", use_container_width=True):
                tanlangan_savollar = []
                for f_nomi, f_savollar in tests.items():
                    labeled = [dict(s, fan=f_nomi) for s in f_savollar]
                    random.shuffle(labeled)
                    tanlangan_savollar.extend(labeled[:10])
                random.shuffle(tanlangan_savollar)
                st.session_state.savollar = tanlangan_savollar
                st.session_state.test_soni = len(tanlangan_savollar)
                st.session_state.javoblar = {}
                st.session_state.joriy_savol = 0
                st.session_state.natija_korsatildi = False
                st.session_state.sahifa = "test"
                st.rerun()
        else:
            max_q = len(tests[fan])
            st.info(f"📋 Bu fanda **{max_q} ta** savol mavjud.")
            soni = st.number_input(
                "Nechta savol ishlaysiz?",
                min_value=1,
                max_value=max_q,
                value=min(10, max_q),
                step=1
            )
            if st.button("🚀 Testni Boshlash", use_container_width=True):
                savollar_copy = [dict(s) for s in tests[fan]]
                random.shuffle(savollar_copy)
                tanlangan = savollar_copy[:soni]
                st.session_state.savollar = tanlangan
                st.session_state.test_soni = soni
                st.session_state.javoblar = {}
                st.session_state.joriy_savol = 0
                st.session_state.natija_korsatildi = False
                st.session_state.sahifa = "test"
                st.rerun()

# ══════════════════════════════════
# TEST SAHIFASI
# ══════════════════════════════════
elif st.session_state.sahifa == "test":
    savollar = st.session_state.savollar
    jami = len(savollar)
    javoblar = st.session_state.javoblar
    fan = st.session_state.tanlangan_fan

    # Progress
    tugallangan = len(javoblar)
    st.progress(tugallangan / jami if jami > 0 else 0)
    st.markdown(
        f"<p style='color:rgba(255,255,255,0.5);font-size:0.85rem;text-align:right'>"
        f"Javob berildi: {tugallangan} / {jami}</p>",
        unsafe_allow_html=True
    )

    # Savollarni ko'rsatish
    for i, savol_data in enumerate(savollar):
        fan_label = savol_data.get("fan", fan)
        variantlar_dict = savol_data["variantlar"]

        # Variantlarni to'liq matn ko'rinishida ko'rsatish: "A: matn"
        options_labeled = [f"{k}: {v}" for k, v in variantlar_dict.items()]

        st.markdown(
            f'<div class="question-card">'
            f'<div class="q-number">Savol {i+1} · {fan_label}</div>'
            f'<div class="q-text">{savol_data["savol"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        display_options = ["— Tanlang —"] + options_labeled
        prev = javoblar.get(i, "— Tanlang —")
        sel = st.radio(
            f"savol_{i}",
            display_options,
            index=display_options.index(prev) if prev in display_options else 0,
            key=f"radio_{i}",
            label_visibility="collapsed"
        )
        if sel != "— Tanlang —":
            javoblar[i] = sel
        elif i in javoblar:
            del javoblar[i]

        st.session_state.javoblar = javoblar
        st.markdown("<br>", unsafe_allow_html=True)

    # Yakunlash tugmasi
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if len(javoblar) < jami:
            st.warning(f"⚠️ Hali {jami - len(javoblar)} ta savolga javob berilmagan.")
        if st.button("✅ Testni Yakunlash", use_container_width=True):
            st.session_state.sahifa = "natija"
            st.session_state.natija_korsatildi = False
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    col_x, col_y = st.columns(2)
    with col_x:
        if st.button("🔄 Qayta Boshlash", use_container_width=True):
            st.session_state.sahifa = "menu"
            st.session_state.savollar = []
            st.session_state.javoblar = {}
            st.rerun()

# ══════════════════════════════════
# NATIJA SAHIFASI
# ══════════════════════════════════
elif st.session_state.sahifa == "natija":
    savollar = st.session_state.savollar
    javoblar = st.session_state.javoblar
    jami = len(savollar)
    fan = st.session_state.tanlangan_fan

    def javob_togri_mi(i, savol_data):
        """Foydalanuvchi tanlagan variant to'g'ri javobga mos keladimi?"""
        berilgan = javoblar.get(i)
        if berilgan is None:
            return False
        # berilgan = "A: matn" formatida — kalitni ajratib olamiz
        kalit = berilgan.split(":")[0].strip()
        return kalit == savol_data["javob"]

    to_gri = sum(1 for i, s in enumerate(savollar) if javob_togri_mi(i, s))
    xato = jami - to_gri
    foiz = round((to_gri / jami) * 100) if jami > 0 else 0

    # Baho
    if foiz >= 90:
        emoji = "🏆"; baho = "A'lo!"; rang = "#ffd700"
    elif foiz >= 70:
        emoji = "🎯"; baho = "Yaxshi!"; rang = "#00e676"
    elif foiz >= 50:
        emoji = "📈"; baho = "Qoniqarli"; rang = "#ff9800"
    else:
        emoji = "📚"; baho = "Ko'proq o'qing"; rang = "#ff5252"

    # Konfetti — har doim natija sahifasi birinchi ko'rsatilganda
    if not st.session_state.natija_korsatildi:
        st.snow()
        st.session_state.natija_korsatildi = True

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(
            f'<div class="result-box">'
            f'<div class="result-emoji">{emoji}</div>'
            f'<div class="result-score" style="color:{rang}">{foiz}%</div>'
            f'<div class="result-label" style="color:{rang};font-weight:700;font-size:1.4rem">{baho}</div>'
            f'<hr style="border-color:rgba(255,255,255,0.1);margin:16px 0">'
            f'<div style="display:flex;justify-content:space-around">'
            f'<div><div style="font-size:2rem;color:#00e676;font-weight:700">{to_gri}</div>'
            f'<div style="color:rgba(255,255,255,0.55);font-size:0.85rem">To\'g\'ri</div></div>'
            f'<div><div style="font-size:2rem;color:#ff5252;font-weight:700">{xato}</div>'
            f'<div style="color:rgba(255,255,255,0.55);font-size:0.85rem">Xato</div></div>'
            f'<div><div style="font-size:2rem;color:#fff;font-weight:700">{jami}</div>'
            f'<div style="color:rgba(255,255,255,0.55);font-size:0.85rem">Jami</div></div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Batafsil tahlil
        with st.expander("📊 Batafsil natijalar ko'rish"):
            for i, savol_data in enumerate(savollar):
                berilgan = javoblar.get(i, "Javob berilmagan")
                togri_kalit = savol_data["javob"]
                togri_matn = savol_data["variantlar"].get(togri_kalit, togri_kalit)
                fan_lbl = savol_data.get("fan", fan)
                if javob_togri_mi(i, savol_data):
                    icon = "✅"; color = "#00e676"
                else:
                    icon = "❌"; color = "#ff5252"
                st.markdown(
                    f"<div style='padding:10px;border-radius:10px;margin:6px 0;"
                    f"background:rgba(255,255,255,0.04);border-left:3px solid {color}'>"
                    f"<b style='color:{color}'>{icon} {i+1}. {savol_data['savol']}</b><br>"
                    f"<span style='color:rgba(255,255,255,0.6);font-size:0.85rem'>"
                    f"Sizning javob: <b style='color:#fff'>{berilgan}</b> · "
                    f"To'g'ri javob: <b style='color:#ffd700'>{togri_kalit}: {togri_matn}</b> · "
                    f"{fan_lbl}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 Qayta Urinish", use_container_width=True):
                st.session_state.sahifa = "menu"
                st.session_state.savollar = []
                st.session_state.javoblar = {}
                st.session_state.natija_korsatildi = False
                st.rerun()
        with c2:
            if st.button("📚 Boshqa Fan", use_container_width=True):
                st.session_state.sahifa = "menu"
                st.session_state.tanlangan_fan = FAN_NOMLARI[0]
                st.session_state.savollar = []
                st.session_state.javoblar = {}
                st.session_state.natija_korsatildi = False
                st.rerun()