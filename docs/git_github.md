# Guía para entregar con Git y GitHub

Estos pasos deben ejecutarse en la carpeta del proyecto después de instalar Git. Sustituí la URL por la URL real del repositorio creado en tu cuenta.

## Primer envío
```powershell
git init
git add .
git status
git commit -m "feat: crea sistema inicial de existencias"
git branch -M main
git remote add origin URL_REAL_DEL_REPOSITORIO
git push -u origin main
```

Si Git solicita identificar al autor, configurá tu identidad:
```powershell
git config --global user.name "Tu nombre"
git config --global user.email "tu-correo@example.com"
```

## Ramas y commits de ejemplo
```powershell
git checkout -b feature/articulos
# realizar y probar cambios
git add .
git commit -m "feat: implementa gestion de articulos"
git push -u origin feature/articulos
```

Luego, en GitHub, abrí un Pull Request desde `feature/articulos` hacia `main`. Para cada función, creá un Issue con la historia de usuario y movelo por las columnas del tablero (Pendiente, En curso, En revisión, Terminado). Los comandos son una guía: solo describí como realizado lo que hayas ejecutado realmente.

## Antes de publicar
- Verificá que `.gitignore` excluya `.venv`, `instance/*.db` y `.env`.
- No subas contraseñas reales, claves secretas ni datos personales.
- Incluí capturas reales del repositorio, Issues, tablero, commits y Pull Requests en la entrega.
