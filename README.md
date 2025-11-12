# python-scrape-bonbast

This project extracts dynamic currency data (EUR and USD rates) from bonbast.com using Playwright. It waits for JavaScript-rendered content to load before extracting the data.

## Requirements
- Python 3.8+
- Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Additionally, install Playwright browsers:

```bash
python -m playwright install
```

## Setting Up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies. Follow these steps:

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment:

- On macOS/Linux:

```bash
source .venv/bin/activate
```

- On Windows:

```bash
.venv\Scripts\activate
```

3. Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage
- Run the script to fetch data from bonbast.com:

```bash
python main.py
```

- The script will output EUR and USD sell/buy rates. Example:

```
EUR€ Sell: 58,000 Toman
EUR€ Buy: 57,500 Toman
USD$ Sell: 50,000 Toman
USD$ Buy: 49,500 Toman
```

- For debugging, the script can also extract the parent table of a specific element (e.g., `eur1`). Uncomment the relevant lines in `main.py` to enable this feature.
