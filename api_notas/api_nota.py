import pymysql
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import urllib.parse
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import pandas as pd
import os

app = FastAPI()

# Configuración de la base de datos
DATABASE_CONFIG = {
    'host': os.getenv('HOST'),
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'database': os.getenv('DATABASE'),
    'port': 3306 
}

def get_db_connection():
    return pymysql.connect(**DATABASE_CONFIG)

def plot_to_base64(plt):
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    # Convertir la imagen en base64
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return 'data:image/png;base64,' + urllib.parse.quote(img_base64)

def generate_radar_chart(data, labels, title):
    data = np.concatenate((data, [data[0]]))
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, data, color='red', alpha=0.25)
    ax.plot(angles, data, color='red', linewidth=2)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    plt.title(title)

    return plot_to_base64(plt)

@app.get("/", response_class=HTMLResponse)
async def main():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT c.id_candidate, c.first_name, c.last_name, ga.professionality, ga.domain, ga.resilience, 
                   ga.social_hab, ga.leadership, ga.collaboration, ga.commitment, ga.initiative, ga.id_assessment 
            FROM candidate c 
            INNER JOIN grades_apt ga ON c.id_candidate = ga.id_candidate 
            WHERE first_name = 'Scottie' AND last_name = 'Cardo'
        """
        cursor.execute(query)
        results2 = cursor.fetchall()

        df2 = pd.DataFrame(results2, columns=[
            'id_candidate', 'first_name', 'last_name', 'professionality', 'domain', 'resilience',
            'social_hab', 'leadership', 'collaboration', 'commitment', 'initiative', 'id_assessment'
        ])

        df2_1 = df2[df2["id_assessment"] == 1]
        df2_2 = df2[df2["id_assessment"] == 2]
        df2_3 = df2[df2["id_assessment"] == 3]

        labels = ['professionality', 'domain', 'resilience', 'social_hab', 'leadership', 'collaboration', 'commitment', 'initiative']

        # Evaluación Grupal
        if not df2_1.empty:
            data = df2_1.iloc[0][labels].values
            data = np.concatenate((data, [data[0]]))
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.fill(angles, data, color='red', alpha=0.25)
            ax.plot(angles, data, color='red', linewidth=2)
            ax.set_yticklabels([])  
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels)
            ax.set_ylim(0, 5)
            plt.title('Evaluación Grupal')

            radar_chart1 = plot_to_base64(plt)
            plt.close(fig)
        else:
            radar_chart1 = "No hay datos para la Evaluación Grupal"

        # Evaluación 1
        if not df2_2.empty:
            data = df2_2.iloc[0][labels].values
            data = np.concatenate((data, [data[0]]))
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.fill(angles, data, color='green', alpha=0.25)
            ax.plot(angles, data, color='green', linewidth=2)
            ax.set_yticklabels([])  
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels)
            ax.set_ylim(0, 5)
            plt.title('Evaluación 1')

            radar_chart2 = plot_to_base64(plt)
            plt.close(fig)
        else:
            radar_chart2 = "No hay datos para la Evaluación 1"

        # Evaluación 2
        if not df2_3.empty:
            data = df2_3.iloc[0][labels].values
            data = np.concatenate((data, [data[0]]))
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.fill(angles, data, color='blue', alpha=0.25)
            ax.plot(angles, data, color='blue', linewidth=2)
            ax.set_yticklabels([])  
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels)
            ax.set_ylim(0, 5)
            plt.title('Evaluación 2')

            radar_chart3 = plot_to_base64(plt)
            plt.close(fig)
        else:
            radar_chart3 = "No hay datos para la Evaluación 2"

        return HTMLResponse(content=f"""
        <html>
            <body>
                <h1>Evaluaciones de Scottie Cardo</h1>
                <h2>Evaluación 1</h2>
                <img src="{radar_chart1}" alt="Evaluación Grupal">
                <h2>Evaluación 2</h2>
                <img src="{radar_chart2}" alt="Evaluación 1">
                <h2>Evaluación 3</h2>
                <img src="{radar_chart3}" alt="Evaluación 2">
            </body>
        </html>
        """)

    except Exception as e:
        print(f"Error: {e}")
        return HTMLResponse(content=f"<html><body><h1>Error: {e}</h1></body></html>")

    finally:
        cursor.close()
        conn.close()


     

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)