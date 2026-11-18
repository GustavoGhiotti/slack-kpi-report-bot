from playwright.sync_api import sync_playwright
import os
import math

class PrintRenderer:

    @staticmethod
    def gerar_print(html_path: str, img_path: str):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            context = browser.new_context(
                viewport={"width": 4000, "height": 2000}
            )

            page = context.new_page()
            page.goto(f"file:///{os.path.abspath(html_path)}")

            page.wait_for_timeout(500)

            table = page.locator("#print-area")

            box = table.bounding_box()
            if box:
                largura = math.ceil(box["width"])
                altura = math.ceil(box["height"])

                page.set_viewport_size({
                    "width": largura + 20,
                    "height": altura + 20
                })

                page.wait_for_timeout(200)

            table.screenshot(path=img_path)

            browser.close()
