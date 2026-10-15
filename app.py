import os, sqlite3
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, g, abort
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'inventario.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cambiar-esta-clave-antes-de-publicar')
app.config['DATABASE'] = DB_PATH
ROLES = ['Administrador', 'Encargado', 'Técnico', 'Consulta']
ESTADOS = ['Disponible', 'En uso', 'Prestado', 'En reparación', 'Fuera de servicio', 'Dado de baja']
MOVIMIENTOS = ['Entrada', 'Salida', 'Préstamo', 'Devolución', 'Traslado', 'Reparación', 'Baja']


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db

@app.teardown_appcontext
def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(app.config['DATABASE'])
    db.execute('PRAGMA foreign_keys = ON')
    db.executescript('''
    CREATE TABLE IF NOT EXISTS roles(id INTEGER PRIMARY KEY, nombre TEXT UNIQUE NOT NULL);
    CREATE TABLE IF NOT EXISTS usuarios(id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, usuario TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, rol_id INTEGER NOT NULL REFERENCES roles(id), activo INTEGER NOT NULL DEFAULT 1);
    CREATE TABLE IF NOT EXISTS categorias(id INTEGER PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, descripcion TEXT DEFAULT '');
    CREATE TABLE IF NOT EXISTS ubicaciones(id INTEGER PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, sector TEXT DEFAULT '');
    CREATE TABLE IF NOT EXISTS articulos(id INTEGER PRIMARY KEY, codigo TEXT UNIQUE NOT NULL, descripcion TEXT NOT NULL, marca TEXT DEFAULT '', modelo TEXT DEFAULT '', serie TEXT DEFAULT '', cantidad INTEGER NOT NULL CHECK(cantidad >= 0), estado TEXT NOT NULL, categoria_id INTEGER NOT NULL REFERENCES categorias(id), ubicacion_id INTEGER NOT NULL REFERENCES ubicaciones(id), activo INTEGER NOT NULL DEFAULT 1, creado_en TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS movimientos(id INTEGER PRIMARY KEY, tipo TEXT NOT NULL, fecha TEXT NOT NULL, cantidad INTEGER NOT NULL DEFAULT 0, observacion TEXT DEFAULT '', articulo_id INTEGER NOT NULL REFERENCES articulos(id), usuario_id INTEGER NOT NULL REFERENCES usuarios(id));
    ''')
    for role in ROLES:
        db.execute('INSERT OR IGNORE INTO roles(nombre) VALUES(?)', (role,))
    if not db.execute('SELECT id FROM usuarios LIMIT 1').fetchone():
        admin_role = db.execute("SELECT id FROM roles WHERE nombre='Administrador'").fetchone()[0]
        db.execute('INSERT INTO usuarios(nombre,usuario,password_hash,rol_id) VALUES(?,?,?,?)', ('Administrador', 'admin', generate_password_hash('Admin123!'), admin_role))
    if not db.execute('SELECT id FROM categorias LIMIT 1').fetchone():
        db.executemany('INSERT INTO categorias(nombre,descripcion) VALUES(?,?)', [('Computadoras','Equipos de escritorio y notebooks'),('Monitores','Pantallas'),('Periféricos','Teclados, mouse y otros'),('Componentes','RAM, discos y placas'),('Red','Routers, switches y cables'),('Herramientas','Herramientas del laboratorio'),('Insumos','Materiales de uso corriente')])
    if not db.execute('SELECT id FROM ubicaciones LIMIT 1').fetchone():
        db.executemany('INSERT INTO ubicaciones(nombre,sector) VALUES(?,?)', [('Laboratorio','Sala principal'),('Depósito','Almacén'),('Taller','Reparaciones')])
    db.commit(); db.close()


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash('Iniciá sesión para continuar.', 'warning')
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper


def roles_required(*roles):
    def decorator(fn):
        @wraps(fn)
        @login_required
        def wrapper(*args, **kwargs):
            if session.get('rol') not in roles:
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator

@app.context_processor
def inject_globals():
    return {'current_user': session.get('nombre'), 'current_role': session.get('rol'), 'estados': ESTADOS, 'tipos_movimiento': MOVIMIENTOS}

