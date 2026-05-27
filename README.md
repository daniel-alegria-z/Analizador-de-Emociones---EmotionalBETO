# EmotionalBETO

**Analizador de emociones en español**

EmotionalBETO es un proyecto personal que detecta la emoción principal de un texto en español, muestra una distribución de probabilidades, detecta posible sarcasmo y nivel de urgencia, y sugiere una respuesta apropiada. Está pensado como demostración y herramienta para prototipado y evaluación de análisis de sentimiento/emoción en aplicaciones en español.

**Estado:** Prototipo funcional. Ideal para demos y pruebas; pendiente optimización y ajustes para producción.

**Demo:** La aplicación UI se sirve con `Gradio` y corre por defecto en el puerto `7860`.

**Características principales**
- **Detección de emoción:** usa un modelo basado en BERT para clasificar emociones.
- **Visualización:** gráfica de barras con la distribución de probabilidades.
- **Heurísticas:** detección de sarcasmo y nivel de urgencia mejoradas por reglas.
- **Respuesta sugerida:** texto sugerido según emoción detectada.
- **Evaluación y tests:** script de evaluación y suite `pytest` incluida.

**Contenido del repositorio**
- **[emotional_bert.py](emotional_bert.py)**: punto de entrada con la interfaz `Gradio`.
- **[emotion_core.py](emotion_core.py)**: lógica de carga del modelo, inferencia y heurísticas.
- **[evaluate.py](evaluate.py)**: script para evaluar el modelo contra un CSV de ejemplo.
- **[data/sample_eval.csv](data/sample_eval.csv)**: dataset de muestra para evaluación rápida.
- **[tests/](tests/)**: tests unitarios y de integración con `pytest`.
- **[requirements.txt](requirements.txt)**: dependencias fijadas.
- **[Dockerfile](Dockerfile)** y **[docker-compose.yml](docker-compose.yml)**: para ejecutar en contenedor.

**Requisitos**
- Python 3.11+
- Espacio en disco y red para descargar el modelo (cuando se ejecute por primera vez).

**Instalación y ejecución local**

1. Crear y activar un entorno virtual (Windows):

```powershell
python -m venv .env
.\.env\Scripts\activate
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt --prefer-binary
```

3. Ejecutar la aplicación:

```powershell
python emotional_bert.py
```

La interfaz Gradio quedará accesible en `http://0.0.0.0:7860`.

**Docker (desarrollo / prueba local)**

Construir la imagen:

```bash
docker build -t emotionalbeto:dev .
```

Ejecutar el contenedor:

```bash
docker run -p 7860:7860 --rm emotionalbeto:dev
```

O con `docker-compose`:

```bash
docker-compose up --build
```

> Nota sobre `torch`: `requirements.txt` está fijado a una build CPU para portabilidad. Si necesitas GPU en producción, reemplaza la dependencia por la rueda adecuada o usa una imagen base con CUDA.

**Evaluación**

Usa el script `evaluate.py` para ejecutar una evaluación rápida sobre un CSV con dos columnas: `text,label`.

```powershell
python evaluate.py
```

El script generará `evaluation_results.json` y `confusion_matrix.csv`.

**Tests**

La suite de pruebas está en `tests/` y se ejecuta con `pytest`:

```bash
pytest -q
```

**Integración continua**

Se incluye un workflow básico para GitHub Actions en `.github/workflows/pytest.yml` que ejecuta los tests en push/PR. Puedes extenderlo para ejecutar linters, coverage y publicar artefactos.

**Buenas prácticas y recomendaciones previas a producción**
- **Evaluar el modelo:** crear un dataset anotado representativo (50–200 ejemplos por clase) y medir métricas por clase.
- **Calibrar umbrales:** revisar `UMBRAL_CONFIANZA` y `UMBRAL_DIFERENCIA` en `emotion_core.py` con datos reales.
- **Optimización de inferencia:** quantization, ONNX export o TorchScript para reducir latencia y consumo CPU.
- **Escalado y despliegue:** para producción usar un orquestador (Kubernetes) o un servicio de PaaS, configurar healthchecks, logging y métricas.
- **Privacidad:** revisar PII en datos de entrada y políticas de retención.

**Limitaciones conocidas**
- El modelo base puede no estar perfectamente adaptado al español coloquial o dominios específicos.
- La detección de `sarcasmo` es heurística y no reemplaza un modelo entrenado para ironía.
- Para alto tráfico o latencias bajas, se recomendará GPU u optimizaciones de inferencia.

**Siguientes pasos recomendados**
1. Publicar el repo como demo pública (por ejemplo en Hugging Face Spaces) para compartir el prototipo. 
2. Recolectar y etiquetar datos reales para evaluación y posible fine-tuning.
3. Preparar Docker optimizado para producción con `uvicorn`/`gunicorn`, healthchecks y metrics.

**Contribuciones**
- Este proyecto es personal; si quieres colaborar, abre un issue o PR con propuestas concretas.

**Contacto y más información**
- Si quieres que configure el deploy en Hugging Face Spaces o prepare la imagen Docker para producción, te puedo ayudar.

**Autoría**

Daniel Esteban Alegría Zamora
Software Developer
Contacto: daniel.alegria.z@outlook.com
LinkedIn: https://www.linkedin.com/in/daniel-esteban-a-52b6752a0/

Contexto del proyecto: proyecto personal.
