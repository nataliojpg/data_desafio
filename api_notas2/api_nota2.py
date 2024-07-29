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

app = FastAPI()

# Configuración de la base de datos
DATABASE_CONFIG = {
    'host': 'database-1.ct46wkioy0f3.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'huevosrotosconjamon',
    'database': 'exe_database',
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

@app.get("/")
async def hallo():
    return FileResponse("index2.html")

@app.post("/candidate-grades2", response_class=HTMLResponse)
async def main(candidate: CandidateRequest):
    name = candidate.name
    lastname = candidate.lastname

    if not name or not lastname:
        raise HTTPException(status_code=400, detail="Es necesario poner el nombre y el apellido")
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        #conn = get_db_connection()
        #cursor = conn.cursor()

        query = """
            SELECT c.id_candidate, c.first_name, c.last_name, ga.professionality, ga.domain, ga.resilience, 
                   ga.social_hab, ga.leadership, ga.collaboration, ga.commitment, ga.initiative, ga.id_assessment 
            FROM candidate c 
            INNER JOIN grades_apt ga ON c.id_candidate = ga.id_candidate 
            WHERE c.first_name = %s AND c.last_name = %s
        """
        cursor.execute(query, (name, lastname))
        results2 = cursor.fetchall()

        if not results2:
            raise HTTPException(status_code=404, detail="Candidato no encontrado")

        df2 = pd.DataFrame(results2, columns=[
            'id_candidate', 'first_name', 'last_name', 'professionality', 'domain', 'resilience',
            'social_hab', 'leadership', 'collaboration', 'commitment', 'initiative', 'id_assessment'
        ])

        df2_1 = df2[df2["id_assessment"] == 2]

        labels = ['professionality', 'domain', 'resilience', 'social_hab', 'leadership', 'collaboration', 'commitment', 'initiative']

        radar_chart1 = ""

        # Evaluación Grupal
        if not df2_1.empty:
            data = df2_1.iloc[0][labels].values
            data = np.concatenate((data, [data[0]]))
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
            angles += angles[:1]
#
            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.fill(angles, data, color='red', alpha=0.25)
            ax.plot(angles, data, color='red', linewidth=2)
            ax.set_yticklabels([])  
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels)
            for label, angle in zip(ax.get_xticklabels(), angles):
                x, y = label.get_position()
                label.set_position((x, y + -0.1))
            ax.set_ylim(0, 5)
            plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  # Ajusta los márgenes


            radar_chart1 = plot_to_base64(plt)
            plt.close(fig)

       

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
