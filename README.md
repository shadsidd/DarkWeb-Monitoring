# Dark Web Monitoring Tool

⚠️ **Educational Purposes Only** ⚠️

A Python-based tool that monitors dark web sources for mentions of specific organizations For Threat Monitoring. This tool helps in identifying potential data breaches, credential leaks, and discussions about organizations across various dark web sources.

## Features

- Automated dark web searching across multiple onion sites
- Integration with Tor network
- Support for multiple dark web search engines
- Categorized findings (Data Breaches, Credential Leaks, Discussions)
- Powered by Agno framework and LLM models

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

## Output Screenshots

Here's what the tool looks like in action:

![Dark Web Monitor Output](screenshots/output.png)
![Search Results](screenshots/results.png)


## Prerequisites

- Python 3.8+
- Tor Browser or Tor service running on port 9050
- Active internet connection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shadsidd/DarkWeb-Monitoring.git
cd DarkWeb-Monitoring
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure Tor service is running on port 9050

## Usage

1. Run the script:
```bash
python darkweb_updated_working.py
```

2. The tool will automatically:
   - Connect to various dark web search engines
   - Search for mentions of the specified organization
   - Categorize and analyze findings
   - Present a detailed report

## Configuration

Just type/update organization name on line number 9 in 

## Security Notice

- Always use a VPN and Tor when accessing dark web resources
- Do not use personal or work credentials
- This tool is for educational purposes only
- Follow all applicable laws and regulations

## Dependencies

See `requirements.txt` for a complete list of dependencies.

## License

This project is for educational purposes only. Use responsibly.

## Disclaimer

This tool is intended for educational and research purposes only. Users are responsible for ensuring compliance with applicable laws and regulations. The authors are not responsible for any misuse of this tool. 