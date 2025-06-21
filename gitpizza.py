from typing import List


class MenuItem:
    """Представляє піцу з назвою, ціною та тегами (напр. вегетаріанська)."""

    def __init__(self, name: str, price: float, tags: List[str] = []):
        if not isinstance(name, str):
            raise TypeError("Назва піци має бути рядком.")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Ціна повинна бути додатнім числом.")
        self.__name = name
        self.__price = price
        self.__tags = tags

    def get_price(self) -> float:
        return self.__price

    def is_vegetarian(self) -> bool:
        return 'meat' not in self.__tags

    def __str__(self):
        return f"{self.__name} ({'вегетаріанська' if self.is_vegetarian() else "м'ясна"}) – {self.__price:.2f}₴"


class PizzaOrder:
    """Представляє замовлення піци."""

    def __init__(self, menu_item: MenuItem, quantity: int = 1):
        if not isinstance(menu_item, MenuItem):
            raise TypeError("menu_item має бути об'єктом MenuItem.")
        if not isinstance(quantity, int) or quantity < 1:
            raise ValueError("Кількість повинна бути цілим числом від 1.")
        self.__menu_item = menu_item
        self.__quantity = quantity

    def total_price(self) -> float:
        return self.__menu_item.get_price() * self.__quantity

    def is_vegetarian(self) -> bool:
        return self.__menu_item.is_vegetarian()

    def add_more(self, count: int):
        if count < 1:
            raise ValueError("Додана кількість має бути позитивною.")
        self.__quantity += count

    def __str__(self):
        return f"{self.__quantity} x {self.__menu_item}"

    def __eq__(self, other):
        return (
                isinstance(other, PizzaOrder)
                and self.__menu_item.get_price() == other.__menu_item.get_price()
                and self.is_vegetarian() == other.is_vegetarian()
        )

    def __lt__(self, other):
        return self.total_price() < other.total_price()

    def __add__(self, other):
        if not isinstance(other, PizzaOrder):
            raise TypeError("Можна додати тільки інший PizzaOrder.")
        if self.__menu_item != other.__menu_item:
            raise ValueError("Неможливо додати різні типи піц.")
        return PizzaOrder(self.__menu_item, self.__quantity + other.__quantity)

    def __mul__(self, number):
        if not isinstance(number, int) or number < 1:
            raise ValueError("Множити можна тільки на додатне ціле число.")
        return PizzaOrder(self.__menu_item, self.__quantity * number)


class Customer:
    """Клієнт піцерії."""

    def __init__(self, name: str, phone: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Ім'я клієнта обов'язкове.")
        if not phone.isdigit() or len(phone) < 7:
            raise ValueError("Неправильний номер телефону.")
        self.__name = name
        self.__phone = phone

    def __str__(self):
        return f"{self.__name} ({self.__phone})"


class OrderManager:
    """Управляє всіма замовленнями."""

    def __init__(self):
        self.__orders = []

    def add_order(self, customer: Customer, order: PizzaOrder):
        self.__orders.append((customer, order))

    def total_revenue(self) -> float:
        return sum(order.total_price() for _, order in self.__orders)

    def list_orders(self):
        for customer, order in self.__orders:
            print(f"{customer} замовив: {order}")

    def largest_order(self):
        if not self.__orders:
            return None
        return max(self.__orders, key=lambda item: item[1].total_price())

    def vegetarian_orders(self):
        return [(c, o) for c, o in self.__orders if o.is_vegetarian()]


if __name__ == "__main__":
    try:
        pizza1 = MenuItem("Маргарита", 145.0, tags=["cheese", "vegetarian"])
        pizza2 = MenuItem("Пепероні", 175.0, tags=["meat", "cheese"])
        pizza3 = MenuItem("Грибна", 155.0, tags=["vegetarian", "cheese", "mushrooms"])
        bad_pizza = MenuItem("Погана", -20.0)
    except Exception as e:
        print("Помилка створення піци:", e)

    order1 = PizzaOrder(pizza1, 2)
    order2 = PizzaOrder(pizza2, 1)
    order3 = PizzaOrder(pizza3, 3)

    print(order1)
    print(order2)
    print("Ціна замовлення 1:", order1.total_price())
    print("Замовлення 1 вегетаріанське?", order1.is_vegetarian())

    try:
        combined_order = order1 + order1
        print("Об'єднане замовлення:", combined_order)
        scaled_order = order2 * 3
        print("Множене замовлення:", scaled_order)
    except Exception as e:
        print("Помилка при додаванні/множенні:", e)

    customer1 = Customer("Олексій", "0931234567")
    customer2 = Customer("Ірина", "0977654321")

    manager = OrderManager()
    manager.add_order(customer1, order1)
    manager.add_order(customer1, order2)
    manager.add_order(customer2, order3)

    print("\nУсі замовлення:")
    manager.list_orders()

    print("\nЗагальна виручка:", manager.total_revenue())

    largest = manager.largest_order()
    if largest:
        print("\nНайбільше замовлення:")
        print(f"{largest[0]} → {largest[1]}")

    print("\nВегетаріанські замовлення:")
    for c, o in manager.vegetarian_orders():
        print(f"{c} → {o}")
