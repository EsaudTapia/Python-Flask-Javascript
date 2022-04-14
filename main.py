import json
from flask import jsonify, request
from flask import Flask, render_template
from forms import Personaform
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@127.0.0.1:3307/flaskApi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #para que no de warning 
db=SQLAlchemy(app) #sqlalchemy te paso la config de app
ma=Marshmallow(app)


class Persona(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    nombre= db.Column(db.String(70), unique=True)
    apellido = db.Column(db.String(255))
  
    
    def __init__(self,nombre,apellido) :
        self.nombre=nombre
        self.apellido=apellido        

db.create_all()


class personaSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','apellido')
        
        
        
persona_schema= personaSchema()
personas_schema= personaSchema(many=True)


@app.route('/')
def index():
 personaform = Personaform()   
 return render_template('index.html',personaform=personaform)

@app.route('/listarpersonas')
def listarpersonas():
 allPerso=Persona.query.all()
 result= personas_schema.dump(allPerso)
 return jsonify(result) 
   


@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    print(output) # This is the output that was stored in the JSON within the browser
    print(type(output))
    result = json.loads(output) #this converts the json output to a python dictionary
    print(result) # Printing the new dictionary
    print(type(result))#this shows the json converted as a python dictionary
    
    if result.get('nombre') and result.get('apellido'):
          nombreper=result.get('nombre')
          apellidoper=result.get('apellido')
          nueva_persona=Persona(nombreper,apellidoper)
          db.session.add(nueva_persona)
          db.session.commit()
          mensaje= 'La persona {} {}, se ha Recibido y creado'.format( result.get('nombre'), result.get('apellido'))
          
          return jsonify({'mensaje':mensaje})
    
    return jsonify({'error':'no hay informacion'})



@app.route('/editar', methods=['POST'])
def editar():
    output = request.get_json()
    print(output) # This is the output that was stored in the JSON within the browser
    print(type(output))
    result = json.loads(output) #this converts the json output to a python dictionary
    print(result) # Printing the new dictionary
    print(type(result))#this shows the json converted as a python dictionary
    
    if result.get('nombre') and result.get('apellido'):
          id= result.get('id')
          persona=Persona.query.get(id)    
          nombreper= result.get('nombre')
          apellido= result.get('apellido')           
          persona.nombre= nombreper
          persona.apellido= apellido             
          db.session.commit()
          mensaje= 'La persona con id {}, se ha  editado a {} {}  '.format( result.get('id'),result.get('nombre'), result.get('apellido'))
          
          return jsonify({'mensaje':mensaje})
    
    return jsonify({'error':'no hay informacion'})  


@app.route('/eliminar', methods=['POST'])
def eliminar():
    output = request.get_json()
    print(output) # This is the output that was stored in the JSON within the browser
    print(type(output))
    result = json.loads(output) #this converts the json output to a python dictionary
    print(result) # Printing the new dictionary
    print(type(result))#this shows the json converted as a python dictionary
    
    if result.get('id'):
          id= result.get('id')
          persona=Persona.query.get(id)
          db.session.delete(persona)
          db.session.commit()
          mensaje= 'La persona con id {}, se ha  eliminado '.format( result.get('id'))
          
          return jsonify({'mensaje':mensaje})
    
    return jsonify({'error':'no hay informacion'})

if __name__=='__main__':
    app.run(debug=True,port=3000)