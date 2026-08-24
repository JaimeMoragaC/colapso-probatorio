import os
import time
from playwright.sync_api import sync_playwright

def explorar_y_extraer_pjud():
    url = "https://oficinajudicialvirtual.pjud.cl/"
    perfil_dir = "/home/jaime/.config/lexcontrol_chrome_profile"
    os.makedirs(perfil_dir, exist_ok=True)
    
    print("="*75)
    print("🚀 INICIANDO EXPLORACIÓN REAL EN VIVO DEL PODER JUDICIAL (PJUD.CL)")
    print("="*75)
    
    with sync_playwright() as p:
        # Lanzamos en modo VISIBLE y con camuflaje STEALTH para burlar el WAF F5 Big-IP
        context = p.chromium.launch_persistent_context(
            user_data_dir=perfil_dir,
            headless=False,
            viewport={"width": 1366, "height": 768},
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars"
            ]
        )
        
        # Inyección Stealth anti-detección de robot
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        page = context.pages[0] if len(context.pages) > 0 else context.new_page()
        print(f"🌐 Navegando a {url} con perfil humano validado...")
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(4)
        
        titulo = page.title()
        print(f"📌 Título de la página detectado: '{titulo}'")
        page.screenshot(path="/home/jaime/Descargas/colapso-probatorio/ojv_real_step1.png", full_page=True)
        print("📸 Screenshot guardado en ojv_real_step1.png")
        
        # Buscar botones de login, Mis Causas o Estado Diario
        botones = page.locator("button, a, input[type='submit']").all()
        print(f"🔍 Elementos interactivos encontrados en la página principal: {len(botones)}")
        for idx, btn in enumerate(botones[:20]):
            try:
                txt = btn.innerText().strip()
                if txt and len(txt) < 50:
                    print(f"   [Elemento {idx+1}] Texto: '{txt}' | Tag: {btn.evaluate('node => node.tagName')}")
            except Exception:
                pass

        # Verificar si hay tablas o iframes de causas
        tablas = page.locator("table").all()
        print(f"📊 Tablas detectadas en DOM actual: {len(tablas)}")
        
        print("\n⏳ Esperando 10 segundos para permitir inspección visual en tu pantalla...")
        time.sleep(10)
        
        context.close()
        print("✅ Exploración completada.")

if __name__ == "__main__":
    explorar_y_extraer_pjud()
