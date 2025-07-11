import json
from collections import namedtuple
from collections import deque 
from typing import Dict, List

DiscountRules = namedtuple('DiscountRules',  ['general', 'desserts', 'kids'])

discounts = DiscountRules(
    general = 10.0,  
    desserts = 4.0,  
    kids = 10.0      
)

class OrderQueue:
    def __init__(self):
        self._queue = deque()
    
    def enqueue(self, order: "Order"):
        self._queue.append(order)
    
    def dequeue(self) -> "Order":
        if not self.is_empty():
            return self._queue.popleft()
        else: 
            raise IndexError("La cola de pedidos está vacía")
    
    def is_empty(self) -> bool:
        return len(self._queue) == 0
    
    def __len__(self):
        return len(self._queue)
    
    def peek(self) -> "Order":
        if not self.is_empty():
            return self._queue[0]
        else:
            raise IndexError("La cola de pedidos está vacía")
    
class Restaurant:
    def __init__(self):
        self.order_queue = OrderQueue()
        self.prepared_orders = []
    
    def receive_order(self, order: "Order"):
        self.order_queue.enqueue(order)
        print(f"Pedido recibido. Órdenes en cola: {len(self.order_queue)}")
    
    def process_next_order(self):
        if not self.order_queue.is_empty():
            next_order = self.order_queue.dequeue()
            print(f"Preparando pedido: {[str(item) for item in next_order.items]}")
            self.prepared_orders.append(next_order)
            return next_order
        else: 
            print("No hay pedidos para procesar")
            return None
    
    def serve_next_order(self):
        if self.prepared_orders:
            return self.prepared_orders.pop(0)
        else:
            print("No hay pedidos listos para servir")
            return None

class Menultem:
    def __init__(self, name: str, price: float):
        self._name = name
        self._price = price

    def total_price(self, *args: "Menultem") -> float:
        sum: float = self._price

        for i in args:
            sum += i._price
        return f"The total price is {sum}"
    
    def get_price(self):
        return self._price
    
    def get_name(self):
        return self._name
    
    def set_price(self, new_price):
        self._price = new_price

    def set_name(self, new_name):
        self._name = new_name

    def __str__(self):
        return f"{self._name} - ${self._price:.2f}"


class Beverages(Menultem):
    def __init__(self, name, price, alcohol: bool):
        super().__init__(name, price)
        self._alcohol = alcohol
    
    def get_alcohol(self):
        return self._alcohol

    def set_alcohol(self, new_alcohol):
        self._alcohol = new_alcohol
        

class Starters(Menultem):
    def __init__(self, name, price, portion: str):
        super().__init__(name, price)
        self._portion = portion
    
    def get_portion(self):
        return self._portion

    def set_portion(self, new_portion):
        self._portion = new_portion


class MainCourse(Menultem):
    def __init__(self, 
                name, 
                price, 
                protein: str, 
                spicy: bool, 
                vegetarian: bool):
        super().__init__(name, price)
        self._protein = protein
        self._spicy = spicy
        self._vegetarian = vegetarian

    def get_protein(self):
        return self._protein
    
    def get_spicy(self):
        return self._spicy
    
    def get_vegetarian(self):
        return self._vegetarian
    
    def set_protein(self, new_protein):
        self._protein = new_protein

    def set_spicy(self, new_spicy):
        self._spicy = new_spicy

    def set_vegetarian(self, new_vegetarian):
        self._vegetarian = new_vegetarian

class Desserts(Menultem):
    def __init__(self, 
                name, 
                price, 
                level_sugar: str, 
                gluten_free: bool):
        super().__init__(name, price)
        self._level_sugar = level_sugar
        self._gluten_free = gluten_free
    
    def get_level_sugar(self):
        return self._level_sugar
    
    def get_gluten_free(self):
        return self._gluten_free
    
    def set_level_sugar(self, new_level_sugar):
        self._level_sugar = new_level_sugar

    def set_gluten_free(self, new_gluten_free):
        self._gluten_free = new_gluten_free


class Extras(Menultem):
    def __init__(self, name, price, with_sausage: bool):
        super().__init__(name, price)
        self._with_sausage = with_sausage

    def get_with_sausage(self):
        return self._with_sausage
    
    def set_with_sausage(self, new_with_sausage):
        self._with_sausage = new_with_sausage
        

