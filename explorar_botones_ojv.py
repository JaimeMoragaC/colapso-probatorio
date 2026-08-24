from playwright.sync_api import sync_playwright

def explorar_todo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        print("🌐 Navegando a OJV para lectura total de texto...")
        page.goto("https://oficinajudicialvirtual.pjud.cl/", wait_until="domcontentloaded")
        page.wait_for_timeout(6000)
        
        print("--- TEXTO COMPLETO DE LA PÁGINA ---")
        try:
            body_txt = page.locator("body").inner_text()
            print(body_txt[:1500])
        except Exception as e_b:
            print(f"Error leyendo body: {e_b}")
            
        print("\n--- TODOS LOS ENLACES (A) CON HREF O ONCLICK ---")
        links = page.locator("a").all()
        for idx, l in enumerate(links[:40]):
            try:
                txt_l = l.inner_text().strip().replace("\n", " ")
                href_l = l.get_attribute("href") or l.get_attribute("onclick") or ""
                if txt_l or href_l:
                    print(f"  [A-{idx}] TEXT: '{txt_l}' | ATTR: '{href_l}'")
            except Exception:
                pass

        browser.close()

if __name__ == "__main__":
    explorar_todo()
