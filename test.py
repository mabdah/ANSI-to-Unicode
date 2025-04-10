import streamlit as st
import pandas as pd
import npttf2utf
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from bijoy2unicode import converter
import tempfile
import os

# Streamlit page setup
st.set_page_config(page_title="ANSI to Unicode Converter", page_icon="📁")
st.title("📁 ANSI to Unicode Converter")

# Dropdown for input font
input_choice = st.selectbox(
    "Choose Input Font",
    options=["Preeti (Nepali)", "Bijoy(Bengla)", ],
    index=0
)

# Load Preeti mapper
map_file = "./map.json"
mapper = npttf2utf.FontMapper(map_file)

# Convert Nepali numbers to English
def convert_phone_to_english(phone_number):
    if pd.notnull(phone_number):
        return transliterate(str(phone_number), sanscript.DEVANAGARI, sanscript.ITRANS).translate(
            str.maketrans("०१२३४५६७८९", "0123456789")
        )
    return ""

# Unified conversion function
def convert_to_unicode(text):
    if pd.notnull(text):
        text = str(text)
        if input_choice == "Preeti (Nepali)":
            return mapper.map_to_unicode(text, from_font="Preeti")
        elif input_choice == "Bijoy(Bangla)":
           test = converter.Unicode()
           return test.convertBijoyToUnicode(text)
    return ""


# File upload section
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if "Title" in df.columns:
        df["Title"] = df["Title"].map(convert_to_unicode)
        if "Location" in df.columns:
            df["Location"] = df["Location"].map(convert_to_unicode)
        df["Name"] = df["Name"].map(convert_to_unicode)
        if "Phone Number" in df.columns:
            df["Phone Number"] = df["Phone Number"].map(convert_phone_to_english)

        # Export converted file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            df.to_excel(tmp.name, index=False)
            tmp_path = tmp.name

        st.success("✅ Conversion complete!")
        with open(tmp_path, "rb") as file:
            st.download_button(
                label="📥 Download Converted File",
                data=file,
                file_name="converted_unicode.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.error("❌ 'Title' column not found in the uploaded file.")
