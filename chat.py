import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Get the API keys from environment variables
tavily_api_key = os.getenv("TAVILY_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not tavily_api_key:
    raise ValueError("Tavily API key not found. Check your .env file.")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Check your .env file.")

# Initialize the LangChain ChatOpenAI model with gpt-4o-mini
llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=openai_api_key)

# Ensure UTF-8 encoding support
import sys
sys.stdout.reconfigure(encoding='utf-8')

class SearchTool:
    def _run(self, query: str) -> dict:
        """Search specific Swedish finance-related websites using Tavily AI and return results."""
        tavily_client = TavilyClient(api_key=tavily_api_key)

        # Modify the query to focus on Swedish tax/finance websites
        query = f"{query} site:skatteverket.se OR site:verksamt.se OR site:vismaspcs.se OR site:bolagsverket.se OR site:fortnox.se"

        try:
            response = tavily_client.search(query=query)

            results = []
            for result in response.get('results', []):
                title = result.get('title', 'No title')
                url = result.get('url', 'No URL')
                results.append({'title': title, 'url': url})

            return {
                'results': results,
                'query': query,
                'follow_up_questions': None,
            }
        except Exception as e:
            return {"error": f"Error fetching search results: {str(e)}"}
        
class AnswerGenerator:
    def __init__(self, llm):
        self.llm = llm

    def generate_answer(self, question: str, search_results: dict) -> str:
        """Generates an answer from OpenAI based on search results, including the URL."""
        
        # Extract URLs from the search results
        urls = [result['url'] for result in search_results.get('results', []) if 'url' in result]

        # Prepare the prompt for the LLM to answer the question
        prompt = (
            f"Fråga: {question}\n"
            f"Sökresultat:\n{search_results}\n\n"
            f"Baserat på sökresultaten, ge ett detaljerat svar om ämnet på svenska utan att inkludera källor."
        )

        try:
            # Use OpenAI to generate the answer in Swedish
            response = self.llm.invoke([HumanMessage(content=prompt)])

            # Create the final answer, including only the last sources
            source_list = "\n".join(urls) if urls else "Inga relevanta URL:er hittades."
            final_answer = f"{response.content}\n\nKällor:\n{source_list}"  # Only list sources at the end
            return final_answer
        except Exception as e:
            return f"Fel vid generering av svar: {str(e)}"
        


# Initialize tools
search_tool = SearchTool()
answer_generator = AnswerGenerator(llm)

def main():
    print("You can now chat with the agent. Type 'exit' to end the conversation.")
    while True:
        user_input = input("\nYou: ")  # Added a blank line for better readability
        if user_input.lower() == 'exit':
            break
        
        # Run search and generate response
        search_results = search_tool._run(user_input)
        answer = answer_generator.generate_answer(user_input, search_results)
        
        # Print the final AI answer with spacing
        print(f"\nAI: {answer}")  # Added a blank line for better readability

if __name__ == "__main__":
    main()
