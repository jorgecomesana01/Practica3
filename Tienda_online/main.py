# Main de la tienda online
# Autor: Jorge Comesaña Lozooya

# No me gusta como nos pediste hacer esta parte, me gusta más con una interfaz interactiva que ya esté mucho más preparado para llevarlo a la FastAPI.
# Por lo que esto lo dejaré como pediste, pero tambien voy a crear un main con un menu mas interactivo con ese fin

from typing import List
from models.usuario import Usuario, Cliente
from models.producto import Producto, ProductoElectronico, ProductoRopa, ProductoLibro
from services.tienda_service import TiendaService


def simulacion_pedida_en_el_ejercicio(servicio:TiendaService)->None:
    """Como dije en el comentario de arriba esta será la parte pedida, pero el main principal será una interfaz interactiva que me parece más divertido hacer eso"""

    print("\n\t SIMULACION DE TIENDA\n")

    # Registro de usuarios
    c1=servicio.registrar_usuario("cliente", "Pedro Picapiedra", "SoyElMotorDeMiCoche@gmail.com", "Calle Triceratops 64, Piedradura")
    c2=servicio.registrar_usuario("cliente", "Principe Vegeta IV", "AlgunDiaGanareAKakarot@gmail.com", "Mansión de Bulma, West City")
    c3=servicio.registrar_usuario("cliente", "Rey Felipe II", "TengoUnImperioDondeNoSePoneElSol@gmail.com", "Real Alcazar de Madrid")
    admin=servicio.registrar_usuario("admin", "Jorge Comesaña", "NoVoyAPonerAquiMiMail@gmail.com")

    # Creacion y añadido de productos
    p1=Producto("Gafas eclipse", 15.95, 24)
    p2=ProductoElectronico("GPU QueNvidia A100", 24999.99, 6, meses_garantia=48)
    p3=ProductoRopa("Camiseta de España 2 estrellas (Contrabando)", 25.00, 50, talla="M", color="Blanco")
    p4=ProductoRopa("Camiseta de España 2 estrellas (Contrabando)", 25.00, 40, talla="L", color="Rojo")
    p5=ProductoLibro("Clean Code: A Handbook of Agile Software Craftmanship", 43.72, 17, autor="Robert C. Martin", edicion="1ª")   # Gracias por la recomendacion Yago, me está gustando bastante

    for prod in [p1,p2,p3,p4,p5]:
        servicio.anhadir_producto(prod)

    # Lista de productos
    print("\n\t INVENTARIO INICIAL DE LA SIMULACION:\n")
    for producto in servicio.listar_productos():
        print(producto)
    print("\n")

    # Simulacion Pedidos
    print("\t PEDIDOS DE LA SIMULACION: \n")
    try:
        print("Éxito:", servicio.realizar_pedido(c1.id, [(p1,4)]))      # Pedro compra gafas de eclipse para toda la familia, que en la edad de piedra pegaban duro
        print("Éxito:", servicio.realizar_pedido(c2.id, [(p1,3),(p2,2),(p5,1)]))    # Vegeta compra las gafas para Bulma y Trunks, 2 A100 de regalo para Bulma y Trunks y el libro de Clean Code para que Trunks vaya aprendiendo
        print("Éxito:", servicio.realizar_pedido(c3.id, [(p1,1),(p3,48),(p4,38)]))  # Felipe II, como buen rey español, compra casi todo el stock de camisetas de España para dar color al palacio, además de unas gafas de exlipse por si le cuadra mientras va de caza
        print("Éxito:", servicio.realizar_pedido(c1.id, [(p2,1)]))    # Luego, Pedro se dio cuenta de que le apetecía conseguir un pisapieles caro, que las piedras estánmuy vistas en la edad de piedra, asi que compró una A100
    except ValueError as e:
        print("\t Error en el pedido:", e)

    # Inventario actualizado despuesde las compras
    print("\n\t INVENTARIO FINAL DE LA SIMULACION: \n")
    for prod in servicio.listar_productos():
        print(prod)
    print("\n")

    # Historial de pedidos de un cliente, en este caso Pedro, que hizo 2 compras
    print(f"\t HISTORIAL DE PEDIDOS DE {c1.nombre}: \n")
    pedidos_pedro=servicio.lista_pedidos_usuario(c1.id)
    if pedidos_pedro:
        for p in pedidos_pedro:
            print(p)
            for item, cantidad in p.lista_items:
                print(f" - {cantidad} {item.nombre} ({item.precio} euros c/u).")
    else:
        print("\tNo hay pedidos registrados para este usuario.\n")
    print("\n")


