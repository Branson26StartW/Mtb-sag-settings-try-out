# mtb_suspension_app.py
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="MTB Suspension Setup", layout="centered")

# Helper data & functions
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

def calc_sag_mm(travel_mm, sag_pct):
    return round(travel_mm * sag_pct / 100, 1)

def base_pressure(weight_kg):
    # eenvoudige baseline
    return round(weight_kg * 1.1, 1)
