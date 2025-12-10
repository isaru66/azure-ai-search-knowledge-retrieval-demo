# save as download_set100_factsheets.py
import os
import time
import csv
from playwright.sync_api import sync_playwright

# 1. Step — get SET100 constituents from CSV file
SET100_CSV_FILE = "SET100_tickers.csv"

def get_set100_tickers():
    """Read SET100 constituent ticker symbols from CSV file"""
    tickers = []
    
    # Read the CSV file
    with open(SET100_CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            symbol = row['Ticker Symbol'].strip()
            if symbol:
                tickers.append(symbol)
    
    if not tickers:
        raise RuntimeError("Could not extract tickers from CSV file")
    
    return tickers

# 2. Step — for each ticker, generate PDF of factsheet using Playwright
FACTSHEET_URL_TEMPLATE = "https://www.set.or.th/th/market/product/stock/quote/{symbol}/factsheet"

def download_factsheet(symbol, dest_folder="factsheets"):
    """Generate PDF of factsheet using Playwright"""
    url = FACTSHEET_URL_TEMPLATE.format(symbol=symbol)
    os.makedirs(dest_folder, exist_ok=True)
    pdf_path = os.path.join(dest_folder, f"{symbol}.pdf")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navigate to the page
            page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Wait a bit for dynamic content to load
            page.wait_for_timeout(2000)
            
            # Generate PDF
            page.pdf(path=pdf_path, format="A4", print_background=True)
            
            browser.close()
            
        print(f"[OK] {symbol}: saved factsheet to {pdf_path}")
    except Exception as e:
        print(f"[ERROR] {symbol}: Failed to generate PDF - {str(e)}")

if __name__ == "__main__":
    tickers = get_set100_tickers()
    print(f"Found {len(tickers)} tickers in SET100")
    # optionally inspect list:
    # print(tickers)

    for sym in tickers:
        download_factsheet(sym)
        time.sleep(0.5)  # be gentle to the server
