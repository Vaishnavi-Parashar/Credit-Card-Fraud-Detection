import streamlit as st
import pandas as pd
import joblib
import sqlite3
import hashlib


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RedFlag AI — Cyber Risk Intelligence",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# DATABASE
# ============================================================

DB_NAME = "users.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def register_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users
            (username, email, password)
            VALUES (?, ?, ?)
            """,
            (
                username,
                email,
                hash_password(password)
            )
        )
        conn.commit()
        conn.close()
        return True, "Registration successful."

    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username or email already exists."


def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username, email
        FROM users
        WHERE username = ? AND password = ?
        """,
        (
            username,
            hash_password(password)
        )
    )

    user = cursor.fetchone()
    conn.close()
    return user


create_database()


# ============================================================
# LOAD MODEL
# ============================================================

try:
    model = joblib.load("fraud_model_top5.pkl")
    top_features = joblib.load("top5_features.pkl")

except FileNotFoundError:
    st.error(
        "Model files not found. Make sure these files are in the "
        "same folder as app.py:"
    )
    st.code(
        """
fraud_model_top5.pkl
top5_features.pkl
        """
    )
    st.stop()


# ============================================================
# SESSION MANAGEMENT
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "page" not in st.session_state:
    st.session_state.page = "login"


# ============================================================
# PREMIUM REDFLAG CYBERSECURITY DESIGN SYSTEM
# ============================================================

st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

/* ============================================================
   REDFLAG COLOR PALETTE & VARIABLES
   ============================================================ */

:root {
    --bg-dark-1: #08070b;
    --bg-dark-2: #0d0a10;
    --bg-dark-3: #120a11;
    --bg-secondary: #111019;
    --panel-bg: #15121c;
    --input-bg: #181422;
    
    --redflag-primary: #ff3154;
    --redflag-secondary: #e92b4f;
    --redflag-soft: #ff7188;
    --redflag-glow: rgba(255, 49, 84, 0.18);
    --border-accent: rgba(255, 49, 84, 0.30);
    
    --text-main: #ffffff;
    --text-secondary: #b7aebb;
    --text-muted: #817887;
    --border-subtle: rgba(255, 255, 255, 0.10);
    
    --alert-fraud: #ff3154;
    --alert-safe: #3dd68c;
}

/* ============================================================
   GLOBAL STYLES & TYPOGRAPHY
   ============================================================ */

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

h1, h2, h3, h4, .grotesk-font, .brand-title, .hero-title, .auth-title {
    font-family: 'Space Grotesk', sans-serif !important;
}

.mono-font {
    font-family: 'Space Mono', monospace !important;
}

.stApp {
    min-height: 100vh;
    background: 
        radial-gradient(circle at 50% -5%, rgba(255, 49, 84, 0.22) 0%, transparent 60%),
        radial-gradient(circle at 85% 25%, rgba(18, 10, 17, 0.8) 0%, transparent 50%),
        radial-gradient(circle at 15% 85%, rgba(233, 43, 79, 0.10) 0%, transparent 50%),
        linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px),
        #08070b !important;
    background-size: 100% 100%, 100% 100%, 100% 100%, 32px 32px, 32px 32px, 100% 100% !important;
    color: var(--text-main);
    overflow-x: hidden;
}

/* Keyframe Animations */
@keyframes shieldFloat {
    0%, 100% {
        transform: translateY(0px);
        filter: drop-shadow(0 0 16px rgba(255, 49, 84, 0.4));
    }
    50% {
        transform: translateY(-8px);
        filter: drop-shadow(0 0 28px rgba(255, 49, 84, 0.75));
    }
}

@keyframes glowPulse {
    0%, 100% {
        box-shadow: 0 0 60px rgba(255, 49, 84, 0.12);
        border-color: rgba(255, 49, 84, 0.35);
    }
    50% {
        box-shadow: 0 0 80px rgba(255, 49, 84, 0.28);
        border-color: rgba(255, 49, 84, 0.60);
    }
}

@keyframes dotPulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.3); opacity: 0.6; }
}

