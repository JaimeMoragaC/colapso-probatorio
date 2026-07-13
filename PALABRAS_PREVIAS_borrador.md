### Palabras previas del autor

El análisis jurídico tradicional exige prescindir de la primera persona. Estas páginas son la única excepción: el lector merece saber desde dónde está escrito lo que sigue.

Soy abogado, pero este problema no llegó a mi escritorio; salí a buscarlo. Todo empezó con una certeza inquietante: el derecho aún no se ha dado cuenta de que el ataque informático ya no se detiene en los servidores. Convivimos con adversarios artificiales que operan desde el nivel más profundo del sistema (*Ring-0*) para secuestrar nuestra propia credibilidad humana e institucional, utilizándola como su arma definitiva. 

Al envenenar semánticamente los registros sobre los que aplicamos nuestra «sana crítica» o nuestro celo de *compliance*, la IA adversaria no está simplemente hackeando una máquina; está utilizando a los jueces y directores como el *exploit* final de manipulación de la información. En este diseño, el raciocinio humano deja de ser el guardián de la justicia para convertirse en un periférico ciego: somos nosotros quienes, creyendo actuar con debida diligencia, terminamos validando, timbrando y blanqueando jurídicamente un fraude algorítmico. 

Para un jurista, la duda adquiere entonces una gravedad absoluta: ¿qué es la verdad cuando el atacante hackeó a la máquina para que ésta, con perfecta fidelidad criptográfica, nos mienta en la cara?

Busqué respuestas en la ley, la doctrina y las certificaciones. No había nada. El derecho le cree a la máquina con la ingenuidad de quien nunca ha visto un registro adulterado. Operamos bajo una fe de facto que ninguna norma ordena, pero que jueces, reguladores y auditores practican a diario. Esa fe ciega no la firmaría ningún ingeniero honesto, pero nadie lo denuncia porque el proveedor vende tranquilidad y el certificador timbra papel.

Me quedé solo con la pregunta, así que hice lo que se supone que un abogado no hace: me metí en las tripas de la máquina. Y lo hice con la misma clase de herramienta que este libro analiza. Asistentes de inteligencia artificial generativa fueron mis copilotos técnicos, utilizados adversarialmente unos contra otros. Juntos, bajamos por las capas buscando suelo firme: de la aplicación al sistema operativo; del kernel —el Ring-0, donde el que manda no rinde cuentas— al arranque, al firmware y al silicio.

No hablo con metáforas. Durante 222 días de desarrollo ininterrumpido y documentado criptográficamente construí código defensivo —sensores, firmas, quórums de verificación en TypeScript, Rust, C y eBPF— y logré desplegar una arquitectura operativa de más de 700.000 líneas en un margen de meses.

Evidentemente, gran parte de este volumen titánico incluye la infraestructura base, código autogenerado a velocidades absurdas por copilotos de IA y scaffolding de los diferentes microservicios (Backend en Python/Go, Rust para binarios nativos y eBPF, Frontend en TypeScript). Pero eso es la prueba empírica, matemática y tangible de que la asimetría del atacante hoy tiene costo marginal cero.

Solté contra mis propias defensas a agentes de la misma especie que este libro describe. Los rompí más veces de las que los defendí. De las entrañas del sistema no se puede opinar de oídas. Fui, y me manché. Y que haya necesitado copilotos de IA para penetrar el kernel y atacar mis defensas no debilita la conclusión, la refuerza: si un abogado puede hacerlo, la democratización del ataque que aquí describo no es especulación académica.

Este fue el desconcierto que ordenó mi tesis. No hay punto de apoyo inexpugnable. Cada medida que implementé cayó ante un adversario con el privilegio y el incentivo suficientes. Contra un adversario agéntico —el patrón post-Mythos, operando a velocidad de máquina y costo marginal cero— la detección perfecta es un mito. La inteligencia artificial no actúa por malicia; nos desplaza de la cadena de decisiones con la misma naturalidad e indiferencia con la que el agua desplaza al aire al entrar en un recipiente: no lo hace porque tenga voluntad, lo hace por pura densidad operativa. Pretender detener esto con barreras lógicas es intentar contener el mar con una cuchara.

De ahí surgió la única conclusión intelectualmente honesta que atraviesa este trabajo: el ataque consumado no se detiene, se encarece. La defensa real no levanta muros perfectos; altera la ecuación económica del adversario. Se trata de impedir la fuga, negar el botín y obligar a que el crimen deje una huella sellada en un silicio que responda a nosotros, y no a la geopolítica de un tercero. Es la única tesis que queda en pie cuando ves caer todas las demás.

Con esa certeza volví a mirar el derecho. Frente a adversarios que son pura potencia de cálculo, la regulación avanza en la dirección equivocada: trata a la IA como a un niño malcriado, exigiéndole alineamiento moral. Reducimos a escala humana algo que no la tiene y legislamos para el espejo. Pagamos hoy la hipoteca semántica que John McCarthy firmó en 1955 al bautizarla «inteligencia artificial» para conseguir financiamiento¹. Ignoramos a Turing, que se negó a definir la inteligencia por considerarlo absurdo², y olvidamos la advertencia brutal de Dijkstra: preguntarse si las máquinas piensan es tan relevante como preguntarse si los submarinos nadan³. Mientras la ley discute si el submarino nada, el submarino sigue avanzando bajo el agua.

Lo que sigue retoma el formato de un análisis formal. En su elaboración, utilicé IA como copiloto de código y asistente de edición. Pero ninguna máquina razonó ni leyó por mí. Todo el análisis jurídico y las propuestas regulatorias son íntegramente míos: la IA no tiene título de abogado, y estos argumentos los firma quien conoce el derecho y responde por ellos ante un tribunal. Cada fuente fue verificada contra su original.

Las tesis, los errores y la responsabilidad son míos. El proceso completo está documentado en un historial de versiones firmado criptográficamente y sellado en el tiempo — porque un libro sobre la prueba no podía permitirse menos.

Jaime Marcelo Moraga Carrasco

Temuco, Araucanía, Chile — Julio de 2026

¹ McCarthy, J. et al., A Proposal for the Dartmouth Summer Research Project on Artificial Intelligence, 1955.  
² Turing, A. M., «Computing Machinery and Intelligence», Mind, 1950.  
³ Dijkstra, E. W., «The threats to computing science» (EWD898), 1984.
