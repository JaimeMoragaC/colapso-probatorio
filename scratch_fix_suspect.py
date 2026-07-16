with open("PAPER_v3_trabajo.md", "r") as f:
    content = f.read()

target = """Esa brecha empírica (3 segundos vs. 72 horas) no es una ventana de oportunidad forense: es un abismo que aniquila la utilidad de la norma. La preservación provisoria no congela el estado del sistema en el momento del hecho: congela el estado que el adversario *eligió dejar tras de sí*, y le confiere, además, rango de prueba conservada por orden judicial.

La orden de conservación es una *read primitive* dirigida al nodo no confiable. Pedirle al proveedor que «preserve» el estado es ejecutar una lectura sobre la memoria del mismo estrato que pudo estar comprometido —exactamente la *subversión de primitivas de lectura* que Garfinkel y Rosenblum formalizaron para la introspección de máquinas virtuales<a href="#fn141" id="fnref141b"><sup>141</sup></a>, y el límite que Thompson demostró para todo verificador que opera *desde dentro* de la frontera de confianza que audita<a href="#fn140" id="fnref140c"><sup>140</sup></a>—. La conservación posterior no cierra el *semantic gap*: lo notariza.

Al ordenar la conservación, el Ministerio Público se convierte en un *diputado confundido* (confused deputy). En la teoría de la seguridad, el *confused deputy* es la entidad que ejerce una autoridad legítima cuya ejecución material delega en quien no merece confianza<a href="#fn173" id="fnref173"><sup>173</sup></a>. 

La orden del Art. 218 bis es impecable en su forma —emana de la potestad persecutoria— pero su ejecución material recae en el proveedor: el único actor cuya honestidad la causa pone en duda. El fiscal cree estar asegurando la prueba; en realidad le pide al sospechoso que custodie su propia coartada. 

Es el Problema de los Generales Bizantinos<a href="#fn171" id="fnref171b"><sup>171</sup></a> trasladado del *log* a la sala de audiencias: un sistema que depende de un nodo central capaz de mentir de forma arbitraria no alcanza un estado confiable por el solo hecho de ordenarle que conserve su versión."""

replacement = """Esa brecha empírica (3 segundos vs. 72 horas) no es una ventana de oportunidad forense: es un abismo que aniquila la utilidad de la norma. La preservación provisoria no congela el estado del sistema en el momento del hecho: congela el estado que el adversario *eligió dejar tras de sí*, y le confiere, además —lo que es procesalmente más grave—, rango de prueba conservada por orden judicial.

La orden de conservación es una *read primitive* dirigida al nodo no confiable. Pedirle al proveedor que «preserve» el estado es ejecutar una lectura sobre la memoria del mismo estrato que pudo estar comprometido —exactamente la *subversión de primitivas de lectura* que Garfinkel y Rosenblum formalizaron para la introspección de máquinas virtuales<a href="#fn141" id="fnref141b"><sup>141</sup></a>, y el límite que Thompson demostró para todo verificador que opera *desde dentro* de la frontera de confianza que audita<a href="#fn140" id="fnref140c"><sup>140</sup></a>—. La conservación posterior no cierra el *semantic gap*: lo notariza.

Al ordenar la conservación, el Ministerio Público se convierte en un *diputado confundido* (confused deputy). En la teoría de la seguridad, el *confused deputy* es la entidad que ejerce una autoridad legítima cuya ejecución material delega en quien no merece confianza<a href="#fn173" id="fnref173"><sup>173</sup></a>. 

La orden del Art. 218 bis es impecable en su forma —emana de la potestad persecutoria— pero su ejecución material recae en el hiperescalador: una entidad que, al operar una caja negra y negarse a proveer atestación de *hardware* sobre su hipervisor, se convierte forensemente en el principal sospechoso de opacidad. El fiscal cree estar asegurando la prueba mediante un tercero neutral; en realidad, le pide a un custodio inatestable que certifique su propia coartada. 

Es el Problema de los Generales Bizantinos<a href="#fn171" id="fnref171b"><sup>171</sup></a> trasladado del *log* a la sala de audiencias: un sistema que depende de un nodo central capaz de mentir de forma arbitraria —o de ocultar su propia vulneración en Ring 0— no alcanza un estado confiable por el solo hecho de que un juez le ordene conservar su versión."""

if target in content:
    with open("PAPER_v3_trabajo.md", "w") as f:
        f.write(content.replace(target, replacement))
    print("Success")
else:
    print("Failed to find target")
