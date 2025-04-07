import streamlit as st
import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic.claude import Claude
from agno.models.google import Gemini
from agno.models.openrouter import OpenRouter
#from agno.tools.thinking import ThinkingTools
import requests
import asyncio
import json
from textwrap import dedent
from datetime import datetime
import re

# Configure page
st.set_page_config(
    page_title="Dark Web Monitor",
    page_icon="🕵️",
    layout="wide"
)

# Define search engines with categories
SEARCH_ENGINES = {
    "Search Engines": {
        "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/": "Ahmia Search",
        "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/": "Torch Search",
        "http://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion": "DuckDuckGo"
    },
    "News & Information": {
        "https://www.bbcnewsd73hkzno2ini43t4gblxvycyac5aw4gnv7t2rccijh7745uqd.onion/": "BBC News",
        "http://ciadotgov4sjwlzihbbgxnqg3xiyrg7so2r2o3lt5wz5ypk4sxyjstad.onion/": "CIA",
        "http://p53lf57qovyuvwsc6xnrppyply3vtqm7l6pcobkmyqsiofyeznfu5uqd.onion/": "ProPublica"
    },
    "Special Services": {
        "http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/wiki/index.php/Main_Page": "Hidden Wiki",
        "http://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion/": "SecureDrop",
        "http://darkzzx4avcsuofgfez5zq75cqc4mprjvfqywo45dfcaxrwqg6qrlfid.onion/": "Darknetlive"
    }
}

# Flatten search engines for processing
FLAT_ENGINES = {url: name for category in SEARCH_ENGINES.values() for url, name in category.items()}