@app.route('/')
def index():
    if not session.get('user_id'): return redirect(url_for('login'))
    db = get_db()
    stats = {
        'articulos': db.execute('SELECT COUNT(*) FROM articulos WHERE activo=1').fetchone()[0],
        'unidades': db.execute('SELECT COALESCE(SUM(cantidad),0) FROM articulos WHERE activo=1').fetchone()[0],
        'reparacion': db.execute("SELECT COUNT(*) FROM articulos WHERE activo=1 AND estado='En reparación'").fetchone()[0],
        'baja': db.execute("SELECT COUNT(*) FROM articulos WHERE estado='Dado de baja'").fetchone()[0],
    }
    movimientos = db.execute('''SELECT m.*, a.codigo, a.descripcion, u.nombre AS responsable FROM movimientos m JOIN articulos a ON a.id=m.articulo_id JOIN usuarios u ON u.id=m.usuario_id ORDER BY m.id DESC LIMIT 8''').fetchall()
    alertas = db.execute("SELECT * FROM articulos WHERE activo=1 AND cantidad<=2 ORDER BY cantidad, descripcion LIMIT 8").fetchall()
    return render_template('dashboard.html', stats=stats, movimientos=movimientos, alertas=alertas)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario','').strip()
        password = request.form.get('password','')
        row = get_db().execute('SELECT u.*, r.nombre AS rol FROM usuarios u JOIN roles r ON r.id=u.rol_id WHERE u.usuario=? AND u.activo=1', (usuario,)).fetchone()
        if row and check_password_hash(row['password_hash'], password):
            session.clear(); session.update(user_id=row['id'], nombre=row['nombre'], rol=row['rol'])
            flash('Sesión iniciada correctamente.', 'success')
            return redirect(url_for('index'))
        flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear(); flash('Cerraste sesión.', 'info'); return redirect(url_for('login'))

@app.route('/articulos')
@login_required
def articulos():
    db=get_db(); q=request.args.get('q','').strip(); estado=request.args.get('estado',''); categoria=request.args.get('categoria',''); ubicacion=request.args.get('ubicacion','')
    sql='''SELECT a.*, c.nombre AS categoria, u.nombre AS ubicacion FROM articulos a JOIN categorias c ON c.id=a.categoria_id JOIN ubicaciones u ON u.id=a.ubicacion_id WHERE a.activo=1'''; params=[]
    if q: sql += ' AND (a.codigo LIKE ? OR a.descripcion LIKE ? OR a.marca LIKE ? OR a.serie LIKE ?)'; params += [f'%{q}%']*4
    if estado: sql += ' AND a.estado=?'; params.append(estado)
    if categoria.isdigit(): sql += ' AND a.categoria_id=?'; params.append(int(categoria))
    if ubicacion.isdigit(): sql += ' AND a.ubicacion_id=?'; params.append(int(ubicacion))
    sql += ' ORDER BY a.descripcion'
    rows=db.execute(sql,params).fetchall()
    return render_template('articulos.html', articulos=rows, categorias=db.execute('SELECT * FROM categorias ORDER BY nombre').fetchall(), ubicaciones=db.execute('SELECT * FROM ubicaciones ORDER BY nombre').fetchall(), filtros={'q':q,'estado':estado,'categoria':categoria,'ubicacion':ubicacion})

@app.route('/articulos/nuevo', methods=['GET','POST'])
@roles_required('Administrador','Encargado')
def nuevo_articulo():
    db=get_db(); categorias=db.execute('SELECT * FROM categorias ORDER BY nombre').fetchall(); ubicaciones=db.execute('SELECT * FROM ubicaciones ORDER BY nombre').fetchall()
    if request.method=='POST':
        codigo=request.form.get('codigo','').strip(); descripcion=request.form.get('descripcion','').strip(); cantidad=request.form.get('cantidad','0').strip(); cat=request.form.get('categoria_id',''); ubi=request.form.get('ubicacion_id',''); estado=request.form.get('estado','Disponible')
        if not codigo or not descripcion or not cantidad.isdigit() or int(cantidad)<0 or not cat.isdigit() or not ubi.isdigit() or estado not in ESTADOS:
            flash('Revisá los campos obligatorios y la cantidad (debe ser un número igual o mayor a cero).','danger')
        else:
            try:
                cur=db.execute('INSERT INTO articulos(codigo,descripcion,marca,modelo,serie,cantidad,estado,categoria_id,ubicacion_id,creado_en) VALUES(?,?,?,?,?,?,?,?,?,?)',(codigo,descripcion,request.form.get('marca','').strip(),request.form.get('modelo','').strip(),request.form.get('serie','').strip(),int(cantidad),estado,int(cat),int(ubi),datetime.now().strftime('%Y-%m-%d %H:%M')))
                db.execute('INSERT INTO movimientos(tipo,fecha,cantidad,observacion,articulo_id,usuario_id) VALUES(?,?,?,?,?,?)',('Entrada',datetime.now().strftime('%Y-%m-%d %H:%M'),int(cantidad),'Registro inicial del artículo',cur.lastrowid,session['user_id']))
                db.commit(); flash('Artículo registrado correctamente.','success'); return redirect(url_for('articulos'))
            except sqlite3.IntegrityError: db.rollback(); flash('Ese código ya existe o una relación seleccionada no es válida.','danger')
    return render_template('articulo_form.html', articulo=None, categorias=categorias, ubicaciones=ubicaciones)

