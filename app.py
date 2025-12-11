import matplotlib
matplotlib.use('Agg') # Indispensable pour un serveur sans écran
import matplotlib.pyplot as plt
import gpxpy
import io
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return """
    <style>body{font-family:sans-serif;background:#0f172a;color:white;text-align:center;padding:50px;}</style>
    <h1>⚡ Runnatic Poster Generator</h1>
    <p>Le backend est en ligne et fonctionnel.</p>
    """

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # 1. Récupérer les infos envoyées par ton site
        if 'gpxfile' not in request.files:
            return "Aucun fichier envoyé", 400
        
        file = request.files['gpxfile']
        race_name = request.form.get('racename', 'COURSE RUNNATIC')
        race_time = request.form.get('racetime', '--:--')
        user_color = request.form.get('color', '#22c55e')

        # 2. Lire le GPX
        gpx = gpxpy.parse(file)
        lat = []
        lon = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    lat.append(point.latitude)
                    lon.append(point.longitude)

        # 3. Dessiner l'affiche
        fig = plt.figure(figsize=(10, 14), facecolor='black')
        
        # Zone du tracé
        ax = plt.Axes(fig, [0.05, 0.25, 0.9, 0.7]) 
        ax.set_facecolor("black")
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # Le tracé
        ax.plot(lon, lat, color=user_color, linewidth=5, alpha=0.9, solid_capstyle='round')
        ax.axis('equal')

        # Les Textes
        # Nom de la course
        fig.text(0.5, 0.18, race_name.upper(), color='white', fontsize=35, fontweight='bold', ha='center')
        
        # Temps
        fig.text(0.5, 0.12, race_time, color=user_color, fontsize=30, fontweight='bold', ha='center', fontname='Monospace')
        
        # Copyright (CORRIGÉ : J'ai retiré letter_spacing)
        fig.text(0.5, 0.08, "RUNNATIC OFFICIAL FINISHER", color='#555555', fontsize=12, ha='center')

        # 4. Sauvegarder dans la mémoire tampon (RAM)
        img_io = io.BytesIO()
        plt.savefig(img_io, format='png', facecolor='black', dpi=150, bbox_inches='tight')
        img_io.seek(0)
        plt.close()

        # 5. Renvoyer l'image au navigateur
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=f'Runnatic_{race_name}.png')

    except Exception as e:
        return f"Erreur: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
