import traceback

import pandas as pd
import plotly.express as px  # type: ignore
import torch  # type: ignore
from transformers import AutoModelForSequenceClassification, AutoTokenizer


NOMBRE_MODELO = "finiteautomata/beto-emotion-analysis"
DISPOSITIVO = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def cargar_recursos_modelo():
    tokenizador_local = AutoTokenizer.from_pretrained(NOMBRE_MODELO)
    modelo_local = AutoModelForSequenceClassification.from_pretrained(NOMBRE_MODELO)
    modelo_local.to(DISPOSITIVO)
    modelo_local.eval()

    etiquetas_locales = [
        modelo_local.config.id2label[indice]
        for indice in sorted(modelo_local.config.id2label)
    ]
    return tokenizador_local, modelo_local, etiquetas_locales


tokenizador, modelo, ETIQUETAS_EMOCION = cargar_recursos_modelo()

TRADUCCION_EMOCIONES = {
    "joy": "alegría",
    "sadness": "tristeza",
    "anger": "enojo",
    "fear": "miedo",
    "surprise": "sorpresa",
    "neutral": "neutral",
    "disgust": "asco",
    "others": "neutral",
}

UMBRAL_CONFIANZA = 0.5
UMBRAL_DIFERENCIA = 0.1


def analizar_texto(texto: str):
    try:
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError("El texto de entrada debe ser una cadena no vacía.")
        texto_limpio = texto.strip()
        texto_normalizado = texto_limpio.lower()

        entradas = tokenizador(texto_limpio, return_tensors="pt", truncation=True, max_length=512)
        entradas = {clave: valor.to(DISPOSITIVO) for clave, valor in entradas.items()}
        with torch.no_grad():
            salidas = modelo(**entradas)
        probabilidades = torch.nn.functional.softmax(salidas.logits, dim=-1)
        probabilidades_np = probabilidades.squeeze(0).detach().cpu().tolist()

        etiquetas = list(ETIQUETAS_EMOCION[: len(probabilidades_np)])
        top_probabilidades, top_indices = torch.topk(probabilidades.squeeze(0), k=min(2, len(probabilidades_np)))
        mayor_prob = float(top_probabilidades[0].item())
        segunda_prob = float(top_probabilidades[1].item()) if len(top_probabilidades) > 1 else 0.0
        indice_max = int(top_indices[0].item())

        if mayor_prob < UMBRAL_CONFIANZA or (mayor_prob - segunda_prob) < UMBRAL_DIFERENCIA:
            emocion_principal = "neutral"
            probabilidad_principal = mayor_prob
        else:
            emocion_principal = etiquetas[indice_max]
            probabilidad_principal = mayor_prob

        emocion_principal_es = TRADUCCION_EMOCIONES.get(emocion_principal, emocion_principal)

        df = pd.DataFrame(
            {
                "Emoción": [TRADUCCION_EMOCIONES.get(e, e) for e in etiquetas],
                "Probabilidad": probabilidades_np,
            }
        )
        figura = px.bar(
            df,
            x="Emoción",
            y="Probabilidad",
            color="Emoción",
            title="Distribución de Probabilidades Emocionales",
            height=400,
        )

        nivel_sarcasmo = detectar_sarcasmo(texto_normalizado, emocion_principal_es)
        nivel_urgencia = detectar_urgencia(texto_normalizado)
        respuesta_sugerida = generar_respuesta(emocion_principal_es, texto_limpio)

        return (
            emocion_principal_es,
            f"{probabilidad_principal*100:.2f}%",
            figura,
            nivel_sarcasmo,
            nivel_urgencia,
            respuesta_sugerida,
        )
    except Exception:
        traceback.print_exc()
        df_error = pd.DataFrame({"Emoción": ["error"], "Probabilidad": [1]})
        figura_error = px.bar(df_error, x="Emoción", y="Probabilidad")
        return (
            "error",
            "0%",
            figura_error,
            "error",
            "error",
            "Ocurrió un error al analizar el texto",
        )