class KidsMenu(Menultem):
    def __init__(self, name, price, haealthy: bool):
        super().__init__(name, price)
        self._healthy = haealthy

    def get_haealthy(self):
        return self._haealthy
    
    def set_level_sugar(self, new_haealthy):
        self._haealthy= new_haealthy


class Order:
    def __init__(self, *args: Menultem):
        self.items = [*args]
        self.menu_file = "menu.json"
        self._initialize_menu_file()
    
    def _initialize_menu_file(self):
        try:
            with open(self.menu_file, 'r') as f:
                pass
        except FileNotFoundError:
            with open(self.menu_file, 'w') as f:
                json.dump({"beverages": [], "starters": [], "main_courses": [], 
                          "desserts": [], "extras": [], "kids_menus": []}, f)
    
    def _save_menu(self, menu_data: Dict):
        with open(self.menu_file, 'w') as f:
            json.dump(menu_data, f, indent=4)
    
    def _load_menu(self) -> Dict:
        with open(self.menu_file, 'r') as f:
            return json.load(f)
    
    def add_menu_item(self, category: str, item_data: Dict):
        menu_data = self._load_menu()
        if category in menu_data:
            menu_data[category].append(item_data)
            self._save_menu(menu_data)
        else:
            raise ValueError(f"Invalid category: {category}")
    
    def update_menu_item(self, category: str, item_name: str, new_data: Dict):
        menu_data = self._load_menu()
        if category in menu_data:
            for item in menu_data[category]:
                if item["name"] == item_name:
                    item.update(new_data)
                    self._save_menu(menu_data)
                    return
            raise ValueError(f"Item {item_name} not found in category {category}")
        else:
            raise ValueError(f"Invalid category: {category}")
    
    def delete_menu_item(self, category: str, item_name: str):
        menu_data = self._load_menu()
        if category in menu_data:
            menu_data[category] = [item for item in menu_data[category] if item["name"] != item_name]
            self._save_menu(menu_data)
        else:
            raise ValueError(f"Invalid category: {category}")
    
    def get_menu_items(self, category: str) -> List[Dict]:
        menu_data = self._load_menu()
        if category in menu_data:
            return menu_data[category]
        else:
            raise ValueError(f"Invalid category: {category}")
    
    def create_menu_item_from_data(self, category: str, item_data: Dict) -> Menultem:
        if category == "beverages":
            return Beverages(item_data["name"], item_data["price"], item_data["alcohol"])
        elif category == "starters":
            return Starters(item_data["name"], item_data["price"], item_data["portion"])
        elif category == "main_courses":
            return MainCourse(item_data["name"], item_data["price"], item_data["protein"], 
                            item_data["spicy"], item_data["vegetarian"])
        elif category == "desserts":
            return Desserts(item_data["name"], item_data["price"], item_data["level_sugar"], 
                          item_data["gluten_free"])
        elif category == "extras":
            return Extras(item_data["name"], item_data["price"], item_data["with_sausage"])
        elif category == "kids_menus":
            return KidsMenu(item_data["name"], item_data["price"], item_data["healthy"])
        else:
            raise ValueError(f"Invalid category: {category}")
    
    def add_items(self, item: "Menultem"):
        self.items.append(item)
    
    def bill_amount(self) -> float:
        sum = 0
        for i in self.items:
            sum += i._price
        return sum
    
    def discount(self) -> float:
        total: float = self.bill_amount()
        discounted: float = total * discounts.general / 100
        return discounted
    
    def discount_desserts(self) -> float:
        counter: int = 0
        desserts: float = 0
        for i in self.items:
            if isinstance(i, Beverages):
                counter += 1
            if isinstance(i, Desserts):
                desserts += i._price

        discounted: float = desserts * counter * discounts.desserts / 100
        return discounted

    def discount_kids_menu(self) -> float:
        counter: int = 0
        kids_menu: float = 0
        for i in self.items:
            if isinstance(i, MainCourse):
                counter += 1
            if isinstance(i, KidsMenu):
                kids_menu += i._price

        discounted: float = kids_menu * counter * discounts.kids / 100
        return discounted
    
    def total_bill_amount(self) -> float:
        subtotal = self.bill_amount()
        discount = self.discount()
        discount_desserts = self.discount_desserts()
        discount_kids_menu = self.discount_kids_menu()
        total_discount = discount + discount_desserts + discount_kids_menu
        return  subtotal - total_discount

    def print_bill(self):
        for item in self.items:
            print(f"{item}")

        discount = self.discount()
        discount_desserts = self.discount_desserts()
        discount_kids_menu = self.discount_kids_menu()
        total_discount = discount + discount_desserts + discount_kids_menu

        print(f"\nSubtotal: ${self.bill_amount():.2f}")
        print(f"Discount: -${discount:.2f}")
        print(f"Discount Desserts: -${discount_desserts:.2f}")
        print(f"Discount Kids Menu: -${discount_kids_menu:.2f}")
        print(f"Total Discount: -${total_discount:.2f}")
        print(f"Total Due: ${self.total_bill_amount():.2f}")
        print("Would you like to pay in cash or with card?")

