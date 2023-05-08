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
    st.title('Bibothek 📚')
    expander = st.expander("Was kann die App?", expanded=False)
    with expander:
        st.write("Bibothek ist eine Webanwendung, die es Nutzern ermöglicht, Buchdaten hochzuladen und in einer Datenbank zu speichern. Mit dieser Anwendung können Benutzer eine Excel-Datei mit einer Liste von Büchern mit ihren jeweiligen Merkmalen (Titel, Autor, Genre, Jahr, Altersgruppe, Sprache und aktueller Standort (eigenes Kinderzimmer, bei Freunden, bei Oma und Opa, usw.) hochladen, in einer Datenbank speichern und als Tabelle anzeigen lassen. Außerdem bietet es eine statistische Analyse der Daten in Form eines Diagramms.")
        st.write("🚀TODO für die kommenden Updates:")
        st.write("- Datenimport via Drag & Drop")
        st.write("- Update & Delete via SQL")
        st.write("- SQL-Kommandos direkt im Interface")
        st.write("- mehrere Filter gleichzeitig")
        st.write("- Bugfix: Jahr")
        st.write("- Standort-Historie")
        st.write("- mehr Charts")
        hide = """
        <style>
        ul.streamlit-expander {
            border: 0 !important;
        </style>
        """
        st.markdown(hide, unsafe_allow_html=True)

    st.sidebar.title('Filtern')

    # Daten importieren
    import_data()

    # Daten anzeigen
    # Spalten für horizontale Darstellung erstellen
    col1, col2 = st.columns(2)

    # Filter
    filters = {
        'Titel': st.sidebar.selectbox('Titel', [''] + list(get_data()['Titel'].unique()), key='selection'),
        'Autor': st.sidebar.selectbox('Autor', [''] + list(get_data()['Autor'].unique()), key='selection_autor'),
        'Genre': st.sidebar.selectbox('Genre', [''] + list(get_data()['Genre'].unique()), key='selection_genre'),
        'Jahr': st.sidebar.selectbox('Jahr', [''] + list(get_data()['Jahr'].unique()), key='selection_jahr'),
        'Altersgruppe': st.sidebar.selectbox('Altersgruppe', [''] + list(get_data()['Altersgruppe'].unique()), key='selection_altersgruppe'),
        'Sprache': st.sidebar.selectbox('Sprache', [''] + list(get_data()['Sprache'].unique()), key='selection_sprache'),
        'Standort': st.sidebar.selectbox('Standort', [''] + list(get_data()['Standort'].unique()), key='selection_standort')
    }


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
                st.write(f"Alle deine Bücher sortiert nach {active_filter}.")
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


    with st.sidebar:
        # Reset-Button
        def reset():
            st.session_state.selection = ""
            st.session_state.selection_autor = ""
            st.session_state.selection_genre = ""
            st.session_state.selection_jahr = ""
            st.session_state.selection_altersgruppe = ""
            st.session_state.selection_sprache = ""
            st.session_state.selection_standort = ""

        st.button('Filter zurücksetzen', on_click=reset) 

        # About Me
        if st.button("About"):
            st.subheader("Bibothek Bücher-Tracking App")
            st.text("Built with Streamlit & ❤")
            '''
            By Max [Twitter](https://www.twitter.com/kick_ban_ignore) // [GitHub](https://github.com/kick-ban-ignore)
            '''
      

if __name__ == '__main__':
    app()
