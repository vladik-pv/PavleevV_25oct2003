import allure
import pytest
import requests
from urllib.parse import urljoin

BASE_URL = "https://altaivita.ru/"

@pytest.mark.api
@allure.feature("API тесты корзины")
class TestCartAPI:
    @allure.story("Добавление товара в корзину")
    def test_add_item_to_cart(self):
        with allure.step("Добавляем товар в корзину"):
            product_id = 238
            quantity = 1
            payload = {"product_id": product_id, "quantity": quantity}

            response = requests.post(
                urljoin(BASE_URL, "cart/add"),
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
        with allure.step("Проверяем ответ"):
            assert response.status_code == 200
            assert response.json().get("success") is True
            assert response.json().get("cart_item_count", 0) > 0

    @allure.story("Очистка корзины")
    def test_clear_cart(self):
        with allure.step("Очищаем корзину"):
            response = requests.post(
                urljoin(BASE_URL, "cart/clear"),
                headers={"Content-Type": "application/json"}
            )

        with allure.step("Проверяем ответ"):
            assert response.status_code == 200
            assert response.json().get("success") is True
            assert response.json().get("cart_item_count", 0) == 0
            