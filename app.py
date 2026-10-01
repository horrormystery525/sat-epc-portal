import streamlit as st
import io
import re
import os
import pandas as pd
import pydeck as pdk
from PIL import Image
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="DocuSphere | SP & E.P.C. Interactive Portal",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# Bilingual Dictionary (English & Hindi)
# ---------------------------------------------------------
I18N = {
    "en": {
        "portal_badge": "● LIVE DIGITAL PORTAL",
        "zero_dl": "ZERO DOWNLOADS NEEDED",
        "all_38": "ALL 38 ILLUSTRATED PRODUCTS",
        "title": "Er. SATYAM PIYUSH — An E.P.C. Company",
        "tagline": "Turnkey Engineering, Procurement & Construction | Clean Green India Solutions",
        "tab_summary": "📖 Executive Summary & Profile",
        "tab_catalog": "🚜 Illustrated Catalog (38 Items)",
        "tab_compare": "⚖️ Side-by-Side Visual Comparer",
        "tab_map": "🗺️ Logistics & Offices Map",
        "tab_pages": "📑 Page-by-Page Explorer",
        "tab_search": "🔍 Search Across Document",
        "tab_qr": "📲 Share & QR Studio",
        "kpi_leadership": "Leadership Credentials",
        "kpi_leadership_sub": "Flight Testing & Ads Mgmt",
        "kpi_catalog": "Total Catalog Scope",
        "kpi_catalog_val": "38 Equipment Units",
        "kpi_catalog_sub": "Vehicles, Bins, Sanitation",
        "kpi_standards": "Accreditations",
        "kpi_standards_sub": "NSIC & Make in India",
        "kpi_phone": "Direct Helpline",
        "about_heading": "🏢 Enterprise Profile & Engineering Heritage",
        "about_body": """**Er. SATYAM PIYUSH — An E.P.C. Company** delivers turnkey Engineering, Procurement, and Construction (EPC) solutions for civic and municipal bodies across India.

##### 🌟 Executive Track Record & Industry Experience:
- ✈️ **Flight Testing Instrumentation** at **Hindustan Aeronautics Limited (HAL India)** — High-precision aerospace systems & instrumentation.
- 📈 **Advertising Manager** at **AMAZON India** — Large-scale operational execution and vendor coordination.
- 🏗️ **Turnkey Municipal Manufacturing** — Specializing in hydraulic waste compactors, street sweepers, community composters, and smart sanitation pods.""",
        "filter_vertical": "Filter by Vertical:",
        "filter_op": "Filter by Operation Mode:",
        "filter_mat": "Filter by Material:",
        "search_placeholder": "Search equipment, specs or models...",
        "all": "All",
        "reg_office": "Registered Office",
        "fab_base": "Fabrication & Workshop Base",
        "phone": "Telephone",
        "email": "Email",
        "open_gmaps": "🗺️ Open in Google Maps"
    },
    "hi": {
        "portal_badge": "● लाइव डिजिटल पोर्टल",
        "zero_dl": "बिना पीडीएफ डाउनलोड सीधा उपयोग",
        "all_38": "कुल 38 सचित्र उपकरण एवं मशीनें",
        "title": "इंजी. सत्यम पीयूष — एक ई.पी.सी. कंपनी",
        "tagline": "टर्नकी इंजीनियरिंग, खरीद और निर्माण (EPC) | स्वच्छ भारत और हरित भारत समाधान",
        "tab_summary": "📖 मुख्य कार्यकारी सारांश एवं परिचय",
        "tab_catalog": "🚜 सचित्र मशीनरी कैटलॉग (38 उत्पाद)",
        "tab_compare": "⚖️ तुलनात्मक विश्लेषण (Side-by-Side)",
        "tab_map": "🗺️ विनिर्माण एवं कार्यालय मानचित्र",
        "tab_pages": "📑 पृष्ठ-वार मूल दस्तावेज़",
        "tab_search": "🔍 दस्तावेज़ में त्वरित खोज",
        "tab_qr": "📲 लाइव लिंक एवं क्यूआर कोड",
        "kpi_leadership": "नेतृत्व का पूर्व अनुभव",
        "kpi_leadership_sub": "HAL एवं Amazon India",
        "kpi_catalog": "उपकरणों की कुल संख्या",
        "kpi_catalog_val": "38 उत्पाद इकाइयां",
        "kpi_catalog_sub": "वाहन, डस्टबिन, स्वच्छता संयंत्र",
        "kpi_standards": "प्रमाणन एवं मानक",
        "kpi_standards_sub": "ISO 9001:2015 एवं NSIC",
        "kpi_phone": "सीधी हेल्पलाइन",
        "about_heading": "🏢 कंपनी का परिचय एवं इंजीनियरिंग विशेषज्ञता",
        "about_body": """**इंजी. सत्यम पीयूष — एक ई.पी.सी. कंपनी** भारत भर में नगरपालिकाओं, स्मार्ट शहरों और ग्रामीण निकायों के लिए पूर्ण इंजीनियरिंग, खरीद और निर्माण (EPC) समाधान प्रदान करती है।

##### 🌟 प्रमुख नेतृत्व अनुभव एवं विशेषज्ञता:
- ✈️ **फ्लाइट टेस्टिंग इंस्ट्रुमेंटेशन** — **हिंदुस्तान एयरोनॉटिक्स लिमिटेड (HAL India)** में उच्च-सटीक एयरोस्पेस सिस्टम और परीक्षण का अनुभव।
- 📈 **एडवरटाइजिंग मैनेजर** — **अमेज़न इंडिया (AMAZON India)** में बड़े पैमाने पर संचालन और डिजिटल प्रबंधन का अनुभव।
- 🏗️ **नगरपालिका वाहन विनिर्माण** — हाइड्रोलिक रिफ्यूज कॉम्पेक्टर, रोड स्वीपर, ठोस कचरा प्रबंधन डस्टबिन और मोबाइल बायो-शौचालय का निर्माण।""",
        "filter_vertical": "श्रेणी के अनुसार चुनें:",
        "filter_op": "संचालन प्रणाली (Operation Mode):",
        "filter_mat": "निर्माण सामग्री (Material):",
        "search_placeholder": "मशीन का नाम, क्षमता या सामग्री खोजें...",
        "all": "सभी",
        "reg_office": "पंजीकृत कार्यालय",
        "fab_base": "विनिर्माण एवं कार्यशाला इकाई",
        "phone": "दूरभाष / हेल्पलाइन",
        "email": "ईमेल",
        "open_gmaps": "🗺️ गूगल मैप्स में देखें"
    }
}

# ---------------------------------------------------------
# Top Navigation Bar with 2 Switches on Top Right Corner
# ---------------------------------------------------------
top_col_brand, top_col_theme, top_col_lang = st.columns([0.54, 0.23, 0.23])

with top_col_theme:
    is_dark = st.toggle(
        "🌙 Dark Mode",
        value=st.session_state.get("dark_mode", False),
        key="dark_mode",
        help="Toggle between Warm Light and Obsidian Dark theme"
    )

with top_col_lang:
    is_hindi = st.toggle(
        "🇮🇳 हिन्दी (Hindi)",
        value=st.session_state.get("is_hindi", False),
        key="is_hindi",
        help="Toggle portal language between English and हिन्दी"
    )
    lang = "hi" if is_hindi else "en"

