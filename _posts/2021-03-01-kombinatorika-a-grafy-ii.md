---
language: cz
title: Kombinatorika a Grafy II
category: "lecture notes"
---


- .
{:toc}

{% lecture_notes_preface Martina Kouteckého|2021/2022%}

### 1. přednáška

#### Největší párování

{% math definition %}Párování v {% latex %}G = \left(V, E\right){% endlatex %} je {% latex %}M \subseteq E{% endlatex %} t. ž. {% latex %}\forall v \in V \exists \le 1{% endlatex %} hrana {% latex %}e \in M: v \in e{% endlatex %}{% endmath %}

- **maximální** (do inkluze) -- přidání další hrany pro dané párování už není možné
	- nezajímá nás (v přednášce), prostě hladově přidávejme
- **největší** -- {% latex %}\mathrm{max}(|M|){% endlatex %}

{% math definition %}**volný vrchol** (vzhledem k {% latex %}M{% endlatex %}) -- vrchol, kterého se nedotýká žádná hrana párování{% endmath %}

{% math definition %}**střídavá cesta** (vzdledem k {% latex %}M{% endlatex %}) -- cesta, na které se střídají hrany v párování a hrany mimo párování: {% latex %}u_0, \ldots, u_k{% endlatex %}, kde každá sudá/lichá hrana je v {% latex %}M{% endlatex %}, lichá/sudá není v {% latex %}M{% endlatex %}{% endmath %}

- **volná** střídavá cesta (VSC) -- krajní vrcholy jsou volné (vůči párování)
- {% latex %}\implies{% endlatex %} obsahuje lichý počet hran, sudý počet vrcholů

{% math lemma %}Nechť {% latex %}G = \left(V, E\right){% endlatex %} je graf, {% latex %}M{% endlatex %} párování v {% latex %}G{% endlatex %}. Pak {% latex %}G{% endlatex %} obsahuje VSC (vzhledem k {% latex %}M{% endlatex %}), právě když {% latex %}M{% endlatex %} není největší párování v {% latex %}G{% endlatex %}.{% endmath %}

{:.rightFloatBox}
<div markdown="1">
{:.center}
![](/assets/kombinatorika-a-grafy-ii/alter.svg)
</div>
- {% latex %}\Leftarrow{% endlatex %} pokud {% latex %}M{% endlatex %} má VSC, mohu {% latex %}M{% endlatex %} zvětšit prohozením hran

- {% latex %}\Leftarrow{% endlatex %} nechť {% latex %}M'{% endlatex %} je párování v {% latex %}G{% endlatex %} t. ž {% latex %}|M'| \ge |M|{% endlatex %}
	- uvažme {% latex %}H = \left(V, M \cup M'\right){% endlatex %}; pak má každý vrchol supeň {% latex %}0, 1{% endlatex %} nebo {% latex %}2{% endlatex %} \implies komponenty souvislosti jsou kružnice sudé délky a cesty
	- (👀) -- musí existovat komponenta, která má více hran z {% latex %}M'{% endlatex %}
		- není to kružnice (musela by být lichá a měli bychom máme kolizi ve vrcholu)
		- je to volná (z definice, vzhledem k {% latex %}M{% endlatex %}) střídavá (jinak by měly stejný počet hran) cesta

---

{% math definition %}květ -- lichá „střídavá“ kružnice s vrcholem {% latex %}v_1{% endlatex %}, ke kterému přiléhají dva vrcholy {% latex %}\not\in M{% endlatex %}{% endmath %}
{% math definition %}stonek -- střídavá cesta z {% latex %}v_1{% endlatex %} (i nulové) délky končící volným vrcholem (dál od květu){% endmath %}
- {% latex %}v_1{% endlatex %} může (a nemusí) být volný vrchol -- stačí, aby byl volný vzhledem ke květu

{% math definition %}kytka -- květ + stonek{% endmath %}

{:.center}
![](/assets/kombinatorika-a-grafy-ii/kytka.svg)

{% math definition %} Nechť {% latex %}G = \left(V, E\right){% endlatex %} je neorientovaný graf a {% latex %}e = \left\{u, v\right\}{% endlatex %} jeho hrana. Zápis {% latex %}G . e{% endlatex %} označuje graf vzniklý z {% latex %}G{% endlatex %} kontrakcí („smrštěním“) hrany {% latex %}e{% endlatex %} do jednoho vrcholu:{% endmath %}

{:.center}
![](/assets/kombinatorika-a-grafy-ii/kontrakce.svg)

{% math lemma %}Nechť {% latex %}C{% endlatex %} je květ v grafu {% latex %}G{% endlatex %}. Potom párování {% latex %}M{% endlatex %} v {% latex %}G{% endlatex %} je maximální, právě když {% latex %}M \setminus E(C){% endlatex %} je maximální párování v grafu {% latex %}G . C{% endlatex %}, tj. s květem {% latex %}C{% endlatex %} zkontrahovaným do jediného vrcholu.{% endmath %}

TODO: důkaz?

{% math algorithm %}Edmondsův „zahradní“ algoritmus -- Vstupem je graf {% latex %}G{% endlatex %} a jeho libovolné párování {% latex %}M{% endlatex %}, třeba prázdné. Výstupem je párování {% latex %}M'{% endlatex %}, které je alespoň o {% latex %}1{% endlatex %} větší, než {% latex %}M{% endlatex %}, případně {% latex %}M{% endlatex %} pokud bylo maximální.{% endmath %}

- zkonstruujeme maximální možný **Edmondsův les** vzhledem k aktuálnímu {% latex %}M{% endlatex %} tím, že z volných vrcolů pustíme BFS a střídavě přidáváme vrcholy
	- hranám, které se v lese neobjeví, se říká kompost a nebudou pro nás důležité

{:.center}
![](/assets/kombinatorika-a-grafy-ii/les.svg)

- pokud existuje hrana mezi sudými hladinami různých stromů, pak máme volnou střídavou cestu, kterou zalterujeme
- pokud existuje hrana mezi sudými hladinami jednoho stromu, máme květ {% latex %}C{% endlatex %} -- ten zkontrahujeme a rekurzivně se zavolame
	- vrátí-li {% latex %}M' = M{% endlatex %}, pak nic dalšího neděláme
	- vratí-li nějaké větší párování, tak vhodně zpárujeme {% latex %}C{% endlatex %}
- neexistuje-li hrana mezi sudými hladinami, pak {% latex %}M' = M{% endlatex %}

TODO: časová složitost, důkaz správnosti
