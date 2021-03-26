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
Pekárna má k dispozici {% latex %}5{% endlatex %} kilo mouky, {% latex %}125{% endlatex %} vajec a půl kila soli. Za jeden chleba získá pekárna {% latex %}20{% endlatex %} korun, za housku {% latex %}2{% endlatex %} koruny, za bagetu {% latex %}10{% endlatex %} korun a za koblihu {% latex %}7{% endlatex %} korun. Pekárna se snaží vydělat co nejvíce. Jak ale zjistí kolik chlebů, housek, baget a koblih má upéci?

<details>
	<summary class="code-summary">Zdrojový kód</summary>
	<div markdown="1">
```py
{% include linearni-programovani-v-pythonu/pekarna.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Výpis</summary>
	<div markdown="1">
```
{% include linearni-programovani-v-pythonu/pekarna.out %}```
</div>
</details>

#### Problém batohu
Pro {% latex %}n{% endlatex %} předmětů, kde {% latex %}i{% endlatex %}-tý má nějakou váhu {% latex %}v_i{% endlatex %} a cenu {% latex %}c_i{% endlatex %}, máme batoh s danou nosností {% latex %}V{% endlatex %} a my se do něj snažíme naskládat předměty tak, abychom maximalizovali celkovou cenu předmětů v batohu.

<details>
	<summary class="code-summary">Zdrojový kód</summary>
	<div markdown="1">
```py
{% include linearni-programovani-v-pythonu/batoh.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Výpis</summary>
	<div markdown="1">
```
{% include linearni-programovani-v-pythonu/batoh.out %}```
</div>
</details>

#### Prokládání přímkou

Máme-li {% latex %}n{% endlatex %} bodů {% latex %}(x_1 , y_1 ), \ldots, (x_n , y_n ){% endlatex %} v rovině, tak najděte přímku {% latex %}\left\{x \in \mathbb{R}: y = ax + b\right\}{% endlatex %}, která minimalizuje součet vertikálních vzdáleností bodů od výsledné přímky. Vertikální vzdálenost je vzdálenost měřena pouze na ose {% latex %}y{% endlatex %}. Pro jednoduchost předpokládejte, že výsledná přímka není kolmá na osu {% latex %}x{% endlatex %}.

<details>
	<summary class="code-summary">Zdrojový kód</summary>
	<div markdown="1">
```py
{% include linearni-programovani-v-pythonu/prokladani.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Výpis</summary>
	<div markdown="1">
```
{% include linearni-programovani-v-pythonu/prokladani.out %}```
</div>
</details>

#### Obarvitelnost grafu

Nalezněte minimální {% latex %}k{% endlatex %} takové, že vrcholy grafu {% latex %}G{% endlatex %} lze korektně obarvit {% latex %}k{% endlatex %} barvami.

<details>
	<summary class="code-summary">Zdrojový kód</summary>
	<div markdown="1">
```py
{% include linearni-programovani-v-pythonu/obarvitelnost.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Výpis</summary>
	<div markdown="1">
```
{% include linearni-programovani-v-pythonu/obarvitelnost.out %}```
</div>
</details>

#### Problém obchodního cestujícího
Pro daný ohodnocený neorientovaný graf {% latex %}G = (V, E, f){% endlatex %}, kde {% latex %}f : E \mapsto \mathbb{R}^+_0{% endlatex %}, chceme najít Hamiltonovskou kružnici v {% latex %}G{% endlatex %} s nejmenším ohodnocením.

<details>
	<summary class="code-summary">Zdrojový kód</summary>
	<div markdown="1">
```py
{% include linearni-programovani-v-pythonu/tsp.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Výpis</summary>
	<div markdown="1">
```
{% include linearni-programovani-v-pythonu/tsp.out %}```
</div>
</details>

#### Bin packing
Zjistěte, do kolika nejméně krabic lze rozdělit množinu {% latex %}n{% endlatex %} předmětů s vahami {% latex %}w_1, \ldots, w_i{% endlatex %}. Do každého koše lze umístit předměty o celkové váze nejvýše {% latex %}C{% endlatex %}.

<details>
	<summary class="code-summary">Zdrojový kód</summary>
	<div markdown="1">
```py
{% include linearni-programovani-v-pythonu/bin.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Výpis</summary>
	<div markdown="1">
```
{% include linearni-programovani-v-pythonu/bin.out %}```
</div>
</details>

#### Partition problem
Zjistěte, zda množinu {% latex %}n{% endlatex %} předmětů s vahami {% latex %}w_1, \ldots, w_i{% endlatex %} jde rozdělit na dvě části tak, aby součty vah těchto částí byly stejné.

<details>
	<summary class="code-summary">Zdrojový kód</summary>
	<div markdown="1">
```py
{% include linearni-programovani-v-pythonu/partition.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Výpis</summary>
	<div markdown="1">
```
{% include linearni-programovani-v-pythonu/partition.out %}```
</div>
</details>

#### Pekárny a obchody (a)
V Kocourkově je {% latex %}n{% endlatex %} pekáren a {% latex %}m{% endlatex %} obchodů. Každý den {% latex %}i{% endlatex %}-tá pekárna upeče {% latex %}p_i \in \mathbb{N}{% endlatex %} rohlíků {% latex %}n{% endlatex %} a {% latex %}j{% endlatex %}-tý obchod prodá {% latex %}o_j \in \mathbb{N}{% endlatex %} rohlíků, kde {% latex %}\sum_{i = 1}^{n} p_i = \sum_{j = 1}^{m} o_j{% endlatex %}. Převoz jednoho rohlíku z {% latex %}i{% endlatex %}-té pekárny do {% latex %}j{% endlatex %}-tého obchodu stojí {% latex %}c_{ij}{% endlatex %} korun.

<details>
	<summary class="code-summary">Zdrojový kód</summary>
	<div markdown="1">
```py
{% include linearni-programovani-v-pythonu/ukol01-a.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Výpis</summary>
	<div markdown="1">
```
{% include linearni-programovani-v-pythonu/ukol01-a.out %}```
</div>
</details>

#### Pekárny a obchody (b)
Praxe v Kocourkově ukázala, že když {% latex %}i{% endlatex %}-tá pekárna zásobuje {% latex %}j{% endlatex %}-tý obchod, tak musí pro tuto trasu zajistit logistiku, která je stojí {% latex %}l_{ij}{% endlatex %}. Logistiku {% latex %}l_{ij} \ge 0{% endlatex %} je nutné platit pouze tehdy, když {% latex %}i{% endlatex %}-tá pekárna zásobuje {% latex %}j{% endlatex %}-tý obchod nenulovým počtem rohlíků, a její cena nezávisí na počtu převážených rohlíků. I nadále je nutné platit přepravné {% latex %}c_{ij}{% endlatex %}. Zformulujte příslušnou úlohu LP.

<details>
	<summary class="code-summary">Zdrojový kód</summary>
	<div markdown="1">
```py
{% include linearni-programovani-v-pythonu/ukol01-b.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Výpis</summary>
	<div markdown="1">
```
{% include linearni-programovani-v-pythonu/ukol01-b.out %}```
</div>
</details>

#### Největší nezávislá množina
Najděte co možná největší množinu vrcholů grafu takovou, že žádné dva nesdílejí hranu.

<details>
	<summary class="code-summary">Zdrojový kód</summary>
	<div markdown="1">
```py
{% include linearni-programovani-v-pythonu/max-independent-set.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Výpis</summary>
	<div markdown="1">
```
{% include linearni-programovani-v-pythonu/max-independent-set.out %}```
</div>
</details>

#### Nejmenší vrcholové pokrytí
Najděte co možná nejmenší množinu vrcholů grafu takovou, že všechny hrany grafu obsahují alespoň jeden vrchol z této množiny.

<details>
	<summary class="code-summary">Zdrojový kód</summary>
	<div markdown="1">
```py
{% include linearni-programovani-v-pythonu/min-vertex-cover.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Výpis</summary>
	<div markdown="1">
```
{% include linearni-programovani-v-pythonu/min-vertex-cover.out %}```
</div>
</details>


### Zdroje/materiály
- [Hands-On Linear Programming: Optimization With Python](https://realpython.com/linear-programming-python/)
- [Dokumentace k PuLPu](https://coin-or.github.io/pulp/)
- [Datasety obecně](https://people.sc.fsu.edu/~jburkardt/datasets/)
- [Datasety k TSP](https://people.sc.fsu.edu/~jburkardt/datasets/tsp/tsp.html)
- [Datasety k batohu](https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/knapsack_01.html)
- [Datasety k partition problému](https://people.sc.fsu.edu/~jburkardt/datasets/partition_problem/partition_problem.html)
