import re

filepath = '/home/jaime/Descargas/colapso-probatorio/PAPER_v3_trabajo.md'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the specific text block
old_text = "Formulado así, el proceso se deja leer con las herramientas que Shannon fundó en 1948 para la teoría de la información, que Turing había anticipado en 1936 al describir la mente como un manipulador de símbolos, y que Simon aterrizó en 1955 bajo el nombre de *racionalidad limitada*: todo decisor —humano o artificial— opera con recursos finitos sobre los datos que recibe, y la calidad de su decisión está acotada, antes que por su inteligencia, por la fidelidad de esos datos."

new_text = 'Formulado así, el proceso se deja leer con las herramientas que Shannon fundó en 1948<a href="#fn311" id="fnref311"><sup>311</sup></a> para la teoría de la información, que Turing había anticipado en 1936<a href="#fn312" id="fnref312"><sup>312</sup></a> al describir la mente como un manipulador de símbolos, y que Simon aterrizó en 1955<a href="#fn313" id="fnref313"><sup>313</sup></a> bajo el nombre de *racionalidad limitada*: todo decisor —humano o artificial— opera con recursos finitos sobre los datos que recibe, y la calidad de su decisión está acotada, antes que por su inteligencia, por la fidelidad de esos datos.'

text = text.replace(old_text, new_text)

# Append the new definitions to the footer block
old_footer = '<p id="fn310"><a name="fn310"></a>310. <a href="https://ssrn.com/abstract=1018004" target="_blank">Guthrie, C., Rachlinski, J. J., & Wistrich, A. J. (2007). *Blinking on the Bench: How Judges Decide Cases* (SSRN)</a>. <a href="#fnref310">↩</a></p>'

new_footer = old_footer + '\n' + """<p id="fn311"><a name="fn311"></a>311. <a href="https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf" target="_blank">Shannon, C. E. (1948). *A Mathematical Theory of Communication*. Bell System Technical Journal, 27(3), 379-423</a>. <a href="#fnref311">↩</a></p>
<p id="fn312"><a name="fn312"></a>312. <a href="https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/plms/s2-42.1.230" target="_blank">Turing, A. M. (1936). *On Computable Numbers, with an Application to the Entscheidungsproblem*. Proceedings of the London Mathematical Society, s2-42(1), 230-265</a>. <a href="#fnref312">↩</a></p>
<p id="fn313"><a name="fn313"></a>313. <a href="https://academic.oup.com/qje/article-abstract/69/1/99/1898717" target="_blank">Simon, H. A. (1955). *A Behavioral Model of Rational Choice*. The Quarterly Journal of Economics, 69(1), 99-118</a>. <a href="#fnref313">↩</a></p>"""

text = text.replace(old_footer, new_footer)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Added Shannon, Turing, and Simon footnotes.")
