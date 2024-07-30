from fastapi import FastAPI, HTTPException
from typing import Dict, Any, List, Optional
import pymysql
import pymysql.cursors 
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymysql.err import MySQLError
import uvicorn

app = FastAPI()

# Configuración de CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # O especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"], # O especifica los métodos permitidos
    allow_headers=["*"], # O especifica los encabezados permitidos
)

# Configuración de la conexión a la base de datos

DATABASE_CONFIG = {
    'host': os.getenv('HOST'),
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'database': os.getenv('DATABASE'),
    'port': 3306
}

# Ponderaciones de las aptitudes

weights = {
    'professionality': 0.08,
    'domain': 0.05,
    'resilience': 0.25,
    'social_hab': 0.15,
    'leadership': 0.12,
    'collaboration': 0.10,
    'commitment': 0.20,
    'initiative': 0.05
}

@app.get("/candidate/{email}")
async def get_candidate(email: str) -> Dict[str, Any]:
    connection = None
    try:
        # Conectar a la base de datos con DictCursor
        connection = pymysql.connect(**DATABASE_CONFIG, cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            # Consulta para obtener datos del candidato y sus fases
            query = """
                SELECT
                    g.id_assessment,
                    g.professionality,
                    g.domain,
                    g.resilience,
                    g.social_hab,
                    g.leadership,
                    g.collaboration,
                    g.commitment,
                    g.initiative,
                    c.first_name,
                    c.last_name
                FROM
                    grades_apt g
                INNER JOIN
                    candidate c ON g.id_candidate = c.id_candidate
                WHERE
                    c.email = %s
                ORDER BY
                    g.id_assessment
            """
            cursor.execute(query, (email,))
            results = cursor.fetchall()

            if not results:
                raise HTTPException(status_code=404, detail="No hay notas disponibles aún.")

            candidate_info = {
                "first_name": results[0]['first_name'],
                "last_name": results[0]['last_name'],
                "phases": []
            }

            total_score = 0
            phases_count = 0

            for phase in range(1, 4):
                phase_results = [r for r in results if r['id_assessment'] == phase]
                if phase_results:
                    phase_score = sum(phase_results[0][key] * weight for key, weight in weights.items())
                    candidate_info["phases"].append({
                        "phase": phase,
                        "score": phase_score
                    })
                    total_score += phase_score
                    phases_count += 1

            if phases_count > 0:
                average_score = total_score / phases_count
                percentage_score = round((average_score / 5) * 100)

                if percentage_score < 50:
                    comment = "El candidato no cumple con las expectativas."
                elif percentage_score <= 70:
                    comment = "El candidato se ajusta a las expectativas."
                elif percentage_score <= 90:
                    comment = "El candidato excede las expectativas."
                else:
                    comment = "El candidato es una opción ideal."

                candidate_info.update({
                    "average_score": f"La valoración media del candidato es {average_score}",
                    "percentage_score": f"El desempeño del candidato es del {percentage_score}%",
                    "comment": comment
                })

            return JSONResponse(content=candidate_info)

    except MySQLError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if connection:
            connection.close()