@keyframes fillBar {
    from { width: 0%; }
    to { width: var(--fill-percent); }
}

/* ============================================================
   STREAMLIT HEADER OVERRIDES & ALIGNMENT
   ============================================================ */

[data-testid="stHeader"] {
    background: rgba(8, 7, 11, 0.88) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    height: 62px !important;
    z-index: 999999 !important;
    border-bottom: 1px solid var(--border-subtle) !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

.block-container {
    max-width: 1140px !important;
    padding-top: 5.8rem !important;
    padding-bottom: 4.5rem !important;
}

#MainMenu, footer {
    visibility: hidden;
}

/* ============================================================
   AUTHENTICATION HIERARCHY & CENTERING
   ============================================================ */

.auth-header-hierarchy {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    margin-bottom: 26px;
    width: 100%;
}

.auth-shield-logo {
    width: 72px;
    height: 72px;
    margin-bottom: 16px;
    animation: shieldFloat 4s ease-in-out infinite;
}

.auth-brand-title {
    font-size: 56px;
    font-weight: 800;
    letter-spacing: -1.8px;
    color: #ffffff;
    line-height: 1.05;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2px;
}

.auth-brand-title span.red-accent {
    color: var(--redflag-primary);
    text-shadow: 0 0 20px rgba(255, 49, 84, 0.6);
}

.auth-tagline-text {
    font-size: 16px;
    font-weight: 500;
    font-style: italic;
    color: var(--text-secondary);
    letter-spacing: 0.3px;
    margin-bottom: 8px;
    text-shadow: 0 0 12px rgba(255, 113, 136, 0.25);
}

.auth-sub-header {
    font-size: 12px;
    font-weight: 800;
    color: var(--redflag-soft);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 22px;
}

/* Cybersecurity Status Indicators */
.security-status-group {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 32px;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(17, 16, 25, 0.85);
    border: 1px solid var(--border-subtle);
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    color: var(--text-secondary);
    letter-spacing: 1px;
    text-transform: uppercase;
    backdrop-filter: blur(8px);
}

.status-badge .pulse-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--redflag-primary);
    box-shadow: 0 0 10px var(--redflag-primary);
    animation: dotPulse 2s ease-in-out infinite;
}

/* ============================================================
   STRICT STREAMLIT TAB CONTAINER CENTERING (ALIGNED TO HEADING)
   ============================================================ */

div[data-testid="stTabs"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
    margin: 0 auto !important;
}

div[data-testid="stTabs"] > div {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
}

div[data-testid="stTabs"] [data-baseweb="tab-list"],
div[data-baseweb="tab-list"] {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 16px !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12) !important;
    background: transparent !important;
    margin: 0 auto 28px auto !important;
    width: 100% !important;
    max-width: 480px !important;
}

div[data-baseweb="tab"] {
    color: var(--text-secondary) !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 12px 28px !important;
    border-radius: 12px 12px 0 0 !important;
    background: transparent !important;
    border: none !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    flex: 1 1 auto !important;
    text-align: center !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

div[data-baseweb="tab"]:hover {
    color: #ffffff !important;
    background: rgba(255, 49, 84, 0.08) !important;
}

div[aria-selected="true"] {
    color: var(--redflag-primary) !important;
    border-bottom: 3px solid var(--redflag-primary) !important;
    background: rgba(255, 49, 84, 0.14) !important;
    box-shadow: inset 0 -10px 20px rgba(255, 49, 84, 0.15) !important;
}

div[data-baseweb="tab-panel"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
}

div[data-baseweb="tab-panel"] > div {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
    max-width: 480px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Glass/Security Auth Terminal Card */
.auth-terminal-panel {
    background: rgba(20, 16, 26, 0.94);
    border: 1px solid rgba(255, 49, 84, 0.40);
    border-radius: 24px;
    padding: 38px 44px;
    width: 100%;
    max-width: 480px;
    margin: 0 auto 24px;
    box-shadow: 0 0 60px rgba(255, 49, 84, 0.12);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    animation: glowPulse 5s ease-in-out infinite;
    text-align: left;
    position: relative;
    overflow: hidden;
}

.auth-terminal-panel::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--redflag-primary), transparent);
}

