import pandas as pd
import psycopg2
import streamlit as st
from main import create_connection
import warnings

warnings.simplefilter("ignore", UserWarning)

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

bundeslaender = [
    "Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg", "Hessen",
    "Mecklenburg-Vorpommern", "Niedersachsen", "Nordrhein-Westfalen", "Rheinland-Pfalz", "Saarland",
    "Sachsen", "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen"
]

table = st.sidebar.radio("Tabelle auswählen", ["Personen", "Wohnort", "Auto", "Personen - Wohnort", "Personen - Auto"])


def show_head(table_name):
    if table_name == "Personen" or table_name == "Wohnort" or table_name == "Auto":
        try:
            conn = create_connection()
            query = f"SELECT * FROM {table_name} ORDER BY ctid DESC LIMIT 5;"
            data = pd.read_sql(query, conn)
            conn.close()

            data.columns = data.columns.str.title()
            st.title(f"{table_name}")
            return data
        except Exception as e:
            st.error(f"Fehler beim Abrufen der Daten: {e}")
            return pd.DataFrame()


    elif table_name == "Personen - Wohnort":
        try:
            conn = create_connection()
            query = """
                    SELECT Personen.Name, Personen.Adresse, Personen.Telefonnummer, Personen.Plz, Wohnort.Stadt, Wohnort.Bundesland
                    FROM Personen
                    INNER JOIN Wohnort ON Personen.PLZ = Wohnort.PLZ
                    ORDER BY Personen.ctid DESC
                    LIMIT 5;
                     """
            data = pd.read_sql(query, conn)
            conn.close()
            data.columns = data.columns.str.title()
            st.title(f"{table_name}")
            return data
        except Exception as e:
            st.error(f"Fehler beim Abrufen der Daten: {e}")
            return pd.DataFrame()

    elif table_name == "Personen - Auto":
        try:
            conn = create_connection()
            query = """
                    SELECT Personen.Name, Personen.Adresse, Personen.Telefonnummer, Personen.Plz, Auto.Seriennummer, Auto.Anzahl_Türen, Auto.Baujahr
                    FROM Personen
                    INNER JOIN Auto ON Personen.Seriennummer = Auto.Seriennummer
                    ORDER BY Personen.ctid DESC
                    LIMIT 5;
                    """
            data = pd.read_sql(query, conn)
            conn.close()
            data.columns = data.columns.str.title()
            st.title(f"{table_name}")
            return data
        except Exception as e:
            st.error(f"Fehler beim Abrufen der Daten: {e}")
            return pd.DataFrame()


def show_person_input():
    st.text("Person hinzufügen")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name:", key="person_name")
        address = st.text_input("Adresse:", key="person_address")
    with col2:
        phone = st.text_input("Telefonnummer:", key="person_phone")
        plz = st.text_input("PLZ:", key="person_plz")
        car = st.text_input("Seriennummer:", key="person_car")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Daten hinzufügen", key="add_person_btn"):
            add_person(name, address, phone, plz, car)
    with col2:
        if st.button("Eintrag löschen", key="delete_person_btn"):
            delete_person(name)


def show_city_input():
    st.text("Stadt hinzufügen")
    plz = st.text_input("PLZ:", key="city_plz")
    city = st.text_input("Stadt:", key="city_name")
    state = st.selectbox("Bundesland", [""] + bundeslaender, key="city_state")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Daten hinzufügen", key="add_city_btn"):
            add_city(plz, city, state)
    with col2:
        if st.button("Eintrag löschen", key="delete_city_btn"):
            delete_city(plz)


def show_car_input():
    st.text("Auto hinzufügen")
    serial = st.text_input("Seriennummer:", key="car_serial")
    doors = st.text_input("Anzahl Türen:", key="car_doors")
    year = st.text_input("Baujahr:", key="car_year")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Daten hinzufügen", key="add_car_btn"):
            add_car(serial, doors, year)
    with col2:
        if st.button("Eintrag löschen", key="delete_car_btn"):
            delete_car(serial)


def show_person_city_input():
    st.text("Beides hinzufügen")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name:", key="person_city_name")
        address = st.text_input("Adresse:", key="person_city_address")
        phone = st.text_input("Telefonnummer:", key="person_city_phone")
        car = st.text_input("Seriennummer:", key="person_city_car")

    with col2:
        plz = st.text_input("PLZ:", key="person_city_plz")
        city = st.text_input("Wohnort:", key="person_city_city")
        state = st.selectbox("Bundesland", [""] + bundeslaender, key="person_city_state")

    with col1:
        if st.button("Daten hinzufügen", key="add_person_city_btn"):
            add_person(name, address, phone, int(plz), int(car))
            add_city(int(plz), city, state)

    with col2:
        if st.button("Eintrag löschen", key="delete_person_city_btn"):
            delete_person(name)
            delete_city(plz)


