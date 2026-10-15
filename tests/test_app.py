import os
import tempfile
import pytest
import app as inventory_app

@pytest.fixture()
def client():
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    original = inventory_app.app.config['DATABASE']
    inventory_app.app.config.update(TESTING=True, DATABASE=path, SECRET_KEY='test-secret')
    # Initialize a fresh database using the configured path.
    db = __import__('sqlite3').connect(path)
    db.execute('PRAGMA foreign_keys = ON')
    db.executescript('''
    CREATE TABLE roles(id INTEGER PRIMARY KEY, nombre TEXT UNIQUE NOT NULL);
    CREATE TABLE usuarios(id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, usuario TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, rol_id INTEGER NOT NULL REFERENCES roles(id), activo INTEGER NOT NULL DEFAULT 1);
    CREATE TABLE categorias(id INTEGER PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, descripcion TEXT DEFAULT '');
    CREATE TABLE ubicaciones(id INTEGER PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, sector TEXT DEFAULT '');
    CREATE TABLE articulos(id INTEGER PRIMARY KEY, codigo TEXT UNIQUE NOT NULL, descripcion TEXT NOT NULL, marca TEXT DEFAULT '', modelo TEXT DEFAULT '', serie TEXT DEFAULT '', cantidad INTEGER NOT NULL CHECK(cantidad >= 0), estado TEXT NOT NULL, categoria_id INTEGER NOT NULL REFERENCES categorias(id), ubicacion_id INTEGER NOT NULL REFERENCES ubicaciones(id), activo INTEGER NOT NULL DEFAULT 1, creado_en TEXT NOT NULL);
    CREATE TABLE movimientos(id INTEGER PRIMARY KEY, tipo TEXT NOT NULL, fecha TEXT NOT NULL, cantidad INTEGER NOT NULL DEFAULT 0, observacion TEXT DEFAULT '', articulo_id INTEGER NOT NULL REFERENCES articulos(id), usuario_id INTEGER NOT NULL REFERENCES usuarios(id));
    INSERT INTO roles VALUES(1,'Administrador'),(2,'Encargado'),(3,'Técnico'),(4,'Consulta');
    INSERT INTO categorias VALUES(1,'Periféricos',''),(2,'Computadoras','');
    INSERT INTO ubicaciones VALUES(1,'Laboratorio','Sala'),(2,'Depósito','Almacén');
    ''')
    from werkzeug.security import generate_password_hash
    db.execute('INSERT INTO usuarios(nombre,usuario,password_hash,rol_id) VALUES(?,?,?,?)', ('Admin Test','admin',generate_password_hash('Admin123!'),1))
    db.commit(); db.close()
    with inventory_app.app.test_client() as test_client:
        yield test_client
    inventory_app.app.config['DATABASE'] = original
    os.unlink(path)

def login(client, user='admin', password='Admin123!'):
    return client.post('/login', data={'usuario':user,'password':password}, follow_redirects=True)

def test_login_correcto(client):
    response = login(client)
    assert response.status_code == 200
    assert b'Panel principal' in response.data

def test_login_incorrecto(client):
    response = login(client, password='incorrecta',)
    assert b'Usuario o contrase' in response.data

def test_ruta_protegida_redirige_al_login(client):
    response = client.get('/articulos')
    assert response.status_code == 302
    assert '/login' in response.location

def test_consulta_no_puede_gestionar_usuarios(client):
    db = __import__('sqlite3').connect(inventory_app.app.config['DATABASE'])
    from werkzeug.security import generate_password_hash
    db.execute('INSERT INTO usuarios(nombre,usuario,password_hash,rol_id) VALUES(?,?,?,?)', ('Consulta','consulta',generate_password_hash('Consulta123!'),4))
    db.commit(); db.close()
    login(client, 'consulta', 'Consulta123!')
    response = client.get('/usuarios')
    assert response.status_code == 403
