# Fråga om Redovisning 💰

En interaktiv Streamlit-app för att ställa frågor om skatt och redovisning, som använder Tavily API och OpenAI:s GPT-4 för att ge svar baserat på aktuella och pålitliga källor.

## Funktioner

- 🔍 Sökning av information från svenska skatte- och redovisningswebbplatser.
- 🧠 Generering av detaljerade svar från AI baserat på sökresultat.
- 💬 Användarvänligt gränssnitt med chatthistorik.

## Installation

Följ dessa steg för att köra appen lokalt:

1. **Klona repositoryt**:
   Öppna CMD och kör följande kommando för att klona repositoryt:

   ```bash
   git clone https://github.com/marvinhalabi/tax_chat.git
   cd tax_chat
   ```

2. **Installera Python 🐍**:
   Se till att du har Python installerat på din dator. Du kan ladda ner det från [python.org](https://www.python.org/downloads/). Under installationen, se till att kryssa i alternativet "Add Python to PATH".

3. **Skapa en virtuell miljö (valfritt men rekommenderat)**:
   För att isolera dina projektberoenden kan du skapa en virtuell miljö:

   ```bash
   python -m venv venv
   ```

   Aktivera den virtuella miljön:

   - För Windows:
     ```bash
     venv\Scripts\activate
     ```

   - För macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Installera krav**:
   Installera nödvändiga paket med `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

5. **Skapa en `.env`-fil**:
   Skapa en `.env`-fil i projektmappen och lägg till dina API-nycklar:

   ```plaintext
   TAVILY_API_KEY=din_nyckel
   OPENAI_API_KEY=din_nyckel
   ```

   Se till att ersätta `din_nyckel` med dina faktiska API-nycklar 🔑

## Användning 🌟

   För att starta appen, kör följande kommando i CMD:

   ```bash
   streamlit run app.py
   ```
