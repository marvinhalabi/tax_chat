import os
import requests
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool
from pydantic import Field

# Load environment variables
load_dotenv()

# Get the API keys from environment variables
tavily_api_key = os.getenv("TAVILY_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not tavily_api_key:
    st.error("Tavily API key not found. Check your .env file.")
if not openai_api_key:
    st.error("OpenAI API key not found. Check your .env file.")

# Set up the OpenAI model
llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=openai_api_key)

# Define the search tool class
class SearchTool(BaseTool):
    name: str = Field(default="web-results", description="The name of the tool used for searching tax-related websites.")
    description: str = Field(default="This tool searches tax- and accounting related websites to provide reliable up-to-date answers.")

    def _run(self, query: str) -> dict:
        """Search specific Swedish finance-related websites using Tavily AI, return results and URLs used."""
        url = f"https://tavily.ai/search?q={query} site:skatteverket.se OR site:verksamt.se OR site:vismaspcs.se OR site:bolagsverket.se OR site:fortnox.se"

        try:
            response = requests.get(url, headers={"Authorization": f"Bearer {tavily_api_key}"})
            response.raise_for_status()
            data = response.json()

            # Print the API response to debug
            print(data)  # Add this line to inspect the response

            results = [
                {'title': result.get('title', 'No title'), 'url': result.get('url', 'No URL')}
                for result in data.get('results', [])
            ]
            return {'results': results} if results else {'results': [{'title': 'Inga resultat', 'url': ''}]}
        
        except requests.exceptions.RequestException as e:
            return {"error": f"Error fetching search results: {str(e)}"}
        
# Define the answer generator class
class AnswerGenerator:
    def __init__(self, llm):
        self.llm = llm

    def generate_answer(self, question: str, search_results: dict) -> str:
        """Genererar ett svar från OpenAI baserat på sökresultat och kontrollerar att URL:er är giltiga."""

        urls = [
    result['url'] 
    for result in search_results.get('results', []) 
    if 'url' in result and result['url'].startswith('http')
    ]

        # Here we implement the detailed prompt with research_summary and question
        research_summary = f"Sökresultat:\n{search_results}\n"
        prompt = (
            f'"{research_summary}" '
            f"""
            Using the above information, answer the following question or topic: "{question}" 
            in a detailed report — The report should focus on the answer to the question, 
            should be well structured, informative, in depth, with facts and numbers if available, 
            a minimum of 1000 words and with markdown syntax and APA format. 
            Write all the valid, correct page source URLs at the end of the report in APA format. 
            You should write your report only based on the given information and nothing else.
            """
        )
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            final_answer = f"{response.content}"
            
            # Skapa en sektion för källor endast om URL:er finns och är giltiga
            source_section = "Källor för Mer Information:\n" + "\n".join(urls[:5]) if urls else ""
            return f"{final_answer}\n\n{source_section}"

        except Exception as e:
            return f"Fel vid generering av svar: {str(e)}"

# Initialize tools
search_tool = SearchTool()  # Initialize the search tool
answer_generator = AnswerGenerator(llm)  # Pass llm to the generator

# Streamlit app
def main():
    st.set_page_config(page_title="Fråga om Redovisning", layout="centered", page_icon=":moneybag:")

    if "generated" not in st.session_state:
        st.session_state["generated"] = []
    if "past" not in st.session_state:
        st.session_state["past"] = []

    st.header("Fråga om Redovisning :moneybag:")

    # Display chat history
    chat_history_placeholder = st.empty()
    with chat_history_placeholder.container():
        for i in range(len(st.session_state['generated'])):
            with st.chat_message("user"):
                st.markdown(st.session_state['past'][i])
            with st.chat_message("assistant"):
                st.markdown(st.session_state['generated'][i], unsafe_allow_html=True)

    # Get user input
    user_input = st.chat_input("Ställ din fråga om redovisning eller skatt här...")
    
    if user_input:
        # Immediately show user input
        st.session_state.past.append(user_input)
        with chat_history_placeholder.container():
            with st.chat_message("user"):
                st.markdown(user_input)

        # Perform search using the query
        search_results = search_tool._run(user_input)

        # Generate the AI's answer
        answer = answer_generator.generate_answer(user_input, search_results)

        st.session_state.generated.append(answer)

        # Refresh the chat history with the new message
        with chat_history_placeholder.container():
            for i in range(len(st.session_state['generated'])):
                with st.chat_message("user"):
                    st.markdown(st.session_state['past'][i])
                with st.chat_message("assistant"):
                    st.markdown(st.session_state['generated'][i], unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()
