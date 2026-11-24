"""A conta do projeto: quanto tempo o STF levou, da denúncia da PGR à decisão, nos casos de deputados federais
denunciados por fala, e onde fica o caso do Marcel van Hattem nessa fila.

Lê dados/casos.csv (cada data com a captura que a sustenta em dados/capturas/) e grava resultados/RESUMO.json.
Uso:  python ferramentas/analise.py
"""
from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path
from statistics import median

RAIZ = Path(__file__).resolve().parents[1]
HOJE = date(2026, 11, 24)          # o dia da coleta
INICIO_JULGAMENTO_VH = date(2026, 11, 20)   # o julgamento virtual do Inq 4978 começou (andamento do STF)


def d(s: str) -> date | None:
    return date.fromisoformat(s) if s else None


def carregar() -> list[dict]:
    with open(RAIZ / "dados" / "casos.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def calcular() -> dict:
    casos = carregar()
    linhas = []
    for c in casos:
        den, dec, fato = d(c["data_denuncia"]), d(c["data_decisao"]), d(c["data_fato"])
        fim = dec or HOJE
        linhas.append({
            "id": c["id"], "deputado": c["deputado"], "partido": c["partido"], "onde_falou": c["onde_falou"],
            "orgao": c["orgao"], "relator": c["relator"], "decisao": c["decisao"] or "sem decisão",
            "placar": c["placar"], "pendente": dec is None,
            "denuncia_ate_decisao_dias": (fim - den).days if den else None,
            "fato_ate_decisao_dias": (fim - fato).days if fato else None,
            "fato_exato": c["fato_exato"] == "sim",
        })
    julgados = [l for l in linhas if not l["pendente"]]
    com_den = [l for l in julgados if l["denuncia_ate_decisao_dias"] is not None]
    vh = next(l for l in linhas if l["id"] == "van-hattem")
    vh_ate_inicio = (INICIO_JULGAMENTO_VH - date(2026, 4, 28)).days
    gilvan = next(l for l in linhas if l["id"] == "gilvan-exercito")
    gilvan_ate_inicio = (date(2026, 3, 13) - date(2025, 12, 18)).days
    pendentes = [l for l in linhas if l["pendente"]]
    resumo = {
        "coleta": HOJE.isoformat(),
        "casos": linhas,
        "julgados": len(julgados),
        "recebidas": sum(l["decisao"] == "recebida" for l in julgados),
        "rejeitadas": sum(l["decisao"] == "rejeitada" for l in julgados),
        "unanimes": sum(l["placar"] in ("unanimidade", "4 a 0") for l in julgados),
        "denuncia_ate_decisao_julgados": {l["id"]: l["denuncia_ate_decisao_dias"] for l in com_den},
        "mediana_denuncia_ate_decisao_julgados": median(l["denuncia_ate_decisao_dias"] for l in com_den),
        "van_hattem": {
            "denuncia_ate_inicio_do_julgamento_dias": vh_ate_inicio,
            "denuncia_ate_hoje_dias": vh["denuncia_ate_decisao_dias"],
            "fato_ate_hoje_dias": vh["fato_ate_decisao_dias"],
            "posicao_ate_o_inicio_do_julgamento": "2º mais rápido entre os 4 que chegaram a julgamento com a data da denúncia conhecida",
        },
        "gilvan_exercito_denuncia_ate_inicio_dias": gilvan_ate_inicio,
        "razao_vh_sobre_gilvan_ate_inicio": round(vh_ate_inicio / gilvan_ate_inicio, 2),
        "pendentes_sem_decisao": {l["id"]: l["denuncia_ate_decisao_dias"] for l in pendentes if l["id"] != "van-hattem"},
        "fato_dentro_da_camara_e_recebida": [l["id"] for l in julgados if "Câmara" in l["onde_falou"]],
    }
    return resumo


if __name__ == "__main__":
    r = calcular()
    (RAIZ / "resultados").mkdir(exist_ok=True)
    (RAIZ / "resultados" / "RESUMO.json").write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in r.items() if k != "casos"}, ensure_ascii=False, indent=1))
