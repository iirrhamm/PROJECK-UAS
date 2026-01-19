from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import os

application = Flask(__name__)
application.secret_key = 'kedai-secret-key'

ALLOWED_EXTENSION = set(['png', 'jpeg', 'jpg', 'pdf', 'bmp'])
UPLOAD_FOLDER = 'static/upload/'

application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['STATIC_UPLOAD_FOLDER'] = 'static/upload/'

conn = cursor = None

# ================== DATABASE ==================

def openDb():
    global conn, cursor
    conn = pymysql.connect(host="localhost", user="root", passwd="", database="kedai")
    cursor = conn.cursor()

def closeDb():
    global conn, cursor
    cursor.close()
    conn.close()

# ================== UTILITY ==================

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Silakan login terlebih dahulu", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ================== AUTH ==================

@application.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = generate_password_hash(password)

        openDb()
        try:
            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (username, hashed))
            conn.commit()
            flash("Registrasi berhasil! Silakan login.", "success")
        except pymysql.err.IntegrityError:
            flash("Username sudah digunakan!", "danger")
        closeDb()
        return redirect(url_for('login'))
    return render_template('register.html')


@application.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        openDb()
        sql = "SELECT * FROM users WHERE username=%s"
        cursor.execute(sql, (username,))
        user = cursor.fetchone()
        closeDb()

        if user and check_password_hash(user[2], password):  
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash(f"Selamat datang, {user[1]}!", "success")
            return redirect(url_for('usersutama'))
        else:
            flash("Username atau password salah!", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')


@application.route('/logout')
def logout():
    session.clear()
    flash("Anda berhasil logout.", "success")
    return redirect(url_for('usersutama'))

@application.route('/home')
@login_required
def usersutama():

    return render_template('users_R-001.html')

# ================== CRUD MAKANAN ==================

@application.route('/menu')
@login_required
def index():
    openDb()
    container = []
    sql = "SELECT * FROM makanan"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        container.append(data)
    closeDb()
    return render_template('menu_R-001.html', container=container)


@application.route('/tambahmenu')
@login_required
def crudmenu():
    # Ambil semua data makanan dari database
    openDb()
    container = []
    sql = "SELECT * FROM makanan"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        container.append(data)
    closeDb()

    # Render template halaman CRUD menu
    return render_template('index_R-001.html', container=container)


@application.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    if request.method == 'POST':
        file = request.files.get('file')
        filename = ''
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['STATIC_UPLOAD_FOLDER'], filename))
        kode = request.form['kode']
        nama = request.form['nama']
        harga = request.form['harga']
        kategory = request.form.get('id_kategory', 1)
        openDb()
        sql = "INSERT INTO makanan (kodemakanan, namamakanan, harga, namafile, id_kategory) VALUES (%s, %s, %s, %s, %s)"
        val = (kode, nama, harga, filename, kategory)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        flash("Makanan berhasil ditambahkan!", "success")
        return redirect(url_for('menu'))
    return render_template('tambah_R-001.html')


@application.route('/edit/<id_makanan>', methods=['GET', 'POST'])
@login_required
def edit(id_makanan):
    openDb()
    cursor.execute('SELECT * FROM makanan WHERE id_makanan=%s', (id_makanan))
    data = cursor.fetchone()
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))

        id_makanan = request.form['id_makanan']
        kode = request.form['kode']
        nama = request.form['nama']
        harga = request.form['harga']
        kategory = request.form['id_kategory']
        sql = "UPDATE makanan SET kodemakanan=%s, namamakanan=%s, harga=%s, id_kategory=%s, namafile=%s WHERE id_makanan=%s"
        val = (kode, nama, harga, kategory, filename, id_makanan)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('menu'))
    else:
        closeDb()
        return render_template('edit_R-001.html', data=data)


@application.route('/hapus/<id_makanan>', methods=['GET', 'POST'])
@login_required
def hapus(id_makanan):
    openDb()
    cursor.execute('DELETE FROM makanan WHERE id_makanan=%s', (id_makanan,))
    conn.commit()
    closeDb()
    flash("Makanan berhasil dihapus!", "success")
    return redirect(url_for('crudmenu'))


@application.route('/menu')
@login_required
def menu():
    openDb()
    container = []
    sql = "SELECT * FROM makanan"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        container.append(data)
    closeDb()
    return render_template('menu_R-001.html', container=container)


@application.route('/makanan')
@login_required
def makanan():
    openDb()
    container = []
    sql = "SELECT * FROM makanan WHERE id_kategory=1"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        container.append(data)
    closeDb()
    return render_template('makanan_R-001.html', container=container)


@application.route('/minuman')
@login_required
def minuman():
    openDb()
    container = []
    sql = "SELECT * FROM makanan WHERE id_kategory=2"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        container.append(data)
    closeDb()
    return render_template('minuman_R-001.html', container=container)


# ================== RUN ==================
if __name__ == '__main__':
    application.run(debug=True)
