import psycopg2


def create_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
        )


def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Personen (
            Id SERIAL PRIMARY KEY,
            Name TEXT NOT NULL,
            Adresse TEXT,
            Telefonnummer TEXT,
            PLZ INT,
            Seriennummer BIGINT
        );

        CREATE TABLE IF NOT EXISTS Wohnort (
            Id SERIAL PRIMARY KEY,
            PLZ INT,
            Stadt TEXT NOT NULL,
            Bundesland TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Auto (
            Seriennummer BIGINT PRIMARY KEY,
            Anzahl_Türen INT NOT NULL,
            Baujahr INT NOT NULL
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()

create_table()
