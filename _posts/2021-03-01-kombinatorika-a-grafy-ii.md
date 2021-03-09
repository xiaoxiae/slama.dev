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

TODO: časová složitost, důkaz správnosti?

### 2. přednáška

{% math definition %}Párování {% latex %}M{% endlatex %} je perfektní, pokud neexistuje v {% latex %}G{% endlatex %} žádný volný vrchol (vůči {% latex %}M{% endlatex %}).{% endmath %}

#### Tutteova věta
{% math definition %}Tutteova podmínka: {% latex %}\forall S \subseteq V: \mathrm{odd}(G - S) \le |S|{% endlatex %}
- kde {% latex %}\mathrm{odd}{% endlatex %} je počet lichých komponent grafu{% endmath %}.

{% math theorem %}Tutteova věta: {% latex %}G{% endlatex %} má perfektní párování {% latex %}\iff{% endlatex %} platí Tutteova podmínka.{% endmath %}

{% math proof %}
{% latex %}\Rightarrow{% endlatex %} obměna: neplatí TP {% latex %}\implies{% endlatex %} není PP. Nehchť {% latex %}\exists S \subseteq V{% endlatex %} t. ž. {% latex %}\mathrm{odd(G - S)} > |S|{% endlatex %}. V perfektním párování by se alespoň {% latex %}1{% endlatex %} vrchol musel spárovat s {% latex %}S{% endlatex %}. To ale nejde, protože jich v {% latex %}S{% endlatex %} není dostatek.

{% latex %}\Leftarrow{% endlatex %} nechť {% latex %}G{% endlatex %} splňuje Tutteovu podmínku. {% latex %}|V|{% endlatex %} je sudá (nastavíme množinu prázdnou). Dokážeme, že {% latex %}G{% endlatex %} má PP indukcí podle počtu nehran.

- základ: {% latex %}G = K_{2n}{% endlatex %}, ten PP má
- indukční podmínka: {% latex %}G{% endlatex %} má nehranu a každý graf na {% latex %}V{% endlatex %}s počtem hran alespoň o 1 větší než {% latex %}|E|{% endlatex %} a platí TP, pak má perfektní párování

- (👀) -- přidáním hrany do grafu se neporuší TP ({% latex %}\forall S \subseteq V{% endlatex %} počet lichých komponent {% latex %}G - S{% endlatex %} buď klesne o {% latex %}2{% endlatex %} nebo zůstane stejný).

{% math definition %}{% latex %}S = \left\{v \in V\ |\ \mathrm{deg}(v) = n - 1\right\} = \left\{v \mid \text{$v$ je spojený se všemi vrcholy} \right\}{% endlatex %}{% endmath %}
- lehký příklad: každá komponenta {% latex %}G - S{% endlatex %} je lichá klika
	- v rámci dané kliky vypáruji vše až na jeden vrchol, ten spáruji v rámci {% latex %}S{% endlatex %} ({% latex %}S{% endlatex %} vidí všechny) a zbytek v {% latex %}S{% endlatex %} spáruji spolu
- alespoň {% latex %}1{% endlatex %} komponenta {% latex %}K{% endlatex %} není klika, tedy {% latex %}\exists x, y{% endlatex %} nesousedi {% latex %}x, y{% endlatex %}
	- ti mají společného souseda {% latex %}u{% endlatex %} (TODO tvrzení)
	- jelikož {% latex %}u{% endlatex %} není spojený s {% latex %}S{% endlatex %}, tak je spojený s nějakým vrcholem {% latex %}v{% endlatex %}

{:.center}
![](/assets/kombinatorika-a-grafy-ii/xyuv.svg)

{% latex %}G_1 = G + e_1{% endlatex %} a {% latex %}G_2 = G + e_2{% endlatex %} díky předchozímu pozorování splňují TP a spolu s IP {% latex %}\implies \exists{% endlatex %} PP {% latex %}M_1, M_2{% endlatex %} v {% latex %}G_1, G_2{% endlatex %}
- jednoduchý příklad: {% latex %}e_1{% endlatex %} nepatří do {% latex %}M_1 \implies M_1{% endlatex %} je PP pro {% latex %}G{% endlatex %}, analogicky pro {% latex %}G{% endlatex %} (případně přealternuju cyklus, na kterém je)

Předpokládejme {% latex %}e_1 \in M_1, e_2 \in M_2, H = (V, M_1 \cup M_2){% endlatex %}. {% latex %}H {% endlatex %} tedy obsahuje „dvoubarevné hrany“ {% latex %}e \in M_1 \cap M_2{% endlatex %} nebo střídavé sudé cykly. Navíc neobsahuje izolované vrcholy a střídavé cesty, protože {% latex %}M_1, M_2{% endlatex %} byly perfektní.
- jednodušší případ: {% latex %}e_1{% endlatex %} leží v jiné komponentě {% latex %}H{% endlatex %} než {% latex %}e_2{% endlatex %} -- stačí přealternovat hrany tak, aby ani {% latex %}e_1{% endlatex %} ani {% latex %}e_2{% endlatex %} v {% latex %}H{% endlatex %} neležely.

{:.center}
![](/assets/kombinatorika-a-grafy-ii/easy.svg)

- složitější příklad: spojíme {% latex %}uy{% endlatex %} a zbytek patřičně doplníme

{:.center}
![](/assets/kombinatorika-a-grafy-ii/hard.svg)

{% endmath %}

{% math theorem %}Petersen: každý {% latex %}3{% endlatex %}-regulární {% latex %}2{% endlatex %}-souvislý (vrcholově i hranově, pro 2-souvislost) graf má PP.{% endmath %}

{% math proof %}Nechť {% latex %}G = (V, E){% endlatex %} je {% latex %}3{% endlatex %}-regulární a {% latex %}2{% endlatex %}-souvislý. Chci ukázat, že {% latex %}G{% endlatex %} splňuje TP. Předpokládejme danou {% latex %}S \subseteq V{% endlatex %}.

1. každá {% latex %}G - S{% endlatex %} je v {% latex %}G{% endlatex %} spojena aspoň dvěma hranami s {% latex %}S{% endlatex %} (je {% latex %}2{% endlatex %}-souvislý...)
2. každá lichá komponenta {% latex %}G - S{% endlatex %} je s {% latex %}S{% endlatex %} spojena lichým počtem hran
	- nechť {% latex %}L{% endlatex %} je lichá komponenta {% latex %}G - S{% endlatex %}; pak:
{% latex display %}\sum_{x \in V(L)}^{\mathrm{deg}_G(x)} \overset{3-\text{reg.}}{=} \underbrace{3|V(L)|}_{\text{liché}} = \underbrace{2 (\text{\# hran vedoucích uvnitř $L$})}_{\text{sudé}} + \underbrace{1 (\text{\# hran vedoucích uvnitř $L$})}_{\text{liché}}{% endlatex %}
což je přesně to, co jsem potřeboval (počet hran vedoucích z {% latex %}L{% endlatex %})

TODO: obrázek

{% latex %}p = \text{\# hran mezi $S$ a lichou komponentou $G - S$}{% endlatex %}
- {% latex %}p \ge 3 \cdot \mathrm{odd(G - S)}{% endlatex %}
- {% latex %}p \le 3 \cdot |S|{% endlatex %} (každý vrchol {% latex %}S{% endlatex %} vysílá ven {% latex %}\le 3{% endlatex %} hrany (z 3-regularity))

{% latex %}3|S| \ge 3 \cdot \mathrm{odd}(G - S){% endlatex %}, tedy TP platí a graf má perfektní párování.
{% endmath %}