.card-title-head {
    font-size: 22px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 6px;
    text-align: center;
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: 0.5px;
}

.card-sub-desc {
    font-size: 13px;
    color: var(--text-secondary);
    margin-bottom: 26px;
    text-align: center;
}

/* ============================================================
   INPUT FIELDS & CTA BUTTONS
   ============================================================ */

[data-testid="stTextInput"], [data-testid="stNumberInput"] {
    margin-bottom: 18px;
    width: 100% !important;
}

[data-testid="stTextInput"] label, [data-testid="stNumberInput"] label {
    color: var(--text-main) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.3px;
    margin-bottom: 6px !important;
}

[data-testid="stTextInput"] input, [data-testid="stNumberInput"] input {
    background: var(--input-bg) !important;
    color: var(--text-main) !important;
    border: 1px solid rgba(255, 255, 255, 0.10) !important;
    border-radius: 12px !important;
    min-height: 48px !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.25s ease !important;
}

[data-testid="stTextInput"] input:focus, [data-testid="stNumberInput"] input:focus {
    border-color: var(--redflag-primary) !important;
    box-shadow: 0 0 18px rgba(255, 49, 84, 0.18) !important;
    background: #1d182a !important;
}

/* Primary Red Gradient CTA Button */
.stButton > button {
    background: linear-gradient(90deg, #e92b4f, #ff3154) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    min-height: 50px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 0.8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    box-shadow: 0 10px 25px rgba(233, 43, 79, 0.4) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #ff3154, #ff5270) !important;
    box-shadow: 0 14px 35px rgba(255, 49, 84, 0.6) !important;
    transform: translateY(-2px) !important;
    filter: brightness(1.08) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ============================================================
   HEADER & NAVBAR
   ============================================================ */

.navbar-brand-group {
    display: flex;
    align-items: center;
    gap: 10px;
}

.navbar-brand-title {
    font-size: 26px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.8px;
    display: flex;
    align-items: center;
    gap: 4px;
}

.navbar-brand-title span.red-accent {
    color: var(--redflag-primary);
}

.navbar-badge {
    background: rgba(255, 49, 84, 0.15);
    border: 1px solid var(--border-accent);
    color: var(--redflag-soft);
    font-size: 11px;
    padding: 3px 9px;
    border-radius: 6px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.user-session-badge {
    background: var(--panel-bg);
    border: 1px solid var(--border-accent);
    padding: 8px 18px;
    border-radius: 30px;
    font-size: 13px;
    color: var(--text-secondary);
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
}

.user-session-badge b {
    color: #ffffff;
}

/* ============================================================
   HERO BANNER
   ============================================================ */

.hero-panel-card {
    background: linear-gradient(145deg, rgba(21, 18, 28, 0.95), rgba(27, 22, 35, 0.88));
    border: 1px solid var(--border-accent);
    border-radius: 26px;
    padding: 38px 44px;
    margin-bottom: 38px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.6), 0 0 35px rgba(255, 49, 84, 0.12);
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    gap: 36px;
}

.hero-panel-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--redflag-primary), transparent);
}

.hero-panel-content {
    flex: 1;
}

.hero-pill-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 49, 84, 0.14);
    border: 1px solid var(--border-accent);
    color: var(--redflag-soft);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.6px;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 14px;
    text-transform: uppercase;
}

.hero-main-heading {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1.2px;
    color: #ffffff;
    line-height: 1.1;
    margin-bottom: 8px;
}

.hero-tagline-quote {
    font-size: 16px;
    font-weight: 600;
    font-style: italic;
    color: var(--redflag-soft);
    margin-bottom: 14px;
}

.hero-body-desc {
    font-size: 15px;
    line-height: 1.65;
    color: var(--text-secondary);
    max-width: 650px;
}

.hero-svg-badge {
    flex-shrink: 0;
    width: 180px;
    height: 180px;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: shieldFloat 4.5s ease-in-out infinite;
}