# Ahora comenzaré con la interfaz interactiva, que es mucho mejor a mi manera de verlo para enfocar este proyecto a futuro hacia una FastAPI
# Para hacerla todo lo completa que quiero necesito un metodos interno extra que usaré para iniciar pedido, ver el historial y eliminar usuario. Además añadí unos metodos para pedir enteros y otra para fltantes que tambien usaré en varias (sobre todola de enteros) 


def _pedir_entero(mensaje:str)->int:
    """Pide un número entero por consola. Util para añadir cantidades a la hora de comprar o añadir un producto al inventario"""

    while True:
        valor=input(mensaje).strip()
        if valor.isdigit():
            return int(valor)
        else:
            print("\tError. Introduce un número entero válido.")


def _pedir_float(mensaje:str)->float:
    """Pide un float. Util para ponerle precios a un nuevo producto añadido al stock"""

    while True:
        valor=input(mensaje).strip().replace(",",".").replace("'",".")
        try:
            return float(valor)
        except:
            print("\tError. Introduce un número float válido. Usa un punto en los decimales.")


def _elegir_de_lista_de_usuarios(candidatos:List[Usuario],etiqueta:str)->Usuario|None:
    """Dada una lista de usuarios permite elegir 1 mediante el id o el nombrey devuelve al usuario elegido. Util, como comenté arriba, para iniciar pedidos, ver historial y elimnar un usuario"""

    if not candidatos:
        print(f"\tNo hay ningún {etiqueta} registrado.")
        return None
    
    print(f"\n¿Cómo quieres buscar al {etiqueta}?")
    print("  1. Por ID")
    print("  2. Por nombre")
    modo=input("\tElige una opción (1-2): ").strip()

    if modo=="1":
        id_buscado=input(f"\tIntroduce el ID del {etiqueta} buscado: ").strip()
        for usuario in candidatos:
            if usuario.id==id_buscado:
                return usuario
        return None
    
    elif modo=="2":
        nombre_buscado=input(f"\tIntroduce el nombre (o parte) del {etiqueta} buscado: ").strip().lower()
        coincidencias=[user for user in candidatos if nombre_buscado in user.nombre.lower()]
        if not coincidencias:
            return None
        if len(coincidencias)==1:
            return coincidencias[0]
        print("\tSe han encontrado varias coincidencias.")

        for i,user in enumerate(coincidencias,start=1):
            print(f"{i}. {user.nombre} - (ID: {user.id[:8]})")
        seleccion=input(f"\tElige el número correspondiente al {etiqueta} buscado (0 para cancelar): ").strip()
        if seleccion.isdigit() and 1<=int(seleccion)<=len(coincidencias):
            return coincidencias[int(seleccion)-1]
        print("\nBúsqueda cancelada.")
        return None 
    
    else:  
        print("\tOpción no válida.")
        return None


