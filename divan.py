import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Инициализация драйвера Chrome с помощью webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://www.divan.ru/category/divany-i-kresla"
driver.get(url)
time.sleep(10)  # Увеличен таймаут ожидания для полной загрузки страницы

# Поиск всех карточек товаров
titles = driver.find_elements(By.CLASS_NAME, "class=WdR1o")
print(f"Найдено {len(titles)} товаров")  # Отладочное сообщение

parsed_data = []
for title in titles:
    try:
        name = title.find_element(By.CSS_SELECTOR, "span.name").text
        price = title.find_element(By.CSS_SELECTOR, "span.ui-LD-ZU KIkOH").text
        link = title.find_element(By.CSS_SELECTOR, "a.url").get_attribute("href")

        print(f"Название: {name}, Цена: {price}, Ссылка: {link}")  # Отладочное сообщение
        parsed_data.append([name, price, link])
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue

driver.quit()

# Проверка собранных данных
if not parsed_data:
    print("Нет данных для записи в файл.")
else:
    print(f"Собрано {len(parsed_data)} записей для сохранения в файл")

# Запись данных в CSV файл
try:
    with open("divan.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Название дивана", "Стоимость дивана", "Ссылка на диван"])
        writer.writerows(parsed_data)
    print("Парсинг завершен, данные сохранены в файл divan.csv")
except Exception as e:
    print(f"Произошла ошибка при записи в файл: {e}")

# Вывод содержимого для проверки
print("Содержимое файла:")
with open("divan.csv", "r", encoding="utf-8") as file:
    print(file.read())






