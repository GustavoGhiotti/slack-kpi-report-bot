import os
from datetime import datetime


class BackupManager:

    @staticmethod
    def preparar_caminhos():
        data = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H")

        pasta = f"backups/{data}"
        os.makedirs(pasta, exist_ok=True)

        return {
            "html": f"{pasta}/meta_relogio_{hora}.html",
            "img": f"{pasta}/meta_relogio_{hora}.png"
        }