import warnings
import streamlit as st
import pandas as pd
from main import create_connection

warnings.simplefilter("ignore", UserWarning)

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)


def get_data(table):
    try:
        conn = create_connection()
        query = f"SELECT * FROM {table};"
        data = pd.read_sql(query, conn)
        conn.close()
        return data
    except Exception as e:
        st.error(f"Fehler beim Abrufen der Daten: {e}")
        return pd.DataFrame()


def join_person_city():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Personen.Name, Personen.Adresse, Personen.Telefonnummer, Personen.Plz, Wohnort.Stadt, Wohnort.Bundesland
            FROM Personen
            INNER JOIN Wohnort
            ON Personen.PLZ = Wohnort.PLZ;
                """)
        column_names = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()

        if not data:
            st.error("Kein INNER Join möglich")

        cursor.close()
        conn.close()
        df = pd.DataFrame(data, columns=column_names)
        st.dataframe(df)

    except Exception as e:
        st.error(f"Fehler beim Joinen der Daten: {e}")
        return pd.DataFrame()

def join_person_car():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Personen.Name, Personen.Adresse, Personen.Telefonnummer, Personen.Plz, Auto.Anzahl_Türen, Auto.Baujahr
            FROM Personen
            INNER JOIN Auto
            ON Personen.Seriennummer = Auto.Seriennummer;
                """)
        column_names = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()

        if not data:
            st.error("Kein INNER Join möglich")

        cursor.close()
        conn.close()
        df = pd.DataFrame(data, columns=column_names)
        st.dataframe(df)

    except Exception as e:
        st.error(f"Fehler beim Joinen der Daten: {e}")
        print(e)
        return pd.DataFrame()


person_selected = st.sidebar.checkbox("Personen")
wohnort_selected = st.sidebar.checkbox("Wohnort")
auto_selected = st.sidebar.checkbox("Auto")

selected_tables = []
if person_selected:
    selected_tables.append("Personen")
if wohnort_selected:
    selected_tables.append("Wohnort")
if auto_selected:
    selected_tables.append("Auto")

if "Personen" in selected_tables:
    st.title("Personen")
    st.dataframe(get_data("Personen"))

if "Wohnort" in selected_tables:
    st.title("Wohnort")
    st.dataframe(get_data("Wohnort"))

if "Auto" in selected_tables:
    st.title("Auto")
    st.dataframe(get_data("Auto"))

if "Personen" in selected_tables and "Wohnort" in selected_tables:
    st.title("Personen Wohnort")
    join_person_city()

if "Personen" in selected_tables and "Auto" in selected_tables:
    st.title("Personen Auto")
    join_person_car()