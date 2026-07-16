import sys

def main():
    path = "/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Ley de Anderson y Enriquecimiento sin causa
    target1 = """el dueño de la infraestructura, no la víctima, soporta el riesgo del entorno que controla.

Conviene precisar el alcance de la analogía para no excederla"""

    replacement1 = """el dueño de la infraestructura, no la víctima, soporta el riesgo del entorno que controla.

Esta jurisprudencia es, en el fondo, una reproducción de manual de la Ley de Anderson. El máximo tribunal ha comprendido económicamente que la opacidad técnica es rentable para quien opera la infraestructura a escala masiva, traduciendo el problema tecnológico a un principio que la judicatura penal y civil sanciona con severidad: **el enriquecimiento sin justa causa y la externalización de costos**. 

La premisa subyacente es que la corporación no opta por una infraestructura *cloud* inatestable porque sea más segura, sino porque es financieramente más eficiente operar a ciegas y transferirle el riesgo forense al usuario asimétrico o al Estado. Prohibir esta externalización destruye la narrativa de la empresa como "víctima" de un ciberataque y la reposiciona como un agente negligente guiado por el lucro: es la entidad operadora —quien diseña, lucra y controla el ecosistema cerrado— quien debe asumir el costo de sus vulnerabilidades. 

En sede penal (Ley 21.595) y sancionatoria (Ley 21.663), esta lógica es letal. Acreditar que el directorio consintió una arquitectura ciego-probatoria para maximizar márgenes operativos, renunciando a la atestación física que el estado del arte permitía, constituye dinamita pura para configurar negligencia inexcusable o, derechamente, dolo eventual ante un escenario de colapso de datos.

El paralelo no es retórico sino empíricamente demostrado. En su estudio fundacional *"Why Information Security is Hard — An Economic Perspective"* (2001), Ross Anderson, de la Universidad de Cambridge, documentó que la seguridad de los cajeros automáticos y sistemas de pago electrónico divergía radicalmente según a quién le asignara la ley la carga de la prueba en las transacciones disputadas. 

En Estados Unidos, donde la regulación federal (*Regulation E*) obligaba al banco a probar que la transacción fue autorizada, las entidades financieras invirtieron masivamente en seguridad robusta porque absorbían el costo del fraude. 

En el Reino Unido, donde la carga recaía sobre el cliente y los bancos podían invocar la infalibilidad de sus sistemas para negar los reclamos por "retiros fantasma" (*phantom withdrawals*), la inversión en seguridad se estancó y se produjo una epidemia de fraude bancario que solo se corrigió cuando los costos se volvieron insostenibles. 

Anderson demostró que la variable determinante no era la sofisticación tecnológica sino la asignación legal de la responsabilidad: cuando el operador de la infraestructura asume el riesgo, invierte en seguridad real; cuando puede externalizarlo hacia el usuario asimétrico, la opacidad se convierte en modelo de negocio.

La Corte Suprema chilena, al aplicar la Ley 20.009 reformada, ha elegido explícitamente el modelo estadounidense que Anderson identificó como el único que genera incentivos reales de seguridad: el operador de la infraestructura es garante, no la víctima.

Conviene precisar el alcance de la analogía para no excederla"""

    if target1 in content:
        content = content.replace(target1, replacement1)
        print("Replaced Ley de Anderson.")
    else:
        print("Ley de Anderson target not found.")

    # 2. Fantasma de facto en Sana Crítica
    # Wait, the user had:
    # En Chile rige la libre valoración conforme a la sana crítica (Arts. 295 a 297 del Código Procesal Penal), que obliga al tribunal a ponderar la prueba según la lógica, las máximas de la experiencia y los conocimientos científicamente afianzados.
    # But in the file it is "### Traducción a la sana crítica chilena."
    # Let's search for "conocimientos científicamente afianzados"
    
    target2 = """En Chile rige la libre valoración conforme a la **sana crítica** (Arts. 295 a 297 del Código Procesal Penal), que obliga al tribunal a ponderar la prueba según la lógica, las máximas de la experiencia y los conocimientos científicamente afianzados.

De ello se desprenden consecuencias letales"""

    replacement2 = """En Chile rige la libre valoración conforme a la **sana crítica** (Arts. 295 a 297 del Código Procesal Penal), que obliga al tribunal a ponderar la prueba según la lógica, las máximas de la experiencia y los conocimientos científicamente afianzados.

Sin embargo, en la praxis judicial suele rondar un peligroso *fantasma de facto*: la inercia cognitiva de asumir que la máquina "no se equivoca". Como se examinó previamente frente a la presunción de regularidad (*omnia praesumuntur rite esse acta*), esta falsa confianza fue concebida para instrumentos mecánicos simples —como relojes, básculas o péndulos— cuyo error es netamente estocástico y físicamente peritable. El sesgo del juzgador consiste en evaluar un ecosistema *cloud* complejo con la misma lógica determinista que aplicaría a la medición de un péndulo, ignorando que la red está habitada por adversarios racionales capaces de alterar activamente la telemetría sin descalibrar el sustrato físico de la máquina.

De ello se desprenden consecuencias letales"""

    if target2 in content:
        content = content.replace(target2, replacement2)
        print("Replaced Fantasma de facto.")
    else:
        print("Fantasma de facto target not found.")

    # 3. Expediente Reservado & CMF
    target3 = """> *Expediente reservado del procedimiento sancionador.* La Delegada de Protección de Datos cumplió cada casilla en sus descargos escritos: ISO 27001 vigente, SOC 2 Type II, contrato con cláusula de auditoría, proveedor certificado. Todo se tramita a puertas cerradas, sin audiencias públicas ni escrutinio transparente sobre cómo el regulador adopta su decisión. En la resolución final, la autoridad asesta un solo golpe: «¿Puede la entidad acreditar, con evidencia independiente del proveedor, que el registro aportado no fue alterado o fabricado por el atacante?». No puede. El expediente se cierra en la opacidad administrativa. Los certificados prueban que la entidad contrató con diligencia documental; no prueban qué ocurrió realmente en la infraestructura. Y el deber de responsabilidad proactiva (*accountability*) no era contratar bien: era poder demostrar de forma irrefutable el estado del sistema ante un regulador que falla en la sombra.

El campo de batalla real del responsable de datos no es, en la mayoría de los casos, el penal, sino el procedimiento administrativo sancionador ante la ANCI (Ley 21.663) y la Agencia de Protección de Datos (Ley 21.719). Y allí la carga probatoria no opera como un refugio garantista ni como una condena automática, sino como un cepo : una tenaza de dos deberes legales cuya única salida compatible con la diligencia es la evidencia atestable."""

    replacement3 = """El campo de batalla real del responsable de datos no es, en la mayoría de los casos, el penal, sino el procedimiento administrativo sancionador ante la ANCI (Ley 21.663), la Agencia de Protección de Datos (Ley 21.719) y la CMF (Normativa de Ciberseguridad y NCG 502). Y allí la carga probatoria no opera como un refugio garantista ni como una condena automática, sino como un cepo: una tenaza de dos deberes legales cuya única salida compatible con la diligencia es la evidencia atestable."""

    if target3 in content:
        content = content.replace(target3, replacement3)
        print("Replaced Expediente Reservado and added CMF.")
    else:
        print("Expediente Reservado target not found.")

    # 4. European Upgrade (GDPR and NIS2)
    # The current text might not have "El Espejo Regulatorio Europeo" at all! Because the user added it!
    # Let's check if the European block is present.
    # We will write the new content back to the file.
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    
if __name__ == "__main__":
    main()
