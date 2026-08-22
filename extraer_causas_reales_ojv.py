import os
import time
import json
from playwright.sync_api import sync_playwright

def extraer_causas_en_vivo_pjud():
    url = "https://oficinajudicialvirtual.pjud.cl/"
    perfil_dir = "/home/jaime/.config/lexcontrol_chrome_profile"
    os.makedirs(perfil_dir, exist_ok=True)
    
    print("="*75)
    print("🚀 INICIANDO EXTRACCIÓN REAL DE CAUSAS DESDE EL PORTAL OJV (INTERNET)")
    print("="*75)
    
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=perfil_dir,
            headless=False,
            viewport={"width": 1366, "height": 768},
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        page = context.pages[0] if len(context.pages) > 0 else context.new_page()
        print(f"🌐 Navegando a {url} en tu pantalla visible...")
        page.goto(url, wait_until="domcontentloaded")
        
        print("\n" + "="*75)
        print("🚨 ATENCIÓN JAIME: EL NAVEGADOR ESTÁ ABIERTO EN TU ESCRITORIO.")
        print("👉 1. Si te pide CAPTCHA o clave, ingrésala en la ventana.")
        print("👉 2. Apenas entres, haz clic en tu sección (ej: 'Mis Causas', 'Civil', 'Laboral' o 'Estado Diario').")
        print("👉 3. El robot estará monitoreando tu pantalla durante 60 segundos para extraer las causas y tablas que aparezcan online.")
        print("="*75 + "\n")
        
        causas_encontradas_online = []
        tablas_detectadas = 0
        
        # Bucle inteligente de 60 segundos leyendo la pantalla en vivo
        for segundo in range(60):
            if len(context.pages) == 0 or page.is_closed():
                print("⚡ Ventana cerrada por el usuario. Finalizando lectura web...")
                break
                
            try:
                # Tomar foto cada 15 segundos o cuando detectemos cambio de página
                if segundo % 15 == 0:
                    page.screenshot(path=f"/home/jaime/Descargas/colapso-probatorio/ojv_pantalla_sec_{segundo}.png")
                
                # Buscar tablas de causas en la pantalla actual
                rows = page.locator("table tr, .row, .causa-item, [class*='causa'], [class*='rol']").all()
                if len(rows) > 0 and len(rows) != tablas_detectadas:
                    tablas_detectadas = len(rows)
                    print(f"⚡ [SEGUNDO {segundo}] ¡Detectados {len(rows)} elementos/filas en pantalla! Analizando contenido web...")
                    
                    for r in rows[:30]:
                        try:
                            txt = r.innerText().strip()
                            if txt and len(txt) > 5 and len(txt) < 300:
                                # Si tiene formato de ROL o carátula, lo capturamos
                                if any(kw in txt.lower() for kw in ["rol", "-", "c-", "o-", "t-", "juzgado", "corte", "v/s", "vs", "materia", "estado"]):
                                    if txt not in causas_encontradas_online:
                                        causas_encontradas_online.append(txt)
                                        print(f"   🏛️ [CAUSA ONLINE DETECTADA]: {txt[:100]}...")
                        except Exception:
                            pass
                            
                # También buscar enlaces o botones con nombres de tribunales o roles
                enlaces = page.locator("a, button").all()
                for enl in enlaces[:20]:
                    try:
                        t_enl = enl.innerText().strip()
                        if any(t_enl.startswith(pref) for pref in ["C-", "O-", "T-", "P-", "R-", "Rol ", "ROL "]) or "Juzgado" in t_enl or "Corte" in t_enl:
                            if t_enl not in causas_encontradas_online:
                                causas_encontradas_online.append(t_enl)
                                print(f"   📌 [ENLACE JUDICIAL DETECTADO]: {t_enl}")
                    except Exception:
                        pass
                        
            except Exception as e:
                pass
                
            page.wait_for_timeout(1000)
            
        print("\n" + "="*75)
        print(f"✅ EXTRACCIÓN FINALIZADA. Total de registros judiciales capturados en internet: {len(causas_encontradas_online)}")
        print("="*75)
        
        # Guardar resultado forense de internet
        res_file = "/home/jaime/Descargas/colapso-probatorio/causas_online_detectadas.json"
        with open(res_file, "w", encoding="utf-8") as f:
            json.dump({
                "fecha_extraccion": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_registros_web": len(causas_encontradas_online),
                "datos_capturados_pjud_online": causas_encontradas_online
            }, f, indent=2, ensure_ascii=False)
            
        print(f"💾 Reporte web guardado en: {res_file}")
        try:
            context.close()
        except Exception:
            pass

if __name__ == "__main__":
    extraer_causas_en_vivo_pjud()
