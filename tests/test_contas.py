"""As contas do projeto conferidas à mão (python -m pytest -q)."""
import json
from datetime import date
from pathlib import Path

R = json.loads((Path(__file__).resolve().parents[1] / "resultados" / "RESUMO.json").read_text(encoding="utf-8"))


def test_dias_julgados():
    assert R["denuncia_ate_decisao_julgados"] == {
        "gilvan-exercito": (date(2026, 3, 20) - date(2025, 12, 18)).days,
        "gayer": (date(2026, 4, 28) - date(2025, 2, 12)).days,
        "otoni": (date(2023, 6, 29) - date(2020, 7, 14)).days,
    }


def test_van_hattem():
    assert R["van_hattem"]["denuncia_ate_inicio_do_julgamento_dias"] == 206
    assert R["gilvan_exercito_denuncia_ate_inicio_dias"] == 85


def test_placar():
    assert (R["julgados"], R["recebidas"], R["rejeitadas"]) == (4, 4, 0)
