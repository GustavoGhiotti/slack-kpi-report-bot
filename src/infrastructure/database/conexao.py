# database/meta_repository.py
import pyodbc
from src.shared.utils.env_load import DB_CONFIG

class MetaRelogioRepository:

    def buscar_dados(self):
        conn = pyodbc.connect(
            f"DRIVER={{SQL Server}};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"UID={DB_CONFIG['user']};"
            f"PWD={DB_CONFIG['password']}"
        )

        query = """
 SET NOCOUNT ON;

        WITH fonte AS (
            SELECT
                CAST(SEGMENTO AS VARCHAR(10)) AS SEGMENTO,
                CAST(FAIXA_ATRASO AS VARCHAR(100)) AS FAIXA_ATRASO,
                COALESCE(
                    TRY_CAST(CONTRATOS AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(CONTRATOS AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS CONTRATOS,
                COALESCE(
                    TRY_CAST(CARTEIRA AS MONEY),
                    TRY_CAST(REPLACE(CAST(CARTEIRA AS VARCHAR(50)), ',', '.') AS MONEY),
                    TRY_CAST(REPLACE(REPLACE(CAST(CARTEIRA AS VARCHAR(50)), '.', ''), ',', '.') AS MONEY)
                ) AS CARTEIRA,
                COALESCE(
                    TRY_CAST(TICKET_MEDIO AS MONEY),
                    TRY_CAST(REPLACE(CAST(TICKET_MEDIO AS VARCHAR(50)), ',', '.') AS MONEY),
                    TRY_CAST(REPLACE(REPLACE(CAST(TICKET_MEDIO AS VARCHAR(50)), '.', ''), ',', '.') AS MONEY)
                ) AS TICKET_MEDIO,
                COALESCE(
                    TRY_CAST(MAILING AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(MAILING AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS MAILING,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ELEGIVEL AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ELEGIVEL AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ELEGIVEL AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ELEGIVEL AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ELEGIVEL,
                COALESCE(
                    TRY_CAST(TRABALHADO AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(TRABALHADO AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS TRABALHADO,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(PENETRACAO AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(PENETRACAO AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(PENETRACAO AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(PENETRACAO AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS PENETRACAO,
                COALESCE(
                    TRY_CAST(META_DISCAGEM AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(META_DISCAGEM AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS META_DISCAGEM,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ICM_DISCAGEM AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ICM_DISCAGEM AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ICM_DISCAGEM AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ICM_DISCAGEM AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ICM_DISCAGEM,
                COALESCE(
                    TRY_CAST(DISCAGEM_REALIZADA AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(DISCAGEM_REALIZADA AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS DISCAGEM_REALIZADA,
                COALESCE(
                    TRY_CAST(META_ATENDIDA AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(META_ATENDIDA AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS META_ATENDIDA,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ICM_ATENDIDA AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ICM_ATENDIDA AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ICM_ATENDIDA AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ICM_ATENDIDA AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ICM_ATENDIDA,
                COALESCE(
                    TRY_CAST(ATENDIMENTO_REALIZADO AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(ATENDIMENTO_REALIZADO AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS ATENDIMENTO_REALIZADO,
                COALESCE(
                    TRY_CAST(META_CPCA AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(META_CPCA AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS META_CPCA,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ICM_CPCA AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ICM_CPCA AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ICM_CPCA AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ICM_CPCA AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ICM_CPCA,
                COALESCE(
                    TRY_CAST(CPCA_REALIZADO AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(CPCA_REALIZADO AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS CPCA_REALIZADO,
                COALESCE(
                    TRY_CAST(META_ACORDO AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(META_ACORDO AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS META_ACORDO,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ICM_ACORDO AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ICM_ACORDO AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ICM_ACORDO AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ICM_ACORDO AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ICM_ACORDO,
                COALESCE(
                    TRY_CAST(ACORDO_REALIZADO AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(ACORDO_REALIZADO AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS ACORDO_REALIZADO,
                COALESCE(
                    TRY_CAST(META_SALDO AS MONEY),
                    TRY_CAST(REPLACE(CAST(META_SALDO AS VARCHAR(50)), ',', '.') AS MONEY),
                    TRY_CAST(REPLACE(REPLACE(CAST(META_SALDO AS VARCHAR(50)), '.', ''), ',', '.') AS MONEY)
                ) AS META_SALDO,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ICM_SALDO AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ICM_SALDO AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ICM_SALDO AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ICM_SALDO AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ICM_SALDO,
                COALESCE(
                    TRY_CAST(SALDO_REALIZADO AS MONEY),
                    TRY_CAST(REPLACE(CAST(SALDO_REALIZADO AS VARCHAR(50)), ',', '.') AS MONEY),
                    TRY_CAST(REPLACE(REPLACE(CAST(SALDO_REALIZADO AS VARCHAR(50)), '.', ''), ',', '.') AS MONEY)
                ) AS SALDO_REALIZADO,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(CONVERSAO AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(CONVERSAO AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(CONVERSAO AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(CONVERSAO AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS CONVERSAO,
                CAST(NULL AS VARCHAR(10)) AS HR_ATUALIZADO
            FROM [10.0.0.72].DB_DADOS.bi.TB_BANCOALFA_META_RELOGIO_SLACK_DIA WITH (NOLOCK)
        )
        SELECT *
        FROM (
            SELECT *
            FROM fonte
            WHERE SEGMENTO = 'EP'
              AND FAIXA_ATRASO NOT IN ('11.MAIOR_720')

            UNION ALL

            SELECT
                'EP' AS SEGMENTO,
                'TOTAL' AS FAIXA_ATRASO,
                SUM(CONTRATOS) AS CONTRATOS,
                SUM(CARTEIRA) AS CARTEIRA,
                SUM(TICKET_MEDIO) AS TICKET_MEDIO,
                SUM(MAILING) AS MAILING,
                ISNULL(SUM(MAILING), 0) * 1.0 / NULLIF(SUM(CONTRATOS), 0) AS ELEGIVEL,
                SUM(TRABALHADO) AS TRABALHADO,
                ISNULL(SUM(TRABALHADO), 0) * 1.0 / NULLIF(SUM(MAILING), 0) AS PENETRACAO,
                SUM(META_DISCAGEM) AS META_DISCAGEM,
                ISNULL(SUM(DISCAGEM_REALIZADA), 0) * 1.0 / NULLIF(SUM(META_DISCAGEM), 0) AS ICM_DISCAGEM,
                SUM(DISCAGEM_REALIZADA) AS DISCAGEM_REALIZADA,
                SUM(META_ATENDIDA) AS META_ATENDIDA,
                ISNULL(SUM(ATENDIMENTO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ATENDIDA), 0) AS ICM_ATENDIDA,
                SUM(ATENDIMENTO_REALIZADO) AS ATENDIMENTO_REALIZADO,
                SUM(META_CPCA) AS META_CPCA,
                ISNULL(SUM(CPCA_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_CPCA), 0) AS ICM_CPCA,
                SUM(CPCA_REALIZADO) AS CPCA_REALIZADO,
                SUM(META_ACORDO) AS META_ACORDO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ACORDO), 0) AS ICM_ACORDO,
                SUM(ACORDO_REALIZADO) AS ACORDO_REALIZADO,
                SUM(META_SALDO) AS META_SALDO,
                ISNULL(SUM(SALDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_SALDO), 0) AS ICM_SALDO,
                SUM(SALDO_REALIZADO) AS SALDO_REALIZADO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(CPCA_REALIZADO), 0) AS CONVERSAO,
                MAX(HR_ATUALIZADO) AS HR_ATUALIZADO
            FROM fonte
            WHERE SEGMENTO = 'EP'
              AND FAIXA_ATRASO NOT IN ('11.MAIOR_720')

            UNION ALL

            SELECT *
            FROM fonte
            WHERE SEGMENTO = 'CT'
              AND FAIXA_ATRASO NOT IN ('10.361-720', '11.MAIOR_720')

            UNION ALL

            SELECT
                'CT' AS SEGMENTO,
                'TOTAL FASE 1' AS FAIXA_ATRASO,
                SUM(CONTRATOS) AS CONTRATOS,
                SUM(CARTEIRA) AS CARTEIRA,
                SUM(TICKET_MEDIO) AS TICKET_MEDIO,
                SUM(MAILING) AS MAILING,
                ISNULL(SUM(MAILING), 0) * 1.0 / NULLIF(SUM(CONTRATOS), 0) AS ELEGIVEL,
                SUM(TRABALHADO) AS TRABALHADO,
                ISNULL(SUM(TRABALHADO), 0) * 1.0 / NULLIF(SUM(MAILING), 0) AS PENETRACAO,
                SUM(META_DISCAGEM) AS META_DISCAGEM,
                ISNULL(SUM(DISCAGEM_REALIZADA), 0) * 1.0 / NULLIF(SUM(META_DISCAGEM), 0) AS ICM_DISCAGEM,
                SUM(DISCAGEM_REALIZADA) AS DISCAGEM_REALIZADA,
                SUM(META_ATENDIDA) AS META_ATENDIDA,
                ISNULL(SUM(ATENDIMENTO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ATENDIDA), 0) AS ICM_ATENDIDA,
                SUM(ATENDIMENTO_REALIZADO) AS ATENDIMENTO_REALIZADO,
                SUM(META_CPCA) AS META_CPCA,
                ISNULL(SUM(CPCA_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_CPCA), 0) AS ICM_CPCA,
                SUM(CPCA_REALIZADO) AS CPCA_REALIZADO,
                SUM(META_ACORDO) AS META_ACORDO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ACORDO), 0) AS ICM_ACORDO,
                SUM(ACORDO_REALIZADO) AS ACORDO_REALIZADO,
                SUM(META_SALDO) AS META_SALDO,
                ISNULL(SUM(SALDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_SALDO), 0) AS ICM_SALDO,
                SUM(SALDO_REALIZADO) AS SALDO_REALIZADO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(CPCA_REALIZADO), 0) AS CONVERSAO,
                MAX(HR_ATUALIZADO) AS HR_ATUALIZADO
            FROM fonte
            WHERE SEGMENTO = 'CT'
              AND FAIXA_ATRASO IN ('01.000-032', '02.033-060', '03.061-090')

            UNION ALL

            SELECT
                'CT' AS SEGMENTO,
                'TOTAL FASE 2' AS FAIXA_ATRASO,
                SUM(CONTRATOS) AS CONTRATOS,
                SUM(CARTEIRA) AS CARTEIRA,
                SUM(TICKET_MEDIO) AS TICKET_MEDIO,
                SUM(MAILING) AS MAILING,
                ISNULL(SUM(MAILING), 0) * 1.0 / NULLIF(SUM(CONTRATOS), 0) AS ELEGIVEL,
                SUM(TRABALHADO) AS TRABALHADO,
                ISNULL(SUM(TRABALHADO), 0) * 1.0 / NULLIF(SUM(MAILING), 0) AS PENETRACAO,
                SUM(META_DISCAGEM) AS META_DISCAGEM,
                ISNULL(SUM(DISCAGEM_REALIZADA), 0) * 1.0 / NULLIF(SUM(META_DISCAGEM), 0) AS ICM_DISCAGEM,
                SUM(DISCAGEM_REALIZADA) AS DISCAGEM_REALIZADA,
                SUM(META_ATENDIDA) AS META_ATENDIDA,
                ISNULL(SUM(ATENDIMENTO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ATENDIDA), 0) AS ICM_ATENDIDA,
                SUM(ATENDIMENTO_REALIZADO) AS ATENDIMENTO_REALIZADO,
                SUM(META_CPCA) AS META_CPCA,
                ISNULL(SUM(CPCA_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_CPCA), 0) AS ICM_CPCA,
                SUM(CPCA_REALIZADO) AS CPCA_REALIZADO,
                SUM(META_ACORDO) AS META_ACORDO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ACORDO), 0) AS ICM_ACORDO,
                SUM(ACORDO_REALIZADO) AS ACORDO_REALIZADO,
                SUM(META_SALDO) AS META_SALDO,
                ISNULL(SUM(SALDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_SALDO), 0) AS ICM_SALDO,
                SUM(SALDO_REALIZADO) AS SALDO_REALIZADO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(CPCA_REALIZADO), 0) AS CONVERSAO,
                MAX(HR_ATUALIZADO) AS HR_ATUALIZADO
            FROM fonte
            WHERE SEGMENTO = 'CT'
              AND FAIXA_ATRASO IN ('04.091-120', '05.121-150', '06.151-180', '07.181-210', '08.211-240', '09.241-360')
        ) AS dados
        ORDER BY
            SEGMENTO,
            CASE
                WHEN SEGMENTO = 'CT' THEN
                    CASE
                        WHEN FAIXA_ATRASO = '01.000-032' THEN 10
                        WHEN FAIXA_ATRASO = '02.033-060' THEN 20
                        WHEN FAIXA_ATRASO = '03.061-090' THEN 30
                        WHEN FAIXA_ATRASO = 'TOTAL FASE 1' THEN 40
                        WHEN FAIXA_ATRASO = '04.091-120' THEN 50
                        WHEN FAIXA_ATRASO = '05.121-150' THEN 60
                        WHEN FAIXA_ATRASO = '06.151-180' THEN 70
                        WHEN FAIXA_ATRASO = '07.181-210' THEN 80
                        WHEN FAIXA_ATRASO = '08.211-240' THEN 90
                        WHEN FAIXA_ATRASO = '09.241-360' THEN 100
                        WHEN FAIXA_ATRASO = 'TOTAL FASE 2' THEN 110
                        ELSE 999
                    END
                ELSE
                    CASE
                        WHEN FAIXA_ATRASO = 'TOTAL' THEN 999
                        ELSE 0
                    END
            END,
            FAIXA_ATRASO;
        """


        cursor = conn.cursor()
        cursor.execute(query)

        while cursor.description is None and cursor.nextset():
            pass

        columns = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

        conn.close()

        return [dict(zip(columns, row)) for row in rows]


