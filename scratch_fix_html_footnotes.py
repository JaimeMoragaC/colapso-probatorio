import os

filepath = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

replacements = {
    '<sup><a href="https://www.bailii.org/ew/cases/EWHC/QB/2019/3408.html" target="_blank">1</a></sup>': '<a href="#fn301" id="fnref301"><sup>301</sup></a>',
    '<sup><a href="https://arsenalrecon.com/resources" target="_blank">2</a></sup>': '<a href="#fn302" id="fnref302"><sup>302</sup></a>',
    '<sup><a href="https://www.poderjudicial.es/search/AN/openDocument/9008bc5d29037abf/20150529" target="_blank">3</a></sup>': '<a href="#fn303" id="fnref303"><sup>303</sup></a>',
    '<sup><a href="https://www.bundesverfassungsgericht.de/SharedDocs/Entscheidungen/EN/2008/02/rs20080227_1bvr037007en.html" target="_blank">4</a></sup>': '<a href="#fn304" id="fnref304"><sup>304</sup></a>',
    '<sup><a href="https://casetext.com/case/state-v-loomis-3" target="_blank">5</a></sup>': '<a href="#fn305" id="fnref305"><sup>305</sup></a>',
    '<sup><a href="https://en.wikipedia.org/wiki/Noise:_A_Flaw_in_Human_Judgment" target="_blank">6</a></sup>': '<a href="#fn306" id="fnref306"><sup>306</sup></a>',
    '<sup><a href="https://arxiv.org/abs/1412.6572" target="_blank">7</a></sup>': '<a href="#fn307" id="fnref307"><sup>307</sup></a>',
    '<sup><a href="https://en.wikipedia.org/wiki/The_Book_of_Why" target="_blank">8</a></sup>': '<a href="#fn308" id="fnref308"><sup>308</sup></a>',
    '<sup><a href="https://doi.org/10.1073/pnas.1018033108" target="_blank">9</a></sup>': '<a href="#fn309" id="fnref309"><sup>309</sup></a>',
    '<sup><a href="https://ssrn.com/abstract=1018004" target="_blank">10</a></sup>': '<a href="#fn310" id="fnref310"><sup>310</sup></a>'
}

for old, new in replacements.items():
    text = text.replace(old, new)

# Now replace the footnotes section
old_footer = """---
*Fuentes y Verificabilidad Jurisprudencial:*
<sup>1</sup> *Bates v Post Office Ltd* [2019] EWHC 3408 (QB). Sentencia histórica de la High Court of Justice del Reino Unido sobre la falibilidad de los logs del sistema Horizon.
<sup>2</sup> *Arsenal Consulting Reports on Bhima Koregaon* (Reportes I, II y III, 2021). Peritaje forense que demostró la inyección remota (NetWire RAT) y la alteración del MFT en los terminales de activistas indios.
<sup>3</sup> Sentencia del Tribunal Supremo de España, Sala de lo Penal: STS 300/2015, de 19 de mayo de 2015 (Ponente: Manuel Marchena).
<sup>4</sup> Sentencia del Tribunal Constitucional Federal de Alemania sobre el derecho fundamental a la confidencialidad e integridad de los sistemas TI (BVerfG, 1 BvR 370/07).
<sup>5</sup> *State v. Loomis*, Corte Suprema de Wisconsin (2016). Validó el uso del algoritmo propietario de caja negra COMPAS para sentencias penales.
<sup>6</sup> Kahneman, D., Sibony, O., & Sunstein, C. R. (2021). *Noise: A Flaw in Human Judgment*.
<sup>7</sup> Goodfellow, I. J., Shlens, J., & Szegedy, C. (2014). *Explaining and Harnessing Adversarial Examples* (arXiv:1412.6572).
<sup>8</sup> Pearl, J., & Mackenzie, D. (2018). *The Book of Why: The New Science of Cause and Effect*.
<sup>9</sup> Danziger, S., Levav, J., & Avnaim-Pesso, L. (2011). *Extraneous factors in judicial decisions* (PNAS).
<sup>10</sup> Guthrie, C., Rachlinski, J. J., & Wistrich, A. J. (2007). *Blinking on the Bench: How Judges Decide Cases* (SSRN)."""

