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

{% math definition "volný vrchol" %} (vzhledem k {% latex %}M{% endlatex %}) -- vrchol, kterého se nedotýká žádná hrana párování{% endmath %}

{% math definition "střídavá cesta" %} (vzdledem k {% latex %}M{% endlatex %}) -- cesta, na které se střídají hrany v párování a hrany mimo párování: {% latex %}u_0, \ldots, u_k{% endlatex %}, kde každá sudá/lichá hrana je v {% latex %}M{% endlatex %}, lichá/sudá není v {% latex %}M{% endlatex %}{% endmath %}

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

{% math definition "květ" %} lichá „střídavá“ kružnice s vrcholem {% latex %}v_1{% endlatex %}, ke kterému přiléhají dva vrcholy {% latex %}\not\in M{% endlatex %}{% endmath %}
{% math definition "stonek" %} střídavá cesta z {% latex %}v_1{% endlatex %} (i nulové) délky končící volným vrcholem (dál od květu){% endmath %}
- {% latex %}v_1{% endlatex %} může (a nemusí) být volný vrchol -- stačí, aby byl volný vzhledem ke květu

{% math definition "kytka" %} květ + stonek{% endmath %}

{:.center}
![](/assets/kombinatorika-a-grafy-ii/kytka.svg)

{% math definition %} Nechť {% latex %}G = \left(V, E\right){% endlatex %} je neorientovaný graf a {% latex %}e = \left\{u, v\right\}{% endlatex %} jeho hrana. Zápis {% latex %}G . e{% endlatex %} označuje graf vzniklý z {% latex %}G{% endlatex %} kontrakcí („smrštěním“) hrany {% latex %}e{% endlatex %} do jednoho vrcholu:{% endmath %}

{:.center}
![](/assets/kombinatorika-a-grafy-ii/kontrakce.svg)

{% math lemma %}Nechť {% latex %}C{% endlatex %} je květ v grafu {% latex %}G{% endlatex %}. Potom párování {% latex %}M{% endlatex %} v {% latex %}G{% endlatex %} je maximální, právě když {% latex %}M \setminus E(C){% endlatex %} je maximální párování v grafu {% latex %}G . C{% endlatex %}, tj. s květem {% latex %}C{% endlatex %} zkontrahovaným do jediného vrcholu.{% endmath %}

TODO: důkaz?

{% math algorithm "Edmondsův „zahradní“" %} vstupem je graf {% latex %}G{% endlatex %} a jeho libovolné párování {% latex %}M{% endlatex %}, třeba prázdné. Výstupem je párování {% latex %}M'{% endlatex %}, které je alespoň o {% latex %}1{% endlatex %} větší, než {% latex %}M{% endlatex %}, případně {% latex %}M{% endlatex %} pokud bylo maximální.{% endmath %}

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

{% math definition "perfektní párování" %}Párování {% latex %}M{% endlatex %} je perfektní, pokud neexistuje v {% latex %}G{% endlatex %} žádný volný vrchol (vůči {% latex %}M{% endlatex %}).{% endmath %}

#### Tutteova věta
{% math definition "Tutteova podmínka" %} {% latex %}\forall S \subseteq V: \mathrm{odd}(G - S) \le |S|{% endlatex %}
- kde {% latex %}\mathrm{odd}{% endlatex %} je počet lichých komponent grafu{% endmath %}.

{% math theorem "Tutteova věta" %} {% latex %}G{% endlatex %} má perfektní párování {% latex %}\iff{% endlatex %} platí Tutteova podmínka.{% endmath %}

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

{% math theorem "Petersen" %} každý {% latex %}3{% endlatex %}-regulární {% latex %}2{% endlatex %}-souvislý (vrcholově i hranově, pro 2-souvislost) graf má PP.{% endmath %}

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

### 3. přednáška


#### Tutte v2.0

{% math lemma "o kontrahovatelné hraně" %} Nechť {% latex %}G{% endlatex %} je 3-souvislý různý od {% latex %}K_4{% endlatex %} ({% latex %}|V| \ge 5{% endlatex %}). Potom {% latex %}G{% endlatex %} obsahuje hranu t. ž. {% latex %}G \ e{% endlatex %} je 3-souvislý.{% endmath %}

{% math proof %}Sporem -- nechť {% latex %}G{% endlatex %} je 3-souvislý ale neexistuje žádná hrana. Tedy {% latex %}\forall e \in E: G \ e{% endlatex %} není 3-souvislý.

{% math theorem %}Pomocné: {% latex %}\forall e = \left\{x, y\right\} \exists z_e \in V \setminus \left\{x, y\right\}{% endlatex %} t. ž. {% latex %}\left\{x, y, z_e\right\}{% endlatex %} tvoří vrcholový řez v G, navíc každý z {% latex %}\left\{x, y, z_e\right\}{% endlatex %} má alespoň jednoho souseda v každé komponentě {% latex %}G \setminus \left\{x, y, z_e\right\}{% endlatex %}.
- počítáme s předpokladem, že žádná hrana není kontrahovatelná!
{% endmath %}

- (👀) -- {% latex %}S{% endlatex %} minimální vrcholový řez {% latex %}G{% endlatex %}, pak každý vrchol {% latex %}S{% endlatex %} má souseda v každé komponentě {% latex %}G \setminus S{% endlatex %} (když to pro nějaký {% latex %}v{% endlatex %} neplatí, tak {% latex %}S \setminus v{% endlatex %} je pořád řez).

TOOD: obrázek?

