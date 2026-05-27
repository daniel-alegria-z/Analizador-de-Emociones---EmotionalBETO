import csv
import json
from collections import Counter, defaultdict
from typing import List

import torch
import pandas as pd

from emotion_core import tokenizador, modelo, ETIQUETAS_EMOCION, TRADUCCION_EMOCIONES, DISPOSITIVO


def cargar_ejemplos(path: str) -> List[dict]:
    filas = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            filas.append({"text": r["text"].strip(), "label": r["label"].strip()})
    return filas


def predecir(texto: str) -> str:
    entradas = tokenizador(texto, return_tensors="pt", truncation=True, max_length=512)
    entradas = {k: v.to(DISPOSITIVO) for k, v in entradas.items()}
    with torch.no_grad():
        out = modelo(**entradas)
    probs = torch.nn.functional.softmax(out.logits, dim=-1)
    idx = int(torch.argmax(probs, dim=-1).item())
    etiqueta = ETIQUETAS_EMOCION[idx] if idx < len(ETIQUETAS_EMOCION) else ETIQUETAS_EMOCION[0]
    etiqueta_es = TRADUCCION_EMOCIONES.get(etiqueta, etiqueta)
    return etiqueta_es


def evaluar(path_csv: str):
    ejemplos = cargar_ejemplos(path_csv)
    y_true = []
    y_pred = []
    for e in ejemplos:
        etiqueta_verdad = e["label"]
        pred = predecir(e["text"])  # Spanish label
        y_true.append(etiqueta_verdad)
        y_pred.append(pred)

    clases = sorted(set(y_true) | set(y_pred))
    # confusion matrix
    cm = pd.DataFrame(0, index=clases, columns=clases)
    for t, p in zip(y_true, y_pred):
        if t not in cm.index:
            cm.loc[t] = 0
        if p not in cm.columns:
            cm[p] = 0
        cm.loc[t, p] += 1

    total = len(y_true)
    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    acc = correct / total if total else 0.0

    metrics = {}
    for c in clases:
        tp = int(cm.loc[c, c]) if c in cm.index and c in cm.columns else 0
        fp = int(cm[c].sum()) - tp if c in cm.columns else 0
        fn = int(cm.loc[c].sum()) - tp if c in cm.index else 0
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
        metrics[c] = {"precision": prec, "recall": rec, "f1": f1, "support": int(cm.loc[c].sum())}

    resultado = {"accuracy": acc, "total": total, "metrics": metrics}

    print("Accuracy:", acc)
    print("Confusion matrix:\n", cm)
    print("Per-class metrics:\n", json.dumps(metrics, indent=2, ensure_ascii=False))

    # Save results
    with open("evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    cm.to_csv("confusion_matrix.csv", encoding="utf-8")


if __name__ == "__main__":
    print("Ejecutando evaluación sobre data/sample_eval.csv")
    evaluar("data/sample_eval.csv")