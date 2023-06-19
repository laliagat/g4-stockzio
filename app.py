from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL connection
app.config['MYSQL_HOST'] = '52.23.232.85'
app.config['MYSQL_USER'] = 'support'
app.config['MYSQL_PASSWORD'] = 'grupo4password'
app.config['MYSQL_DB'] = 'Stockzio'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

#MAIN principal
@app.route('/')
def Index():
    return jsonify({
        'Bienvenido(a) a Stockzio'
    })

#TEST
@app.route('/test', methods=['GET'])
def test():
    return jsonify(
        {
            'status':'success'
        }
    )

#CRUD PRODUCTO 

@app.route('/productos')
def productos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT *  FROM Producto')
    data=cur.fetchall()
    stock=[]

    for prod in data:
        producto = {
            'id_producto': prod[0], 
            'descripcion': prod[1], 
            'precio': prod[2], 
            'marca': prod[3],
            'stock': prod[4], 
            'categoria': prod[5]
        }
        stock.append(producto)
    return jsonify({'productos': stock})

@app.route('/delete_producto', methods=['DELETE'])
def delete_producto():
    response = {'status': 'success'}
    id = request.form.get('id_producto')
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Producto WHERE id_producto = %s', (id,))
    mysql.connection.commit()
    return jsonify(response)

@app.route('/add_producto', methods=['POST'])
def add_producto():
    if request.method == 'POST': #Define método de envío
        response = {'status': 'success'}
        descripcion = request.form.get('descripcion') # request.form recoge datos de formulario
        precio = request.form.get('precio')
        marca = request.form.get('marca')
        stock = request.form.get('stock')
        id_categoria = request.form.get('id_categoria')
        
        cur = mysql.connection.cursor() #genera conexion DB SQL
        cur.execute('INSERT INTO Producto (descripcion, precio, marca, stock, id_categoria) VALUES (%s, %s, %s, %s, %s)', 
        (descripcion, precio, marca, stock, id_categoria)) # ejecuta comando SLQ datos recogidos del form
        mysql.connection.commit() # Guarda cambios en DB
        return jsonify(response)
    
@app.route('/update_producto', methods = ['PUT'])
def update_producto():
    try:
        response_object = {'status': 'success'}
        id = str(request.form.get('id_producto'))
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        marca = request.form.get('marca')
        stock = request.form.get('stock')
        id_cat = request.form.get('id_categoria')
        cursor = mysql.connection.cursor()
        cursor.execute("""
        UPDATE Producto
        SET descripcion = %s,
            precio = %s,
            marca = %s,
            stock = %s,
            id_categoria = %s
        WHERE id_producto = %s
        """, (descripcion,precio,marca,stock,id_cat,id ))
        mysql.connection.commit()
        return jsonify(response_object)

    except Exception as e:
        response_object = {'status': 'error'}
        response_object['message'] = f"Error al editar el equipo : {e}"
        print(response_object)
        return jsonify(response_object)   

#CRUD CLIENTE

@app.route('/clientes')
def clientes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Cliente')
    data=cur.fetchall()
    lista=[]
    for cli in data:
        cliente = {
            'id_cliente': cli[0], 
            'nombres': cli[1], 
            'apellidos': cli[2], 
            'n_celular': cli[3],
            'email': cli[4], 
            'direccion': cli[5]
        }
        lista.append(cliente)
    return jsonify({'clientes': lista}) 


@app.route('/delete_cliente', methods=['DELETE'])
def delete_cliente():
    response = {'status': 'success'}
    id = request.form.get('id_cliente')
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Cliente WHERE id_cliente = %s', (id,))
    mysql.connection.commit()
    return jsonify(response)

@app.route('/add_cliente', methods=['POST'])
def add_cliente():
    if request.method == 'POST': #Define método de envío
        response = {'status': 'success'}
        descripcion = request.form.get('descripcion') # request.form recoge datos de formulario
        nombres = request.form.get('nombres')
        apellidos = request.form.get('apellidos')
        n_celular = request.form.get('n_celular')
        email = request.form.get('email')
        direccion = request.form.get('direccion')
        
        cur = mysql.connection.cursor() #genera conexion DB SQL
        cur.execute('INSERT INTO Cliente (nombres, apellidos, n_celular, email, direccion) VALUES (%s, %s, %s, %s, %s)', 
        (nombres, apellidos, n_celular, email, direccion)) # ejecuta comando SLQ datos recogidos del form
        mysql.connection.commit() # Guarda cambios en DB
        return jsonify(response)
    
@app.route('/update_cliente', methods = ['PUT'])
def update_cliente():
    try:
        response_object = {'status': 'success'}
        id = str(request.form.get('id_cliente'))
        nombres = request.form.get('nombres')
        apellidos = request.form.get('apellidos')
        n_celular = request.form.get('n_celular')
        email = request.form.get('email')
        direccion = request.form.get('direccion')

        cursor = mysql.connection.cursor()
        cursor.execute("""
        UPDATE Cliente
        SET nombres = %s,
            apellidos = %s,
            n_celular = %s,
            email = %s,
            direccion = %s
        WHERE id_cliente = %s
        """, (nombres,apellidos,n_celular,email,direccion,id ))
        mysql.connection.commit()
        return jsonify(response_object)

    except Exception as e:
        response_object = {'status': 'error'}
        response_object['message'] = f"Error al editar el registro : {e}"
        print(response_object)
        return jsonify(response_object)     

