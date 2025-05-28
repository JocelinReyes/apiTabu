from flask import Flask, request, jsonify, render_template
import math
import random

app = Flask(__name__)

def distancia(c1, c2):
    return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

def evaluar(ruta, ciudades):
    return sum(distancia(ciudades[ruta[i]], ciudades[ruta[i+1]]) for i in range(len(ruta)-1)) + distancia(ciudades[ruta[-1]], ciudades[ruta[0]])

def generar_vecinos(ruta):
    vecinos = []
    for i in range(len(ruta)):
        for j in range(i+1, len(ruta)):
            vecino = ruta[:]
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append(vecino)
    return vecinos

def busqueda_tabu(ciudades, max_iteraciones=100, tamaño_memoria=10):
    n = len(ciudades)
    ruta_actual = list(range(n))
    random.shuffle(ruta_actual)

    mejor_ruta = ruta_actual[:]
    mejor_distancia = evaluar(mejor_ruta, ciudades)

    memoria_tabu = []
    iteraciones = max_iteraciones

    while iteraciones > 0:
        iteraciones -= 1
        vecinos = generar_vecinos(ruta_actual)
        random.shuffle(vecinos)

        for vecino in vecinos:
            if vecino not in memoria_tabu:
                d_vecino = evaluar(vecino, ciudades)

                if d_vecino < evaluar(ruta_actual, ciudades):
                    ruta_actual = vecino[:]
                    memoria_tabu.append(vecino[:])
                    if len(memoria_tabu) > tamaño_memoria:
                        memoria_tabu.pop(0)
                    if d_vecino < mejor_distancia:
                        mejor_ruta = vecino[:]
                        mejor_distancia = d_vecino
                    break
                elif d_vecino < mejor_distancia:
                    ruta_actual = vecino[:]
                    memoria_tabu.append(vecino[:])
                    if len(memoria_tabu) > tamaño_memoria:
                        memoria_tabu.pop(0)
                    mejor_ruta = vecino[:]
                    mejor_distancia = d_vecino
                    break

    return mejor_ruta, mejor_distancia

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tabu', methods=['POST'])
def resolver_tabu():
    data = request.json
    ciudades = data['ciudades']
    iteraciones = int(data.get('iteraciones', 100))
    memoria = int(data.get('memoria', 10))

    mejor_ruta, distancia_total = busqueda_tabu(ciudades, iteraciones, memoria)

    return jsonify({
        'ruta': mejor_ruta,
        'distancia': round(distancia_total, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
