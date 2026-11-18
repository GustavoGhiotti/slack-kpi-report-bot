from decimal import Decimal


class MetaRelogioService:

    @staticmethod
    def _to_float(valor):
        """
        Converte valores vindos do banco (nvarchar) para float seguro.
        Aceita: '233%', '73,5', None, '', int, float
        """
        if valor is None:
            return 0.0

        if isinstance(valor, (int, float, Decimal)):
            return float(valor)

        if isinstance(valor, str):
            valor = (
                valor.replace("%", "")
                     .replace(",", ".")
                     .strip()
            )
            try:
                return float(valor)
            except ValueError:
                return 0.0

        return 0.0


    @staticmethod
    def calcular_percentual(realizado, meta):
        meta = MetaRelogioService._to_float(meta)
        realizado = MetaRelogioService._to_float(realizado)

        if meta == 0:
            return 0

        return (realizado / meta) * 100

    def processar(self, dados):
        for row in dados:
            # Normaliza ICMs (usados no HTML para setas)
            row["ICM_DISCAGEM"] = self._to_float(row.get("ICM_DISCAGEM"))
            row["ICM_ATENDIDA"] = self._to_float(row.get("ICM_ATENDIDA"))
            row["ICM_CPCA"]     = self._to_float(row.get("ICM_CPCA"))
            row["ICM_ACORDO"]   = self._to_float(row.get("ICM_ACORDO"))
            row["ICM_SALDO"]    = self._to_float(row.get("ICM_SALDO"))

            # (Opcional) normalizar metas e realizados se quiser consistência
            row["META_ACORDO"]       = self._to_float(row.get("META_ACORDO"))
            row["ACORDO_REALIZADO"]  = self._to_float(row.get("ACORDO_REALIZADO"))
            row["META_SALDO"]        = self._to_float(row.get("META_SALDO"))
            row["SALDO_REALIZADO"]   = self._to_float(row.get("SALDO_REALIZADO"))

        return dados

    
