import os
import time
from playwright.sync_api import sync_playwright

def probar_clic_fisico_humano():
    perfil_dir = "/home/jaime/.config/lexcontrol_chrome_profile"
    url = "https://oficinajudicialvirtual.pjud.cl/"
    
    print("🚀 Iniciando navegador visible para prueba de clic físico humano en 'Mi Estado Diario'...")
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=perfil_dir,
            headless=False,
            viewport={"width": 1366, "height": 768},
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled", "--disable-infobars", "--no-first-run"]
        )
        page = context.pages[0] if len(context.pages) > 0 else context.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.navigator.chrome = { runtime: {}, app: {}, csid: {}, loadTimes: () => {} };
        """)
        
        print("🌐 Cargando portada OJV...")
        page.goto(url)
        
        print("==========================================================================")
        print("🚨 JAIME: SI TE PIDE CLAVE, INGRESALA AHORA PARA ENTRAR AL PORTAL.")
        print("⌛ Esperando hasta 60 segundos a ver tu sesión activa (Jaime Moraga C.)...")
        print("==========================================================================")
        
        sesion_lista = False
        for i in range(60):
            txt_body = page.locator("body").inner_text().lower()
            if "jaime moraga" in txt_body or "mi estado diario" in txt_body or "cerrar sesión" in txt_body:
                sesion_lista = True
                print(f"✅ ¡Sesión privada detectada con éxito en segundo {i}!")
                break
            time.sleep(1)
            
        if not sesion_lista:
            print("❌ No se detectó el ingreso en 60 segundos.")
            return

        print("🛑 PAUSA DE 3 SEGUNDOS tras login para estabilizar el portal...")
        page.wait_for_timeout(3000)

        loc_ed = page.locator("text=Mi Estado Diario").first
        if loc_ed.count() == 0:
            loc_ed = page.locator("text=Estado Diario").first
            
        if loc_ed.count() > 0:
            print("🎯 Elemento 'Mi Estado Diario' encontrado en el DOM.")
            # Obtener caja de coordenadas
            box = loc_ed.bounding_box()
            if box:
                target_x = box["x"] + box["width"] / 2
                target_y = box["y"] + box["height"] / 2
                print(f"🖱️ Moviendo ratón gradualmente con trayectoria humana hacia ({target_x:.1f}, {target_y:.1f})...")
                # Movimiento en 25 pasos intermedios (trayectoria humana)
                page.mouse.move(target_x, target_y, steps=25)
                page.wait_for_timeout(400)
                
                print("👇 Ejecutando clic físico con retardo de 160ms (presión natural de mouse)...")
                loc_ed.click(delay=160, timeout=5000)
            else:
                print("⚠️ No se pudo obtener bounding box, haciendo clic con retardo de 160ms...")
                loc_ed.click(delay=160, timeout=5000)
        else:
            print("❌ No se encontró el enlace a Estado Diario.")
            return

        print("⌛ Esperando 5 segundos para ver si el tribunal carga la sección o si lanza el recuadro rojo...")
        page.wait_for_timeout(5000)
        
        foto_res = "/home/jaime/Descargas/colapso-probatorio/prueba_clic_humano_res.png"
        page.screenshot(path=foto_res, full_page=True)
        print(f"📸 Foto posterior al clic guardada en: {foto_res}")
        
        # Verificar si existe recuadro rojo de rechazo
        txt_body_post = page.locator("body").inner_text()
        if "was rejected" in txt_body_post or "support id" in txt_body_post.lower():
            print("❌ FALLO: El recuadro rojo 'The requested URL was rejected' APARECIÓ NUEVAMENTE.")
        else:
            print("🎉 ¡ÉXITO ROTUNDO! No hay recuadro de rechazo. La sección 'Mi Estado Diario' se abrió limpiamente.")
            
        time.sleep(3)

if __name__ == "__main__":
    probar_clic_fisico_humano()