{% math proof %}
Vím, že {% latex %}G \setminus e{% endlatex %} není 3-souvislý, tedy má vrcholový řez velikosti 2. Nechť {% latex %}v_e = {% endlatex %} vrchol vzniklý kontrakcí {% latex %}\left\{x, y\right\} = e{% endlatex %}. Tento řez obsahuje {% latex %}v_e{% endlatex %}, jinak by to byl řez už pro {% latex %}G{% endlatex %}.

Označme řez {% latex %}v_e, z_e{% endlatex %}.

TODO: obrázek?

Po rozkontrahování vidíme, že {% latex %}\forall \left\{x, y, z_e\right\}{% endlatex %} musí mít souseda v každé komponentě (jinak spor s 3-souvislostí). Tedy {% latex %}z_e{% endlatex %} je hledaný vrchol.
{% endmath %}

Pro důkaz původního lemmatu si zvolím {% latex %}e = \left\{x, y \right\} \in E{% endlatex %} a {% latex %}z_e{% endlatex %} z pomocného tvrzení tak, aby nejmenší komponenta {% latex %}G - z, y, z_e{% endlatex %} byla co nejmenší (co do počtu vrcholů).

TODO: obrázek?

Protože {% latex %}z_e{% endlatex %} má souseda ve všech komponentách, má nějakého souseda {% latex %}u \in C, f = \left\{z_e, u\right\}{% endlatex %} (kde {% latex %}C{% endlatex %} je naše nejmenší komponenta). Pomocné tvrzení pro {% latex %}f{% endlatex %} dá nějaký {% latex %}z_f \in V{% endlatex %} t. ž. {% latex %}\left\{z_e, z_f, u\right\}{% endlatex %} je vrcholový řez {% latex %}G{% endlatex %}.

Nechť {% latex %}D{% endlatex %} je komponenta {% latex %}G - z_e, z_f, u{% endlatex %} neobsahující {% latex %}x, y{% endlatex %} (existuje, protože {% latex %}x, y{% endlatex %} jsou spojené a graf se rozpadne alespoň na 2 komponenty). Tvrdím, že {% latex %}D \subseteq C \setminus \left\{u\right\}{% endlatex %}, protože {% latex %}D{% endlatex %} nemůže obsahovat {% latex %}z_e, z_f, u{% endlatex %} (vrcholy řezu), {% latex %}x, y{% endlatex %} (z definice {% latex %}D{% endlatex %}), ale {% latex %}u{% endlatex %} má souseda, takže v {% latex %}D{% endlatex %} ještě něco zbyde. Tedy {% latex %}|D| < |C|{% endlatex %}, což je spor s minimalitou.
{% endmath %}

{% math theorem "Tutteova charakterizace 3-souvislých grafů" %} Graf {% latex %}G{% endlatex %} je 3-souvislý {% latex %}\iff{% endlatex %} existuje posloupnost {% latex %}K_4 \cong G_0 \cong G_1 \cong \ldots \cong G{% endlatex %} t. ž. {% latex %}\forall i \in [n], G_{i - 1}{% endlatex %} vznikne z {% latex %}G_i{% endlatex %} kontrakcí hrany, navíc {% latex %}G_i{% endlatex %} má všechny vrcholy stupně {% latex %}\ge 3{% endlatex %}{% endmath %}

TODO: obrázek?

{% math proof %} {% latex %}\Rightarrow{% endlatex %} Jednoduchá induktivní aplikace lemma o kontrahovatelné hraně.
{% latex %}\Leftarrow{% endlatex %} Mějme {% latex %}G_0, \ldots, G_n{% endlatex %} dle předpokladu. Chceme, že {% latex %}G_n \cong G{% endlatex %} je 3-souvislý. Indukcí:
- {% latex %}K_4{% endlatex %} je 3-souvislý
- {% latex %}G_{i - 1}{% endlatex %} je 3-souvislý {% latex %}\implies G_i{% endlatex %} je 3-souvislý

Pro spor nechť {% latex %}G_i{% endlatex %} má vrcholový řez velikosti 2, označme ho {% latex %}R{% endlatex %}. Pak každá komponenta {% latex %}G_i - R{% endlatex %} má alespoň 2 vrcholy {% latex %}x, y{% endlatex %} (TODO: obrázek) (osamocený vrchol může sousedit jen s řezem, ale ten je velikosti 2, spor s {% latex %}\forall \mathrm{deg}(v) \ge 3{% endlatex %}).

Potom ani {% latex %}G_{i - 1}{% endlatex %} nebyl 3-souvislý.
- {% latex %}e = \left\{x, y\right\} \implies G_{i - 1}{% endlatex %} má řez velikosti 1.
- {% latex %}e{% endlatex %} celá obsažená v komponentě {% latex %}\implies \left\{x, y\right\}{% endlatex %} je stále {% latex %}G_{i - 1}{% endlatex %}
- {% latex %}e = \left\{z, y\right\}{% endlatex %} pro {% latex %}z{% endlatex %} z nějaké komponenty {% latex %}\implies \left\{zy, x\right\}{% endlatex %} je řez v {% latex %}G_{i - 1}{% endlatex %}
	- využíváme, že každá komponenta má alespoň {% latex %}2{% endlatex %} vrcholy -- kdyby ne, tak {% latex %}\left\{zy, x\right\}{% endlatex %} nemusí nic odříznout, pokud tam byla jednovrcholová komponenta
{% endmath %}

#### Minory

{% math definition "minor" %} Nechť {% latex %}H, G{% endlatex %} jsou grafy. Pak {% latex %}H{% endlatex %} je minor {% latex %}G{% endlatex %} (nebo že {% latex %}G {% endlatex %} obsahuje {% latex %}H{% endlatex %} jako minor), značíme {% latex %}H \preceq G{% endlatex %}, pokud {% latex %}H{% endlatex %} lze získat z {% latex %}G{% endlatex %} posloupností mazání vrcholů, mazání hran nebo kontrakcí hran.{% endmath %}

