import streamlit as st
import numpy as np

st.set_page_config(page_title="MTB Suspension Setup", layout="centered")

# -----------------------
# Config & helper data
# -----------------------

BRANDS = {
    "Algemeen / onbekend": 1.00,
    "Fox": 1.02,
    "RockShox": 0.98,
    "Öhlins": 1.05,
}

STYLE_FACTORS = {
    "XC / Marathon": 0.90,
    "Trail / All-Mountain": 1.00,
    "Enduro / Aggressief": 1.10,
}

TERRAIN_FACTORS = {
    "Flow / smooth": 0.95,
    "Mixed / trail": 1.00,
    "Rockgarden / roots": 1.05,
    "Bikepark / jumps": 1.08,
}

def calc_sag_mm(travel_mm: float, sag_pct: float) -> float:
    return round(travel_mm * sag_pct / 100.0, 1)

def base_pressure(weight_kg: float) -> float:
    # eenvoudige baseline: ~1.1x lichaamsgewicht
    return round(weight_kg * 1.1, 1)

def tuned_pressure(weight_kg: float,
                   brand_factor: float,
                   style_factor: float,
                   terrain_factor: float,
                   front: bool = True) -> float:
    base = base_pressure(weight_kg)
    # voorvork iets hoger, demper iets lager
    if front:
        base *= 1.05
    else:
        base *= 0.95
    pressure = base * brand_factor * style_factor * terrain_factor
    return round(pressure, 1)

# -----------------------
# UI
# -----------------------

st.title("MTB Suspension Setup")
st.write("Bereken een **realistische start‑setup** voor vork en demper op basis van jouw gewicht, rijstijl en terrein.")

with st.sidebar:
    st.header("Rijder & fiets")
    weight_kg = st.number_input("Rijdergewicht (kg, met gear)", 50.0, 130.0, 80.0, 1.0)
    brand = st.selectbox("Merk (vork/demper)", list(BRANDS.keys()))
    style = st.selectbox("Rijstijl", list(STYLE_FACTORS.keys()))
    terrain = st.selectbox("Terrein", list(TERRAIN_FACTORS.keys()))

    st.header("Fietsparameters")
    fork_travel = st.number_input("Vork travel (mm)", 80, 190, 150, 5)
    shock_travel = st.number_input("Demper stroke (mm)", 30, 70, 60, 1)

    st.header("Doel‑SAG (%)")
    fork_sag_pct = st.slider("Doel‑SAG vork (%)", 15, 35, 20)
    shock_sag_pct = st.slider("Doel‑SAG demper (%)", 20, 40, 30)

brand_factor = BRANDS[brand]
style_factor = STYLE_FACTORS[style]
terrain_factor = TERRAIN_FACTORS[terrain]

# Berekeningen
fork_sag_mm = calc_sag_mm(fork_travel, fork_sag_pct)
shock_sag_mm = calc_sag_mm(shock_travel, shock_sag_pct)

fork_pressure = tuned_pressure(weight_kg, brand_factor, style_factor, terrain_factor, front=True)
shock_pressure = tuned_pressure(weight_kg, brand_factor, style_factor, terrain_factor, front=False)

st.subheader("Resultaten – startinstellingen")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Vork")
    st.write(f"**Doel‑SAG:** {fork_sag_pct}%  →  **{fork_sag_mm} mm**")
    st.write(f"**Geschatte druk:** {fork_pressure} psi")
    st.caption("Tip: meet SAG in rijhouding, met gear, in je normale positie.")

with col2:
    st.markdown("### Demper")
    st.write(f"**Doel‑SAG:** {shock_sag_pct}%  →  **{shock_sag_mm} mm**")
    st.write(f"**Geschatte druk:** {shock_pressure} psi")
    st.caption("Tip: gebruik o‑ring of tie‑wrap om slag te meten.")

st.markdown("---")
st.markdown(
    "Dit zijn **startwaarden**. Fijn‑tuning doe je op trail: "
    "meer druk voor support & pop, minder druk voor grip & comfort."
)