new_footer = """---
*Fuentes y Verificabilidad Jurisprudencial (Anexo del Capítulo 8):*
<p id="fn301">301. <a href="https://www.bailii.org/ew/cases/EWHC/QB/2019/3408.html" target="_blank">*Bates v Post Office Ltd* [2019] EWHC 3408 (QB)</a>. Sentencia histórica de la High Court of Justice del Reino Unido sobre la falibilidad de los logs del sistema Horizon. <a href="#fnref301">↩</a></p>
<p id="fn302">302. <a href="https://arsenalrecon.com/resources" target="_blank">*Arsenal Consulting Reports on Bhima Koregaon* (Reportes I, II y III, 2021)</a>. Peritaje forense que demostró la inyección remota (NetWire RAT) y la alteración del MFT en los terminales de activistas indios. <a href="#fnref302">↩</a></p>
<p id="fn303">303. <a href="https://www.poderjudicial.es/search/AN/openDocument/9008bc5d29037abf/20150529" target="_blank">Sentencia del Tribunal Supremo de España, Sala de lo Penal: STS 300/2015</a>, de 19 de mayo de 2015 (Ponente: Manuel Marchena). <a href="#fnref303">↩</a></p>
<p id="fn304">304. <a href="https://www.bundesverfassungsgericht.de/SharedDocs/Entscheidungen/EN/2008/02/rs20080227_1bvr037007en.html" target="_blank">Sentencia del Tribunal Constitucional Federal de Alemania sobre el derecho fundamental a la confidencialidad e integridad de los sistemas TI (BVerfG, 1 BvR 370/07)</a>. <a href="#fnref304">↩</a></p>
<p id="fn305">305. <a href="https://casetext.com/case/state-v-loomis-3" target="_blank">*State v. Loomis*, Corte Suprema de Wisconsin (2016)</a>. Validó el uso del algoritmo propietario de caja negra COMPAS para sentencias penales. <a href="#fnref305">↩</a></p>
<p id="fn306">306. <a href="https://en.wikipedia.org/wiki/Noise:_A_Flaw_in_Human_Judgment" target="_blank">Kahneman, D., Sibony, O., & Sunstein, C. R. (2021). *Noise: A Flaw in Human Judgment*</a>. <a href="#fnref306">↩</a></p>
<p id="fn307">307. <a href="https://arxiv.org/abs/1412.6572" target="_blank">Goodfellow, I. J., Shlens, J., & Szegedy, C. (2014). *Explaining and Harnessing Adversarial Examples* (arXiv:1412.6572)</a>. <a href="#fnref307">↩</a></p>
<p id="fn308">308. <a href="https://en.wikipedia.org/wiki/The_Book_of_Why" target="_blank">Pearl, J., & Mackenzie, D. (2018). *The Book of Why: The New Science of Cause and Effect*</a>. <a href="#fnref308">↩</a></p>
<p id="fn309">309. <a href="https://doi.org/10.1073/pnas.1018033108" target="_blank">Danziger, S., Levav, J., & Avnaim-Pesso, L. (2011). *Extraneous factors in judicial decisions* (PNAS)</a>. <a href="#fnref309">↩</a></p>
<p id="fn310">310. <a href="https://ssrn.com/abstract=1018004" target="_blank">Guthrie, C., Rachlinski, J. J., & Wistrich, A. J. (2007). *Blinking on the Bench: How Judges Decide Cases* (SSRN)</a>. <a href="#fnref310">↩</a></p>"""

text = text.replace(old_footer, new_footer)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Footnotes actualizados al formato HTML cross-link correcto.")