@app.route('/articulos/<int:articulo_id>/editar', methods=['GET','POST'])
@roles_required('Administrador','Encargado')
def editar_articulo(articulo_id):
    db=get_db(); a=db.execute('SELECT * FROM articulos WHERE id=? AND activo=1',(articulo_id,)).fetchone()
    if not a: abort(404)
    categorias=db.execute('SELECT * FROM categorias ORDER BY nombre').fetchall(); ubicaciones=db.execute('SELECT * FROM ubicaciones ORDER BY nombre').fetchall()
    if request.method=='POST':
        codigo=request.form.get('codigo','').strip(); descripcion=request.form.get('descripcion','').strip(); cantidad=request.form.get('cantidad','').strip(); cat=request.form.get('categoria_id',''); ubi=request.form.get('ubicacion_id',''); estado=request.form.get('estado','Disponible')
        if not codigo or not descripcion or not cantidad.isdigit() or int(cantidad)<0 or not cat.isdigit() or not ubi.isdigit() or estado not in ESTADOS:
            flash('Revisá los campos obligatorios y la cantidad.','danger')
        else:
            try:
                db.execute('UPDATE articulos SET codigo=?,descripcion=?,marca=?,modelo=?,serie=?,cantidad=?,estado=?,categoria_id=?,ubicacion_id=? WHERE id=?',(codigo,descripcion,request.form.get('marca','').strip(),request.form.get('modelo','').strip(),request.form.get('serie','').strip(),int(cantidad),estado,int(cat),int(ubi),articulo_id)); db.commit(); flash('Artículo actualizado.','success'); return redirect(url_for('articulos'))
            except sqlite3.IntegrityError: db.rollback(); flash('El código ya está usado por otro artículo.','danger')
        a=db.execute('SELECT * FROM articulos WHERE id=?',(articulo_id,)).fetchone()
    return render_template('articulo_form.html', articulo=a, categorias=categorias, ubicaciones=ubicaciones)

@app.route('/articulos/<int:articulo_id>/baja', methods=['POST'])
@roles_required('Administrador')
def baja_articulo(articulo_id):
    db=get_db(); a=db.execute('SELECT * FROM articulos WHERE id=? AND activo=1',(articulo_id,)).fetchone()
    if not a: abort(404)
    db.execute("UPDATE articulos SET activo=0, estado='Dado de baja' WHERE id=?",(articulo_id,))
    db.execute('INSERT INTO movimientos(tipo,fecha,cantidad,observacion,articulo_id,usuario_id) VALUES(?,?,?,?,?,?)',('Baja',datetime.now().strftime('%Y-%m-%d %H:%M'),a['cantidad'],'Baja lógica del artículo',articulo_id,session['user_id']))
    db.commit(); flash('Artículo dado de baja; se conservó el historial.','success'); return redirect(url_for('articulos'))

