import os
import time
import re
import pytesseract
from PIL import Image
from playwright.sync_api import sync_playwright

def limpiar_y_leer_captcha(img_path):
    try:
        # Cargar imagen en escala de grises (L)
        img = Image.open(img_path).convert('L')
        
        # Binarización por umbral (Thresholding): resaltamos caracteres oscuros sobre fondo claro
        # Si el valor de brillo es menor a 160 lo dejamos en negro (0), si no en blanco (255)
        img = img.point(lambda p: 0 if p < 160 else 255, '1')
        
        limpio_path = "/home/jaime/Descargas/colapso-probatorio/captcha_limpio.png"
        img.save(limpio_path)
        
        # Ejecutar Tesseract OCR limitando a alfanuméricos (CAPTCHA estándar del PJUD de 6 caracteres)
        custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        texto = pytesseract.image_to_string(img, config=custom_config).strip()
        
        if not texto or len(texto) < 4:
            texto_raw = pytesseract.image_to_string(img, config='--psm 8').strip()
            texto = re.sub(r'[^a-zA-Z0-9]', '', texto_raw)
            
        return texto
    except Exception as e:
        print(f"⚠️ Error procesando imagen OCR en PIL: {e}")
        return ""

def probar_resolucion_optica():
    url = "https://oficinajudicialvirtual.pjud.cl/"
    perfil_dir = "/home/jaime/.config/lexcontrol_chrome_profile"
    os.makedirs(perfil_dir, exist_ok=True)
    
    print("="*75)
    print("🤖 INICIANDO ROBOT CON INTELIGENCIA ÓPTICA (OCR) PARA ROMPER CAPTCHA PJUD")
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
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(3)
        
        # Verificar si hay CAPTCHA visible
        # Buscamos imagen que no sea logo ni ícono pequeño, típicamente la del CAPTCHA
        imgs = page.locator("img").all()
        captcha_img_loc = None
        for img in imgs:
            try:
                box = img.bounding_box()
                if box and box["width"] > 100 and box["height"] > 30 and box["height"] < 150:
                    captcha_img_loc = img
                    break
            except Exception:
                pass
                
        if captcha_img_loc:
            print("🔍 ¡CAPTCHA F5 WAF detectado en pantalla! Tomando fotografía de alta resolución al elemento...")
            img_path = "/home/jaime/Descargas/colapso-probatorio/captcha_raw.png"
            captcha_img_loc.screenshot(path=img_path)
            
            codigo_ocr = limpiar_y_leer_captcha(img_path)
            print(f"🧠 [INTELIGENCIA ÓPTICA] Código descifrado por Tesseract: '{codigo_ocr}'")
            
            if len(codigo_ocr) >= 4:
                # Buscar el input de texto del CAPTCHA
                inputs = page.locator("input[type='text'], input:not([type])").all()
                if len(inputs) > 0:
                    print(f"⚡ Escribiendo código '{codigo_ocr}' en caja de validación...")
                    inputs[0].fill(codigo_ocr)
                    time.sleep(1)
                    
                    # Presionar submit
                    btn_submit = page.locator("button, input[type='submit'], a:has-text('submit')").all()
                    if len(btn_submit) > 0:
                        btn_submit[0].click()
                    else:
                        inputs[0].press("Enter")
                        
                    print("🚀 Botón Submit presionado. Esperando respuesta del servidor WAF...")
                    time.sleep(5)
                    print(f"🌐 Nuevo título de página tras asalto OCR: '{page.title()}'")
                    page.screenshot(path="/home/jaime/Descargas/colapso-probatorio/ojv_post_ocr.png", full_page=True)
                    print("📸 Screenshot post-OCR guardado en ojv_post_ocr.png")
            else:
                print("⚠️ El OCR no pudo descifrar con seguridad los 6 caracteres de la imagen.")
        else:
            print("ℹ️ No se detectó imagen de CAPTCHA. ¡El portal ya te permitió la entrada sin obstáculos!")
            print(f"🌐 Título actual: '{page.title()}'")
            page.screenshot(path="/home/jaime/Descargas/colapso-probatorio/ojv_post_ocr.png", full_page=True)
            
        time.sleep(5)
        context.close()
        print("✅ Prueba de resolución óptica finalizada.")

if __name__ == "__main__":
    probar_resolucion_optica()
