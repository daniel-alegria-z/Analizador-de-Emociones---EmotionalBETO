import pytest

from emotion_core import detectar_sarcasmo, detectar_urgencia, generar_respuesta


def test_detectar_sarcasmo_alto():
    texto = "Claro, como si todo fuera perfecto... por supuesto!!!"
    assert "Alto" in detectar_sarcasmo(texto, "neutral")


def test_detectar_sarcasmo_bajo():
    assert detectar_sarcasmo("hola", "alegría") == "🟢 Bajo"


def test_detectar_urgencia_alta():
    assert "Alta urgencia" in detectar_urgencia("Necesito ayuda urgente ahora")


def test_detectar_urgencia_media():
    assert "Urgencia media" in detectar_urgencia("¿Me responden?")


def test_generar_respuesta_corta_alegria():
    r = generar_respuesta("alegría", "¡bien!")
    assert "Nos alegra" in r or "Fantástico" in r


def test_generar_respuesta_larga_alegria():
    r = generar_respuesta("alegría", "x" * 100)
    assert "Fantástico" in r
