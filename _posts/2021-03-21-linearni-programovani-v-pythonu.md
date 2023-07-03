---
language: cz
title: Lineární programování v Pythonu
end: "<a href='/youtube/linear-programming-in-python'>English version of the article</a>"
---

- .
{:toc}

### Úvodní informace
Tato stránka obsahuje náhodné programy ze cvičení/přednášky předmětu Lineární programování a kombinatorická optimalizace. Ke spuštění programů je potřeba nainstalovat Pythoní knihovnu `pulp` (přes `pip install pulp`), kterou k řešení problémů používám.

Pokud s `pulp`em také vyřešíte nějaký problém, tak budu moc rád za email/pull request, ať tu máme příkladů co možná nejvíce 🙂.

### Praktické příklady

#### Problém pekárny
Pekárna má k dispozici \(5000\ \mathrm{g}\) mouky, \(125\) vajec a \(500\ \mathrm{g}\) soli.
Může z nich péct chleby, housky, bagety a koblihy s tím, že každé pečivo vyžaduje jiné množství surovin; konkrétně

|       | chléb               | houska              | bageta              | kobliha             |
| ---   | --:                 | --:                 | --:                 | --:                 |
| mouka | \(500\ \mathrm{g}\) | \(150\ \mathrm{g}\) | \(230\ \mathrm{g}\) | \(100\ \mathrm{g}\) |
| vejce | \(10\ \mathrm{ks}\) | \(2\ \mathrm{ks}\)  | \(7\ \mathrm{ks}\)  | \(1\ \mathrm{ks}\)  |
| sůl   | \(50\ \mathrm{g}\)  | \(10\ \mathrm{g}\)  | \(15\ \mathrm{g}\)  |                     |

Za jeden chleba získá pekárna \(20\ \mathrm{Kč}\), za housku \(2\ \mathrm{Kč}\), za bagetu \(10\ \mathrm{Kč}\) a za koblihu \(7\ \mathrm{Kč}\).

Pekárna se snaží vydělat co nejvíce -- kolik chlebů, housek, baget a koblih má ze surovin upéci?

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
Pro \(n\) předmětů, kde \(i\)-tý má nějakou váhu \(v_i\) a cenu \(c_i\), máme batoh s danou nosností \(V\) a my se do něj snažíme naskládat předměty tak, abychom maximalizovali celkovou cenu předmětů v batohu.

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

Máme-li \(n\) bodů \((x_1 , y_1 ), \ldots, (x_n , y_n )\) v rovině, tak najděte přímku \(\left\{x \in \mathbb{R}: y = ax + b\right\}\), která minimalizuje součet vertikálních vzdáleností bodů od výsledné přímky. Vertikální vzdálenost je vzdálenost měřena pouze na ose \(y\). Pro jednoduchost předpokládejte, že výsledná přímka není kolmá na osu \(x\).

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

#### Vrcholová obarvitelnost grafu

Nalezněte minimální \(k\) takové, že vrcholy grafu \(G\) lze korektně obarvit \(k\) barvami.

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

#### Hranová obarvitelnost grafu

Nalezněte minimální \(k\) takové, že hrany grafu \(G\) lze korektně obarvit \(k\) barvami.

<details>
	<summary class="code-summary">Zdrojový kód</summary>
	<div markdown="1">
```py
{% include linearni-programovani-v-pythonu/obarvitelnost2.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Výpis</summary>
	<div markdown="1">
```
{% include linearni-programovani-v-pythonu/obarvitelnost2.out %}```
</div>
</details>

#### Problém obchodního cestujícího
Pro daný ohodnocený neorientovaný graf \(G = (V, E, f)\), kde \(f : E \mapsto \mathbb{R}^+_0\), chceme najít Hamiltonovskou kružnici v \(G\) s nejmenším ohodnocením.

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
Zjistěte, do kolika nejméně krabic lze rozdělit množinu \(n\) předmětů s vahami \(w_1, \ldots, w_i\). Do každého koše lze umístit předměty o celkové váze nejvýše \(C\).

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
Zjistěte, zda množinu \(n\) předmětů s vahami \(w_1, \ldots, w_i\) jde rozdělit na dvě části tak, aby součty vah těchto částí byly stejné.

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
V Kocourkově je \(n\) pekáren a \(m\) obchodů. Každý den \(i\)-tá pekárna upeče \(p_i \in \mathbb{N}\) rohlíků \(n\) a \(j\)-tý obchod prodá \(o_j \in \mathbb{N}\) rohlíků, kde \(\sum_{i = 1}^{n} p_i = \sum_{j = 1}^{m} o_j\). Převoz jednoho rohlíku z \(i\)-té pekárny do \(j\)-tého obchodu stojí \(c_{ij}\) korun.

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
Praxe v Kocourkově ukázala, že když \(i\)-tá pekárna zásobuje \(j\)-tý obchod, tak musí pro tuto trasu zajistit logistiku, která je stojí \(l_{ij}\). Logistiku \(l_{ij} \ge 0\) je nutné platit pouze tehdy, když \(i\)-tá pekárna zásobuje \(j\)-tý obchod nenulovým počtem rohlíků, a její cena nezávisí na počtu převážených rohlíků. I nadále je nutné platit přepravné \(c_{ij}\). Zformulujte příslušnou úlohu LP.

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
