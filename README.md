# EmotionalBETO

**Análisis de emociones en español basado en BERT**

EmotionalBETO es una herramienta de procesamiento de lenguaje natural diseñada para identificar la emoción predominante en textos en español. Incorpora un sistema de inferencia basado en modelos BERT, acompañado de visualización avanzada de probabilidades y heurísticas de detección de sarcasmo y nivel de urgencia. Además, sugiere respuestas automáticas adaptadas al contexto emocional.

*Despliegue*: https://huggingface.co/spaces/Dannzho/EmotionalBETO

## Características principales

- **Clasificación de emociones:** Detección automática de la emoción principal en el texto de entrada.
- **Distribución de probabilidades:** Visualización mediante gráfica de barras para mayor transparencia.
- **Heurísticas inteligentes:** Análisis de sarcasmo y urgencia para mensajes destacados.
- **Sugerencias contextuales:** Generación de una respuesta recomendada basada en el diagnóstico de emociones.
- **Evaluación y tests automáticos:** Scripts para evaluación rápida e integración de pruebas unitarias con `pytest`.

## Contenido del repositorio

- `emotional_bert.py`: Interfaz principal basada en Gradio para interacción rápida.
- `app.py`: Entrada compatible con Hugging Face Spaces.
- `emotion_core.py`: Núcleo del modelo, lógica de inferencia y heurísticas.
- `evaluate.py`: Script para evaluación y métricas del modelo.
- `data/sample_eval.csv`: Dataset de muestra para tests y benchmarking.
- `tests/`: Suite de pruebas automatizadas.
- `requirements.txt`: Dependencias del proyecto.
- `Dockerfile` y `docker-compose.yml`: Listos para despliegue en contenedores.

## Instalación y uso

**Requisitos previos**
- Python 3.11 o superior.

**Instalación**

1. Clona el repositorio y entra en el directorio:

    ```bash
    git clone https://github.com/daniel-alegria-z/Analizador-de-Emociones---EmotionalBETO.git
    cd Analizador-de-Emociones---EmotionalBETO
    ```

2. Crea y activa un entorno virtual:

    ```bash
    python -m venv .env
    # Windows:
    .\.env\Scripts\activate
    # Linux/Mac:
    source .env/bin/activate
    ```

3. Instala dependencias:

    ```bash
    pip install -r requirements.txt --prefer-binary
    ```

4. Ejecuta la aplicación:

    ```bash
    python emotional_bert.py
    ```

El panel interactivo estará disponible en `http://0.0.0.0:7860`.

## Despliegue recomendado en Hugging Face Spaces

Para una demo pública, gratuita y sencilla, la mejor opción es publicar el proyecto como un Space de tipo `Gradio`.

**Por qué lo recomiendo**
- No necesitas pagar una VM ni configurar infraestructura compleja.
- Gradio encaja de forma natural con Spaces.
- Puedes compartir una URL pública con tu portafolio en pocos minutos.

**Pasos resumidos**

1. Sube el repositorio a GitHub.
2. En Hugging Face, crea un nuevo Space y selecciona `Gradio`.
3. Importa el repo desde GitHub o sube estos archivos clave:
    - `app.py`
    - `emotional_bert.py`
    - `emotion_core.py`
    - `requirements.txt`
    - `README.md`
4. Hugging Face instalará dependencias y ejecutará `app.py`.

**Notas importantes**
- La primera ejecución puede tardar porque descarga `torch`, `transformers` y el modelo.
- Si después quieres más rendimiento o un despliegue privado, puedes migrar a hardware dedicado.
- Mantén el Space público si quieres una demo de portafolio sin coste.

## Ejecución con Docker

1. Construye la imagen:

    ```bash
    docker build -t emotionalbeto:dev .
    ```

2. Ejecuta el contenedor:

    ```bash
    docker run -p 7860:7860 --rm emotionalbeto:dev
    ```

O utiliza `docker-compose`:

    ```bash
    docker-compose up --build
    ```

## Evaluación y testing

- Ejecuta una evaluación rápida con:

    ```bash
    python evaluate.py
    ```

- Corre la suite de pruebas automatizadas con:

    ```bash
    pytest -q
    ```

## Integración continua

El repositorio incluye configuración para GitHub Actions en `.github/workflows/pytest.yml`, permitiendo ejecución automática de tests en cada push o pull request. El flujo es fácilmente extensible para linters, metrics y publicación de artefactos.

## Contribuir

¿Te gustaría aportar a EmotionalBETO? Abre un issue o pull request con tu propuesta. ¡Colaboraciones bienvenidas!

## Autor

**Daniel Esteban Alegría Zamora**  
Software Developer  
📧 daniel.alegria.z@outlook.com  
[LinkedIn](https://www.linkedin.com/in/daniel-esteban-a-52b6752a0/)

---
Proyecto personal desarrollado para análisis, experimentación y portafolio profesional.
