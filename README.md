# Reto-07
## FIFO Queue
```python
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
```
## Named Tuple
```python
discounts = DiscountRules(
    general = 10.0,  
    desserts = 4.0,  
    kids = 10.0      
)
```
## menu.json
```python
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
```
## Output
```
Coke - $5.90
Coke - $5.40
Limonada - $4.50
Coke - $5.40
Spaghetti Bolognese - $16.70
Spaghetti Bolognese - $16.70
Pasta Carbonara - $14.50
Spaghetti Bolognese - $16.70

Subtotal: $85.80
Discount: -$8.58
Discount Desserts: -$0.00
Discount Kids Menu: -$0.00
Total Discount: -$8.58
Total Due: $77.22
Would you like to pay in cash or with card?
The total price is 54.7
The total price is 13.57
The total price is 31.599999999999998
Paying 77.22000000000001 with card 8596
Payment made in cash. Change: 4922.78
Pedido recibido. Órdenes en cola: 1
Pedido recibido. Órdenes en cola: 2
Preparando pedido: ['Coke - $5.40', 'Spring rolls - $10.45']
Preparando pedido: ['Spaghetti Bolognese - $16.70', 'Cheesecake - $8.90']
Coke - $5.40
Spring rolls - $10.45

Subtotal: $15.85
Discount: -$1.58
Discount Desserts: -$0.00
Discount Kids Menu: -$0.00
Total Discount: -$1.58
Total Due: $14.27
Would you like to pay in cash or with card?
```
