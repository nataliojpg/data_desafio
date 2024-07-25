from fastapi import FastAPI, HTTPException
import pymysql
import matplotlib.pyplot as plt
import io
import base64
import urllib.parse
from fastapi.responses import HTMLResponse
import pandas as pd
import numpy as np
import uvicorn


app = FastAPI()

DATABASE_CONFIG = {
    'host': 'el host',
    'user': 'admin',
    'password': 'la contraseña',
    'database': 'exe_database',
    'port': 3306  
}

def get_db_connection():
    return pymysql.connect(**DATABASE_CONFIG)

def plot_to_base64(plt):
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return 'data:image/png;base64,' + urllib.parse.quote(string)


# HOLA
#@app.get("/")
#def read_root():
    #return {"Estas son las gráficas"}

# STATS
@app.get("/", response_class=HTMLResponse)
def read_root():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Generar la gráfica de distribución de géneros
    cursor.execute("SELECT gender FROM candidate")
    results = cursor.fetchall()
    df1 = pd.DataFrame(results, columns=['gender'])
    gender_counts = df1['gender'].value_counts()

    plt.figure(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(gender_counts, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 9})
    plt.title('Distribución de Géneros', fontsize=15)
    for autotext in autotexts:
        autotext.set_position((1.8 * autotext.get_position()[0], 1.8 * autotext.get_position()[1]))
    plt.legend(wedges, gender_counts.index, title="Géneros", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)
    gender_img = plot_to_base64(plt)
    plt.close()

    # Generar la gráfica de radar para las evaluaciones
    cursor.execute("SELECT * FROM grades_apt")
    results2 = cursor.fetchall()
    df2 = pd.DataFrame(results2)
    def radar_chart(df, assessment_id, title):
        df_assessment = df[df["id_assessment"] == assessment_id]
        means = df_assessment[['professionality', 'domain', 'resilience', 'social_hab', 'leadership', 'collaboration', 'commitment', 'initiative']].mean().values
        labels = ['professionality', 'domain', 'resilience', 'social_hab', 'leadership', 'collaboration', 'commitment', 'initiative']
        means = np.concatenate((means, [means[0]]))
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, means, color='red', alpha=0.25)
        ax.plot(angles, means, color='red', linewidth=2)
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        plt.title(title)
        return plot_to_base64(plt)

    radar_img1 = radar_chart(df2, 1, 'Media de Aptitudes en CentroEvaluación')
    plt.close()
    radar_img2 = radar_chart(df2, 2, 'Media de Aptitudes en Evaluación 1')
    plt.close()
    radar_img3 = radar_chart(df2, 3, 'Media de Aptitudes en Evaluación 2')
    plt.close()

    cursor.close()
    conn.close()

    html_content = f"""
    <html>
    <body>
        <h1>Dashboard de Evaluaciones</h1>
        <h2>Distribución de Géneros</h2>
        <img src="{gender_img}" alt="Distribución de Géneros">

        <h2>Media de Aptitudes en Evaluación 1</h2>
        <img src="{radar_img1}" alt="Media de Aptitudes en Evaluación 1">

        <h2>Media de Aptitudes en Evaluación 2</h2>
        <img src="{radar_img2}" alt="Media de Aptitudes en Evaluación 2">

        <h2>Media de Aptitudes en Evaluación 3</h2>
        <img src="{radar_img3}" alt="Media de Aptitudes en Evaluación 3">
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

