# Fråga om Redovisning 💰

## Beskrivning
"Fråga om Redovisning" är en interaktiv Streamlit-app som använder AI-teknologi från Tavily och OpenAI för att ge användare svar på frågor rörande skatt och redovisning. Genom att söka i pålitliga svenska källor ger appen användarna aktuella och noggranna svar.

## Funktioner
- Sökning på svenska skatte- och redovisningssidor.
- Generering av svar från OpenAI baserat på aktuella sökresultat.
- En användarvänlig chattgränssnitt för att ställa frågor och få svar.
- Dynamisk visning av chatthistorik.

## Krav
Innan du kör appen, se till att du har följande installerat:

- Python 3.7 eller högre
- [Streamlit](https://streamlit.io/)
- [dotenv](https://pypi.org/project/python-dotenv/)
- [requests](https://docs.python-requests.org/en/latest/)
- [langchain](https://pypi.org/project/langchain/)

Du kan installera nödvändiga paket genom att köra:

```bash
pip install -r requirements.txt
```

## Konfiguration
1. **Skapa en `.env`-fil** i roten av ditt projekt.
2. **Lägg till dina API-nycklar** i `.env`-filen:

   ```plaintext
   TAVILY_API_KEY=din_tavily_api_nyckel
   OPENAI_API_KEY=din_openai_api_nyckel
   ```

   *Ersätt `din_tavily_api_nyckel` och `din_openai_api_nyckel` med dina riktiga API-nycklar.*

## Kör appen
För att köra appen, använd följande kommando:

```bash
streamlit run app.py
```

Appen öppnas i din webbläsare, där du kan ställa frågor om redovisning eller skatt.
