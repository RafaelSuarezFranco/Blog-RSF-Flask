from flask import Flask, render_template, request, session
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'app secret key'

#configurar ckeditor
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 400
#app.config['CKEDITOR_WIDTH'] = 1000
ckeditor = CKEditor(app)

listaid=[0, 1]
titulares=["Titular 1", "Titular 2"]
entradas=["Cuerpo 1", "Cuerpo 2"]



@app.route("/")
def raiz():
    #en un principio no somos admin.
    if 'administrador' not in session:
      session['administrador'] = "NO"

    #if session["administrador"] != "SI":
    #    session["administrador"]="NO"
    return render_template('index.html', titulares=titulares, entradas=entradas, listaid=listaid)

#visualizar una noticia
@app.route('/noticia')
def noticia():
    id = int(request.args.get('id'))
    #indice = listaid.index(id)
    titular = titulares[id]
    entrada = entradas[id]
    return render_template("noticia.html", titular=titular, entrada=entrada)  


#entrar en la pg de login
@app.route('/login', methods=["POST"])
def login():
    error = "NO"
    return render_template("login.html" ,error=error)  

#logearse como admin
@app.route("/acceder",methods=["POST"])
def accederadmin():
    usuario = request.form.get('usuario')
    clave = request.form.get('clave')

    if usuario == "admin" and clave == "password":
        session["administrador"]="SI"
        return render_template('index.html', titulares=titulares, entradas=entradas, listaid=listaid)
    else:
        return render_template("login.html" ,error="SI") 

#cerrar sesión de admin
@app.route('/logout', methods=["POST"])
def logout():
    session["administrador"]="NO"
    return render_template('index.html', titulares=titulares, entradas=entradas, listaid=listaid)  

#crear nueva noticia
@app.route('/nueva')
def nueva():
    if session["administrador"] == "SI":
        return render_template("nueva.html", indice="ninguno", modo="creacion", titulares=titulares, entradas=entradas)
    else:
        return render_template("erroradmin.html")

#ir a la pg de creación de noticia. Crear o editar noticia es la misma página
@app.route("/crearnoticia", methods=["POST"])
def crearnoticia():
    if session["administrador"] == "SI":
        return render_template("nueva.html", indice="ninguno", modo="creacion", titulares=titulares, entradas=entradas)
    else:
        return render_template("erroradmin.html")

#método del form de crear noticia.
@app.route('/nuevanoticia', methods=['POST'])
def crearnueva():
    titulo = request.form.get('titulo')
    cuerpo = request.form.get('ckeditor')
    ultimoid = 0
    try: # en caso de que borremos todas las noticias, esto puede causar problemas
        ultimoid = listaid[-1]
    except Exception:
        ultimoid = -1
    nuevoid = ultimoid + 1
    listaid.append(nuevoid)
    titulares.append(titulo)
    entradas.append(cuerpo)
    return render_template('index.html', titulares=titulares, entradas=entradas, listaid=listaid)


#ir a la pantalla de edición de noticia
@app.route("/editarnoticia")
def editarnoticia():
    id = int(request.args.get('id'))
    indice = listaid.index(id)
    if session["administrador"] == "SI":
        return render_template("nueva.html", indice=indice, modo="edicion", titulares=titulares, entradas=entradas)
    else:
        return render_template("erroradmin.html")

#editar una noticia
@app.route('/noticiaeditada', methods=['POST'])
def noticiaeditada():
    titulo = request.form.get('titulo')
    cuerpo = request.form.get('ckeditor')
    indice = int(request.form.get('indice'))
    titulares[indice] = titulo
    entradas[indice] = cuerpo
    return render_template('index.html', titulares=titulares, entradas=entradas, listaid=listaid)

#eliminar una noticia
@app.route("/eliminarnoticia")
def eliminarnoticia():
    id = int(request.args.get('id'))
    
    if session["administrador"] == "SI":
        titulares.pop(id)
        entradas.pop(id)
        global listaid
        listaid = list(range(0, len(titulares)))
        return render_template('index.html', titulares=titulares, entradas=entradas, listaid=listaid)
    else:
        return render_template("erroradmin.html")

 


@app.errorhandler(404)
def page_not_found(error):
    return 'Página no encontrada...', 404

if __name__ == "__main__":
    app.run()