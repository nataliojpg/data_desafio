![Banner](./img/banna.jpg)
# Data Science - Proyecto para EmpiezaPorEducar

## Descripción del Proyecto
Este proyecto forma parte de una colaboración entre los equipos de Data Science, Full Stack y Ciberseguridad para la ONG Empieza Por Educar. El objetivo del proyecto es optimizar y gestionar la información de los candidatos mediante una base de datos alojada en **AWS** y una serie de APIs que permiten obtener datos. La estructura de la base de datos fue diseñada en conjunto con el equipo de Full Stack, teniendo en cuenta las necesidades específicas de la ONG.


## Estructura del Repositorio
El repositorio está organizado de la siguiente manera:

• **CSVs/:** Carpeta que contiene los archivos CSV con datos de prueba para las tablas de la base de datos.

• **API/:** Carpeta que contiene la implementación de la API para las gráficas.

    ↪ api.py: Código fuente de la API (utiliza Python, MySQL, Pandas y Uvicorn).
    
    ↪ requirements.txt: Lista de dependencias necesarias para ejecutar la API.
    
• **FILTER/:** Carpeta que contiene el código para el filtro de desempeño de los candidatos en las evaluaciones.

    ↪ api_grades_filter.py: Código fuente del filtro de desempeño (utiliza Python, FastAPI y Uvicorn).
    
    ↪ requirements.txt: Lista de dependencias necesarias para ejecutar el filtro.


## Detalles Técnicos
• **Base de Datos**

La base de datos se encuentra alojada en la nube de AWS y se ha implementado utilizando MySQL. Las tablas fueron creadas y se han cargado datos de ejemplo desde los archivos CSV ubicados en la carpeta CSVs.

• **API para Gráficas**

La API proporciona varios endpoints que devuelven datos en formato JSON, los cuales son utilizados para generar gráficas en la web. Los endpoints disponibles son los siguientes:

    ↪ /status: Estado del proceso de los candidatos activos.

    ↪ /notas-evalgrupal: Media de notas en la evaluación grupal.

    ↪ /notas-eval1: Media de notas en la evaluación personal 1.

    ↪ /notas-eval2: Media de notas en la evaluación personal 2.

    ↪ /generos: Distribución por géneros.

    ↪ /registros: Registro de candidatos por mes.

    ↪ /academic: Nivel académico de candidatos.

    ↪ /nivel-ingles: Nivel de inglés de candidatos.

    ↪ /reclutadores: Actividad por reclutador.

• **Filtro de Desempeño**

El filtro de desempeño de los candidatos clasifica las evaluaciones en base a los siguientes umbrales (se le hicieron ponderaciones a las aptitudes):

Porcentaje de menos del 50%: No apto.

Entre 50% y 70%: Cumple con las expectativas.

Entre 70% y 90%: Excede las expectativas.

Entre 90% y 100%: Ideal.


## Herramientas

    ✦ Python

    ✦ FastAPI

    ✦ MySQL

    ✦ Pandas

    ✦ Uvicorn