def detectar_sarcasmo(texto: str, emocion_predicha: str) -> str:
    """Heurística mejorada para detectar posible sarcasmo.

    Entrada: `texto` ya normalizado en minúsculas.
    Devuelve una etiqueta con semáforo similar al comportamiento previo.
    """
    import re

    # Marcadores y patrones comunes de sarcasmo/ironía
    markers = [
        r"\bclaro\b",
        r"\bpor supuesto\b",
        r"\bcomo si\b",
        r"\bsí, claro\b",
        r"\bqué sorpresa\b",
    ]

    # Emoticons/emoji positivos que pueden contradecir el texto
    positive_emojis = ["😊", "😄", "😁", "👍", "🙂"]

    # Conteo de signos de exclamación y preguntas
    exclams = texto.count("!")
    questions = texto.count("?")
    ellipsis = "..." in texto

    marker_hits = sum(1 for m in markers if re.search(m, texto))
    emoji_hit = any(e in texto for e in positive_emojis)

    # Contradicción simple: palabras negativas + un emoji positivo
    contradiction = False
    if emoji_hit and any(w in texto for w in ("mal", "terrible", "peor", "nunca")):
        contradiction = True

    score = 0
    score += marker_hits * 2
    score += min(exclams, 3)
    score += 1 if ellipsis else 0
    score += 1 if contradiction else 0
    score += 1 if questions > 1 else 0

    if emocion_predicha == "neutral" and score >= 3:
        return "🔴 Alto (posible sarcasmo)"
    if score >= 2:
        return "🟡 Medio (posible sarcasmo)"
    return "🟢 Bajo"


def detectar_urgencia(texto: str) -> str:
    """Heurística mejorada para detectar urgencia. Devuelve etiqueta de semáforo."""
    import re

    urgentes = ["urgente", "ahora", "inmediato", "rápido", "necesito ya", "importante", "ya mismo"]

    # Detectar tiempos o cantidades que sugieren plazo
    tiempo_patron = re.search(r"\b(\d+\s*(min|mins|minutos|horas|h|segundos|s))\b", texto)

    # Conteo signos de exclamación, mayúsculas y palabras clave
    exclams = texto.count("!")
    all_caps = sum(1 for c in texto if c.isupper())
    caps_ratio = (all_caps / max(1, len(texto))) if len(texto) > 3 else 0

    if any(k in texto for k in urgentes) or tiempo_patron:
        return "🔴 Alta urgencia"

    # Mensajes con varias exclamaciones o texto escrito en mayúsculas son de urgencia media
    if exclams >= 2 or caps_ratio > 0.25:
        return "🟡 Urgencia media"

    # Preguntas o una sola exclamación sugieren urgencia moderada
    if "?" in texto or exclams == 1:
        return "🟡 Urgencia media"

    return "🟢 Sin urgencia"


def generar_respuesta(emocion: str, texto_original: str) -> str:
    base_respuestas = {
        "alegría": [
            "¡Nos alegra mucho escuchar eso! 😊 ¿En qué más podemos ayudarte?",
            "¡Fantástico! Estamos encantados de saber que estás contento.",
        ],
        "tristeza": [
            "Lamentamos que estés pasando por esto. Estamos aquí para lo que necesites.",
            "Entendemos que esto es difícil para ti. Vamos a buscar una solución.",
        ],
        "enojo": [
            "Entendemos tu frustración. Trabajaremos para resolverlo inmediatamente.",
            "Lamentamos esta situación. Estamos ocupándonos del asunto.",
        ],
        "neutral": [
            "Gracias por tu mensaje. ¿Hay algo más que quieras compartir?",
            "Hemos recibido tu consulta. Estamos revisando la información.",
        ],
        "miedo": [
            "Tu seguridad es nuestra prioridad. Actuaremos de inmediato.",
            "Entendemos tu preocupación. Estamos aquí para protegerte.",
        ],
        "sorpresa": [
            "¡Vaya! Revisaremos esto cuidadosamente para ayudarte.",
            "¡Qué sorpresa! Asegurémonos de manejar esto adecuadamente.",
        ],
        "error": [
            "Lo sentimos, hubo un error al procesar tu mensaje.",
            "Ocurrió un problema técnico. Por favor intenta nuevamente.",
        ],
    }
    respuestas = base_respuestas.get(emocion, base_respuestas["neutral"])
    return respuestas[0] if len(texto_original) < 60 else respuestas[1]