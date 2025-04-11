from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)
def search_amazon(driver, product):
    driver.get("https://www.amazon.in")
    try:
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
        search_box.send_keys(product)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
        title = driver.find_element(By.CSS_SELECTOR, ".s-title-instructions-style span").text
        price = driver.find_element(By.CSS_SELECTOR, ".a-price-whole").text
        link = driver.find_element(By.CSS_SELECTOR, ".s-title-instructions-style a").get_attribute("href")
        return {"site": "Amazon", "title": title, "price": int(price.replace(",", "")), "link": link}
    except Exception as e:
        return {"site": "Amazon", "title": f"Error: {e}", "price": float('inf'), "link": "#"}
def search_flipkart(driver, product):
    driver.get("https://www.flipkart.com")
    time.sleep(2)
    try:
        close_popup = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'✕')]"))
        )
        close_popup.click()
    except:
        pass  # Popup might not show

    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(product)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        # Try common selectors
        titles = driver.find_elements(By.CSS_SELECTOR, "._4rR01T")
        prices = driver.find_elements(By.CSS_SELECTOR, "._30jeq3._1_WHN1")
        links = driver.find_elements(By.CSS_SELECTOR, "a._1fQZEK")

        if not titles or not prices or not links:
            raise Exception("No results found on Flipkart or layout changed.")

        title = titles[0].text
        price = prices[0].text
        link = links[0].get_attribute("href")

        return {
            "site": "Flipkart",
            "title": title,
            "price": int(price.replace("₹", "").replace(",", "")),
            "link": link,
        }
    except Exception as e:
        return {
            "site": "Flipkart",
            "title": f"Error: {e}",
            "price": float("inf"),
            "link": "#",
        }


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/compare", methods=["POST"])
def compare():
    product = request.form["product"]
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    amazon = search_amazon(driver, product)
    flipkart = search_flipkart(driver, product)
    driver.quit()
    best = amazon if amazon["price"] < flipkart["price"] else flipkart
    return render_template("result.html", best=best)

if __name__ == "__main__":
    app.run(debug=True)
