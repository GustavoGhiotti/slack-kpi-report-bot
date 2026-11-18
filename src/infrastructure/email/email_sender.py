import os
import smtplib
from datetime import datetime
from email.message import EmailMessage

from src.shared.utils.env_load import (
    EMAIL_PASSWORD,
    EMAIL_SMTP_HOST,
    EMAIL_SMTP_PORT,
    EMAIL_USER,
)


class EmailSender:
    @staticmethod
    def enviar_meta_relogio(img_path: str) -> None:
        remetente = EMAIL_USER
        senha = EMAIL_PASSWORD
        destinatarios = [
            "desenvolvimento@empresa.example",
            "planejamento@empresa.example",
            "colaborador10@empresa.example",
            "colaborador11@empresa.example"
            ]

        extra_destinatarios = os.getenv("EMAIL_DESTINATARIOS")
        if extra_destinatarios:
            destinatarios = [
                email.strip()
                for email in extra_destinatarios.split(",")
                if email.strip()
            ]

        if not remetente or not senha:
            print("EMAIL_USER e EMAIL_PASSWORD nao configurados.")
            return

        if not destinatarios:
            print("EMAIL_DESTINATARIOS nao configurado.")
            return

        hora = datetime.now().strftime("%H")

        msg = EmailMessage()
        msg["Subject"] = f"PARCIAL META RELOGIO - {hora}H"
        msg["From"] = remetente
        msg["To"] = ", ".join(destinatarios)
        msg.set_content("")

        try:
            with open(img_path, "rb") as arquivo_imagem:
                msg.add_attachment(
                    arquivo_imagem.read(),
                    maintype="image",
                    subtype="png",
                    filename=os.path.basename(img_path),
                )
        except Exception as exc:
            print(f"Erro ao anexar print do HTML: {exc}")
            return

        try:
            with smtplib.SMTP_SSL(EMAIL_SMTP_HOST, EMAIL_SMTP_PORT) as smtp:
                smtp.login(remetente, senha)
                smtp.send_message(msg)
            print("Email enviado com sucesso.")
        except Exception as exc:
            print(f"Erro ao enviar e-mail: {exc}")
