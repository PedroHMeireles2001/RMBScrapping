import json
from selenium.webdriver.common.by import By


def pegar_json(driver,url):
    driver.get(url)
    content = driver.find_element(By.TAG_NAME, 'pre').text
    parsed_json = json.loads(content)
    return parsed_json
def salvar_json(data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)