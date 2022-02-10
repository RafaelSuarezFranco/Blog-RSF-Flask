from flask import Flask
from flask import render_template
from flask import request
from flask import session

app = Flask(__name__)
app.secret_key = 'app secret key'

listaadmin = ["juan", "lolo"]
listaadminclave = ["123", "abc"]
listainvitado = ["pepe", "alonso"]
listainvitadoclave = ["pepepe", "alonso1"]

listaid=[0, 1]
titulares=["Titular 1", "Titular 2"]
entradas=["Cuerpo 1", "Cuerpo 2"]

@app.route("/")
def raiz():
    return render_template('index.html', titulares=titulares, entradas=entradas, listaid=listaid)


@app.route('/noticia')
def noticia():
    id = request.args.get('id')
    titular = request.args.get('titular')
    entrada = request.args.get('entrada')

    return render_template("noticia.html" ,id=id,titular=titular, entrada=entrada)  



@app.route('/login')
def login():
    error = "NO"
    return render_template("login.html" ,error=error)  




@app.route("/login",methods=["POST"])
def acceder():
    #session["administrador"]="NO"
    error = "NO"
    return render_template("login.html" ,error=error)




@app.route("/acceso",methods=["POST"])
def acceso():
    usuario = request.form.get('usuario')
    clave = request.form.get('clave')
    session["usuario"]=usuario
    session["administrador"]="NO"
    error = "NO"
    usuarioexiste = False
    clavecorrecta = False

    if usuario == "" or clave == "":
        return render_template("index.html" ,error="SI")
    else:
        #comprobar si es admin
        contador = 0
        for u in listaadmin:
    
            if usuario == u:
                usuarioexiste = True
                if listaadminclave[contador] == clave:
                    print("administrador ok")
                    clavecorrecta = True
                    session["administrador"]="SI"
            contador = contador + 1
        
        contador = 0
        if usuarioexiste == False: #si no es admin, comprobamos si es invitado
            for u in listainvitado:
                
                if usuario == u:
                    usuarioexiste = True
                    if listainvitadoclave[contador] == clave:
                        print("invitado ok")
                        clavecorrecta = True
                        session["administrador"]="NO"
                contador = contador + 1
        
        if usuarioexiste == False or clavecorrecta == False:
            return render_template("index.html" ,error="SI")
        else:
            return render_template("ver.html", listainvitado=listainvitado, listaadmin=listaadmin)    
    


@app.route('/alta')
def alta():
    error = "NO"
    return render_template("alta.html" ,error=error)  
    


@app.route("/daralta",methods=["POST"])
def daralta():
    usuarionuevo = request.form.get("usuarionuevo")
    clavenueva = request.form.get("clavenueva")
    error = "NO"

    if usuarionuevo == "" or clavenueva == "":
        return render_template('alta.html', error="SI")       
    else:
        listaadmin.append(usuarionuevo)
        listaadminclave.append(clavenueva)
        return render_template("ver.html" , listainvitado=listainvitado, listaadmin=listaadmin) 
      

@app.route("/cerrarsesion",methods=["POST"])
def cerrarsesion():
    session["administrador"]="NO"
    error = "NO"
    return render_template("index.html" ,error=error)
   

@app.errorhandler(404)
def page_not_found(error):
    return 'Página no encontrada...', 404

if __name__ == "__main__":
    app.run()