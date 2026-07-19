import re
import os

filepath = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace inline tags with pandoc tags
text = text.replace('<sup>1</sup> *Bates v', '[^301] *Bates v') # just in case
# Actually the inline links are already [^301] because my previous script DID replace the inline ones!
# Wait, let me check the inline ones:
# The previous script replaced '<a href="#fn301" id="fnref301"><sup>301</sup></a>' with '[^301]'
# BUT wait! Earlier I said the previous script failed to replace the FOOTER, but did it replace the INLINE ones?
# Let's just use regex for the whole footer replacement.

pattern = re.compile(r'\*Fuentes y Verificabilidad Jurisprudencial:\*.*?(?=## Profundizaciones en la frontera)', re.DOTALL)

new_footer = """*Fuentes y Verificabilidad Jurisprudencial (Anexo del Capítulo 8):*

[^301]: [*Bates v Post Office Ltd* [2019] EWHC 3408 (QB)](https://www.bailii.org/ew/cases/EWHC/QB/2019/3408.html). Sentencia histórica de la High Court of Justice del Reino Unido sobre la falibilidad de los logs del sistema Horizon.
[^302]: [*Arsenal Consulting Reports on Bhima Koregaon* (Reportes I, II y III, 2021)](https://arsenalrecon.com/resources). Peritaje forense que demostró la inyección remota (NetWire RAT) y la alteración del MFT en los terminales de activistas indios.
[^303]: [Sentencia del Tribunal Supremo de España, Sala de lo Penal: STS 300/2015](https://www.poderjudicial.es/search/AN/openDocument/9008bc5d29037abf/20150529), de 19 de mayo de 2015 (Ponente: Manuel Marchena).
[^304]: [Sentencia del Tribunal Constitucional Federal de Alemania sobre el derecho fundamental a la confidencialidad e integridad de los sistemas TI (BVerfG, 1 BvR 370/07)](https://www.bundesverfassungsgericht.de/SharedDocs/Entscheidungen/EN/2008/02/rs20080227_1bvr037007en.html).
[^305]: [*State v. Loomis*, Corte Suprema de Wisconsin (2016)](https://casetext.com/case/state-v-loomis-3). Validó el uso del algoritmo propietario de caja negra COMPAS para sentencias penales.
[^306]: [Kahneman, D., Sibony, O., & Sunstein, C. R. (2021). *Noise: A Flaw in Human Judgment*](https://en.wikipedia.org/wiki/Noise:_A_Flaw_in_Human_Judgment).
[^307]: [Goodfellow, I. J., Shlens, J., & Szegedy, C. (2014). *Explaining and Harnessing Adversarial Examples* (arXiv:1412.6572)](https://arxiv.org/abs/1412.6572).
[^308]: [Pearl, J., & Mackenzie, D. (2018). *The Book of Why: The New Science of Cause and Effect*](https://en.wikipedia.org/wiki/The_Book_of_Why).
[^309]: [Danziger, S., Levav, J., & Avnaim-Pesso, L. (2011). *Extraneous factors in judicial decisions* (PNAS)](https://doi.org/10.1073/pnas.1018033108).
[^310]: [Guthrie, C., Rachlinski, J. J., & Wistrich, A. J. (2007). *Blinking on the Bench: How Judges Decide Cases* (SSRN)](https://ssrn.com/abstract=1018004).

"""

text, count = pattern.subn(new_footer, text)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Footer replaced {count} times.")
