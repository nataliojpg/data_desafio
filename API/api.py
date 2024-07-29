from fastapi import FastAPI, HTTPException
import pymysql
import pandas as pd
from fastapi.responses import JSONResponse
import uvicorn
import os

app = FastAPI()

DATABASE_CONFIG = {
    'host': os.getenv('HOST'),
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'database': os.getenv('DATABASE'),
    'port': 3306  
}

def get_db_connection():
    return pymysql.connect(**DATABASE_CONFIG)


@app.get("/")
def hola():
    return "/status"

@app.get("/status")
def get_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    cursor.execute("""
        SELECT candidate.id_status, candidate.active, status.name_status
        FROM candidate
        INNER JOIN status ON candidate.id_status = status.id_status
    """)
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=['id_status', 'active', 'name_status'])
    df = df[df['active'] == 1]
    stat_counts = df['name_status'].value_counts()
    
   
    data = {
        "labels": stat_counts.index.tolist(),
        "values": stat_counts.values.tolist()
    }

    cursor.close()
    conn.close()

    return JSONResponse(content=data)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

