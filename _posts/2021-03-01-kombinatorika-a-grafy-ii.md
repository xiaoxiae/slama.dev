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

- **maximální** (do inkluze) -- přidání další hrany pro dané párování už není možné; v přednášce nás nezajímá
- **největší** -- {% latex %}\mathrm{max}(|M|){% endlatex %}

{% math definition "volný vrchol" %} (vzhledem k {% latex %}M{% endlatex %}) -- vrchol, kterého se nedotýká žádná hrana párování.{% endmath %}

{% math definition "střídavá cesta" %} (vzdledem k {% latex %}M{% endlatex %}) -- cesta, na které se střídají hrany v párování a hrany mimo párování: {% latex %}u_0, \ldots, u_k{% endlatex %}, kde každá sudá/lichá hrana je v {% latex %}M{% endlatex %}, lichá/sudá není v {% latex %}M{% endlatex %}{% endmath %}

- **volná** střídavá cesta (VSC) -- krajní vrcholy jsou volné (vůči párování)
- {% latex %}\implies{% endlatex %} obsahuje lichý počet hran, sudý počet vrcholů

{% math lemma %}Nechť {% latex %}G = \left(V, E\right){% endlatex %} je graf, {% latex %}M{% endlatex %} párování v {% latex %}G{% endlatex %}. Pak {% latex %}G{% endlatex %} obsahuje VSC (vzhledem k {% latex %}M{% endlatex %}), právě když {% latex %}M{% endlatex %} není největší párování v {% latex %}G{% endlatex %}.{% endmath %}

{:.rightFloatBox}
<div markdown="1">
{:.center}
![](/assets/kombinatorika-a-grafy-ii/alter.svg)
</div>
- {% latex %}\Rightarrow{% endlatex %} pokud {% latex %}M{% endlatex %} má VSC, mohu {% latex %}M{% endlatex %} zvětšit prohozením hran

