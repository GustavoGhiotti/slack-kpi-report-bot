from playwright.sync_api import sync_playwright
from pathlib import Path
import time

class SlackSender:

    def __init__(self, url_conversa: str):
        self.url = url_conversa

    def enviar_imagem(self, imagem_path: str, mensagem: str = ""):
        imagem = Path(imagem_path).resolve()

        if not imagem.exists():
            raise FileNotFoundError(f"Imagem não encontrada: {imagem}")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                storage_state="src/infrastructure/slack/slack_session/storage.json"
            )
            page = context.new_page()

            page.goto(self.url, timeout=60000)

            page.wait_for_selector(
                '[contenteditable="true"]',
                timeout=60000
            )

            page.click('[contenteditable="true"]')

            page.set_input_files(
                'input[type="file"]',
                imagem
            )

            time.sleep(2)

            if mensagem:
                page.keyboard.type(mensagem)

            time.sleep(1)

            page.keyboard.press("Enter")

            time.sleep(3)

            context.close()
            browser.close()
