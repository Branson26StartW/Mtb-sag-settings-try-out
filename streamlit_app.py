# mtb_suspension_app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="MTB Suspension Setup", layout="centered")

# -----------------------------
# Helper data & functies
# -----------------------------

BRANDS = {
    "Algemeen / onbekend": 1.00,
    "Fox": 1.02,
    "RockShox": 0.98,
    "Öhlins": 1.05,
}

STYLE_FACTORS = {
    "XC / Marathon": 0.90,
    "Trail / All‑Mountain": 1.00,
    "Enduro / Aggressief": 1.10,
}

TERRAIN_FACTORS = {
    "Flow / smooth": 0.95,
    "Mixed / trail": 1.00,
    "Rockgarden / roots": 1.05,
    "Bikepark / jumps": 1.08,
}

def calc_sag_mm(travel_mm, sag_pct):
    return round(travel_mm * sag_pct / 100, 1)

def base_pressure(weight_kg):
    # eenvoudige baseline
    return weight_kg * 1.1

def tuned_pressure(weight_kg, style, terrain, brand):
    p = base_pressure(weight_kg)
    p *= STYLE_FACTORS[style]
    p *= TERRAIN_FACTORS[terrain]
    p *= BRANDS[brand]
    return int(round(p))

def rebound_advice(style, terrain):
    if style == "XC / Marathon":
        return "Snelle rebound (meer open) — focus op efficiëntie."
    if style == "Trail / All‑Mountain":
        return "Gebalanceerde rebound — mix van grip en support."
    if style == "Enduro / Aggressief":
        if terrain in ["Rockgarden / roots", "Bikepark / jumps"]:
            return "Tragere rebound (meer dicht) — controle bij harde impacts."
        return "Medium‑trage rebound — stabiliteit bij snelheid."
    return "Standaard rebound."

def compression_advice(style, terrain):
    if style == "XC / Marathon":
        return "Meer compressie (firm) — minder inzakken bij trappen."
    if style == "Trail / All‑Mountain":
        return "Medium compressie — balans tussen grip en support."
    if style == "Enduro / Aggressief":
        if terrain in ["Rockgarden / roots", "Bikepark / jumps"]:
            return "Minder compressie (open) — maximale grip en tracking."
        return "Medium‑low compressie — gevoelig begin, support in midden."
    return "Standaard compressie."

def ensure_session():
    if "setups" not in st.session_state:
        st.session_state["setups"] = []

# -----------------------------
# UI
# -----------------------------

st.title("🚵 MTB Suspension Setup Tool vΩ")
st.write("Webapp voor **SAG**, **luchtdruk**, **rebound** en **compressie**, afgestemd op **gewicht**, **rijstijl**, **merk** en **terrein**.")

st.header("1. Rijdergegevens")
col_w1, col_w2 = st.columns(2)
with col_w1:
    weight = st.slider("Gewicht (kg)", 45, 120, 78)
with col_w2:
    style = st.selectbox("Rijstijl", ["XC / Marathon", "Trail / All‑Mountain", "Enduro / Aggressief"])

st.header("2. Fiets & veerweg")
col_b1, col_b2 = st.columns(2)
with col_b1:
    fork_travel = st.number_input("Voorvork veerweg (mm)", 100, 200, 150)
    fork_brand = st.selectbox("Voorvork merk", list(BRANDS.keys()))
with col_b2:
    shock_travel = st.number_input("Achterdemper veerweg (mm)", 30, 80, 55)
    shock_brand = st.selectbox("Achterdemper merk", list(BRANDS.keys()))

st.header("3. Terrein & SAG‑doel")
col_t1, col_t2 = st.columns(2)
with col_t1:
    terrain = st.selectbox("Typisch terrein", list(TERRAIN_FACTORS.keys()))
with col_t2:
    sag_pct = st.slider("Gewenste SAG (%)", 15, 35, 30)

if st.button("🔧 Bereken setup"):
    ensure_session()

    # SAG
    fork_sag = calc_sag_mm(fork_travel, sag_pct)
    shock_sag = calc_sag_mm(shock_travel, sag_pct)

    # Druk
    fork_psi = tuned_pressure(weight, style, terrain, fork_brand)
    shock_psi = tuned_pressure(weight, style, terrain, shock_brand)

    # Rebound & compressie
    rebound = rebound_advice(style, terrain)
    compression = compression_advice(style, terrain)

    st.subheader("📌 Resultaten")

    st.markdown("### 🔧 SAG‑instellingen")
    st.write(f"- Voorvork SAG: **{fork_sag} mm** ({sag_pct}%)")
    st.write(f"- Achterdemper SAG: **{shock_sag} mm** ({sag_pct}%)")

    st.markdown("### 💨 Aanbevolen luchtdruk")
    st.write(f"- Voorvork (**{fork_brand}**): **{fork_psi} PSI**")
    st.write(f"- Achterdemper (**{shock_brand}**): **{shock_psi} PSI**")

    st.markdown("### 🔁 Rebound‑advies")
    st.write(rebound)

    st.markdown("### 🧱 Compressie‑advies")
    st.write(compression)

    # Setup bewaren
    setup = {
        "gewicht_kg": weight,
        "stijl": style,
        "terrein": terrain,
        "fork_travel_mm": fork_travel,
        "shock_travel_mm": shock_travel,
        "fork_brand": fork_brand,
        "shock_brand": shock_brand,
        "sag_pct": sag_pct,
        "fork_sag_mm": fork_sag,
        "shock_sag_mm": shock_sag,
        "fork_psi": fork_psi,
        "shock_psi": shock_psi,
        "rebound": rebound,
        "compressie": compression,
    }
    st.session_state["setups"].append(setup)

    st.success("Setup berekend en toegevoegd aan je lijst.")

    # Grafieken
    st.markdown("### 📈 SAG‑curve (mm vs %)")
    sag_range = np.arange(15, 36)
    fork_sag_curve = [calc_sag_mm(fork_travel, p) for p in sag_range]
    shock_sag_curve = [calc_sag_mm(shock_travel, p) for p in sag_range]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(sag_range, fork_sag_curve, label="Voorvork SAG (mm)")
    ax.plot(sag_range, shock_sag_curve, label="Achterdemper SAG (mm)")
    ax.axvline(sag_pct, color="gray", linestyle="--", alpha=0.7)
    ax.set_xlabel("SAG (%)")
    ax.set_ylabel("SAG (mm)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    st.markdown("### 📈 Druk vs gewicht (simulatie)")
    weights = np.arange(50, 111, 5)
    fork_pressures = [tuned_pressure(w, style, terrain, fork_brand) for w in weights]
    shock_pressures = [tuned_pressure(w, style, terrain, shock_brand) for w in weights]

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot(weights, fork_pressures, label="Voorvork PSI")
    ax2.plot(weights, shock_pressures, label="Achterdemper PSI")
    ax2.axvline(weight, color="gray", linestyle="--", alpha=0.7)
    ax2.set_xlabel("Gewicht (kg)")
    ax2.set_ylabel("PSI")
    ax2.grid(True)
    ax2.legend()
    st.pyplot(fig2)

st.markdown("---")
st.header("📂 Opgeslagen setups")

ensure_session()
if st.session_state["setups"]:
    df_setups = pd.DataFrame(st.session_state["setups"])
    st.dataframe(df_setups, use_container_width=True)

    csv = df_setups.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download setups als CSV",
        data=csv,
        file_name="mtb_suspension_setups.csv",
        mime="text/csv",
    )
else:
    st.info("Nog geen setups opgeslagen. Bereken eerst een setup.")
