import os
from playwright.sync_api import sync_playwright

def probar_nav_login():
    url = "https://oficinajudicialvirtual.pjud.cl/"
    perfil_dir = "/home/jaime/.config/lexcontrol_chrome_profile"
    os.makedirs(perfil_dir, exist_ok=True)
    
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=perfil_dir,
            headless=False,
            viewport={"width": 1366, "height": 768},
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        page = context.pages[0] if len(context.pages) > 0 else context.new_page()
        print("🌐 Navegando a portada OJV...")
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        
        print("⚡ Analizando enlaces directos y modales en la portada...")
        enlaces = page.locator("a, button, [onclick], [class*='btn']").all()
        for i, enl in enumerate(enlaces[:50]):
            try:
                txt = enl.innerText().strip().replace("\n", " ")
                href = enl.get_attribute("href") or enl.get_attribute("onclick") or ""
                if any(k in txt.lower() or k in href.lower() for k in ["clave", "pjud", "servicio", "causa", "login", "ingreso", "modal", "tab"]):
                    print(f"  [{i}] TEXTO: '{txt}' | RUTA/ACCION: '{href}'")
            except Exception:
                pass
                
        page.wait_for_timeout(2000)
        out_png = "/home/jaime/Descargas/colapso-probatorio/ojv_step2_login.png"
        page.screenshot(path=out_png)
        print(f"📸 Foto guardada tras el clic: {out_png}")
        print(f"🌐 Título actual: '{page.title()}' | URL actual: {page.url}")
        context.close()

if __name__ == "__main__":
    probar_nav_login()
