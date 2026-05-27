from types import SimpleNamespace
from unittest.mock import patch

import torch

from emotion_core import analizar_texto, ETIQUETAS_EMOCION


def fake_tokenizer(text, return_tensors=None, truncation=None, max_length=None):
    return {
        "input_ids": torch.tensor([[1, 2, 3]]),
        "attention_mask": torch.tensor([[1, 1, 1]]),
    }


def test_analizar_texto_mock():
    # create logits matching the number of etiquetas
    n = len(ETIQUETAS_EMOCION)
    logits = torch.zeros((1, n))
    logits[0, 0] = 10.0  # make the first class dominant

    fake_model = lambda **kwargs: SimpleNamespace(logits=logits)

    with patch("emotion_core.tokenizador", new=fake_tokenizer), patch("emotion_core.modelo", new=fake_model):
        resultado = analizar_texto("Esto es una prueba")
        assert isinstance(resultado, tuple)
        assert len(resultado) == 6
        emocion_principal = resultado[0]
        assert isinstance(emocion_principal, str)
