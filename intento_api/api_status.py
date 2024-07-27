from fastapi import FastAPI, HTTPException
import pymysql
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import urllib.parse
from fastapi.responses import HTMLResponse
import pandas as pd
import uvicorn

app = FastAPI()

DATABASE_CONFIG = {
    'host': HOST,
    'user': USER,
    'password': PASSWORD,
    'database': DATABASE,
    'port': 3306  
}

def get_db_connection():
    return pymysql.connect(**DATABASE_CONFIG)

def plot_to_base64(plt):
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return 'data:image/png;base64,' + urllib.parse.quote(string)

@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
    cursor.execute("SELECT candidate.id_status, candidate.active, status.name_status FROM candidate INNER JOIN status ON candidate.id_status = status.id_status;")
    results = cursor.fetchall()
    df1 = pd.DataFrame(results, columns=['id_status', 'active', 'name_status'])
    df1 = df1[df1['active'] == 1]
    stat_counts = df1['name_status'].value_counts()

    plt.figure(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(stat_counts, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 9})
    plt.title('Status de Candidatos Activos', fontsize=15)
    for autotext in autotexts:
        autotext.set_position((1.8 * autotext.get_position()[0], 1.8 * autotext.get_position()[1]))
    plt.legend(wedges, stat_counts.index, title="Status", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=10)
    status_img = plot_to_base64(plt)
    plt.close()

    cursor.close()
    conn.close()

    html_content = f"""
    <html>
    <body>
        <h1>Status de Candidatos Activos</h1>
        <img src="{status_img}" alt="Status de Candidatos Activos">
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