class Payment:
    def __init__(self):
        pass

    def pay(self, amount: float):
        raise NotImplementedError("You have to choose a payment method.")

class Card(Payment):
    def __init__(self, number: str, cvv: int):
        super().__init__()
        self.number = number
        self.cvv = cvv

    def pay(self, amount: float):
        print(f"Paying {amount} with card {self.number[-4:]}")

class Cash(Payment):
    def __init__(self, amount_given: float):
        super().__init__()
        self.amount_given = amount_given

    def pay(self, amount: float):
        if self.amount_given >= amount:
            print(f"Payment made in cash. Change: {self.amount_given - amount}")
        else:
            print(f"Insufficient funds. Missing {amount - self.amount_given} for complete the payment.")


menu = Order()
menu.add_menu_item("beverages", {
    "name": "Coke",
    "price": 5.4,
    "alcohol": False
})

menu.add_menu_item("main_courses", {
    "name": "Spaghetti Bolognese",
    "price": 16.7,
    "protein": "Meat",
    "spicy": False,
    "vegetarian": False
})

menu.update_menu_item("beverages", "Coke", {"price": 5.9})

order_items = []
for item_data in menu.get_menu_items("beverages"):
    order_items.append(menu.create_menu_item_from_data("beverages", item_data))
for item_data in menu.get_menu_items("main_courses"):
    order_items.append(menu.create_menu_item_from_data("main_courses", item_data))

order = Order(*order_items)
order.print_bill()

main_course1 = MainCourse("Spaghetti Bolognese", 16.7, "Meat", False, False)
main_course2 = MainCourse("Curry", 18, "Tofu", True, True)
main_course3 = MainCourse("Grilled salmon with vegetables", 20, "Salmon", False, False)
dessert1 = Desserts("Strawberry Donut", 4.67, "High", True)
dessert2 = Desserts("Cheesecake", 8.9,"Medium", False)
beverage1 = Beverages("Coke", 5.4, False)
beverage2 = Beverages("Wine", 20, True)
beverage3 = Beverages("Appel Juice", 6.2, False)

print(main_course1.total_price(main_course2, main_course3))
print(dessert1.total_price(dessert2))
print(beverage1.total_price(beverage2, beverage3))

card= Card("15263748596", 707)
card.pay(order.total_bill_amount())
cash = Cash(5000)
cash.pay(order.total_bill_amount())

restaurant = Restaurant()
order1 = Order(
    Beverages("Coke", 5.4, False),
    Starters("Spring rolls", 10.45, "Small")
)
order2 = Order(
    MainCourse("Spaghetti Bolognese", 16.7, "Meat", False, False),
    Desserts("Cheesecake", 8.9, "Medium", False)
)

restaurant.receive_order(order1)
restaurant.receive_order(order2)

restaurant.process_next_order()
restaurant.process_next_order()

served_order = restaurant.serve_next_order()
if served_order:
    served_order.print_bill()

#Json
# Inicialización del menú
menu_manager = Order()  # Esto crea el archivo menu.json vacío

# Añadir ítems al menú
menu_manager.add_menu_item("beverages", {
    "name": "Limonada",
    "price": 4.5,
    "alcohol": False
})

menu_manager.add_menu_item("starters", {
    "name": "Bruschetta",
    "price": 8.0,
    "portion": "Medium"
})

menu_manager.add_menu_item("main_courses", {
    "name": "Pasta Carbonara",
    "price": 14.5,
    "protein": "Panceta",
    "spicy": False,
    "vegetarian": False
})

menu_manager.add_menu_item("desserts", {
    "name": "Tiramisú",
    "price": 6.8,
    "level_sugar": "Medium",
    "gluten_free": False
})