from flask import Flask, jsonify, request
import googlemaps, json, requests, base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/ejercicio1', methods=['POST'])
def ejercicio1():
    try:
        origen = request.json['origen']
        destino = request.json['destino']
    except:
        resp_json = "{\"error\": \"no se especifico el origen\"}"
        return resp_json, 400
    
    try:
        maps = googlemaps.Client(key='AIzaSyAzzrnc71pLvEvOdY322DQwwbUsFQZT7Vg')
        resp = maps.directions(origen,destino)
    except:
        resp_json = "{\"error\": \"Error de Google Maps\"}"
        return resp_json, 500

    resp_json = "{\"ruta\":["

    for x in range(len(resp[0]['legs'][0]['steps'])):
        resp_json += "{\"lat\":"
        resp_json += str(resp[0]['legs'][0]['steps'][x]['start_location']['lat'])
        resp_json += ", "
        resp_json += "\"lon\":"
        resp_json += str(resp[0]['legs'][0]['steps'][x]['start_location']['lng'])
        resp_json += "}, "
        if x == len(resp[0]['legs'][0]['steps']) - 1:
            resp_json += "{\"lat\":"
            resp_json += str(resp[0]['legs'][0]['steps'][x]['end_location']['lat'])
            resp_json += ", "
            resp_json += "\"lon\":"
            resp_json += str(resp[0]['legs'][0]['steps'][x]['end_location']['lng'])
            resp_json += "} "
    
    resp_json += "]}"
    print (resp_json)
    return resp_json, 201

@app.route('/ejercicio2', methods=['POST'])
def ejercicio2():
    try:
        origen = request.json['origen']
    except:
        resp_json = "{\"error\": \"no se especifico el origen\"}"
        return resp_json, 400

    try:
        maps = googlemaps.Client(key='AIzaSyCf2TIfdRHOMobsTot_vEnTQVnPrX9mzeU')
        geocode_result = maps.geocode(origen)
    
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']

        resp = maps.places_nearby((lat,lng),500,type='restaurant')
    except:
        resp_json = "{\"error\": \"Error de Google Maps\"}"
        return resp_json, 500

    resp_json = "{\"restaurantes\":["

    for x in range(len(resp['results'])):
        resp_json += "{\"nombre\":\""
        resp_json += str(resp['results'][x]['name'])
        resp_json += "\", "
        resp_json += "\"lat\":"
        resp_json += str(resp['results'][x]['geometry']['location']['lat'])
        resp_json += ", "
        resp_json += "\"lon\":"
        resp_json += str(resp['results'][x]['geometry']['location']['lng'])
        if x == len(resp['results']) - 1:
            resp_json += "} "
        else:
            resp_json += "}, "
    
    resp_json += "]}"

    return resp_json, 201

@app.route('/ejercicio3', methods=['POST'])
def ejercicio3():
    try:
        nombre = request.json['nombre']
        data = request.json['data']
    except:
        resp_json = "{\"error\": \"no se especifico el origen\"}"
        return resp_json, 400

    try:
        image = Image.open(BytesIO(base64.b64decode(data)))
    except:
        resp_json = "{\"error\": \"Error, intente de nuevo.\"}"
        return resp_json, 500

    width, height = image.size

    BWImage = Image.new('RGB', (width,height))
    pixels = BWImage.load()

    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x,y))
            R,G,B = pixel
            
            luminosity = 0.21 * R + 0.72 * G + 0.07 * B

            R = int(luminosity)
            G = int(luminosity)
            B = int(luminosity)

            newPixel = R,G,B

            BWImage.putpixel((x,y),(newPixel))
    
    try:
        BWImage.save(nombre)
        with open(nombre, "rb") as img:
            BWData = base64.b64encode(img.read())
        data = str(BWData)
        data = data[2:-1] 
    except:
        resp_json = "{\"error\": \"Error, intente de nuevo.\"}"
        return resp_json, 500

    array = nombre.split(".")
    resp_json = "{\"nombre\": \""
    resp_json += array[0]
    resp_json += "(blanco y negro)."
    resp_json += array[1]
    resp_json += "\", \"data\": \""
    resp_json += data
    resp_json += "\"}"

    return resp_json, 201

@app.route('/ejercicio4', methods=['POST'])
def ejercicio4():
    try:
        nombre = request.json['nombre']
        data = request.json['data']
        tamano = request.json['tamaño']
    except:
        resp_json = "{\"error\": \"no se especifico el origen\"}"
        return resp_json, 400

    try:
        image = Image.open(BytesIO(base64.b64decode(data)))
    except:
        resp_json = "{\"error\": \"Error, intente de nuevo.\"}"
        return resp_json, 500

    width, height = image.size

    if tamano['alto'] > height or tamano['ancho'] > width:
         resp_json = "{\"error\": \"Tamaño pedido es mas grande que la imagen original.\"}"
         return resp_json, 500

    DivX = width/tamano['ancho']
    DivY = height/tamano['alto']

    ResizedWidth = int(width/DivX)
    ResizedHeight = int(height/DivY)

    ResizedImage = Image.new('RGB',(ResizedWidth, ResizedHeight))
    pixels = ResizedImage.load()

    for x in range(tamano['ancho']):
        for y in range(tamano['alto']):
            pixels = image.getpixel((x * DivX, y * DivY))
            ResizedImage.putpixel((x, y), pixels)

    try:
        ResizedImage.save(nombre)
        with open(nombre, "rb") as img:
            ResizedData = base64.b64encode(img.read())
        data = str(ResizedData)
        data = data[2:-1] 
    except:
        resp_json = "{\"error\": \"Error, intente de nuevo.\"}"
        return resp_json, 500

    array = nombre.split(".")
    resp_json = "{\"nombre\": \""
    resp_json += array[0]
    resp_json += "(reducida)."
    resp_json += array[1]
    resp_json += "\", \"data\": \""
    resp_json += data
    resp_json += "\"}"

    return resp_json, 201

if __name__ == '__main__':
    app.run(port=8080, debug=True)
