import requests
import csv
from bs4 import BeautifulSoup

url = "https://www.divan.ru/category/divany-i-kresla"
response = requests.get(url)
response.raise_for_status()  # Проверка успешного запроса

soup = BeautifulSoup(response.content, 'html.parser')

# Поиск всех карточек товаров
titles = soup.find_all('div', class_='product-card')
print(f"Найдено {len(titles)} товаров")  # Отладочное сообщение

parsed_data = []
for title in titles:
    try:
        name = title.find('span', attrs={'data-ui-name': 'product_name'}).text.strip()
        price = title.find('span', attrs={'data-ui-name': 'product_price'}).text.strip()
        link = title.find('a', attrs={'data-ui-name': 'product_card'})['href']

        print(f"Название: {name}, Цена: {price}, Ссылка: {link}")  # Отладочное сообщение
        parsed_data.append([name, price, link])
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue

# Проверка собранных данных
if not parsed_data:
    print("Нет данных для записи в файл.")
else:
    print(f"Собрано {len(parsed_data)} записей для сохранения в файл")

# Запись данных в CSV файл
csv_filename = "divan1.csv"
try:
    with open(csv_filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Название дивана", "Стоимость дивана", "Ссылка на диван"])
        writer.writerows(parsed_data)
    print(f"Парсинг завершен, данные сохранены в файл {csv_filename}")
except Exception as e:
    print(f"Произошла ошибка при записи в файл: {e}")

# Вывод содержимого для проверки
try:
    with open(csv_filename, "r", encoding="utf-8") as file:
        print("Содержимое файла:")
        print(file.read())
except FileNotFoundError:
    print(f"Файл {csv_filename} не найден.")
except Exception as e:
    print(f"Произошла ошибка при чтении файла: {e}")

