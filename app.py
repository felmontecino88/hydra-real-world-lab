from flask import Flask, request, render_template_string

app = Flask(__name__)

USERS = {
    "admin": "supersegura123",
    "soporte": "dragon", 
    "root": "root1234"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Panel de Administración Interno</title></head>
<body style="font-family: Arial, sans-serif; margin: 50px;">
    <h2>Login de Infraestructura</h2>
    {% if msg %}
        <p style="color: red;"><strong>{{ msg }}</strong></p>
    {% endif %}
    <form method="POST">
        Usuario: <br><input type="text" name="user"><br><br>
        Contraseña: <br><input type="password" name="pass"><br><br>
        <input type="submit" value="Ingresar">
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('pass')
        
        if username in USERS:
            if USERS[username] == password:
                return "<h1>¡BIENVENIDO AL PANEL DE CONTROL!</h1>"
            else:
                msg = f"La contrasenia para el usuario {username} es incorrecta"
        else:
            msg = "Usuario no encontrado"
            
    return render_template_string(HTML_TEMPLATE, msg=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)