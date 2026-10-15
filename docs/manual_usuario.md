# Manual breve de usuario

## 1. Iniciar sesión
Abrí `http://127.0.0.1:5000`. Ingresá con el usuario asignado. En una instalación nueva, el acceso inicial de demostración es `admin` / `Admin123!`; debe cambiarse antes de cualquier uso real.

## 2. Panel principal
Muestra el número de artículos activos, la suma de unidades, los artículos en reparación, las bajas, los últimos movimientos y una alerta para artículos con dos unidades o menos.

## 3. Consultar el inventario
Entrá en **Artículos**. Podés buscar por código, descripción, marca o número de serie, y filtrar por estado, categoría y ubicación.

## 4. Registrar un artículo
Con rol Administrador o Encargado, pulsá **Nuevo artículo**. Completá código, descripción, cantidad, categoría, ubicación y estado. El código no debe repetirse y la cantidad debe ser igual o mayor a cero. Guardá el formulario.

## 5. Editar o dar de baja
Administrador y Encargado pueden editar artículos. Solo el Administrador puede realizar la baja lógica. La baja no borra el registro histórico.

## 6. Registrar movimientos
Administrador, Encargado y Técnico pueden ingresar en **Movimientos**, seleccionar un artículo, tipo, cantidad y observación, y guardar. El sistema rechaza salidas, préstamos o bajas superiores al stock existente.

## 7. Consultar reportes
En **Reportes** se encuentra el inventario general, los artículos en reparación y los dados de baja. El botón de impresión permite imprimir o guardar el reporte como PDF desde el navegador.

## 8. Administrar usuarios
Solo Administrador puede crear usuarios, asignar roles y activar/desactivar cuentas. Las contraseñas deben tener al menos ocho caracteres y se almacenan como hash.

## 9. Cerrar sesión
Pulsá **Cerrar sesión** en la barra lateral.

## Capturas para la entrega
Después de ejecutar el sistema, realizar capturas reales de: login, panel principal, listado de artículos, formulario de alta, historial de movimientos, reportes y administración de usuarios. Insertarlas en el informe o presentación.
