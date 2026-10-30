# Servicios de la tienda
# Autor: Jorge Coemsaña Lozoya

from typing import List, Tuple
from models.usuario import Usuario, Cliente, Admin
from models.producto import Producto
from models.pedido import Pedido


class TiendaService:
    """Clase que gestiona la logistica de la tienda y simula una base de datosen memoria"""


    def __init__(self):
        self.usuarios:List[Usuario]=[]
        self.productos:List[Producto]=[]
        self.pedidos:List[Pedido]=[]


    def registrar_usuario(self, tipo:str, nombre:str, email:str, direccion:str="")->Usuario:
        """Registra un nuevo usuario segun su tipo (cliente o admin)"""

        if tipo.lower()=="cliente":
            nuevo_usuario=Cliente(nombre, email, direccion)

        elif tipo.lower()=="admin":
            nuevo_usuario=Admin(nombre, email)

        else:
            raise ValueError("Tipo de usuario no definido. Debe ser 'cliente' o 'admin'.")

        self.usuarios.append(nuevo_usuario)
        return nuevo_usuario


    def anhadir_producto(self, nuevo_producto:Producto)->None:
        """Añade un producto al inventario. Si ya existe uno con el mismo nombre y precio lo añade a su stock"""

        for prod_existente in self.productos:
            if prod_existente.nombre==nuevo_producto.nombre and prod_existente.precio==nuevo_producto.precio:
                prod_existente.actualizar_stock(nuevo_producto.stock)
                return
        self.productos.append(nuevo_producto)
                


    def eliminar_producto(self, id_producto:str)->bool:
        """Elimina el producto del inventario mediante el id"""

        for producto in self.productos:
            if producto.id==id_producto:
                self.productos.remove(producto)
                return True
        return False


    def listar_productos(self)->List[Producto]:
        """Da la lista de todos los productos disponibles"""

        return self.productos


    def _buscar_cliente(self, id_usuario:str)->Cliente|None:
        """Busca un cliente por su id. Metodo interno ya que solo se usa para hacer pedidos, no en el main"""

        for usuario in self.usuarios:
            if usuario.id==id_usuario and isinstance(usuario,Cliente):
                return usuario
        return None

    
    def realizar_pedido(self, id_cliente:str, carro_compra:List[Tuple[Producto,int]])->Pedido:
        """Crea un pedido. Primero verifica la existencia del cliente y el stock. Luego resta del stock lo pedido y por ultimo genera el pedido"""

        cliente=self._buscar_cliente(id_cliente)
        if not cliente:
            raise ValueError("Cliente no existente o el usuario no es de tipo 'cliente'.")
        for producto, cantidad_pedida in carro_compra:
            if not producto.hay_stock(cantidad_pedida):
                raise ValueError(f"Stock insuficiente para el producto: {producto.nombre}."
                                 f"Disponible: {producto.stock}. Solicitado: {cantidad_pedida}.")

        for producto, cantidad_pedida in carro_compra:
            producto.actualizar_stock(-cantidad_pedida)
        nuevo_pedido=Pedido(cliente, carro_compra)
        self.pedidos.append(nuevo_pedido)
        return nuevo_pedido


    def lista_pedidos_usuario(self, id_usuario:str)->List[Pedido]:
        """Da los pedidos del usuario ordenados por fecha"""

        pedidos_usuario=[p for p in self.pedidos if p.cliente.id==id_usuario]
        pedidos_usuario.sort(key=lambda p:p.fecha_pedido)
        return pedidos_usuario


    # Los siguientes métodos los añado por que me parece que son necesarios para hacer el main  como quiero hacerlo, con la interfaz interactiva con las opciones que qiuiero añadirle (como eliminar un usuario o buscar  un usuario en general y no solo uncliente)


    def eliminar_usuario(self, id_usuario:str)->bool:
        """Elimina un usuario del sistema mediante su id"""

        for usuario in self.usuarios:
            if usuario.id==id_usuario:
                self.usuarios.remove(usuario)
                return True
        return False


    def buscar_usuario_por_id(self,id_usuario:str)->Usuario|None:
        """Busca usuarios por id"""

        for usuario in self.usuarios:
            if usuario.id==id_usuario:
                return usuario
        return None


    def es_admin_valido(self, id_usuario:str)->bool:
        """Compruebaque el usuario es un admin  para poder eliminar usuarios en el main. Es, basicamente,un control de seguridad"""

        usuario=self.buscar_usuario_por_id(id_usuario)
        return usuario is not None and usuario.is_admin()