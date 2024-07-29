from fastapi import FastAPI, HTTPException
import pymysql
import pandas as pd
from fastapi.responses import JSONResponse
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware
import re


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],  # O especifica los métodos permitidos
    allow_headers=["*"],  # O especifica los encabezados permitidos
)

DATABASE_CONFIG = {
    'host': os.getenv('HOST'),
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'database': os.getenv('DATABASE'),
    'port': 3306  
}


def get_db_connection():
    return pymysql.connect(**DATABASE_CONFIG)

# INICIO
@app.get("/")
def hola():
    return "Apis"

# DATA STATUS ACTIVOS
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


# DATA MEDIA NOTA EVAL GRUPAL ACTIVOS
@app.get("/notas-evalgrupal", response_class=JSONResponse)
async def main():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
            SELECT c.id_candidate, c.active, ga.professionality, ga.domain, ga.resilience, ga.social_hab, ga.leadership, ga.collaboration, ga.commitment, ga.initiative, ga.id_assessment
            FROM candidate c INNER JOIN grades_apt ga ON c.id_candidate = ga.id_candidate WHERE c.active = 1
        """
        cursor.execute(query)
        results2 = cursor.fetchall()

        if not results2:
            raise HTTPException(status_code=404, detail="No se encontraron candidatos activos")

        df2 = pd.DataFrame(results2, columns=[
            'id_candidate', 'active', 'professionality', 'domain', 'resilience',
            'social_hab', 'leadership', 'collaboration', 'commitment', 'initiative', 'id_assessment'
        ])

        df2_1 = df2[df2["id_assessment"] == 1]

        labels = ['professionality', 'domain', 'resilience', 'social_hab', 'leadership', 'collaboration', 'commitment', 'initiative']
        labels_esp = ['profesionalidad', 'dominio', 'resiliencia', 'hab_sociales', 'liderazgo', 'colaboración', 'compromiso', 'iniciativa']

        if not df2_1.empty:
            mean_data = df2_1[labels].mean().values.tolist()
            return JSONResponse(content={"labels": labels_esp, "values": mean_data})

        raise HTTPException(status_code=404, detail="No hay datos de evaluación grupal para los candidatos activos")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# DATA MEDIA NOTA EVAL 1 ACTIVOS
@app.get("/notas-eval1", response_class=JSONResponse)
async def main2():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
            SELECT c.id_candidate, c.active, ga.professionality, ga.domain, ga.resilience, ga.social_hab, ga.leadership, ga.collaboration, ga.commitment, ga.initiative, ga.id_assessment
            FROM candidate c INNER JOIN grades_apt ga ON c.id_candidate = ga.id_candidate WHERE c.active = 1
        """
        cursor.execute(query)
        results2 = cursor.fetchall()

        if not results2:
            raise HTTPException(status_code=404, detail="No se encontraron candidatos activos")

        df2 = pd.DataFrame(results2, columns=[
            'id_candidate', 'active', 'professionality', 'domain', 'resilience',
            'social_hab', 'leadership', 'collaboration', 'commitment', 'initiative', 'id_assessment'
        ])

        df2_1 = df2[df2["id_assessment"] == 2]

        labels = ['professionality', 'domain', 'resilience', 'social_hab', 'leadership', 'collaboration', 'commitment', 'initiative']
        labels_esp = ['profesionalidad', 'dominio', 'resiliencia', 'hab_sociales', 'liderazgo', 'colaboración', 'compromiso', 'iniciativa']

        if not df2_1.empty:
            mean_data = df2_1[labels].mean().values.tolist()
            return JSONResponse(content={"labels": labels_esp, "values": mean_data})

        raise HTTPException(status_code=404, detail="No hay datos de evaluación grupal para los candidatos activos")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# DATA MEDIA NOTA EVAL 2 ACTIVOS
@app.get("/notas-eval2", response_class=JSONResponse)
async def main3():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
            SELECT c.id_candidate, c.active, ga.professionality, ga.domain, ga.resilience, ga.social_hab, ga.leadership, ga.collaboration, ga.commitment, ga.initiative, ga.id_assessment
            FROM candidate c INNER JOIN grades_apt ga ON c.id_candidate = ga.id_candidate WHERE c.active = 1
        """
        cursor.execute(query)
        results2 = cursor.fetchall()

        if not results2:
            raise HTTPException(status_code=404, detail="No se encontraron candidatos activos")

        df2 = pd.DataFrame(results2, columns=[
            'id_candidate', 'active', 'professionality', 'domain', 'resilience',
            'social_hab', 'leadership', 'collaboration', 'commitment', 'initiative', 'id_assessment'
        ])

        df2_1 = df2[df2["id_assessment"] == 3]

        labels = ['professionality', 'domain', 'resilience', 'social_hab', 'leadership', 'collaboration', 'commitment', 'initiative']
        labels_esp = ['profesionalidad', 'dominio', 'resiliencia', 'hab_sociales', 'liderazgo', 'colaboración', 'compromiso', 'iniciativa']

        if not df2_1.empty:
            mean_data = df2_1[labels].mean().values.tolist()
            return JSONResponse(content={"labels": labels_esp, "values": mean_data})

        raise HTTPException(status_code=404, detail="No hay datos de evaluación grupal para los candidatos activos")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# DATA GENEROS
@app.get("/generos", response_class=JSONResponse)
async def generos():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
            SELECT c.gender
            FROM candidate c WHERE c.active = 1
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            raise HTTPException(status_code=404, detail="No se encontraron candidatos activos")

        df = pd.DataFrame(results, columns=['gender'])
        gender_counts = df['gender'].value_counts().to_dict()

        return JSONResponse(content={"labels": list(gender_counts.keys()), "values": list(gender_counts.values())})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


# DATA REGISTROS X MES
@app.get("/registros", response_class=JSONResponse)
async def registros():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
            SELECT registration_date
            FROM candidate
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            raise HTTPException(status_code=404, detail="No se encontraron registros")


        df = pd.DataFrame(results, columns=['registration_date'])

    
        month_pattern = re.compile(r'(\d{4}-\d{2})')


        df['month'] = df['registration_date'].apply(lambda x: month_pattern.match(x).group(1) if month_pattern.match(x) else None)


        month_counts = df['month'].value_counts().sort_index().to_dict()


        labels = list(month_counts.keys())
        values = list(month_counts.values())

        return JSONResponse(content={"labels": labels, "values": values})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# DATA NIVEL ACADEMICO
@app.get("/academic", response_class=JSONResponse)
async def academic():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
            SELECT academic_degree
            FROM form
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            raise HTTPException(status_code=404, detail="No se encontraron niveles académicos")
        print("Results:", results)

        df = pd.DataFrame(results, columns= 'academic_degree')

        adegree_counts = df['academic_degree'].value_counts().sort_index().to_dict()
        labels = list(adegree_counts.keys())
        values = list(adegree_counts.values())

        return JSONResponse(content={"labels": labels, "values": values})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# DATA NIVEL INGLES
@app.get("/nivel-ingles", response_class=JSONResponse)
async def nivel_ingles():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
            SELECT languages
            FROM form
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            raise HTTPException(status_code=404, detail="No se encontraron niveles de inglés")
        
        print("Results:", results)

        df = pd.DataFrame(results, columns='languages')

        nivel_counts = df['languages'].value_counts().sort_index().to_dict()
        labels = list(nivel_counts.keys())
        values = list(nivel_counts.values())

        return JSONResponse(content={"labels": labels, "values": values})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

