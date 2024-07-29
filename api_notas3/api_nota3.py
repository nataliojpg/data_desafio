import pymysql
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import urllib.parse
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
import pandas as pd
from pydantic import BaseModel
import os
from matplotlib import font_manager

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
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return 'data:image/png;base64,' + urllib.parse.quote(img_base64)

class CandidateRequest(BaseModel):
    name: str
    lastname: str

font_path = 'Poppins-Regular.ttf'
font_prop = font_manager.FontProperties(fname=font_path)

@app.get("/")
async def hallo():
    return '/candidate-grades3'

@app.post("/candidate-grades3", response_class=HTMLResponse)
async def main():

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        query = """
            "SELECT c.id_candidate, c.active, ga.professionality, ga.domain, ga.resilience, ga.social_hab, ga.leadership, ga.collaboration, ga.commitment, ga.initiative, ga.id_assessment
            FROM candidate c INNER JOIN grades_apt ga ON c.id_candidate = ga.id_candidate WHERE c.active = 1
        """
        cursor.execute(query)
        results2 = cursor.fetchall()

        if not results2:
            raise HTTPException(status_code=404, detail="Candidato no encontrado")

        df2 = pd.DataFrame(results2)

        df2_1 = df2[df2["id_assessment"] == 1]

        labels = ['professionality', 'domain', 'resilience', 'social_hab', 'leadership', 'collaboration', 'commitment', 'initiative']
        labels_esp = ['profesionalidad', 'dominio', 'resiliencia', 'hab_sociales', 'liderazgo', 'colaboración', 'compromiso', 'iniciativa']

        radar_chart1 = ""

        # Evaluación Grupal
        if not df2_1.empty:

            mean_data = df2_1[labels].mean().values


            mean_data = np.concatenate((mean_data, [mean_data[0]]))
    

            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
            angles += angles[:1]


            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.fill(angles, mean_data, color='#116249', alpha=0.25)
            ax.plot(angles, mean_data, color='#116249', linewidth=2)

    
            ax.set_yticklabels([])  
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels_esp, fontproperties=font_prop)  
            for label, angle in zip(ax.get_xticklabels(), angles):
                        x, y = label.get_position()
                        label.set_position((x, y + -0.15))
                        ax.set_ylim(0, 5)
                        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  # Ajusta los márgenes

            ax.set_ylim(0, 5)
            plt.show()

        else:
            print("No hay datos para la Evaluación Grupal")

       

        return HTMLResponse(content=f"""
        <html>
            <body>
                <img src="{radar_chart1}" alt="Evaluación Grupal">

            </body>
        </html>
        """)

    except Exception as e:
        print(f"Error: {e}")
        return HTMLResponse(content=f"""
        <html>
            <body>
                <h1>Error: {e}</h1>
                <img src="{radar_chart1}" alt="Evaluación Grupal">
            </body>
        </html>
        """)

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