class MetaRelogioOntemRepository:

    def buscar_dados(self):
        conn = pyodbc.connect(
            f"DRIVER={{SQL Server}};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"UID={DB_CONFIG['user']};"
            f"PWD={DB_CONFIG['password']}"
        )

        query = """
        SET NOCOUNT ON;

        WITH fonte AS (
            SELECT
                CAST(SEGMENTO AS VARCHAR(10)) AS SEGMENTO,
                CAST(FAIXA_ATRASO AS VARCHAR(100)) AS FAIXA_ATRASO,
                COALESCE(
                    TRY_CAST(CONTRATOS AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(CONTRATOS AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS CONTRATOS,
                COALESCE(
                    TRY_CAST(CARTEIRA AS MONEY),
                    TRY_CAST(REPLACE(CAST(CARTEIRA AS VARCHAR(50)), ',', '.') AS MONEY),
                    TRY_CAST(REPLACE(REPLACE(CAST(CARTEIRA AS VARCHAR(50)), '.', ''), ',', '.') AS MONEY)
                ) AS CARTEIRA,
                COALESCE(
                    TRY_CAST(TICKET_MEDIO AS MONEY),
                    TRY_CAST(REPLACE(CAST(TICKET_MEDIO AS VARCHAR(50)), ',', '.') AS MONEY),
                    TRY_CAST(REPLACE(REPLACE(CAST(TICKET_MEDIO AS VARCHAR(50)), '.', ''), ',', '.') AS MONEY)
                ) AS TICKET_MEDIO,
                COALESCE(
                    TRY_CAST(MAILING AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(MAILING AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS MAILING,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ELEGIVEL AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ELEGIVEL AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ELEGIVEL AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ELEGIVEL AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ELEGIVEL,
                COALESCE(
                    TRY_CAST(TRABALHADO AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(TRABALHADO AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS TRABALHADO,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(PENETRACAO AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(PENETRACAO AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(PENETRACAO AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(PENETRACAO AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS PENETRACAO,
                COALESCE(
                    TRY_CAST(META_DISCAGEM AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(META_DISCAGEM AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS META_DISCAGEM,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ICM_DISCAGEM AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ICM_DISCAGEM AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ICM_DISCAGEM AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ICM_DISCAGEM AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ICM_DISCAGEM,
                COALESCE(
                    TRY_CAST(DISCAGEM_REALIZADA AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(DISCAGEM_REALIZADA AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS DISCAGEM_REALIZADA,
                COALESCE(
                    TRY_CAST(META_ATENDIDA AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(META_ATENDIDA AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS META_ATENDIDA,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ICM_ATENDIDA AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ICM_ATENDIDA AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ICM_ATENDIDA AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ICM_ATENDIDA AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ICM_ATENDIDA,
                COALESCE(
                    TRY_CAST(ATENDIMENTO_REALIZADO AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(ATENDIMENTO_REALIZADO AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS ATENDIMENTO_REALIZADO,
                COALESCE(
                    TRY_CAST(META_CPCA AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(META_CPCA AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS META_CPCA,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ICM_CPCA AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ICM_CPCA AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ICM_CPCA AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ICM_CPCA AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ICM_CPCA,
                COALESCE(
                    TRY_CAST(CPCA_REALIZADO AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(CPCA_REALIZADO AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS CPCA_REALIZADO,
                COALESCE(
                    TRY_CAST(META_ACORDO AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(META_ACORDO AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS META_ACORDO,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ICM_ACORDO AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ICM_ACORDO AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ICM_ACORDO AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ICM_ACORDO AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ICM_ACORDO,
                COALESCE(
                    TRY_CAST(ACORDO_REALIZADO AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(ACORDO_REALIZADO AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS ACORDO_REALIZADO,
                COALESCE(
                    TRY_CAST(META_SALDO AS MONEY),
                    TRY_CAST(REPLACE(CAST(META_SALDO AS VARCHAR(50)), ',', '.') AS MONEY),
                    TRY_CAST(REPLACE(REPLACE(CAST(META_SALDO AS VARCHAR(50)), '.', ''), ',', '.') AS MONEY)
                ) AS META_SALDO,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ICM_SALDO AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ICM_SALDO AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ICM_SALDO AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ICM_SALDO AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ICM_SALDO,
                COALESCE(
                    TRY_CAST(SALDO_REALIZADO AS MONEY),
                    TRY_CAST(REPLACE(CAST(SALDO_REALIZADO AS VARCHAR(50)), ',', '.') AS MONEY),
                    TRY_CAST(REPLACE(REPLACE(CAST(SALDO_REALIZADO AS VARCHAR(50)), '.', ''), ',', '.') AS MONEY)
                ) AS SALDO_REALIZADO,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(CONVERSAO AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(CONVERSAO AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(CONVERSAO AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(CONVERSAO AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS CONVERSAO,
                CAST(NULL AS VARCHAR(10)) AS HR_ATUALIZADO
            FROM [10.0.0.72].DB_DADOS.bi.TB_BANCOALFA_META_RELOGIO_SLACK_DIA_ANTERIOR WITH (NOLOCK)
        )
        SELECT *
        FROM (
            SELECT *
            FROM fonte
            WHERE SEGMENTO = 'EP'
              AND FAIXA_ATRASO NOT IN ('11.MAIOR_720')

            UNION ALL

            SELECT
                'EP' AS SEGMENTO,
                'TOTAL' AS FAIXA_ATRASO,
                SUM(CONTRATOS) AS CONTRATOS,
                SUM(CARTEIRA) AS CARTEIRA,
                SUM(TICKET_MEDIO) AS TICKET_MEDIO,
                SUM(MAILING) AS MAILING,
                ISNULL(SUM(MAILING), 0) * 1.0 / NULLIF(SUM(CONTRATOS), 0) AS ELEGIVEL,
                SUM(TRABALHADO) AS TRABALHADO,
                ISNULL(SUM(TRABALHADO), 0) * 1.0 / NULLIF(SUM(MAILING), 0) AS PENETRACAO,
                SUM(META_DISCAGEM) AS META_DISCAGEM,
                ISNULL(SUM(DISCAGEM_REALIZADA), 0) * 1.0 / NULLIF(SUM(META_DISCAGEM), 0) AS ICM_DISCAGEM,
                SUM(DISCAGEM_REALIZADA) AS DISCAGEM_REALIZADA,
                SUM(META_ATENDIDA) AS META_ATENDIDA,
                ISNULL(SUM(ATENDIMENTO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ATENDIDA), 0) AS ICM_ATENDIDA,
                SUM(ATENDIMENTO_REALIZADO) AS ATENDIMENTO_REALIZADO,
                SUM(META_CPCA) AS META_CPCA,
                ISNULL(SUM(CPCA_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_CPCA), 0) AS ICM_CPCA,
                SUM(CPCA_REALIZADO) AS CPCA_REALIZADO,
                SUM(META_ACORDO) AS META_ACORDO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ACORDO), 0) AS ICM_ACORDO,
                SUM(ACORDO_REALIZADO) AS ACORDO_REALIZADO,
                SUM(META_SALDO) AS META_SALDO,
                ISNULL(SUM(SALDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_SALDO), 0) AS ICM_SALDO,
                SUM(SALDO_REALIZADO) AS SALDO_REALIZADO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(CPCA_REALIZADO), 0) AS CONVERSAO,
                MAX(HR_ATUALIZADO) AS HR_ATUALIZADO
            FROM fonte
            WHERE SEGMENTO = 'EP'
              AND FAIXA_ATRASO NOT IN ('11.MAIOR_720')

            UNION ALL

            SELECT *
            FROM fonte
            WHERE SEGMENTO = 'CT'
              AND FAIXA_ATRASO NOT IN ('10.361-720', '11.MAIOR_720')

            UNION ALL

            SELECT
                'CT' AS SEGMENTO,
                'TOTAL FASE 1' AS FAIXA_ATRASO,
                SUM(CONTRATOS) AS CONTRATOS,
                SUM(CARTEIRA) AS CARTEIRA,
                SUM(TICKET_MEDIO) AS TICKET_MEDIO,
                SUM(MAILING) AS MAILING,
                ISNULL(SUM(MAILING), 0) * 1.0 / NULLIF(SUM(CONTRATOS), 0) AS ELEGIVEL,
                SUM(TRABALHADO) AS TRABALHADO,
                ISNULL(SUM(TRABALHADO), 0) * 1.0 / NULLIF(SUM(MAILING), 0) AS PENETRACAO,
                SUM(META_DISCAGEM) AS META_DISCAGEM,
                ISNULL(SUM(DISCAGEM_REALIZADA), 0) * 1.0 / NULLIF(SUM(META_DISCAGEM), 0) AS ICM_DISCAGEM,
                SUM(DISCAGEM_REALIZADA) AS DISCAGEM_REALIZADA,
                SUM(META_ATENDIDA) AS META_ATENDIDA,
                ISNULL(SUM(ATENDIMENTO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ATENDIDA), 0) AS ICM_ATENDIDA,
                SUM(ATENDIMENTO_REALIZADO) AS ATENDIMENTO_REALIZADO,
                SUM(META_CPCA) AS META_CPCA,
                ISNULL(SUM(CPCA_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_CPCA), 0) AS ICM_CPCA,
                SUM(CPCA_REALIZADO) AS CPCA_REALIZADO,
                SUM(META_ACORDO) AS META_ACORDO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ACORDO), 0) AS ICM_ACORDO,
                SUM(ACORDO_REALIZADO) AS ACORDO_REALIZADO,
                SUM(META_SALDO) AS META_SALDO,
                ISNULL(SUM(SALDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_SALDO), 0) AS ICM_SALDO,
                SUM(SALDO_REALIZADO) AS SALDO_REALIZADO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(CPCA_REALIZADO), 0) AS CONVERSAO,
                MAX(HR_ATUALIZADO) AS HR_ATUALIZADO
            FROM fonte
            WHERE SEGMENTO = 'CT'
              AND FAIXA_ATRASO IN ('01.000-032', '02.033-060', '03.061-090')

            UNION ALL

            SELECT
                'CT' AS SEGMENTO,
                'TOTAL FASE 2' AS FAIXA_ATRASO,
                SUM(CONTRATOS) AS CONTRATOS,
                SUM(CARTEIRA) AS CARTEIRA,
                SUM(TICKET_MEDIO) AS TICKET_MEDIO,
                SUM(MAILING) AS MAILING,
                ISNULL(SUM(MAILING), 0) * 1.0 / NULLIF(SUM(CONTRATOS), 0) AS ELEGIVEL,
                SUM(TRABALHADO) AS TRABALHADO,
                ISNULL(SUM(TRABALHADO), 0) * 1.0 / NULLIF(SUM(MAILING), 0) AS PENETRACAO,
                SUM(META_DISCAGEM) AS META_DISCAGEM,
                ISNULL(SUM(DISCAGEM_REALIZADA), 0) * 1.0 / NULLIF(SUM(META_DISCAGEM), 0) AS ICM_DISCAGEM,
                SUM(DISCAGEM_REALIZADA) AS DISCAGEM_REALIZADA,
                SUM(META_ATENDIDA) AS META_ATENDIDA,
                ISNULL(SUM(ATENDIMENTO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ATENDIDA), 0) AS ICM_ATENDIDA,
                SUM(ATENDIMENTO_REALIZADO) AS ATENDIMENTO_REALIZADO,
                SUM(META_CPCA) AS META_CPCA,
                ISNULL(SUM(CPCA_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_CPCA), 0) AS ICM_CPCA,
                SUM(CPCA_REALIZADO) AS CPCA_REALIZADO,
                SUM(META_ACORDO) AS META_ACORDO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ACORDO), 0) AS ICM_ACORDO,
                SUM(ACORDO_REALIZADO) AS ACORDO_REALIZADO,
                SUM(META_SALDO) AS META_SALDO,
                ISNULL(SUM(SALDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_SALDO), 0) AS ICM_SALDO,
                SUM(SALDO_REALIZADO) AS SALDO_REALIZADO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(CPCA_REALIZADO), 0) AS CONVERSAO,
                MAX(HR_ATUALIZADO) AS HR_ATUALIZADO
            FROM fonte
            WHERE SEGMENTO = 'CT'
              AND FAIXA_ATRASO IN ('04.091-120', '05.121-150', '06.151-180', '07.181-210', '08.211-240', '09.241-360')
        ) AS dados
        ORDER BY
            SEGMENTO,
            CASE
                WHEN SEGMENTO = 'CT' THEN
                    CASE
                        WHEN FAIXA_ATRASO = '01.000-032' THEN 10
                        WHEN FAIXA_ATRASO = '02.033-060' THEN 20
                        WHEN FAIXA_ATRASO = '03.061-090' THEN 30
                        WHEN FAIXA_ATRASO = 'TOTAL FASE 1' THEN 40
                        WHEN FAIXA_ATRASO = '04.091-120' THEN 50
                        WHEN FAIXA_ATRASO = '05.121-150' THEN 60
                        WHEN FAIXA_ATRASO = '06.151-180' THEN 70
                        WHEN FAIXA_ATRASO = '07.181-210' THEN 80
                        WHEN FAIXA_ATRASO = '08.211-240' THEN 90
                        WHEN FAIXA_ATRASO = '09.241-360' THEN 100
                        WHEN FAIXA_ATRASO = 'TOTAL FASE 2' THEN 110
                        ELSE 999
                    END
                ELSE
                    CASE
                        WHEN FAIXA_ATRASO = 'TOTAL' THEN 999
                        ELSE 0
                    END
            END,
            FAIXA_ATRASO;
        """

        cursor = conn.cursor()
        cursor.execute(query)

        while cursor.description is None and cursor.nextset():
            pass

        columns = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

        conn.close()

        return [dict(zip(columns, row)) for row in rows]


