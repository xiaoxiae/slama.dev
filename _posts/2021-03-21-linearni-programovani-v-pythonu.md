---
language: cz
title: Lineární programování v Pythonu
---


- .
{:toc}

### Úvodní informace
Tato stránka obsahuje náhodné programy ze cvičení/přednášky předmětu Lineární programování a kombinatorická optimalizace. Ke spuštění programů je potřeba nainstalovat Pythoní knihovnu `pulp` (přes `pip install pulp`), kterou k řešení problémů používám.

Pokud s `pulp`em také vyřešíte nějaký problém, tak budu moc rád za email/pull request, ať tu máme příkladů co možná nejvíce 🙂.

### Praktické příklady

#### Problém pekárny
Pekárna má k dispozici {% latex %}5{% endlatex %} kilo mouky, {% latex %}125{% endlatex %} vajec a půl kila soli. Za jeden chleba zı́ská pekárna {% latex %}20{% endlatex %} korun, za housku {% latex %}2{% endlatex %} koruny, za bagetu {% latex %}10{% endlatex %} korun a za koblihu {% latex %}7{% endlatex %} korun. Pekárna se snažı́ vydělat co nejvı́ce. Jak ale zjistı́ kolik chlebů, housek, baget a koblih má upéci?

<details>
	<summary class="code-summary">Zdrojový kód</summary>
	<div markdown="1">
```py
{% include linearni-programovani-v-pythonu/pekarna.py %}```
</div>
</details>

#### Problém batohu
Zformulujte Problém batohu pomocı́ celočı́sleného lineárnı́ho programovánı́. Tedy pro {% latex %}n{% endlatex %} předmětů, kde {% latex %}i{% endlatex %}-tý má nějakou váhu {% latex %}v_i{% endlatex %} a cenu {% latex %}c_i{% endlatex %}, máme batoh s danou nosnostı́ {% latex %}V{% endlatex %} a my se do něj snažı́me naskládat předměty tak, abychom maximalizovali celkovou cenu předmětů v batohu.

<details>
	<summary class="code-summary">Zdrojový kód</summary>
	<div markdown="1">
```py
{% include linearni-programovani-v-pythonu/batoh.py %}```
</div>
</details>

#### Prokládání přímkou

Formulujte Prokládánı́ přı́mkou jako úlohu LP. Neboli máme-li {% latex %}n{% endlatex %} bodů {% latex %}(x1 , y1 ), \cdot, (xn , yn ){% endlatex %} v rovině, tak najděte přı́mku {% latex %}\left\{x \in \mathbb{R}: y = ax + b\right\}{% endlatex %}, která minimalizuje součet vertikálnı́ch vzdálenostı́ bodů od výsledné přı́mky. Vertikálnı́ vzdálenost je vzdálenost měřena pouze na ose {% latex %}y{% endlatex %}. Pro jednoduchost předpokládejte, že výsledná přı́mka nenı́ kolmá na osu {% latex %}x{% endlatex %}.

<details>
	<summary class="code-summary">Zdrojový kód</summary>
	<div markdown="1">
```py
{% include linearni-programovani-v-pythonu/prokladani.py %}```
</div>
</details>


### Zdroje/materiály
- [Hands-On Linear Programming: Optimization With Python](https://realpython.com/linear-programming-python/)
- [Dokumentace k PuLPu](https://coin-or.github.io/pulp/)
