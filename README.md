# ⚡ DocuSphere — Futuristic Interactive PDF Web Dashboard

Modernize static PDFs (Job Descriptions, Product Catalogs, Specifications, Resumes) into a high-performance, dynamic, clickable web dashboard with zero PDF download fatigue.

---

## 🌟 Key Features

1. **🚀 Responsive Futuristic UI**:
   - Cyber-glassmorphism styling with glowing badge indicators, responsive metric cards, and clean typography.
2. **📂 Dynamic PDF Ingestion & Parsing**:
   - Sidebar file uploader powered by `pdfplumber` and `pypdf`.
   - Automatic section discovery (Overview, Responsibilities, Requirements, Technical Specs, Contacts).
   - Regex-based key attribute extraction (Experience, Locations, Emails, Phone Numbers).
3. **✨ Preloaded Rich Showcase (SP & E.P.C. Company)**:
   - Out-of-the-box support for the 8-page EPC company catalog with structured interactive vehicle & equipment specs, urban art, waste management solutions, and contact points.
4. **🤖 AI-Like Smart Search & Query Engine**:
   - Instant search across all parsed pages and sections.
   - Relevance scoring and glowing keyword highlighting.
5. **📲 Dynamic QR Code Studio**:
   - Built-in live link sharing generator using `qrcode` and `Pillow`.
   - Custom color themes (Cyber Cyan, Emerald Green, Electric Purple, Classic Dark).
   - 1-click High-Resolution PNG download.

---

## 🛠️ Tech Stack

- **Frontend & Backend:** Python, Streamlit
- **PDF Extraction:** `pypdf`, `pdfplumber`
- **QR Code Engine:** `qrcode[pil]`, `Pillow`
- **Data & Tables:** `pandas`

---

## 🚀 Quickstart & Local Setup

### 1. Clone or Open the directory
```bash
cd sat_nexgen
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit App
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ Deploying to Streamlit Community Cloud

1. Push this repository to **GitHub**.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Connect your GitHub account and select your repository.
4. Set Main file path: `app.py`.
5. Click **Deploy!** 🎉
