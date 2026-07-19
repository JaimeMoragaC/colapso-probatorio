import os

filepath = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix El espejo comparado (superscripts with links inside)
text = text.replace('**Reino Unido — Horizon / [*Bates v Post Office* [2019] EWHC 3408 (QB)¹](https://www.bailii.org/ew/cases/EWHC/QB/2019/3408.html).**', '**Reino Unido — Horizon / *Bates v Post Office* [2019] EWHC 3408 (QB)<sup><a href="https://www.bailii.org/ew/cases/EWHC/QB/2019/3408.html" target="_blank">1</a></sup>.**')

text = text.replace('**India — Caso Bhima Koregaon y la inyección remota (2021)².**', '**India — Caso Bhima Koregaon y la inyección remota (2021)<sup><a href="https://arsenalrecon.com/resources" target="_blank">2</a></sup>.**')

text = text.replace('**España — [*STS 300/2015* y la manipulación visual³](https://www.poderjudicial.es/search/AN/openDocument/9008bc5d29037abf/20150529).**', '**España — *STS 300/2015* y la manipulación visual<sup><a href="https://www.poderjudicial.es/search/AN/openDocument/9008bc5d29037abf/20150529" target="_blank">3</a></sup>.**')

text = text.replace('**Alemania — el *Staatstrojaner* y el [*BVerfG* (27 de febrero de 2008, 1 BvR 370/07)⁴](https://www.bundesverfassungsgericht.de/SharedDocs/Entscheidungen/EN/2008/02/rs20080227_1bvr037007en.html).**', '**Alemania — el *Staatstrojaner* y el BVerfG (27 de febrero de 2008, 1 BvR 370/07)<sup><a href="https://www.bundesverfassungsgericht.de/SharedDocs/Entscheidungen/EN/2008/02/rs20080227_1bvr037007en.html" target="_blank">4</a></sup>.**')

text = text.replace('**Estados Unidos — [*State v. Loomis*, 881 N.W.2d 749 (Wis. 2016)⁵](https://casetext.com/case/state-v-loomis-3).**', '**Estados Unidos — *State v. Loomis*, 881 N.W.2d 749 (Wis. 2016)<sup><a href="https://casetext.com/case/state-v-loomis-3" target="_blank">5</a></sup>.**')

# Fix in-text citations (neurobiology and AI sections)
text = text.replace('Kahneman⁶,', 'Kahneman<sup><a href="https://en.wikipedia.org/wiki/Noise:_A_Flaw_in_Human_Judgment" target="_blank">6</a></sup>,')

text = text.replace('[Goodfellow, Shlens & Szegedy (2014)⁷](https://arxiv.org/abs/1412.6572)', 'Goodfellow, Shlens & Szegedy (2014)<sup><a href="https://arxiv.org/abs/1412.6572" target="_blank">7</a></sup>')

text = text.replace('[Judea Pearl en sus trabajos sobre inferencia causal (2018)⁸](https://en.wikipedia.org/wiki/The_Book_of_Why)', 'Judea Pearl en sus trabajos sobre inferencia causal (2018)<sup><a href="https://en.wikipedia.org/wiki/The_Book_of_Why" target="_blank">8</a></sup>')

text = text.replace('los estudios empíricos sobre el condicionamiento metabólico del fallo', 'los estudios empíricos sobre el condicionamiento metabólico del fallo (Danziger et al., 2011)<sup><a href="https://doi.org/10.1073/pnas.1018033108" target="_blank">9</a></sup>')

text = text.replace('las heurísticas judiciales (§8.3)', 'las heurísticas judiciales (Guthrie et al., 2007)<sup><a href="https://ssrn.com/abstract=1018004" target="_blank">10</a></sup> (§8.3)')

text = text.replace('¹ *Bates v Post Office', '<sup>1</sup> *Bates v Post Office')
text = text.replace('² *Arsenal Consulting', '<sup>2</sup> *Arsenal Consulting')
text = text.replace('³ Sentencia del Tribunal Supremo', '<sup>3</sup> Sentencia del Tribunal Supremo')
text = text.replace('⁴ Sentencia del Tribunal Constitucional', '<sup>4</sup> Sentencia del Tribunal Constitucional')
text = text.replace('⁵ *State v. Loomis*', '<sup>5</sup> *State v. Loomis*')
text = text.replace('⁶ Kahneman, D.', '<sup>6</sup> Kahneman, D.')
text = text.replace('⁷ Goodfellow, I. J.', '<sup>7</sup> Goodfellow, I. J.')
text = text.replace('⁸ Pearl, J.', '<sup>8</sup> Pearl, J.')

# Add footnotes 9 and 10 to the bottom
text = text.replace('⁸ Pearl, J., & Mackenzie, D. (2018). *The Book of Why: The New Science of Cause and Effect*.', '<sup>8</sup> Pearl, J., & Mackenzie, D. (2018). *The Book of Why: The New Science of Cause and Effect*.\n<sup>9</sup> Danziger, S., Levav, J., & Avnaim-Pesso, L. (2011). *Extraneous factors in judicial decisions* (PNAS).\n<sup>10</sup> Guthrie, C., Rachlinski, J. J., & Wistrich, A. J. (2007). *Blinking on the Bench: How Judges Decide Cases* (SSRN).')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Superíndices arreglados en PAPER_v3_trabajo.md")
