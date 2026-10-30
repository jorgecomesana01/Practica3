# Clase Producto
# Autor: Jorge Comesaña Lozoya  

import uuid     # Usaré la opcion de generar un id random con uuid4


class Producto:
    """Clase padre para cualquier producto de la tienda"""


    def __init__(self, nombre: str, precio: float, stock: int):
        self.id: str=str(uuid.uuid4())
        self.nombre:str=nombre
        self.precio:float=precio
        self.stock:int=stock


    def __str__(self)->str:
        return f"[{self.id[:8]}] - {self.nombre} - {self.precio} eur.  (Stock:{self.stock})."


    def hay_stock(self, cantidad:int)->bool:
        "Verifica si hay stock disponible para lo pedido"

        return self.stock >=cantidad


    def actualizar_stock(self,cantidad:int)->None:
        "Actualiza el stock. Un numero positivo añade (reponer) y uno negativo resta (vender)"

        self.stock +=cantidad



class ProductoElectronico (Producto):
    """Subclase para productos electronicos"""


    def __init__(self, nombre:str, precio:float, stock:int, meses_garantia:int):
        super().__init__(nombre, precio, stock)
        self.meses_garantia:int= meses_garantia


    def __str__(self)->str:
        str_producto=super().__str__()
        return f"{str_producto} - Garantia: {self.meses_garantia} meses."



class ProductoRopa(Producto):
    """Subclase para ropa, que necesita a mayores datos de talla y color"""


    def __init__(self, nombre:str, precio:float, stock:int, talla:str, color:str):
        super().__init__(nombre, precio, stock)
        self.talla:str=talla
        self.color:str=color


    def __str__(self)->str:
        str_producto=super().__str__()
        return f"{str_producto} - Talla: {self.talla} - Color: {self.color}."



class ProductoLibro(Producto):
    """Añado esta subclase extra para vender libros. Tiene los atributos autor y edicion a mayores"""


    def __init__(self, nombre:str, precio:float, stock:int, autor:str, edicion:str):
        super().__init__(nombre, precio, stock)
        self.autor:str=autor
        self.edicion:str=edicion


    def __str__(self)->str:
        str_producto=super().__str__()
        return f"{str_producto} - Autor: {self.autor} - Edición: {self.edicion}."
