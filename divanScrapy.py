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
        name_element = title.find('span', attrs={'data-ui-name': 'product_name'})
        price_element = title.find('span', attrs={'data-ui-name': 'product_price'})
        link_element = title.find('a', attrs={'data-ui-name': 'product_card'})

        # Отладочные сообщения для проверки наличия элементов
        print(f"Элемент name_element: {name_element}")
        print(f"Элемент price_element: {price_element}")
        print(f"Элемент link_element: {link_element}")

        if name_element and price_element and link_element:
            name = name_element.text.strip()
            price = price_element.text.strip()
            link = "https://www.divan.ru" + link_element['href']

            print(f"Название: {name}, Цена: {price}, Ссылка: {link}")  # Отладочное сообщение
            parsed_data.append([name, price, link])
        else:
            print("Не удалось найти один из элементов: название, цена или ссылка")
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