@app.route('/movimientos', methods=['GET','POST'])
@roles_required('Administrador','Encargado','Técnico')
def movimientos():
    db=get_db()
    if request.method=='POST':
        aid=request.form.get('articulo_id',''); tipo=request.form.get('tipo',''); cant=request.form.get('cantidad','0').strip(); obs=request.form.get('observacion','').strip()
        a=db.execute('SELECT * FROM articulos WHERE id=? AND activo=1',(aid,)).fetchone() if aid.isdigit() else None
        if not a or tipo not in MOVIMIENTOS or not cant.isdigit() or int(cant)<0:
            flash('Completá los datos del movimiento correctamente.','danger')
        elif tipo in ('Salida','Préstamo','Baja') and int(cant)>a['cantidad']:
            flash('No hay existencias suficientes para ese movimiento.','danger')
        else:
            n=int(cant); nueva=a['cantidad']; estado=a['estado']
            if tipo=='Entrada': nueva+=n; estado='Disponible' if nueva>0 else estado
            elif tipo in ('Salida','Préstamo','Baja'): nueva-=n; estado={'Préstamo':'Prestado','Baja':'Dado de baja'}.get(tipo, estado)
            elif tipo=='Devolución': nueva+=n; estado='Disponible'
            elif tipo=='Reparación': estado='En reparación'
            elif tipo=='Traslado': pass
            db.execute('UPDATE articulos SET cantidad=?, estado=? WHERE id=?',(nueva,estado,a['id']))
            db.execute('INSERT INTO movimientos(tipo,fecha,cantidad,observacion,articulo_id,usuario_id) VALUES(?,?,?,?,?,?)',(tipo,datetime.now().strftime('%Y-%m-%d %H:%M'),n,obs,a['id'],session['user_id']))
            db.commit(); flash('Movimiento registrado.','success'); return redirect(url_for('movimientos'))
    hist=db.execute('''SELECT m.*,a.codigo,a.descripcion,u.nombre AS responsable FROM movimientos m JOIN articulos a ON a.id=m.articulo_id JOIN usuarios u ON u.id=m.usuario_id ORDER BY m.id DESC''').fetchall()
    arts=db.execute('SELECT id,codigo,descripcion,cantidad FROM articulos WHERE activo=1 ORDER BY descripcion').fetchall()
    return render_template('movimientos.html', movimientos=hist, articulos=arts)

@app.route('/reportes')
@login_required
def reportes():
    db=get_db(); rows=db.execute('''SELECT a.codigo,a.descripcion,a.marca,a.modelo,a.serie,a.cantidad,a.estado,c.nombre AS categoria,u.nombre AS ubicacion FROM articulos a JOIN categorias c ON c.id=a.categoria_id JOIN ubicaciones u ON u.id=a.ubicacion_id ORDER BY c.nombre,a.descripcion''').fetchall()
    reparacion=db.execute("SELECT * FROM articulos WHERE estado='En reparación' AND activo=1 ORDER BY descripcion").fetchall(); bajas=db.execute("SELECT * FROM articulos WHERE estado='Dado de baja' OR activo=0 ORDER BY descripcion").fetchall()
    return render_template('reportes.html', articulos=rows,reparacion=reparacion,bajas=bajas)

@app.route('/usuarios', methods=['GET','POST'])
@roles_required('Administrador')
def usuarios():
    db=get_db()
    if request.method=='POST':
        nombre=request.form.get('nombre','').strip(); usuario=request.form.get('usuario','').strip(); password=request.form.get('password',''); rol=request.form.get('rol_id','')
        if not nombre or not usuario or len(password)<8 or not rol.isdigit(): flash('Completá los campos; la contraseña debe tener al menos 8 caracteres.','danger')
        else:
            try:
                db.execute('INSERT INTO usuarios(nombre,usuario,password_hash,rol_id) VALUES(?,?,?,?)',(nombre,usuario,generate_password_hash(password),int(rol))); db.commit(); flash('Usuario creado.','success'); return redirect(url_for('usuarios'))
            except sqlite3.IntegrityError: db.rollback(); flash('Ese nombre de usuario ya existe.','danger')
    rows=db.execute('SELECT u.id,u.nombre,u.usuario,u.activo,r.nombre AS rol FROM usuarios u JOIN roles r ON r.id=u.rol_id ORDER BY u.nombre').fetchall()
    roles=db.execute('SELECT * FROM roles ORDER BY id').fetchall()
    return render_template('usuarios.html',usuarios=rows,roles=roles)

@app.route('/usuarios/<int:user_id>/estado', methods=['POST'])
@roles_required('Administrador')
def estado_usuario(user_id):
    if user_id==session['user_id']: flash('No podés desactivar tu propia cuenta.','warning'); return redirect(url_for('usuarios'))
    db=get_db(); db.execute('UPDATE usuarios SET activo=CASE activo WHEN 1 THEN 0 ELSE 1 END WHERE id=?',(user_id,)); db.commit(); flash('Estado del usuario actualizado.','success'); return redirect(url_for('usuarios'))

@app.errorhandler(403)
def forbidden(e): return render_template('error.html',code=403,mensaje='No tenés permiso para realizar esta acción.'),403
@app.errorhandler(404)
def not_found(e): return render_template('error.html',code=404,mensaje='No encontramos el recurso solicitado.'),404

init_db()
if __name__=='__main__': app.run(debug=True)
