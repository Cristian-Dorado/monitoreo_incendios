# Monitoreo de Incendios - Dashboard
Monitoreo de Incendios y Alerta Temprana

https://monitoreo-de-incendios.onrender.com/
![cap_america_sat](https://github.com/Cristian-Dorado/monitoreo_incendios/assets/113219668/0471537f-9aa7-4fd9-9d8b-f9dfa5ce6ccd)


## Descripción

Este proyecto Personal surge como respuesta a la creciente problemática de incendios descontrolados en Bolivia, afectando gravemente la flora, fauna y el ecosistema en general. La falta de recursos y entidades dedicadas al monitoreo y respuesta oportuna de estos desastres naturales motivó la creación de este Dashboard de Monitoreo de Incendios.

## Objetivo

El objetivo principal es proporcionar a la sociedad una herramienta accesible y dinámica para el monitoreo en tiempo real de incendios en América del Sur, con un enfoque especial en Bolivia. La información se extrae de la API Administrada por la NASA, utilizando datos de incendios activos en tiempo casi real (NRT) desde el espectrorradiómetro de imágenes de resolución moderada (MODIS) a bordo de los satelites Aqua y Terra. Estos datos estan disponibles dentro de las 3 horas posteriores a la observación satelital.

## Características Principales

- **Dashboard Dinámico:** Desarrollado en Python utilizando la librería Plotly Dash.
- **Filtrado Personalizado:** Permite al usuario seleccionar la región de interés, proporcionando datos específicos sobre incendios en Bolivia o en toda América del Sur.
- **Datos en Tiempo Real:** Utiliza la API de la NASA para acceder a datos actualizados casi en tiempo real.

## Uso

1. **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/Cristian-Dorado/monitoreo_incendios.git
    ```

2. **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Ejecutar la Aplicación:**
    ```bash
    python app.py
    ```

## Contribuciones

¡Contribuciones y sugerencias son bienvenidas! Si encuentras algún problema o tienes ideas para mejorar el proyecto, por favor, abre un problema o envía un pull request.

## Enlaces Importantes

- **Repositorio GitHub:** [Monitoreo de Incendios](https://github.com/Cristian-Dorado/monitoreo_incendios)
