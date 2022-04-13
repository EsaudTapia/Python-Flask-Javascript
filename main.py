import json

from flask import jsonify, request

from flask import Flask, render_template

from forms import Persona

app = Flask(__name__)



@app.route('/')
def index():
 persona = Persona()   
 return render_template('index.html',persona=persona)


@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    print(output) # This is the output that was stored in the JSON within the browser
    print(type(output))
    result = json.loads(output) #this converts the json output to a python dictionary
    print(result) # Printing the new dictionary
    print(type(result))#this shows the json converted as a python dictionary
    
    if result.get('nombre') and result.get('apellido'):
          mensaje= 'La persona {} {}, se ha Recibido'.format( result.get('nombre'), result.get('apellido'))
          
          return jsonify({'mensaje':mensaje})
    
    return jsonify({'error':'no hay informacion'})


if __name__=='__main__':
    app.run(debug=True,port=3000)