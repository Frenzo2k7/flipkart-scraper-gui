import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import tkinter as tk
from tkinter import scrolledtext

def get_html(search_query):
    url = f"https://www.flipkart.com/search?q={quote(search_query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all("a", class_="CGtC98")
    clothing_layout = False

    if not products:
        products = soup.find_all("a", class_="_2rpwqI")  
        clothing_layout = True

    result_text = ""
    if not products:
        return "❌ No products found or page structure changed.\n"

    for product in products[:5]:
        if clothing_layout:
            title = product.find("div", class_="_2WkVRV")
            description = product.find("a", class_="IRpwTa")
            price = product.find("div", class_="_30jeq3")
            rating = product.find("div", class_="_3LWZlK")
        else:
            title = product.find("div", class_="KzDlHZ")
            description = title
            price = product.find("div", class_="Nx9bqj")
            rating = product.find("div", class_="XQDdHH")

        result_text += f"📦 Title: {(title or description).text.strip() if (title or description) else 'N/A'}\n"
        result_text += f"💰 Price: {price.text.strip() if price else 'N/A'}\n"
        result_text += f"⭐ Rating: {rating.text.strip() if rating else 'N/A'}\n"
        result_text += "-" * 40 + "\n"

    return result_text

def search_products():
    query = entry.get()
    if not query.strip():
        result_box.delete('1.0', tk.END)
        result_box.insert(tk.END, "⚠️ Please enter a product name.\n")
        return

    html = get_html(query)
    if html:
        result = parse_html(html)
        result_box.delete('1.0', tk.END)
        result_box.insert(tk.END, result)
    else:
        result_box.delete('1.0', tk.END)
        result_box.insert(tk.END, "❌ Failed to fetch data. Try again later.\n")

root = tk.Tk()
root.title("Flipkart Product Scraper")
root.geometry("600x400")

tk.Label(root, text="Enter Product to Search:", font=("Arial", 12)).pack(pady=10)

entry = tk.Entry(root, font=("Arial", 12), width=40)
entry.bind("<Return>", lambda e: search_products())
entry.pack()

tk.Button(root, text="Search", font=("Arial", 12), command=search_products).pack(pady=10)

result_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 10))
result_box.pack(expand=True, fill='both', padx=10, pady=10)

root.mainloop()