- {% latex %}\Leftarrow{% endlatex %} pro spor nechť {% latex %}M'{% endlatex %} je párování v {% latex %}G{% endlatex %} t. ž {% latex %}|M'| \ge |M|{% endlatex %}
	- uvažme {% latex %}H = \left(V, M \cup M'\right){% endlatex %}; pak má každý vrchol stupeň {% latex %}0, 1{% endlatex %} nebo {% latex %}2{% endlatex %} {% latex %}\implies{% endlatex %} komponenty souvislosti jsou kružnice sudé délky a cesty (navíc jsou střídavé)
	- (👀) -- musí existovat komponenta, která má více hran z {% latex %}M'{% endlatex %} (je větší)
		- není to kružnice (musela by být lichá a měli bychom máme kolizi ve vrcholu)
		- je to volná (z definice, vzhledem k {% latex %}M{% endlatex %}) střídavá (jinak by měly stejný počet hran) cesta

{% math definition "květ" %} lichá „střídavá“ kružnice s vrcholem {% latex %}v_1{% endlatex %}, ke kterému přiléhají dvě hrany {% latex %}\not\in M{% endlatex %}{% endmath %}
{% math definition "stonek" %} střídavá cesta z {% latex %}v_1{% endlatex %} (i nulové) délky končící volným vrcholem (dál od květu){% endmath %}
- {% latex %}v_1{% endlatex %} může (a nemusí) být volný vrchol -- stačí, aby byl volný vzhledem ke květu

{% math definition "kytka" %} květ + stonek{% endmath %}

{:.center}
![](/assets/kombinatorika-a-grafy-ii/kytka.svg)

{% math definition "kontrakce hrany" %} Nechť {% latex %}G = \left(V, E\right){% endlatex %} je neorientovaný graf a {% latex %}e = \left\{u, v\right\}{% endlatex %} jeho hrana. Zápis {% latex %}G . e{% endlatex %} označuje graf vzniklý z {% latex %}G{% endlatex %} kontrakcí („smrštěním“) hrany {% latex %}e{% endlatex %} do jednoho vrcholu:{% endmath %}

{:.center}
![](/assets/kombinatorika-a-grafy-ii/kontrakce.svg)

{% math lemma %}Nechť {% latex %}C{% endlatex %} je květ v grafu {% latex %}G{% endlatex %}. Potom párování {% latex %}M{% endlatex %} v {% latex %}G{% endlatex %} je maximální, právě když {% latex %}M \setminus E(C){% endlatex %} je maximální párování v grafu {% latex %}G . C{% endlatex %}, tj. s květem {% latex %}C{% endlatex %} zkontrahovaným do jediného vrcholu. Navíc pokud znám VSC pro {% latex %}M . C{% endlatex %}, tak v poly. čase najdu VSC pro {% latex %}M{% endlatex %} v {% latex %}G{% endlatex %}.{% endmath %}

{% math proof %}Tady je [http://www.cs.dartmouth.edu/~ac/Teach/CS105-Winter05/Handouts/tarjan-blossom.pdf](sketchy důkaz), tady je [míň sketchy důkaz](https://stanford.edu/~rezab/classes/cme323/S16/projects_reports/shoemaker_vare.pdf).
{% endmath %}

{% math algorithm "Edmondsův „zahradní/blossom“" %} vstupem je graf {% latex %}G{% endlatex %} a jeho libovolné párování {% latex %}M{% endlatex %}, třeba prázdné. Výstupem je párování {% latex %}M'{% endlatex %}, které je alespoň o {% latex %}1{% endlatex %} větší, než {% latex %}M{% endlatex %}, případně {% latex %}M{% endlatex %} pokud bylo maximální.{% endmath %}

- zkonstruujeme maximální možný **Edmondsův les** vzhledem k aktuálnímu {% latex %}M{% endlatex %} tím, že z volných vrcolů pustíme BFS a střídavě přidáváme vrcholy
	- hranám, které se v lese neobjeví, se říká kompost a nebudou pro nás důležité

{:.center}
![](/assets/kombinatorika-a-grafy-ii/les.svg)

- pokud existuje hrana mezi (potenciálně různými) sudými hladinami různých stromů, pak máme volnou střídavou cestu, kterou zalterujeme a jsme hotovi (párování je o {% latex %}1{% endlatex %} větší)
- pokud existuje hrana mezi (potenciálně různými) sudými hladinami jednoho stromu, máme květ {% latex %}C{% endlatex %} -- ten zkontrahujeme a rekurzivně se zavoláme
	- vrátí-li {% latex %}M' = M{% endlatex %}, pak nic dalšího neděláme
	- vratí-li nějaké větší párování, tak z něho zkonstruujeme párování v {% latex %}G{% endlatex %}
- neexistuje-li hrana mezi sudými hladinami, pak {% latex %}M' = M{% endlatex %}

{% math lemma %}Edmondsův algoritmus spuštěný na {% latex %}G{% endlatex %} a {% latex %}M{% endlatex %} doběhne v čase {% latex %}\mathcal{O}(n \cdot (n + m)){% endlatex %} a najde párování {% latex %}M'{% endlatex %} alespoň o {% latex %}1{% endlatex %} hranu větší než {% latex %}M{% endlatex %}, případně oznámí, že {% latex %}M{% endlatex %} je největší {% latex %}\implies{% endlatex %} nejlepší párování lze nalézt v čase {% latex %}\mathcal{O}(n^2 (n + m)){% endlatex %}.{% endmath %}

### 2. přednáška

{% math definition "perfektní párování" %}Párování {% latex %}M{% endlatex %} je perfektní, pokud neexistuje v {% latex %}G{% endlatex %} žádný volný vrchol.{% endmath %}

#### Tutteova věta
{% math definition "Tutteova podmínka" %} {% latex %}\forall S \subseteq V: \mathrm{odd}(G - S) \le |S|{% endlatex %}
- {% latex %}\mathrm{odd}{% endlatex %} je počet lichých komponent grafu{% endmath %}.

{% math theorem "Tutteova věta" %} {% latex %}G{% endlatex %} má perfektní párování {% latex %}\iff{% endlatex %} platí Tutteova podmínka.{% endmath %}

{% math proof %}
{% latex %}\Rightarrow{% endlatex %} obměna: neplatí TP {% latex %}\implies{% endlatex %} není PP. Nechť {% latex %}\exists S \subseteq V{% endlatex %} t. ž. {% latex %}\mathrm{odd(G - S)} > |S|{% endlatex %}. V perfektním párování se alespoň {% latex %}1{% endlatex %} vrchol z každé liché komponenty musí spárovat s nějakým z {% latex %}S{% endlatex %}, ale těch není dostatek.

{% latex %}\Leftarrow{% endlatex %} nechť {% latex %}G{% endlatex %} splňuje Tutteovu podmínku. {% latex %}|V|{% endlatex %} je sudá (nastavíme {% latex %}S{% endlatex %} prázdnou). Dokážeme, že {% latex %}G{% endlatex %} má PP indukcí podle počtu nehran.

- **základ:** {% latex %}G = K_{2n}{% endlatex %}, ten PP má
- **indukční podmínka:** {% latex %}G{% endlatex %} má nehranu a každý graf na {% latex %}V{% endlatex %}s počtem hran alespoň o 1 větší než {% latex %}|E|{% endlatex %} a platí TP, pak má perfektní párování

Nechť {% latex %}S = \left\{v \in V\ |\ \deg(v) = n - 1\right\} = \left\{v \mid \text{$v$ je spojený se všemi vrcholy} \right\}{% endlatex %}
- lehký případ: každá lichá komponenta {% latex %}G - S{% endlatex %} je klika
	- v rámci dané kliky vypáruji vše až na jeden vrchol, ten spáruji v rámci {% latex %}S{% endlatex %} ({% latex %}S{% endlatex %} vidí všechny) a zbytek v {% latex %}S{% endlatex %} spáruji spolu (sudé komponenty do parity nepřispívají, liché + {% latex %}1{% endlatex %} z {% latex %}S{% endlatex %} také ne a v {% latex %}S{% endlatex %} tedy zbyde sudý počet vrcholů)

{:.center}
![](/assets/kombinatorika-a-grafy-ii/1.svg)

- alespoň {% latex %}1{% endlatex %} komponenta {% latex %}K{% endlatex %} není klika, tedy {% latex %}\exists x, y{% endlatex %} nesousedi
	- ti mají společného souseda {% latex %}u{% endlatex %} (tvrzení o třešničce), který není v {% latex %}S{% endlatex %}
	- pro {% latex %}u{% endlatex %} existuje vrchol {% latex %}v{% endlatex %}, se kterým **není** spojený (jinak by {% latex %}u{% endlatex %} byl v {% latex %}S{% endlatex %}, což ale víme že není)


{:.center}
![](/assets/kombinatorika-a-grafy-ii/2.svg)

- (👀) -- přidáním hrany do grafu se neporuší TP ({% latex %}\forall S \subseteq V{% endlatex %} počet lichých komponent {% latex %}G - S{% endlatex %} buď klesne o {% latex %}2{% endlatex %} nebo zůstane stejný).

Indukujeme dvakrát: {% latex %}G_1 = G + e_1{% endlatex %} a {% latex %}G_2 = G + e_2{% endlatex %} díky předchozímu pozorování splňují TP a spolu s IP {% latex %}\implies \exists{% endlatex %} PP {% latex %}M_1, M_2{% endlatex %} v {% latex %}G_1, G_2{% endlatex %}
- jednoduchý případ: {% latex %}e_1 \not\in M_1 \implies M_1{% endlatex %} je PP pro {% latex %}G{% endlatex %}, analogicky pro {% latex %}e_2{% endlatex %} a {% latex %}M_2{% endlatex %}

Těžší případ: {% latex %}e_1 \in M_1, e_2 \in M_2, H = (V, M_1 \cup M_2){% endlatex %}
- {% latex %}H {% endlatex %} obsahuje **„dvoubarevné hrany“** {% latex %}e \in M_1 \cap M_2{% endlatex %} nebo **střídavé sudé cykly**
- {% latex %}H {% endlatex %} neobsahuje **izolované vrcholy** a **střídavé cesty,** protože {% latex %}M_1, M_2{% endlatex %} byly perfektní

{:.center}
![](/assets/kombinatorika-a-grafy-ii/3.svg)

- jednodušší případ těžšího případu: {% latex %}e_1{% endlatex %} leží v jiné komponentě {% latex %}H{% endlatex %} než {% latex %}e_2{% endlatex %} -- stačí přealternovat hrany tak, aby ani {% latex %}e_1{% endlatex %} ani {% latex %}e_2{% endlatex %} v {% latex %}H{% endlatex %} neležely.

{:.center}
![](/assets/kombinatorika-a-grafy-ii/4.svg)

- složitější případ těžšího případu: {% latex %}e_1{% endlatex %} a {% latex %}e_2{% endlatex %} leží ve stejné komponentě -- vybereme podle obrázku

{:.center}
![](/assets/kombinatorika-a-grafy-ii/5.svg)

{% endmath %}

{% math theorem "Petersen" %} každý {% latex %}3{% endlatex %}-regulární {% latex %}2{% endlatex %}-souvislý (vrcholově i hranově, pro 2-souvislost je to to samé; alternativně můžeme říct graf bez mostů a artikulací) graf má PP.{% endmath %}

{% math proof %}Nechť {% latex %}G = (V, E){% endlatex %} je {% latex %}3{% endlatex %}-regulární a {% latex %}2{% endlatex %}-souvislý. Chci ukázat, že {% latex %}G{% endlatex %} splňuje TP. Předpokládejme danou {% latex %}S \subseteq V{% endlatex %}.

1. každá komponenta {% latex %}G - S{% endlatex %} je v {% latex %}G{% endlatex %} spojena aspoň dvěma hranami s {% latex %}S{% endlatex %}
	- je {% latex %}2{% endlatex %}-souvislý, nemáme mosty

2. dokážeme, že každá lichá komponenta {% latex %}G - S{% endlatex %} je s {% latex %}S{% endlatex %} spojena lichým počtem hran:
	- nechť {% latex %}L{% endlatex %} je lichá komponenta {% latex %}G - S{% endlatex %}; pak:
{% latex display %}\sum_{x \in V(L)}\deg_G(x) \overset{3-\text{reg.}}{=} \underbrace{3|V(L)|}_{\text{liché číslo}} = \underbrace{2 (\text{\# hran vedoucích uvnitř $L$})}_{\text{sudé číslo}} + \underbrace{1 (\text{\# hran vedoucích uvnitř $L$})}_{\text{musí být liché}}{% endlatex %}

- kombinace (1) a (2) říká, že každá lichá komponenta {% latex %}G - S{% endlatex %} je s {% latex %}S{% endlatex %} spojena {% latex %}\ge 3{% endlatex %} hranami:
	- {% latex %}p = {% endlatex %} počet hran mezi {% latex %}S{% endlatex %} a lichými komponentami {% latex %}G - S{% endlatex %}
		- {% latex %}p \ge 3 \cdot \mathrm{odd(G - S)}{% endlatex %} (ukázali jsme výše)
		- {% latex %}p \le 3 \cdot |S|{% endlatex %} (každý vrchol {% latex %}S{% endlatex %} vysílá ven {% latex %}\le 3{% endlatex %} hrany (z {% latex %}3{% endlatex %}-regularity))

{:.center}
![](/assets/kombinatorika-a-grafy-ii/6.svg)

{% latex %}|S| \ge \mathrm{odd}(G - S){% endlatex %}, tedy TP platí a graf má perfektní párování.

{% endmath %}

### 3. přednáška


#### Tutte v2.0

{% math lemma "o kontrahovatelné hraně" %} Nechť {% latex %}G{% endlatex %} je vrcholově {% latex %}3{% endlatex %}-souvislý různý od {% latex %}K_4{% endlatex %} ({% latex %}|V| \ge 5{% endlatex %}). Potom {% latex %}G{% endlatex %} obsahuje hranu t. ž. {% latex %}G \setminus e{% endlatex %} je 3-souvislý.{% endmath %}

{% math proof %}Sporem -- nechť {% latex %}G{% endlatex %} je 3-souvislý ale neexistuje žádná hrana, která jde zkontrahovat. Tedy {% latex %}\forall e \in E: G \setminus e{% endlatex %} není {% latex %}3{% endlatex %}-souvislý.

{% math lemma "pomocné" %} {% latex %}\forall e = \left\{x, y\right\} \exists z_e \in V \setminus \left\{x, y\right\}{% endlatex %} t. ž. {% latex %}\left\{x, y, z_e\right\}{% endlatex %} tvoří vrcholový řez v G, navíc každý z {% latex %}\left\{x, y, z_e\right\}{% endlatex %} má alespoň jednoho souseda v každé komponentě {% latex %}G \setminus \left\{x, y, z_e\right\}{% endlatex %}.{% endmath %}
- přesně popisuje situaci, že kontrakce libovolné hrany nám dá řez velikosti {% latex %}2{% endlatex %}
- ve skutečnosti **neplatí** (ale dovětek ano) a dokazujeme ho pouze v rámci sporu!
- (👀 které platí) {% latex %}S{% endlatex %} minimální vrcholový řez {% latex %}G{% endlatex %}, pak každý vrchol {% latex %}S{% endlatex %} má souseda v každé komponentě {% latex %}G \setminus S{% endlatex %} -- když to pro nějaký {% latex %}v{% endlatex %} neplatí, tak {% latex %}S \setminus v{% endlatex %} je pořád řez

{% xopp 1 %}

{% math proof %}
Vím, že {% latex %}G \setminus e{% endlatex %} není {% latex %}3{% endlatex %}-souvislý, tedy má vrcholový řez velikosti {% latex %}2{% endlatex %}. Nechť {% latex %}v_e{% endlatex %} je vrchol vzniklý kontrakcí {% latex %}e = \left\{x, y\right\}{% endlatex %}. Řez velikosti {% latex %}2{% endlatex %} obsahuje {% latex %}v_e{% endlatex %}, jinak by to byl řez už pro {% latex %}G{% endlatex %} (obsahoval by vrcholy z původního grafu, které nekontrahujeme).

Označme řez {% latex %}v_e, z_e{% endlatex %}. Po rozkontrahování vidíme, že {% latex %}\forall \left\{x, y, z_e\right\}{% endlatex %} musí mít souseda v každé komponentě (jinak spor s 3-souvislostí). Tedy {% latex %}z_e{% endlatex %} je hledaný vrchol.
{% endmath %}

{% xopp 2 %}

Pro důkaz původního lemmatu si zvolím {% latex %}e = \left\{x, y \right\} \in E{% endlatex %} a {% latex %}z_e{% endlatex %} z pomocného tvrzení tak, aby nejmenší komponenta {% latex %}G - z, y, z_e{% endlatex %} byla co nejmenší (co do počtu vrcholů).

Protože {% latex %}z_e{% endlatex %} má souseda ve všech komponentách, má nějakého souseda {% latex %}u \in C, f = \left\{z_e, u\right\}{% endlatex %} (kde {% latex %}C{% endlatex %} je naše nejmenší komponenta). Pomocné tvrzení pro {% latex %}f{% endlatex %} dá nějaký {% latex %}z_f \in V{% endlatex %} t. ž. {% latex %}\left\{z_e, z_f, u\right\}{% endlatex %} je vrcholový řez {% latex %}G{% endlatex %}. Chceme dokázat, že {% latex %}G - z_e, z_f, u{% endlatex %} má menší komponentu než {% latex %}C{% endlatex %}.

{% xopp 3 %}

Nechť {% latex %}D{% endlatex %} je komponenta {% latex %}G - z_e, z_f, u{% endlatex %} neobsahující {% latex %}x, y{% endlatex %}. Existuje, protože {% latex %}x, y{% endlatex %} jsou spojené a graf se rozpadne alespoň na {% latex %}2{% endlatex %} komponenty). Tvrdím, že {% latex %}D \subseteq C \setminus \left\{u\right\}{% endlatex %}, protože {% latex %}D{% endlatex %} nemůže obsahovat {% latex %}z_e, z_f, u{% endlatex %} (vrcholy řezu), {% latex %}x, y{% endlatex %} (z definice {% latex %}D{% endlatex %}), ale {% latex %}u{% endlatex %} má nějakého souseda v {% latex %}D{% endlatex %} (podle pomocného tvrzení), takže v {% latex %}D{% endlatex %} ještě něco zbyde. Navíc ho tam mělo {% latex %}u{% endlatex %} i předtím, takže opravdu {% latex %}D \subseteq C \setminus \left\{u\right\}{% endlatex %}. Tedy {% latex %}|D| < |C|{% endlatex %}, což je spor s minimalitou.
{% endmath %}

- netvrdím, že {% latex %}D{% endlatex %} je nejmenší!

{% math theorem "Tutteova charakterizace 3-souvislých grafů" %} Graf {% latex %}G{% endlatex %} je 3-souvislý {% latex %}\iff{% endlatex %} existuje posloupnost {% latex %}K_4 \cong G_0 \cong G_1 \cong \ldots \cong G{% endlatex %} t. ž. {% latex %}\forall i \in [n], G_{i - 1}{% endlatex %} vznikne z {% latex %}G_i{% endlatex %} kontrakcí hrany, navíc {% latex %}G_i{% endlatex %} má všechny vrcholy stupně {% latex %}\ge 3{% endlatex %}.{% endmath %}

{% math proof %} {% latex %}\Rightarrow{% endlatex %} Induktivní aplikace lemmatu o kontrahovatelné hraně.

{% latex %}\Leftarrow{% endlatex %} Mějme {% latex %}G_0, \ldots, G_n{% endlatex %} dle předpokladu. Chceme, že {% latex %}G_n \cong G{% endlatex %} je 3-souvislý. Indukcí:
- {% latex %}K_4{% endlatex %} je 3-souvislý
- {% latex %}G_{i - 1}{% endlatex %} je 3-souvislý {% latex %}\implies G_i{% endlatex %} je 3-souvislý

{:.rightFloatBox}
<div markdown="1">
{% xopp 4 %}
</div>
Obměnou nechť {% latex %}G_i{% endlatex %} má vrcholový řez velikosti 2, označme ho {% latex %}R = \left\{x,y\right\}{% endlatex %}. Pak každá komponenta {% latex %}G_i - R{% endlatex %} má alespoň 2 vrcholy (osamocený vrchol {% latex %}z{% endlatex %} mohl sousedit jen s řezem, ale ten je velikosti 2, což je spor se stupněm vrcholů {% latex %}\ge 3{% endlatex %} pro {% latex %}v{% endlatex %}).

Pak ale {% latex %}G_{i - 1}{% endlatex %} nebyl 3-souvislý, rozborem toho, kde vznikla hrana:
- {% latex %}e = \left\{x, y\right\} \implies G_{i - 1}{% endlatex %} má řez velikosti 1.
- {% latex %}e{% endlatex %} celá obsažená v komponentě {% latex %}\implies \left\{x, y\right\}{% endlatex %} je stále řez v {% latex %}G_{i - 1}{% endlatex %}
- {% latex %}e = \left\{z, y\right\}{% endlatex %} pro {% latex %}z{% endlatex %} z nějaké komponenty {% latex %}\implies \left\{zy, x\right\}{% endlatex %} je řez v {% latex %}G_{i - 1}{% endlatex %}
	- využíváme předchozí pozorování, že každá komponenta má alespoň {% latex %}2{% endlatex %} vrcholy -- kdyby ne, tak {% latex %}\left\{zy, x\right\}{% endlatex %} nemusí nic odříznout, pokud tam byla jednovrcholová komponenta
{% endmath %}

#### Minory

{% math definition "minor" %} Nechť {% latex %}H, G{% endlatex %} jsou grafy. Pak {% latex %}H{% endlatex %} je minor {% latex %}G{% endlatex %} (nebo že {% latex %}G {% endlatex %} obsahuje {% latex %}H{% endlatex %} jako minor), značíme {% latex %}H \preceq G{% endlatex %}, pokud {% latex %}H{% endlatex %} lze získat z {% latex %}G{% endlatex %} posloupností mazání vrcholů, mazání hran nebo kontrakcí hran.{% endmath %}

- (👀) {% latex %}\preceq{% endlatex %} je transitivní (prostě spojím posloupnosti operací)
- (👀) {% latex %}H{% endlatex %} podgraf {% latex %}G \implies H{% endlatex %} minor {% latex %}G{% endlatex %}
	- podgraf vzniká přesně mazáním vrcholů a mazáním hran
- (👀, spíš fakt) {% latex %}G{% endlatex %} rovinný {% latex %}\implies{% endlatex %} jeho minory jsou také rovinné
	- pro podgraf očividné, je jen potřeba si rozmyslet kontrakci (že nic topologicky nerozbije)

{% math theorem "Kuratowského" %} {% latex %}G{% endlatex %} rovinný {% latex %}\iff{% endlatex %} neobsahuje dělení {% latex %}K_5{% endlatex %} ani {% latex %}K_{3, 3}{% endlatex %}{% endmath %}

{% math theorem "Kuratowski 1930, Warner 1937" %} Následující jsou ekvivalentní:{% endmath %}
1. {% latex %}G{% endlatex %} je rovinný
2. {% latex %}G{% endlatex %} neobsahuje dělení {% latex %}K_5{% endlatex %} ani {% latex %}K_{3, 3}{% endlatex %} jako podgraf
3. {% latex %}G{% endlatex %} neobsahuje dělení {% latex %}K_5{% endlatex %} ani {% latex %}K_{3, 3}{% endlatex %} jako minor.

{% math proof %} {% latex %}\\{% endlatex %}
- *{% latex %}1 \implies 2{% endlatex %}: z prváku, protože {% latex %}K_5{% endlatex %} ani {% latex %}K_{3, 3}{% endlatex %} nejsou rovinné
- {% latex %}3 \implies 2{% endlatex %}: obměna: „obsahuje dělení jako podgraf“ {% latex %}\implies{% endlatex %} „obsahuje dělení jako minor“
- {% latex %}1 \implies 3{% endlatex %}: je-li rovinný, tak i minor bude rovinný (fakt výše)
- *{% latex %}2 \implies 3{% endlatex %}: TODO: bylo na cvičení
- *{% latex %}3 \implies 1{% endlatex %}: indukcí podle {% latex %}|V(G)|{% endlatex %}
	- pro {% latex %}|V(G)| \le 4{% endlatex %} vše funguje
	- předpokládám {% latex %}G{% endlatex %} má alespoň 5 vrcholů a neobsahuje {% latex %}K_5{% endlatex %} ani {% latex %}K_{3, 3}{% endlatex %} jako minor. Rozeberu případy podle {% latex %}k_v(G){% endlatex %} (vrcholová souvislost {% latex %}G{% endlatex %})
		- {% latex %}k_v(G) = 0\implies{% endlatex %} nesouvislý graf, použijeme indukci
		- {% latex %}k_v(G) = 1\implies{% endlatex %} artikulačním vrcholem {% latex %}x{% endlatex %} rozpojíme, podle IP nakreslíme
			- {% latex %}x{% endlatex %} musí být na vnější stěně, což umíme přes trik s projekcí z koule na rovinu
		- {% latex %}k_v(G) = 2\implies{% endlatex %}, rozložení podél dvou vrcholů tvořících řez
{% endmath %}

### 4. přednáška
- {% latex %}k_v(G) \ge 3\implies{% endlatex %} použijeme lemma o kontrahovatelné hraně: {% latex %}\exists e = \left\{x, y\right\}{% endlatex %} t. ž. {% latex %}G \setminus e = G'{% endlatex %} je {% latex %}3{% endlatex %}-souvislý
	- (👀) {% latex %}G'{% endlatex %} nemůže obsahovat {% latex %}K_5{% endlatex %} ani {% latex %}K_{3, 3}{% endlatex %} jako minor (kontrakcí něčeho, co je nemělo, je nevytvoříme)
	- {% latex %}\mathcal{G}' \ldots{% endlatex %} rovinné nakreslení {% latex %}G'{% endlatex %} (existuje z IP)
	- {% latex %}G'' = G' - v_e{% endlatex %} (vrchol vzniklý kontrakcí {% latex %}e{% endlatex %}) {% latex %} = G - \left\{x, y\right\}{% endlatex %}
		- (👀) {% latex %}G''{% endlatex %} bude {% latex %}2{% endlatex %}-souvislý (protože {% latex %}G'{% endlatex %} je {% latex %}3{% endlatex %}-souvislý a {% latex %}G''{% endlatex %} vznikne odebráním vrcholu)
		- (👀) taky rovinný (odebráním mi žádný minor nevznikne)
		- {% latex %}\mathcal{G}''{% endlatex %} nakreslení {% latex %}G''{% endlatex %} vzniklé z {% latex %}\mathcal{G}'{% endlatex %} odebráním {% latex %}v_e{% endlatex %}

Označme {% latex %}C{% endlatex %} kružnici ohraničující stěnu {% latex %}\mathcal{G}''{% endlatex %}, v níž ležel (v {% latex %}\mathcal{G}'{% endlatex %} vrchol {% latex %}v_e{% endlatex %}) -- musí to být kružnice, protože v rovinném nakreslení každého {% latex %}2{% endlatex %}-souvislého grafu je každá stěna kružnice.

{% xopp tmp %}

- {% latex %}N(x){% endlatex %} -- sousedi {% latex %}x{% endlatex %}
- {% latex %}N(y){% endlatex %} -- sousedi {% latex %}y{% endlatex %}
- {% latex %}N(x) \cup N(y) \setminus \left\{x, y\right\} \subseteq C{% endlatex %} (každý soused {% latex %}x{% endlatex %} kromě {% latex %}y{% endlatex %} je i sousedem {% latex %}v_e{% endlatex %} v {% latex %}G'{% endlatex %}, stejně pro {% latex %}y{% endlatex %}

3 případy:
- {% latex %}|N(x) \cap N(y)| \ge 3{% endlatex %} -- nenastane, protože kontrakcí dostanu {% latex %}K_5{% endlatex %}, což je spor s předpokladem

{% xopp p1 %}

- {% latex %}\exists a_1, a_2 \in N(x) \cap C, \exists b_1, b_2 \in N(y) \cap C{% endlatex %}, na {% latex %}C{% endlatex %} jsou v pořadí {% latex %}a_1, b_1, a_2, b_2{% endlatex %} -- nenastane, protože kontrakcí dostanu {% latex %}K_{3, 3}{% endlatex %}

{% xopp p2 %}

- zbytek -- nenasatane ani (1), ani (2)
	- označme {% latex %}a_1, \ldots, a_k \in N(x) \cap C{% endlatex %} v pořadí, jak se objevují na {% latex %}C{% endlatex %}
	- můžu nakreslit všechny hrany {% latex %}xa_1, \ldots xa_k{% endlatex %}
	- {% latex %}a_1, \ldots, a_k{% endlatex %} rozdělují {% latex %}C{% endlatex %} na vnitřně disjunktní cesty {% latex %}P_1, \ldots P_k{% endlatex %} ({% latex %}k \ge 2{% endlatex %} protože {% latex %}G{% endlatex %} je {% latex %}3{% endlatex %}-souvislý... {% latex %}x{% endlatex %} sousedí s {% latex %}y{% endlatex %} a s {% latex %}\ge 2{% endlatex %} dalšími vrcholy)
		- chceme: {% latex %}N(y) \setminus \left\{x\right\}{% endlatex %} patří do jediné {% latex %}P_i{% endlatex %} (pro nějaké {% latex %}i{% endlatex %}), jinak by nastaly předchozí případy
	- {% latex %}y{% endlatex %} nakreslím do té správně stěny, spojím s {% latex %}b_i{% endlatex %} a mám hotovo

{% xopp p3 %}
{% xopp p4 %}

#### Kreslení grafů na plochy
{% math definition %}Nechť {% latex %}X \subseteq \mathbb{R}^n, Y \subseteq \mathbb{R}^m{% endlatex %}. Potom homeomorfismus z {% latex %}X{% endlatex %} na {% latex %}Y{% endlatex %} je funkce {% latex %}f: X \mapsto Y{% endlatex %}, která je spojitá, bijekce a {% latex %}f^{-1}{% endlatex %} je spojitá. {% latex %}X, Y{% endlatex %} jsou homeomorfní ({% latex %}X \cong Y{% endlatex %}) pokud mezi nimi existuje homeomorfismus.{% endmath %}
- něco jako isomorfismus u grafů ({% latex %}X \cong Y{% endlatex %} znamená, že se chovají stejně)

{% math definition "plocha" %} kompaktní (uzavřená, omezená), souvislá (např. oblouková -- každé dva body můžu propojit obloukem), {% latex %}2{% endlatex %}-rozměrná varieta bez hranice (dostatečně malé okolí každého bodu je homeomorfní otevřenému okolí v {% latex %}\mathbb{R}^2{% endlatex %}).{% endmath %}
- např. sféra v {% latex %}\mathbb{R}^3{% endlatex %} nebo torus v {% latex %}\mathbb{R}^3{% endlatex %}
- není to např.
	- {% latex %}\mathbb{R}^2{% endlatex %}, jelikož není kompaktní (omezená)
	- čtverec s hranici, jelikož pro každý krajní body není homeomorfní {% latex %}\mathbb{R}^2{% endlatex %}

Operace s plochami, přes které umíme všechny zkonstruovat:


{:.rightFloatBox}
<div markdown="1">
{% xopp o1 %}
</div>
- přidání ucha (od hrnku)
	- vyříznu dva kruhy
	- vezmu plášť pálce bez dna a vrchu
	- ohnu a přílepím jej na díry po kruzích
	- (👀) -- teleport, do kterého když vejdeme, tak na druhé straně vyjdeme opačně („otočeně“)

{:.rightFloatBox}
<div markdown="1">
{% xopp o2 %}
</div>
- přidání křížítka (cross-cupu):
	- (👀) -- teleport, do kterého když vejdeme, tak nás to přesune naproti

Pro {% latex %}g \in \left\{0, 1, \ldots\right\}{% endlatex %} nechť {% latex %}\sum_g{% endlatex %} značí plochu zvniklou ze sféry přidáním {% latex %}g{% endlatex %} uší, tak říkáme, že {% latex %}\sum g{% endlatex %} je **orientovatelná plocha** rodu {% latex %}g{% endlatex %}.

Pro {% latex %}g \in \left\{1, 2, \ldots\right\}{% endlatex %} nechť {% latex %}\prod_g{% endlatex %} značí plochu zvniklou ze sféry přidáním {% latex %}g{% endlatex %} křížítek, tak říkáme, že {% latex %}\prod g{% endlatex %} je **neorientovatelná plocha** rodu {% latex %}g{% endlatex %}.

{% math fact %}Každá plocha je homeomorfní právě jedné z posloupností {% latex %}\sum_0, \prod_1, \sum_1, \prod_2,\ldots{% endlatex %}{% endmath %}
- máme tu skryté tvrzení, že žádné dvě z této posloupností nejsou homeomorfní.

{% math fact %}Přidám-li ke sféře ({% latex %}= \Sigma_0{% endlatex %}) {% latex %}k \ge 0{% endlatex %} uší a {% latex %}l \ge 1{% endlatex %} křížítek, vznikne **neorientovatelná plocha** homeomorfní {% latex %}\prod_{2k + l}{% endlatex %} ({% latex %}\approx{% endlatex %} „přidání dvou křížítek je jako přidání ucha,“ **pokud** už tam bylo {% latex %}\ge 1{% endlatex %} křížítko){% endmath %}

- {% latex %}\sum_0 \ldots{% endlatex %} sféra
- {% latex %}\prod_1 \ldots{% endlatex %} projektivní rovina
- {% latex %}\sum_1 \ldots{% endlatex %} torus
- {% latex %}\prod_2 \ldots{% endlatex %} kleinova láhev

### 5. přednáška
{% math definition "nakreslení grafu" %} {% latex %}G = (V, E){% endlatex %} na plochu {% latex %}\Gamma{% endlatex %} je zobrazení {% latex %}\varphi{% endlatex %} t. ž.:
- každému vrcholu {% latex %}v \in V{% endlatex %} přiřadí bod {% latex %}\varphi(v) \in \Gamma{% endlatex %}
- každé hraně {% latex %}e \in E{% endlatex %} přiřadí prostou (neprotínající se) křivku {% latex %}\varphi(e) \in \Gamma{% endlatex %} spojující konce {% latex %}\varphi(x), \varphi(y){% endlatex %}
- vrcholy se nepřekrývají: {% latex %}x, y \in V: x \neq y \implies \varphi(x) \neq \varphi(y){% endlatex %}
- hrany se překrývají nejvýše ve sdílených vrcholech: {% latex %}e, f \in E: e \neq f \implies \varphi(e) \cap \varphi(f) = \left\{\varphi(x) \mid x \in e \cap f\right\}{% endlatex %}
- vrcholy, které neleží na hraně se s ní neprotínají: {% latex %}e \in E, x \in V: x \not\in e \implies \varphi(x) \not\in \varphi(e){% endlatex %}
{% endmath %}

{% math definition "stěna nakreslení" %} souvislá komponenta {% latex %}\Gamma \setminus \left(\left(\bigcup_{e \in E}^{\varphi(e)}\right) \cup \left(\bigcup_{x \in V}^{\varphi(x)}\right)\right){% endlatex %}{% endmath %}
- prostě souvislé komponenty toho, když odeberu všechna nakreslení hran a vrcholů

{% math definition "buňkové nakreslení" %} každá stěna je homeomorfní otevřenému kruhu v {% latex %}\mathbb{R}^2{% endlatex %}.{% endmath %}

{% xopp torus %}

{% math reminder %}{% latex %}G = (V, E){% endlatex %} souvislý {% latex %}\Rightarrow{% endlatex %} v každém rovinném nakreslení platí {% latex %}|V| - |E| + S = 2{% endlatex %} {% endmath %}
- využíváme faktu, že rovinné nakreslení {% latex %}G{% endlatex %} je buňkové {% latex %}\iff G{% endlatex %} je souvislé
- {% latex %}2{% endlatex %} je speciální pro rovinu

{% math definition "Eulerova charakteristika plochy" %} charakteristika plochy {% latex %}\Gamma{% endlatex %} je

{% latex display %}
\begin{aligned}
\Chi(\Gamma) &= \begin{cases} 2 - g & \Gamma \cong \prod (g \ge 1) \\ 2 - 2g & \Gamma \cong \sum (g \ge 0) \end{cases} \\
\            &= 2 - \text{\# křížítek} - 2 \cdot \text{\# uší}
\end{aligned}
{% endlatex %}
{% endmath %}

{% math theorem "zobecněná Eulerova formule" %}Nechť máme nakreslení grafu {% latex %}G = (V, E){% endlatex %} na ploše {% latex %}\Gamma{% endlatex %}, které má {% latex %}S{% endlatex %} stěn. Pak {% latex %}|V| - |E| + |S| \ge \Chi(\Gamma){% endlatex %}. Pokud je buňkové, tak dokonce {% latex %}|V| - |E| + |S| = \Chi(\Gamma){% endlatex %}.{% endmath %} 

{% math proof "rovnosti" %}idea je indukce podle rodu {% latex %}\Gamma{% endlatex %}
- {% latex %}\Gamma \cong \Sigma_0{% endlatex %} platí

{:.rightFloatBox}
<div markdown="1">
{% xopp s1 %}
</div>
Mějme buňkové nakreslení {% latex %}G = (V, E){% endlatex %} na {% latex %}\Gamma \cong \Pi_g{% endlatex %}
- pro {% latex %}\Gamma \cong \Sigma_g{% endlatex %} se dělá analogicky, jen trháme obě ucha a vyjde to
- {% latex %}v(G), e(G), s(G){% endlatex %} značíme počet vrcholů, hran a stěn

Nechť {% latex %}K{% endlatex %} je křížítko na {% latex %}\Gamma{% endlatex %}, {% latex %}x_1, \ldots, x_k{% endlatex %} jsou body {% latex %}K{% endlatex %} (ne nutně vrcholy grafu), kde hrany {% latex %}G{% endlatex %} kříží {% latex %}K{% endlatex %}
- (👀) {% latex %}k \ge 1{% endlatex %}, jinak by stěna obsahující {% latex %}K{% endlatex %} nebyla buňka
- rovněž předpokládám, že vrchol neleží přesně na křížítku, jinak bych ho mohl BUNO posunout

{:.rightFloatBox}
<div markdown="1">
{% xopp s2 %}
</div>
Vytvoříme {% latex %}G'{% endlatex %} přidáním dvou dělících vrcholů na každou hranu křížící {% latex %}K{% endlatex %} těsně vedle {% latex %}x_1, \ldots, x_k{% endlatex %} („před a za křížítkem“). Děláme to proto, že jedna hrana by mohla procházet křížítkem na více místech a bylo by to pak dost rozbitý.
- {% latex %}v(G') = v(G) + 2k{% endlatex %}
- {% latex %}e(G') = e(G) + 2k{% endlatex %}
- {% latex %}s(G') = s(G){% endlatex %}
- tedy: {% latex %}L(G') = L(G){% endlatex %} (kde {% latex %}L{% endlatex %} je levá strana)

{:.rightFloatBox}
<div markdown="1">
{% xopp s3 %}
</div>
Vytvoříme {% latex %}G''{% endlatex %} přidaním cest délky {% latex %}2{% endlatex %} k sousedním vrcholům z předchozího kroku. Vznikne tím kružnice {% latex %}C{% endlatex %} obcházející {% latex %}K{% endlatex %}.
- {% latex %}v(G'') = v(G') + 2k{% endlatex %}
- {% latex %}e(G'') = e(G') + 4k{% endlatex %}
- {% latex %}s(G'') = s(G') + 2k{% endlatex %} (každou z {% latex %}k{% endlatex %} stěn dělím na {% latex %}3{% endlatex %} kusy)
- tedy: {% latex %}L(G'') = L(G'){% endlatex %}

{:.rightFloatBox}
<div markdown="1">
{% xopp s4 %}
</div>
Vytvoříme {% latex %}G'''{% endlatex %} odebráním všeho uvnitř {% latex %}C{% endlatex %}.
- {% latex %}v(G''') = v(G''){% endlatex %}
- {% latex %}e(G''') = e(G'') - k{% endlatex %} ({% latex %}k{% endlatex %} křížících-se hran uvnitř {% latex %}C{% endlatex %})
- {% latex %}s(G''') = s(G'') - k + 1{% endlatex %} („spojím“ {% latex %}k{% endlatex %} stěn do jedné)
- tedy: {% latex %}L(G''') = L(G'') + 1{% endlatex %}

{% latex display %}L(G''') = \Chi(\Pi_{g - 1}) = \Chi(\Gamma) + 1 \qquad \mid \text{dle IP}{% endlatex %}
{% latex display %}L(G''') - 1 = L(G'') = L(G') = L(G) \qquad \mid \text{z výpočtu}{% endlatex %}

Tedy {% latex display %}\Chi(\Gamma) = L(G){% endlatex %}
{% endmath %}

{% math consequence %}Každý graf {% latex %}G{% endlatex %} nakreslitelný na plochu {% latex %}\Gamma{% endlatex %} splní {% latex %}|E| \le 3|V| - 3\Chi(\Gamma){% endlatex %}, pokud {% latex %}|V| \ge 4{% endlatex %}
- důkaz přes to, že předpokládáme, že každá stěna je trojúhelník a dosadíme {% latex %}|S| = \frac{2}{3}|E|{% endlatex %}, jelikož každá stěna je tvořena třemi hranami a zároveň je každá hrana ve dvou stěnách
- každý takový graf má průměrný stupeň {% latex %}\frac{2|E|}{|V|} \le 6 - \frac{6\Chi(\Gamma)}{|V|}{% endlatex %}
	- na žádnou zafixovanou plochu nelze nakreslit libovolně velký {% latex %}7{% endlatex %}-regulární graf
	- pro libovolně velký úplňák dokážeme vytvořit plochu, na kterou ho nakreslíme
{% endmath %}

{% math lemma %}Nechť {% latex %}\Gamma{% endlatex %} je plocha, {% latex %}\Gamma \neq \Sigma_0{% endlatex %}, nechť {% latex %}G{% endlatex %} je graf nakreslený na {% latex %}\Gamma{% endlatex %}, potom {% latex %}G{% endlatex %} obsahuje vrchol stupně {% latex %}\le \left\lfloor \frac{5 + \sqrt{49 - 24\Chi(\Gamma)}}{2} \right\rfloor{% endlatex %}{% endmath %}

{% math proof %}Mějme {% latex %}G{% endlatex %} podle předpokladu. Opět značíme {% latex %}v(G), e(G){% endlatex %} jako počet vrcholů a hran. ROzlišíme {% latex %}3{% endlatex %} případy:
- {% latex %}\Chi(\Gamma) = 1{% endlatex %} (t.j. {% latex %}\Gamma \cong \prod_1{% endlatex %}), dosazením do předchozího důsledku dostáváme průměrný stupeň {% latex %}< 6{% endlatex %}, tedy existuje vrchol stupně {% latex %}\le 5{% endlatex %}, což jsme chtěli
- {% latex %}\Chi(\Gamma) = 0{% endlatex %} (t.j. {% latex %}\Gamma \cong \prod_2{% endlatex %} nebo {% latex %}\Gamma \cong \sum_1{% endlatex %}), průměrný stupeň {% latex %}\le 6 \implies \exists{% endlatex %} vrchol stupně {% latex %}\le 6{% endlatex %}
- {% latex %}\Chi(\Gamma) < 0 \ldots \delta(G) = {% endlatex %} min. stupeň {% latex %}G{% endlatex %}; víme:
	- {% latex %}\delta(G) \le 6 - \frac{6 \Chi(\Gamma)}{v(G)}{% endlatex %}
	- {% latex %}\delta(G) \le v(G) - 1{% endlatex %} (žádný vrchol nemá víc než {% latex %}v(G) - 1{% endlatex %} sousedů)
	- chceme zjistit max. hodnotu {% latex %}\delta{% endlatex %}, což je řešení dvou rovnic výše; dosazením a vyřešením kvadratické rovnice vyjde přesně výraz, který dokazujeme
{% endmath %}

{% math consequence "Heawoodova formule, 1890" %} Pokud {% latex %}\Gamma \not\cong \sum_0{% endlatex %}, tak každý graf nakreslitelny na {% latex %}\Gamma{% endlatex %} je nejvýš {% latex %}H(\Gamma) = 1 + \left\lfloor \frac{5 + \sqrt{49 - 24 \Chi(\Gamma)}}{2} \right\rfloor = \left\lfloor \frac{7 + \sqrt{49 - 24 \Chi(\Gamma)}}{2} \right\rfloor{% endlatex %}-obarvitelný{% endmath %}
- vyplývá z předchozího důsledku -- pokud má graf stupeň nejvýše {% latex %}\delta{% endlatex %}, tak je {% latex %}\delta+1{% endlatex %}-obarvitelný
- platí i pro stéru: věta o {% latex %}4{% endlatex %}-barvách
- tento odhad je těsný pro všechny plochy kromě {% latex %}\prod_2{% endlatex %}
- na každou plochu {% latex %}\Gamma \not\cong \prod_2{% endlatex %} lze kreslit kliku velikosti {% latex %}H(\Gamma){% endlatex %}
	- (každý graf nakreslitelný na {% latex %}\prod_2{% endlatex %} je dokonce {% latex %}6{% endlatex %}-obarvitelný)

### 6. přednáška

#### Vrcholové barvení
- {% latex %}\Chi(G) ={% endlatex %} barevnost {% latex %}G = {% endlatex %} nejmenší počet barev, kterými lze (dobře) obarvit vrcholy {% latex %}G{% endlatex %}
- {% latex %}\Delta(G) = {% endlatex %} max. stupeň {% latex %}G = {% endlatex %}, {% latex %}\delta(G) = {% endlatex %} min. stupeň {% latex %}G{% endlatex %}

{% math definition %}{% latex %}G{% endlatex %} je {% latex %}d{% endlatex %}-degenerovaný {% latex %}\equiv{% endlatex %} každý podgraf {% latex %}H{% endlatex %} grafu {% latex %}G{% endlatex %} má {% latex %}\delta(H) \le d{% endlatex %}{% endmath %}
- {% latex %}={% endlatex %} každý podgraf má vrchol stupně nejvýše {% latex %}d{% endlatex %}
- {% latex %}\iff \exists{% endlatex %} pořadí vrcholů (eliminační) {% latex %}v_1, \ldots v_n{% endlatex %} t. ž. {% latex %}\forall i: G_i := G - \left\{v_1, \ldots, v_i\right\}: \delta(G_i) \le d{% endlatex %} a {% latex %}v_{i - 1}{% endlatex %} má {% latex %}\le d{% endlatex %} sousedů v {% latex %}G_i{% endlatex %}
	- trháme vrcholy v pořadí tak, že každý další odebraný má nejvýše {% latex %}d{% endlatex %} sousedů
	- {% math observation %}{% latex %}G{% endlatex %} je {% latex %}d{% endlatex %}-degenerovaný {% latex %}\implies \Chi(G) \le d + 1{% endlatex %}{% endmath %} (barvím indukcí v pořadí {% latex %}v_n, \ldots, v_1{% endlatex %})

![](/assets/kombinatorika-a-grafy-ii/degen.png)

- z minule: pokud {% latex %}G{% endlatex %} je nakreslitelný na {% latex %}\Gamma \implies G{% endlatex %} má vrchol stupně nejvýše {% latex %}H(\Gamma) - 1{% endlatex %} a {% latex %}G - v{% endlatex %} je stále nakreslitelný na {% latex %}\Gamma \implies G{% endlatex %} je {% latex %}\left(H(\Gamma) - 1\right){% endlatex %}-degenerovaný {% latex %}\implies{% endlatex %} je {% latex %}H(\Gamma){% endlatex %} obarvitelný

{% math observation %}{% latex %}G{% endlatex %} je {% latex %}\Delta(G){% endlatex %}-degenerovaný (triviálně) {% latex %}\implies \Chi(G) \le \Delta(G) + 1{% endlatex %} (z pozorování výše){% endmath %}

- s rovností platí např. pro úplné grafy a liché cykly

{% math lemma %}{% latex %}G{% endlatex %} souvislý graf a {% latex %}\delta(G) < \Delta(G){% endlatex %}, pak {% latex %}\Chi(G) \le \Delta(G){% endlatex %}{% endmath %}
- když nás zajímá předchozí otázka, tak se stačí zaměřit na nějaký regulární graf

{:.rightFloatBox}
<div markdown="1">
{% xopp a1 %}
</div>
{% math proof %}Tvrdím, že {% latex %}G{% endlatex %} je ({% latex %}\Delta(G) - 1{% endlatex %})-degenerovaný. Volme {% latex %}H{% endlatex %} neprázdný podgraf {% latex %}G{% endlatex %} a dokazujeme, že v {% latex %}H{% endlatex %} existuje {% latex %}v{% endlatex %} stupně {% latex %}\le \Delta(G) - 1{% endlatex %} 
- pokud {% latex %}H{% endlatex %} obsahuje všechny vrcholy {% latex %}\implies{% endlatex %} platí z předpokladu.
- jinak {% latex %}\exists e = \left\{x, y\right\} \in G{% endlatex %} t. ž. {% latex %}x \in H{% endlatex %} a {% latex %}y \not\in H{% endlatex %}
	- {% latex %}\deg_H(x) \le \deg_G(x) - 1 \le \Delta(G) - 1{% endlatex %}
{% endmath %}

{% math theorem "Brooks, 1941" %}Nechť {% latex %}G{% endlatex %} je souvislý graf který není úplný a není lichá kružnice. Pak je {% latex %}G \le \Delta(G){% endlatex %}-obarvitelný.{% endmath %}

{% math proof %}nechť {% latex %}\Chi = \Chi(G), \Delta = \Delta(G){% endlatex %} a navíc předpokládám, že {% latex %}G{% endlatex %} je {% latex %}\Delta{% endlatex %}-regulární (jinak viz. předchozí lemma.

- {% latex %}\Delta = 1{% endlatex %}
	- {% latex %}K_2{% endlatex %}: zakázané
- {% latex %}\Delta = 2{% endlatex %}
	- {% latex %}C_{2k}{% endlatex %}: {% latex %}\Chi = 2{% endlatex %}
	- {% latex %}C_{2k + 1}{% endlatex %}: zakázané
- {% latex %}\Delta \ge 3{% endlatex %}; označme {% latex %}k_V(G) = {% endlatex %} vrcholová souvislost {% latex %}G{% endlatex %}
	- {% latex %}k_V(G) = 1{% endlatex %} -- máme artikulaci; vrchol artikulace {% latex %}v{% endlatex %} měl souseda v obou částech grafu, proto {% latex %}\deg_{G_1}(v), \deg_{G_2}(V) < \Delta \implies{% endlatex %} podle lemmatu ({% latex %}G_1{% endlatex %} a {% latex %}G_2{% endlatex %} nejsou regulární) lze {% latex %}G_1{% endlatex %} i {% latex %}G_2{% endlatex %} {% latex %}\Delta{% endlatex %}-obarvit a stačí přepermutovat barvy, aby měl v obou obarveních stejnou
	- {% latex %}k_V(G) = 2{% endlatex %}
		- dobré případy (lze slepit)
			- {% latex %}b_1(x) = b_1(y){% endlatex %} a {% latex %}b_2(x) = b_2(y){% endlatex %} 
			- {% latex %}b_1(x) \neq b_1(y){% endlatex %} a {% latex %}b_2(x) \neq b_2(y){% endlatex %} 
		- těžší případ -- na jedné straně stejné, na druhé různé
			- {% latex %}b_1(x) = b_1(y){% endlatex %} a {% latex %}b_2(x) \neq b_2(y){% endlatex %} 
				- pokud {% latex %}\deg_{G_1}(x){% endlatex %} nebo {% latex %}\deg_{G_1}(y) \le \Delta - 2{% endlatex %}, tak po přidání hrany půjde použít lemma a vrcholy budou mít různou barvu a máme dobrý případ
					- nemůže se stát, že by např. druhý měl {% latex %}\deg_{G_1} = \Delta{% endlatex %}, protože musí vidět i do druhé komponenty
				- nebo {% latex %}\deg_{G_1}(x) = \deg_{G_1}(y) = \Delta - 1{% endlatex %}
					- pak musí {% latex %}\deg_{G_2}(x) = \deg_{G_2}(y) = 1{% endlatex %} (stupeň je celkově {% latex %}\Delta{% endlatex %})
					- z předpokladu máme k použití alespoň {% latex %}3{% endlatex %} barvy, přebarvím jimi {% latex %}x{% endlatex %} a {% latex %}y{% endlatex %} a máme dobrý případ
	- {% latex %}k_V(G) \ge 3{% endlatex %} -- použiji lemma o třešničce (souvislý graf, který není klika, obsahuje třešničku)
		- seřadím vrcholy jako {% latex %}v_1 = x, v_2 = y, \ldots, v_n = z{% endlatex %} tak, aby {% latex %}\forall v_i: 3 \le i \le n - 1{% endlatex %} měl alespoň jednoho souseda napravo a barvím (hladově):
			- umíme získat jako BFS vrstvy od {% latex %}z{% endlatex %}, kromě {% latex %}x{% endlatex %} a {% latex %}y{% endlatex %}
			- {% latex %}b(x) = b(y) = 1{% endlatex %}
			- {% latex %}b(v_3)\ldots{% endlatex %} má {% latex %}\ge 1{% endlatex %} neobarveného souseda {% latex %}\implies{% endlatex %} je nějaká nepoužitá z {% latex %}\Delta{% endlatex %} barev
			- {% latex %}\ldots{% endlatex %}
			- {% latex %}b(v_n)\ldots{% endlatex %} všichni sousedé už obarvení, ale dva sousedé ({% latex %}x, y{% endlatex %}) mají stejnou barvu, tedy {% latex %}z{% endlatex %} vidí {% latex %}\le \Delta - 1{% endlatex %} barev a jedna je volná

---

Obrázek případů pro {% latex %}k_V(G) = 2{% endlatex %}:

{% xopp cases %}

---

{% endmath %}

#### Pár poznámek

**Harwigerova domněnka:** {% latex %}K_t \not\preceq_m G{% endlatex %} (není minor){% latex %} \implies \Chi(G) < t{% endlatex %}
- {% latex %}t = 4 \ldots{% endlatex %} relativně jednoduché
- {% latex %}t = 5 \ldots{% endlatex %} zobecnění věty o {% latex %}4{% endlatex %} barvách
- {% latex %}t = 6 \ldots{% endlatex %} pomocí věty o {% latex %}4{% endlatex %} barvách + hodně práce
- {% latex %}t \ge 7 \ldots{% endlatex %} neví se

{% math claim %}{% latex %}G{% endlatex %} nakreslitelný na Kleinovu láhev {% latex %}\implies G{% endlatex %} je {% latex %}6{% endlatex %}-obarvitelný.{% endmath %}

{% math proof %}Z Eulerovy formule plyne, že platí jedno z následujících:
- {% latex %}\delta(G)\le 5 \implies \exists v: \deg(v) \le 5{% endlatex %}{% endmath %}
	- {% latex %}G - v \ldots{% endlatex %}  obarvím z indukce, přidám {% latex %}v{% endlatex %} a mám volnou barvu
- {% latex %}G{% endlatex %} je {% latex %}6{% endlatex %}-regulární:
	- {% latex %}G \cong K_7{% endlatex %} -- nesmí, protože nejde nakreslit (je potřeba si rozmyslet)
	- {% latex %}G \not\cong K_7{% endlatex %} -- přímo Brooksova věta

#### Hranové obarvení
{% math definition %}{% latex %}b: E \mapsto B{% endlatex %} (barvy) t. ž. {% latex %}\forall e \neq f \in E, e \cap f \neq \emptyset \implies b(e) \neq b(f){% endlatex %}. Hranová barevnost {% latex %}G{% endlatex %} ("chromatic index") {% latex %}\Chi'(G){% endlatex %} je min. počet barev pro hranové barvení {% latex %}G{% endlatex %}.{% endmath %}

### 7. přednáška

{% math theorem "Vizing, 1964" %}Pro každý graf {% latex %}G{% endlatex %} platí, že {% latex %}\Delta(G) \le \Chi'(G) \le \Delta(G) + 1{% endlatex %}{% endmath %}
- grafy Vizingovy třídy {% latex %}1{% endlatex %} jsou grafy {% latex %}\Chi'(G) = \Delta(G){% endlatex %}, třídy {% latex %}2{% endlatex %} jsou {% latex %}\Chi'(G) = \Delta(G) + 1{% endlatex %}
- je NP-úplné rozhodnout, zda daný graf {% latex %}G{% endlatex %} má VIzingovu třídu {% latex %}1{% endlatex %} (i pro grafy s {% latex %}\Delta(G) = 3{% endlatex %})
- důkaz jsem zpracoval do [YouTube videa](https://www.youtube.com/watch?v=OZWZpQmGp0g)

#### Perfektní grafy

{% math theorem "Slabá věta o perfektních grafech, 1972" %}{% latex %}G{% endlatex %} je perfektní {% latex %}\iff{% endlatex %} {% latex %}\bar{G}{% endlatex %} je perfektní.{% endmath %}
- důkaz jsem zpracoval do [YouTube videa](https://www.youtube.com/watch?v=Koc63QhxPgk)

### 8. přednáška

#### Chordální grafy

{% math definition "chordální graf" %}Graf je chordální, pokud neobsahuje {% latex %}C_k, k \ge 4{% endlatex %} jako in. podgraf.{% endmath %}
- alternativní pohled vycházející ze jména: každá kružnice má _chordu_ (tětivu)

{% math definition %}Nechť {% latex %}x, y{% endlatex %} dva nesousední vrcholy {% latex %}G{% endlatex %}. {% latex %}R{% endlatex %} je {% latex %}x{\text -}y{% endlatex %}-řez, pokud je to řez takový, že {% latex %}x, y{% endlatex %} patří do různých komponent {% latex %}G \setminus R{% endlatex %}.{% endmath %}

{% math lemma %}{% latex %}G{% endlatex %} je chordální {% latex %}\iff{% endlatex %} pro každé dva nesousední vrcholy {% latex %}x, y \in V, x \neq y{% endlatex %} existuje {% latex %}x{\text -}y{% endlatex %}-řez, který je klika.{% endmath %}

{% math proof %} {% latex %}\Leftarrow{% endlatex %} nechť {% latex %}G{% endlatex %} není chordální, tedy obsahuje indukovanou kružnici {% latex %}C_4{% endlatex %}. Uvážíme-li dva její nesousední vrcholy, tak jakýkoliv řez musí obsahovat vrcholy z horní a dolní cesty mezi {% latex %}x{% endlatex %} a {% latex %}y{% endlatex %}. Ty nesousedí, tedy řez nebude klika.

{% latex %}\Rightarrow{% endlatex %} nechť {% latex %}G{% endlatex %} je chordální, {% latex %}x, y{% endlatex %} nesousední. Nechť {% latex %}R{% endlatex %} je {% latex %}x{\text -}y{% endlatex %}-řez s co nejméně vrcholy. Tvrdím, že {% latex %}R{% endlatex %} tvoří kliku.

Pro spor: {% latex %}R{% endlatex %} není klika {% latex %}\implies{% endlatex %} obsahuje {% latex %}u, v{% endlatex %} nesousedy. Protože {% latex %}R{% endlatex %} je nejmenší, má {% latex %}u{% endlatex %} i {% latex %}v{% endlatex %} sousedy na obou stranách. Jelikož jsou to komponenty souvislosti, tak tam bude existovat cesta. Vezmu nejkratší cesty {% latex %}P_x, P_y{% endlatex %} v komponentách {% latex %}G_x{% endlatex %}, {% latex %}G_y{% endlatex %}. Vrcholy {% latex %}P_x, P_y{% endlatex %} nesousedí (jinak by {% latex %}R{% endlatex %} nebyl řez), {% latex %}P_x-u-P_y-v{% endlatex %} tvoří indukovaný cyklus.

{% xopp another1 %}

{% endmath %}

{% math definition %}Vrchol {% latex %}x{% endlatex %} je v grafu {% latex %}G{% endlatex %} simpliciální, pokud jeho sousedství ({% latex %}N_G(x){% endlatex %} tvoří kliku {% latex %}G{% endlatex %}.{% endmath %}

{% math theorem %}Každý chordální graf (kromě prázdného) obsahuje simpliciální vrchol.{% endmath %}
- dokážeme pomocí silnějšího tvrzení

{% math theorem %}Každý chordální graf je buď úplný, nebo obsahuje dva nesousední simpliciální vrcholy.{% endmath %}

{% math proof %}indukcí podle {% latex %}|V(G)|{% endlatex %}
- základ: {% latex %}|V(G)| = 1{% endlatex %} platí
- pro více vrcholů
	- {% latex %}G{% endlatex %} je úplný, platí
	- nebo nechť {% latex %}x, y{% endlatex %} nesousedi v {% latex %}G{% endlatex %} a {% latex %}R{% endlatex %} je {% latex %}x{\text -}y{% endlatex %}-řez tvořící kliku
		- {% latex %}G_x^+ = \left(\text{komponenta $G \setminus R$ obsahující $x$}\right) \cup R{% endlatex %}, obdobně {% latex %}G_y^+{% endlatex %}
		- (👀) pokud {% latex %}G{% endlatex %} byl chordální, pak {% latex %}H \le G{% endlatex %} je také chordalní
		- použijeme IP na {% latex %}G_x^+{% endlatex %}
			- pokud {% latex %}G_x^+{% endlatex %} klika, vezmi jako {% latex %}s_x{% endlatex %} libovolný vrchol {% latex %}G_x{% endlatex %} (např. {% latex %}x{% endlatex %})
			- pokud {% latex %}G_x^+{% endlatex %} není klika, má dva simpliciální vrcholy; nejvýše jeden může ležet v {% latex %}R{% endlatex %}, jelikož je to klika a za {% latex %}s_x{% endlatex %} zvolím ten druhý; analogicky pro {% latex %}G_y^+{% endlatex %}
			- (👀) jelikož {% latex %}R{% endlatex %} je řez, tak se sousedství nezmění: {% latex %}N_{G_x^+}(s_x) = N_{G}(s_x){% endlatex %}

{% xopp another2 %}
{% endmath %}

{:.rightFloatBox}
<div markdown="1">
{:.center}
![](/assets/kombinatorika-a-grafy-ii/dog.svg)
</div>
{% math definition "PES" %} Perfektní eliminační schéma (PES) grafu {% latex %}G{% endlatex %} je pořadí vrcholů {% latex %}v_1, \ldots, v_n{% endlatex %} t. ž. {% latex %}\forall i \in [n]{% endlatex %} platí, že leví sousedé {% latex %}v_i{% endlatex %} ({% latex %}= \left\{v_j \mid j < i, v_jv_i \in E\right\}{% endlatex %}) tvoří kliku.{% endmath %}

{% math theorem %}G je chordální {% latex %}\iff{% endlatex %} G má PES.{% endmath %}

{% math proof %}{% latex %}\Rightarrow{% endlatex %} obměnou nechť {% latex %}G{% endlatex %} není chordální a má tedy indukovanou kružnici velikosti alespoň {% latex %}4{% endlatex %}. Pro spor nechť máme PES. Nejlevější vrchol špatné kružnice v PES nemá souseda na této kružnici, což je spor s definicí PES.

{% latex %}\Leftarrow{% endlatex %} nechť {% latex %}G{% endlatex %} je chordální. Má tedy simpliciální vrchol {% latex %}v_n{% endlatex %}. Jeho sousedé tvoří kliku a {% latex %}G - v_n{% endlatex %} je opět chordální (pozorování výše) a opakujeme, čímž vznikne PES pro {% latex %}G{% endlatex %}.
{% endmath %}

{% math consequence %}pro daný graf {% latex %}G{% endlatex %} lze v polynomiálním čase rozhodnout, zda je chordální.{% endmath %}

{% math consequence %}chordální grafy jsou perfektní.{% endmath %}

{% math definition %}{% latex %}G{% endlatex %} je hamiltonovský, pokud má kružnici na {% latex %}n{% endlatex %} vrcholech (jako podgraf).{% endmath %}

{% math theorem "Bondyho-Chvátalova" %}Nechť {% latex %}G{% endlatex %} je graf na {% latex %}\ge 3{% endlatex %} vrcholech. Nechť {% latex %}x,y{% endlatex %} jsou nesousedé t. ž. {% latex %}\deg_G(x) + \deg_G(y) \ge n{% endlatex %}. Nechť {% latex %}G^+ = (V, E \cup \left\{xy\right\}){% endlatex %}. Pak {% latex %}G{% endlatex %} je hamiltonovský {% latex %}\iff{% endlatex %} {% latex %}G^+{% endlatex %} je hamiltonovský.{% endmath %}

{% math proof %} {% latex %}\Rightarrow{% endlatex %} jasné

{% latex %}\Leftarrow{% endlatex %} nechť {% latex %}C{% endlatex %} je hamiltonovská kružnice {% latex %}G^+{% endlatex %} a {% latex %}x,y{% endlatex %} vrcholy splňující podmínku.
- pokud {% latex %}C{% endlatex %} neobsahuje {% latex %}xy{% endlatex %}, pak {% latex %}C{% endlatex %} je hamiltonovská kružnice {% latex %}G{% endlatex %}
- jinak {% latex %}v_1, \ldots, v_n{% endlatex %} očíslujeme vrcholy {% latex %}C{% endlatex %} a navíc {% latex %}v_1 = x, v_n = y{% endlatex %}
	- chceme {% latex %}C' := \left(C \setminus \left\{xy, v_iv_{i + 1}\right\}\right) \cup \left\{v_iy, v_{i + 1}x\right\}{% endlatex %} je ham. kružnice v {% latex %}G{% endlatex %}
	- {% latex %}I_1 := \left\{i \in \left\{2, \ldots, n - 2\right\}\ \text{t. ž. }\left\{x, v_{i + 1}\right\} \in E\right\}{% endlatex %} (vrcholy dobré pro {% latex %}x{% endlatex %})
		- povoluji vrcholy {% latex %}v_3, \ldots, v_{n-1}{% endlatex %}, viz. indexování
	- {% latex %}I_2 := \left\{i \in \left\{2, \ldots, n - 2\right\}\ \text{t. ž. }\left\{y, v_i\right\} \in E\right\}{% endlatex %} (vrcholy dobré pro {% latex %}y{% endlatex %})
		- povoluji vrcholy {% latex %}v_2, \ldots, v_{n - 2}{% endlatex %}, viz. indexování
	- {% latex %}|I_1 \cup I_2| \le n - 3{% endlatex %}
	- {% latex %}|I_1| = \deg_G(x) - 1{% endlatex %} (nesmím použít {% latex %}v_2{% endlatex %})
	- {% latex %}|I_2| = \deg_G(y) - 1{% endlatex %} (nesmím použít {% latex %}v_{n - 1}{% endlatex %})
	- {% latex %}|I_1| + |I_2| = \deg_G(x) - 1 + \deg_G(y) - 1 \ge n - 2{% endlatex %} (z předpokladu)
	- {% latex %}|I_1 \cup I_2| \le 3{% endlatex %} ale {% latex %}|I_1 + I_2| \ge n - 2{% endlatex %} znamená, že se překrývají

{% xopp another3 %}
{% endmath %}

{% math theorem "Divac" %}{% latex %}G{% endlatex %} graf na {% latex %}n \ge 3{% endlatex %} vrcholech s min. stupněm {% latex %}\ge n/2{% endlatex %} je hamiltonovský.{% endmath %}

{% math proof %}Z Bondy-Chvátalovy věty doplníme na {% latex %}K_n{% endlatex %}, který je hamiltonovský.{% endmath %}

### 9. přednáška

#### Tutteův polynom

{% math definition: "multigraf" %} {% latex %}G = (V, E){% endlatex %} kde {% latex %}V{% endlatex %} jsou vrcholy a {% latex %}E{% endlatex %} multimnožina prvků z {% latex %}V \cup \binom{V}{2}{% endlatex %}{% endmath %}
- odstranění a kontrakce fungují intuitivně -- kontrakce nezahazuje hrany, protože máme multigraf

{% math definition "most" %}hrana {% latex %}e \in E{% endlatex %} je most, v multigrafu {% latex %}G{% endlatex %}, pokud {% latex %}G - e{% endlatex %} má více komponent než {% latex %}G{% endlatex %}{% endmath %}
- {% latex %}k(G) = k(V, E) = \text{počet komponent}{% endlatex %}

{% math definition: "hodnost/rank" %}{% latex %}E{% endlatex %} je {% latex %}r(E) := |V| - k(G){% endlatex %}{% endmath %}
- intuice: {% latex %}\sim{% endlatex %} velikost největší „neredundantní“ podmnožiny {% latex %}F \subseteq E{% endlatex %} (t. ž. {% latex %}k(G) = k(V, F){% endlatex %})

{% math proof %}Chceme dokázat, že {% latex %}F{% endlatex %} neobsahuje cykly a že {% latex %}r(E) = r(F){% endlatex %}. Víme, že {% latex %}k(G) = k(V, F){% endlatex %}.

Postupné přidávání hran z {% latex %}F{% endlatex %}
- snižuje počet komponent, vždy o {% latex %}1{% endlatex %}, tedy {% latex %}k(V, F) = n - |F| = |V| - |F|{% endlatex %}
- zvyšuje {% latex %}\mathrm{r}{% endlatex %} vždy o {% latex %}1{% endlatex %} (nastává druhý případ z tabulky dole), tedy {% latex %}r(F) = |F|{% endlatex %}

Spojením dostáváme {% latex %}r(F) = |F| = |V| - k(V, F) = |V| - k(G){% endlatex %}.
{% endmath %}

{% math definition: "nulita" %}{% latex %}E{% endlatex %} je {% latex %}n(E) := |E| - r(E){% endlatex %}{% endmath %}
- intuice: velikost největší „redundantní“ podmnožiny {% latex %}F \subseteq E{% endlatex %} (t. ž. počet komponent se nezmění po jejím odebrání)

{% math example %}{% latex %}G = (V, \emptyset){% endlatex %}
- {% latex %}r(\emptyset) = 0{% endlatex %}
- {% latex %}n(\emptyset) = 0{% endlatex %}

| změna                                   | {% latex %}r(E){% endlatex %}     | {% latex %}n(E){% endlatex %}     |
| ---                                     | ---                               | ---                               |
| přidání hrany bez změny počtu komponent | {% latex %}r(E){% endlatex %}     | {% latex %}n(E) + 1{% endlatex %} |
| přidání hrany se změnou počtu komponent | {% latex %}r(E) + 1{% endlatex %} | {% latex %}n(E){% endlatex %}     |

- přidáním hrany se rank:
	- nezmění, pokud se nezmění počet komponent
	- zvětší o {% latex %}1{% endlatex %}, pokud se dvě komponenty spojily
{% endmath %}

{% math definition: "Tutteův polynom" %}multigrafu {% latex %}G = (V, E){% endlatex %} je polynom proměnných {% latex %}x, y{% endlatex %} definovaný jako {% latex display %}T_G(x, y) := \sum_{F \subseteq E} (x - 1)^{r(E) - r(F)} \cdot (y - 1)^{n(F)}{% endlatex %}{% endmath %}

{% math lemma %}pro {% latex %}G{% endlatex %} souvislý je {% latex %}T_G(1, 1){% endlatex %} počet koster {% latex %}G{% endlatex %}{% endmath %}

{% math proof %}Dosadím do polynomu a získám {% latex %}0^{r(E) - r(F)} 0^{n(F)}{% endlatex %}. Vím, že {% latex %}x^0 \equiv 1{% endlatex %}, tedy výraz bude počet {% latex %}F{% endlatex %} takových, že {% latex %}r(E) = r(F){% endlatex %} a {% latex %}n(F) = 0{% endlatex %}.
- z předpokladu souvislosti je počet komponent {% latex %}1{% endlatex %}
	- {% latex %}F{% endlatex %} musí mít také pouze {% latex %}1{% endlatex %}, protože {% latex %}r(E) = r(F){% endlatex %}
- {% latex %}n(F) = 0{% endlatex %} znamená, že {% latex %}0 = |F| - |V| - 1{% endlatex %}, tedy {% latex %}|F| = |V| - 1{% endlatex %}
- kombinace počtu hran a souvislosti dává, že je to strom a tedy kostra
{% endmath %}

{% math lemma %}Nechť {% latex %}G_1 = (V_1, E_1), G_2 = (V_2, G_2){% endlatex %} jsou multigrafy, t. ž. {% latex %}|V_1 \cap V_2| \le 1{% endlatex %}, {% latex %}|E_1 \cap E_2| = 0{% endlatex %} (protínají se nejvýše v jednom vrcholu a v žádné hraně). Definujeme {% latex %}G = (V, E){% endlatex %}, kde {% latex %}V = V_1 \cup V_2{% endlatex %} a {% latex %}E = E_1 \cup E_2{% endlatex %}. Potom {% latex %}T_G(x, y) = T_{G_1}(x, y) \cdot T_{G_2}(x, y){% endlatex %}
{% endmath %}

{% math proof %}V definici kvantifikuji přes podmnožiny hran. Ty ale můžu vždy rozdělit na disjunktní sjednocení podle {% latex %}E_1{% endlatex %} a {% latex %}E_2{% endlatex %}. Navíc:
- {% latex %}r(F) = r(F_1) + r(F_2){% endlatex %} (z pohledu jako největší neredundantní množina hran)
- {% latex %}n(F) = n(F_1) + n(F_2){% endlatex %} (analogicky, opět z intuice)

Pak rozepíšu:
{% latex display %}
\begin{aligned}
	T_G(x, y) &= \sum_{F \subseteq E} (x - 1)^{r(E) - r(F)} (y - 1)^{n(F)} \\
	          &= \sum_{F_1 \subseteq E_1} \sum_{F_2 \subseteq E_2} (x - 1)^{r(E_1 \cup E_2) - r(F_1 \cup F_2)} (y - 1)^{n(F_1 \cup F_2)} \\
	          &= \sum_{F_1 \subseteq E_1} \sum_{F_2 \subseteq E_2} (x - 1)^{r(E_1) - r(F_1) + r(E_2) - r(F_2)} (y - 1)^{n(F_1) +n(F_2) } \\
	          &= \sum_{F_1 \subseteq E_1} \sum_{F_2 \subseteq E_2} (x - 1)^{r(E_1) - r(F_1)} (x - 1)^{r(E_2) - r(F_2)} (y - 1)^{n(F_1)} (y - 1)^{n(F_2)} \\
	          &= \sum_{F_1 \subseteq E_1} (x - 1)^{r(E_1) - r(F_1)}(y - 1)^{n(F_1)}  \left(\sum_{F_2 \subseteq E_2} (x - 1)^{r(E_2) - r(F_2)} (y - 1)^{n(F_2)}\right) \\
	          &= T_{G_1}(x, y) \cdot T_{G_2}(x, y) \\
\end{aligned}
{% endlatex %}
{% endmath %}

{% math consequence %}dva grafy se stejným Tutteovým polynomem nemusí být stejné (neobsahuje informaci o počtu komponent či počtu vrcholů).{% endmath %}

{% math theorem %}Nechť {% latex %}G = (V, E){% endlatex %} je multigraf. Potom {% latex %}T_G(x, y){% endlatex %} je jednoznačně určen rekurencemi:
{% endmath %}
- {% latex %}E = \emptyset{% endlatex %}: {% latex %}T_G(x, y) = 1{% endlatex %}
- jinak pro {% latex %}e{% endlatex %}:

| most   | {% latex %}T_G(x, y) = x \cdot T_{G - e}(x, y)= x \cdot T_{G \setminus e}(x, y){% endlatex %}  |
|        | poslední rovnost: z důsledku výše                                                              |
| smyčka | {% latex %}T_G(x, y) = y \cdot T_{G - e}(x, y) = y \cdot T_{G \setminus e}(x, y){% endlatex %} |
|        | poslední rovnost: odstranění smyčky je to stejné jako její kontrakce                           |
| jindy  | {% latex %}T_G(x, y) = T_{G - e}(x, y) + \cdot T_{G \setminus e}(x, y){% endlatex %}           |

{% math proof %}Pro {% latex %}E = \emptyset{% endlatex %} jasné, všude je {% latex %}0{% endlatex %}. Jinak rozdělíme:

{% latex display %}T_G(x, y) = \underbrace{\sum_{F \subseteq E, e \not\in F} (x - 1)^{r(E) - r(F)} \cdot (y - 1)^{n(F)}}_{s_1} + \underbrace{\sum_{F \subseteq E, e \in F} (x - 1)^{r(E) - r(F)} \cdot (y - 1)^{n(F)}}_{s_2}{% endlatex %}

Stačí dokázat následující:
1. pokud {% latex %}e{% endlatex %} není most, tak {% latex %}s_1 = T_{G - e}(x, y){% endlatex %}
	- {% latex %}e{% endlatex %} není most, jeho odebráním se rank nezmění, jen dosadím...
2. pokud {% latex %}e{% endlatex %} je most, tak {% latex %}s_1 = (x - 1) \cdot T_{G - e}(x, y){% endlatex %}
	- {% latex %}e{% endlatex %} je most, jeho odebráním se rank zvětší o {% latex %}1{% endlatex %}, zase jen dosadím...
3. pokud {% latex %}e{% endlatex %} není smyčka, tak {% latex %}s_2 = T_{G \setminus e}(x, y){% endlatex %}
4. pokud {% latex %}e{% endlatex %} je smyčka, tak {% latex %}s_2 = (y - 1)T_{G \setminus e}(x, y){% endlatex %}

Poté pro větu stačí následující:
- {% latex %}e{% endlatex %} je most: (2) + (3)
- {% latex %}e{% endlatex %} je smyčka: (1) + (4)
- {% latex %}e{% endlatex %} není most ani smyčka: (1) + (3)

{% endmath %}

{% math definition: "chromatický polynom" %}multigrafu {% latex %}G = (V, E){% endlatex %} je funkce {% latex %}\mathrm{ch}_G(b): \mathbb{N}_0 \mapsto \mathbb{N}_0{% endlatex %}, kde pro {% latex %}b \in \mathbb{N}_0{% endlatex %} je {% latex %}\mathrm{ch}_G(b) := {% endlatex %} počet dobrých obarvení (posunutí udělá nové obarvení) {% latex %}G{% endlatex %} pomocí barev {% latex %}\left\{1, \ldots, b\right\}{% endlatex %}.
{% endmath %}
- pokud {% latex %}G{% endlatex %} má smyčku, pak {% latex %}\mathrm{ch}_G(b) = 0, \forall b{% endlatex %}

{% math theorem %}Pro každý multigraf {% latex %}G = (V, E){% endlatex %} platí
{% latex display %}\mathrm{ch}_G(b) = \left(-1\right)^{|V| + k(G)} \cdot b^{k(G)} \cdot T_G(1 - b, 0){% endlatex %}
{% endmath %}

### 10. přednáška

#### Formální mocniné řady
{% math definition %}Pro posloupnost reálných čísel {% latex %}a_0, a_1, \ldots{% endlatex %} je formální mocninná řada (FMŘ) zápis tvaru {% latex %}a_0 + a_1x^1 + a_2x^2 + \ldots = \sum_{i = 0}^{\infty} a_i x^i{% endlatex %}{% endmath %}
- {% latex %}\mathbb{R} \llbracket x \rrbracket \ldots{% endlatex %} všechny FMŘ nad {% latex %}x{% endlatex %}
- pro {% latex %}A(x) = a_0 + a_1 x + a_2x^2 + \ldots{% endlatex %} je {% latex %}[x^n]A(x) = a_n{% endlatex %}
- pro FMŘ {% latex %}A(x), B(x){% endlatex %} je
	- {% latex %}A(x) + B(x) = (a_0 + b_0) + (a_1 + b_1)x + (a_2 + b_2)x^2 + \ldots{% endlatex %}
	- {% latex %}A(x) \cdot B(x) = c_0 + c_1x + c_2x^2 + \ldots{% endlatex %}, kde {% latex %}c_n = a_0 b_n + a_1 b_{n - 1} + \ldots + a_{n - 1}b_1 + a_{n} b_0{% endlatex %} (konvoluce)

{% math fact %} {% latex %}\mathbb{R}\llbracket x \rrbracket{% endlatex %} tvoří (komutativní) okruh (máme {% latex %}+, \cdot, 0, 1{% endlatex %}){% endmath %}
- {% latex %}0 = A(x){% endlatex %} s nulovými koeficienty
- {% latex %}1 = A(x){% endlatex %} s {% latex %}a_0 = 1{% endlatex %} a zbytek nulové koeficienty

{% math fact %} {% latex %}\mathbb{R}\llbracket x \rrbracket{% endlatex %} tvoří vektorový postor (násobení konstantou je FMŘ pro {% latex %}a_0 = c{% endlatex %}{% endmath %}

{% math definition "převrácená hodnota" %} FMŘ {% latex %}A(x){% endlatex %} je taková FMŘ, že {% latex %}A(x) \cdot B(x) = 1{% endlatex %}{% endmath %}

- {% latex %}A(x) = c \ldots B(x) = \frac{1}{c}{% endlatex %}
- {% latex %}A(x) = x \ldots B(x){% endlatex %} není (muselo by být něco jako {% latex %}\frac{1}{x}{% endlatex %})
- {% latex %}A(x) = 1 - x \ldots B(x) = 1 + x + x^2 + \ldots{% endlatex %}
	- {% latex %}C(x) = A(x) \cdot B(x) = (1 + x + x^2 + \ldots) - (x + x^2 + x^3 + \ldots){% endlatex %}, kde {% latex %}[x^n]C(x){% endlatex %} bude nulové pro {% latex %}n \ge 1{% endlatex %} (požere se to), proto {% latex %}(1 + x + x^2 + \ldots) = \frac{1}{1 - x}{% endlatex %}

{% math lemma %}Nechť {% latex %}A(x) = \sum_{n = 0}^{\infty} a_n x^n{% endlatex %} je FMŘ. Potom {% latex %}\frac{1}{A(x)}{% endlatex %} existuje, právě když {% latex %}a_0 \neq 0{% endlatex %} (a pak je jednoznačně určena).{% endmath %}

{% math proof %}Hledejme inverz. Rozepsáním {% latex %}A(x) \cdot B(x) = 1 + 0x + 0x^2 + \ldots{% endlatex %} nám dává soustavu takovýchto rovnic, které mají jednoznačné řešení:

{% latex display %}
\begin{aligned}
	a_0 b_0 = 1 &\qquad b_0 = \frac{1}{a_0} \\
	a_0 b_1 + a_1b_0 = 0 &\qquad b_1 = \frac{1}{a_0}(-a_1 b_0)\\
	a_0 b_2 + a_1b_1 + a_2b_0 = 0 &\qquad b_2 = \frac{1}{a_0} (-a_1 b_1 - a_2b_2) \\
	                          &\;\;\;\vdots \\
\end{aligned}
{% endlatex %}
{% endmath %}

{% math definition "složení" %}{% latex %}A(x) = \sum a_nx^n, B(x) = \sum b_nx^n{% endlatex %} jsou FMŘ. Složení je {% latex %}A(B(x)) = a_0B(x)^0 + a_1B(x)^1 + \ldots{% endlatex %} {% endmath %}. Obecně je problém to zadefinovat, potřeboval bych znát hodnotu součtu, ale jde to, když:

1. {% latex %}A(x){% endlatex %} je polynom ({% latex %}\equiv \exists n_0 \in \mathbb{N}{% endlatex %} t. ž. {% latex %}\forall n \ge n_0: a_n = 0{% endlatex %})
{% latex display %}a_0 B(x)^0 + a_1B(x)^1 + a_2B(x)^2 + \ldots + \underbrace{a_{n_0}B(x)^{n_0} + \ldots}_{= 0}{% endlatex %}
2. {% latex %}b_0 = 0{% endlatex %}
	- chci ukázat, že součet {% latex %}\left[x^n\right]A(B(x)) = \left[x^n\right]a_0B(x)^0 + \left[x^n\right]a_1B(x)^1 + \ldots{% endlatex %} je konečný
		- {% latex %}\left[x^0\right]B(x) = b_0 = 0{% endlatex %}
		- {% latex %}B(x) = x \tilde{B}(x){% endlatex %} pro {% latex %}\tilde{B}(x){% endlatex %} FMŘ
		- {% latex %}B(x)^k = x^k \tilde{B}(x)^k{% endlatex %}, koeficient u {% latex %}x^{k - 1}, x^{k - 2}, \ldots, x^0{% endlatex %} je nulový, tedy všechny koeficienty {% latex %}\left[x^k\right]{% endlatex %} pro {% latex %}k > n{% endlatex %} jsou nulové

{% math definition: "derivace" %}FMŘ {% latex %}A(x){% endlatex %} značená {% latex %}\frac{d}{dx}A(x) = \sum a_{n + 1}(n + 1)x^n = a_1 + 2a_2x + 3a_3x^3 + \ldots{% endlatex %}{% endmath %}

{% math example %} Můžu mít také FMŘ více proměnných, např. {% latex %}A(x, y) = \sum_{n \ge 0, m \ge 0} a_{n, m} \cdot x^n \cdot y^m \in \mathbb{R}\llbracket x, y \rrbracket{% endlatex %}
{% endmath %}

#### Obyčejné vyvořující funkce
Nechť {% latex %}\mathcal{A}{% endlatex %} je množina, jejíž každý prvek {% latex %}\alpha \in \mathcal{A}{% endlatex %} má definovanout velikost {% latex %}|\alpha| \in \mathbb{N}_0{% endlatex %}, předpokládáme že {% latex %}\forall n \in \mathbb{N}_0{% endlatex %} je v {% latex %}\mathcal{A}{% endlatex %} konečně mnoho prvků velikosti {% latex %}n{% endlatex %}.
- {% latex %}\mathcal{A}_n = \left\{\alpha \in \mathcal{A} \mid |\alpha| = n\right\}, a_n = |\mathcal{A}_n|{% endlatex %}

Porom obyčejná vytvořující funkce pro {% latex %}\mathcal{A}{% endlatex %} je FMŘ {% latex display %}\mathrm{OVF}(\mathcal{A}) = \sum_{n \ge 0} a_n x^n{% endlatex %}

{% math example %} Jídla ({% latex %}\mathcal{J} = \mathcal{P} \cup \mathcal{H}{% endlatex %}):
- Polévky ({% latex %}\mathcal{P}{% endlatex %})
	- gulášová: {% latex %}30{% endlatex %}
	- knedlíčková: {% latex %}35{% endlatex %}
- Hlavní jídla ({% latex %}\mathcal{H}{% endlatex %})
	- guláš: {% latex %}100{% endlatex %}
	- řízek: {% latex %}100{% endlatex %}
	- smažák: {% latex %}90{% endlatex %}

- {% latex %}P(x) = \mathrm{OVF}(\mathcal{P}) = x^{30} + x^{35} {% endlatex %}
- {% latex %}H(x) = \mathrm{OVF}(\mathcal{H}) = x^{90} + 2x^{100} {% endlatex %}
- {% latex %}J(x) = P(x) + H(x){% endlatex %}

---

- (👀) {% latex %}\mathrm{OVF}(\mathcal{A} \cup \mathcal{B}) = \mathrm{OVF}(\mathcal{A}) + \mathrm{OVF}(\mathcal{B}){% endlatex %}
- (👀) {% latex %}\mathrm{OVF}(\mathcal{A}) \cdot \mathrm{OVF}(\mathcal{B}) = \mathrm{OVF}(\mathcal{A} \times \mathcal{B}){% endlatex %}
	- {% latex %}P(x) \cdot H(x) = {% endlatex %} kartézský součin dvojic (polívka, hlavní jídlo)
	- {% latex %}[x^{130}](J(x) \cdot J(x)) = {% endlatex %} počet uspořádaných dvojic jídel, které se sečtou na {% latex %}130{% endlatex %}

{% endmath %}

### 11. přednáška
#### Exponenciální vytvořující funkce
Chci dojít k {% latex %}L(x){% endlatex %}, což bude vytvořující funkce pro počet lesů na {% latex %}n{% endlatex %} vrcholech, pomocí {% latex %}S(x){% endlatex %} vytvořující funkce pro počet stromů na {% latex %}n{% endlatex %} vrcholech.

Nechť {% latex %}s_n{% endlatex %} je počet stromů na vrcholech {% latex %}\left\{1, \ldots, n\right\}{% endlatex %}
{% latex display %}S(x) = \sum_{n \ge 0} s_n \cdot \frac{x^n}{n!} \qquad \in \mathbb{R}\llbracket x \rrbracket{% endlatex %}

Nechť {% latex %}k_n{% endlatex %} je počet kružnic na vrcholech {% latex %}\left\{1, \ldots, n\right\}{% endlatex %}
{% latex display %}K(x) = \sum_{n \ge 0}  k_n \cdot \frac{x^n}{n!} {% endlatex %}

Definujeme {% latex %}A(x) = S(x) \cdot K(x){% endlatex %} a {% latex %}a_0, a_1, \ldots{% endlatex %} tak, aby {% latex %}A(x) = \sum_{n \ge 0} a_n \cdot \frac{x^n}{n!} {% endlatex %}

Potom platí, že {% latex %}a_n = \sum_{j = 0}^{n} \binom{n}{j} \cdot s_j \cdot k_{n - j}{% endlatex %}, tedy {% latex %}a_n = {% endlatex %} počet grafů na {% latex %}n{% endlatex %} vrcholech mající dvě komponenty souvislosti, z nichž jedna je strom a druhá kružnice:
{% latex display %}
\begin{aligned}
	\left[x^n\right]\left(S(x) \cdot K(x)\right) &= \sum_{j = 0}^{n} \left(\left[x^j\right] S(x)\right) \cdot \left(\left[x^{n - j}\right] K(x)\right) \\
	&= \sum_{j = 0}^{n} \frac{s_j}{j!} \cdot \frac{k_{n - j}}{(n - j)!} \\
	&= \sum_{j = 0}^{n} \frac{n!}{j!(n - j)!} \cdot \frac{1}{n!} \cdot s_j k_{n - j} \\
	&= \frac{1}{n!}\sum_{j = 0}^{n} \binom{n}{j} s_j k_{n - j} \\
	&= \left[x^n\right] A(x)
\end{aligned}
{% endlatex %}

Definujeme {% latex %}B(x) = S(x)^2{% endlatex %} a {% latex %}b_0, b_1, \ldots{% endlatex %} tak, aby {% latex %}B(x) = \sum_{n \ge 0} b_n \cdot \frac{x^n}{n!}{% endlatex %}
- počet způsobů, jak rozdělit vrcholy na červené a modré a vytvořit strom na každé barvě
{% latex display %}b_n = \sum_{j = 0}^{n} \binom{n}{j} \cdot s_j \cdot s_{n - j}{% endlatex %}

Dále definujeme hromadu dalších věcí:
- {% latex %}C(x){% endlatex %} jako {% latex %}c_n = \frac{b_n}{2}{% endlatex %}, abychom měli počet lesů se dvěma komponentami, tedy {% latex %}C(x) = \frac{1}{2} B(x) = \frac{1}{2} S^2(x){% endlatex %}.
- {% latex %}D(x) = S^k(x){% endlatex %}, tedy {% latex %}d_n{% endlatex %} je počet uspořádaných {% latex %}k{% endlatex %}-tic stromů tvořící rozklad vrcholů
- {% latex %}E(x) = \frac{S^k(x)}{k!}{% endlatex %}, tedy {% latex %}e_x{% endlatex %} je počet lesů s {% latex %}k{% endlatex %} komponentami

Konečně vyjádříme {% latex display %}L(x) = 1 + S(x) + \frac{S^2(x)}{2!} + \ldots = \sum_{n \ge 0} \frac{S^n(x)}{n!} = \mathrm{exp}(S(x)) = e^{S(x)}{% endlatex %}

---

V následujících definicích a pozorováních je _takovýhle text_ odkaz na to, co si pod tím představovat v rámci minulého příkladu.

{% math definition %}Mějme množinu {% latex %}\mathcal{A}{% endlatex %} (_všechny konečné stromy s očíslovaňými vrcholy_), předpokladejme:
1. každý prvek {% latex %}\alpha \in \mathcal{A}{% endlatex %} (_nějaký strom_) má množinu vrcholů (_vrcholů_) {% latex %}V(\alpha) \subseteq \mathbb{N}, V(\alpha){% endlatex %} konečná
2. pro každou konečnou {% latex %}V \subseteq \mathbb{N}{% endlatex %} existuje konečně mnoho {% latex %}\alpha \in \mathcal{A}{% endlatex %} t. ž. {% latex %}V(\alpha) = V{% endlatex %} 
	- (_existuje konečné množství stromů_)
3. pro dvě konečné množiny {% latex %}V, W \subseteq \mathbb{N}{% endlatex %} t. ž. {% latex %}|V| = |W|{% endlatex %} platí, že počet {% latex %}\alpha \in \mathcal{A}{% endlatex %} t. ž. {% latex %}V(\alpha) = V{% endlatex %} je stejný jako {% latex %}\alpha \in \mathcal{A}{% endlatex %} t. ž. {% latex %}V(\alpha) = W{% endlatex %} (co do počtu, záleží jen na velikosti množiny vrcholů)
	- (_dvě stejně velké množiny vrcholů mají stejný počet stromů_)

Potom **exponenciální vytvořující funkce** pro {% latex %}\mathcal{A}{% endlatex %} je {% latex display %}\mathrm{EVF(\mathcal{A})} = \sum_{n \ge 0} a_n \frac{x^n}{n!}{% endlatex %}kde {% latex display %}a_n = \#\ \alpha \in \mathcal{A} \text{ t. ž. } V(\alpha) = \left\{1, \ldots, n\right\}{% endlatex %}
{% endmath %}

{% math observation %}Nechť {% latex %}A(x){% endlatex %} je {% latex %}\mathrm{EVF(\mathcal{A})}, B(x) = \mathrm{EVF}(\mathcal{B}){% endlatex %}, potom:
1. pokud {% latex %}\mathcal{A}, \mathcal{B}{% endlatex %} jsou disjunktní (příklad výše), pak {% latex %}A(x) + B(x){% endlatex %} je {% latex %}\mathrm{EVF}(\mathcal{A} \cup \mathcal{B}){% endlatex %}
	- stejné jako u {% latex %}\mathrm{OFV}{% endlatex %}, protože {% latex %}\left[x^n\right] \left(A(x) + B(x)\right) = \frac{a_n}{n!} + \frac{b_n}{n!} = \frac{a_n + b_n}{n!}{% endlatex %}
2. {% latex %}A(x) \cdot B(x) = \sum c_n \frac{x^n}{n!}{% endlatex %}, kde {% latex %}c_n{% endlatex %} je počet uspořádaných dvojic {% latex %}\left(\alpha, \beta\right){% endlatex %} t.ž. {% latex %}\alpha \in \mathcal{A}, \beta \in \mathcal{B}, V(\alpha) \cup V(\beta) = \left\{1, \ldots, n\right\}{% endlatex %} (tvoří rozklad)
3. {% latex %}A^k(x) = \sum d_n \frac{x^n}{n!}{% endlatex %}, kde {% latex %}d_n{% endlatex %} je počet uspořádaných {% latex %}k{% endlatex %}-tic {% latex %}(\alpha_1, \ldots, \alpha_n){% endlatex %}, kde
{% latex display %}\alpha_1, \ldots, \alpha_n \in \mathcal{A} \text{ t.ž. } V(\alpha_1) \cup \ldots \cup V(\alpha_k) = \left\{1, \ldots, n\right\} \qquad \star{% endlatex %}
4. pokud {% latex %}V(\alpha) \neq \emptyset, \forall \alpha \in \mathcal{A}{% endlatex %}, pak {% latex display %}\frac{A^k(x)}{k!} = \sum e_n \frac{x^n}{n!}{% endlatex %}kde {% latex %}e_n{% endlatex %} je počet {% latex %}k{% endlatex %}-prvkových množin splňujících {% latex %}\star{% endlatex %}
5. pokud {% latex %}\forall \alpha \in \mathcal{A}: V(\alpha) \neq \emptyset{% endlatex %}, pak {% latex display %}\mathrm{exp}(\mathcal{A}(x)) = e^{A(x)} = 1 + A(x) + \frac{A^2(x)}{2} + \ldots = \sum_{n \ge 0} f_n \frac{x^n}{n!}{% endlatex %} kde {% latex %}f_n{% endlatex %} je počet množin {% latex %}\left\{\alpha_1, \ldots, \alpha_k\right\} \subseteq \mathcal{A}{% endlatex %}, kde {% latex %}V(\alpha_1) \cup \ldots \cup V(\alpha_{k}) = \left\{1, \ldots, n\right\}{% endlatex %}

{% endmath %}

#### Groupy a Burnside
{% math definition "akce grupy" %}nechť {% latex %}A{% endlatex %} je množina, nechť {% latex %}\Gamma{% endlatex %} je grupa, {% latex %}1_\Gamma{% endlatex %} její neutrální prvek. Potom akce grupy {% latex %}\Gamma{% endlatex %} na množině {% latex %}A{% endlatex %} je binární operace {% latex %}\cdot: \Gamma \times A \mapsto A{% endlatex %} t.ž.
1. {% latex %}\forall x \in A: 1_\Gamma \cdot x = x{% endlatex %}
2. {% latex %}\forall \gamma, \delta \in \Gamma, \forall x \in A: \gamma \cdot (\delta \cdot x) = (\gamma \delta) \cdot x{% endlatex %}
	- pozor, {% latex %}\cdot{% endlatex %} a {% latex %}\gamma\delta{% endlatex %} jsou jiné operace
{% endmath %}

{% math observation %}Pokud {% latex %}\gamma \in \Gamma, \gamma^{-1}{% endlatex %} je inverzní prvek k {% latex %}\gamma{% endlatex %}, potom {% latex %}\forall x, y \in A: \gamma \cdot x = y \iff \gamma^{-1} \cdot y = x{% endlatex %}{% endmath %}

{% math consequence %}{% latex %}\forall p \in \Gamma:{% endlatex %} zobrazení {% latex %}x \mapsto p \cdot x{% endlatex %} je bijekce {% latex %}A \longleftrightarrow A{% endlatex %}{% endmath %}

### 12. přednáška
{% math definition: "množina pevných bodů" %}{% latex %}\gamma \in \Gamma{% endlatex %}, značená {% latex %}\mathrm{Fix}(\gamma) = \left\{x \in A \mid \gamma x = x\right\}{% endlatex %}{% endmath %}

{% math definition: "stabilizátor" %} prvku {% latex %}x \in A{% endlatex %} je {% latex %}\mathrm{Stab}(x) = \left\{\gamma \in \Gamma \mid \gamma x = x\right\}{% endlatex %}{% endmath %}

{% math observation %}{% latex %}\gamma \in \Gamma, x \in A: \gamma \in \mathrm{Stab}(x) \iff x \in \mathrm{Fix}(\gamma) \iff \gamma x = x{% endlatex %}{% endmath %}

{% math observation %}{% latex %}\mathrm{Stab}(x){% endlatex %} je podgrupa {% latex %}\Gamma{% endlatex %}
- {% latex %}1_\Gamma \in \mathrm{Stab}(x){% endlatex %}, protože {% latex %}1_\Gamma x = x{% endlatex %}
- {% latex %}\gamma \in \mathrm{Stab}(x) \implies \gamma^{-1} \in \mathrm{Stab}(x){% endlatex %} z pozorování {% latex %}\gamma x = y \iff x = \gamma^{-1}y{% endlatex %}
- {% latex %}\gamma, \delta \in \mathrm{Stab}(x) \implies \gamma x = x, \delta x = x{% endlatex %}, dosazením dostávám {% latex %}\gamma \delta x = x{% endlatex %}
{% endmath %}

Prvky {% latex %}x, y \in A{% endlatex %} jsou ekvivalentní (značím {% latex %}x \sim_{\Gamma} y{% endlatex %}, pokud {% latex %}\exists \gamma \in \Gamma{% endlatex %} t.ž. {% latex %}\gamma x = y{% endlatex %}
- (👀) {% latex %}\sim_{\Gamma}{% endlatex %} je to ekvivalence:
	- reflexivní -- {% latex %}x = 1_\Gamma x{% endlatex %}
	- symetrická -- {% latex %}\gamma x = y \iff \gamma^{-1}y = x{% endlatex %}
	- transitivní -- {% latex %}\gamma x = y \land \gamma y = z \implies (\delta \gamma)x = z{% endlatex %}

{% math definition: "orbita" %} obsahující prvek {% latex %}x \in A{% endlatex %} je množina {% latex display %}\left[x\right]_{\Gamma} = \left\{y \in A \mid x \sim_\Gamma y\right\} = \left\{\gamma x \mid \gamma \in \Gamma\right\}{% endlatex %}
možinu orbit značíme {% latex %}A / \Gamma{% endlatex %}.
{% endmath %}

{% math example %}Koláčky (mák, tvaroh povidla).

{% latex display %}\mathcal{K} = \left\{\boxed{a{b\atop c} d} \mid a, b, c, d \in \left\{T, M, P\right\}\right\} \qquad |\mathcal{K}| = 3^4 = 81{% endlatex %}

{% latex display %}\Gamma = \left\{\text{otočení o násobky 90$\degree$ mod 360$\degree$}\right\} = \left\{0\degree, 90\degree, 180\degree, 270\degree \right\}{% endlatex %}

- akce odpovídají otočením koláčku.
- {% latex %}\mathrm{Fix}(90\degree) = \left\{\boxed{a{b\atop b} a} \mid a, b \in \left\{T, M, P\right\}\right\}{% endlatex %}
- {% latex %}\mathrm{Stab\left(\boxed{M{T\atop P} M}\right)} = \left\{0\degree\right\}{% endlatex %}
- {% latex %}\left[\boxed{M{T\atop P} M}\right] = \left\{\boxed{M{T\atop P} M}, \boxed{P{M\atop M} T}, \boxed{M{P\atop T} M}, \boxed{T{M\atop M} P}\right\}{% endlatex %}
{% endmath %}

{% math lemma "o orbitě stabilizátoru" %}Nechť {% latex %}\Gamma{% endlatex %} je konečná grupa s akcí na množině {% latex %}A{% endlatex %}. Potom {% latex display %}\forall x \in A: |\mathrm{Stab(x)}| \cdot |\left[x\right]| = |\Gamma|{% endlatex %} {% endmath %}

{% math definition %}Nechť množina {% latex %}\mathrm{Map}(x, y){% endlatex %} je množina akcí {% latex %}a{% endlatex %}, pro které {% latex %}a.x = y{% endlatex %}. Pro akce {% latex %}\sigma \in \mathrm{Map}(x, y){% endlatex %} pomocí {% latex %}\sigma a \sigma^{-1}{% endlatex %} lze definovat bijekci mezi {% latex %}\mathrm{Map}(x, x){% endlatex %}. Poté {% latex display %}\forall x \in A, |\Gamma| = \sum_{y \in [x]} |\mathrm{Map}(x, y)| = \sum_{y \in [x]} |\mathrm{Stab}(x)| = |[x]| |\mathrm{Stab}(x)|{% endlatex %}
{% endmath %}

{% math theorem "Bursideovo lemma" %}Nechť {% latex %}\Gamma{% endlatex %} je konečná grupa s akcí na {% latex %}A{% endlatex %}
{% endmath %}
1. (jednoduchá) pokud {% latex %}A{% endlatex %} je konečná, pak {% latex display %}|A / \Gamma| = \frac{1}{|\Gamma} \sum_{\gamma \in \Gamma} |\mathrm{Fix}(\gamma)|{% endlatex %} {% latex %}={% endlatex %} počet orbit je roven „průměrnému počtu pervných bodů“ 
2. Nechť každá orbita {% latex %}o \in A / \Gamma{% endlatex %} má přiřazenou váhu {% latex %}w(o){% endlatex %}. Potom {% latex display %}\sum_{o \in A/\Gamma} w(o) = \frac{1}{|\Gamma|} \sum_{\gamma \in \Gamma} \sum_{x \in \mathrm{Fix}(\gamma)} w([x]){% endlatex %}

{% math proof %} {% latex %}(2) \Rightarrow (1){% endlatex %}, když jsou váhy {% latex %}1{% endlatex %}.

{% latex %}(2){% endlatex %} -- dvojím počítáním {% latex %}s := \sum_{\gamma, x} \in \Gamma \times A, \gamma x = x{% endlatex %}

{% latex display %}s = \sum_{\gamma \in \Gamma} \sum_{x \in \mathrm{Fix}(\gamma)} w([x]){% endlatex %}

{% latex display %} \begin{aligned}
	s &= \sum_{x \in A} \sum_{\gamma \in \mathrm{Stab}(x)} w([x]) \qquad w([x])\text{ závisí pouze na váze orbity}\\
	  &= \sum_{o \in A / \Gamma} \sum_{x \in o} \sum_{\gamma \in \mathrm{Stab}(x)} w(o) \qquad \text{vnitřní suma závisí na $\mathrm{Stab}(x)$} \\
	  &= \sum_{o \in A / \Gamma} \sum_{x \in o} |\mathrm{Stab}(x)| w(o) \qquad \text{lemma o orbitě a stabilizátoru} \\
	  &= \sum_{o \in A / \Gamma} \sum_{x \in o} \frac{|\Gamma|}{|o|} w(o) \qquad \text{obsah sumy závisí na velikosti orbity} \\
	  &= \sum_{o \in A / \Gamma} |o| \frac{|\Gamma|}{|o|} w(o) \\
	  &= |\Gamma| \sum_{o \in A / \Gamma} w(o) \\
\end{aligned} {% endlatex %}
{% endmath %}

Poté první a druhý způsob dám do rovnosti, vydělím velikostí grupy a hotovo.

{% math example %}
Koláčky na steroidech: množina koláčků {% latex %}\mathcal{R}{% endlatex %}, v každé části nezáporný počet rozinek, akce jsou stejné.

Pro {% latex %}k \in \mathbb{N}_0, a_k = {% endlatex %} počet orbit, jejichž koláčky mají celkem {% latex %}k{% endlatex %} rozinek. Cíl je získat vzorec pro {% latex %}A(x) = \sum_{n \ge 0} a_n x^n{% endlatex %}

Použijeme obecnější Burnsideovo lemma. Chceme, aby {% latex display %}A(x) = \sum_{o \in A/\Gamma} w(o) = \frac{1}{|\Gamma|} \sum_{\gamma \in \Gamma} \sum_{x \in \mathrm{Fix}(\gamma)} w([x]){% endlatex %}

Váhu orbity s {% latex %}k{% endlatex %} rozinkami nastavíme na {% latex %}x^k{% endlatex %}. Pro {% latex %}q \in \mathcal{R}{% endlatex %} označím {% latex %}r(q){% endlatex %} počet rozinek v {% latex %}q{% endlatex %}, {% latex %}w([q]) = x^{r(q)}{% endlatex %}.

| {% latex %}\gamma{% endlatex %}                                   | {% latex %}1_\Gamma{% endlatex %}                       | {% latex %}90\degree{% endlatex %}, {% latex %}270\degree{% endlatex %} | {% latex %}180\degree{% endlatex %}                       |
| ---                                                               | ---                                                     | ---                                                                     | ---                                                       |
| {% latex %}\mathrm{Fix}(\gamma){% endlatex %}                     | {% latex %}\mathcal{R}{% endlatex %}                    | všude je stejný počet rozinek                                           | protější strany mají stejný počet rozinek                 |
| {% latex %}\sum_{q \in \mathrm{Fix}(\gamma)} w([q]){% endlatex %} | {% latex %}\left(\frac{1}{1 - x}\right)^4{% endlatex %} | {% latex %}\frac{1}{1 - x^4}{% endlatex %}                              | {% latex %}\left(\frac{1}{1 - x^2}\right)^2{% endlatex %} |

Vytvořující funkce z tabulky jsme odvodili následně:

{% latex display %}\sum_{q \in \mathrm{Fix}(\gamma) = \mathcal{R}} = \sum_{q \in \mathcal{R}} x^{r(q)} = \sum_{(a, b, c, d) \in \mathbb{N}_0^4} x^{a + b + c + d} = \left(\sum_{a \in \mathbb{N}_0} x^a\right)^4 = \left(\frac{1}{1 - x}\right)^4{% endlatex %}
{% latex display %}\sum_{q \in \mathrm{Fix}(\gamma) = \left\{(a, a, a, a) \mid a \in \mathbb{N}_0\right\}} = \sum_{a \in \mathbb{N}_0} x^{4a} = \frac{1}{1 - x^4}{% endlatex %}
{% latex display %}\sum_{q \in \mathrm{Fix}(\gamma) = \left\{(a, b, a, b) \mid a, b \in \mathbb{N}_0\right\}} = \left(\sum_{a \in \mathbb{N}_0} x^{2a}\right) \left(\sum_{b \in \mathbb{N}_0} x^{2b}\right) = \left(\frac{1}{1 - x^2}\right)^2{% endlatex %}

Tedy dostáváme, že {% latex display %}A(x) = \frac{1}{4} \left(\left(\frac{1}{1 - x}\right)^4 + 2 \left(\frac{1}{1-x^4}\right) + \left(\frac{1}{1 - x^2}\right)^2\right){% endlatex %}

{% endmath %}

### 13. přednáška

#### Extremální teorie grafů a hypergrafů
{% math notation %}pro graf {% latex %}H{% endlatex %} označím {% latex %}\mathrm{ex}(n, H){% endlatex %} největší {% latex %}m{% endlatex %} t.ž. existuje graf {% latex %}G{% endlatex %} s {% latex %}n{% endlatex %} vrcholy, {% latex %}m{% endlatex %} hranami a neobsahující {% latex %}H{% endlatex %} jako podgraf.
{% endmath %}
- {% latex %}\mathrm{ex}(n, K_3) = |E(K_{\left\lfloor \frac{n}{2} \right\rfloor, \left\lceil \frac{n}{2} \right\rceil})| = \left\lfloor \frac{n}{2} \right\rfloor \cdot \left\lceil \frac{n}{2} \right\rceil \cong n^2{% endlatex %}
- {% latex %}\mathrm{ex}(n, C_4) = \mathcal{O}(n^{3/2} = \mathcal{O}(n \sqrt{n}){% endlatex %}
	- viz. poznámky z [Kombinatoriky a Grafů I](/lecture-notes/kombinatorika-a-grafy-i/#grafy-bez-ckc_kck)

{% math definition %}{% latex %}k, n \in \mathbb{N}{% endlatex %}, označme {% latex %}T_k(n){% endlatex %} úplný {% latex %}k{% endlatex %}-partitní graf na {% latex %}n{% endlatex %} vrcholech, jehož všechny partity mají velikost {% latex %}\left\lfloor \frac{n}{k} \right\rfloor{% endlatex %} nebo {% latex %}\left\lceil \frac{n}{k} \right\rceil{% endlatex %}. Nechť {% latex %}t_k(n) = |E(T_k(n))|{% endlatex %}{% endmath %}
- {% latex %}k{% endlatex %}-partitní je to samé jako {% latex %}k{% endlatex %}-obarvitelný ({% latex %}\Chi(G){% endlatex %})
- partity mohou být i prázdné -- {% latex %}k{% endlatex %}-partitní je i {% latex %}k'{% endlatex %}-partitní, pro {% latex %}k' \ge k{% endlatex %}
- úplný {% latex %}k{% endlatex %}-partitní -- každé {% latex %}2{% endlatex %} partity jsou úplný bipartitní graf

{% math observation %}{% latex %}\forall r \in \mathbb{N}, r \ge 2: \mathrm{ex}(n, K_r) \ge t_{r - 1}(n){% endlatex %}, protože {% latex %}T_{r - 1}(n){% endlatex %} neobsahuje {% latex %}K_r{% endlatex %} (z každé nezávislé množiny si klika vezme {% latex %}\le 1{% endlatex %} vrchol) {% endmath %}

{% math lemma "1" %}Každý {% latex %}k{% endlatex %}-partitní graf na {% latex %}n{% endlatex %} vrcholech má nanejvýš {% latex %}t_{k}(n){% endlatex %} hran.{% endmath %}

{% math proof %}Nechť {% latex %}G = (V, E){% endlatex %} je {% latex %}k{% endlatex %}-partitní, {% latex %}P_1, \ldots, P_k{% endlatex %} jsou jeho partity. Navíc {% latex %}|P_1| \le |P_2| \le \ldots \le |P_k|{% endlatex %}
- buď {% latex %}|P_k| \le |P_{1}| + 1{% endlatex %}, pak {% latex %}G \cong T_k(n){% endlatex %}
- jinak pro spor {% latex %}|P_k| \ge |P_1| + 2{% endlatex %}
	- idea důkazu je ta, že vezmeme vrchol z poslední partity a přesuneme ho do první
	- nechť {% latex %}x \in P_k{% endlatex %}, nechť {% latex %}\tilde{G}{% endlatex %} je úplný {% latex %}k{% endlatex %}-partitní s partitami {% latex %}P_1 \cup \left\{x\right\}, P_2, P_3, \ldots, P_{k} \setminus \left\{x\right\}{% endlatex %}; potom {% latex %}|E(\tilde{G})| > |E(G)|{% endlatex %}, což je spor:
		- stupně pro {% latex %}P_2, \ldots, P_k{% endlatex %} se nemění (vrcholy stále vidí {% latex %}x{% endlatex %}, jen je teď jinde)
		- stupně pro {% latex %}P_1{% endlatex %} klesne o {% latex %}1{% endlatex %} (vrcholy přestanou vidět {% latex %}x{% endlatex %})
		- stupně pro {% latex %}P_k \setminus \left\{x\right\}{% endlatex %} vzroste o {% latex %}1{% endlatex %} (vrcholy začnou vidět {% latex %}x{% endlatex %})
		- stupně pro {% latex %}x{% endlatex %} vzroste alespoň o {% latex %}1{% endlatex %} ({% latex %}x{% endlatex %} přestane vidět {% latex %}P_1{% endlatex %} a začne vidět {% latex %}P_k{% endlatex %})
{% endmath %}

{% math lemma "2" %}Nechť {% latex %}G = (V, E){% endlatex %} je graf neobsahující {% latex %}K_r{% endlatex %} jako podgraf. Potom {% latex %}\exists H = (V, E_H){% endlatex %} {% latex %}(r-1){% endlatex %}-partitní t.ž. {% latex %}\deg_G(x) \le \deg_H(x){% endlatex %} (a tudíž {% latex %}|E(G)| \le |E(H)|{% endlatex %}){% endmath %}

{% math proof %}indukcí podle {% latex %}r{% endlatex %}
- {% latex %}r = 2 \implies G{% endlatex %} neobsahuje {% latex %}K_2{% endlatex %} a je tedy nemá hrany; {% latex %}G = H{% endlatex %} splňuje tvrzení (celé tvoří jednu partitu)
- {% latex %}r > 2{% endlatex %}: {% latex %}G{% endlatex %} neobsahuje {% latex %}K_r{% endlatex %}:

Nechť {% latex %}x \in V(G){% endlatex %} je vrchol max. stupně v {% latex %}G{% endlatex %}
- {% latex %}S = N_G(x){% endlatex %} (sousedství)
- {% latex %}G_S = G\left[S\right]{% endlatex %} (podgraf indukovaný {% latex %}S{% endlatex %})
	- {% math observation %}{% latex %}G_S{% endlatex %} neobsahuje {% latex %}k_{r - 1}{% endlatex %}, jinak {% latex %}G\left[S \cup \left\{x\right\}\right]{% endlatex %} obsahuje {% latex %}k_r{% endlatex %}{% endmath %} 
	- využijeme ip: {% latex %}\exists (r - 2){% endlatex %}-partitní graf {% latex %}H_S = (S, E_{H_{S}}){% endlatex %}
		- splňuje (dle IP), že {% latex %}\forall y \in s: \deg_{H_S} (y) \ge \deg_{G_S}(y){% endlatex %}
		- {% latex %}V \setminus S{% endlatex %} zadefinuji jako ({% latex %}(r-1){% endlatex %}.) partitu a vše patřičně spojím, čímž získám {% latex %}H{% endlatex %}

{% xopp lol %}

Ověříme {% latex %}\forall y \in V: \deg_G(x) \le \deg_H(x){% endlatex %}
1. {% latex %}y \in V \setminus S: \deg_H(y) = |S| = \deg_H(x) = \deg_G(x) \ge \deg_G(y){% endlatex %} ({% latex %}x{% endlatex %} je vrchol s největším stupněm)
2. {% latex %}y \in S: \deg_H(y) = \deg_{H_S} + |V \setminus S| \overset{\mathrm{IP}}{\ge} \deg_{G_S}(y) + |V \setminus S| \ge \deg_G(y){% endlatex %}
	- rozdělili jsme to na dva případy podle toho, co vidí uvnitř a co vně {% latex %}S{% endlatex %}
	- poslední nerovnost plyne z toho, že {% latex %}y{% endlatex %} v {% latex %}G{% endlatex %} vidí sousedy v {% latex %}G_S{% endlatex %} + nanejvýš všechny z {% latex %}V \setminus S{% endlatex %}

{% endmath %}

{% math theorem "Turán, 1941" %}{% latex %}\forall r \ge 2: \mathrm{ex}(n, K_r) = t_{r - 1}(n){% endlatex %}{% endmath %}

{% math proof %} Vezmu {% latex %}G{% endlatex %} nějaký graf bez {% latex %}K_r{% endlatex %}.

- už jsme (v pozorování výše) viděli {% latex %}\mathrm{ex}(n, K_r) \ge t_{r - 1}(n){% endlatex %} (protože {% latex %}T_{r - 1}(n){% endlatex %} neobsahuje {% latex %}K_r{% endlatex %})
- dle tvrzení (2) {% latex %}\exists (r-1){% endlatex %}-partitní graf {% latex %}H{% endlatex %} t.ž. {% latex %}|E(G) | \le |E(H)|{% endlatex %}
- dle tvrzení (1) je {% latex %}|E(H)| \le t_{r - 1} (n) \Rightarrow |E(G)| \le t_{r - 1}(n) \Rightarrow \mathrm{ex}(n, K_r) \le t_{r - 1}(n){% endlatex %}

Spojení odhadů dává rovnost.
{% endmath %}

{% math remark %}{% latex %}t_k(n) = \frac{k-1}{k} \binom{n}{2} + \mathcal{O}(n) = \frac{k - 1}{2k} n^2 + \mathcal{O}(n){% endlatex %}{% endmath %}

---

{% math definition %}pro graf {% latex %}H: \mathrm{ex}_\preceq(n, H){% endlatex %} je maximalní počet hran grafu {% latex %}G{% endlatex %} na {% latex %}N{% endlatex %} vrcholech bez {% latex %}H{% endlatex %} jako minoru.{% endmath %}

{% math observation %}{% latex %}\mathrm{ex}(n, H) \ge \mathrm{ex}_\preceq(n, H){% endlatex %}, protože graf bez {% latex %}H{% endlatex %}-minoru nemá ani {% latex %}H{% endlatex %}-podgraf (obráceně platit nemusí).{% endmath %}

{% math observation %}{% latex %}\mathrm{ex}_\preceq(n, K_3) = n - 1{% endlatex %} (dostávám stromy!){% endmath %}

{% math theorem %}{% latex %}\forall r \ge 3 \exists c_r > 0: \forall n: \mathrm{ex}_\preceq(n, K_r) < c_r \cdot n{% endlatex %}{% endmath %}
- jinými slovy: každý graf {% latex %}G = (V, E){% endlatex %} s {% latex %}|E| \ge c_r \cdot n{% endlatex %} obsahuje {% latex %}K_r{% endlatex %}-minor
- ještě jinými slovy: grafy, kterým zakážeme {% latex %}K_r{% endlatex %}-minor mají lineární počet hran (pro nějakou konstantu {% latex %}c_r{% endlatex %} závisející pouze na {% latex %}r{% endlatex %})

{% math proof %}dokážeme pro {% latex %}c_r = 2^{r - 3}{% endlatex %}, indukcí dle {% latex %}r{% endlatex %}
- základ {% latex %}r = 3{% endlatex %}, což jsou lesy a víme, že platí
- {% latex %}r > 3{% endlatex %}, sporem
	- {% latex %}\exists G = (V, E){% endlatex %} neobsahující {% latex %}K_r{% endlatex %}-minor ale {% latex %}|E| \ge c_r \cdot |V|{% endlatex %} a zároveň nejmenší pro {% latex %}|V| + |E|{% endlatex %}
	- pokud {% latex %}G' = (V', E'){% endlatex %} je vlastní minor {% latex %}G{% endlatex %}, tak {% latex %}|E'| < c_r \cdot |V'|{% endlatex %}, jinak bychom zvolili {% latex %}G'{% endlatex %}

**Pomocné tvrzení:** {% latex %}\forall \left\{x, y\right\} = e \in E{% endlatex %} platí {% latex %}|N(x) \cap N(y)| \ge c_r{% endlatex %}

{% math proof %}Vezmu {% latex %}G' = G.e{% endlatex %}
- {% latex %}|E| \ge c_r \cdot |V|{% endlatex %} (protože {% latex %}G{% endlatex %} je protipříklad)
- {% latex %}|E'| < c_r \cdot |V'| = c_r (|V| - 1){% endlatex %} (protože {% latex %}G'{% endlatex %} není protipříklad)

Odečtem nerovností máme {% latex %}|E| - |E'| > c_r{% endlatex %}. Navíc {% latex %}|E| - |E'| = 1 + |N(x) \cap N(y)|{% endlatex %} (zanikají hrany do společných sousedů a navíc hrana {% latex %}e{% endlatex %}), dosazením dostáváme hledanou nerovnost.
{% endmath %}

K důkazu původního vyberu {% latex %}x \in V(G){% endlatex %}, {% latex %}S = N_G(x), G_S = G\left[S\right]{% endlatex %}.
- dle pomocného tvrzení {% latex %}\forall y \in S: \deg_{G_S}(y) \ge c_r{% endlatex %}, jelikož všichni sousedé {% latex %}x{% endlatex %} leží v {% latex %}S{% endlatex %}.
- {% latex %}|E(G_S)| \ge \frac{c_r}{2} \cdot |S| = \frac{2^{r - 3}}{2} |S| = c_{r - 1} |S|{% endlatex %}
	- dle IP musí {% latex %}G_S{% endlatex %} obsahovat {% latex %}K_{r - 1}{% endlatex %} minor a ten spolu s {% latex %}x{% endlatex %} tvoří v {% latex %}G{% endlatex %} {% latex %}K_r{% endlatex %}-minor, což je spor

{% math reminder %}odhad byl dost hrubý, věta platí dokonce pro {% latex %}c_r = \mathcal{O}(r \cdot \sqrt{\log r}{% endlatex %}{% endmath %}
{% endmath %}

---

{% math definition %}{% latex %}k{% endlatex %}-uniformní hypergraf je dvojice {% latex %}(V, E){% endlatex %}, kde {% latex %}E \subseteq \binom{V}{k}{% endlatex %}{% endmath %}
- {% latex %}f(k, n) :={% endlatex %} max. {% latex %}m{% endlatex %} t.ž. {% latex %}\exists{% endlatex %} {% latex %}k{% endlatex %}-uniformní hypergraf {% latex %}H = (V, E){% endlatex %} t.ž. {% latex %}|V| = n, |E| = m{% endlatex %} a {% latex %}E{% endlatex %} je „pronikající systém množin“ (t.j. {% latex %}\forall e, e' \in E: e \cap e' \neq \emptyset{% endlatex %}
	- je dobré si rozmyslet, že braní všech hran nemusí fungovat (musí se protínat všechny dvojice)!

{:.rightFloatBox}
<div markdown="1">
{% xopp slun %}
</div>
{% math observation %} rozebereme několik případů:
- {% latex %}k > n: f(k, n) = 0{% endlatex %}, protože neexistují hyperhrany
- {% latex %}k \le n < 2k: f(k, n) = \binom{n}{k}{% endlatex %}, protože každé dvě množiny z {% latex %}\binom{V}{k}{% endlatex %} se protínají
- {% latex %}n \ge 2k: f(k, n) \ge \binom{n - 1}{k - 1}{% endlatex %} -- konstrukce, kde {% latex %}E = \left\{\left\{1\right\} \cup e' \mid e' \in \binom{\left\{2, \ldots, n\right\}}{k - 1}\right\}{% endlatex %}
	- „slunečnicová“ proto, že vezmeme jeden střed a poté hrany na zbylých vrcholech
{% endmath %}

{% math theorem "Erdös-Ko-Rado, 196*" %}{% latex %}\forall k, n \in \mathbb{N}: n \ge 2k \implies f(k, n) = \binom{n - 1}{k - 1}{% endlatex %}{% endmath %}

{% math proof %} dokazujeme dva odhady:

- dolní odhad {% latex %}f(k, n) \ge \binom{n - 1}{k - 1}{% endlatex %} ze slunečnicové konstrukce
- horní odhad {% latex %}f(k, n) \le \binom{n - 1}{k - 1}{% endlatex %}: máme {% latex %}H = (V, E){% endlatex %} {% latex %}k{% endlatex %}-uniformní hypergraf t.ž. {% latex %}E{% endlatex %} je protínající systém množin

{% math definition %}cyklické pořadí {% latex %}\left\{1, \ldots, n\right\}{% endlatex %} je nějaká {% latex %}1{% endlatex %}-cyklová permutace {% latex %}\left\{1, \ldots, n\right\}{% endlatex %}{% endmath %}
- {% latex %}k{% endlatex %}-intervaly (v tomhle příkladě {% latex %}3{% endlatex %}-intervaly) permutace {% latex %}C = (3, 1, 5, 4, 2, 7, 6, 8){% endlatex %} jsou {% latex %}315, 154, 542, 768, 683, 831{% endlatex %}

{% math observation %}intervalů daného pořadí {% latex %}C{% endlatex %} je {% latex %}n{% endlatex %}{% endmath %}

{% math observation %}cyklických pořadí je {% latex %}(n - 1)!{% endlatex %}
- kvůli tomu, že libovolnou permutaci můžu posunout o {% latex %}n{% endlatex %} míst a stále to bude stejný cyklus
{% endmath %}

{% math observation %}pokud {% latex %}e = \left\{a_1, \ldots, a_k\right\}{% endlatex %} je vůči {% latex %}C{% endlatex %} interval, pak {% latex %}\exists \le k - 1{% endlatex %} dalších hran {% latex %}e'{% endlatex %} t.ž. jsou intervaly vůči {% latex %}C{% endlatex %}{% endmath %}

{% math proof %}Může nastat vždy právě jeden z následujících případů, protože z předpokladu je {% latex %}E{% endlatex %} pronikající systém množin (a {% latex %}e'{% endlatex %} s {% latex %}e''{% endlatex %} by byly disjunktní):

{% xopp slunnnn %}

Dvojic je tedy nejvýše {% latex %}r - 1{% endlatex %}.
{% endmath %}

Důkaz věty bude dvojí počítání {% latex %}(e, C){% endlatex %} t.ž. {% latex %}e \in E, c{% endlatex %} cyklické pořadí a {% latex %}e{% endlatex %} tvoří v {% latex %}C{% endlatex %} interval.
1. vezmu {% latex %}e{% endlatex %} a chci tvořit cyklické pořadí t.ž. {% latex %}e{% endlatex %} tvoří interval: {% latex %}e{% endlatex %} zpermutuji {% latex %}k!{% endlatex %} způsoby a {% latex %}V \setminus e{% endlatex %} zpermutuji {% latex %}(n - k)!{% endlatex %} způsoby, pro každou hranu, tedy {% latex display %}\# (e, C) = |E| \cdot k! \cdot (n - k)!{% endlatex %}
2. vezmu {% latex %}C{% endlatex %}: těch je {% latex %}(n - 1)!{% endlatex %}
	- podle pozorování je {% latex %}e{% endlatex %} tvořících interval nanejvýš {% latex %}k{% endlatex %}, tedy {% latex display %}\# (e, C) \le k \cdot (n - 1)!{% endlatex %}

Spojením dostávám {% latex display %}|E| \le \binom{n - 1}{k - 1}{% endlatex %}
{% endmath %}

### zdroje/materiály
- [stránky přednášky](https://research.koutecky.name/db/teaching:kg22021_prednaska).
[[-]] [Poznámky Václava Končického](https://kam.mff.cuni.cz/~koncicky/notes/kag2/pdf) z roku 2019.

### Poděkování
- `@FloyGun` za upozornění na několik překlepů/chyb v důkazech a definicích.
