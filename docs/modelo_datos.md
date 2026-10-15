# Modelo de datos

## Diagrama entidad-relación
```mermaid
erDiagram
    ROL ||--o{ USUARIO : asigna
    CATEGORIA ||--o{ ARTICULO : clasifica
    UBICACION ||--o{ ARTICULO : contiene
    ARTICULO ||--o{ MOVIMIENTO : registra
    USUARIO ||--o{ MOVIMIENTO : realiza
    ROL { int id PK string nombre }
    USUARIO { int id PK string nombre string usuario string password_hash int rol_id FK int activo }
    CATEGORIA { int id PK string nombre string descripcion }
    UBICACION { int id PK string nombre string sector }
    ARTICULO { int id PK string codigo UK string descripcion string marca string modelo string serie int cantidad string estado int categoria_id FK int ubicacion_id FK int activo }
    MOVIMIENTO { int id PK string tipo string fecha int cantidad string observacion int articulo_id FK int usuario_id FK }
```

## Tablas y relaciones
- **Rol:** identifica el perfil y sus permisos generales. Un rol puede asignarse a muchos usuarios.
- **Usuario:** almacena nombre, nombre de usuario, hash de contraseña, rol y estado activo. Un usuario puede registrar muchos movimientos.
- **Categoría:** clasifica artículos, por ejemplo computadoras, periféricos, componentes, red, herramientas e insumos.
- **Ubicación:** indica el lugar físico o sector donde se encuentra el artículo.
- **Artículo:** contiene código único, descripción, marca, modelo, serie, cantidad, estado, categoría, ubicación y marca lógica de activo.
- **Movimiento:** conserva tipo, fecha, cantidad, observación, artículo relacionado y usuario responsable.

## Claves y validaciones
- Cada tabla posee una clave primaria `id`.
- `articulos.codigo` y `usuarios.usuario` son únicos.
- Las claves foráneas conectan las tablas relacionadas.
- La cantidad no puede ser negativa.
- La baja de un artículo se realiza de forma lógica para conservar su historial.
- Las contraseñas se guardan con hash, no como texto plano.
