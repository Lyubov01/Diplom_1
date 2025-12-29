
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT) #Не запускался иначе
from unittest.mock import Mock
import pytest
from praktikum.burger import Burger


@pytest.fixture
def bun_factory():
    """Мок булочки."""
    def _make(name: str = "white bun", price: float = 200.0):
        m = Mock()
        m.get_name.return_value = name
        m.get_price.return_value = price
        return m
    return _make


@pytest.fixture
def ingredient_factory():
    """Мок ингредиента."""
    def _make(type_: str = "SAUCE", name: str = "Ketchup", price: float = 10.0):
        m = Mock()
        m.get_type.return_value = type_
        m.get_name.return_value = name
        m.get_price.return_value = price
        return m
    return _make


@pytest.fixture
def burger(bun_factory):
    """Пустой бургер с установленной булкой по умолчанию."""
    b = Burger()
    b.set_buns(bun_factory())
    return b