/* ============================================================
   SECTIONS & CARDS
   ============================================================ */

.section-title-bar {
    font-size: 24px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.5px;
    margin-top: 40px;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Space Grotesk', sans-serif !important;
}

.section-sub-text {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 22px;
}

.feature-glass-box {
    background: var(--panel-bg);
    border: 1px solid var(--border-accent);
    border-radius: 18px;
    padding: 22px 18px;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    text-align: center;
}

.feature-glass-box:hover {
    background: #1b1623;
    border-color: var(--redflag-primary);
    transform: translateY(-4px);
    box-shadow: 0 14px 30px rgba(255, 49, 84, 0.25);
}

.feature-rank-tag {
    font-size: 10px;
    font-weight: 800;
    color: var(--text-muted);
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.feature-code-name {
    font-size: 26px;
    font-weight: 800;
    color: var(--redflag-primary);
    margin-top: 6px;
    font-family: 'Space Mono', monospace;
}

/* ============================================================
   PREDICTION RESULT CARDS
   ============================================================ */

.result-card-panel {
    border-radius: 22px;
    padding: 32px 38px;
    margin-top: 26px;
    position: relative;
    backdrop-filter: blur(14px);
    transition: all 0.3s ease;
}

.result-card-panel.fraud {
    background: linear-gradient(135deg, rgba(255, 49, 84, 0.18) 0%, rgba(21, 18, 28, 0.98) 100%);
    border: 1px solid var(--alert-fraud);
    box-shadow: 0 16px 45px rgba(255, 49, 84, 0.28);
}

.result-card-panel.safe {
    background: linear-gradient(135deg, rgba(61, 214, 140, 0.18) 0%, rgba(21, 18, 28, 0.98) 100%);
    border: 1px solid var(--alert-safe);
    box-shadow: 0 16px 45px rgba(61, 214, 140, 0.22);
}

.result-tag-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.result-card-panel.fraud .result-tag-label { color: var(--alert-fraud); }
.result-card-panel.safe .result-tag-label { color: var(--alert-safe); }

.result-header-text {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: 'Space Grotesk', sans-serif !important;
}

.result-body-text {
    font-size: 15px;
    color: var(--text-main);
    line-height: 1.65;
}

.risk-meter-track {
    margin-top: 16px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    height: 10px;
    width: 100%;
    overflow: hidden;
}

.risk-meter-bar {
    height: 100%;
    border-radius: 12px;
    animation: fillBar 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.result-card-panel.fraud .risk-meter-bar {
    background: linear-gradient(90deg, #ff7188, #ff3154);
    box-shadow: 0 0 12px rgba(255, 49, 84, 0.8);
}

.result-card-panel.safe .risk-meter-bar {
    background: linear-gradient(90deg, #52e8a1, #3dd68c);
    box-shadow: 0 0 12px rgba(61, 214, 140, 0.8);
}

.prob-score-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 8px 18px;
    border-radius: 10px;
    font-weight: 800;
    color: #ffffff;
    font-family: 'Space Mono', monospace;
    margin-top: 14px;
}

/* ============================================================
   HOW IT WORKS PIPELINE
   ============================================================ */

.pipeline-card-step {
    background: var(--panel-bg);
    border: 1px solid var(--border-subtle);
    border-radius: 20px;
    padding: 26px;
    height: 100%;
    transition: all 0.3s ease;
}

.pipeline-card-step:hover {
    border-color: var(--redflag-primary);
    transform: translateY(-4px);
    box-shadow: 0 14px 35px rgba(0, 0, 0, 0.5);
}

.step-num-code {
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    font-weight: 800;
    color: var(--redflag-soft);
    margin-bottom: 10px;
}

.pipeline-card-step h3 {
    font-size: 18px !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    margin-bottom: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.pipeline-card-step p {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.6;
    margin: 0;
}

/* ============================================================
   FOOTER
   ============================================================ */

.footer-cyber-line {
    text-align: center;
    color: var(--text-muted);
    font-size: 13px;
    margin-top: 54px;
    padding-top: 26px;
    border-top: 1px solid var(--border-subtle);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.footer-cyber-line span {
    color: var(--redflag-soft);
    font-weight: 700;
}

/* Responsive fixes */
@media (max-width: 768px) {
    .hero-panel-card {
        flex-direction: column;
        padding: 26px;
        text-align: center;
    }
    .hero-svg-badge {
        width: 150px;
        height: 150px;
    }
    .auth-brand-title {
        font-size: 40px;
    }
    .auth-terminal-panel {
        padding: 26px 20px;
    }
}
</style>
""")


# ============================================================
# CUSTOM VECTOR SVG SHIELD LOGO & ICONS (NO EMOJIS)
# ============================================================

def get_redflag_shield_svg(width=68, height=68):
    """Geometric, minimal, modern SVG shield with 'R' emblem (No emoji)."""
    return f"""
    <svg width="{width}" height="{height}" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="shieldBg" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ff3154" />
                <stop offset="100%" stop-color="#9a132e" />
            </linearGradient>
            <filter id="redGlowEffect" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="5" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <!-- Outer Shield Frame -->
        <path d="M50 8L18 22V46C18 68 32 86 50 92C68 86 82 68 82 46V22L50 8Z" fill="url(#shieldBg)" stroke="#ff7188" stroke-width="2" filter="url(#redGlowEffect)"/>
        <!-- Inner Dark Panel -->
        <path d="M50 18L26 28V47C26 63 36 77 50 82C64 77 74 63 74 47V28L50 18Z" fill="#15121c" opacity="0.9"/>
        <!-- Minimal 'R' Emblem -->
        <path d="M44 36H53C56.5 36 59 38.5 59 41.5C59 44.5 56.5 47 53 47H44V36ZM44 47H52L59 62H52.5L46.5 49H44V62H39.5V36H44V47Z" fill="#ffffff"/>
    </svg>
    """


def get_search_svg(width=18, height=18):
    return f"""
    <svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" stroke="#ff3154" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px; margin-right:6px;">
        <circle cx="11" cy="11" r="8"/>
        <line x1="21" y1="21" x2="16.65" y2="16.65"/>
    </svg>
    """


def get_brain_svg(width=22, height=22):
    return f"""
    <svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" stroke="#ff3154" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-3px; margin-right:8px;">
        <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 4.44-2.04Z"/>
        <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-4.44-2.04Z"/>
    </svg>
    """


def get_zap_svg(width=22, height=22):
    return f"""
    <svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" stroke="#ff3154" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-3px; margin-right:8px;">
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
    </svg>
    """


def get_gears_svg(width=22, height=22):
    return f"""
    <svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" stroke="#ff3154" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-3px; margin-right:8px;">
        <circle cx="12" cy="12" r="3"/>
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
    </svg>
    """


def get_alert_svg(width=24, height=24):
    return f"""
    <svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" stroke="#ff3154" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
        <line x1="12" y1="9" x2="12" y2="13"/>
        <line x1="12" y1="17" x2="12.01" y2="17"/>
    </svg>
    """


def get_check_svg(width=24, height=24):
    return f"""
    <svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" stroke="#3dd68c" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
        <polyline points="22 4 12 14.01 9 11.01"/>
    </svg>
    """


def get_hero_graphic_svg(size=180):
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 240 240" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="120" cy="120" r="100" fill="#15121c" stroke="rgba(255, 49, 84, 0.3)" stroke-width="2"/>
        <circle cx="120" cy="120" r="94" stroke="#ff3154" stroke-width="1.5" stroke-dasharray="6 4" opacity="0.6"/>
        
        <text x="70" y="65" font-family="Space Mono, monospace" font-size="10" fill="#ff7188" font-weight="700" opacity="0.8">011010</text>
        <text x="148" y="82" font-family="Space Mono, monospace" font-size="9" fill="#ffffff" font-weight="700" opacity="0.6">10</text>
        <text x="56" y="100" font-family="Space Mono, monospace" font-size="9" fill="#ffffff" font-weight="700" opacity="0.5">11010</text>
        <text x="145" y="115" font-family="Space Mono, monospace" font-size="9" fill="#ff3154" font-weight="700" opacity="0.9">11101</text>
        <text x="156" y="142" font-family="Space Mono, monospace" font-size="8" fill="#ff7188" font-weight="700" opacity="0.7">101011</text>

        <rect x="42" y="70" width="40" height="70" rx="8" fill="#08070b"/>
        <rect x="45" y="74" width="34" height="62" rx="5" fill="#1b1623"/>
        <circle cx="62" cy="105" r="11" fill="#e92b4f"/>
        <text x="56" y="110" font-family="Space Grotesk, sans-serif" font-size="12" font-weight="800" fill="#ffffff">RF</text>

        <rect x="42" y="150" width="48" height="28" rx="4" fill="#292033"/>
        <rect x="42" y="160" width="48" height="6" fill="#e92b4f"/>
        <rect x="47" y="168" width="8" height="6" rx="1" fill="#ffffff"/>

        <path d="M125 58C148 58 178 75 185 105H115C115 80 120 58 125 58Z" fill="#08070b"/>
        <path d="M117 96C140 98 160 98 183 96V105H117V96Z" fill="#e92b4f"/>
        <path d="M110 105C110 105 140 108 190 105C185 110 178 114 150 114C122 114 115 110 110 105Z" fill="#15121c"/>
        <circle cx="150" cy="60" r="4.5" fill="#ff3154"/>

        <path d="M135 125C135 125 130 152 155 158C180 164 190 135 190 120" stroke="#08070b" stroke-width="6" stroke-linecap="round"/>
        <path d="M187 120H193V132H187Z" fill="#ffffff" rx="1"/>

        <g>
            <path d="M115 138L138 168" stroke="#08070b" stroke-width="9" stroke-linecap="round"/>
            <path d="M115 138L138 168" stroke="#e92b4f" stroke-width="5" stroke-linecap="round"/>
            <circle cx="106" cy="124" r="24" fill="#292033" stroke="#08070b" stroke-width="4"/>
            <circle cx="106" cy="124" r="20" fill="#e9e4ea"/>
            <text x="94" y="131" font-family="Space Mono, monospace" font-size="16" font-weight="800" fill="#e92b4f">101</text>
        </g>
    </svg>
    """


# ============================================================
# AUTHENTICATION PAGE (PERFECTLY CENTERED HIERARCHY)
# ============================================================

if not st.session_state.logged_in:

    # 1. CENTERED BRANDING & SHIELD LOGO HIERARCHY
    st.html(f"""
    <div class="auth-header-hierarchy">
        <div class="auth-shield-logo">
            {get_redflag_shield_svg(72, 72)}
        </div>
        <div class="auth-brand-title">
            Red<span class="red-accent">Flag</span>
        </div>
        <div class="auth-tagline-text">
            "Flagging fraud before it flags you."
        </div>
        <div class="auth-sub-header">
            INTELLIGENT FRAUD PREVENTION
        </div>
        <div class="security-status-group">
            <div class="status-badge"><span class="pulse-dot"></span> AI MODEL ONLINE</div>
            <div class="status-badge"><span class="pulse-dot"></span> SECURE SESSION</div>
            <div class="status-badge"><span class="pulse-dot"></span> REAL-TIME RISK ANALYSIS</div>
        </div>
    </div>
    """)

    # 2. CENTERED STREAMLIT TABS
    login_tab, register_tab = st.tabs(
        [
            "Sign In",
            "Create Account"
        ]
    )

    # 3. CENTERED FORM TERMINAL PANELS
    with login_tab:
        st.html("""
        <div class="auth-terminal-panel">
            <div class="card-title-head">SECURE ACCESS</div>
            <div class="card-sub-desc">
                Sign in to analyze credit card transactions using the trained Random Forest model.
            </div>
        </div>
        """)

        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        login_clicked = st.button(
            "SIGN IN",
            use_container_width=True,
            key="login_button"
        )

        if login_clicked:
            if username.strip() == "" or password.strip() == "":
                st.warning("Please enter both username and password.")
            else:
                user = login_user(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user[0]
                    st.session_state.username = user[1]
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

    with register_tab:
        st.html("""
        <div class="auth-terminal-panel">
            <div class="card-title-head">CREATE ACCOUNT</div>
            <div class="card-sub-desc">
                Set up your secure RedFlag workspace credentials.
            </div>
        </div>
        """)

        new_username = st.text_input(
            "Username",
            placeholder="Choose a username",
            key="register_username"
        )

        new_email = st.text_input(
            "Email",
            placeholder="Enter your email address",
            key="register_email"
        )

        new_password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="register_confirm"
        )

        register_clicked = st.button(
            "CREATE ACCOUNT",
            use_container_width=True,
            key="register_button"
        )

        if register_clicked:
            if (
                new_username.strip() == ""
                or new_email.strip() == ""
                or new_password.strip() == ""
                or confirm_password.strip() == ""
            ):
                st.warning("Please fill in all fields.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            elif len(new_password) < 6:
                st.error("Password must contain at least 6 characters.")
            else:
                success, message = register_user(
                    new_username.strip(),
                    new_email.strip(),
                    new_password
                )
                if success:
                    st.success("Account created successfully! You can now sign in.")
                else:
                    st.error(message)

    st.html(f"""
    <div class="footer-cyber-line">
        {get_redflag_shield_svg(16, 16)} <span>RedFlag</span> · "Flagging fraud before it flags you."
    </div>
    """)
    st.stop()


# ============================================================
# DASHBOARD NAVIGATION
# ============================================================

nav1, nav2, nav3 = st.columns([5, 3, 1.2])

with nav1:
    st.html(f"""
    <div class="navbar-brand-group">
        {get_redflag_shield_svg(28, 28)}
        <div class="navbar-brand-title">
            Red<span class="red-accent">Flag</span>
        </div>
        <span class="navbar-badge mono-font">AI ENGINE</span>
    </div>
    """)

with nav2:
    st.html(
        f"""
        <div class="user-session-badge">
            ● Active Analyst: <b>{st.session_state.username}</b>
        </div>
        """
    )

with nav3:
    logout_clicked = st.button("Logout", use_container_width=True)
    if logout_clicked:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_id = None
        st.session_state.page = "login"
        st.rerun()


# ============================================================
# HERO SECTION
# ============================================================

st.html(f"""
<div class="hero-panel-card">
    <div class="hero-panel-content">
        <div class="hero-pill-tag mono-font">
            {get_search_svg(14, 14)} REAL-TIME RISK ANALYSIS ENGINE
        </div>
        <div class="hero-main-heading">
            Intelligent Fraud Prevention
        </div>
        <div class="hero-tagline-quote">
            "Flagging fraud before it flags you."
        </div>
        <div class="hero-body-desc">
            Evaluate credit card transaction PCA feature patterns using an optimized <b>Random Forest Classifier</b>.
            Trained on feature importance scoring to instantly detect suspicious anomaly signals.
        </div>
    </div>
    <div class="hero-svg-badge">
        {get_hero_graphic_svg(180)}
    </div>
</div>
""")


# ============================================================
# MODEL INTELLIGENCE (TOP 5 FEATURES)
# ============================================================

st.html(f'<div class="section-title-bar">{get_brain_svg(22, 22)} Model Intelligence</div>')
st.html("""
<div class="section-sub-text">
    Top 5 features selected through Random Forest feature importance scoring.
</div>
""")

feature_columns = st.columns(5)

for i, feature in enumerate(top_features):
    with feature_columns[i]:
        st.html(
            f"""
            <div class="feature-glass-box">
                <div class="feature-rank-tag">RANK 0{i + 1}</div>
                <div class="feature-code-name">{feature}</div>
            </div>
            """
        )


# ============================================================
# TRANSACTION RISK ANALYSIS INPUTS
# ============================================================

st.html(f'<div class="section-title-bar">{get_zap_svg(22, 22)} Check Transaction Risk</div>')
st.html("""
<div class="section-sub-text">
    Provide feature parameter values below to evaluate potential risk probabilities.
</div>
""")

col1, col2, col3 = st.columns(3)

with col1:
    v14 = st.number_input(
        "V14 Feature Value",
        value=0.0,
        format="%.6f",
        key="v14_input"
    )

with col2:
    v10 = st.number_input(
        "V10 Feature Value",
        value=0.0,
        format="%.6f",
        key="v10_input"
    )

with col3:
    v12 = st.number_input(
        "V12 Feature Value",
        value=0.0,
        format="%.6f",
        key="v12_input"
    )

col4, col5 = st.columns(2)

with col4:
    v17 = st.number_input(
        "V17 Feature Value",
        value=0.0,
        format="%.6f",
        key="v17_input"
    )

with col5:
    v4 = st.number_input(
        "V4 Feature Value",
        value=0.0,
        format="%.6f",
        key="v4_input"
    )


# ============================================================
# PREDICTION ENGINE WITH ANIMATED RISK METER
# ============================================================

analyze_clicked = st.button("ANALYZE TRANSACTION")

if analyze_clicked:

    input_data = pd.DataFrame(
        [[v14, v10, v12, v17, v4]],
        columns=["V14", "V10", "V12", "V17", "V4"]
    )

    input_data = input_data[top_features]

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]
    probability_percent = probability * 100

    if prediction == 1:
        st.html(
            f"""
            <div class="result-card-panel fraud">
                <div class="result-tag-label">{get_alert_svg(16, 16)} ALERT DETECTED</div>
                <div class="result-header-text">Potential Fraud Detected</div>
                <div class="result-body-text">
                    The Random Forest classifier has flagged this transaction pattern as <b>high risk</b>.
                    <div class="risk-meter-track">
                        <div class="risk-meter-bar" style="--fill-percent: {probability_percent:.1f}%;"></div>
                    </div>
                    <div class="prob-score-badge">Fraud Risk Probability: {probability_percent:.2f}%</div>
                </div>
            </div>
            """
        )
    else:
        st.html(
            f"""
            <div class="result-card-panel safe">
                <div class="result-tag-label">{get_check_svg(16, 16)} VERIFIED GENUINE</div>
                <div class="result-header-text">Transaction Appears Genuine</div>
                <div class="result-body-text">
                    The Random Forest classifier evaluated this feature pattern within <b>normal parameters</b>.
                    <div class="risk-meter-track">
                        <div class="risk-meter-bar" style="--fill-percent: {probability_percent:.1f}%;"></div>
                    </div>
                    <div class="prob-score-badge">Fraud Risk Probability: {probability_percent:.2f}%</div>
                </div>
            </div>
            """
        )


# ============================================================
# HOW IT WORKS
# ============================================================

st.html(f'<div class="section-title-bar">{get_gears_svg(22, 22)} How It Works</div>')
st.html("""
<div class="section-sub-text">
    End-to-end classification pipeline for live transaction parameters.
</div>
""")

c1, c2, c3 = st.columns(3)

with c1:
    st.html("""
    <div class="pipeline-card-step">
        <div class="step-num-code">01 // PARSE</div>
        <h3>Feature Extraction</h3>
        <p>Captures top 5 PCA features (V14, V10, V12, V17, V4) from transaction telemetry.</p>
    </div>
    """)

with c2:
    st.html("""
    <div class="pipeline-card-step">
        <div class="step-num-code">02 // EVALUATE</div>
        <h3>Random Forest Inference</h3>
        <p>Evaluates feature splits across decision tree ensembles in real-time.</p>
    </div>
    """)

with c3:
    st.html("""
    <div class="pipeline-card-step">
        <div class="step-num-code">03 // DECIDE</div>
        <h3>Risk Score Output</h3>
        <p>Returns binary classification status along with precise fraud probability scores.</p>
    </div>
    """)


# ============================================================
# FOOTER
# ============================================================

st.html(f"""
<div class="footer-cyber-line">
    {get_redflag_shield_svg(16, 16)} <span>RedFlag</span> · "Flagging fraud before it flags you." · Python · Scikit-Learn · Streamlit
</div>
""")