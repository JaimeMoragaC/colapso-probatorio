import sys

file_path = "PAPER_v3_trabajo.md"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target = """#### El *Zero-Day* Procesal: La aniquilación de la prueba electrónica ante la sana crítica

La consecuencia jurídica es terminal y opera en dos planos. En la *admisibilidad*, bajo la *Federal Rule of Evidence* 901(b)(9) sistematizada en *Lorraine v. Markel*<a href="#fn122" id="fnref122b"><sup>122</sup></a>, el oferente debe acreditar que el sistema «produce un resultado preciso» —y la conservación acredita persistencia, no precisión—. En la *valoración*, el ordenamiento chileno es aquí *más* severo que el *common law*: a diferencia del Reino Unido, que recién deroga su presunción de buen funcionamiento del computador tras el desastre Horizon<a href="#fn106" id="fnref106c"><sup>106</sup></a>, el proceso penal chileno *nunca consagró tal presunción*; rige la sana crítica (Arts. 295-297 CPP), bajo la cual el juez no *presume* la fiabilidad de la máquina: la *exige*. Un registro conservado por orden del Art. 218 bis, pero inatestado en su origen, llega a esa valoración con la cadena de custodia ya rota en T₀ —y ninguna diligencia posterior a T₁ reconstruye una propiedad que la irreversibilidad del proceso destruyó—.

El rechazo de la evidencia inatestada bajo las reglas de la sana crítica genera una **paradoja probatoria**. El litigante tradicional, formado en la dogmática penal clásica, podría leer esta exclusión y concluir: *«Excelente. Si los logs cloud son inadmisibles o el atacante los purgó, el Ministerio Público se queda sin pruebas. Y si no hay pruebas de cargo, opera la presunción de inocencia (in dubio pro reo) y mi cliente queda absuelto»*. 

Esa defensa es hoy una sentencia de cárcel. El "Zero-Day Procesal" no es un salvavidas para la corporación, es una trampa mortal de **inversión fáctica de la carga probatoria**. 

Bajo la Ley 21.595, si el Agente de IA de la empresa comete el delito (ej. desvía fondos, manipula precios o filtra datos), el daño material es evidente y la acción de la máquina es innegable. Para salvarse de la condena penal, el directorio necesita probar una **eximente**: que el sistema fue secuestrado por un tercero (un hacker) en Ring 0. Es exactamente aquí donde la rigurosidad de la sana crítica los condena a muerte. Al carecer de atestación de *hardware*, la empresa no tiene cómo probar de forma fidedigna su coartada tecnológica ante un juez que le exige certidumbre científica (Art. 297 CPP). El fiscal no necesita el *log* para probar que la IA de la empresa causó el daño; la empresa necesita el *log* inmutable para probar que fue hackeada. Al no tener evidencia admisible para su defensa, el directorio asume la responsabilidad penal total por omisión inexcusable.

En otras palabras, el Art. 218 bis no es una herramienta de persecución infalible; es una *vulnerabilidad de Día Cero (Zero-Day) procesal* que codifica la indefensión de la corporación. El legislador chileno programó un `assert(proveedor == honesto)` en el núcleo del Código Procesal Penal. El atacante polimórfico simplemente hace un *bypass* de esa aserción, destruye la coartada y deja al gerente legal frente al juez sin evidencia material válida ante la sana crítica.

Ante este colapso inminente, el litigante tradicional intentará instintivamente refugiarse en la Ley 19.799 sobre Documentos Electrónicos, argumentando que si el proveedor firmó digitalmente el registro, la evidencia goza de presunción legal de integridad. Como ya se demostró exhaustivamente (véase *supra*, § «El secuestro de la Ley 19.799»), esta defensa es técnicamente falaz: el ataque polimórfico en *Ring-0* altera el dato en la memoria *antes* de la subrutina de cifrado, logrando que el propio sistema estampe una firma matemáticamente perfecta sobre un evento ideológicamente falso. Con ello, se invalida de paso la exigencia taxativa del Art. 2, letra d) de la ley: que quien firma debe mantener el dominio y «exclusivo control» de los medios de creación, una ficción contractual insostenible cuando el hipervisor pertenece y es administrado por un hiperescalar extranjero.

*El colapso dogmático se vuelve empírico al bajar al código.* Para visualizar la magnitud de esta asimetría —y comprender exactamente dónde se derrumbarán las imputaciones del Ministerio Público y las multas de la CMF ante un tribunal preparado—, basta observar la anatomía de la evidencia. Comparemos el registro de texto plano que la ley hoy presume válido, frente a la irrefutabilidad criptográfica que la verdadera ingeniería forense exige para condenar:"""

