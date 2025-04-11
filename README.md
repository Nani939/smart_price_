# smart_price
# Price Comparison Bot

## Overview
This Python project is a web scraper that compares product prices from Amazon and Flipkart. It automates the search process and fetches the latest prices to help users find the best deal.

## Features
- **Automated Price Scraping**: Uses Selenium to fetch product prices from Amazon and Flipkart.
- **Best Deal Finder**: Compares prices and directs users to the cheaper platform.
- **User Input**: Allows users to enter the product name and get real-time price comparisons.
- **WebDriver Management**: Uses `webdriver-manager` to handle ChromeDriver installation.

## Technologies Used
- Python
- Selenium
- WebDriver Manager

## Installation
Ensure you have Python installed, then install the required dependencies:
```bash
pip install selenium webdriver-manager
```

## Usage
Run the script and enter the product name:
```bash
python compare.py
```
The script will fetch the prices and suggest the best deal.

## Project Structure
```
price_comparison/
│── templates/
        │──index.html
        │──result.html
│── app.py      #backend part search the given product in amazon and flipcart.
│── README.md   # Project documentation
```

## How It Works
1. **Searches the Product**: Uses Selenium to navigate to Amazon and Flipkart.
2. **Extracts Prices**: Scrapes the price from each platform.
3. **Compares Prices**: Determines the cheaper option and prints the result.

## Example Output
```
Enter the product name: iPhone 15
Amazon Price: ₹74,999
Flipkart Price: ₹73,499
Best Deal: Flipkart
```

## Issues and Improvements
- The project may break if the website structure changes.
- Could be improved by adding more e-commerce platforms.

## Contributing
Feel free to fork and improve this project!

## License
This project is licensed under the MIT License.