class DarkWebSearchTool:
    async def execute(self, organization: str):
        results = {"_summary": {"total_sources": len(FLAT_ENGINES)}}
        scan_status = {"success": [], "pending": list(FLAT_ENGINES.values()), "failed": []}
        
        with st.container():
            st.markdown("""
            <style>
            .status-success { color: #00CC00; }
            .status-pending { color: #808080; }
            .status-error { color: #FF4B4B; }
            </style>
            ### 🔍 Scan Status
            """, unsafe_allow_html=True)
            
            cols = st.columns(3)
            progress_bar = st.progress(0)
            
            for idx, (url, engine_name) in enumerate(FLAT_ENGINES.items()):
                progress_bar.progress((idx + 1) / len(FLAT_ENGINES))
                scan_status["pending"].remove(engine_name)
                
                try:
                    response = requests.get(
                        f"{url}{'?q=' + organization if 'search' in url else ''}", 
                        proxies={'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        found = organization.lower() in response.text.lower()
                        scan_status["success"].append(engine_name)
                        results[url] = {"found": found, "status": "Found mention" if found else "No mention found", "engine_name": engine_name}
                    else:
                        scan_status["failed"].append(engine_name)
                        results[url] = {"found": False, "status": f"Failed (Status: {response.status_code})", "engine_name": engine_name}
                except Exception as e:
                    scan_status["failed"].append(engine_name)
                    results[url] = {"found": False, "status": f"Error: {str(e)}", "engine_name": engine_name}
                
                # Update status columns
                for col, (status, title, style) in zip(cols, [
                    (scan_status["success"], "✅ Successful", "success"),
                    (scan_status["pending"], "⏳ Pending", "pending"),
                    (scan_status["failed"], "❌ Failed", "error")
                ]):
                    with col:
                        st.markdown(f"**{title}**")
                        for name in status:
                            st.markdown(f'<p class="status-{style}">• {name}</p>', unsafe_allow_html=True)
            
            # Summary metrics
            st.markdown("---")
            success_rate = (len(scan_status["success"]) / len(FLAT_ENGINES)) * 100
            for col, (title, value) in zip(st.columns(3), [
                ("Successfully Scanned", len(scan_status["success"])),
                ("Failed Scans", len(scan_status["failed"])),
                ("Success Rate", f"{success_rate:.1f}%")
            ]):
                with col:
                    st.metric(title, value)
        
        # Update summary
        results["_summary"].update({
            "sources_with_mentions": sum(1 for r in results.values() if isinstance(r, dict) and r.get("found", False)),
            "successful_scans": len(scan_status["success"]),
            "failed_scans": len(scan_status["failed"]),
            "success_rate": f"{success_rate:.1f}%"
        })
        
        return results

def analyze_results(results: str) -> str:
    """Analyze dark web search results.
    
    Args:
        results (str): JSON string of search results
        
    Returns:
        str: Analysis report in markdown format
    """
    data = json.loads(results)
    summary = data.get('_summary', {})
    
    # Generate detailed markdown report
    report = [
        f"# Dark Web Analysis Report\n",
        "## Summary of Findings\n"
    ]
    
    # Add summary statistics
    total_sources = summary.get('total_sources', 0)
    found_count = summary.get('sources_with_mentions', 0)
    error_count = summary.get('error_count', 0)
    success_rate = summary.get('success_rate', '0%')
    
    report.extend([
        f"Out of {total_sources} monitored sources:",
        f"- Found mentions in: {found_count} sources",
        f"- Successful searches: {success_rate}",
        f"- Failed/Error searches: {error_count}\n"
    ])
    
    # Risk Assessment
    risk_level = "HIGH" if found_count > 5 else "MEDIUM" if found_count > 2 else "LOW"
    report.extend([
        "## Risk Assessment\n",
        f"Current risk level: **{risk_level}**\n",
        "Factors considered:",
        "- Number of sources with mentions",
        "- Accessibility of sources",
        "- Search success rate\n"
    ])
    
    # Detailed Analysis
    report.append("## Detailed Analysis\n")
    for engine, details in data.items():
        if engine != '_summary':
            status = details.get('status', 'Unknown')
            found = "✅ Mention found" if details.get('found', False) else "❌ No mention found"
            
            report.append(f"### {engine}")
            report.append(f"- Status: {status}")
            report.append(f"- Result: {found}")
            if 'error' in details:
                report.append(f"- Error details: {details['error'][:100]}...")
            report.append("")
    
    # Recommendations
    report.extend([
        "## Recommendations\n",
        "Based on the analysis, we recommend:",
        "1. Continue regular monitoring of dark web sources",
        f"2. {'Immediate security audit' if risk_level == 'HIGH' else 'Regular security assessment' if risk_level == 'MEDIUM' else 'Maintain current security measures'}",
        "3. Keep monitoring for changes in risk levels",
        "4. Document and investigate any new mentions found\n"
    ])
    
    return "\n".join(report)

def main():
    # Global styles
    st.markdown("""
    <style>
    .title { font-size: 2.5rem; color: #1E88E5; text-align: center; padding: 1rem; margin-bottom: 2rem; }
    .warning-box { background-color: #FF4B4B20; color: #FF4B4B; padding: 1rem; border: 1px solid #FF4B4B; text-align: center; margin: 1rem 0; }
    .source-box { background-color: #1E1E1E10; padding: 0.5rem; margin: 0.2rem 0; }
    .stats-box { background-color: #F0F2F6; padding: 1rem; margin: 1rem 0; }
    .footer { position: fixed; bottom: 0; left: 0; right: 0; background-color: white; padding: 1rem; text-align: center; border-top: 1px solid #E0E0E0; }
    </style>
    <div class="title">🕵️ Dark Web Monitor</div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("""<div class="warning-box">⚠️ <strong>EDUCATIONAL USE ONLY</strong> ⚠️<br>
        Monitor dark web sources responsibly.<br>Ensure compliance with applicable laws.</div>""", unsafe_allow_html=True)
        
        st.divider()
        model_option = st.selectbox("Select LLM Provider", 
            ["OpenRouter (Llama)", "OpenAI GPT-4", "Anthropic Claude 3", "Google Gemini Pro"],
            help="Choose your preferred language model"
        )
        api_key = st.text_input("API Key", type="password", help="Enter your API key")
        
        st.divider()
        st.markdown("### 📡 Monitored Sources")
        for category, sources in SEARCH_ENGINES.items():
            with st.expander(category):
                for name in sources.values():
                    st.markdown(f"""<div class="source-box">🔹 {name}</div>""", unsafe_allow_html=True)
    
    # Main content
    org_name = st.text_input("Organization Name [Just the name]", placeholder="e.g., Facebook", key="org_name_input")
    _, btn_col, _ = st.columns([2, 1, 2])
    search_button = btn_col.button("🔍 Start Search", type="primary", use_container_width=True)

    if search_button and org_name and api_key:
        try:
            # Initialize model based on selection
            model_map = {
                "OpenRouter (Llama)": lambda: OpenRouter(api_key=api_key, id="meta-llama/llama-4-maverick:free"),
                "OpenAI GPT-4": lambda: OpenAIChat(api_key=api_key, id="gpt-4-turbo-preview"),
                "Anthropic Claude 3": lambda: Claude(api_key=api_key, id="claude-3-sonnet-20240229"),
                "Google Gemini Pro": lambda: Gemini(api_key=api_key, id="gemini-pro")
            }
            
            agent = Agent(
                model=model_map[model_option](),
                tools=[DarkWebSearchTool()],
                reasoning=True,
                role="Dark web search agent for educational purposes",
                instructions=f"""Search for mentions of {org_name} across dark web URLs.
                Categorize findings into:
                1. Data Breaches (dumps, leaks, reports)
                2. Credential Leaks (passwords, login info)
                3. Discussions and Mentions (forums, context)
                
                For each finding, provide:
                - Source URL
                - Category
                - Context summary
                - Relevant details
                
                Search URLs: {', '.join(FLAT_ENGINES.keys())}"""
            )
            
            with st.spinner("🔍 Searching..."):
                result = agent.run(org_name)
            
            # Store stats
            st.session_state.last_search = {
                'sources_checked': len(FLAT_ENGINES),
                'mentions_found': result.content.lower().count('found mention'),
                'timestamp': datetime.now()
            }
            
            # Display results
            st.markdown("### 📊 Analysis Results")
            
            # Show key metrics in a single row
            mentions = result.content.lower().count('found mention')
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Sources Checked", len(FLAT_ENGINES))
            with col2:
                # Count unique URLs that appear in the results
                found_urls = set(url for url in FLAT_ENGINES.keys() if url in result.content)
                successful = len(found_urls)
                st.metric("Successfully Connected", f"{successful}/{len(FLAT_ENGINES)}")
            
            st.markdown("---")
            
            # Show detailed findings
            st.markdown("#### 📑 Detailed Findings")
            st.markdown(result.content)
            
            # Download button
            st.download_button(
                "📥 Download Full Report",
                f"""# Dark Web Analysis Report for {org_name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Organization: {org_name}
- Total Sources: {len(FLAT_ENGINES)}
- Successfully Connected: {successful}/{len(FLAT_ENGINES)}

## Detailed Findings
{result.content}""",
                f"dark_web_analysis_{org_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                "text/markdown"
            )
            
        except Exception as e:
            st.error(f"🚫 Error: {str(e)}")
            st.error("Please ensure Tor service is running on port 9050")
    elif search_button:
        st.warning("⚠️ Please enter both organization name and API key")
    
    # Footer
    st.markdown("""<div class="footer">Made for cybersecurity research | 
    <a href='https://github.com/shadsidd/DarkWeb-Monitoring</a></div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main() 
