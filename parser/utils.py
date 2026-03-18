import os
import json
import pprint
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs


class Product:
  def __init__(self):
    self.link       : str = ""
    self.name       : str = ""
    self.description: list[str] = []
    self.article    : str = ""
    self.is_in_stock: bool = True
    self.price      : int = 0
    self.new_price  : int | None = None
    self.features   : dict[str, str] = {}
    self.category   : str = ""
    self.accessories: list[str] | None = None

  def __str__(self):
    desc_str = pprint.pformat(self.description, indent=2, width=80, compact=False)
    features_str = pprint.pformat(self.features, indent=2, width=80, compact=False)
    accessories_str = pprint.pformat(self.accessories, indent=2, width=80, compact=False) if self.accessories else "None"

    return (
      f"Ссылка: {self.link}\n"
      f"Название: {self.name}\n"
      f"Описание: {desc_str}\n"
      f"Артикул: {self.article}\n"
      f"В наличии: {self.is_in_stock}\n"
      f"Цена: {self.price}\n"
      f"Новая цена: {self.new_price}\n"
      f"Характеристики: {features_str}\n"
      f"Категория: {self.category}\n"
      f"Аксессуары: {accessories_str}\n"
      + "-" * 40
    )
  

def get_products(soup: BeautifulSoup) -> list:
  products = soup.find_all(class_="product_content")

  return products

def get_links(products: list) -> list:
  links = []

  for product in products:
    a = product.find('a')

    if a and a.get('href'):
      links.append("https://drtechno.ru/" + a['href'])
  
  return links

def load_file(wait: WebDriverWait, driver: webdriver) -> None:
  with open("links.txt", "w") as file:
    page_number = 1

    while True:
      print(page_number)

      soup = BeautifulSoup(driver.page_source, "html.parser")
      products = get_products(soup)
      links = get_links(products)

      for link in links:
        file.write(link + '\n')
      
      try:
        next_btn = driver.find_element(By.LINK_TEXT, "далее")
        next_btn.click()
        page_number += 1
        # time.sleep(2)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product_content")))
      except:
        break

