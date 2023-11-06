import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ---- DATABASE ----
url = "https://docs.google.com/spreadsheets/d/1O5KK8MmtcgqMb5JDhteJnNv1V1TK2g-S/edit?usp=sharing"

conn = st.experimental_connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url, worksheet="1562282668")
st.dataframe(data)