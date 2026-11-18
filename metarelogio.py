from datetime import datetime

import os
from src.application.service.backup_service import BackupManager
from src.application.service.builder_service import HtmlBuilder
from src.application.service.meta_service import MetaRelogioService
from src.infrastructure.database.conexao import MetaRelogioRepository
from src.infrastructure.email.email_sender import EmailSender
from src.infrastructure.render.print import PrintRenderer
from src.infrastructure.slack.slack_sender import SlackSender


def enviar_para_slack(img_path):
    hora = datetime.now().strftime("%H")

    canal = os.getenv("SLACK_CANAL_URL", "https://app.slack.com/client/T0000000000/C0000000000")
    sender = SlackSender(canal)
    sender.enviar_imagem(
        imagem_path=img_path,
        mensagem=f" PARCIAL META RELOGIO - {hora}H",
    )


def enviar_por_email(img_path):
    EmailSender.enviar_meta_relogio(img_path)


def main():
    repo = MetaRelogioRepository()
    service = MetaRelogioService()
    builder = HtmlBuilder()

    dados = repo.buscar_dados()
    dados_processados = service.processar(dados)
    html = builder.gerar_html(dados_processados)
    caminhos = BackupManager.preparar_caminhos()

    with open(caminhos["html"], "w", encoding="utf-8") as f:
        f.write(html)

    PrintRenderer.gerar_print(
        html_path=caminhos["html"],
        img_path=caminhos["img"],
    )

    print("Processo concluido com sucesso:")
    print(f"HTML: {caminhos['html']}")
    print(f"PRINT: {caminhos['img']}")


    enviar_para_slack(caminhos["img"])
    # Envio provisorio: mantem o envio Slack no codigo, mas usa email nesta execucao.
    #enviar_por_email(caminhos["img"])


if __name__ == "__main__":
    main()
