import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sponsor Match", layout="wide")
st.title("Golden Goal: Hitta sponsorer i Göteborgsområdet")

st.markdown("""
Denna app hjälper ideella idrottsföreningar att matchas med företag i Göteborgsområdet baserat på föreningens storlek och plats.
""")

#  1. Ladda in båda dataseten
@st.cache_data

def load_data():
    df1 = pd.read_csv("/mnt/data/Foretag.gbg.csv", sep=";")
    df2 = pd.read_excel("/mnt/data/bolag_1_300.xlsx")

    df1 = df1.rename(columns={"Företag": "Företagsnamn"})
    df = pd.concat([df1, df2], ignore_index=True)

    # Klassificera storlek
    def classify(row):
        try:
            anst = int(row["Anställda"])
            if anst <= 100:
                return "Liten"
            elif anst <= 500:
                return "Mellan"
            else:
                return "Stor"
        except:
            return "Okänd"

    df["storlek"] = df.apply(classify, axis=1)
    return df

df = load_data()

#  2. Föreningens information
st.header("Föreningens profil")
club_name = st.text_input("Föreningens namn")
club_location = st.text_input("Ort eller stadsdel")
club_size = st.selectbox("Föreningens storlek (medlemmar)", ["Liten (1–100)", "Mellan (101–500)", "Stor (500+)"])

# 👀 3. Filtrering baserat på match
st.subheader("Företag som matchar din förening")

if club_size.startswith("Liten"):
    matched = df[df["storlek"] == "Liten"]
elif club_size.startswith("Mellan"):
    matched = df[df["storlek"] == "Mellan"]
else:
    matched = df[df["storlek"] == "Stor"]

if club_location:
    matched = matched[matched["Postadress"].str.contains(club_location, case=False, na=False)]

if matched.empty:
    st.warning("Inga matchande företag hittades.")
else:
    st.dataframe(matched[["Företagsnamn", "Postadress", "Omsättning (tkr)", "Anställda", "storlek"]])

