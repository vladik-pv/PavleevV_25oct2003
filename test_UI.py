import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

@pytest.mark.ui
@allure.feature("UI тесты корзины")
class TestCartUI:
    @pytest.fixture(scope="function")
    def driver(self):
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        yield driver
        driver.quit()

    @allure.story("Добавление товара в корзину через UI")
    def test_add_to_cart_ui(self, driver):
        with allure.step("Открываем главную страницу"):
            driver.get("https://altaivita.ru/")
            
        with allure.step("Ищем товар в поиске"):
            search_name = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input.js-searchpro__field-input"))
            )
            search_name.send_keys("Алтайский ключ")

        with allure.step("Находим и кликаем на первый товар"):
            first_product = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.digi-product__label"))
            )
            first_product.click()
            
        with allure.step("Добавляем товар в корзину"):
            add_to_cart_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.product-card__add_2_0"))
            )
            add_to_cart_btn.click()
            
        with allure.step("Проверяем, что товар добавлен"):
            cart_counter = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "a.header__basket-link"))
            )
            assert cart_counter.text == "1"

    @allure.story("Удаление товара из корзины через UI")
    def test_remove_from_cart_ui(self, driver):
        with allure.step("Добавляем товар в корзину для теста"):
            driver.get("https://altaivita.ru/product/123")  # Заменить на реальный URL товара
            add_to_cart_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart"))
            )
            add_to_cart_btn.click()
            
        with allure.step("Переходим в корзину"):
            driver.get("https://altaivita.ru/cart")
            
        with allure.step("Удаляем товар из корзины"):
            remove_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".remove-item"))
            )
            remove_btn.click()
            
        with allure.step("Проверяем, что корзина пуста"):
            empty_cart_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".empty-cart-message"))
            )
            assert "Ваша корзина пуста" in empty_cart_message.text