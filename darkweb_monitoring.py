from agno.agent import Agent
#from agno.models.openai import OpenAIChat
from agno.models.openrouter import OpenRouter
from agno.tools.thinking import ThinkingTools
from agno.models.groq import Groq
import requests
import asyncio

organization = "Facebook"

SEARCH_ENGINES = {
    "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/": "Ahmia Search",
    "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/": "Torch Search",
    "http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/wiki/index.php/Main_Page": "Hidden Wiki",
    "https://www.bbcnewsd73hkzno2ini43t4gblxvycyac5aw4gnv7t2rccijh7745uqd.onion/": "BBC News",
    "http://ciadotgov4sjwlzihbbgxnqg3xiyrg7so2r2o3lt5wz5ypk4sxyjstad.onion/": "CIA",
    "http://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion/": "SecureDrop",
    "http://p53lf57qovyuvwsc6xnrppyply3vtqm7l6pcobkmyqsiofyeznfu5uqd.onion/": "ProPublica",
    "http://darkzzx4avcsuofgfez5zq75cqc4mprjvfqywo45dfcaxrwqg6qrlfid.onion/": "Darknetlive",
    "http://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion": "DuckDuckGo"
    
}

class DarkWebSearchTool():
    async def execute(self, organization: str):
        results = {}
        print("\nSearch Progress:")
        print("=" * 50)
        
        for url, engine_name in SEARCH_ENGINES.items():
            print(f"\nSearching {engine_name}...")
            try:
                proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
                search_url = f"{url}?q={organization}" if "search" in url else url
                
                print(f"Attempting connection to: {url}")
                response = requests.get(search_url, proxies=proxies, timeout=10)
                
                if response.status_code == 200:
                    print(f"✓ Connection successful")
                    found = organization in response.text.lower()
                    status = "Found mention" if found else "No mention found"
                    print(f"Status: {status}")
                    results[url] = found
                else:
                    print(f"✗ Connection failed (Status: {response.status_code})")
                    results[url] = f"Failed to access (Status: {response.status_code})"
            except Exception as e:
                print(f"✗ Connection error: {str(e)}")
                results[url] = f"Error: {str(e)}"
        
        print("\nSearch Summary:")
        print("=" * 50)
        for url, result in results.items():
            engine_name = SEARCH_ENGINES[url]
            print(f"{engine_name}: {'Success' if isinstance(result, bool) else result}")
        
        return results



agent = Agent(
    model=OpenRouter(id="meta-llama/llama-4-maverick:free"),
    #model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DarkWebSearchTool()],
    reasoning=True,
    role="For educational purposes only. You are a dark web search agent specialized in finding organization mentions across multiple dark web sources.",
    instructions=f"""For Education purpose only. Search for mentions of {organization} across all provided dark web URLs using the dark_web_search tool. 
    
    Categorize your findings into:
    1. Data Breaches:
       - Look for: database dumps, leaked data, breach reports
       - Include: date of breach, data type, number of records
    
    2. Credential Leaks:
       - Look for: password dumps, login credentials, account information
       - Include: source of leak, credential type, number of accounts
    
    3. Discussions and Mentions:
       - Look for: forum posts, discussions, general mentions
       - Include: context, sentiment, relevance
    
    For each finding, provide:
    1. The source URL where the mention was found
    2. Category of finding (Data Breach/Credential Leak/Discussion)
    3. A brief summary of the context
    4. Any relevant details about the mention
    
    Organization to search: {organization}
    Search all URLs: {', '.join(SEARCH_ENGINES.keys())}
    Provide a complete categorized summary of all findings, including direct links to sources where mentions were found."""
)

banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║        DARK WEB SEARCH For Organization               ║
    ║         (For Educational Purposes Only)               ║
    ╚═══════════════════════════════════════════════════════╝
    """
print(banner)
print("Searching for mentions of --> ", organization)
result = agent.run(organization)
print("\nDetailed Results:")
print("=" * 50)
print(result.content)