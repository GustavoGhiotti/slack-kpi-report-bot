import os
from datetime import datetime

from src.application.service.backup_service import BackupManager
from src.application.service.builder_service import HtmlBuilder
from src.application.service.meta_service import MetaRelogioService
from src.infrastructure.database.conexao import MetaRelogioOntemRepository
from src.infrastructure.email.email_sender import EmailSender
from src.infrastructure.render.print import PrintRenderer
from src.infrastructure.slack.slack_sender import SlackSender


def enviar_para_slack(img_path):
    hora = datetime.now().strftime("%H")

    canal = os.getenv("SLACK_CANAL_URL", "https://app.slack.com/client/T0000000000/C0000000000")
    sender = SlackSender(canal)
    sender.enviar_imagem(
        imagem_path=img_path,
        mensagem=f" FECHAMENTO D-1 - {hora}H",
    )


def enviar_por_email(img_path):
    EmailSender.enviar_meta_relogio(img_path)


def main():
    repo = MetaRelogioOntemRepository()
    service = MetaRelogioService()
    builder = HtmlBuilder()

    dados = repo.buscar_dados()
    dados_processados = service.processar(dados)
    html = builder.gerar_html(dados_processados)
    caminhos = BackupManager.preparar_caminhos()

    html_path = caminhos["html"].replace("meta_relogio_", "meta_relogio_ontem_")
    img_path = caminhos["img"].replace("meta_relogio_", "meta_relogio_ontem_")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    PrintRenderer.gerar_print(
        html_path=html_path,
        img_path=img_path,
    )

    print("Processo concluido com sucesso:")
    print(f"HTML: {html_path}")
    print(f"PRINT: {img_path}")

    enviar_para_slack(img_path)
    # Envio provisorio: mantem o envio Slack no codigo, mas usa email nesta execucao.
    # enviar_por_email(img_path)


if __name__ == "__main__":
    main()