with top_col_brand:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:8px; padding-top:6px;">
        <span style="font-weight:800; font-size:0.92rem; letter-spacing:0.04em; color:{'#ffffff' if is_dark else '#0f172a'};">SP & E.P.C. PORTAL</span>
        <span style="font-size:0.78rem; font-weight:700; color:{'#38bdf8' if is_dark else '#c2410c'};">● Live Digital Suite</span>
    </div>
    """, unsafe_allow_html=True)

t = I18N[lang]

# ---------------------------------------------------------
# Dynamic CSS Injection (Light vs Dark)
# ---------------------------------------------------------
if not is_dark:
    # Warm Editorial Light Theme CSS — Ultra High Human-Eye Contrast
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;1,6..72,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        :root, html, body, .stApp {
            color-scheme: light !important;
            --text-color: #0f172a !important;
            --primary-color: #c2410c !important;
            --background-color: #f8f6f0 !important;
            --secondary-background-color: #ede8df !important;
        }

        header[data-testid="stHeader"] {
            background-color: #f8f6f0 !important;
            border-bottom: 1.5px solid #dcd5c9 !important;
        }
        .stApp, html, body {
            font-family: 'Plus Jakarta Sans', 'Noto Sans Devanagari', sans-serif !important;
            background-color: #f8f6f0 !important;
            color: #0f172a !important;
            overflow-x: hidden !important;
        }
        [data-testid="stSidebar"], [data-testid="stSidebarContent"], [data-testid="stSidebarNav"] {
            background-color: #ede8df !important;
            border-right: 1.5px solid #dcd5c9 !important;
        }
        [data-testid="stSidebar"] * {
            color: #0f172a !important;
        }
        h1, h2, h3, .serif-heading {
            font-family: 'Newsreader', Georgia, 'Noto Sans Devanagari', serif !important;
            color: #0f172a !important;
            font-weight: 700 !important;
            letter-spacing: -0.015em !important;
        }
        h4, h5, h6 {
            font-family: 'Plus Jakarta Sans', 'Noto Sans Devanagari', sans-serif !important;
            color: #0f172a !important;
            font-weight: 700 !important;
        }
        p, span, div, li, label {
            color: #0f172a !important;
        }
        /* High Contrast Captions & Subtitles */
        [data-testid="stCaptionContainer"], .stCaption, small {
            color: #334155 !important;
            font-size: 0.88rem !important;
            font-weight: 600 !important;
            line-height: 1.5 !important;
        }
        hr {
            border-color: #dcd5c9 !important;
        }

        /* Expander Styling */
        [data-testid="stExpander"], details {
            background-color: #ffffff !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 12px !important;
            margin-bottom: 12px !important;
            box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04) !important;
        }
        [data-testid="stExpander"] summary {
            background-color: #ffffff !important;
            color: #0f172a !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            padding: 12px 16px !important;
        }
        [data-testid="stExpander"] summary p, [data-testid="stExpander"] summary span {
            color: #0f172a !important;
            font-weight: 700 !important;
            font-size: 0.98rem !important;
        }
        [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
            background-color: #ffffff !important;
            color: #0f172a !important;
            padding: 14px 16px !important;
            border-top: 1.5px solid #e2e8f0 !important;
        }

        /* 100% BULLETPROOF LIGHT MODE TABS (SOLID HIGH-CONTRAST PILLS WITH GENEROUS SPACING) */
        .stTabs, [data-testid="stTabs"], .stTabs > div, [data-testid="stTabs"] > div {
            background-color: transparent !important;
            margin-top: 8px !important;
            margin-bottom: 20px !important;
        }
        .stTabs [data-baseweb="tab-list"],
        [data-testid="stTabs"] [data-baseweb="tab-list"],
        div[role="tablist"] {
            background-color: #e2e8f0 !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 12px !important;
            padding: 8px 10px !important;
            gap: 16px !important;
            display: flex !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.08) !important;
        }
        /* Hide Default Tab Line Highlight */
        [data-baseweb="tab-highlight"],
        [data-baseweb="tab-border"] {
            display: none !important;
            height: 0px !important;
        }
        /* Unselected Tab Button with spacious margins */
        [data-testid="stTabs"] button[role="tab"],
        .stTabs button[role="tab"],
        button[data-baseweb="tab"],
        button[role="tab"] {
            background-color: #ffffff !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 8px !important;
            padding: 10px 20px !important;
            margin-right: 12px !important;
            white-space: nowrap !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
            opacity: 1 !important;
            transition: all 0.15s ease-in-out !important;
        }
        /* Unselected Tab Text */
        [data-testid="stTabs"] button[role="tab"] *,
        .stTabs button[role="tab"] *,
        button[data-baseweb="tab"] *,
        button[data-baseweb="tab"] p,
        button[data-baseweb="tab"] span,
        [data-baseweb="tab"] [data-testid="stMarkdownContainer"] p {
            color: #0f172a !important; /* Pitch Jet-Black */
            -webkit-text-fill-color: #0f172a !important;
            font-size: 0.94rem !important;
            font-weight: 700 !important;
            white-space: nowrap !important;
            letter-spacing: 0.01em !important;
            opacity: 1 !important;
            visibility: visible !important;
        }
        /* Hover Tab */
        [data-testid="stTabs"] button[role="tab"]:hover,
        button[data-baseweb="tab"]:hover {
            background-color: #fff7ed !important;
            border-color: #ea580c !important;
        }
        [data-testid="stTabs"] button[role="tab"]:hover *,
        button[data-baseweb="tab"]:hover * {
            color: #ea580c !important;
            -webkit-text-fill-color: #ea580c !important;
        }
        /* Active Selected Tab */
        [data-testid="stTabs"] button[aria-selected="true"],
        .stTabs button[aria-selected="true"],
        button[data-baseweb="tab"][aria-selected="true"],
        button[role="tab"][aria-selected="true"] {
            background-color: #c2410c !important; /* Rich Terracotta Orange */
            border: 1.5px solid #9a3412 !important;
            border-radius: 8px !important;
            box-shadow: 0 3px 10px rgba(194, 65, 12, 0.4) !important;
            opacity: 1 !important;
        }
        [data-testid="stTabs"] button[aria-selected="true"] *,
        .stTabs button[aria-selected="true"] *,
        button[data-baseweb="tab"][aria-selected="true"] *,
        button[data-baseweb="tab"][aria-selected="true"] p,
        button[data-baseweb="tab"][aria-selected="true"] span {
            color: #ffffff !important; /* Pure White */
            -webkit-text-fill-color: #ffffff !important;
            font-weight: 800 !important;
            opacity: 1 !important;
        }

        /* Form Inputs & Selectboxes & Radios */
        [data-testid="stSelectbox"] label, [data-testid="stTextInput"] label, [data-testid="stRadio"] label, [data-testid="stRadio"] p {
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
            font-weight: 700 !important;
            font-size: 0.92rem !important;
        }
        [data-baseweb="select"] > div {
            background-color: #ffffff !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 8px !important;
            color: #0f172a !important;
        }
        [data-baseweb="select"] * {
            color: #0f172a !important;
            font-weight: 600 !important;
        }
        [data-testid="stTextInput"] input {
            background-color: #ffffff !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 8px !important;
            color: #0f172a !important;
            font-weight: 600 !important;
        }
        div[data-testid="stToggle"] label p, div[data-testid="stToggle"] label span {
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
            font-weight: 700 !important;
        }

        /* Code snippets */
        code {
            font-family: 'JetBrains Mono', monospace !important;
            background-color: #e2e8f0 !important;
            color: #0f172a !important;
            padding: 3px 7px !important;
            border-radius: 5px !important;
            border: 1px solid #cbd5e1 !important;
            font-weight: 600 !important;
            font-size: 0.86rem !important;
        }
        .editorial-header-box {
            background-color: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-radius: 16px;
            padding: clamp(16px, 3vw, 26px);
            margin-bottom: 18px;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
        }
        .editorial-hero-title {
            font-family: 'Newsreader', Georgia, serif;
            font-size: clamp(1.4rem, 4vw, 2.2rem);
            font-weight: 700;
            color: #0f172a;
            line-height: 1.22;
            margin-bottom: 6px;
        }
        .editorial-hero-sub {
            color: #334155;
            font-size: clamp(0.85rem, 2vw, 0.98rem);
            line-height: 1.5;
            font-weight: 600;
        }
        .notion-card {
            background-color: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 2px 5px rgba(15, 23, 42, 0.03);
            height: 100%;
        }
        .card-label-warm {
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            color: #c2410c;
            margin-bottom: 4px;
        }
        .card-val-warm {
            font-family: 'Newsreader', Georgia, serif;
            font-size: clamp(1.25rem, 3vw, 1.5rem);
            font-weight: 700;
            color: #0f172a;
            line-height: 1.25;
        }
        .card-sub-warm {
            font-size: 0.84rem;
            font-weight: 600;
            color: #334155;
            margin-top: 4px;
        }
        .badge-warm {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 5px 10px;
            border-radius: 7px;
            font-size: 0.75rem;
            font-weight: 700;
            margin-right: 4px;
            margin-bottom: 4px;
        }
        .badge-terracotta { background: #fee2e2; border: 1.5px solid #fca5a5; color: #991b1b; }
        .badge-sage { background: #dcfce7; border: 1.5px solid #86efac; color: #166534; }
        .badge-slate { background: #dbeafe; border: 1.5px solid #93c5fd; color: #1e40af; }
        .context-product-card {
            background: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 16px;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
        }
        .item-title-serif {
            font-family: 'Newsreader', Georgia, serif;
            font-size: 1.2rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 3px;
        }
        .item-type-sub {
            font-size: 0.85rem;
            color: #c2410c;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .search-hit-box {
            background: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-left: 4px solid #c2410c;
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 2px 5px rgba(15, 23, 42, 0.03);
        }
    </style>
    """, unsafe_allow_html=True)
