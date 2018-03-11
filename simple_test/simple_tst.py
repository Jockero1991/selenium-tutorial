import pytest
from selenium import webdriver
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    wd = webdriver.Chrome(chrome_options=chrome_options)

    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_simple(driver):
    
    driver.get('https://vk.com/')
    wait = WebDriverWait(driver, 5)
    # Безуспешная авторизация
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="index_email"]'))).send_keys('tst@ts.com')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="index_pass"]'))).send_keys('123a')
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="index_login_button"]'))).click()
    # Ищем сообщение о том что авторизация не прошла.
    result = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_message"]/div/div/b[1]'))).text
    assert result == 'Не удается войти.'
    