TODO: příklad

- (👀) -- {% latex %}\preceq{% endlatex %} je transitivní (prostě spojím posloupnosti)
- (👀) -- {% latex %}H{% endlatex %} podgraf {% latex %}G \implies H{% endlatex %} minor {% latex %}G{% endlatex %}
	- podgraf vzniká přesně mazáním vrcholů a mazáním hran
- (👀) -- {% latex %}G{% endlatex %} rovinný {% latex %}\implies{% endlatex %} jeho minory jsou také rovinné
	- pro podgraf očividné, je jen potřeba si rozmyslet kontrakci (že nic topologicky nerozbije)

{% math theorem "Kuratowského" %} {% latex %}G{% endlatex %} rovinný {% latex %}\iff{% endlatex %} neobsahuje jako dělení {% latex %}K_5{% endlatex %} ani {% latex %}K_{3, 3}{% endlatex %}{% endmath %}
- umíme {% latex %}\implies{% endlatex %}, protože {% latex %}K_5{% endlatex %} ani {% latex %}K_{3, 3}{% endlatex %} nejsou rovinné a dělením se to rovinným také nestane)

{% math theorem "Kuratowski 1930, Warner 1937" %} Následující jsou ekvivalentní:
1. {% latex %}G{% endlatex %} je rovinný
2. {% latex %}G{% endlatex %} neobsahuje dělení {% latex %}K_5{% endlatex %} ani {% latex %}K_{3, 3}{% endlatex %} jako podgraf
3. {% latex %}G{% endlatex %} neobsahuje dělení {% latex %}K_5{% endlatex %} ani {% latex %}K_{3, 3}{% endlatex %} jako minor.
{% endmath %}

- Kuratowski dokázal {% latex %}1\iff 2{% endlatex %}, Wagner {% latex %}1\iff 3{% endlatex %}

{% math proof %}
- {% latex %}1 \implies 2{% endlatex %} (z prváku)
- {% latex %}3 \implies 2{% endlatex %} (obměna + „obsahuej dělení jako podgraf“ {% latex %}\implies{% endlatex %} „obsahuje minor“)
- {% latex %}1 \implies 3{% endlatex %}: vyplývá z pozorování, že je-li rovinný, tak i minor bude rovinný
- {% latex %}2 \implies 3{% endlatex %} na cvičení.
- {% latex %}3 \implies 1{% endlatex %}: hlavní důkaz.

Indukcí podle {% latex %}|V(G)|{% endlatex %}, pro {% latex %}|V(G)| \le 4{% endlatex %} ok; předpokládám {% latex %}G{% endlatex %} má alespoň 5 vrcholů a neobsahuje {% latex %}K_5{% endlatex %} ani {% latex %}K_{3, 3}{% endlatex %} jako minor. Rozeberu případy podle {% latex %}k_v(G){% endlatex %} (vrcholová souvislost {% latex %}G{% endlatex %}).
0. {% latex %}\implies{% endlatex %} nesouvislý graf, každá komponenta je rovina podle IP
1. {% latex %}\implies{% endlatex %} artikulačním vrcholem {% latex %}x{% endlatex %} rozpojíme, podle IP nakreslíme (s tím, že {% latex %}x{% endlatex %} bude na vnější stěně -- to umíme tím, že to dáme na kouli a projektujeme na rovinu).
2. {% latex %}\implies{% endlatex %} na cvičení.
3. (více než) {% latex %}\implies{% endlatex %} příští přednáška.
{% endmath %}

### 4. přednáška
Dokazuji: {% latex %}G{% endlatex %} nemá {% latex %}K_5{% endlatex %} a {% latex %}K_{3, 3}{% endlatex %} jako minor {% latex %}\implies{% endlatex %} {% latex %}G{% endlatex %} je rovinný ({% latex %}\iff{% endlatex %} má rovinné nakreslení).

Rozebíráme {% latex %}k_v (G) \ge 3{% endlatex %}. Použijeme LoKH (lemma o kontrahovatelné hraně) -- {% latex %}\exists e = \left\{x, y\right\}{% endlatex %} t. ž. {% latex %}G.e = G'{% endlatex %} je {% latex %}3{% endlatex %}-souvislý.
- (👀) -- {% latex %}G'{% endlatex %} nemůže obsahovat {% latex %}K_5{% endlatex %} ani {% latex %}K_{3, 3}{% endlatex %} jako minor (spor s předpokladem) {% latex %}\rightarrow \mathcal{G}' \ldots{% endlatex %} rovinné nakreslení {% latex %}G'{% endlatex %} (z IP existuje)