#CRUD VENTAS

@app.route('/ventas')
def ventas():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Venta')
    data=cur.fetchall()
    transacciones=[]
    for ve in data:
        venta = {
            'id_venta': ve[0], 
            'id_producto': ve[1], 
            'id_cliente': ve[2], 
            'talla': ve[3],
            'color': ve[4], 
            'cantidad': ve[5],
            'fecha': ve[6],
            'monto': ve[7]
        }
        transacciones.append(venta)
    return jsonify({'ventas': transacciones}) 

@app.route('/delete_venta', methods=['DELETE'])
def delete_venta():
    response = {'status': 'success'}
    id = request.form.get('id_venta')
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Venta WHERE id_venta = %s', (id,))
    mysql.connection.commit()
    return jsonify(response)

@app.route('/add_venta', methods=['POST'])
def add_venta():
    if request.method == 'POST': #Define método de envío
        response = {'status': 'success'}
        id_producto = request.form.get('id_producto') # request.form recoge datos de formulario
        id_cliente = request.form.get('id_cliente')
        talla = request.form.get('talla')
        color = request.form.get('color')
        cantidad = request.form.get('cantidad')
        fecha = request.form.get('fecha')
        monto = request.form.get('monto')
        
        cur = mysql.connection.cursor() #genera conexion DB SQL
        cur.execute('INSERT INTO Venta (id_producto, id_cliente, talla, color, cantidad, fecha, monto) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
        (id_producto, id_cliente, talla, color, cantidad, fecha, monto)) # ejecuta comando SLQ datos recogidos del form
        mysql.connection.commit() # Guarda cambios en DB
        return jsonify(response)

@app.route('/update_venta', methods = ['PUT'])
def update_venta():
    try:
        response_object = {'status': 'success'}
        id = str( request.form.get('id_venta'))
        id_producto = request.form.get('id_producto')
        id_cliente = request.form.get('id_cliente')
        talla = request.form.get('talla')
        color = request.form.get('color')
        cantidad = request.form.get('cantidad')
        fecha = request.form.get('fecha')
        monto = request.form.get('monto')

        cursor = mysql.connection.cursor()
        cursor.execute("""
        UPDATE Venta
        SET id_producto = %s,
            id_cliente = %s,
            talla = %s,
            color = %s,
            cantidad = %s,
            fecha = %s,
            monto= %s
        WHERE id_venta = %s
        """, (id_producto,id_cliente,talla,color,cantidad, fecha, monto, id ))
        mysql.connection.commit()
        return jsonify(response_object)

    except Exception as e:
        response_object = {'status': 'error'}
        response_object['message'] = f"Error al editar el registro: {e}"
        print(response_object)
        return jsonify(response_object)  

#CRUD CATEGORIA

@app.route('/categorias')
def categorias():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Categoria')
    data=cur.fetchall()
    lista=[]
    for cat in data:
        categoria = {
            'id_categoria': cat[0], 
            'nombre': cat[1], 
            'descripcion': cat[2], 
        }
        lista.append(categoria)
    return jsonify({'categorias': lista}) 

@app.route('/delete_categoria', methods=['DELETE'])
def delete_categoria():
    response = {'status': 'success'}
    id = request.form.get('id_categoria')
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Categoria WHERE id_categoria = %s', (id,))
    mysql.connection.commit()
    return jsonify(response)

@app.route('/add_categoria', methods=['POST'])
def add_categoria():
    if request.method == 'POST': #Define método de envío
        response = {'status': 'success'}
        nombre = request.form.get('nombre') # request.form recoge datos de formulario
        descripcion = request.form.get('descripcion')
        
        cur = mysql.connection.cursor() #genera conexion DB SQL
        cur.execute('INSERT INTO Categoria (nombre, descripcion) VALUES (%s, %s)', 
        (nombre, descripcion)) # ejecuta comando SLQ datos recogidos del form
        mysql.connection.commit() # Guarda cambios en DB
        return jsonify(response)

@app.route('/update_categoria', methods = ['PUT'])
def update_categoria():
    try:
        response_object = {'status': 'success'}
        id = str(request.form.get('id_categoria'))
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')

        cursor = mysql.connection.cursor()
        cursor.execute("""
        UPDATE Categoria 
        SET nombre = %s,
            descripcion = %s
        WHERE id_categoria = %s
        """, (nombre,descripcion, id ))
        mysql.connection.commit()
        return jsonify(response_object)

    except Exception as e:
        response_object = {'status': 'error'}
        response_object['message'] = f"Error al editar el registro: {e}"
        print(response_object)
        return jsonify(response_object)  

if __name__ == '__main__':
    app.run(port = 5000, debug = True)
