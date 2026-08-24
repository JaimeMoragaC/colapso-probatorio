from playwright.sync_api import sync_playwright

def inspeccionar_portada():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("🌐 Navegando a OJV para inspeccionar botón Todos los servicios...")
        page.goto("https://oficinajudicialvirtual.pjud.cl/", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        
        print("⚡ Buscando todos los elementos que contengan la palabra 'servicios' o 'clave'...")
        els = page.locator("*:has-text('servicios'), *:has-text('Clave'), *:has-text('Consulta')").all()
        for i, el in enumerate(els[:30]):
            try:
                tag = el.evaluate("node => node.tagName")
                cls = el.get_attribute("class") or ""
                id_val = el.get_attribute("id") or ""
                txt = el.innerText().strip().replace("\n", " ")[:60]
                if len(txt) < 50 and ("servicios" in txt.lower() or "clave" in txt.lower() or "consulta" in txt.lower()):
                    print(f"  [{i}] TAG: <{tag}> | ID: '{id_val}' | CLASS: '{cls}' | TEXTO: '{txt}'")
            except Exception:
                pass
                
        browser.close()

if __name__ == "__main__":
    inspeccionar_portada()