else:
    # Obsidian Cyber Dark Theme CSS
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        :root, html, body, .stApp {
            color-scheme: dark !important;
            --text-color: #f8fafc !important;
            --primary-color: #38bdf8 !important;
            --background-color: #0b0f19 !important;
            --secondary-background-color: #0f172a !important;
        }

        header[data-testid="stHeader"] {
            background-color: #0b0f19 !important;
            border-bottom: 1.5px solid #1e293b !important;
        }
        .stApp, html, body {
            font-family: 'Plus Jakarta Sans', 'Noto Sans Devanagari', sans-serif !important;
            background-color: #0b0f19 !important;
            color: #f8fafc !important;
            overflow-x: hidden !important;
        }
        [data-testid="stSidebar"], [data-testid="stSidebarContent"], [data-testid="stSidebarNav"] {
            background-color: #0f172a !important;
            border-right: 1.5px solid #1e293b !important;
        }
        [data-testid="stSidebar"] * {
            color: #f8fafc !important;
        }
        h1, h2, h3, .serif-heading {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            letter-spacing: -0.02em !important;
        }
        h4, h5, h6 {
            color: #38bdf8 !important;
            font-weight: 700 !important;
        }
        p, span, div, li, label {
            color: #f8fafc !important;
        }
        [data-testid="stCaptionContainer"], .stCaption, small {
            color: #94a3b8 !important;
            font-size: 0.88rem !important;
            font-weight: 500 !important;
            line-height: 1.5 !important;
        }
        hr {
            border-color: #1e293b !important;
        }

        /* Expander Styling */
        [data-testid="stExpander"], details {
            background-color: #131b2e !important;
            border: 1.5px solid #1e293b !important;
            border-radius: 12px !important;
            margin-bottom: 12px !important;
        }
        [data-testid="stExpander"] summary {
            background-color: #131b2e !important;
            color: #f8fafc !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            padding: 12px 16px !important;
        }
        [data-testid="stExpander"] summary p, [data-testid="stExpander"] summary span {
            color: #f8fafc !important;
            font-weight: 700 !important;
            font-size: 0.98rem !important;
        }
        [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
            background-color: #131b2e !important;
            color: #e2e8f0 !important;
            padding: 14px 16px !important;
            border-top: 1.5px solid #1e293b !important;
        }

        /* 100% BULLETPROOF DARK MODE TABS (SOLID HIGH-CONTRAST PILLS WITH GENEROUS SPACING) */
        .stTabs, [data-testid="stTabs"], .stTabs > div, [data-testid="stTabs"] > div {
            background-color: transparent !important;
            margin-top: 8px !important;
            margin-bottom: 20px !important;
        }
        .stTabs [data-baseweb="tab-list"],
        [data-testid="stTabs"] [data-baseweb="tab-list"],
        div[role="tablist"] {
            background-color: #0f172a !important;
            border: 1.5px solid #1e293b !important;
            border-radius: 12px !important;
            padding: 8px 10px !important;
            gap: 16px !important;
            display: flex !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.3) !important;
        }
        /* Hide Default Tab Line Highlight */
        [data-baseweb="tab-highlight"],
        [data-baseweb="tab-border"] {
            display: none !important;
            height: 0px !important;
        }
        /* Unselected Tab Button with spacious margins */
        [data-testid="stTabs"] button[role="tab"],
        .stTabs button[role="tab"],
        button[data-baseweb="tab"],
        button[role="tab"] {
            background-color: #1e293b !important;
            border: 1.5px solid #334155 !important;
            border-radius: 8px !important;
            padding: 10px 20px !important;
            margin-right: 12px !important;
            white-space: nowrap !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
            opacity: 1 !important;
            transition: all 0.15s ease-in-out !important;
        }
        /* Unselected Tab Text */
        [data-testid="stTabs"] button[role="tab"] *,
        .stTabs button[role="tab"] *,
        button[data-baseweb="tab"] *,
        button[data-baseweb="tab"] p,
        button[data-baseweb="tab"] span,
        [data-baseweb="tab"] [data-testid="stMarkdownContainer"] p {
            color: #f8fafc !important; /* Crisp Pure White */
            -webkit-text-fill-color: #f8fafc !important;
            font-size: 0.94rem !important;
            font-weight: 700 !important;
            white-space: nowrap !important;
            letter-spacing: 0.01em !important;
            opacity: 1 !important;
            visibility: visible !important;
        }
        /* Hover Tab */
        [data-testid="stTabs"] button[role="tab"]:hover,
        button[data-baseweb="tab"]:hover {
            background-color: #334155 !important;
            border-color: #38bdf8 !important;
        }
        [data-testid="stTabs"] button[role="tab"]:hover *,
        button[data-baseweb="tab"]:hover * {
            color: #38bdf8 !important;
            -webkit-text-fill-color: #38bdf8 !important;
        }
        /* Active Selected Tab */
        [data-testid="stTabs"] button[aria-selected="true"],
        .stTabs button[aria-selected="true"],
        button[data-baseweb="tab"][aria-selected="true"],
        button[role="tab"][aria-selected="true"] {
            background-color: #0284c7 !important; /* Vibrant Ocean Blue */
            border: 1.5px solid #38bdf8 !important;
            border-radius: 8px !important;
            box-shadow: 0 3px 12px rgba(56, 189, 248, 0.45) !important;
            opacity: 1 !important;
        }
        [data-testid="stTabs"] button[aria-selected="true"] *,
        .stTabs button[aria-selected="true"] *,
        button[data-baseweb="tab"][aria-selected="true"] *,
        button[data-baseweb="tab"][aria-selected="true"] p,
        button[data-baseweb="tab"][aria-selected="true"] span {
            color: #ffffff !important; /* Crisp White */
            -webkit-text-fill-color: #ffffff !important;
            font-weight: 800 !important;
            opacity: 1 !important;
        }

        /* Form Inputs & Radios */
        [data-testid="stSelectbox"] label, [data-testid="stTextInput"] label, [data-testid="stRadio"] label, [data-testid="stRadio"] p, [data-testid="stRadio"] span {
            color: #f8fafc !important;
            -webkit-text-fill-color: #f8fafc !important;
            font-weight: 700 !important;
            font-size: 0.92rem !important;
        }
        [data-baseweb="select"] > div {
            background-color: #131b2e !important;
            border: 1.5px solid #334155 !important;
            border-radius: 8px !important;
            color: #f8fafc !important;
        }
        [data-baseweb="select"] * {
            color: #f8fafc !important;
            font-weight: 600 !important;
        }
        [data-testid="stTextInput"] input {
            background-color: #131b2e !important;
            border: 1.5px solid #334155 !important;
            border-radius: 8px !important;
            color: #f8fafc !important;
            font-weight: 600 !important;
        }
        div[data-testid="stToggle"] label p, div[data-testid="stToggle"] label span {
            color: #f8fafc !important;
            -webkit-text-fill-color: #f8fafc !important;
            font-weight: 700 !important;
        }

        code {
            font-family: 'JetBrains Mono', monospace !important;
            background-color: #1e293b !important;
            color: #38bdf8 !important;
            padding: 3px 7px !important;
            border-radius: 5px !important;
            border: 1px solid #334155 !important;
            font-weight: 600 !important;
            font-size: 0.86rem !important;
        }
        .editorial-header-box {
            background: linear-gradient(135deg, #0f172a 0%, #131b2e 100%);
            border: 1.5px solid #1e293b;
            border-radius: 16px;
            padding: clamp(16px, 3vw, 26px);
            margin-bottom: 18px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        .editorial-hero-title {
            font-size: clamp(1.4rem, 4vw, 2.2rem);
            font-weight: 800;
            color: #ffffff;
            line-height: 1.22;
            margin-bottom: 6px;
        }
        .editorial-hero-sub {
            color: #94a3b8;
            font-size: clamp(0.85rem, 2vw, 0.98rem);
            line-height: 1.5;
            font-weight: 500;
        }
        .notion-card {
            background-color: #131b2e;
            border: 1.5px solid #1e293b;
            border-radius: 12px;
            padding: 16px;
            height: 100%;
        }
        .card-label-warm {
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            color: #38bdf8;
            margin-bottom: 4px;
        }
        .card-val-warm {
            font-size: clamp(1.25rem, 3vw, 1.5rem);
            font-weight: 800;
            color: #ffffff;
            line-height: 1.25;
        }
        .card-sub-warm {
            font-size: 0.84rem;
            color: #94a3b8;
            margin-top: 4px;
        }
        .badge-warm {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 5px 10px;
            border-radius: 7px;
            font-size: 0.75rem;
            font-weight: 700;
            margin-right: 4px;
            margin-bottom: 4px;
        }
        .badge-terracotta { background: rgba(56, 189, 248, 0.15); border: 1.5px solid #0284c7; color: #38bdf8; }
        .badge-sage { background: rgba(52, 211, 153, 0.15); border: 1.5px solid #059669; color: #34d399; }
        .badge-slate { background: rgba(168, 85, 247, 0.15); border: 1.5px solid #7c3aed; color: #c084fc; }
        .context-product-card {
            background: #131b2e;
            border: 1.5px solid #1e293b;
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 16px;
        }
        .item-title-serif {
            font-size: 1.2rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 3px;
        }
        .item-type-sub {
            font-size: 0.85rem;
            color: #38bdf8;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .search-hit-box {
            background: #131b2e;
            border: 1.5px solid #1e293b;
            border-left: 4px solid #38bdf8;
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 12px;
        }
    </style>
    """, unsafe_allow_html=True)





# ---------------------------------------------------------
# Ensure Contextual Images are Available
# ---------------------------------------------------------
ITEMS_DIR = "extracted_pages/items"
PAGES_DIR = "extracted_pages"
os.makedirs(ITEMS_DIR, exist_ok=True)

def crop_and_save(page_num, box, filename):
    p_path = f"{PAGES_DIR}/page_{page_num}.png"
    out_path = f"{ITEMS_DIR}/{filename}"
    if os.path.exists(p_path) and not os.path.exists(out_path):
        try:
            im = Image.open(p_path)
            im.crop(box).save(out_path)
        except Exception:
            pass

def ensure_all_crops():
    crop_and_save(2, (150, 100, 1040, 700), 'selfie_point.png')
    crop_and_save(2, (120, 720, 650, 1400), 'mural_art.png')
    crop_and_save(2, (650, 720, 1080, 1400), 'scrap_sculpture.png')
    crop_and_save(3, (160, 110, 630, 370), 'wheel_paddle_bins.png')
    crop_and_save(3, (680, 110, 1120, 370), 'waste_container_bucket.png')
    crop_and_save(3, (160, 380, 630, 640), 'ss_household_bin.png')
    crop_and_save(3, (680, 380, 1120, 640), 'ss_roadside_hanging.png')
    crop_and_save(3, (160, 650, 630, 910), 'plastic_roadside_hanging.png')
    crop_and_save(3, (680, 650, 1120, 910), 'wheel_barrows.png')
    crop_and_save(3, (160, 920, 630, 1190), 'plastic_waste_container.png')
    crop_and_save(3, (680, 920, 1120, 1190), 'ms_waste_container.png')
    crop_and_save(3, (160, 1200, 630, 1470), 'heavy_garbage_container.png')
    crop_and_save(3, (680, 1200, 1120, 1470), 'garbage_rickshaw.png')
    crop_and_save(4, (160, 110, 630, 370), 'segregation_cart.png')
    crop_and_save(4, (680, 110, 1120, 370), 'outdoor_fountain.png')
    crop_and_save(4, (160, 380, 630, 640), 'compost_machine.png')
    crop_and_save(4, (680, 380, 1120, 640), 'shredder_machine.png')
    crop_and_save(4, (160, 650, 630, 910), 'hand_fogging.png')
    crop_and_save(4, (680, 650, 1120, 910), 'vehicle_fogging.png')
    crop_and_save(4, (160, 920, 630, 1190), 'frp_urinal.png')
    crop_and_save(4, (680, 920, 1120, 1190), 'portable_toilet.png')
    crop_and_save(4, (160, 1200, 630, 1470), 'mobile_toilet.png')
    crop_and_save(4, (680, 1200, 1120, 1470), 'modular_toilet.png')
    crop_and_save(5, (160, 110, 610, 390), 'open_box_tipper.png')
    crop_and_save(5, (680, 420, 1120, 690), 'box_body_tipper.png')
    crop_and_save(5, (160, 660, 610, 930), 'sky_lifter.png')
    crop_and_save(5, (680, 920, 1120, 1190), 'recovery_vehicle.png')
    crop_and_save(5, (160, 1190, 610, 1470), 'mini_suction.png')
    crop_and_save(6, (160, 110, 610, 390), 'self_propelled_sweeper.png')
    crop_and_save(6, (680, 420, 1120, 690), 'refuse_compactor.png')
    crop_and_save(6, (160, 660, 610, 930), 'truck_road_sweeper.png')
    crop_and_save(6, (680, 920, 1120, 1190), 'cattle_catcher.png')
    crop_and_save(6, (160, 1190, 610, 1470), 'truck_jetting_machine.png')
    crop_and_save(7, (160, 110, 500, 390), 'water_tank.png')
    crop_and_save(7, (510, 110, 830, 390), 'tractor_trolley.png')
    crop_and_save(7, (840, 110, 1150, 390), 'ecart_garbage.png')
    crop_and_save(7, (160, 410, 500, 710), 'diesel_generator.png')
    crop_and_save(7, (510, 410, 830, 710), 'high_mast_light.png')
    crop_and_save(7, (840, 410, 1150, 710), 'high_mast_flag.png')
    crop_and_save(7, (160, 730, 500, 990), 'overhead_signboard.png')
    crop_and_save(7, (510, 730, 830, 990), 'road_signage.png')
    crop_and_save(7, (840, 730, 1150, 990), 'road_barricade.png')
    crop_and_save(7, (160, 1010, 640, 1470), 'safety_equipment.png')
    crop_and_save(7, (650, 1010, 1150, 1470), 'chemicals.png')
    crop_and_save(8, (120, 630, 1100, 760), 'cert_badges.png')

ensure_all_crops()


# ---------------------------------------------------------
# Comprehensive Multi-Criteria Data Store
# ---------------------------------------------------------
PDF_ALL_PAGES_DATA = [
    {
        "page_number": 1,
        "page_title": "Cover & Leadership Credentials",
        "category": "Corporate Overview",
        "image_file": os.path.join(PAGES_DIR, "page_1.png"),
        "content_summary": "Company Branding, Swachh Bharat Abhiyan, HAL & Amazon credentials, Clean Green India.",
        "details": {
            "Company Name": "Er. SATYAM PIYUSH — An E.P.C. company",
            "Branding & Logos": "SP Official Logo, Swachh Bharat Abhiyan, Clean Green INDIA",
            "Past Leadership Experience": [
                "i) Flight Testing Instrumentation in HAL India (Hindustan Aeronautics Limited)",
                "ii) Advertising Manager in AMAZON India"
            ],
            "Mission Themes": "Clean Green India, Swachh Bharat Abhiyan, Municipal Infrastructure Transformation"
        }
    },
    {
        "page_number": 2,
        "page_title": "Urban Beautification & Public Art",
        "category": "Art & Civic Upliftment",
        "image_file": os.path.join(PAGES_DIR, "page_2.png"),
        "content_summary": "Selfie points, 3D mural wall art, scrap sculpture landmark installations.",
        "items": [
            {
                "name": "Selfie Point",
                "name_hi": "3D सेल्फी पॉइंट (आई लव सिटी)",
                "type": "Public Landmark Installation (e.g., 'I ❤️ TAJPUR')",
                "operation": "Static / Architectural",
                "material": "Acrylic / Metal",
                "thumb": os.path.join(ITEMS_DIR, "selfie_point.png"),
                "specs": {"Application": "Civic Tourism & City Entry Landmark", "Lighting": "LED Backlit Lettering", "Finish": "Weatherproof Exterior Coating"}
            },
            {
                "name": "3D Mural Wall Art",
                "name_hi": "3D वॉल पेंटिंग एवं पर्यावरण म्यूरल",
                "type": "Civic Awareness & Public Wall Painting",
                "operation": "Static / Art",
                "material": "Weatherproof Pigment",
                "thumb": os.path.join(ITEMS_DIR, "mural_art.png"),
                "specs": {"Theme": "Clean India, Wildlife & Nature Conservation", "Durability": "UV Resistant All-Weather Pigments"}
            },
            {
                "name": "Scrap Sculpture",
                "name_hi": "स्क्रैप मेटल कलाकृतियां",
                "type": "Waste-to-Art Public Installations",
                "operation": "Static / Art",
                "material": "Recycled Metal Scrap",
                "thumb": os.path.join(ITEMS_DIR, "scrap_sculpture.png"),
                "specs": {"Material": "100% Repurposed Metal Scrap & Auto Parts", "Subject": "Roosters & Wildlife Sculptures", "Finish": "Anti-Rust Protective Coating"}
            }
        ]
    },
    {
        "page_number": 3,
        "page_title": "Waste Management — Bins & Containers",
        "category": "Waste Containment",
        "image_file": os.path.join(PAGES_DIR, "page_3.png"),
        "content_summary": "10 specific bin types: pedal bins, SS household/roadside bins, containers, wheel barrows, rickshaws.",
        "items": [
            {"name": "All Type of Wheel & Foot Paddle Dustbin", "name_hi": "पहिएदार एवं पैडल डस्टबिन (सभी प्रकार)", "type": "Pedal-Operated Wheeled Bins", "operation": "Manual / Pedal", "material": "HDPE Polymer", "thumb": os.path.join(ITEMS_DIR, "wheel_paddle_bins.png"), "specs": {"Colors": "Green, Black, Blue, Red, Yellow", "Variant": "Foot Paddle & Heavy Wheels"}},
            {"name": "Waste Container (10-12) Ltr", "name_hi": "घरेलू कचरा बाल्टी (10-12 लीटर)", "type": "Household Waste Bucket", "operation": "Manual", "material": "HDPE Polymer", "thumb": os.path.join(ITEMS_DIR, "waste_container_bucket.png"), "specs": {"Capacity": "10-12 Litres", "Variants": "Green & Blue with reinforced handle"}},
            {"name": "SS House Hold Dustbin", "name_hi": "स्टेनलेस स्टील (SS) इनडोर डस्टबिन", "type": "Stainless Steel Indoor Bins", "operation": "Manual / Pedal", "material": "Stainless Steel", "thumb": os.path.join(ITEMS_DIR, "ss_household_bin.png"), "specs": {"Material": "High Grade Stainless Steel", "Models": "Open top, foot pedal, swing lid"}},
            {"name": "SS Roadside Hanging Dustbin", "name_hi": "सड़क किनारे SS हैंगिंग डस्टबिन", "type": "Public Pole Mounted Dustbin", "operation": "Manual Swivel", "material": "Stainless Steel", "thumb": os.path.join(ITEMS_DIR, "ss_roadside_hanging.png"), "specs": {"Structure": "Stainless Steel Twin & Triple Post Mounted", "Tilt": "Swivel Emptying"}},
            {"name": "Plastic Roadside Hanging Dustbin", "name_hi": "प्लास्टिक हैंगिंग ट्विन डस्टबिन", "type": "Segregated Public Dual Bins", "operation": "Manual", "material": "HDPE Polymer", "thumb": os.path.join(ITEMS_DIR, "plastic_roadside_hanging.png"), "specs": {"Color Coding": "Dual Green (Wet) & Blue (Dry)", "Mount": "Heavy Steel Ground Anchor Pole"}},
            {"name": "Wheel Barrows", "name_hi": "मैन्युअल कचरा ट्राली (व्हील बारो)", "type": "Manual Waste Transfer Trolley", "operation": "Manual", "material": "Mild Steel", "thumb": os.path.join(ITEMS_DIR, "wheel_barrows.png"), "specs": {"Body": "Deep Pressed Mild Steel", "Wheels": "Heavy-Duty Solid Rubber / Pneumatic"}},
            {"name": "Plastic Waste Container", "name_hi": "4-पहिएदार प्लास्टिक कंटेनर", "type": "4-Wheeled Community Bulk Bin", "operation": "Manual / Tipper Compatible", "material": "HDPE Polymer", "thumb": os.path.join(ITEMS_DIR, "plastic_waste_container.png"), "specs": {"Material": "UV-Stabilized High-Density Polymer", "Castors": "4 Heavy Swivel Wheels"}},
            {"name": "MS Waste Container", "name_hi": "4-पहिएदार माइल्ड स्टील (MS) कंटेनर", "type": "4-Wheeled Mild Steel Bin", "operation": "Hydraulic Tipper Arm Lifting", "material": "Mild Steel", "thumb": os.path.join(ITEMS_DIR, "ms_waste_container.png"), "specs": {"Material": "Heavy Gauge Mild Steel", "Compatibility": "Direct Tipper Arm Lifting"}},
            {"name": "Heavy Waste Garbage Container", "name_hi": "भारी कचरा संग्रहण कंटेनर", "type": "Static Large Volume Bulk Dump Container", "operation": "Static", "material": "Mild Steel", "thumb": os.path.join(ITEMS_DIR, "heavy_garbage_container.png"), "specs": {"Material": "Welded Structural Steel Sheet", "Lids": "Dual Top Flap Lids"}},
            {"name": "Garbage Tricycle or Rickshaw", "name_hi": "कचरा ढोने वाला तिपहिया रिक्शा", "type": "Manual Door-to-Door Collection", "operation": "Manual Pedal", "material": "Mild Steel", "thumb": os.path.join(ITEMS_DIR, "garbage_rickshaw.png"), "specs": {"Chassis": "Reinforced Pedal Cycle Chassis", "Storage": "Dual Partitioned Green & Blue Box"}}
        ]
    },
    {
        "page_number": 4,
        "page_title": "Waste Processing, Compost & Public Sanitation",
        "category": "Processing & Sanitation",
        "image_file": os.path.join(PAGES_DIR, "page_4.png"),
        "content_summary": "Compost machines, shredders, foggers, portable FRP urinals, modular & mobile toilets.",
        "items": [
            {"name": "Segregation Cart", "name_hi": "कचरा पृथक्करण कार्ट (4 बिन)", "type": "Mobile Multi-Bin Sorting Cart", "operation": "Manual Wheeled", "material": "Steel & Polymer", "thumb": os.path.join(ITEMS_DIR, "segregation_cart.png"), "specs": {"Compartments": "4-Color Coded Bins (Blue, Red, Black, Green) on Wheeled Trolley"}},
            {"name": "Outdoor Fountain", "name_hi": "सजावटी आउटडोर फव्वारा", "type": "Civic Water Feature", "operation": "Electric Pump", "material": "FRP / Stone", "thumb": os.path.join(ITEMS_DIR, "outdoor_fountain.png"), "specs": {"Design": "Multi-Tiered Decorative Public Fountain"}},
            {"name": "Organic Waste Compost Machine", "name_hi": "जैविक कचरा खाद बनाने की मशीन (Composter)", "type": "Enclosed Aerobic Digester", "operation": "Automated Electric", "material": "Stainless Steel / MS", "thumb": os.path.join(ITEMS_DIR, "compost_machine.png"), "specs": {"Function": "Rapid decomposition of organic food waste into rich compost"}},
            {"name": "Shredder Machine", "name_hi": "औद्योगिक कचरा श्रेडर मशीन", "type": "Industrial Solid Waste Shredder", "operation": "Electric Motor Powered", "material": "Hardened Alloy Steel", "thumb": os.path.join(ITEMS_DIR, "shredder_machine.png"), "specs": {"Hopper": "Heavy Duty Infeed Chute with Hardened Shredding Blades"}},
            {"name": "Hand Fogging Machine", "name_hi": "हाथ से चलने वाली थर्मल फॉगिंग मशीन", "type": "Thermal Vector Control Fogger", "operation": "Thermal Pulse-Jet", "material": "Stainless Steel", "thumb": os.path.join(ITEMS_DIR, "hand_fogging.png"), "specs": {"Operation": "Portable Hand-Carried Thermal Pulse-Jet Fogger"}},
            {"name": "Vehicle Mounted Fogging Machine", "name_hi": "वाहन पर लगने वाली फॉगिंग मशीन", "type": "High-Capacity Ultra Vector Fogger", "operation": "Engine / Vehicle Powered", "material": "Heavy Alloy", "thumb": os.path.join(ITEMS_DIR, "vehicle_fogging.png"), "specs": {"Mount": "Truck Bed / Pickup Mounted Dual Fogging Barrels"}},
            {"name": "FRP Urinal", "name_hi": "एफआरपी (FRP) मूत्रालय पॉड", "type": "Single Pod Public Sanitation", "operation": "Static", "material": "FRP (Fiber Reinforced Polymer)", "thumb": os.path.join(ITEMS_DIR, "frp_urinal.png"), "specs": {"Material": "Fiber Reinforced Polymer (FRP)", "Features": "Corrosion Proof & Washable"}},
            {"name": "Portable / Potable Toilet", "name_hi": "पोर्टेबल शौचालय केबिन", "type": "Single Pod Restroom Cabin", "operation": "Static / Quick Deploy", "material": "FRP / HDPE", "thumb": os.path.join(ITEMS_DIR, "portable_toilet.png"), "specs": {"Fixtures": "Integrated Commode, Water Inlet & Odor Seal Trap"}},
            {"name": "Mobile Toilet (4,6,8,10 Seaters)", "name_hi": "मोबाइल टॉयलेट ट्रेलर (4/6/8/10 सीटर)", "type": "Towable Multi-Cabin Toilet Trailer", "operation": "Towable Trailer", "material": "Mild Steel Frame & FRP", "thumb": os.path.join(ITEMS_DIR, "mobile_toilet.png"), "specs": {"Seater Options": "4, 6, 8, 10 Individual Cabins", "Tanks": "Built-in Fresh Water & Sewage Tanks"}},
            {"name": "Modular Toilet", "name_hi": "मॉड्यूलर स्थायी शौचालय ब्लॉक", "type": "Prefab Permanent Community Sanitation Block", "operation": "Permanent Modular", "material": "Galvanized Steel & Prefab Panels", "thumb": os.path.join(ITEMS_DIR, "modular_toilet.png"), "specs": {"Frame": "Heavy Steel Column Frame with Overhead Water Tanks"}}
        ]
    },
    {
        "page_number": 5,
        "page_title": "Automotive — Commercial Vehicles & Tippers",
        "category": "Municipal Automotive",
        "image_file": os.path.join(PAGES_DIR, "page_5.png"),
        "content_summary": "Open Box Hopper Tipper, Box Body Tipper, Sky Lifter, Recovery Vehicle, Mini Suction Jetting.",
        "items": [
            {
                "name": "Open Box Hopper Tipper Dumper",
                "name_hi": "ओपन बॉक्स हॉपर टिपर डम्पर",
                "type": "Light Commercial Vehicle (LCV) Tipper",
                "operation": "Hydraulic / Engine & Battery",
                "material": "Mild Steel",
                "thumb": os.path.join(ITEMS_DIR, "open_box_tipper.png"),
                "specs": {
                    "Model": "Open Box Tipper",
                    "Vehicle Type": "Light Commercial Vehicle (LCV)",
                    "Tipping Angle": "45 Degree Clean Dump",
                    "Material of Construction": "Mild Steel",
                    "Hydraulic System": "Main Engine / Battery Operated"
                }
            },
            {
                "name": "Box Body Garbage Tipper",
                "name_hi": "बॉक्स बॉडी गारबेज टिपर (बंद वाहन)",
                "type": "LCV / MCV Enclosed Tipper",
                "operation": "Hydraulic / Engine & Battery",
                "material": "Mild Steel",
                "thumb": os.path.join(ITEMS_DIR, "box_body_tipper.png"),
                "specs": {
                    "Model": "Box Body Tipper",
                    "Vehicle Type": "LCV / MCV",
                    "Tipping Angle": "45 Degree High Dump",
                    "Material of Construction": "Mild Steel",
                    "Hydraulic System": "Main Engine / Battery Operated"
                }
            },
            {
                "name": "Sky Lifter",
                "name_hi": "स्काई लिफ्टर (स्ट्रीट लाइट रिपेयर वाहन)",
                "type": "Troubleshooting & Utility Tower",
                "operation": "Hydraulic Telescopic",
                "material": "Mild Steel",
                "thumb": os.path.join(ITEMS_DIR, "sky_lifter.png"),
                "specs": {
                    "Model": "Sky Lifter",
                    "Application": "Roadside Troubleshooting Management System",
                    "Vehicle Type": "Medium Commercial Vehicle (MCV)",
                    "Material of Construction": "Mild Steel",
                    "Stabilizer": "On Vehicle Chassis with Lifting Unit"
                }
            },
            {
                "name": "Recovery Vehicle",
                "name_hi": "टोइंग एवं रिकवरी वाहन",
                "type": "Towing & Vehicle Lifting Platform",
                "operation": "Hydraulic Crane / Chain",
                "material": "Mild Steel",
                "thumb": os.path.join(ITEMS_DIR, "recovery_vehicle.png"),
                "specs": {
                    "Model": "Recovery Vehicle",
                    "Application": "Vehicle Lifting for Recovery Platform",
                    "Tipping Hooks": "Lifting Chain with Carrying Platform",
                    "Material of Construction": "Mild Steel",
                    "Stabilizer": "Light and Medium Capacity Vehicle"
                }
            },
            {
                "name": "Mini Suction Cum Jetting Machine",
                "name_hi": "मिनी सक्शन सह जेटिंग मशीन",
                "type": "Municipal Drain & Jetting Unit",
                "operation": "High Pressure Hydraulic Pump",
                "material": "Mild Steel",
                "thumb": os.path.join(ITEMS_DIR, "mini_suction.png"),
                "specs": {
                    "Model": "Mini Suction Machine",
                    "Application": "For Municipal Waste Management System Unit",
                    "Tipping Hooks": "Complete Fabrication Unit",
                    "Material of Construction": "Mild Steel",
                    "Stabilizer": "Light and Medium Capacity Vehicle"
                }
            }
        ]
    },
    {
        "page_number": 6,
        "page_title": "Automotive — Compactors, Sweepers & Jetters",
        "category": "Municipal Automotive",
        "image_file": os.path.join(PAGES_DIR, "page_6.png"),
        "content_summary": "Self Propelled Sweeper, Refuse Compactor, Truck Mounted Sweeper, Cattle Catcher, Truck Jetter.",
        "items": [
            {
                "name": "Self Propelled Sweeping Machine",
                "name_hi": "सेल्फ प्रोपेल्ड रोड स्वीपिंग मशीन",
                "type": "Compact Street Sweeper",
                "operation": "Self Propelled Engine",
                "material": "Mild Steel",
                "thumb": os.path.join(ITEMS_DIR, "self_propelled_sweeper.png"),
                "specs": {
                    "Model": "Sweeping Machine",
                    "Application": "City Cleaning Management System Unit",
                    "Tipping Hooks": "Complete Fabrication Unit",
                    "Material of Construction": "Mild Steel",
                    "Stabilizers": "Self Propelled Manufacturing Unit"
                }
            },
            {
                "name": "Refuse Compactor",
                "name_hi": "रिफ्यूज कॉम्पेक्टर (कचरा दबाने वाला बड़ा वाहन)",
                "type": "Heavy Solid Waste Compactor",
                "operation": "Manual Hydraulic Control",
                "material": "Mild Steel",
                "thumb": os.path.join(ITEMS_DIR, "refuse_compactor.png"),
                "specs": {
                    "Model": "Refuse Compactor",
                    "Control System": "Manual Hydraulic Control",
                    "Lift Capacity": "1000 Kg. & Above",
                    "Lift Time": "18 Second",
                    "Warranty": "12 Months"
                }
            },
            {
                "name": "Truck Chassis Mounted Road Sweeper",
                "name_hi": "ट्रक माउंटेड रोड स्वीपर (6000 लीटर)",
                "type": "Heavy Highway & Street Sweeper",
                "operation": "Dedicated Diesel Auxiliary",
                "material": "Mild Steel",
                "thumb": os.path.join(ITEMS_DIR, "truck_road_sweeper.png"),
                "specs": {
                    "Model": "Road Sweeper",
                    "Application": "Use to Sweep the Road, Street etc.",
                    "Container Volume": "6000 Ltr.",
                    "Material of Construction": "Mild Steel",
                    "Auxiliary Engine": "Available (Diesel)"
                }
            },
            {
                "name": "Cattle Catcher Vehicle",
                "name_hi": "पशु बचाव एवं कैटल कैचर वाहन",
                "type": "Animal Rescue & Transit Vehicle",
                "operation": "Hydraulic & Chain System",
                "material": "Mild Steel",
                "thumb": os.path.join(ITEMS_DIR, "cattle_catcher.png"),
                "specs": {
                    "Model": "Cattle Catcher",
                    "Application": "Carrying Sick & Accidental Animals",
                    "Tipping Hooks": "Hydraulic & Chain System with Cattle Cabine",
                    "Material of Construction": "Mild Steel",
                    "Stabilizer": "Heavy Vehicle Chassis Platform"
                }
            },
            {
                "name": "Truck Mounted Suction or Jet Machine",
                "name_hi": "ट्रक माउंटेड सक्शन सह जेटिंग मशीन (10,000 लीटर)",
                "type": "Heavy Sludge Collection & Jetting Unit",
                "operation": "Heavy Duty PTO / Hydraulic",
                "material": "Mild Steel",
                "thumb": os.path.join(ITEMS_DIR, "truck_jetting_machine.png"),
                "specs": {
                    "Model": "Dump Tank Mounted on Truck",
                    "Application": "Truck Mounted Tank Unit for Collection of Sludge",
                    "Tank Capacity": "10,000 Ltr.",
                    "Material of Construction": "Mild Steel",
                    "Stabilizer": "Heavy Capacity Vehicle"
                }
            }
        ]
    },
    {
        "page_number": 7,
        "page_title": "Auxiliary Equipment, Infrastructure, Signage & Chemicals",
        "category": "Civil, Electrical & Safety",
        "image_file": os.path.join(PAGES_DIR, "page_7.png"),
        "content_summary": "Water tanks, tractor trolley, E-carts, generator, high mast lights, flags, signage, barricades, chemicals.",
        "items": [
            {"name": "MS/SS Water Tank", "name_hi": "पानी का टैंकर (MS / SS वाटर टैंक)", "type": "Towable Water Tanker", "operation": "Tractor Towed", "material": "Mild Steel / Stainless Steel", "thumb": os.path.join(ITEMS_DIR, "water_tank.png"), "specs": {"Material": "Mild Steel (MS) or Stainless Steel (SS)", "Towing": "Tractor Tow Hitch"}},
            {"name": "Hydraulic Tractor Trolley", "name_hi": "हाइड्रोलिक ट्रैक्टर ट्रॉली", "type": "Agricultural & Municipal Tipping Trolley", "operation": "Hydraulic Tipping", "material": "Mild Steel", "thumb": os.path.join(ITEMS_DIR, "tractor_trolley.png"), "specs": {"Tipping": "Hydraulic Ram Tipping Bed", "Body": "Reinforced Steel"}},
            {"name": "E-Cart for Garbage (Tipping & Non Tipping)", "name_hi": "ई-कार्ट कचरा वाहन (इलेक्ट्रिक बैटरी)", "type": "Electric Battery Waste Vehicle", "operation": "Electric Battery Powered", "material": "Mild Steel Chassis", "thumb": os.path.join(ITEMS_DIR, "ecart_garbage.png"), "specs": {"Drive": "Electric Battery Powered", "Variants": "Hydraulic Tipping & Static Body"}},
            {"name": "Silent Diesel Generator", "name_hi": "साइलेंट डीजल जनरेटर (DG Set)", "type": "Power Generation Unit", "operation": "Diesel Powered Engine", "material": "Acoustic Steel Enclosure", "thumb": os.path.join(ITEMS_DIR, "diesel_generator.png"), "specs": {"Enclosure": "Acoustic Weatherproof Silent Canopy", "Fuel": "Diesel"}},
            {"name": "Light on High Mast Pole", "name_hi": "हाई मास्ट लाइट पोल (चौराहा प्रकाश)", "type": "Plaza & Highway Illumination", "operation": "Electric / Motorized Winch", "material": "Galvanized Steel", "thumb": os.path.join(ITEMS_DIR, "high_mast_light.png"), "specs": {"Structure": "Multi-floodlight Circular Array on Polygonal Mast"}},
            {"name": "Flag on High Mast Pole", "name_hi": "हाई मास्ट राष्ट्रीय ध्वज पोल", "type": "National Flag Installation", "operation": "Motorized / Manual Winch", "material": "Galvanized Steel", "thumb": os.path.join(ITEMS_DIR, "high_mast_flag.png"), "specs": {"Structure": "Heavy-Duty High Mast Pole for Large National Flags"}},
            {"name": "Over Head Sign Board", "name_hi": "ओवरहेड हाईवे डायरेक्शन साइन बोर्ड", "type": "Highway Direction Signage", "operation": "Static Reflective", "material": "Galvanized Steel Truss", "thumb": os.path.join(ITEMS_DIR, "overhead_signboard.png"), "specs": {"Example Sign": "Patiala, Chandigarh, Shimla", "Reflectivity": "Retroreflective High Visibility"}},
            {"name": "Road Signage", "name_hi": "सड़क दिशा एवं सुरक्षा संकेतक", "type": "Municipal Direction & Caution Boards", "operation": "Static", "material": "Reflective Aluminum Sheeting", "thumb": os.path.join(ITEMS_DIR, "road_signage.png"), "specs": {"Application": "Official Municipal & Civic Guidance"}},
            {"name": "Road Barricade", "name_hi": "ट्रैफिक एवं सुरक्षा बैरिकेड", "type": "Traffic & Crowd Safety Barrier", "operation": "Modular Movable", "material": "Powder-Coated Steel", "thumb": os.path.join(ITEMS_DIR, "road_barricade.png"), "specs": {"Structure": "Steel Frame Barricade with SP Logo"}},
            {"name": "Safety Equipments", "name_hi": "सुरक्षा किट एवं PPE उपकरण", "type": "Sanitation Workforce PPE Kit", "operation": "Manual PPE", "material": "Rubber, Polymer & High-Vis Fabric", "thumb": os.path.join(ITEMS_DIR, "safety_equipment.png"), "specs": {"Components": "Helmets, Heavy Gloves, Goggles, Reflective Jackets, Boots, Caution Tape, Cones"}},
            {"name": "Chemicals", "name_hi": "कीट नियंत्रण एवं कीटाणुनाशक रसायन", "type": "Disinfection & Pest Control", "operation": "Chemical Spray", "material": "Disinfectants", "thumb": os.path.join(ITEMS_DIR, "chemicals.png"), "specs": {"Products": "Bleaching Powder, Sodium Hypochlorite, Malathion 50% E.C., Kingfog"}}
        ]
    },
    {
        "page_number": 8,
        "page_title": "Certifications, Accreditations & Contact Directory",
        "category": "Corporate & Contact Base",
        "image_file": os.path.join(PAGES_DIR, "page_8.png"),
        "content_summary": "World map network, ISO 9001:2015, NSIC, Make in India, Vocal for Local, Registered & Work addresses.",
        "details": {
            "Company Head": "Er. SATYAM PIYUSH",
            "Certifications & Badges": [
                "BE VOCAL ABOUT LOCAL",
                "ISO 9001:2015 CERTIFIED COMPANY",
                "NSIC (National Small Industries Corporation)",
                "MAKE IN INDIA",
                "SP Official Logo"
            ],
            "Registered Office": "Patel Nagar Jogbani, Araria, Bihar Pin- 854328",
            "Work / Fabrication Base": "C/o Ashok Kumar Pandey, Infront of DIET Forbesganj, Araria Pin- 854318 Bihar",
            "Direct Telephone": "+91 8539977611",
            "Official Email": "piyushsatyam04@gmail.com"
        }
    }
]


# ---------------------------------------------------------
# Dynamic Parsing & Rendering for Custom Uploads
# ---------------------------------------------------------
def extract_and_render_custom_pdf(uploaded_file):
    text_by_page = []
    rendered_images = []
    try:
        import pypdfium2 as pdfium
        uploaded_file.seek(0)
        pdf = pdfium.PdfDocument(uploaded_file.read())
        for i, page in enumerate(pdf):
            p_text = page.get_textpage().get_text_range()
            text_by_page.append({"page": i + 1, "text": p_text})
            img = page.render(scale=2.0).to_pil()
            rendered_images.append(img)
    except Exception:
        pass
    return text_by_page, rendered_images


def generate_editorial_qr(url_text, fill_color="#2d2b29", back_color="#ffffff"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(url_text)
    qr.make(fit=True)
    try:
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            fill_color=fill_color,
            back_color=back_color
        )
    except Exception:
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
    return img


# ---------------------------------------------------------
# Sidebar File Uploader
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📖 **Document Library**")
    
    doc_source = st.radio(
        "Document Source:" if lang == "en" else "दस्तावेज़ स्रोत:",
        ["SP & E.P.C. Company (Default)", "Upload Custom PDF File"],
        index=0
    )
    
    is_custom = False
    uploaded_file = None
    
    if doc_source == "Upload Custom PDF File":
        uploaded_file = st.file_uploader(
            "Upload any PDF file",
            type=["pdf"],
            help="Drop any PDF (Job Description, Spec Sheet, Report) to convert it to an interactive page."
        )
        if uploaded_file is not None:
            is_custom = True

    st.markdown("---")
    st.markdown("#### 🔖 **Status**")
    st.markdown(f"""
    <div style="background:{'#131b2e' if is_dark else '#ffffff'}; border:1px solid {'#1e293b' if is_dark else '#e8e3da'}; border-radius:8px; padding:12px; font-size:0.8rem; color:{'#94a3b8' if is_dark else '#5c5751'}; line-height:1.6;">
        <div>• <b>{'Source' if lang == 'en' else 'स्रोत'}:</b> SP & E.P.C. Company</div>
        <div>• <b>{'Items' if lang == 'en' else 'उत्पाद'}:</b> 38 Equipment Units</div>
        <div>• <b>{'Theme' if lang == 'en' else 'थीम'}:</b> {'🌙 Dark' if is_dark else '☀️ Light'}</div>
        <div>• <b>{'Language' if lang == 'en' else 'सक्रिय भाषा'}:</b> {'English' if lang == 'en' else 'हिन्दी (Hindi)'}</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# Parse Custom File if Uploaded
# ---------------------------------------------------------
custom_pages_data = []
custom_page_images = []

if is_custom and uploaded_file is not None:
    with st.spinner("Extracting text and rendering high-resolution visual pages..."):
        custom_pages_data, custom_page_images = extract_and_render_custom_pdf(uploaded_file)


# ---------------------------------------------------------
# Editorial Header
# ---------------------------------------------------------
st.markdown(f"""
<div class="editorial-header-box">
    <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:8px; align-items:center;">
        <span class="badge-warm badge-terracotta">{t['portal_badge']}</span>
        <span class="badge-warm badge-sage">{t['all_38']}</span>
        <span class="badge-warm badge-slate">{t['zero_dl']}</span>
    </div>
    <div class="editorial-hero-title">
        {t['title'] if not is_custom else uploaded_file.name.replace('.pdf', '').title()}
    </div>
    <div class="editorial-hero-sub">
        {t['tagline']} • ISO 9001:2015 • Make in India
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Navigation Tabs
# ---------------------------------------------------------
tab_summary, tab_catalog, tab_compare, tab_map, tab_pages, tab_search, tab_qr = st.tabs([
    t["tab_summary"],
    t["tab_catalog"],
    t["tab_compare"],
    t["tab_map"],
    t["tab_pages"],
    t["tab_search"],
    t["tab_qr"]
])


# =========================================================
# TAB 1: EXECUTIVE SUMMARY & PROFILE (FIRST TAB)
# =========================================================
with tab_summary:
    if not is_custom:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="notion-card">
                <div class="card-label-warm">{t['kpi_leadership']}</div>
                <div class="card-val-warm">HAL & Amazon</div>
                <div class="card-sub-warm">{t['kpi_leadership_sub']}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="notion-card">
                <div class="card-label-warm">{t['kpi_catalog']}</div>
                <div class="card-val-warm">{t['kpi_catalog_val']}</div>
                <div class="card-sub-warm">{t['kpi_catalog_sub']}</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="notion-card">
                <div class="card-label-warm">{t['kpi_standards']}</div>
                <div class="card-val-warm">ISO 9001:2015</div>
                <div class="card-sub-warm">{t['kpi_standards_sub']}</div>
            </div>
            """, unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div class="notion-card">
                <div class="card-label-warm">{t['kpi_phone']}</div>
                <div class="card-val-warm">+91 8539977611</div>
                <div class="card-sub-warm">piyushsatyam04@gmail.com</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        col_main, col_side = st.columns([1.25, 0.75])
        with col_main:
            with st.expander(t["about_heading"], expanded=True):
                st.markdown(t["about_body"])
                st.markdown("""
                <div style="margin-top:10px;">
                    <span class="badge-warm badge-terracotta">#SwachhBharatAbhiyan</span>
                    <span class="badge-warm badge-sage">#CleanGreenIndia</span>
                    <span class="badge-warm badge-slate">#MakeInIndia</span>
                    <span class="badge-warm">#VocalAboutLocal</span>
                </div>
                """, unsafe_allow_html=True)

            with st.expander("🎯 " + ("National Accreditations & Badges" if lang == "en" else "राष्ट्रीय प्रमाणन एवं मानक"), expanded=True):
                for badge in PDF_ALL_PAGES_DATA[7]["details"]["Certifications & Badges"]:
                    st.markdown(f"• **{badge}**")

        with col_side:
            if os.path.exists(PDF_ALL_PAGES_DATA[0]["image_file"]):
                st.image(PDF_ALL_PAGES_DATA[0]["image_file"], use_container_width=True)

            with st.expander("📍 " + ("Office & Fabrication Base" if lang == "en" else "कार्यालय एवं कार्यशाला विवरण"), expanded=True):
                st.markdown(f"""
                **🏛️ {t['reg_office']}:**  
                {PDF_ALL_PAGES_DATA[7]['details']['Registered Office']}
                
                **🏭 {t['fab_base']}:**  
                {PDF_ALL_PAGES_DATA[7]['details']['Work / Fabrication Base']}
                
                **📞 {t['phone']}:**  
                [`{PDF_ALL_PAGES_DATA[7]['details']['Direct Telephone']}`](tel:{PDF_ALL_PAGES_DATA[7]['details']['Direct Telephone'].replace(' ', '')})
                
                **✉️ {t['email']}:**  
                [`{PDF_ALL_PAGES_DATA[7]['details']['Official Email']}`](mailto:{PDF_ALL_PAGES_DATA[7]['details']['Official Email']})
                """)


# =========================================================
# TAB 2: ADVANCED MULTI-CRITERIA FILTERED CATALOG
# =========================================================
with tab_catalog:
    st.markdown(f"### 🚜 **{t['tab_catalog']}**")
    st.caption("Browse and filter all 38 products by multiple criteria: Vertical, Operation Mode, and Construction Material." if lang == "en" else "श्रेणी, संचालन मोड और निर्माण सामग्री के अनुसार सभी 38 उत्पादों को फ़िल्टर करें।")

    if not is_custom:
        all_catalog_items = []
        for p in PDF_ALL_PAGES_DATA:
            if "items" in p:
                for it in p["items"]:
                    all_catalog_items.append({"source_page": f"Page {p['page_number']}", "category": p["category"], **it})

        # Multi-Criteria Filter Toolbar
        fc1, fc2, fc3, fc4 = st.columns([1, 1, 1, 1.2])
        
        with fc1:
            cats = [f"✨ {t['all']} ({len(all_catalog_items)})"] + sorted(list(set([it["category"] for it in all_catalog_items])))
            f_cat = st.selectbox(t["filter_vertical"], cats)
            
        with fc2:
            op_modes = [f"✨ {t['all']}"] + sorted(list(set([it.get("operation", "Standard") for it in all_catalog_items])))
            f_op = st.selectbox(t["filter_op"], op_modes)
            
        with fc3:
            mats = [f"✨ {t['all']}"] + sorted(list(set([it.get("material", "Standard") for it in all_catalog_items])))
            f_mat = st.selectbox(t["filter_mat"], mats)
            
        with fc4:
            search_q = st.text_input(f"🔍 {t['search_placeholder']}", "")

        # Execute Filter
        filtered = []
        for it in all_catalog_items:
            if f_cat != f"✨ {t['all']} ({len(all_catalog_items)})" and it["category"] not in f_cat:
                continue
            if f_op != f"✨ {t['all']}" and it.get("operation") != f_op:
                continue
            if f_mat != f"✨ {t['all']}" and it.get("material") != f_mat:
                continue
            if search_q:
                q_l = search_q.lower()
                name_en = it["name"].lower()
                name_hi = it.get("name_hi", "").lower()
                specs_str = " ".join([str(v) for v in it["specs"].values()]).lower()
                if q_l not in name_en and q_l not in name_hi and q_l not in specs_str:
                    continue
            filtered.append(it)

        st.markdown(f"**{'Showing' if lang == 'en' else 'दिखाए जा रहे उत्पाद'}: {len(filtered)} / {len(all_catalog_items)}**")

        # Grid view
        cols = st.columns(2)
        for idx, item in enumerate(filtered):
            with cols[idx % 2]:
                disp_name = item["name_hi"] if lang == "hi" and "name_hi" in item else item["name"]
                st.markdown(f"""
                <div class="context-product-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="font-size:0.75rem; font-weight:800; color:{'#38bdf8' if is_dark else '#c2410c'}; text-transform:uppercase;">
                            {item['source_page']} • {item['category']}
                        </span>
                        <span style="font-size:0.72rem; font-weight:700; background:{'#1e293b' if is_dark else '#e2e8f0'}; border:1px solid {'#334155' if is_dark else '#cbd5e1'}; padding:3px 8px; border-radius:6px; color:{'#38bdf8' if is_dark else '#0f172a'};">
                            {item.get('material', 'Standard')}
                        </span>
                    </div>
                    <div class="item-title-serif">{disp_name}</div>
                    <div class="item-type-sub">{item['type']}</div>
                """, unsafe_allow_html=True)

                c_img, c_specs = st.columns([0.85, 1.15])
                with c_img:
                    if "thumb" in item and os.path.exists(item["thumb"]):
                        st.image(item["thumb"], use_container_width=True)
                    else:
                        st.caption("Photo in catalog")
                with c_specs:
                    for sk, sv in item["specs"].items():
                        st.markdown(f"• **{sk}:** `{sv}`")
                    st.markdown(f"• **⚡ Mode:** `{item.get('operation', 'Standard')}`")
                
                st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TAB 3: SIDE-BY-SIDE VISUAL COMPARER
# =========================================================
with tab_compare:
    st.markdown(f"### ⚖️ **{t['tab_compare']}**")
    st.caption("Compare specifications and photos of two models side-by-side." if lang == "en" else "दो अलग-अलग मशीनों की तस्वीरों और विशिष्टताओं की तुलना करें।")

    if not is_custom:
        all_item_names = [it["name"] for p in PDF_ALL_PAGES_DATA if "items" in p for it in p["items"]]
        
        cmp1, cmp2 = st.columns(2)
        with cmp1:
            sel_a = st.selectbox("Select Model A:" if lang == "en" else "मॉडल A चुनें:", all_item_names, index=13) # Refuse Compactor
        with cmp2:
            sel_b = st.selectbox("Select Model B:" if lang == "en" else "मॉडल B चुनें:", all_item_names, index=14) # Road Sweeper

        item_a = next((it for p in PDF_ALL_PAGES_DATA if "items" in p for it in p["items"] if it["name"] == sel_a), None)
        item_b = next((it for p in PDF_ALL_PAGES_DATA if "items" in p for it in p["items"] if it["name"] == sel_b), None)

        if item_a and item_b:
            c1, c2 = st.columns(2)
            with c1:
                disp_a = item_a["name_hi"] if lang == "hi" and "name_hi" in item_a else item_a["name"]
                st.markdown(f"""
                <div class="context-product-card" style="border-top: 4px solid {'#38bdf8' if is_dark else '#c2410c'};">
                    <div class="item-title-serif">{disp_a}</div>
                    <div class="item-type-sub">{item_a['type']}</div>
                """, unsafe_allow_html=True)
                if "thumb" in item_a and os.path.exists(item_a["thumb"]):
                    st.image(item_a["thumb"], use_container_width=True)
                for k, v in item_a["specs"].items():
                    st.markdown(f"• **{k}:** `{v}`")
                st.markdown(f"• **⚡ Operation:** `{item_a.get('operation', 'Standard')}`")
                st.markdown(f"• **🧱 Material:** `{item_a.get('material', 'Standard')}`")
                st.markdown("</div>", unsafe_allow_html=True)

            with c2:
                disp_b = item_b["name_hi"] if lang == "hi" and "name_hi" in item_b else item_b["name"]
                st.markdown(f"""
                <div class="context-product-card" style="border-top: 4px solid {'#34d399' if is_dark else '#16a34a'};">
                    <div class="item-title-serif">{disp_b}</div>
                    <div class="item-type-sub" style="color:{'#34d399' if is_dark else '#16a34a'};">{item_b['type']}</div>
                """, unsafe_allow_html=True)
                if "thumb" in item_b and os.path.exists(item_b["thumb"]):
                    st.image(item_b["thumb"], use_container_width=True)
                for k, v in item_b["specs"].items():
                    st.markdown(f"• **{k}:** `{v}`")
                st.markdown(f"• **⚡ Operation:** `{item_b.get('operation', 'Standard')}`")
                st.markdown(f"• **🧱 Material:** `{item_b.get('material', 'Standard')}`")
                st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TAB 4: INTERACTIVE LOGISTICS & OFFICE MAP
# =========================================================
with tab_map:
    st.markdown(f"### 🗺️ **{t['tab_map']}**")
    st.caption("Interactive geolocation map of Registered Headquarters, Fabrication Base, and North India logistics reach." if lang == "en" else "पंजीकृत मुख्यालय, निर्माण कार्यशाला और आपूर्ति नेटवर्क का इंटरैक्टिव मानचित्र।")

    map_view_choice = st.radio(
        "Map Focus / मानचित्र दृश्य:" if lang == "en" else "मानचित्र फोकस:",
        [
            "📍 Entire Corridor (Jogbani & Forbesganj — 14 km)" if lang == "en" else "📍 संपूर्ण कॉरिडोर (जोगबनी एवं फारबिसगंज — 14 किमी)",
            "🏛️ Registered HQ (Jogbani, Araria)" if lang == "en" else "🏛️ पंजीकृत मुख्यालय (जोगबनी, अररिया)",
            "🏭 Fabrication & Works (Forbesganj, Araria)" if lang == "en" else "🏭 विनिर्माण इकाई (फारबिसगंज, अररिया)"
        ],
        index=0,
        horizontal=True
    )

    # Determine View Center based on selection
    if "Jogbani" in map_view_choice and "Forbesganj" not in map_view_choice:
        center_lat, center_lon, zoom_lvl = 26.4172, 87.2750, 13.5
    elif "Forbesganj" in map_view_choice and "Jogbani" not in map_view_choice:
        center_lat, center_lon, zoom_lvl = 26.2974, 87.2558, 13.5
    else:
        center_lat, center_lon, zoom_lvl = 26.3573, 87.2654, 10.5

    loc_df = pd.DataFrame([
        {
            "name": "🏛️ Registered HQ (Jogbani)" if lang == "en" else "🏛️ पंजीकृत मुख्यालय (जोगबनी)",
            "lat": 26.4172,
            "lon": 87.2750,
            "address": "Patel Nagar Jogbani, Araria, Bihar — Pin 854328",
            "role": "Corporate Office & Governance" if lang == "en" else "कॉर्पोरेट एवं प्रशासनिक मुख्यालय",
            "color": [194, 65, 12, 240] if not is_dark else [56, 189, 248, 240]
        },
        {
            "name": "🏭 Fabrication Base (Forbesganj)" if lang == "en" else "🏭 विनिर्माण इकाई (फारबिसगंज)",
            "lat": 26.2974,
            "lon": 87.2558,
            "address": "Infront of DIET Forbesganj, Araria — Pin 854318",
            "role": "Heavy Machinery & Compactor Assembly" if lang == "en" else "भारी मशीनरी एवं कॉम्पेक्टर असेंबली यूनिट",
            "color": [22, 101, 52, 240] if not is_dark else [52, 211, 153, 240]
        }
    ])

    corridor_line_df = pd.DataFrame([
        {
            "path": [[87.2750, 26.4172], [87.2558, 26.2974]],
            "name": "NH-527C Transit Corridor (~14 km)"
        }
    ])

    # Pydeck Layers
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=loc_df,
        get_position="[lon, lat]",
        get_color="color",
        get_radius=1200,
        pickable=True,
        filled=True,
        stroked=True,
        get_line_color=[255, 255, 255, 255],
        get_line_width=180
    )

    text_layer = pdk.Layer(
        "TextLayer",
        data=loc_df,
        get_position="[lon, lat]",
        get_text="name",
        get_color=[255, 255, 255],
        get_size=15,
        get_alignment_baseline="'bottom'",
        get_pixel_offset=[0, -18],
        background_color=[15, 23, 42, 240] if is_dark else [15, 23, 42, 240],
        background_padding=[8, 6, 8, 6],
        background_border_radius=6
    )

    path_layer = pdk.Layer(
        "PathLayer",
        data=corridor_line_df,
        get_path="path",
        get_color=[56, 189, 248, 200] if is_dark else [194, 65, 12, 200],
        get_width=280,
        pickable=True
    )

    deck_map = pdk.Deck(
        layers=[path_layer, scatter_layer, text_layer],
        initial_view_state=pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=zoom_lvl,
            pitch=0
        ),
        map_provider="carto",
        map_style="light" if not is_dark else "dark",
        tooltip={"html": "<b>{name}</b><br/>{address}<br/><i>{role}</i>"}
    )

    st.pydeck_chart(deck_map)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f"""
        <div class="notion-card">
            <div class="card-label-warm">🏛️ {t['reg_office']}</div>
            <div style="font-weight:700; color:{'#ffffff' if is_dark else '#0f172a'}; font-size:0.95rem; margin-bottom:6px;">Patel Nagar Jogbani, Araria, Bihar — Pin 854328</div>
            <div style="font-size:0.85rem; font-weight:600; color:{'#94a3b8' if is_dark else '#334155'}; margin-bottom:10px;">Coordinates: 26.4172° N, 87.2750° E</div>
            <a href="https://maps.google.com/?q=26.4172,87.2750" target="_blank" style="display:inline-block; font-size:0.85rem; font-weight:700; color:{'#38bdf8' if is_dark else '#c2410c'}; text-decoration:none; padding:5px 12px; background:{'#1e293b' if is_dark else '#fee2e2'}; border:1.5px solid {'#38bdf8' if is_dark else '#fca5a5'}; border-radius:6px;">
                {t['open_gmaps']} ↗
            </a>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown(f"""
        <div class="notion-card">
            <div class="card-label-warm">🏭 {t['fab_base']}</div>
            <div style="font-weight:700; color:{'#ffffff' if is_dark else '#0f172a'}; font-size:0.95rem; margin-bottom:6px;">Infront of DIET Forbesganj, Araria, Bihar — Pin 854318</div>
            <div style="font-size:0.85rem; font-weight:600; color:{'#94a3b8' if is_dark else '#334155'}; margin-bottom:10px;">Coordinates: 26.2974° N, 87.2558° E</div>
            <a href="https://maps.google.com/?q=26.2974,87.2558" target="_blank" style="display:inline-block; font-size:0.85rem; font-weight:700; color:{'#38bdf8' if is_dark else '#c2410c'}; text-decoration:none; padding:5px 12px; background:{'#1e293b' if is_dark else '#fee2e2'}; border:1.5px solid {'#38bdf8' if is_dark else '#fca5a5'}; border-radius:6px;">
                {t['open_gmaps']} ↗
            </a>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# TAB 5: PAGE-BY-PAGE EXPLORER
# =========================================================
with tab_pages:
    st.markdown(f"### 📑 **{t['tab_pages']}**")
    st.caption("Inspect original high-resolution PDF page images alongside structured data." if lang == "en" else "मूल उच्च-रिज़ॉल्यूशन पीडीएफ पृष्ठों को उनकी विशिष्टताओं के साथ देखें।")

    if not is_custom:
        page_options = [f"Page {p['page_number']}: {p['page_title']} ({p['category']})" for p in PDF_ALL_PAGES_DATA]
        selected_page_str = st.selectbox("Select Page to Inspect:", page_options, index=0)
        p_num = int(selected_page_str.split(":")[0].replace("Page ", ""))
        p_data = PDF_ALL_PAGES_DATA[p_num - 1]

        col_img, col_data = st.columns([1, 1.1])
        with col_img:
            st.markdown(f"##### 🖼️ Original PDF Page {p_num}:")
            if os.path.exists(p_data["image_file"]):
                st.image(p_data["image_file"], caption=f"PDF Page {p_num}: {p_data['page_title']}", use_container_width=True)

        with col_data:
            st.markdown(f"##### ⚡ Interactive Breakdown:")
            st.markdown(f"**Category:** `{p_data['category']}`")
            st.markdown(f"""
            <div style="background:{'#131b2e' if is_dark else '#f8fafc'}; border:1.5px solid {'#1e293b' if is_dark else '#cbd5e1'}; border-left:4px solid {'#38bdf8' if is_dark else '#c2410c'}; border-radius:8px; padding:12px 14px; margin-bottom:14px; color:{'#e2e8f0' if is_dark else '#0f172a'}; font-size:0.92rem; font-weight:500;">
                {p_data['content_summary']}
            </div>
            """, unsafe_allow_html=True)

            if "items" in p_data:
                for item in p_data["items"]:
                    disp_i = item["name_hi"] if lang == "hi" and "name_hi" in item else item["name"]
                    st.markdown(f"""
                    <div class="context-product-card">
                        <div class="item-title-serif">{disp_i}</div>
                        <div class="item-type-sub">{item['type']}</div>
                    """, unsafe_allow_html=True)
                    
                    ci, cs = st.columns([0.7, 1.3])
                    with ci:
                        if "thumb" in item and os.path.exists(item["thumb"]):
                            st.image(item["thumb"], use_container_width=True)
                    with cs:
                        for k, v in item["specs"].items():
                            st.markdown(f"• **{k}:** `{v}`")
                    st.markdown("</div>", unsafe_allow_html=True)
            elif "details" in p_data:
                st.json(p_data["details"])


# =========================================================
# TAB 6: SEARCH ACROSS DOCUMENT
# =========================================================
with tab_search:
    st.markdown(f"### 🔍 **{t['tab_search']}**")
    st.caption("Search across all 38 products and 8 pages with visual matching previews." if lang == "en" else "पूरे कैटलॉग और पृष्ठों में कीवर्ड खोजें।")

    q_input = st.text_input(f"💬 {t['search_placeholder']}", placeholder="e.g. Sweeper, Compactor, 1000 Kg, Araria, HAL")

    if q_input.strip():
        search_corpus = []
        for p in PDF_ALL_PAGES_DATA:
            if "items" in p:
                for it in p["items"]:
                    search_corpus.append({
                        "section": f"Page {p['page_number']} ({p['category']}) → {it['name']}",
                        "item": it,
                        "content": f"{it['name']} ({it.get('name_hi','')}) ({it['type']}) — " + " | ".join([f"{k}: {v}" for k, v in it['specs'].items()])
                    })
            elif "details" in p:
                search_corpus.append({
                    "section": f"Page {p['page_number']} — {p['page_title']}",
                    "item": None,
                    "content": str(p["details"])
                })

        kw = [w.lower() for w in re.findall(r'\w+', q_input.strip()) if len(w) > 2]
        matches = []
        for entry in search_corpus:
            txt_lower = entry["content"].lower()
            score = sum(txt_lower.count(w) for w in kw)
            if score > 0:
                matches.append((score, entry))

        matches.sort(key=lambda x: x[0], reverse=True)

        if matches:
            st.success(f"🎯 {'Found' if lang == 'en' else 'मिले परिणाम'}: **{len(matches)}**")
            for score, hit in matches[:6]:
                hl = hit['content']
                for w in kw:
                    hl = re.sub(f"(?i)({re.escape(w)})", r"**`\1`**", hl)

                st.markdown(f"""
                <div class="search-hit-box">
                    <div style="font-size:0.78rem; font-weight:800; color:{'#38bdf8' if is_dark else '#c2410c'}; text-transform:uppercase; margin-bottom:6px;">
                        📍 {hit['section']}
                    </div>
                """, unsafe_allow_html=True)

                if hit["item"] and "thumb" in hit["item"] and os.path.exists(hit["item"]["thumb"]):
                    sc_i, sc_t = st.columns([0.4, 1.6])
                    with sc_i:
                        st.image(hit["item"]["thumb"], use_container_width=True)
                    with sc_t:
                        st.markdown(f"<div style='color:{'#f8fafc' if is_dark else '#0f172a'}; font-size:0.95rem; font-weight:500; line-height:1.6;'>{hl}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='color:{'#f8fafc' if is_dark else '#0f172a'}; font-size:0.95rem; font-weight:500; line-height:1.6;'>{hl}</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TAB 7: SHARE & QR STUDIO
# =========================================================
with tab_qr:
    st.markdown(f"### 📲 **{t['tab_qr']}**")
    st.caption("Distribute this complete interactive catalog without sending large PDF files." if lang == "en" else "बिना भारी पीडीएफ भेजे लाइव लिंक और क्यूआर कोड साझा करें।")

    c_left, c_right = st.columns([1, 1])
    with c_left:
        target_link = st.text_input("🌐 Live Link URL:", value="http://localhost:8501")
        if not is_dark:
            palette = st.selectbox("🎨 QR Theme:", ["Warm Charcoal (#2d2b29)", "Terracotta Amber (#a75d2a)", "Deep Sage (#4a614e)"])
            p_map = {"Warm Charcoal (#2d2b29)": "#2d2b29", "Terracotta Amber (#a75d2a)": "#a75d2a", "Deep Sage (#4a614e)": "#4a614e"}
            bg_c = "#ffffff"
        else:
            palette = st.selectbox("🎨 QR Theme:", ["Cyber Cyan (#00f0ff)", "Emerald (#10b981)", "Clean White (#ffffff)"])
            p_map = {"Cyber Cyan (#00f0ff)": "#00f0ff", "Emerald (#10b981)": "#10b981", "Clean White (#ffffff)": "#ffffff"}
            bg_c = "#0b0f19"

    with c_right:
        img_qr = generate_editorial_qr(target_link, fill_color=p_map[palette], back_color=bg_c)
        b_buf = io.BytesIO()
        img_qr.save(b_buf, format="PNG")
        qr_bin = b_buf.getvalue()

        st.image(qr_bin, caption=f"Scan to open live portal: {target_link}", width=220)
        st.download_button(
            "📥 Download QR Code PNG" if lang == "en" else "📥 क्यूआर कोड डाउनलोड करें (PNG)",
            data=qr_bin,
            file_name="SP_EPC_Catalog_QR.png",
            mime="image/png",
            use_container_width=True
        )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; color:{'#94a3b8' if is_dark else '#334155'}; font-size:0.85rem; font-weight:600; padding: 6px 0 20px 0;">
    <div>📖 <b>DocuSphere Portal</b> • {'Bilingual & Multi-Theme Digital Hub' if lang == 'en' else 'द्विभाषी एवं डार्क/लाइट मोड डिजिटल पोर्टल'}</div>
    <div>ISO 9001:2015 Quality Certified • Swachh Bharat Abhiyan Partner</div>
</div>
""", unsafe_allow_html=True)
