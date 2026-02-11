import streamlit as st
from groq import Groq

# -----------------------------
# CONFIGURATION GROQ
# -----------------------------
GROQ_API_KEY = "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"  # 🔴 Remplace par ta clé Groq (ne la partage pas)
client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# STYLE GLOBAL (POLICE + THEME)
# -----------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    h1 {
        color: #2C3E50;
        font-weight: 700;
        margin-bottom: 20px;
    }

    h2, h3 {
        color: #34495E;
        font-weight: 600;
        margin-top: 25px;
    }

    .stAlert {
        border-radius: 10px;
        padding: 15px;
    }

    textarea {
        border-radius: 10px !important;
        border: 1px solid #BDC3C7 !important;
        padding: 10px !important;
        font-size: 15px !important;
    }

    .stButton>button {
        background-color: #1ABC9C;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        transition: 0.3s;
        cursor: pointer;
    }

    .stButton>button:hover {
        background-color: #16A085;
        transform: scale(1.02);
    }

    .section-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E0E0E0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div style="background-color:#1ABC9C;padding:20px;border-radius:10px;margin-bottom:20px;">
    <h1 style="color:white;text-align:center;margin:0;">Assistant OPC – Analyse Professionnelle d'Offres</h1>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# INTERFACE DE SAISIE
# -----------------------------
st.write("Colle ici l'offre d'emploi que tu veux analyser :")
offre = st.text_area("Offre d'emploi", height=1000)

# -----------------------------
# SCORING OPC (VERSION POURCENTAGE)
# -----------------------------
def calculer_score(texte):
    score_total = 0
    score_max = 0
    details = {}

    criteres = {
        "OPC": 80,
        "bâtiment": 90,
        "logement": 60,
        "construction neuve": 80,
        "pilotage de chantier": 80,
        "Suivi de travaux": 60,
        "travaux de réhabilitation": 40,
        "site occupé": 30,
        "suivi budgetaire": 80,
        "ordonnancement": 60,
        "coordination": 50,
        "planning": 70,
        "MS Project": 60,
        "Primavera": 60,
        "chantier": 30,
        "BTP": 20,
        "infrastructure": 20,
        "sécurité": 40,
        "pilotage": 50,
    }

    texte_lower = texte.lower()

    for mot, pourcentage in criteres.items():
        score_max += pourcentage
        if mot.lower() in texte_lower:
            score_total += pourcentage
            details[mot] = pourcentage

    score_global = round((score_total / score_max) * 100, 1)

    return score_global, details

# -----------------------------
# RÉSUMÉ IA GROQ
# -----------------------------
def resumer_ia(texte):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es un expert en analyse d'offres d'emploi, spécialisé en OPC. "
                        "Produis un résumé structuré et détaillé. "
                        "Structure : 1) Présentation du poste, 2) Missions, 3) Compétences, "
                        '4) Profil recherché, 5) Mots clés importants.'
                    )
                },
                {"role": "user", "content": texte}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        return completion.choices[0].message.content

    except Exception as e:
        return f"Erreur Groq : {str(e)}"

# -----------------------------
# ANALYSE APPROFONDIE
# -----------------------------
def analyse_offre_ia(texte):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Analyse cette offre d'emploi de manière professionnelle. "
                        "Structure obligatoire : "
                        "1) Résumé global, "
                        "2) Missions principales, "
                        "3) Compétences techniques, "
                        "4) Outils/logiciels, "
                        "5) Profil recherché, "
                        "6) Contraintes du poste, "
                        "7) Mots clés importants."
                    )
                },
                {"role": "user", "content": texte}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        return completion.choices[0].message.content

    except Exception as e:
        return f"Erreur Groq : {str(e)}"

# -----------------------------
# PROFIL D'AHMED
# -----------------------------
profil_ahmed = """
Ingénieur civil spécialisé en OPC, coordination, ordonnancement et pilotage, bâtiment et le calcul de structure, BIM et planification 4D. 
Compétences : planification, MS Project, sécurité, réunions de chantier, reporting, gestion des risques, suivi de travaux, rédaction des comptes rendus, élaboration des plannings DCE et TCE, MOE, MOA. 
Expérience en coordination multi-intervenants et suivi d'avancement, suivi des travaux en milieu occupé, opérations de réhabilitation et construction neuves, suivi budgetaire, plannings financier. 
"""

# -----------------------------
# ANALYSE DE COMPATIBILITÉ
# -----------------------------
def analyse_compatibilite(offre, profil):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Compare le profil du candidat avec l'offre d'emploi. "
                        "Structure : 1) Points forts, 2) Points faibles, "
                        "3) Ce qu'il doit mettre en avant, 4) Ce qu'il doit préparer pour l'entretien."
                    )
                },
                {"role": "user", "content": f"OFFRE : {offre}\n\nPROFIL : {profil}"}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        return completion.choices[0].message.content

    except Exception as e:
        return f"Erreur Groq : {str(e)}"

# -----------------------------
# LETTRE DE MOTIVATION
# -----------------------------
def lettre_motivation(offre, profil):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Rédige une lettre de motivation professionnelle, concise, personnalisée, "
                        "adaptée à l'offre et au profil du candidat."
                    )
                },
                {"role": "user", "content": f"OFFRE : {offre}\n\nPROFIL : {profil}"}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        return completion.choices[0].message.content

    except Exception as e:
        return f"Erreur Groq : {str(e)}"

# -----------------------------
# BOUTON ANALYSER
# -----------------------------
if st.button("Analyser"):
    if offre.strip() == "":
        st.warning("Merci de coller une offre avant d'analyser.")
    else:

        # Score OPC
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("📊 Score OPC")
        score, details = calculer_score(offre)
        st.success(f"Score OPC : {score} %")
        st.write("Détails des mots clés détectés :")
        if details:
            for mot, pts in details.items():
                st.write(f"- {mot} : +{pts} %")
        else:
            st.write("Aucun mot clé OPC détecté.")
        st.markdown('</div>', unsafe_allow_html=True)


        # Résumé IA
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("🧠 Résumé IA (intelligent)")
        st.write(resumer_ia(offre))
        st.markdown('</div>', unsafe_allow_html=True)

        # Analyse approfondie
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("🔍 Analyse approfondie de l'offre")
        st.write(analyse_offre_ia(offre))
        st.markdown('</div>', unsafe_allow_html=True)

        # Compatibilité
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("🎯 Analyse de compatibilité")
        st.write(analyse_compatibilite(offre, profil_ahmed))
        st.markdown('</div>', unsafe_allow_html=True)

        # Lettre de motivation
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("✉️ Lettre de motivation automatique")
        st.write(lettre_motivation(offre, profil_ahmed))
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
<hr>
<div style="text-align:center;color:#7F8C8D;font-size:13px;margin-top:10px;">
    Développé par Ahmed – Assistant OPC IA • 2026
</div>
""", unsafe_allow_html=True)