def interfaz_interactiva(servicio:TiendaService)->None:
    """Interfaz en consola para interactuar con la tienda"""

    while True:
        print("\n\t INTERFAZ DE LA TIENDA \n")
        print("\t\t 1. Ver catálogo de productos.")
        print("\t\t 2. Ver lista de clientes.")
        print("\t\t 3. Iniciar un pedido.")
        print("\t\t 4. Ver historial de pedidos de un cliente.")
        print("\t\t 5. Registrar un usuario.")
        print("\t\t 6. Eliminar un usuario.")
        print("\t\t 7. Añadir un producto al inventario.")
        print("\t\t 8. Eliminar un producto del inventario.")
        print("\t\t 9. Salir.")
        opcion=input("\n Elige una opción (1-9): ").strip()

        if opcion=="1":
            print("\nCATÁLOGO:\n")
            catalogo=servicio.listar_productos()
            if not catalogo:
                print("\tNo hay productos en este momento.")
            for prod in catalogo:
                print(prod)

        elif opcion=="2":
            print("\nCLIENTES:")
            clientes=[user for user in servicio.usuarios if isinstance(user,Cliente)]
            if not clientes:
                print("\tNo hay clientes registrados en este momento.")
            for cliente in clientes:
                print(f"ID: {cliente.id[:8]} - Nombre: {cliente.nombre} - Email: {cliente.email}.")

        elif opcion=="3":
            print("\nNUEVO PEDIDO:\n")
            clientes=[user for user in servicio.usuarios if isinstance(user,Cliente)]
            cliente=_elegir_de_lista_de_usuarios(clientes,"cliente")
            if cliente is None:
                print("\t No se ha encontrado ningún clientecon esos datos.")
                continue
            print(f"\tCliente seleccionado: {cliente.nombre}.")
            carro:dict={}

            while True:
                productos=servicio.listar_productos()
                if not productos:
                    print("\tNo hay productos en el inventario.")
                    break

                print("\nProductos disponibles: ")
                for i, prod in enumerate(productos,start=1):
                    print(f"\t{i}. {prod}")
                print("\t0. Terminar pedido.")
                seleccion=input("\n\tElige un producto por su número (0 para terminar): ").strip()

                if seleccion=="0":
                    break

                if not seleccion.isdigit() or not (1<=int(seleccion)<=len(productos)):
                    print("\tOpción no válida.")
                    continue
                producto_elegido=productos[int(seleccion)-1]

                cantidad=_pedir_entero(f"\t¿Cuántas unidades de {producto_elegido.nombre} quieres?")
                if cantidad<=0:
                    print("\tLa cantidad debe ser mayor que 0.")
                    continue

                ya_en_el_carro=carro.get(producto_elegido.id,[producto_elegido,0])[1]
                if not producto_elegido.hay_stock(cantidad+ya_en_el_carro):
                    print(f"\tStock insuficiente. Disponible: {producto_elegido.stock-ya_en_el_carro}.")
                    continue
                if producto_elegido.id in carro:
                    carro[producto_elegido.id][1]+=cantidad
                else:
                    carro[producto_elegido.id]=[producto_elegido,cantidad]
                print(f"\tAñadido/s {cantidad} {producto_elegido.nombre}.")

            if not carro:
                print("\nPedido cancelado: ningún producto ha sido añadido.")
                continue
            
            carro_compra=[(producto,cantidad) for producto,cantidad in carro.values()]
            print("\nResumen de la compra: ")
            total_compra=0.0
            for producto, cantidad in carro_compra:
                total_por_producto=producto.precio*cantidad
                total_compra+=total_por_producto
                print(f"\t\t{cantidad} {producto.nombre} = {total_por_producto:.2f} euros.")
            print(f"\tTotal de la compra: {total_compra:.2f} euros.")
            confirmar=input("\n¿Confirmas el pedido? (s/n): ").strip().lower()

            if confirmar!="s":
                print("\tPedido cancelado.")
                continue
            
            try:
                pedido=servicio.realizar_pedido(cliente.id,carro_compra)
                print("\nPedido realizado.")
                print(pedido)
            except ValueError as e:
                print("Error al realizar el pedido: ",e)

        elif opcion=="4":
            print("\nHISTORIAL DE PEDIDOS: ")
            clientes=[user for user in servicio.usuarios if isinstance(user,Cliente)]
            cliente=_elegir_de_lista_de_usuarios(clientes,"cliente")
            if cliente is None:
                print("\tNo se ha encontrado ningún cliente con esos datos.")
                continue
            
            pedidos_cliente=servicio.lista_pedidos_usuario(cliente.id)
            if not pedidos_cliente:
                print(f"\n\t{cliente.nombre} no tiene pedidos registrados.")
                continue
            
            print(f"\n\tPedidos de {cliente.nombre}: \n")
            for pedido in pedidos_cliente:
                print("\t",pedido)
                for producto, cantidad in pedido.lista_items:
                    print(f"\t\t{cantidad} {producto.nombre} ({producto.precio} euros c/u).")
            print("\n")

        elif opcion=="5":
            print("\nREGISTRAR USUARIO:\n")
            print("\t1. Registrar cliente.")
            print("\t2. Registrar admin.")
            tipo_opcion=input("\n\t¿Qué tipode usuario  quieres registrar? (1-2): \n").strip()

            if tipo_opcion=="1":
                nombre_c=input("\t\tNombre: ").strip()
                email_c=input("\t\tEmail: ").strip()
                direccion_c=input("\t\tDirección postal: ").strip()
                nuevo_cliente=servicio.registrar_usuario("cliente",nombre_c,email_c,direccion_c)
                print(f"\n\tNuevo cliente registrado. ID: {nuevo_cliente.id} - Nombre: {nuevo_cliente.nombre}.")

            elif tipo_opcion=="2":
                id_autorizador=input("\tPor seguridad, introduce el ID de un admin existente: ").strip()
                if not servicio.es_admin_valido(id_autorizador):
                    print("\tID de admin ofrecido no válido. No se puede registrar el nuevo admin.")
                    continue
                
                nombre_a=input("\t\tNombre: ").strip()
                email_a=input("\t\tEmail: ").strip()
                nuevo_admin=servicio.registrar_usuario("admin",nombre_a,email_a)
                print(f"\n\tNuevo admin registrado. ID: {nuevo_admin.id} - Nombre: {nuevo_admin.nombre}.")

            else:
                print("\n\tOpción no válida.")

        elif opcion=="6":
            print("\nELIMINAR USUARIO:\n")
            usuario=_elegir_de_lista_de_usuarios(servicio.usuarios,"usuario")

            if usuario is None:
                print("\tNo se ha encontrado ningún usuario con esos datos.")
                continue
            rol="Admin" if usuario.is_admin() else "Cliente"
            confirmar=input(f"\n\t¿Seguro que quieres eliminar a {usuario.nombre} ({rol})? (s/n): ").strip().lower()

            if confirmar =="s":
                servicio.eliminar_usuario(usuario.id)
                print("\tUsuario eliminado correctamente.")

            else:
                print("\tEliminación cancelada.")

        elif opcion=="7":
            print("\nAÑADIR PRODUCTO:\n")
            print("\t1. Producto genérico.")
            print("\t2. Producto electrónico.")
            print("\t3. Ropa.")
            print("\t4. Libro.")
            tipo_producto=input("\n\tElige el tipo de producto a añadir (1-4): ").strip()

            if tipo_producto not in {"1","2","3","4"}:
                print("\tOpción no válida.")
                continue
            nombre=input("\tNombre del producto: ").strip()
            precio=_pedir_float("\tPrecio (euros): ")
            stock=_pedir_entero("\tStock: ")

            if tipo_producto=="1":
                nuevo_producto=Producto(nombre,precio,stock)

            elif tipo_producto=="2":
                meses_garantia=_pedir_entero("\tMeses de garantía: ")
                nuevo_producto=ProductoElectronico(nombre, precio,stock,meses_garantia)

            elif tipo_producto=="3":
                talla=input("\tTalla: ").strip()
                color=input("\tColor: ").strip()
                nuevo_producto=ProductoRopa(nombre, precio,stock,talla,color)

            else:
                autor=input("\tAutor: ").strip()
                edicion=input("\tEdición: ").strip()
                nuevo_producto=ProductoLibro(nombre, precio,stock,autor,edicion)

            servicio.anhadir_producto(nuevo_producto)
            print(f"\nProducto añadido: {nuevo_producto}")

        elif opcion=="8":
            print("\nELIMINAR PRODUCTO\n")
            productos=servicio.listar_productos()

            if not productos:
                print("\tNo hay productos en el inventario.")
                continue
            for i, prod in enumerate(productos,start=1):
                print(f"\t{i}. {prod}")
            seleccion=input("\n\tElige el número del producto a eliminar (0 para cancelar): ").strip()

            if seleccion=="0":
                print("\n\tOperación cancelada.\n")
                continue

            if not seleccion.isdigit()  or not (1<=int(seleccion)<=len(productos)):
                print("\tOpción no válida.")
                continue
            
            producto=productos[int(seleccion)-1]
            confirmar=input(f"\n\t¿Seguro que quieres eliminar {producto.nombre}? (s/n): ").strip().lower()

            if confirmar=="s":
                servicio.eliminar_producto(producto.id)
                print("\tProducto eliminado del inventario.")

            else:
                print("\tOperación cancelada.")

        elif opcion=="9":
            print("\nHasta luego.\n")
            break

        else:
            print("\nOperación no válida, elige un número del 1 al 9.")


def main():
    servicio=TiendaService()
    simulacion_pedida_en_el_ejercicio(servicio)
    respuesta=input("\n¿Quieres abrir la interfaz interactiva a continuación? (s/n): ").strip().lower()

    if respuesta=="s":
        interfaz_interactiva(servicio)

    else:
        print("\n\tFin de la ejecución, hasta luego.\n")


if __name__=="__main__":
    main()