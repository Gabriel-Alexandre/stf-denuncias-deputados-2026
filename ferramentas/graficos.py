"""Os gráficos do projeto, 1920x1080, só a partir de resultados/RESUMO.json.

Uso:  python ferramentas/graficos.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
FIG = RAIZ / "resultados" / "figuras"
REPO = "github.com/Gabriel-Alexandre/stf-denuncias-deputados-2026"
COR = {"vh": "#D9822B", "outro": "#5B7DA6", "pendente": "#B8B8B8", "texto": "#1F1F1F", "verde": "#2E7D5B"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 22, "axes.edgecolor": "#BBBBBB",
                     "axes.spines.top": False, "axes.spines.right": False, "text.parse_math": False})


def figura(titulo: str, subtitulo: str):
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor="white")
    fig.text(0.05, 0.93, titulo, fontsize=44, weight="bold", color=COR["texto"], va="top")
    fig.text(0.05, 0.845, subtitulo, fontsize=24, color="#444444", va="top")
    return fig


def rodape(fig, fonte: str) -> None:
    fig.text(0.05, 0.035, f"Fonte: {fonte}", fontsize=16, color="#555555")
    fig.text(0.05, 0.008, f"{REPO} · conta feita com o auxílio do Claude (IA)", fontsize=15, color="#777777")


def g01(r: dict) -> None:
    j = r["denuncia_ate_decisao_julgados"]; p = r["pendentes_sem_decisao"]; vh = r["van_hattem"]["denuncia_ate_inicio_do_julgamento_dias"]
    barras = [("Gilvan da Federal (general)", j["gilvan-exercito"], COR["outro"], "recebida"),
              ("Marcel van Hattem", vh, COR["vh"], "até começar o julgamento (pendente)"),
              ("Gustavo Gayer", j["gayer"], COR["outro"], "recebida"),
              ("Gilvan da Federal (\"ladrão\")", p["gilvan-ladrao-lula"], COR["pendente"], "sem decisão até hoje"),
              ("Nikolas Ferreira", p["nikolas"], COR["pendente"], "sem decisão até hoje"),
              ("Otoni de Paula", j["otoni"], COR["outro"], "recebida")]
    fig = figura("Da denúncia ao julgamento: quanto tempo?",
                 "Denúncias da PGR contra deputados federais por fala, em dias corridos")
    ax = fig.add_axes([0.30, 0.13, 0.62, 0.66])
    for i, (nome, v, cor, nota) in enumerate(reversed(barras)):
        ax.barh(i, v, color=cor, height=0.62)
        rotulo = f"{v} a {r['van_hattem']['denuncia_ate_inicio_se_a_denuncia_for_de_marco_dias']} dias" if "van Hattem" in nome else f"{v} dias"
        ax.text(v + 15, i, f"{rotulo} · {nota}", va="center", fontsize=21, color=COR["texto"])
        fig.text(0.29, 0.13 + (i + 0.5) * 0.66 / len(barras), nome, ha="right", va="center", fontsize=23,
                 weight="bold" if "van Hattem" in nome else "normal", color=COR["texto"])
    ax.set_xlim(0, 1500); ax.set_ylim(-0.5, len(barras) - 0.5); ax.set_yticks([]); ax.tick_params(axis="x", labelsize=18)
    rodape(fig, "STF, andamentos do Inq 4978, Pet 15178, Inq 4974 e Pet 9007; PGR e imprensa para as datas das denúncias (24/11/2026)")
    fig.savefig(FIG / "g01_tempo_denuncia_julgamento.png"); plt.close(fig)


def g02(r: dict) -> None:
    fig = figura("Quantas denúncias o STF aceitou?", "Os casos de deputado denunciado pela PGR por fala que chegaram a julgamento")
    n, rec = r["julgados"], r["recebidas"]
    fig.text(0.5, 0.52, f"{rec} de {n}", ha="center", va="center", fontsize=200, weight="bold", color=COR["verde"])
    fig.text(0.5, 0.30, "recebidas, todas por unanimidade", ha="center", fontsize=40, color=COR["texto"])
    fig.text(0.5, 0.22, "Otoni de Paula (2023) · Gustavo Gayer (abr/2026) · Gilvan da Federal (mar e ago/2026)",
             ha="center", fontsize=24, color="#444444")
    rodape(fig, "STF (andamentos e acórdão da Pet 15178), PGR e imprensa; os casos achados em 24/11/2026, não é a lista completa")
    fig.savefig(FIG / "g02_recebidas.png"); plt.close(fig)


def g03(r: dict) -> None:
    fig = figura("O caso do van Hattem, do discurso ao julgamento", "Inq 4978, relator Flávio Dino, 1ª Turma do STF")
    ax = fig.add_axes([0.05, 0.2, 0.9, 0.5]); ax.axis("off")
    eventos = [("14/08/2024", "discurso na\ntribuna da Câmara"), ("18/09/2024", "inquérito\nno STF"),
               ("28/04/2026", "denúncia\nda PGR"), ("11/11/2026", "pauta do\njulgamento virtual"),
               ("20/11/2026", "Dino vota por receber;\nZanin pede destaque"), ("21/11/2026", "Moraes acompanha;\nvai à sessão presencial")]
    xs = [0, 1.3, 4.0, 5.2, 6.4, 7.6]
    ax.plot([xs[0], xs[-1]], [0, 0], color="#888888", lw=4)
    for (data, rot), x in zip(eventos, xs):
        ax.plot(x, 0, "o", ms=26, color=COR["vh"])
        ax.text(x, 0.35 if xs.index(x) % 2 == 0 else -0.35, f"{data}\n{rot}", ha="center", va="bottom" if xs.index(x) % 2 == 0 else "top",
                fontsize=19, color=COR["texto"])
    ax.text(2.65, 0.06, "20 meses até a denúncia", ha="center", fontsize=22, color="#444444")
    ax.set_xlim(-0.7, 8.4); ax.set_ylim(-1.3, 1.3)
    rodape(fig, "STF (andamento do Inq 4978), Gazeta do Povo, Congresso em Foco e Revista Oeste (votos e destaque)")
    fig.savefig(FIG / "g03_linha_do_tempo_van_hattem.png"); plt.close(fig)


if __name__ == "__main__":
    FIG.mkdir(parents=True, exist_ok=True)
    r = json.loads((RAIZ / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))
    g01(r); g02(r); g03(r)
    print("3 gráficos em", FIG)
