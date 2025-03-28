from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_amazon_price(product):
    """Fetch product price from Amazon"""
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=webdriver.ChromeService(ChromeDriverManager().install()), options=options)
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--no-sandbox")    # Bypass OS security model  
    driver.get("https://www.amazon.in/")
    
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys(product + Keys.RETURN)
    
    time.sleep(3)  # Allow page to load

    try:
        price = driver.find_element(By.CLASS_NAME, "a-price-whole").text
        print(f"Amazon price for {product}: ₹{price}")
    except:
        print("Amazon: Price not found.")
        price = None

    driver.quit()
    return price

def get_flipkart_price(product):
    """Fetch product price from Flipkart"""
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=webdriver.ChromeService(ChromeDriverManager().install()), options=options)
    driver.get("https://www.flipkart.com/")

    try:
        close_popup = driver.find_element(By.XPATH, "//button[contains(text(),'✕')]")
        close_popup.click()
    except:
        pass  # No popup found

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(product + Keys.RETURN)

    time.sleep(3)  # Allow page to load

    try:
        price = driver.find_element(By.CLASS_NAME, "_30jeq3").text.replace("₹", "").replace(",", "")
        print(f"Flipkart price for {product}: ₹{price}")
    except:
        print("Flipkart: Price not found.")
        price = None

    driver.quit()
    return price

def best_deal(product):
    """Compare prices and direct to the best deal"""
    amazon_price = get_amazon_price(product)
    flipkart_price = get_flipkart_price(product)

    if amazon_price and flipkart_price:
        amazon_price = int(amazon_price)
        flipkart_price = int(flipkart_price)

        if amazon_price < flipkart_price:
            print(f"Best deal for {product} is on Amazon at ₹{amazon_price}. Opening Amazon...")
            url = "https://www.amazon.in/s?k=" + product.replace(" ", "+")
        else:
            print(f"Best deal for {product} is on Flipkart at ₹{flipkart_price}. Opening Flipkart...")
            url = "https://www.flipkart.com/search?q=" + product.replace(" ", "%20")

    elif amazon_price:
        print(f"Only Amazon has the price. Opening Amazon at ₹{amazon_price}...")
        url = "https://www.amazon.in/s?k=" + product.replace(" ", "+")
    elif flipkart_price:
        print(f"Only Flipkart has the price. Opening Flipkart at ₹{flipkart_price}...")
        url = "https://www.flipkart.com/search?q=" + product.replace(" ", "%20")
    else:
        print("No prices found.")
        return

    # Open the best website
    import webbrowser
    webbrowser.open(url)
