import streamlit as st
from api_data_clients import get_entreprise_infos

st.title("Recherche d'informations sur une entreprise")

nom = st.text_input("Nom de l'entreprise")
code_postal = st.text_input("Code postal (pas obligatoire)")

if st.button("Rechercher"):
    if nom:
        try:
            df = get_entreprise_infos(nom, code_postal)
            if df.empty:
                st.warning("Aucun résultat trouvé.")
            else:
                st.dataframe(df)
        except Exception as e:
            st.error(f"Erreur lors de la recherche : {e}")
    else:
        st.info("Veuillez entrer le nom de l'entreprise.")