def show_person_car_input():
    st.text("Beides hinzufügen")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name:", key="person_car_name")
        address = st.text_input("Adresse:", key="person_car_address")
        phone = st.text_input("Telefonnummer:", key="person_car_phone")
        plz = st.text_input("PLZ:", key="person_car_plz")

    with col2:
        serial = st.text_input("Seriennummer:", key="person_car_car")
        doors = st.text_input("Anzahl Türen:", key="person_car_doors")
        year = st.text_input("Baujahr:", key="person_car_year")

    with col1:
        if st.button("Daten hinzufügen", key="add_person_city_btn"):
            add_person(name, address, phone, int(plz), int(serial))
            add_car(int(serial), int(doors), int(year))

    with col2:
        if st.button("Eintrag löschen", key="delete_person_city_btn"):
            delete_person(name)
            delete_city(plz)


def add_person(name, address, phone, plz, car):
    if not all([name, address, phone, plz, car]):
        st.warning("Bitte alle Felder ausfüllen!")
        return

    if len(str(plz)) < 5 or not str(plz).isdigit():
        st.error("PLZ muss mindestens 5 Buchstaben haben!")
        return
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Personen (Name, Adresse, Telefonnummer, PLZ, Seriennummer)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, address, phone, plz, car))

        conn.commit()
        cursor.close()
        conn.close()
        st.success("Person erfolgreich hinzugefügt!")
    except psycopg2.DatabaseError as e:
        st.error(f"Fehler: {e}")


def add_city(plz, city, state):
    if not all([plz, city, state]):
        st.warning("Bitte alle Felder ausfüllen!")
        return

    if len(str(plz)) < 5 or not str(plz).isdigit():
        st.error("PLZ muss mindestens 5 Buchstaben haben!")
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Wohnort (PLZ, Stadt, Bundesland)
            VALUES (%s, %s, %s)
        """, (plz, city, state))

        conn.commit()
        cursor.close()
        conn.close()
        st.success("Wohnort erfolgreich hinzugefügt!")
    except psycopg2.DatabaseError as e:
        st.error(f"Fehler: {e}")


def add_car(serial, doors, year):
    if not all([serial, doors, year]):
        st.warning("Bitte alle Felder ausfüllen!")
        return

    if type(serial) != int:
        try:
            int(serial)
        except Exception as e:
            st.error("Gebe eine korrekte Seriennummer ein.")
            st.error(e)
            return

    if type(doors) != int:
        st.error("Gebe einen korrekten Anzahl Türen Wert ein.")
        return
    if doors == 0 or doors > 20:
        st.error("Ein Auto mit dieser Anzahl an Türen existiert nicht.")
        return

    if type(year) == int:
        if int(year) > 2025:
            st.error("Dieses Jahr gibt es noch nicht!")
            return
    else:
        st.error("Gebe ein gültiges Jahr ein!")
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Auto (Seriennummer, Anzahl_Türen, Baujahr)
            VALUES (%s, %s, %s)
        """, (serial, doors, year))

        conn.commit()
        cursor.close()
        conn.close()
        st.success("Auto erfolgreich hinzugefügt!")
    except psycopg2.DatabaseError as e:
        st.error(f"Fehler: {e}")


def delete_person(name):
    if not name:
        st.warning("Bitte einen Namen eingeben!")
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM Personen;")
        names = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()

        if str(name) in names:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Personen WHERE Name = %s", (name,))
            conn.commit()
            cursor.close()
            conn.close()
            st.success(f"Person '{name}' erfolgreich gelöscht!")
        else:
            st.error(f"{name} existiert nicht in der Datenbank")
    except psycopg2.DatabaseError as e:
        st.error(f"Fehler: {e}")


def delete_city(plz):
    if not plz:
        st.warning("Bitte gebe eine Postleitzahl ein!")
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT PLZ FROM Wohnort;")
        postcode = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()

        if int(plz) in postcode:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Wohnort WHERE PLZ = %s", (plz,))
            conn.commit()
            cursor.close()
            conn.close()
            st.success(f"PLZ: '{plz}' erfolgreich gelöscht!")
        else:
            st.error(f"{plz} existiert nicht in der Datenbank")
    except psycopg2.DatabaseError as e:
        st.error(f"Fehler: {e}")


def delete_car(serial):
    if not serial:
        st.warning("Bitte eine Seriennummer eingeben!")
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT seriennummer FROM Auto;")
        serial_numbers = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()

        if int(serial) in serial_numbers:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Auto WHERE Seriennummer = %s", (serial,))
            conn.commit()
            cursor.close()
            conn.close()
            st.success(f"Auto Nr.:'{serial}' erfolgreich gelöscht!")
        else:
            st.error(f"{serial} existiert nicht in der Datenbank")
    except psycopg2.DatabaseError as e:
        st.error(f"Fehler: {e}")


df = show_head(table)
st.dataframe(df, use_container_width=True)

if table == "Personen":
    show_person_input()
elif table == "Wohnort":
    show_city_input()
elif table == "Auto":
    show_car_input()
elif table == "Personen - Wohnort":
    show_person_city_input()
elif table == "Personen - Auto":
    show_person_car_input()
