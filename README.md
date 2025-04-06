# Dark Web Monitor 🕵️

A tool for educational purposes to monitor dark web sources for organization mentions. This tool supports both a web-based UI and command-line interface.

⚠️ **Educational Use Only** - Monitor dark web sources responsibly and ensure compliance with applicable laws.

## Prerequisites

### 1. Tor (Required)
This tool REQUIRES Tor to function as it accesses .onion addresses. Without Tor, no searches will work.

Choose one of these options:
- **Option A: Tor Browser** (Recommended for beginners)
  1. Download [Tor Browser](https://www.torproject.org/download/)
  2. Install and launch it
  3. Keep it running while using this tool

- **Option B: Tor Service**
  - On macOS:
    ```bash
    brew install tor
    brew services start tor
    ```
  - On Linux:
    ```bash
    sudo apt install tor
    sudo systemctl start tor
    ```
  - On Windows:
    ```bash
    choco install tor
    ```

Verify Tor is working:
```bash
curl --socks5 127.0.0.1:9050 https://check.torproject.org/api/ip
```

### 2. Python Requirements
```bash
pip install -r requirements.txt
```

## Usage

### Web UI Mode (Streamlit)

1. Ensure Tor is running (required)
2. Start the web interface:
   ```bash
   streamlit run app.py
   ```
3. Access the UI in your browser (typically http://localhost:8501)
4. Enter your organization name and API key
5. Select your preferred LLM provider
6. Click "Start Search" to begin monitoring

### CLI Mode (darkweb_monitoring.py)

1. Ensure Tor is running (required)
2. Edit darkweb_monitoring.py to set your organization:
   ```python
   organization = "Your Organization Name"  # Change this line
   ```
3. Choose your LLM provider by uncommenting the appropriate model:
   ```python
   # Choose one of these:
   model=OpenRouter(id="meta-llama/llama-4-maverick:free")
   #model=Groq(id="llama-3.3-70b-versatile")
   ```
4. Run the script:
   ```bash
   python darkweb_monitoring.py
   ```

### Output
1. Web UI
![Screenshot 2025-04-06 at 9 40 07 PM](https://github.com/user-attachments/assets/67349242-6f0d-4278-99ee-a82285a7bf04)

2. CLI
![Screenshot 2025-04-06 at 3 58 10 PM](https://github.com/user-attachments/assets/2f48dcfb-6f38-43d6-b066-03ac16aa2f13)

The script will automatically:
- Search all configured dark web sources
- Show real-time progress for each source
- Display connection status
- Provide detailed findings in categories

## Features

- **Multiple Sources**: Searches across various dark web sources including:
  - Search Engines (Ahmia, Torch, DuckDuckGo)
  - News & Information (BBC, CIA, ProPublica)
  - Special Services (Hidden Wiki, SecureDrop, Darknetlive)

- **Comprehensive Analysis**:
  - Connection status tracking
  - Source accessibility checking
  - Detailed findings report
  - Downloadable results

- **LLM Provider Support In UI **:
  - OpenRouter (Llama)
  - OpenAI GPT-4
  - Anthropic Claude 3
  - Google Gemini Pro

## Security Notes

- Always use Tor for dark web access
- Keep API keys secure
- Review findings carefully
- Follow responsible disclosure practices

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

MIT License - See LICENSE file for details

## Features 🌟

- Dark web source monitoring
- Multiple LLM provider support (OpenAI, Anthropic Claude, Google Gemini)
- Real-time search progress tracking
- Risk assessment and analysis
- Security recommendations
- User-friendly Streamlit interface

## Currently Monitored Sites

The tool currently searches across the following dark web sources:

1. Ahmia Search Engine
2. Torch Search Engine
3. Hidden Wiki
4. BBC News
5. CIA Official Site
6. SecureDrop
7. ProPublica
8. Darknetlive
9. DuckDuckGo


## Dependencies

See `requirements.txt` for a complete list of dependencies.

## Security Notice

- Do not use personal or work credentials
- This tool is for educational purposes only
- Follow all applicable laws and regulations
- Keep your API keys secure and never share them

## Disclaimer

This tool is intended for educational and research purposes only. Users are responsible for ensuring compliance with applicable laws and regulations. The authors are not responsible for any misuse of this tool. 
