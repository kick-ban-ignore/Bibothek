import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

### Bibothek is a web application that allows users to upload and store book data in a database. 
### The app displays the data in a list format and provides a statistical analysis of the data in the form 
### of charts.

st.set_page_config(page_title="Bibothek App", layout="wide")

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect('book_data.db')

# Tabelle erstellen, wenn sie nicht existiert
conn.execute('''CREATE TABLE IF NOT EXISTS books
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT NOT NULL,
             author TEXT NOT NULL,
             genre TEXT NOT NULL,
             year INTEGER NOT NULL,
             age TEXT NOT NULL,
             language TEXT NOT NULL,
             location TEXT NOT NULL);''')

# CSV-Datei importieren und in die Datenbank schreiben
@st.cache_data()
def import_data():
    data = pd.read_excel('book_data.xlsx')
    data.to_sql('books', conn, if_exists='replace', index=False)

# Daten aus der Datenbank lesen
def get_data():
    cursor = conn.execute('SELECT * FROM books')
    data = pd.DataFrame(cursor.fetchall(), columns=['Titel', 'Autor', 'Genre', 'Jahr', 'Altersgruppe', 
                                                    'Sprache', 'Standort'
])
    return data

# Filter-Funktion
def filter_data(data, filters):
    for column, value in filters.items():
        if value:
            data = data[data[column].str.contains(value, case=False)]
    return data

# App-Layout
def app():
    st.title('Bibothek')
    st.sidebar.title('Filtern')

    # Daten importieren
    import_data()

    # Daten anzeigen
    # Spalten für horizontale Darstellung erstellen
    col1, col2 = st.columns(2)

    # Filter
    filters = {
        'Titel': st.sidebar.selectbox('Titel', [''] + list(get_data()['Titel'].unique())),
        'Autor': st.sidebar.selectbox('Autor', [''] + list(get_data()['Autor'].unique())),
        'Genre': st.sidebar.selectbox('Genre', [''] + list(get_data()['Genre'].unique())),
        'Jahr': st.sidebar.selectbox('Jahr', [''] + list(get_data()['Jahr'].unique())),
        'Altersgruppe': st.sidebar.selectbox('Altersgruppe', [''] + list(get_data()['Altersgruppe'].unique())),
        'Sprache': st.sidebar.selectbox('Sprache', [''] + list(get_data()['Sprache'].unique())),
        'Standort': st.sidebar.selectbox('Standort', [''] + list(get_data()['Standort'].unique()))
    }

    # Reset-Button
    if st.sidebar.button('Filter zurücksetzen'):
        filters = {key: '' for key in filters}

    # Daten filtern
    all_data = get_data()
    data = filter_data(all_data, filters)




    # Datenanalyse

    with col2:
        st.subheader('Statistische Auswertung')

        # get active filter
        active_filter = None
        
        for column, value in filters.items():
            if value:
                active_filter = column
                st.write(f"Sortiert nach {active_filter}.")
                # group data by active filter and count number of occurrences
                #agg_data = data.groupby(active_filter).size().reset_index(name='Anzahl #')
                agg_data = all_data.groupby(active_filter).size().reset_index(name='Anzahl #')
                # plot bar chart of aggregated data
                st.bar_chart(agg_data.set_index(active_filter))

        # display message if no active filter is selected
        if not active_filter:
            st.write("Gefilterte Daten sind gleich hier zu sehen 👇")
  
    # Daten als Liste anzeigen

    with col1:
        st.subheader('Liste der Bücher')

        for column, value in filters.items():
            if value:
                active_filter = column
                st.write(f"Deine Bibliothek enthält {data.shape[0]} Buch/Bücher mit {active_filter} {value}.")
        st.table(data)


if __name__ == '__main__':
    app()
