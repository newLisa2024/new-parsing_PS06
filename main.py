import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

url = "https://tomsk.hh.ru/vacancies/programmist"
driver.get(url)
time.sleep(10)  # Увеличен таймаут ожидания для полной загрузки страницы

# Поиск всех карточек вакансий
vacancies = driver.find_elements(By.CLASS_NAME, "vacancy-card--z_UXteNo7bRGzxWVcL7y")

parsed_data = []
for vacancy in vacancies:
    try:
        title = vacancy.find_element(By.CSS_SELECTOR, "span.vacancy-name--c1Lay3KouCl7XasYakLk").text
        company = vacancy.find_element(By.CSS_SELECTOR, "span.company-info-text--vgvZouLtf8jwBmaD1xgp").text
        salary_elements = vacancy.find_elements(By.CSS_SELECTOR, "span.compensation-text--kTJ0_rp54B2vNeZ3CTt2")
        salary = salary_elements[0].text if salary_elements else "Не указано"
        link = vacancy.find_element(By.CSS_SELECTOR, "a.itemprop=url").get_attribute("href")

        parsed_data.append([title, company, salary, link])
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue

driver.quit()

# Запись данных в CSV файл
with open("hh.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Название вакансии", "Название компании", "Зарплата", "Ссылка на вакансию"])
    writer.writerows(parsed_data)

print("Парсинг завершен, данные сохранены в файл hh.csv")