def load_json(wait: WebDriverWait, driver: webdriver) -> None:
    products: list[dict] = []
    successful_count = 0

    with open("db.json", "w", encoding="utf-8") as file, \
         open("logs.txt", "w", encoding="utf-8") as logs:

        links = [line.strip() for line in open("links.txt", "r").readlines() if line.strip()]

        for link in links:
            product = None
            try:
                driver.get(link)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product_content")))
                soup = BeautifulSoup(driver.page_source, "html.parser")

                product = Product()
                info = soup.find(class_="right_column")
                if not info:
                    raise ValueError("Не найден блок right_column")

                is_in_stock = True
                try:
                    fonts = soup.find_all('font')
                    green_circles = [font for font in fonts
                                     if font.get_text().strip() == '●' and font.get('color') == 'green']
                    is_in_stock = len(green_circles) > 0
                except Exception as e:
                    logs.write(f"Ошибка при проверке наличия для {link}: {e}\n")
                product.is_in_stock = is_in_stock

                name_tag = soup.find(class_="product_title")
                product.name = name_tag.get_text().strip() if name_tag else ""

                product.link = link

                description_full = info.find(class_="description_full")
                if description_full:
                    for p in description_full.find_all('p'):
                        text = p.get_text().replace("\n", " ").strip()
                        if text:
                            product.description.append(text)

                article_tag = info.find(class_="title")
                if article_tag:
                    p_tag = article_tag.find('p')
                    if p_tag:
                        raw_article = p_tag.get_text().replace("Арт.: ", "").strip()
                        product.article = raw_article

                try:
                    cost_info = info.find(class_="cost_info")
                    if cost_info:
                        ci_cost = cost_info.find(class_="ci_cost")
                        if ci_cost:
                            del_tag = ci_cost.find('del')
                            cost_tag = ci_cost.find(class_='cost')
                            if del_tag and cost_tag:
                                product.price = del_tag.get_text().strip()
                                product.new_price = cost_tag.get_text().strip()
                            elif cost_tag:
                                product.price = cost_tag.get_text().strip()
                except Exception as e:
                    logs.write(f"Ошибка при парсинге цены для {link}: {e}\n")

                try:
                    features_container = soup.find(class_="information_tabs")
                    if features_container:
                        listing = features_container.find(class_="listing")
                        if listing:
                            for feature in listing.find_all('li'):
                                feature_text = feature.get_text().strip()
                                if not feature_text:
                                    continue

                                if ':' not in feature_text:
                                    logs.write(f"Строка без ':' (пропущена): {feature_text} в {link}\n")
                                    continue

                                key, value = feature_text.split(':', 1)
                                key = key.strip()
                                value = value.strip()

                                if ';' in value:
                                    parts = [part.strip() for part in value.split(';') if part.strip()]
                                    if parts:
                                        product.features[key] = parts[0]
                                        for part in parts[1:]:
                                            if ':' in part:
                                                sub_key, sub_value = part.split(':', 1)
                                                product.features[sub_key.strip()] = sub_value.strip()
                                            else:
                                                logs.write(f"Необработанная часть характеристики (нет ':'): {part} в {link}\n")
                                else:
                                    product.features[key] = value

                except Exception as e:
                    logs.write(f"Ошибка при парсинге характеристик для {link}: {e}\n")

                try:
                    breadcrumbs = soup.find(class_="bradcrumbs redef_bc")
                    if breadcrumbs:
                        li_list = breadcrumbs.find_all('li')
                        if len(li_list) > 1:
                            product.category = li_list[1].get_text().strip()
                except Exception as e:
                    logs.write(f"Ошибка при парсинге категории для {link}: {e}\n")

                try:
                    slider = soup.find(class_="catalog_product_slider")
                    if slider:
                        items = slider.select('.catalog_list.jcarousel-list.jcarousel-list-horizontal li .product_title a')
                        if items:
                            product.accessories = ['https://drtechno.ru/' + a['href'] for a in items]
                except Exception as e:
                    logs.write(f"Ошибка при парсинге аксессуаров для {link}: {e}\n")

                products.append(product.__dict__)
                successful_count += 1
                print(f"Обработано: {successful_count} – {product.name}")

            except Exception as e:
                logs.write(f"Критическая ошибка по ссылке: {link}\n")
                logs.write(f"Ошибка: {e}\n\n")

        json.dump(products, file, ensure_ascii=False, indent=2)
        print(f"\nГотово. Успешно обработано: {successful_count} из {len(links)}")


def parse_images(wait: WebDriverWait, driver: webdriver) -> None:
    os.makedirs("images", exist_ok=True)
    
    links = [line.strip() for line in open("links.txt", "r").readlines() if line.strip()]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for link in links:
        driver.get(link)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product_content")))
        soup = BeautifulSoup(driver.page_source, "html.parser")

        photos = soup.select(".mini_slider2 ul li a")
        
        parsed = urlparse(link)
        product_id = parse_qs(parsed.query).get('Id', ['unknown'])[0]
        product_dir = os.path.join("images", product_id)
        os.makedirs(product_dir, exist_ok=True)

        for idx, photo in enumerate(photos, start=1):
            href = photo.get('href')
            if not href:
                continue
                
            photo_url = "https://drtechno.ru/" + href
            
            ext = os.path.splitext(href)[1] or '.jpg'
            filename = f"{product_id}_{idx}{ext}"
            filepath = os.path.join(product_dir, f"{idx}{ext}")
            
            print(f"Скачиваю: {photo_url}")
            try:
                response = requests.get(photo_url, headers=headers, timeout=10, verify=False)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"Сохранено: {filepath}")
                else:
                    print(f"Ошибка {response.status_code}: {photo_url}")
            except Exception as e:
                print(f"Ошибка скачивания {photo_url}: {e}")
