# Slack KPI Report Bot

> **Versão de portfólio.** Código real de produção, anonimizado: nomes de empresa, clientes, pessoas, hosts, e-mails e credenciais foram trocados por valores fictícios (`Acme`, `Banco Alfa`, `10.0.0.x`, `empresa.example`). Toda configuração sensível vem do `.env` (modelo em `.env.example`). O código não aponta para nenhum sistema real.

Robô que consulta indicadores de produção no SQL Server, monta um painel HTML ("meta relógio" e consolidados D-1), renderiza como imagem com Playwright e publica no Slack e por e-mail em horários agendados.

**Stack:** Python, pyodbc/SQL Server, Playwright, SMTP

## Destaques

- Pipeline repositório → serviço de cálculo → `HtmlBuilder` → `PrintRenderer` (screenshot) → envio.
- Versões de conferência que publicam em canal separado antes do envio oficial.
- Backup de cada HTML/imagem gerado.

## Estrutura

```text
slack-kpi-report-bot/
├── src/
│   ├── application/
│   │   ├── service/
│   │   └── templates/
│   ├── infrastructure/
│   │   ├── database/
│   │   ├── email/
│   │   ├── render/
│   │   └── slack/
│   └── shared/
│       └── utils/
├── consolidado.py
├── consolidado_conferencia.py
├── main_ontem.py
├── main_ontem_conferencia.py
├── metarelogio.py
└── requirements.txt
```

## Como executar

```bash
pip install -r requirements.txt && playwright install chromium
python main_ontem.py
```
