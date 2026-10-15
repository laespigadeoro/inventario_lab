# Casos de prueba

Ejecutar las pruebas automatizadas con `python -m pytest -v` y completar el resultado real de cada prueba manual.

| ID | Caso | Acción | Resultado esperado | Resultado real |
|---|---|---|---|---|
| CP01 | Login válido | Ingresar admin y contraseña inicial. | Se abre el panel principal. | Completar al ejecutar |
| CP02 | Login inválido | Ingresar una contraseña incorrecta. | No permite entrar y muestra mensaje claro. | Completar al ejecutar |
| CP03 | Código duplicado | Registrar dos artículos con el mismo código. | Rechaza el segundo registro. | Completar al ejecutar |
| CP04 | Cantidad negativa | Enviar una cantidad menor que cero. | El sistema rechaza el dato. | Completar al ejecutar |
| CP05 | Permisos | Un usuario Consulta intenta entrar a gestión de usuarios. | Se deniega el acceso. | Completar al ejecutar |
| CP06 | Stock insuficiente | Registrar salida/préstamo mayor que el stock. | Se rechaza la operación. | Completar al ejecutar |
| CP07 | Movimiento | Registrar una entrada o préstamo válido. | Se guarda fecha, artículo, responsable y detalle; se actualiza stock/estado. | Completar al ejecutar |
| CP08 | Baja lógica | Administrador da de baja un artículo. | Se oculta del inventario activo y queda en el reporte de bajas. | Completar al ejecutar |
| CP09 | Filtros | Buscar por código o estado. | Se muestran solo coincidencias. | Completar al ejecutar |
| CP10 | Diseño adaptable | Abrir en pantalla angosta. | El contenido se adapta y las tablas permiten desplazamiento horizontal. | Completar al ejecutar |

## Incidencias detectadas
Anotar aquí los errores que aparezcan durante las pruebas y cómo se corrigieron. No completar resultados antes de ejecutar el sistema.
