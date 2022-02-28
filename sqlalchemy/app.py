from flask import Flask, render_template, request, session, redirect
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'app secret key'
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///noticias.sqlite3'
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#configurar ckeditor
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 400
#app.config['CKEDITOR_WIDTH'] = 1000
ckeditor = CKEditor(app)

db = SQLAlchemy(app)

class Noticia(db.Model):
    __tablename__ = 'noticias'
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100))
    cuerpo = db.Column(db.String(250))

def __init__(self, titulo, cuerpo):
    self.titulo = titulo
    self.cuerpo = cuerpo

db.create_all()

#prueba = Noticia(titulo='Titular 1 sql', cuerpo='Cuerpo 1 de sqsl')
#db.session.add(prueba)
#db.session.commit()

@app.route("/")
def raiz():
    #en un principio no somos admin.
    if 'administrador' not in session:
      session['administrador'] = "NO"
    return render_template('index.html', noticias = Noticia.query.all())

#visualizar una noticia
@app.route('/noticia')
def noticia():
    id = int(request.args.get('id'))
    noticia1 = Noticia.query.filter_by(id=id).first()
    return render_template("noticia.html", noticia=noticia1)  


#entrar en la pg de login
@app.route('/login', methods=["POST", "GET"])
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
        return redirect('/')
        #return render_template('index.html', noticias = Noticia.query.all()) 
    else:
        return render_template("login.html" ,error="SI") 

#cerrar sesión de admin
@app.route('/logout', methods=["POST"])
def logout():
    session["administrador"]="NO"
    return redirect('/')
    #return render_template('index.html', noticias = Noticia.query.all()) 

#crear nueva noticia
@app.route('/nueva')
def nueva():
    if session["administrador"] == "SI":
        return render_template("nueva.html", error="NO", modo="creacion", noticia = None)
    else:
        return render_template("erroradmin.html")

#ir a la pg de creación de noticia. Crear o editar noticia es la misma página
@app.route("/crearnoticia", methods=["POST"])
def crearnoticia():
    if session["administrador"] == "SI":
        return render_template("nueva.html", error="NO" , modo="creacion", noticia = None)
    else:
        return render_template("erroradmin.html")

#método del form de crear noticia.
@app.route('/nuevanoticia', methods=['POST'])
def crearnueva():
    titulo = request.form.get('titulo')
    cuerpo = request.form.get('ckeditor')
    if titulo == "" or cuerpo == "":
        return render_template("nueva.html", error="SI" , modo="creacion", noticia = None)
    else:
        nuevanoticia = Noticia(titulo=titulo, cuerpo=cuerpo)
        db.session.add(nuevanoticia)
        db.session.commit()

        return redirect('/')
        #return render_template('index.html', noticias = Noticia.query.all()) 


#ir a la pantalla de edición de noticia
@app.route("/editarnoticia")
def editarnoticia():
    id = int(request.args.get('id'))

    noticia1 = Noticia.query.filter_by(id=id).first()
    
    if session["administrador"] == "SI":
        return render_template("nueva.html", error="NO", modo="edicion",  noticia = noticia1)
    else:
        return render_template("erroradmin.html")

#editar una noticia
@app.route('/noticiaeditada', methods=['POST'])
def noticiaeditada():
    titulo = request.form.get('titulo')
    cuerpo = request.form.get('ckeditor')
    idnoticia = int(request.form.get('id'))
    noticia1 = Noticia.query.filter_by(id=idnoticia).first()
    if titulo == "" or cuerpo == "":
        return render_template("nueva.html", error="SI" , modo="edicion", noticia = noticia1)
    else:
        noticia1.titulo = titulo
        noticia1.cuerpo = cuerpo
        db.session.commit()

        return redirect('/')
        #return render_template('index.html', noticias = Noticia.query.all()) 

#eliminar una noticia
@app.route("/eliminarnoticia")
def eliminarnoticia():
    id = int(request.args.get('id'))
    
    if session["administrador"] == "SI":
        noticia1 = Noticia.query.filter_by(id=id).first()
        db.session.delete(noticia1)
        db.session.commit()
 
        return redirect('/')
        #return render_template('index.html', noticias = Noticia.query.all()) 
    else:
        return render_template("erroradmin.html")

 


@app.errorhandler(404)
def page_not_found(error):
    return 'Página no encontrada...', 404

if __name__ == "__main__":
    app.run()