"""
Extract ticker symbols from SET100.html and save to CSV file
"""
import re
import csv
from pathlib import Path

def extract_ticker_symbols(html_file):
    """Extract unique ticker symbols from HTML file"""
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all data-symbol attributes using regex
    # Pattern: data-symbol="TICKER"
    pattern = r'data-symbol="([A-Z0-9]+)"'
    matches = re.findall(pattern, content)
    
    # Get unique symbols and sort them
    unique_symbols = sorted(set(matches))
    
    return unique_symbols

def save_to_csv(symbols, output_file):
    """Save ticker symbols to CSV file"""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['Ticker Symbol'])
        # Write each symbol
        for symbol in symbols:
            writer.writerow([symbol])
    
    print(f"✅ Saved {len(symbols)} ticker symbols to {output_file}")

def main():
    # Define file paths
    script_dir = Path(__file__).parent
    html_file = script_dir / 'SET100.html'
    output_file = script_dir / 'SET100_tickers.csv'
    
    # Check if HTML file exists
    if not html_file.exists():
        print(f"❌ Error: {html_file} not found!")
        return
    
    print(f"📖 Reading {html_file}...")
    
    # Extract ticker symbols
    symbols = extract_ticker_symbols(html_file)
    
    print(f"✨ Found {len(symbols)} unique ticker symbols")
    print(f"📝 First 10 symbols: {', '.join(symbols[:10])}")
    
    # Save to CSV
    save_to_csv(symbols, output_file)
    
    print(f"\n📊 Summary:")
    print(f"   Total symbols: {len(symbols)}")
    print(f"   Output file: {output_file}")

if __name__ == '__main__':
    main()