replacement = """#### El *Zero-Day* Procesal: La bilateralidad del colapso probatorio ante la sana crítica

La consecuencia jurídica de la arquitectura opaca es terminal y opera como un "Zero-Day Procesal" que aniquila la utilidad de la evidencia electrónica en dos frentes simultáneos: destruye la capacidad del Estado (CMF/Ministerio Público) para sancionar, y la capacidad del directorio corporativo para defenderse.

##### 1. El colapso de la acusación: Admisibilidad y Valoración
En la *admisibilidad*, bajo la *Federal Rule of Evidence* 901(b)(9) sistematizada en *Lorraine v. Markel*<a href="#fn122" id="fnref122b"><sup>122</sup></a>, el oferente (sea el fiscal o el regulador) debe acreditar que el sistema «produce un resultado preciso» —y la mera orden de conservación del Art. 218 bis acredita persistencia, no precisión—. En la *valoración*, el ordenamiento chileno es aquí *más* severo que el *common law*: a diferencia del Reino Unido, que recién deroga su presunción de buen funcionamiento del computador tras el desastre Horizon<a href="#fn106" id="fnref106c"><sup>106</sup></a>, el proceso penal chileno *nunca consagró tal presunción*; rige la sana crítica (Arts. 295-297 CPP), bajo la cual el juez no *presume* la fiabilidad de la máquina: la *exige*. Un registro *cloud* conservado, pero inatestado en su origen, llega a esa valoración con la cadena de custodia rota en T₀ —y ninguna diligencia posterior reconstruye una propiedad que la irreversibilidad del proceso destruyó—.

##### 2. El colapso de la defensa: La paradoja probatoria bajo Ley 21.595
El rechazo de la evidencia inatestada bajo las reglas de la sana crítica genera una **paradoja probatoria**. El litigante tradicional, formado en la dogmática penal clásica, podría leer esta exclusión y concluir: *«Excelente. Si los logs cloud son inadmisibles o el atacante los purgó, el Ministerio Público se queda sin pruebas. Y si no hay pruebas de cargo, opera la presunción de inocencia (in dubio pro reo) y mi cliente queda absuelto»*. 

Esa defensa es hoy una sentencia de cárcel. El "Zero-Day Procesal" no es un salvavidas para la corporación, es una trampa mortal de **inversión fáctica de la carga probatoria**. 

Bajo la Ley 21.595, si el Agente de IA de la empresa comete el delito (ej. desvía fondos, manipula precios o filtra datos), el daño material es evidente y la acción de la máquina es innegable. Para salvarse de la condena penal, el directorio necesita probar una **eximente**: que el sistema fue secuestrado por un tercero (un hacker) en Ring 0. Es exactamente aquí donde la rigurosidad de la sana crítica los condena a muerte. Al carecer de atestación de *hardware*, la empresa no tiene cómo probar de forma fidedigna su coartada tecnológica ante un juez que le exige certidumbre científica (Art. 297 CPP). El fiscal no necesita el *log* para probar que la IA de la empresa causó el daño; la empresa necesita el *log* inmutable para probar que fue hackeada. Al no tener evidencia admisible para su defensa, el directorio asume la responsabilidad penal total por omisión inexcusable.

En otras palabras, el Art. 218 bis no es una herramienta de persecución infalible; es una vulnerabilidad que codifica la indefensión de la corporación. El legislador chileno programó un `assert(proveedor == honesto)` en el núcleo del Código Procesal Penal. El atacante polimórfico simplemente hace un *bypass* de esa aserción, destruye la coartada y deja al gerente legal frente al juez sin evidencia material válida ante la sana crítica.

##### 3. El colapso documental: El secuestro de la Ley 19.799
Ante este colapso inminente, el litigante tradicional intentará instintivamente refugiarse en la Ley 19.799 sobre Documentos Electrónicos, argumentando que si el proveedor firmó digitalmente el registro, la evidencia goza de presunción legal de integridad. Como ya se demostró exhaustivamente (véase *supra*, § «El secuestro de la Ley 19.799»), esta defensa es técnicamente falaz: el ataque polimórfico en *Ring-0* altera el dato en la memoria *antes* de la subrutina de cifrado, logrando que el propio sistema estampe una firma matemáticamente perfecta sobre un evento ideológicamente falso. Con ello, se invalida de paso la exigencia taxativa del Art. 2, letra d) de la ley: que quien firma debe mantener el dominio y «exclusivo control» de los medios de creación, una ficción contractual insostenible cuando el hipervisor pertenece y es administrado por un hiperescalar extranjero.

##### 4. Anatomía del empate empírico: Evidencia Cloud vs. Evidencia Soberana
*El colapso dogmático se vuelve empírico al bajar al código.* Para visualizar la magnitud de esta asimetría —y comprender exactamente dónde se derrumbarán tanto las imputaciones de la CMF como las defensas corporativas ante un tribunal preparado—, basta observar la anatomía de la evidencia. Comparemos el registro de texto plano que la ley hoy presume válido, frente a la irrefutabilidad criptográfica que la verdadera ingeniería forense exige para litigar:"""

if target in content:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.replace(target, replacement))
    print("SUCCESS")
else:
    print("FAILED TO FIND TARGET")
