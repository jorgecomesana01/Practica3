# PRACTICA3

**Autor:** Jorge Comesaña Lozoya


## DESCRIPCION

Esta practica consiste en implementar en git la práctica 1. Esta consta del núcleo para una tienda de comercio electrónico desarrollada en Python, implementando una arquitectura orientada a objetos (POO) limpia, desacoplada y modular.

Actualmente, el sistema simula una base de datos en memoria para gestionar el inventario, los usuarios (clientes y administradores) y las transacciones de pedidos, controlando la consistencia del stock en tiempo real. Aunque inicialmente fue planteado como un script secuencial de prueba, el diseño ha sido ampliado con una interfaz de consola interactiva pensada para facilitar una transición directa hacia una API REST con FastAPI, la cual ya fue hecha en la Práctica 2.


## CARACTERISTICAS

* **Gestión Polimórfica de Catálogo:** Soporte para múltiples tipos de producto mediante herencia:
  *  Producto Genérico
  *  Producto Electrónico (con meses de garantía)
  *  Producto Ropa (con talla y color)
  *  Producto Libro (con autor y edición)
* **Control de Usuarios y Roles:**
  * **Clientes:** Capacidad para almacenar dirección de envío y consultar historial de pedidos.
  * **Administradores:** Permisos especiales de gestión y validación para el registro y borrado de usuarios.
* **Motor de Pedidos y Validación de Stock:**
  * Validación atómica del stock disponible antes de formalizar la compra.
  * Deducción automática del inventario tras la confirmación del pedido.
  * Cálculo dinámico del total acumulado del carrito.
* **Doble Modo de Ejecución:**
  1. **Simulación automatizada:** Ejecución de pruebas predefinidas con casos extremos (compras múltiples, falta de stock, etc.).
  2. **Consola Interactiva:** Menú navegable con 9 opciones para operar la tienda en tiempo real.


## ESTRUCTURA

Tienda_online/
│
├── models/                     # Modelos de datos del dominio
│   ├── __init__.py
│   ├── usuario.py              # Clases Usuario, Cliente y Admin
│   ├── producto.py             # Jerarquía de clases de Productos
│   └── pedido.py               # Clase Pedido y cálculo de importes
│
├── services/                   # Lógica de negocio
│   ├── __init__.py
│   └── tienda_service.py       # Servicio central (gestión de estado en memoria)
│
├── main.py                     # Punto de entrada (simulación + menú interactivo)
├── Dockerfile                  # Empaquetado de la aplicación
├── .gitignore                  # Exclusión de ficheros temporales y entornos
└── README.md                   # Documentación del proyecto