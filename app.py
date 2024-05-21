import os
from flask import Flask, render_template, request, redirect, url_for
import matplotlib
matplotlib.use('Agg')  # Utilizar el backend 'Agg' para evitar problemas de visualización

import matplotlib.pyplot as plt
from collections import defaultdict
import io
import base64

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configurar Matplotlib para usar una fuente específica
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial']

# Diccionario para almacenar los votos
votes = defaultdict(int)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        restaurant1 = request.form.get('restaurant1')
        restaurant2 = request.form.get('restaurant2')
        restaurant3 = request.form.get('restaurant3')
        
        if restaurant1:
            votes[restaurant1] += 1
        if restaurant2:
            votes[restaurant2] += 1
        if restaurant3:
            votes[restaurant3] += 1

        return redirect(url_for('results'))
    
    return render_template('index.html')

@app.route('/results')
def results():
    # Generar la gráfica de barras
    fig, ax = plt.subplots()
    restaurants = list(votes.keys())
    vote_counts = list(votes.values())
    
    ax.barh(restaurants, vote_counts, color='skyblue')
    ax.set_xlabel('Número de Votos')
    ax.set_title('Restaurantes Nominados para una Estrella Michelin en Pachuca')

    # Guardar la gráfica en un objeto BytesIO y convertirla a base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('results.html', plot_url=plot_url)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
