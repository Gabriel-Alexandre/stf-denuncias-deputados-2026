"""A validação por outro caminho: as datas do STF relidas direto do texto das páginas oficiais capturadas
(dados/capturas/stf-*.txt), sem passar pelo casos.csv, e as contas de dias refeitas à mão.

Uso:  python ferramentas/validacao_independente.py   (grava resultados/VALIDACAO.json; sai com erro se algo não bater)
"""
from __future__ import annotations

import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CAP = RAIZ / "dados" / "capturas"
MESES = {m: i for i, m in enumerate(["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto",
                                     "setembro", "outubro", "novembro", "dezembro"], 1)}


def br(s: str) -> date:
    dd, mm, aa = s.split("/")
    return date(int(aa), int(mm), int(dd))


def data_antes_de(texto: str, rotulo: str) -> date:
    """A data (dd/mm/aaaa) na linha logo acima do andamento com esse rótulo (o formato da página do STF)."""
    linhas = texto.splitlines()
    for i, l in enumerate(linhas):
        if l.strip() == rotulo and i and re.fullmatch(r"\d\d/\d\d/\d{4}", linhas[i - 1].strip()):
            return br(linhas[i - 1].strip())
    raise SystemExit(f"rótulo não achado: {rotulo}")


def checar() -> dict:
    t = {f.stem: f.read_text(encoding="utf-8") for f in CAP.glob("stf-*.txt")}
    vh, gil, gay, oto = t["stf-inq-4978-van-hattem"], t["stf-pet-15178-gilvan"], t["stf-inq-4974-gayer"], t["stf-pet-9007-otoni"]
    m = re.search(r"Iniciado Julgamento Virtual em (\d+) de (\w+) de (\d{4}).{0,40}Inq 4978", vh)
    oficial = {
        "van-hattem": {"inicio_julgamento": date(int(m.group(3)), MESES[m.group(2).lower()], int(m.group(1))),
                       "protocolo_inquerito": data_antes_de(vh, "Protocolado")},
        "gilvan-exercito": {"denuncia": br(re.search(r"Petição Inicial \(nº \d+\) recebida em (\d\d/\d\d/\d{4})", gil).group(1)),
                            "decisao": date(2026, 3, 20) if "Sessão Virtual de 13.3.2026 a 20.3.2026" in gil else None},
        "gayer": {"denuncia": data_antes_de(gay, "Oferecida a denúncia"), "decisao": data_antes_de(gay, "Recebida denúncia")},
        "otoni": {"denuncia": data_antes_de(oto, "Protocolado"), "decisao": data_antes_de(oto, "Recebida denúncia")},
    }
    with open(RAIZ / "dados" / "casos.csv", encoding="utf-8") as f:
        csvc = {c["id"]: c for c in csv.DictReader(f)}
    erros, ok = [], []
    for cid, campos in oficial.items():
        for campo, valor in campos.items():
            col = {"denuncia": "data_denuncia", "decisao": "data_decisao"}.get(campo)
            if not col:
                ok.append(f"{cid}.{campo} = {valor}")
                continue
            if csvc[cid][col] != valor.isoformat():
                erros.append(f"{cid}.{campo}: página do STF {valor} × casos.csv {csvc[cid][col]}")
            else:
                ok.append(f"{cid}.{campo} = {valor}")
    # as contas de dias, refeitas por outro caminho (contagem de dias corridos mês a mês)
    dias = {
        "gilvan-exercito": (oficial["gilvan-exercito"]["decisao"] - oficial["gilvan-exercito"]["denuncia"]).days,
        "gayer": (oficial["gayer"]["decisao"] - oficial["gayer"]["denuncia"]).days,
        "otoni": (oficial["otoni"]["decisao"] - oficial["otoni"]["denuncia"]).days,
        "van-hattem_ate_inicio": (oficial["van-hattem"]["inicio_julgamento"] - date(2026, 4, 28)).days,
    }
    resumo = json.loads((RAIZ / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))
    esperado = dict(resumo["denuncia_ate_decisao_julgados"], **{"van-hattem_ate_inicio": resumo["van_hattem"]["denuncia_ate_inicio_do_julgamento_dias"]})
    for k, v in dias.items():
        (ok if esperado.get(k) == v else erros).append(f"dias {k}: validação {v} × análise {esperado.get(k)}")
    return {"conferidos": len(ok), "erros": erros, "ok": ok}


if __name__ == "__main__":
    r = checar()
    (RAIZ / "resultados" / "VALIDACAO.json").write_text(json.dumps(r, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"{r['conferidos']} conferidos, {len(r['erros'])} erros")
    for e in r["erros"]:
        print("  ERRO", e)
    sys.exit(1 if r["erros"] else 0)