{% latex %}G'' = G' - v_e{% endlatex %} (vrchol vzniklý kontrakcí {% latex %}e{% endlatex %}) {% latex %} = G - \left\{x, y\right\}{% endlatex %}
- (👀) -- {% latex %}G''{% endlatex %} bude {% latex %}2{% endlatex %}-souvislý (protože {% latex %}G'{% endlatex %} je {% latex %}3{% endlatex %}-souvislý a {% latex %}G''{% endlatex %} vznikne odebráním vrcholu)
- taky rovinný (odebráním mi žádný minor nevznikne), {% latex %}\mathcal{G}''{% endlatex %} nakreslení {% latex %}G''{% endlatex %} vzniklé z {% latex %}\mathcal{G}'{% endlatex %} odebráním {% latex %}v_e{% endlatex %}

TODO: obrázek, tady je potřeba

- {% latex %}N(x){% endlatex %} -- sousedi {% latex %}x{% endlatex %}
- {% latex %}N(y){% endlatex %} -- sousedi {% latex %}y{% endlatex %}
- {% latex %}N(x) \cup N(y) \setminus \left\{x, y\right\} \subseteq C{% endlatex %} (každý soused {% latex %}x{% endlatex %} kromě {% latex %}y{% endlatex %} je i sousedem {% latex %}v_e{% endlatex %} v {% latex %}G'{% endlatex %}, stejně pro {% latex %}y{% endlatex %}

3 případy (TODO: obrázky):
1. {% latex %}|N(x) \cap N(y)| \ge 3{% endlatex %} -- nenastane, protože kontrakcí dostanu {% latex %}K_5{% endlatex %}
2. {% latex %}\exists a_1, a_2 \in N(x) \cap C, \exists b_1, b_2 \in N(y) \cap C{% endlatex %}, na {% latex %}C{% endlatex %} jsou v pořadí {% latex %}a_1, b_1, a_2, b_2{% endlatex %} -- nenastane, protože kontrakcí dostanu {% latex %}K_{3, 3}{% endlatex %}
3. zbytek -- nenasatane ani (1), ani (2)
	- označme {% latex %}a_1, \ldots, a_k \in N(x) \cap C{% endlatex %} v pořadí, jak se objevují na {% latex %}C{% endlatex %}
	- můžu nakreslit všechny hrany {% latex %}xa_1, \ldots xa_k{% endlatex %}
	- {% latex %}a_1, \ldots, a_k{% endlatex %} rozdělují {% latex %}C{% endlatex %} na vnitřně disjunktní cesty {% latex %}P_1, \ldots P_k{% endlatex %} ({% latex %}k \ge 2{% endlatex %} protože {% latex %}G{% endlatex %} je {% latex %}3{% endlatex %}-souvislý... {% latex %}x{% endlatex %} sousedí s {% latex %}y{% endlatex %} a s {% latex %}\ge 2{% endlatex %} dalšími vrcholy)
		- chceme: {% latex %}N(y) \setminus \left\{x\right\}{% endlatex %} patří do jediné {% latex %}P_i{% endlatex %} (pro nějaké {% latex %}i{% endlatex %})
		- TODO: případy přes obrázek
		- TODO: rozbor případů
	- {% latex %}y{% endlatex %} tedy nakreslím do té správně stěny a mám hotovo

#### Kreslení grafů na plochy
{% math definition %}Nechť {% latex %}X \subseteq \mathbb{R}^n, Y \subseteq \mathbb{R}^m{% endlatex %}. Potom homeomorfismus z {% latex %}X{% endlatex %} na {% latex %}Y{% endlatex %} je funkce {% latex %}f: X \mapsto Y{% endlatex %}, která je spojitá, bijekce a {% latex %}f^{-1}{% endlatex %} je spojitá. {% latex %}X, Y{% endlatex %} jsou homeomorfní ({% latex %}X \cong Y{% endlatex %}) pokud mezi nimi existuje homeomorfismus.{% endmath %}
- něco jako isomorfismus u grafů ({% latex %}X \cong Y{% endlatex %} znamená, že se chovají stejně)

{% math definition "plocha" %} kompaktní (uzavřená, omezená), souvislá (např. oblouková -- každé dva body můžu propojit obloukem), {% latex %}2{% endlatex %}-rozměrná varieta bez hranice (dostatečně malé okolí každého bodu je homeomorfní otevřenému okolí v {% latex %}\mathbb{R}^2{% endlatex %}).{% endmath %}
- např. sféra v {% latex %}\mathbb{R}^3{% endlatex %} nebo torus v {% latex %}\mathbb{R}^3{% endlatex %}

Operace s plochami (začínám u sféry, TODO: obrázky):
1. přidání ucha (od hrnku)
	- vyříznu dva kruhy
	- vezmu plášť pálce bez dna a vrchu
	- ohnu a přílepím jej na díry po kruzích
	- (👀) -- teleport, do kterého když vejdeme, tak na druhé straně vyjdeme opačně („otočeně“)
2. přidání křížítka (cross-cupu):
	- (👀) -- teleport, do kterého když vejdeme, tak nás to teleportuje naproti (v rámci toho kruhu)

Pro {% latex %}g \in \left\{0, 1, \ldots\right\}{% endlatex %} nechť {% latex %}\sum_g{% endlatex %} značí plochu zvniklou ze féry přidáním {% latex %}g{% endlatex %} uší, tak říkáme, že {% latex %}\sum g{% endlatex %} je orientovatelná plocha rodu {% latex %}g{% endlatex %}.

Pro {% latex %}g \in \left\{1, 2, \ldots\right\}{% endlatex %} nechť {% latex %}\prod_g{% endlatex %} značí plochu zvniklou ze féry přidáním {% latex %}g{% endlatex %} křížítek, tak říkáme, že {% latex %}\prod g{% endlatex %} je neorientovatelná plocha rodu {% latex %}g{% endlatex %}.

{% math fact %}Každá plocha je homeomorfní právě jedné z posloupností {% latex %}\sum_0, \prod_1, \sum_1, \prod_2,\ldots{% endlatex %} (zde máme skryté tvrzení, že žádné dvě z této posloupností nejsou homeomorfní.{% endmath %}

{% math fact %}Přidám-li ke sféře {% latex %}k \ge 0{% endlatex %} uší a {% latex %}l \ge 1{% endlatex %} křížítek, vznikne neorientovatelná plocha homeomorfní {% latex %}\prod_{2k + l}{% endlatex %} ({% latex %}\approx{% endlatex %} „přidání dvou křížítek je jako přidání ucha,“ **pokud** už tam bylo {% latex %}\ge 1{% endlatex %} křížítko){% endmath %}

- {% latex %}\sum_0 \ldots{% endlatex %} sféra
- {% latex %}\prod_1 \ldots{% endlatex %} projektivní rovina
- {% latex %}\sum_1 \ldots{% endlatex %} torus
- {% latex %}\prod_2 \ldots{% endlatex %} kleinova láhev

TODO: ten cool pohled ze cvik.


### 5. přednáška
{% math definition "nakreslení grafu" %} {% latex %}G = (V, E){% endlatex %} na pllochu {% latex %}\Gamma{% endlatex %} je zobrazení {% latex %}\phi{% endlatex %}t. ž.:
- každému vrcholu $v \in V$ přiřadí bod {% latex %}\phi(v) \in \Gamma{% endlatex %}
- každé hrane $e \in E$ přiřadí prostou (neprotínající se) křivku {% latex %}\phi(e) \in \Gamma{% endlatex %} spojující konce {% latex %}\phi(x), \phi(y){% endlatex %}
- {% latex %}x, y \ni V: x \neq y \implies \phi(x) \neq \phi(y){% endlatex %}
- {% latex %}e, f \in E: e \neq f \implies \phi(e) \cap \phi(f) = \left\{\phi(x) \mid x \in e \cap f\right\}{% endlatex %}
- e \in E, x \in V: x \in e \implies \phi(x) \not\in \phi(e)
{% endmath %}

Tzn. nakreslení, kde se nekříží hrany, atd...

{% math definition "stěna nakreslení" %} je souvislá komponenta {% latex %}\Gamma \setminus \left(\left(\bigcup_{e \in E}^{\phi(e)}\right) \cup \left(\bigcup_{x \in V}^{\phi(x)}\right)\right){% endlatex %}{% endmath %}

{% math definition "buňkové nakreslení" %} je nakreslení, kde každá stěna je homeomorfní otevřenému kruhu v {% latex %}\mathbb{R}^2{% endlatex %}.{% endmath %}

TODO: obrázky toru

{% math reminder %}{% latex %}G = (V, E){% endlatex %} souvislý {% latex %}\implies{% endlatex %} v každém rovinném nakreslení platí {% latex %}|V| - |E| + S = 2{% endlatex %} {% endmath %}
- využíváme faktu, že rovinné nakreslení {% latex %}G{% endlatex %} je buňkové {% latex %}\iff G{% endlatex %} je souvislé

{% math definition "Eulerova charakteristika plochy" %} charakteristika plochy {% latex %}\Gamma{% endlatex %} je

{% latex display %}
\begin{aligned}
\Chi(\Gamma) &= \begin{cases} 2 - g & \Gamma \cong \prod (g \ge 1) \\ 2 - 2g & \Gamma \cong \sum (g \ge 0) \end{cases} \\
\            &= 2 - \text{\# křížítek} - 2 \cdot \text{\# uší}
\end{aligned}
{% endlatex %}
{% endmath %}

{% math theorem "zobecněná Eulerofa formule" %}Nechť máme nakreslení grafu {% latex %}G = (V, E){% endlatex %} na ploše {% latex %}\Gamma{% endlatex %}, které má {% latex %}S{% endlatex %} stěn. Pak {% latex %}|V| - |E| + |S| \ge \Chi(\Gamma).{% endlatex %}{% endmath %} 
- pokud nakreslení je buňkové, tak {% latex %}|V| - |E| + S = \Chi(\Gamma){% endlatex %}

{% math proof "rovnosti" %}idea je indukce podle rodu {% latex %}\Gamma{% endlatex %}
- {% latex %}\Gamma \cong \sum_0{% endlatex %} platí

Mějme nyní buňkové nakreslení {% latex %}G = (V, E){% endlatex %} na {% latex %}\Gamma{% endlatex %}
	- {% latex %}v(G), e(G), s(G){% endlatex %} značíme počet vrcholů, hran a stěn

Nechť {% latex %}K{% endlatex %} je křížítko na {% latex %}\Gamma{% endlatex %}, {% latex %}x_1, \ldots, x_k{% endlatex %} jsou body {% latex %}K{% endlatex %}, kde hrany {% latex %}G{% endlatex %} kříží {% latex %}K{% endlatex %}
- (👀) -- {% latex %}k \ge 1{% endlatex %}, jinak stěna obsahující {% latex %}k{% endlatex %} nebyla buňka -- máme předpoklad, že nakreslení je buňkové)

Vytvoříme {% latex %}G'{% endlatex %} přidáním dvou dělících vrcholů na každou hranu křížící {% latex %}K{% endlatex %} těsně vedle {% latex %}x_1, \ldots, x_k{% endlatex %} („před a za křížítkem“). TODO: obrázek
- děláme to proto, že jedna hrana by mohla procházet křížítkem na více místech a bylo by to pak dost rozbitý
- {% latex %}v(G') = v(G) + 2k{% endlatex %}
- {% latex %}e(G') = e(G) + 2k{% endlatex %}
- {% latex %}s(G') = s(G){% endlatex %}
- {% latex %}L(G') = L(G){% endlatex %}

Vytvoříme {% latex %}G''{% endlatex %} přidaním cest délky {% latex %}2{% endlatex %} k sousedním vrcholům z předchozího kroku. Vznikne tím kružnice {% latex %}C{% endlatex %} obcházející {% latex %}K{% endlatex %}. TODO: obrázek
- {% latex %}v(G'') = v(G') + 2k{% endlatex %}
- {% latex %}e(G'') = e(G') + 4k{% endlatex %}
- {% latex %}s(G'') = s(G') + 2k{% endlatex %} (každou z {% latex %}k{% endlatex %} stěn dělím na {% latex %}3{% endlatex %} kusy)
- {% latex %}L(G'') = L(G'){% endlatex %}

Vytvoříme {% latex %}G'''{% endlatex %} odebráním všeho uvnitř {% latex %}C{% endlatex %}. TODO: obrázek
- {% latex %}v(G''') = v(G''){% endlatex %}
- {% latex %}e(G''') = e(G'') - k{% endlatex %} ({% latex %}k{% endlatex %} křížících-se hran uvnitř {% latex %}C{% endlatex %})
- {% latex %}s(G''') = s(G'') - k + 1{% endlatex %} („spojím“ {% latex %}k{% endlatex %} stěn do jedné)
	- {% latex %}L(G''') = L(G'') + 1{% endlatex %}
- IP: {% latex display %}L(G''') = \Chi(\sum_{g - 1}) = \Chi(\Gamma) + 1 \ldots \Chi(\Gamma) = L(G''') - 1{% endlatex %}

Tedy {% latex %}\Chi(\Gamma) = L(G''') - 1 = L(G'') = L(G') = L(G){% endlatex %}
{% endmath %}

{% math consequence %}Každý graf {% latex %}G{% endlatex %} nakreslitelný na plochu {% latex %}\Gamma{% endlatex %} splní {% latex %}|E| \le 3|V| - 3\Chi(\Gamma){% endlatex %}, pokud {% latex %}|V| \ge 4{% endlatex %}
- každý takový graf má průměrný stupeň {% latex %}\frac{2|E|}{|V|} \le 6 - \frac{6\Chi(\Gamma)}{|V|}{% endlatex %}
	- na žádnou zafixovanou plochu nelze nakreslit libovolně velký {% latex %}7{% endlatex %}-regulární graf
	- pro libovolně velký úplňák dokážeme vytvořit plochu, na kterou ho nakreslíme
{% endmath %}

{% math lemma %}Nechť {% latex %}\Gamma{% endlatex %} je plocha, {% latex %}\Gamma \neq \sum_0{% endlatex %}, nechť {% latex %}G{% endlatex %} je graf nakreslený na {% latex %}\Gamma{% endlatex %}, potom {% latex %}G{% endlatex %} obsahuje vrchol stupně {% latex %}\le \left\lfloor \frac{5 + \sqrt{49 - 24\Chi(\Gamma)}}{2} \right\rfloor{% endlatex %}{% endmath %}

{% math proof %}Mějme {% latex %}G{% endlatex %} podle předpokladu. Opět značíme {% latex %}v(G), e(G){% endlatex %} jako počet vrcholů a hran. ROzlišíme {% latex %}3{% endlatex %} případy:
- {% latex %}\Chi(\Gamma) = 1{% endlatex %} (t.j. {% latex %}\Gamma \cong \prod_1{% endlatex %}), dosazením dostáváme průměrný stupeň {% latex %}< 6{% endlatex %} (dosazením do důsledku){% latex %}\implies \exists{% endlatex %} vrchol stupně {% latex %}\le 5{% endlatex %}, což jsme chtěli
- {% latex %}\Chi(\Gamma) = 0{% endlatex %} (t.j. {% latex %}\Gamma \cong \prod_2{% endlatex %} nebo {% latex %}\Gamma \cong \sum_1{% endlatex %}), průměrný stupeň {% latex %}\le 6 \implies \exists{% endlatex %} vrchol stupně {% latex %}\le 6{% endlatex %}
- {% latex %}\Chi(\Gamma) < 0 \ldots \delta(G) = {% endlatex %} min. stupeň {% latex %}G{% endlatex %}; víme:
	- {% latex %}\delta(G) \le 6 - \frac{6 \Chi(\Gamma)}{v(G)}{% endlatex %}
	- {% latex %}\delta(G) \le v(G) - 1{% endlatex %} (žádný vrchol nemá víc než {% latex %}v(G) - 1{% endlatex %} sousedů)
	- chceme zjistit max. hodnotu {% latex %}\delta{% endlatex %}, což je řešení dvou rovnic výše; dosazením a vyřešením kvadratické rovnice vyjde přesně to, co dokazujeme

TODO: grafík
{% endmath %}

{% math consequence "Heawoodova formule, 1890" %} Pokud {% latex %}\Gamma \not\cong \sum_0{% endlatex %}, tak každý graf nakreslitelny na {% latex %}\Gamma{% endlatex %} je nejvýš {% latex %}H(\Gamma) = \left\lfloor \frac{7 + \sqrt{49 - 24 \Chi(\Gamma)}}{2} \right\rfloor{% endlatex %}-obarvitelný{% endmath %}
- platí i pro stéru: věta o {% latex %}4{% endlatex %}-barvách
- tento odhad je těsný pro všechny plochy kromě {% latex %}\prod_2{% endlatex %}, dokonce: na každou plochu {% latex %}\Gamma \not\cong \prod_2{% endlatex %} lze kreslit kliku velikosti {% latex %}H(\Gamma){% endlatex %}
	- (každý graf nakreslitelný na {% latex %}\prod_2{% endlatex %} je dokonce {% latex %}6{% endlatex %}-obarvitelný)

### 6. přednáška

#### Vrcholové barvení
- {% latex %}\chi(G) = \text{barevnost } G = {% endlatex %} nejmenší počet barev, kterými lze (dobře) obarvit {% latex %}G{% endlatex %}
- {% latex %}\Delta(G) = \text{max. stupeň } G = {% endlatex %}, {% latex %}\delta(G) = \text{min. stupeň } G{% endlatex %}

{% math reminder %}{% latex %}G{% endlatex %} je {% latex %}d{% endlatex %}-degenerovaný {% latex %}\equiv{% endlatex %} každý podgraf {% latex %}H{% endlatex %} grafu {% latex %}G{% endlatex %} má {% latex %}\delta(H) \le d{% endlatex %} \iff {% latex %}\exists{% endlatex %} pořadí vrcholů {% latex %}v_1, \ldots v_n{% endlatex %} t. ž. {% latex %}\forall i: G - \left\{v_1, \ldots, v_i\right\} : \delta(G_i) \le d{% endlatex %} a {% latex %}v_{i - 1}{% endlatex %} má {% latex %}\le d{% endlatex %} sousedů v {% latex %}G_i{% endlatex %}{% endmath %}

{% math observation %}{% latex %}G{% endlatex %} je {% latex %}d{% endlatex %}-degenerovnaý {% latex %}\implies \Chi(G) \le d + 1{% endlatex %}, TODO: obrázek, že vrcholy vidí dopředu{% endmath %}
- z minule: pokud {% latex %}G{% endlatex %} je nakreslitelný na {% latex %}\Gamma \implies G{% endlatex %} má vrchol stupně {% latex %}H(\Gamma) - 1{% endlatex %} a {% latex %}G - v{% endlatex %} je stále nakreslitelný na {% latex %}\Gamma \implies G{% endlatex %} je {% latex %}\left(H(\Gamma) - 1\right){% endlatex %}-degenerovaný {% latex %}\implies{% endlatex %} je {% latex %}H(\Gamma){% endlatex %} obarvitelný

{% math observation %}{% latex %}G{% endlatex %} je {% latex %}\Delta(G){% endlatex %}-degenerovaný (triviálně) {% latex %}\implies \Chi(G) \le \Delta(G) + 1{% endlatex %} (pozorování výše){% endmath %}

{% math question %}Pro které gravy platí {% latex %}\Chi(G) = \Delta(G) + 1{% endlatex %}?{% endmath %}
- úplné grafy
- liché cykly, protože se mi to u jednoho vrcholu srazí

{% math lemma %}{% latex %}G{% endlatex %} souvislý graf a {% latex %}\delta(G) \le \Delta(G){% endlatex %} (neboli {% latex %}\exists{% endlatex %} vrchol stupně {% latex %}<\Delta(G) \implies Chi(G) \le \Delta(G){% endlatex %}{% endmath %}
- když nás zajímá předchozí otázka, tak se stačí zaměřit na nějaký regulární graf

{% math proof %}Tvrdím, že {% latex %}G{% endlatex %} je ({% latex %}\Delta(G) - 1{% endlatex %})-degenerovaný. Volme {% latex %}H{% endlatex %} neprázdný podgraf {% latex %}G{% endlatex %}.
- pokud {% latex %}H{% endlatex %} má všechny vrcholy {% latex %}\implies{% endlatex %} platí z předpokladu.
- jinak {% latex %}\exists e = \left\{x, y\right\} \in G{% endlatex %} t. ž. {% latex %}x \in H{% endlatex %} a {% latex %}y \not\in H{% endlatex %} (TODO obrázek)
	- {% latex %}\mathrm{deg}_H(x) \le \mathrm{deg}_G(x) - 1 \le \Delta(G) - 1{% endlatex %}
{% endmath %}

{% math theorem "Brooks, 1941" %}Nechť {% latex %}G{% endlatex %} je souvislý graf který není úplný a není lichá kružnice. Pak je {% latex %}G \le \Delta(G){% endlatex %}-obarvitelný.{% endmath %}

{% math proof %}nechť {% latex %}\Chi = \Chi(G), \Delta = \Delta(G){% endlatex %} a navíc předpokládám, že {% latex %}G{% endlatex %} je {% latex %}\Delta{% endlatex %}-regulární (jinak viz. předchozí lemma.

- {% latex %}\Delta \le 2 \implies \Chi \le \Delta{% endlatex %}
	- {% latex %}K_2{% endlatex %} -- zakázané
	- {% latex %}C_{2k}{% endlatex %} -- {% latex %}\Chi = 2{% endlatex %}
	- {% latex %}C_{2k + 1}{% endlatex %} -- zakázané
- {% latex %}\Delta \ge 3{% endlatex %}; označme {% latex %}k_V(G) = {% endlatex %} vrcholová souvislost {% latex %}G{% endlatex %}
	- {% latex %}k_V(G) = 1{% endlatex %} -- máme artikulaci, vrchol artikulace {% latex %}v{% endlatex %} měl souseda v obou částech grafu, proto {% latex %}\mathrm{deg}_{G_1}(v), \mathrm{deg}_{G_2}(V) < \Delta \implies{% endlatex %} podle lemmatu lze {% latex %}G_1{% endlatex %} i {% latex %}G_2{% endlatex %} {% latex %}\Delta{% endlatex %}-obarvit a stačí přepermutovat barvy, aby měl v obou obarveních stejnou barvu, pak slepím, TODO: obrázek
	- {% latex %}k_V(G) = 2{% endlatex %} -- TODO: obrázek
		- dobré případy (lze slepit)
			- {% latex %}b_1(x) = b_1(y){% endlatex %} a {% latex %}b_2(x) = b_2(y){% endlatex %} 
			- {% latex %}b_1(x) \neq b_1(y){% endlatex %} a {% latex %}b_2(x) \neq b_2(y){% endlatex %} 
		- těžší případ -- na jedné straně stejné, na druhé různé
			- {% latex %}b_1(x) = b_1(y){% endlatex %} a {% latex %}b_2(x) \neq b_2(y){% endlatex %} 
				a) pokud {% latex %}\mathrm{deg}_{G_1}(x){% endlatex %} nebo {% latex %}\mathrm{deg}_{G_1}(y) \le \Delta - 2{% endlatex %}, tak po přidání hrany půjde použít lemma a vrcholy budou mít různou barvu a máme dobrý případ
				b) {% latex %}\mathrm{deg}_{G_1}(x) = \mathrm{deg}_{G_1}(y) = \Delta - 1{% endlatex %} (TODO: obrázek)
					- {% latex %}\implies \mathrm{deg}_{G_2}(x) = \mathrm{deg}_{G_2}(y) = 1{% endlatex %}; z předpokladu máme k použití alespoň {% latex %}3{% endlatex %} barvy, přebarvím jimi {% latex %}x{% endlatex %} a {% latex %}y{% endlatex %} a máme dobrý případ (TODO: obrázek)
	- {% latex %}k_V(G) \ge 3{% endlatex %} -- použiji lemma o třešničce: souvislý graf, který není klika, obsahuje třešničku (obrázek)
		- TODO: obrázek kostry a intuice
		- seřadím vrcholy jako {% latex %}\underbrace{v_1}_{x}, \underbrace{v_2}_{y}, \ldots, \underbrace{v_n}_{z}{% endlatex %} tak, aby {% latex %}\forall v_i: 3 \le i \le n - 1{% endlatex %} měl alespoň jednoho souseda napravo (BFS vrstvy podle vzdáleností od {% latex %}z{% endlatex %} a barvím:
			- {% latex %}b(x) = b(y) = 1{% endlatex %}
			- {% latex %}b(v_3)\ldots{% endlatex %} má {% latex %}\ge 1{% endlatex %} neobarveného souseda {% latex %}\implies{% endlatex %} je nějaká nepoužitá z celkových {% latex %}\Delta{% endlatex %} barev
			- {% latex %}\ldots{% endlatex %}
			- {% latex %}b(v_n)\ldots{% endlatex %} všichni sousedé už obarvení, ale dva ({% latex %}x, y{% endlatex %}) mají stejnou barvu, tedy {% latex %}v_n{% endlatex %} vidí {% latex %}\le 1{% endlatex %} barev a jedna je volná
{% endmath %}

#### Pár poznámek

**Harwigerova domněnka:** {% latex %}K_t \not\preceq_m G \implies \Chi(G) < t{% endlatex %}
	- {% latex %}t = 5 \ldots{% endlatex %} zobecnění věty o {% latex %}4{% endlatex %} barvách
	- {% latex %}t = 4 \ldots{% endlatex %} jednoduché
	- {% latex %}t = 6 \ldots{% endlatex %} pomocí věty o {% latex %}4{% endlatex %} barvách + dost práce
	- {% latex %}t \ge 7 \ldots{% endlatex %} neví se

{% math claim %}{% latex %}G{% endlatex %} nakreslitelný na Kleinovu láhev {% latex %}\implies G{% endlatex %} je {% latex %}6{% endlatex %}-obarvitelný.{% endmath %}

{% math proof %}Z Eulerovy formule plyne, že buď {% latex %}\gamma(G){% endlatex %} \le 5 \implies \exists v: \mathrm{deg}(v) \le 5{% endmath %}
- {% latex %}G - v \ldots{% endlatex %}  obarvím z indukce, přidám {% latex %}v{% endlatex %} a mám volnou barvu
- {% latex %}G{% endlatex %} je {% latex %}6{% endlatex %}-regulární:
	- {% latex %}G \cong K_7{% endlatex %} -- nesmí, protože nejde nakreslit
	- {% latex %}G \not\cong K_7{% endlatex %} -- Brooksova věta

#### Hranové obarvení
{% math definition %}b: E \mapsto B{% endmath %} (barvy) t. ž. {% latex %}\forall e \neq f \in E, e \cap f \neq \emptyset \implies b(e) \neq b(f). Hranová barevnost {% latex %}G{% endlatex %} ("chromatic index") {% latex %}\Chi'(G){% endlatex %} je min. počet barev, který nám stačí pro hranové barvení {% latex %}G{% endlatex %}.{% endlatex %}

TODO: obrázek na příklad

{% math observation %}\Delta(G) \le \Chi'(G) \le 2 \Delta(G){% endmath %}
- první triviální (jinak se mi ve vrcholu srazí hrany)
- druhé přes line graph (TODO: obrázek)

{% math theorem "Vizing, 1964" %}Pro každý graf {% latex %}G{% endlatex %} platí, že {% latex %}\Delta \le \Chi'(G) \le \Delta + 1{% endlatex %}{% endmath %}
- grafy Vizingovy třídy {% latex %}1{% endlatex %} jsou grafy s {% latex %}\Chi'(G) = \Delta{% endlatex %}, s {% latex %}2{% endlatex %} jsou {% latex %}\Chi'(G) = \Delta + 1{% endlatex %}
- je NP-úplné rozhodnout, zda daný graf {% latex %}G{% endlatex %} má VIzingovu třídu {% latex %}1{% endlatex %} (i pro grafy s {% latex %}\Delta(G) = 3{% endlatex %})

### Zdroje/materiály
- [Stránky přednášky](https://research.koutecky.name/db/teaching:kg22021_prednaska).
- [Poznámky Václava Končického](https://kam.mff.cuni.cz/~koncicky/notes/kag2/pdf) z roku 2019.
