from playwright.sync_api import sync_playwright
import os

SESSION_PATH = "src/infrastructure/slack/slack_session/storage.json"

def salvar_sessao_slack():
    os.makedirs(os.path.dirname(SESSION_PATH), exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False é obrigatório aqui
        context = browser.new_context()
        page = context.new_page()

        print("Abra o Slack e FAÇA LOGIN MANUALMENTE")
        page.goto(os.getenv("SLACK_WORKSPACE_URL", "https://app.slack.com/client/T0000000000"))

        # Aguarda você logar manualmente
        page.wait_for_timeout(240_000)  # 60 segundos (ajuste se quiser)

        # Salva a sessão
        context.storage_state(path=SESSION_PATH)
        print(f"Sessão salva em {SESSION_PATH}")

        browser.close()

if __name__ == "__main__":
    salvar_sessao_slack()
