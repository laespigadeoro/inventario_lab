# Sistema de Existencias — Laboratorio de Informática

Aplicación web educativa realizada con Python, Flask, SQLite, HTML y CSS. Permite administrar artículos de un laboratorio, consultar cantidades y ubicaciones, registrar movimientos y consultar reportes. El proyecto se organiza según las etapas de Scrum propuestas en el trabajo práctico.

## Requisitos
- Windows 10/11 (o sistema compatible).
- Python 3.10 o superior.
- Git para el control de versiones.
- Navegador web.

## Instalación en Windows
1. Descomprimí la carpeta del proyecto.
2. Abrí la carpeta `inventario_lab` en Visual Studio Code.
3. Abrí una terminal en esa carpeta.
4. Creá el entorno virtual:

   ```powershell
   py -m venv .venv
   ```
5. Activá el entorno virtual:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   Si PowerShell bloquea la activación, podés abrir una terminal CMD y ejecutar `.venv\Scripts\activate.bat`.
6. Instalá las dependencias:

   ```powershell
   python -m pip install -r requirements.txt
   ```
7. Ejecutá la aplicación:

   ```powershell
   python app.py
   ```
8. Abrí `http://127.0.0.1:5000` en el navegador.

La base SQLite se crea automáticamente en `instance/inventario.db`, junto con los roles, categorías, ubicaciones y un usuario inicial.

## Acceso inicial
- Usuario: `admin`
- Contraseña: `Admin123!`

Es una cuenta de demostración. Cambiá la contraseña desde el entorno local antes de usar el sistema con información real o publicarlo. Configurá también una variable de entorno `SECRET_KEY` propia; no publiques secretos.

## Funcionalidades
- Inicio y cierre de sesión con contraseñas almacenadas como hash.
- Roles: Administrador, Encargado, Técnico y Consulta.
- Alta, consulta, edición y baja lógica de artículos.
- Categorías y ubicaciones precargadas.
- Búsqueda por código, descripción, marca o serie y filtros por estado, categoría y ubicación.
- Registro de entradas, salidas, préstamos, devoluciones, traslados, reparaciones y bajas.
- Historial con fecha, responsable, artículo, cantidad y observación.
- Panel con totales y alerta de stock bajo.
- Reportes de inventario, reparación y baja; impresión desde el navegador.
- Interfaz adaptable a pantallas pequeñas.

## Roles y permisos
| Rol | Permisos principales |
|---|---|
| Administrador | Consultar, registrar, editar y dar de baja artículos; gestionar usuarios; movimientos y reportes. |
| Encargado | Consultar, registrar y editar artículos; registrar movimientos; consultar reportes. |
| Técnico | Consultar inventario y registrar movimientos/estados técnicos. |
| Consulta | Consultar inventario y reportes sin modificar información. |

## Pruebas
Instalá las dependencias y ejecutá:

```powershell
python -m pytest -v
```

Consultá `docs/casos_de_prueba.md` para el plan de pruebas manuales y los resultados que debés registrar después de probar la aplicación.

## Estructura
```text
inventario_lab/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── instance/              # SQLite local; no subir a GitHub
├── templates/             # Plantillas HTML/Jinja2
├── static/css/estilos.css
├── tests/test_app.py
└── docs/
    ├── backlog_scrum.md
    ├── modelo_datos.md
    ├── casos_de_prueba.md
    ├── git_github.md
    └── manual_usuario.md
```

## Límites conocidos y mejoras posibles
- El alta de categorías y ubicaciones está preparada mediante datos iniciales; una mejora futura sería incorporar pantallas para administrarlas.
- El registro de movimientos es básico y debe validarse en pruebas antes de usarlo con inventario real. Para un despliegue público se necesita configuración segura, gestión de secretos, protección CSRF, HTTPS, copias de seguridad y revisión de seguridad.
- La aplicación usa SQLite directamente para facilitar la instalación. SQLAlchemy puede incorporarse como mejora recomendada por la consigna.

## Git y GitHub
Consultá `docs/git_github.md` para crear el repositorio remoto, realizar commits, trabajar con ramas, Issues y Pull Requests.

## Trabajo académico
Ver `docs/backlog_scrum.md`, `docs/modelo_datos.md`, `docs/casos_de_prueba.md` y `docs/manual_usuario.md`. El historial de Git, las ramas, los Issues, Pull Requests y las capturas deben crearse con el uso real de GitHub; este paquete no simula esas evidencias.
