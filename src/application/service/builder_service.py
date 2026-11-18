from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from pathlib import Path
from decimal import Decimal
import os 

class HtmlBuilder:

    def __init__(self):
        base_dir = os.path.dirname((os.path.dirname(__file__)))
        templates_path = os.path.join(base_dir, "templates")
        assets_dir = Path(templates_path) / "assets"
        self.logo_bancoalfa_url = (assets_dir / "logo_bancoalfa.png").resolve().as_uri()
        self.logo_cobranca_url = (assets_dir / "logo_cobranca.png").resolve().as_uri()

        def format_int(value):
            if value in (None, ""):
                return ""
            try:
                value = int(round(float(value)))
            except (TypeError, ValueError):
                return ""
            if value == 0:
                return ""
            return f"{value:,}".replace(",", ".")

        def format_money(value):
            if value in (None, ""):
                return ""
            try:
                value = float(value)
            except (TypeError, ValueError):
                return ""
            if value == 0:
                return ""
            formatted = f"{value:,.2f}"
            formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
            return f"R$ {formatted}"

        def percent_value(value):
            if value in (None, ""):
                return None
            try:
                value = float(value)
            except (TypeError, ValueError):
                return None
            return value * 100

        def format_percent(value, decimals=2, fixed=True):
            pct = percent_value(value)
            if pct is None:
                return ""
            formatted = f"{pct:,.{decimals}f}"
            formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
            if not fixed and "," in formatted:
                formatted = formatted.rstrip("0").rstrip(",")
            return f"{formatted}%"

        def icm_class(value):
            pct = percent_value(value)
            if pct is None:
                return ""
            return "up" if pct >= 100 else "down"

        def icm_arrow(value):
            pct = percent_value(value)
            if pct is None:
                return ""
            return "▲" if pct >= 100 else "▼"

        self.env = Environment(
            loader=FileSystemLoader(templates_path),
            autoescape=True
        )
        self.env.filters["fmt_int"] = format_int
        self.env.filters["fmt_money"] = format_money
        self.env.filters["fmt_percent"] = format_percent
        self.env.filters["icm_class"] = icm_class
        self.env.filters["icm_arrow"] = icm_arrow

    @staticmethod
    def _to_float(value):
        if value in (None, ""):
            return 0.0
        if isinstance(value, (int, float, Decimal)):
            return float(value)
        if isinstance(value, str):
            value = value.replace("R$", "").replace("%", "")
            value = value.replace("\u00a0", " ").strip()
            if "," in value and "." in value:
                value = value.replace(".", "").replace(",", ".")
            else:
                value = value.replace(",", ".")
            value = value.replace(" ", "")
            try:
                return float(value)
            except ValueError:
                return 0.0
        return 0.0

    def _avg_field(self, rows, key):
        values = []
        for row in rows:
            raw = row.get(key)
            if raw in (None, ""):
                continue
            values.append(self._to_float(raw))
        if not values:
            return 0.0
        return sum(values) / len(values)

    def _ratio(self, numerator, denominator):
        numerator_value = self._to_float(numerator)
        denominator_value = self._to_float(denominator)
        if not denominator_value:
            return 0.0
        return numerator_value / denominator_value

    def _with_derived_metrics(self, row):
        row_data = dict(row)
        row_data["PENETRACAO"] = self._ratio(
            row_data.get("TRABALHADO"),
            row_data.get("MAILING"),
        )
        row_data["ICM_DISCAGEM"] = self._ratio(
            row_data.get("DISCAGEM_REALIZADA"),
            row_data.get("META_DISCAGEM"),
        )
        row_data["ICM_ATENDIDA"] = self._ratio(
            row_data.get("ATENDIMENTO_REALIZADO"),
            row_data.get("META_ATENDIDA"),
        )
        row_data["ICM_CPCA"] = self._ratio(
            row_data.get("CPCA_REALIZADO"),
            row_data.get("META_CPCA"),
        )
        row_data["ICM_ACORDO"] = self._ratio(
            row_data.get("ACORDO_REALIZADO"),
            row_data.get("META_ACORDO"),
        )
        row_data["ICM_SALDO"] = self._ratio(
            row_data.get("SALDO_REALIZADO"),
            row_data.get("META_SALDO"),
        )
        row_data["TKM_ACORDO"] = self._ratio(
            row_data.get("SALDO_REALIZADO"),
            row_data.get("ACORDO_REALIZADO"),
        )
        return row_data

    def _calcular_total_fase_1_2(self, rows):
        total = {
            "CONTRATOS": 0.0,
            "CARTEIRA": 0.0,
            "MAILING": 0.0,
            "TRABALHADO": 0.0,
            "META_DISCAGEM": 0.0,
            "DISCAGEM_REALIZADA": 0.0,
            "META_ATENDIDA": 0.0,
            "ATENDIMENTO_REALIZADO": 0.0,
            "META_CPCA": 0.0,
            "CPCA_REALIZADO": 0.0,
            "META_ACORDO": 0.0,
            "ACORDO_REALIZADO": 0.0,
            "META_SALDO": 0.0,
            "SALDO_REALIZADO": 0.0
        }
        for row in rows:
            total["CONTRATOS"] += self._to_float(row.get("CONTRATOS"))
            total["CARTEIRA"] += self._to_float(row.get("CARTEIRA"))
            total["MAILING"] += self._to_float(row.get("MAILING"))
            total["TRABALHADO"] += self._to_float(row.get("TRABALHADO"))
            total["META_DISCAGEM"] += self._to_float(row.get("META_DISCAGEM"))
            total["DISCAGEM_REALIZADA"] += self._to_float(row.get("DISCAGEM_REALIZADA"))
            total["META_ATENDIDA"] += self._to_float(row.get("META_ATENDIDA"))
            total["ATENDIMENTO_REALIZADO"] += self._to_float(row.get("ATENDIMENTO_REALIZADO"))
            total["META_CPCA"] += self._to_float(row.get("META_CPCA"))
            total["CPCA_REALIZADO"] += self._to_float(row.get("CPCA_REALIZADO"))
            total["META_ACORDO"] += self._to_float(row.get("META_ACORDO"))
            total["ACORDO_REALIZADO"] += self._to_float(row.get("ACORDO_REALIZADO"))
            total["META_SALDO"] += self._to_float(row.get("META_SALDO"))
            total["SALDO_REALIZADO"] += self._to_float(row.get("SALDO_REALIZADO"))

        total["TICKET_MEDIO"] = (
            total["CARTEIRA"] / total["CONTRATOS"] if total["CONTRATOS"] else 0.0
        )
        total["ELEGIVEL"] = self._avg_field(rows, "ELEGIVEL")
        total["PENETRACAO"] = (
            total["TRABALHADO"] / total["MAILING"] if total["MAILING"] else 0.0
        )
        total["ICM_DISCAGEM"] = self._ratio(
            total["DISCAGEM_REALIZADA"],
            total["META_DISCAGEM"],
        )
        total["ICM_ATENDIDA"] = self._ratio(
            total["ATENDIMENTO_REALIZADO"],
            total["META_ATENDIDA"],
        )
        total["ICM_CPCA"] = self._ratio(
            total["CPCA_REALIZADO"],
            total["META_CPCA"],
        )
        total["ICM_ACORDO"] = self._ratio(
            total["ACORDO_REALIZADO"],
            total["META_ACORDO"],
        )
        total["ICM_SALDO"] = self._ratio(
            total["SALDO_REALIZADO"],
            total["META_SALDO"],
        )
        total["TICKET_MEDIO"] = sum(
            self._to_float(r.get("TICKET_MEDIO")) for r in rows
        )
        total["TKM_ACORDO"] = self._ratio(
            total["SALDO_REALIZADO"],
            total["ACORDO_REALIZADO"],
        )
        return total

    def gerar_html(self, dados):
        agrupado = {}
        for row in dados:
            row_data = self._with_derived_metrics(row)
            agrupado.setdefault(row_data["SEGMENTO"], []).append(row_data)

        ct_rows = agrupado.get("CT", [])
        faixa_values = [
            str(r.get("FAIXA_ATRASO", "")).upper() for r in ct_rows
        ]
        fase_totais = [
            r for r, faixa in zip(ct_rows, faixa_values)
            if "TOTAL FASE" in faixa
        ]
        base_rows = fase_totais or [
            r for r, faixa in zip(ct_rows, faixa_values)
            if "TOTAL" not in faixa
        ]
        total_fase_1_2 = self._calcular_total_fase_1_2(base_rows)

        template = self.env.get_template("meta_template_documento_cores_exatas.html")

        return template.render(
            dados=agrupado,
            hora=datetime.now().strftime("%H:%M"),
            logo_bancoalfa_url=self.logo_bancoalfa_url,
            logo_cobranca_url=self.logo_cobranca_url,
            total_fase_1_2=total_fase_1_2
        )