class MetaRelogioConsolidadoRepository:

    def buscar_dados(self):
        conn = pyodbc.connect(
            f"DRIVER={{SQL Server}};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"UID={DB_CONFIG['user']};"
            f"PWD={DB_CONFIG['password']}"
        )

        query = """
         SET NOCOUNT ON;

        WITH fonte AS (
            SELECT
                CAST(SEGMENTO AS VARCHAR(10)) AS SEGMENTO,
                CAST(FAIXA_ATRASO AS VARCHAR(100)) AS FAIXA_ATRASO,
                COALESCE(
                    TRY_CAST(CONTRATOS AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(CONTRATOS AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS CONTRATOS,
                COALESCE(
                    TRY_CAST(CARTEIRA AS MONEY),
                    TRY_CAST(REPLACE(CAST(CARTEIRA AS VARCHAR(50)), ',', '.') AS MONEY),
                    TRY_CAST(REPLACE(REPLACE(CAST(CARTEIRA AS VARCHAR(50)), '.', ''), ',', '.') AS MONEY)
                ) AS CARTEIRA,
                COALESCE(
                    TRY_CAST(TICKET_MEDIO AS MONEY),
                    TRY_CAST(REPLACE(CAST(TICKET_MEDIO AS VARCHAR(50)), ',', '.') AS MONEY),
                    TRY_CAST(REPLACE(REPLACE(CAST(TICKET_MEDIO AS VARCHAR(50)), '.', ''), ',', '.') AS MONEY)
                ) AS TICKET_MEDIO,
                COALESCE(
                    TRY_CAST(MAILING AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(MAILING AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS MAILING,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ELEGIVEL AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ELEGIVEL AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ELEGIVEL AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ELEGIVEL AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ELEGIVEL AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ELEGIVEL,
                COALESCE(
                    TRY_CAST(TRABALHADO AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(TRABALHADO AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS TRABALHADO,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(PENETRACAO AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(PENETRACAO AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(PENETRACAO AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(PENETRACAO AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(PENETRACAO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS PENETRACAO,
                COALESCE(
                    TRY_CAST(META_DISCAGEM AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(META_DISCAGEM AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS META_DISCAGEM,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ICM_DISCAGEM AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ICM_DISCAGEM AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ICM_DISCAGEM AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ICM_DISCAGEM AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ICM_DISCAGEM AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ICM_DISCAGEM,
                COALESCE(
                    TRY_CAST(DISCAGEM_REALIZADA AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(DISCAGEM_REALIZADA AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS DISCAGEM_REALIZADA,
                COALESCE(
                    TRY_CAST(META_ATENDIDA AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(META_ATENDIDA AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS META_ATENDIDA,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ICM_ATENDIDA AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ICM_ATENDIDA AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ICM_ATENDIDA AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ICM_ATENDIDA AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ICM_ATENDIDA AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ICM_ATENDIDA,
                COALESCE(
                    TRY_CAST(ATENDIMENTO_REALIZADO AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(ATENDIMENTO_REALIZADO AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS ATENDIMENTO_REALIZADO,
                COALESCE(
                    TRY_CAST(META_CPCA AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(META_CPCA AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS META_CPCA,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ICM_CPCA AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ICM_CPCA AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ICM_CPCA AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ICM_CPCA AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ICM_CPCA AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ICM_CPCA,
                COALESCE(
                    TRY_CAST(CPCA_REALIZADO AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(CPCA_REALIZADO AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS CPCA_REALIZADO,
                COALESCE(
                    TRY_CAST(META_ACORDO AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(META_ACORDO AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS META_ACORDO,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ICM_ACORDO AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ICM_ACORDO AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ICM_ACORDO AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ICM_ACORDO AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ICM_ACORDO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ICM_ACORDO,
                COALESCE(
                    TRY_CAST(ACORDO_REALIZADO AS BIGINT),
                    TRY_CAST(REPLACE(REPLACE(CAST(ACORDO_REALIZADO AS VARCHAR(50)), '.', ''), ',', '') AS BIGINT)
                ) AS ACORDO_REALIZADO,
                COALESCE(
                    TRY_CAST(META_SALDO AS MONEY),
                    TRY_CAST(REPLACE(CAST(META_SALDO AS VARCHAR(50)), ',', '.') AS MONEY),
                    TRY_CAST(REPLACE(REPLACE(CAST(META_SALDO AS VARCHAR(50)), '.', ''), ',', '.') AS MONEY)
                ) AS META_SALDO,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(ICM_SALDO AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(ICM_SALDO AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(ICM_SALDO AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(ICM_SALDO AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(ICM_SALDO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS ICM_SALDO,
                COALESCE(
                    TRY_CAST(SALDO_REALIZADO AS MONEY),
                    TRY_CAST(REPLACE(CAST(SALDO_REALIZADO AS VARCHAR(50)), ',', '.') AS MONEY),
                    TRY_CAST(REPLACE(REPLACE(CAST(SALDO_REALIZADO AS VARCHAR(50)), '.', ''), ',', '.') AS MONEY)
                ) AS SALDO_REALIZADO,
                CASE
                    WHEN NULLIF(LTRIM(RTRIM(CAST(CONVERSAO AS VARCHAR(50)))), '') IS NULL THEN NULL
                    WHEN CHARINDEX('%', CAST(CONVERSAO AS VARCHAR(50))) > 0
                        THEN COALESCE(
                            TRY_CAST(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), '%', '') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), '%', ''), '.', ''), ',', '.') AS DECIMAL(18,6)),
                            TRY_CAST(REPLACE(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), '%', ''), ',', '.') AS DECIMAL(18,6))
                        ) / 100
                    ELSE COALESCE(
                        TRY_CAST(CONVERSAO AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                        TRY_CAST(REPLACE(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                    ) / CASE
                            WHEN COALESCE(
                                TRY_CAST(CONVERSAO AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), ',', '.') AS DECIMAL(18,6)),
                                TRY_CAST(REPLACE(REPLACE(CAST(CONVERSAO AS VARCHAR(50)), '.', ''), ',', '.') AS DECIMAL(18,6))
                            ) > 1 THEN 100
                            ELSE 1
                        END
                END AS CONVERSAO,
                CAST(NULL AS VARCHAR(10)) AS HR_ATUALIZADO
            FROM [10.0.0.72].DB_DADOS.bi.TB_BANCOALFA_META_RELOGIO_SLACK_CONSOLIDADO WITH (NOLOCK)
        )
        SELECT *
        FROM (
            SELECT *
            FROM fonte
            WHERE SEGMENTO = 'EP'
              AND FAIXA_ATRASO NOT IN ('11.MAIOR_720')

            UNION ALL

            SELECT
                'EP' AS SEGMENTO,
                'TOTAL' AS FAIXA_ATRASO,
                SUM(CONTRATOS) AS CONTRATOS,
                SUM(CARTEIRA) AS CARTEIRA,
                SUM(TICKET_MEDIO) AS TICKET_MEDIO,
                SUM(MAILING) AS MAILING,
                ISNULL(SUM(MAILING), 0) * 1.0 / NULLIF(SUM(CONTRATOS), 0) AS ELEGIVEL,
                SUM(TRABALHADO) AS TRABALHADO,
                ISNULL(SUM(TRABALHADO), 0) * 1.0 / NULLIF(SUM(MAILING), 0) AS PENETRACAO,
                SUM(META_DISCAGEM) AS META_DISCAGEM,
                ISNULL(SUM(DISCAGEM_REALIZADA), 0) * 1.0 / NULLIF(SUM(META_DISCAGEM), 0) AS ICM_DISCAGEM,
                SUM(DISCAGEM_REALIZADA) AS DISCAGEM_REALIZADA,
                SUM(META_ATENDIDA) AS META_ATENDIDA,
                ISNULL(SUM(ATENDIMENTO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ATENDIDA), 0) AS ICM_ATENDIDA,
                SUM(ATENDIMENTO_REALIZADO) AS ATENDIMENTO_REALIZADO,
                SUM(META_CPCA) AS META_CPCA,
                ISNULL(SUM(CPCA_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_CPCA), 0) AS ICM_CPCA,
                SUM(CPCA_REALIZADO) AS CPCA_REALIZADO,
                SUM(META_ACORDO) AS META_ACORDO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ACORDO), 0) AS ICM_ACORDO,
                SUM(ACORDO_REALIZADO) AS ACORDO_REALIZADO,
                SUM(META_SALDO) AS META_SALDO,
                ISNULL(SUM(SALDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_SALDO), 0) AS ICM_SALDO,
                SUM(SALDO_REALIZADO) AS SALDO_REALIZADO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(CPCA_REALIZADO), 0) AS CONVERSAO,
                MAX(HR_ATUALIZADO) AS HR_ATUALIZADO
            FROM fonte
            WHERE SEGMENTO = 'EP'
              AND FAIXA_ATRASO NOT IN ('11.MAIOR_720')

            UNION ALL

            SELECT *
            FROM fonte
            WHERE SEGMENTO = 'CT'
              AND FAIXA_ATRASO NOT IN ('10.361-720', '11.MAIOR_720')

            UNION ALL

            SELECT
                'CT' AS SEGMENTO,
                'TOTAL FASE 1' AS FAIXA_ATRASO,
                SUM(CONTRATOS) AS CONTRATOS,
                SUM(CARTEIRA) AS CARTEIRA,
                SUM(TICKET_MEDIO) AS TICKET_MEDIO,
                SUM(MAILING) AS MAILING,
                ISNULL(SUM(MAILING), 0) * 1.0 / NULLIF(SUM(CONTRATOS), 0) AS ELEGIVEL,
                SUM(TRABALHADO) AS TRABALHADO,
                ISNULL(SUM(TRABALHADO), 0) * 1.0 / NULLIF(SUM(MAILING), 0) AS PENETRACAO,
                SUM(META_DISCAGEM) AS META_DISCAGEM,
                ISNULL(SUM(DISCAGEM_REALIZADA), 0) * 1.0 / NULLIF(SUM(META_DISCAGEM), 0) AS ICM_DISCAGEM,
                SUM(DISCAGEM_REALIZADA) AS DISCAGEM_REALIZADA,
                SUM(META_ATENDIDA) AS META_ATENDIDA,
                ISNULL(SUM(ATENDIMENTO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ATENDIDA), 0) AS ICM_ATENDIDA,
                SUM(ATENDIMENTO_REALIZADO) AS ATENDIMENTO_REALIZADO,
                SUM(META_CPCA) AS META_CPCA,
                ISNULL(SUM(CPCA_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_CPCA), 0) AS ICM_CPCA,
                SUM(CPCA_REALIZADO) AS CPCA_REALIZADO,
                SUM(META_ACORDO) AS META_ACORDO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ACORDO), 0) AS ICM_ACORDO,
                SUM(ACORDO_REALIZADO) AS ACORDO_REALIZADO,
                SUM(META_SALDO) AS META_SALDO,
                ISNULL(SUM(SALDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_SALDO), 0) AS ICM_SALDO,
                SUM(SALDO_REALIZADO) AS SALDO_REALIZADO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(CPCA_REALIZADO), 0) AS CONVERSAO,
                MAX(HR_ATUALIZADO) AS HR_ATUALIZADO
            FROM fonte
            WHERE SEGMENTO = 'CT'
              AND FAIXA_ATRASO IN ('01.000-032', '02.033-060', '03.061-090')

            UNION ALL

            SELECT
                'CT' AS SEGMENTO,
                'TOTAL FASE 2' AS FAIXA_ATRASO,
                SUM(CONTRATOS) AS CONTRATOS,
                SUM(CARTEIRA) AS CARTEIRA,
                SUM(TICKET_MEDIO) AS TICKET_MEDIO,
                SUM(MAILING) AS MAILING,
                ISNULL(SUM(MAILING), 0) * 1.0 / NULLIF(SUM(CONTRATOS), 0) AS ELEGIVEL,
                SUM(TRABALHADO) AS TRABALHADO,
                ISNULL(SUM(TRABALHADO), 0) * 1.0 / NULLIF(SUM(MAILING), 0) AS PENETRACAO,
                SUM(META_DISCAGEM) AS META_DISCAGEM,
                ISNULL(SUM(DISCAGEM_REALIZADA), 0) * 1.0 / NULLIF(SUM(META_DISCAGEM), 0) AS ICM_DISCAGEM,
                SUM(DISCAGEM_REALIZADA) AS DISCAGEM_REALIZADA,
                SUM(META_ATENDIDA) AS META_ATENDIDA,
                ISNULL(SUM(ATENDIMENTO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ATENDIDA), 0) AS ICM_ATENDIDA,
                SUM(ATENDIMENTO_REALIZADO) AS ATENDIMENTO_REALIZADO,
                SUM(META_CPCA) AS META_CPCA,
                ISNULL(SUM(CPCA_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_CPCA), 0) AS ICM_CPCA,
                SUM(CPCA_REALIZADO) AS CPCA_REALIZADO,
                SUM(META_ACORDO) AS META_ACORDO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_ACORDO), 0) AS ICM_ACORDO,
                SUM(ACORDO_REALIZADO) AS ACORDO_REALIZADO,
                SUM(META_SALDO) AS META_SALDO,
                ISNULL(SUM(SALDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(META_SALDO), 0) AS ICM_SALDO,
                SUM(SALDO_REALIZADO) AS SALDO_REALIZADO,
                ISNULL(SUM(ACORDO_REALIZADO), 0) * 1.0 / NULLIF(SUM(CPCA_REALIZADO), 0) AS CONVERSAO,
                MAX(HR_ATUALIZADO) AS HR_ATUALIZADO
            FROM fonte
            WHERE SEGMENTO = 'CT'
              AND FAIXA_ATRASO IN ('04.091-120', '05.121-150', '06.151-180', '07.181-210', '08.211-240', '09.241-360')
        ) AS dados
        ORDER BY
            SEGMENTO,
            CASE
                WHEN SEGMENTO = 'CT' THEN
                    CASE
                        WHEN FAIXA_ATRASO = '01.000-032' THEN 10
                        WHEN FAIXA_ATRASO = '02.033-060' THEN 20
                        WHEN FAIXA_ATRASO = '03.061-090' THEN 30
                        WHEN FAIXA_ATRASO = 'TOTAL FASE 1' THEN 40
                        WHEN FAIXA_ATRASO = '04.091-120' THEN 50
                        WHEN FAIXA_ATRASO = '05.121-150' THEN 60
                        WHEN FAIXA_ATRASO = '06.151-180' THEN 70
                        WHEN FAIXA_ATRASO = '07.181-210' THEN 80
                        WHEN FAIXA_ATRASO = '08.211-240' THEN 90
                        WHEN FAIXA_ATRASO = '09.241-360' THEN 100
                        WHEN FAIXA_ATRASO = 'TOTAL FASE 2' THEN 110
                        ELSE 999
                    END
                ELSE
                    CASE
                        WHEN FAIXA_ATRASO = 'TOTAL' THEN 999
                        ELSE 0
                    END
            END,
            FAIXA_ATRASO;
        """

        cursor = conn.cursor()
        cursor.execute(query)

        while cursor.description is None and cursor.nextset():
            pass

        columns = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

        conn.close()

        return [dict(zip(columns, row)) for row in rows]
