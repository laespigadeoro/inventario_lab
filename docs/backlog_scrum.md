# Scrum — Sistema de Existencias

## Objetivo del producto
Desarrollar una aplicación web para centralizar los datos de equipos, componentes, periféricos e insumos del laboratorio, incluyendo cantidades, estado, ubicación y registro de movimientos.

## Organización para modalidad individual
El práctico propone equipos de 3 a 5 estudiantes. Para una entrega individual, una misma persona puede asumir de forma simulada las responsabilidades de Product Owner, Scrum Master y Developer. Esto permite practicar los artefactos, pero no reemplaza la colaboración real solicitada en el enunciado. El docente puede revisar y validar la adaptación.

## Product Backlog priorizado
| ID | Historia de usuario | Prioridad | Puntos | Criterio de aceptación |
|---|---|---:|---:|---|
| HU01 | Como usuario quiero iniciar sesión para acceder según mi rol. | Alta | 5 | Credenciales correctas permiten entrar; incorrectas se rechazan. |
| HU02 | Como administrador quiero gestionar usuarios y roles. | Alta | 8 | Se crean usuarios con rol y contraseña hasheada; se puede activar/desactivar. |
| HU03 | Como encargado quiero registrar artículos. | Alta | 5 | Código único, descripción, categoría, ubicación y cantidad válida. |
| HU04 | Como encargado quiero editar estado y ubicación. | Alta | 5 | Los cambios se guardan y se ven en el listado. |
| HU05 | Como usuario autorizado quiero buscar y filtrar inventario. | Alta | 3 | Se filtra por texto, estado, categoría y ubicación. |
| HU06 | Como encargado quiero registrar movimientos para conservar trazabilidad. | Alta | 8 | Se guarda tipo, fecha, cantidad, artículo, usuario y observación. |
| HU07 | Como técnico quiero registrar equipos en reparación. | Media | 5 | El estado de reparación queda visible y se registra el movimiento. |
| HU08 | Como administrador quiero consultar reportes. | Media | 5 | Se visualizan inventario, reparaciones y bajas. |
| HU09 | Como usuario quiero ver un panel resumen. | Media | 5 | Se muestran cantidades generales, alertas y movimientos recientes. |

## Sprint 0 — Preparación
**Objetivo:** comprender el problema, definir alcance, preparar el repositorio y diseñar los datos.

**Tareas:** revisar la consigna; escribir el README; definir historias; dibujar el modelo de datos; crear repositorio Git; configurar `.gitignore`.

**Incremento esperado:** documentación inicial, backlog y estructura del proyecto.

## Sprint 1 — Base del sistema
**Objetivo:** construir la aplicación web y el CRUD de artículos.

**Tareas:** crear Flask; configurar SQLite; crear tablas de roles, usuarios, categorías, ubicaciones, artículos y movimientos; implementar listado, alta, edición, búsqueda y filtros.

**Incremento esperado:** inventario consultable y artículos registrables.

## Sprint 2 — Seguridad y perfiles
**Objetivo:** controlar el acceso.

**Tareas:** implementar login/logout; guardar contraseñas como hash; aplicar permisos por rol; crear gestión de usuarios; verificar acceso no autorizado.

**Incremento esperado:** acceso según perfil.

## Sprint 3 — Movimientos
**Objetivo:** registrar operaciones del inventario.

**Tareas:** implementar entradas, salidas, préstamos, devoluciones, traslados, reparaciones y bajas; guardar historial; validar cantidades y stock disponible.

**Incremento esperado:** movimientos consultables y existencias actualizadas.

## Sprint 4 — Calidad y cierre
**Objetivo:** terminar documentación y verificar el sistema.

**Tareas:** completar reportes y panel; ejecutar pruebas; corregir errores; redactar manual; capturar pantallas reales; preparar demostración.

**Incremento esperado:** versión revisada y documentada.

## Eventos Scrum adaptados
- **Sprint Planning:** al comenzar cada Sprint, seleccionar historias y tareas.
- **Daily Scrum individual:** anotar diariamente qué se hizo, qué se hará y qué impedimentos aparecieron.
- **Sprint Review:** demostrar las funciones que efectivamente funcionan.
- **Sprint Retrospective:** registrar qué salió bien, qué dificultó el trabajo y qué se mejorará.

## Registro diario para completar
| Fecha | ¿Qué avancé? | ¿Qué haré? | Impedimentos |
|---|---|---|---|
| Completar después de trabajar |  |  |  |

## Evidencias pendientes de crear en GitHub
1. Crear un repositorio llamado `sistema-existencias-laboratorio`.
2. Subir el proyecto sin `.venv`, secretos ni base local.
3. Crear Issues para las historias/tareas.
4. Crear ramas como `feature/articulos`, `feature/login` y `feature/movimientos`.
5. Realizar commits pequeños y descriptivos.
6. Si se trabaja individualmente, crear Pull Requests propios solo si el docente los acepta como evidencia; aclarar que no hubo revisión de otro integrante.
7. Capturar el tablero y el historial reales.
