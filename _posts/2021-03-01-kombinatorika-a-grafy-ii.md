---
language: cz
title: Kombinatorika a Grafy II
category: "poznamky z prednasky"
category_noslug: "poznámky z přednášky"
pdf: true
redirect_from:
 - /lecture-notes/kombinatorika-a-grafy-ii/
 - /poznámky-z-přednášky/kombinatorika-a-grafy-ii/
---


- .
{:toc}

{% lecture_notes_preface Martina Kouteckého|2020/2021%}

### 1. přednáška

#### Největší párování

- TLDR celé této části jsem zpracoval do [YouTube videa](https://www.youtube.com/watch?v=3roPs1Bvg1Q)

{% math definition %}Párování v \(G = \left(V, E\right)\) je \(M \subseteq E\) t. ž. \(\forall v \in V \exists \le 1\) hrana \(e \in M: v \in e\){% endmath %}

- **maximální** (do inkluze) -- přidání další hrany pro dané párování už není možné; v přednášce nás nezajímá
- **největší** -- \(\mathrm{max}(|M|)\)

{% math definition: "volný vrchol" %} (vzhledem k \(M\)) je vrchol, kterého se nedotýká žádná hrana párování.{% endmath %}

{% math definition: "střídavá cesta" %} (vzhledem k \(M\)) je cesta, na které se střídají hrany v párování a hrany mimo párování: \(u_0, \ldots, u_k\), kde každá sudá/lichá hrana je v \(M\), lichá/sudá není v \(M\){% endmath %}

- **volná** střídavá cesta (VSC) -- krajní vrcholy jsou volné (vůči párování)
- \(\Rightarrow\) obsahuje lichý počet hran, sudý počet vrcholů

{% math claim %}Nechť \(G = \left(V, E\right)\) je graf, \(M\) párování v \(G\). Pak \(G\) obsahuje VSC (vzhledem k \(M\)), právě když \(M\) není největší párování v \(G\).{% endmath %}


<!---MARKDOWN-->

{:.rightFloatBox}
<div markdown="1">
![](/assets/kombinatorika-a-grafy-ii/alter.svg)
</div>

<!---PDF
\begin{wrapfigure}{R}{0.2\textwidth} 
\centering
\fbox{\includesvg{../assets/kombinatorika-a-grafy-ii/alter.svg}}
\end{wrapfigure}
-->
- \(\Rightarrow\) pokud \(M\) má VSC, mohu \(M\) zvětšit prohozením hran

- \(\Leftarrow\) pro spor nechť \(M'\) je párování v \(G\) t. ž \(|M'| \ge |M|\)
	- uvažme \(H = \left(V, M \cup M'\right)\); pak má každý vrchol stupeň \(0, 1\) nebo \(2\) \(\Rightarrow\) komponenty souvislosti jsou kružnice sudé délky a cesty (navíc jsou střídavé)
	- {% math observation %}musí existovat komponenta, která má více hran z \(M'\) (je větší){% endmath %}
		- není to kružnice (musela by být lichá a měli bychom máme kolizi ve vrcholu)
		- je to volná (z definice, vzhledem k \(M\)) střídavá (jinak by měly stejný počet hran) cesta

{% math definition "květ" %} lichá „střídavá“ kružnice s vrcholem \(v_1\), ke kterému přiléhají dvě hrany \(\not\in M\){% endmath %}
{% math definition "stonek" %} střídavá cesta z \(v_1\) (i nulové) délky končící volným vrcholem (dál od květu){% endmath %}
- \(v_1\) může (a nemusí) být volný vrchol -- stačí, aby byl volný vzhledem ke květu

{% math definition "kytka" %} květ + stonek{% endmath %}

![](/assets/kombinatorika-a-grafy-ii/kytka.svg)

{% math definition "kontrakce hrany" %} Nechť \(G = \left(V, E\right)\) je neorientovaný graf a \(e = \left\{u, v\right\}\) jeho hrana. Zápis \(G . e\) označuje graf vzniklý z \(G\) kontrakcí („smrštěním“) hrany \(e\) do jednoho vrcholu:{% endmath %}

![](/assets/kombinatorika-a-grafy-ii/kontrakce.svg)

{% math claim %}Nechť \(C\) je květ v grafu \(G\). Potom párování \(M\) v \(G\) je maximální, právě když \(M \setminus E(C)\) je maximální párování v grafu \(G . C\), tj. s květem \(C\) zkontrahovaným do jediného vrcholu. Navíc pokud znám VSC pro \(M . C\), tak v poly. čase najdu VSC pro \(M\) v \(G\).{% endmath %}

{% math proof %}Tady je [sketchy důkaz](http://www.cs.dartmouth.edu/~ac/Teach/CS105-Winter05/Handouts/tarjan-blossom.pdf), tady je [míň sketchy důkaz](https://stanford.edu/~rezab/classes/cme323/S16/projects_reports/shoemaker_vare.pdf).
{% endmath %}

{% math algorithm "Edmondsův „zahradní/blossom“" %} vstupem je graf \(G\) a jeho libovolné párování \(M\), třeba prázdné. Výstupem je párování \(M'\), které je alespoň o \(1\) větší, než \(M\), případně \(M\) pokud bylo maximální.{% endmath %}

- zkonstruujeme maximální možný **Edmondsův les** vzhledem k aktuálnímu \(M\) tím, že z volných vrcolů pustíme BFS a střídavě přidáváme vrcholy
	- hranám, které se v lese neobjeví, se říká kompost a nebudou pro nás důležité

![](/assets/kombinatorika-a-grafy-ii/les.svg)

- pokud existuje hrana mezi (potenciálně různými) sudými hladinami různých stromů, pak máme volnou střídavou cestu, kterou zalterujeme a jsme hotovi (párování je o \(1\) větší)
- pokud existuje hrana mezi (potenciálně různými) sudými hladinami jednoho stromu, máme květ \(C\) -- ten zkontrahujeme a rekurzivně se zavoláme
	- vrátí-li \(M' = M\), pak nic dalšího neděláme
	- vratí-li nějaké větší párování, tak z něho zkonstruujeme párování v \(G\)
- neexistuje-li hrana mezi sudými hladinami, pak \(M' = M\)

{% math claim %}Edmondsův algoritmus spuštěný na \(G\) a \(M\) doběhne v čase \(\mathcal{O}(n \cdot (n + m))\) a najde párování \(M'\) alespoň o \(1\) hranu větší než \(M\), případně oznámí, že \(M\) je největší \(\Rightarrow\) nejlepší párování lze nalézt v čase \(\mathcal{O}(n^2 (n + m))\).{% endmath %}

{% math proof %}nejvýše \(n\)-krát se vždy zrekurzíme s tím, že při každém rekurzení prohledáme celý graf (\(\mathcal{O}(n + m)\)). Tohle celé opakujeme nejvýše dokud nejsou všechny vrcholy zpárované, tedy \(n\)-krát.  {% endmath %}

### 2. přednáška

{% math definition "perfektní párování" %}Párování \(M\) je perfektní, pokud neexistuje v \(G\) žádný volný vrchol.{% endmath %}

#### Tutteova věta
{% math definition "Tutteova podmínka" %} \(\forall S \subseteq V: \mathrm{odd}(G - S) \le |S|\)
- \(\mathrm{odd}\) je počet lichých komponent grafu{% endmath %}.

{% math theorem "Tutteova věta" %} \(G\) má perfektní párování \(\iff\) platí Tutteova podmínka.{% endmath %}

{% math proof %}
\(\Rightarrow\) obměna: neplatí TP \(\Rightarrow\) není PP. Nechť \(\exists S \subseteq V\) t. ž. \(\mathrm{odd(G - S)} > |S|\). V perfektním párování se alespoň \(1\) vrchol z každé liché komponenty musí spárovat s nějakým z \(S\), ale těch není dostatek.

\(\Leftarrow\) nechť \(G\) splňuje Tutteovu podmínku. \(|V|\) je sudá (nastavíme \(S\) prázdnou). Dokážeme, že \(G\) má PP indukcí podle počtu nehran.

- **základ:** \(G = K_{2n}\), ten PP má
- **indukční podmínka:** \(G\) má nehranu a každý graf na \(V\)s počtem hran alespoň o 1 větší než \(|E|\) a platí TP, pak má perfektní párování

Nechť \(S = \left\{v \in V\ |\ \deg(v) = n - 1\right\} = \left\{v \mid \text{$v$ je spojený se všemi vrcholy} \right\}\)
- lehký případ: každá komponenta \(G - S\) je klika
    - sudé kliky spárujeme triviálně
	- v rámci liché kliky vypáruji vše až na jeden vrchol, ten spáruji v rámci \(S\) (\(S\) vidí všechny) a zbytek v \(S\) spáruji spolu (sudé komponenty do parity nepřispívají, liché + \(1\) z \(S\) také ne a v \(S\) tedy zbyde sudý počet vrcholů)

![](/assets/kombinatorika-a-grafy-ii/1.svg)

- alespoň \(1\) komponenta \(K\) není klika, tedy \(\exists x, y \in K\) nesousední
	- ti mají společného souseda \(u\) (tvrzení o třešničce), který není v \(S\)
	- pro \(u\) existuje vrchol \(v\), se kterým **není** spojený (jinak by \(u\) byl v \(S\), což ale víme že není)


![](/assets/kombinatorika-a-grafy-ii/2.svg)

- {% math observation %}přidáním hrany do grafu se neporuší TP (\(\forall S \subseteq V\) počet lichých komponent \(G - S\) buď klesne o \(2\) nebo zůstane stejný).{% endmath %}

Indukujeme dvakrát: \(G_1 = G + e_1\) a \(G_2 = G + e_2\) díky předchozímu pozorování splňují TP a spolu s IP \(\Rightarrow \exists\) PP \(M_1, M_2\) v \(G_1, G_2\)
- jednoduchý případ: \(e_1 \not\in M_1 \Rightarrow M_1\) je PP pro \(G\), analogicky pro \(e_2\) a \(M_2\)

Těžší případ: \(e_1 \in M_1, e_2 \in M_2, H = (V, M_1 \cup M_2)\)
- \(H \) obsahuje **„dvoubarevné hrany“** \(e \in M_1 \cap M_2\) nebo **střídavé sudé cykly**
- \(H \) neobsahuje **izolované vrcholy** a **střídavé cesty,** protože \(M_1, M_2\) byly perfektní

![](/assets/kombinatorika-a-grafy-ii/3.svg)

- jednodušší případ těžšího případu: \(e_1\) leží v jiné komponentě \(H\) než \(e_2\) -- stačí přealternovat hrany tak, aby ani \(e_1\) ani \(e_2\) v \(H\) neležely.

![](/assets/kombinatorika-a-grafy-ii/4.svg)

- složitější případ těžšího případu: \(e_1\) a \(e_2\) leží ve stejné komponentě -- vybereme podle obrázku

![](/assets/kombinatorika-a-grafy-ii/5.svg)

{% endmath %}

{% math theorem "Petersen" %} každý \(3\)-regulární \(2\)-souvislý (vrcholově i hranově, pro 3-regulární grafy je to to samé; alternativně můžeme říct graf bez mostů a artikulací) graf má PP.{% endmath %}

{% math proof %}Nechť \(G = (V, E)\) je \(3\)-regulární a \(2\)-souvislý. Chci ukázat, že \(G\) splňuje TP. Předpokládejme danou \(S \subseteq V\).

1. každá komponenta \(G - S\) je v \(G\) spojena aspoň dvěma hranami s \(S\)
	- je \(2\)-souvislý, nemáme mosty

2. dokážeme, že každá lichá komponenta \(G - S\) je s \(S\) spojena lichým počtem hran:
	- nechť \(L\) je lichá komponenta \(G - S\); pak:
\[\sum_{x \in V(L)}\deg_G(x) \overset{3-\text{reg.}}{=} \underbrace{3|V(L)|}_{\text{liché číslo}} = \underbrace{2 (\text{\# hran vedoucích uvnitř $L$})}_{\text{sudé číslo}} + \underbrace{1 (\text{\# hran vedoucích uvnitř $L$})}_{\text{musí být liché}}\]

- kombinace (1) a (2) říká, že každá lichá komponenta \(G - S\) je s \(S\) spojena \(\ge 3\) hranami:
	- \(p = \) počet hran mezi \(S\) a lichými komponentami \(G - S\)
		- \(p \ge 3 \cdot \mathrm{odd(G - S)}\) (ukázali jsme výše)
		- \(p \le 3 \cdot |S|\) (každý vrchol \(S\) vysílá ven \(\le 3\) hrany (z \(3\)-regularity))

![](/assets/kombinatorika-a-grafy-ii/6.svg)

\(|S| \ge \mathrm{odd}(G - S)\), tedy TP platí a graf má perfektní párování.

{% endmath %}

### 3. přednáška

#### Tutte v2.0

{% math lemma "o kontrahovatelné hraně = LoKH" %} Nechť \(G\) je vrcholově \(3\)-souvislý různý od \(K_4\). Potom \(G\) obsahuje hranu t. ž. \(G \setminus e\) je 3-souvislý.{% endmath %}

{% math proof %}Sporem -- nechť \(G\) je 3-souvislý ale neexistuje žádná hrana, která jde zkontrahovat. Tedy \(\forall e \in E: G \setminus e\) není \(3\)-souvislý.

{% math lemma "pomocné" %} \(\forall e = \left\{x, y\right\} \exists z_e \in V \setminus \left\{x, y\right\}\) t. ž. \(\left\{x, y, z_e\right\}\) tvoří vrcholový řez v G, navíc každý z \(\left\{x, y, z_e\right\}\) má alespoň jednoho souseda v každé komponentě \(G \setminus \left\{x, y, z_e\right\}\).{% endmath %}
- přesně popisuje situaci, že kontrakce libovolné hrany nám dá řez velikosti \(2\)
- ve skutečnosti **neplatí** (ale dovětek ano) a dokazujeme ho pouze v rámci sporu!
- {% math observation "které platí" %}\(S\) minimální vrcholový řez \(G\), pak každý vrchol \(S\) má souseda v každé komponentě \(G \setminus S\) -- když to pro nějaký \(v\) neplatí, tak \(S \setminus v\) je pořád řez{% endmath %} 

{% xopp 1 %}

{% math proof "způsob z přednášky" %}
Vím, že \(G \setminus e\) není \(3\)-souvislý, tedy má vrcholový řez velikosti \(2\). Nechť \(v_e\) je vrchol vzniklý kontrakcí \(e = \left\{x, y\right\}\). Řez velikosti \(2\) obsahuje \(v_e\), jinak by to byl řez už pro \(G\) (obsahoval by vrcholy z původního grafu, které nekontrahujeme).

Označme řez \(v_e, z_e\). Po rozkontrahování vidíme, že \(\forall \left\{x, y, z_e\right\}\) musí mít souseda v každé komponentě (jinak spor s 3-souvislostí). Tedy \(z_e\) je hledaný vrchol.
{% endmath %}

{% xopp 2 %}

{% math proof "moje intuice" %}Pokud by neplatilo (existovala by taková hrana), tak máme hranu, přes kterou kontrahujeme. Jelikož pro tu hranu platí, že neexistuje \(z\), které spolu s jejími vrcholy tvoří řez, tak bude graf i po kontrakci \(3\)-souvislý.
{% endmath %}

Pro důkaz původního lemmatu si zvolím \(e = \left\{x, y \right\} \in E\) a \(z_e\) z pomocného tvrzení tak, aby nejmenší komponenta \(G - z, y, z_e\) byla co nejmenší (co do počtu vrcholů).

Protože \(z_e\) má souseda ve všech komponentách, má nějakého souseda \(u \in C, f = \left\{z_e, u\right\}\) (kde \(C\) je naše nejmenší komponenta). Pomocné tvrzení pro \(f\) dá nějaký \(z_f \in V\) t. ž. \(\left\{z_e, z_f, u\right\}\) je vrcholový řez \(G\). Chceme dokázat, že \(G - z_e, z_f, u\) má menší komponentu než \(C\).

{% xopp 3 %}

Nechť \(D\) je komponenta \(G - z_e, z_f, u\) neobsahující \(x, y\). Existuje, protože \(x, y\) jsou spojené a graf se rozpadne alespoň na \(2\) komponenty. Tvrdím, že \(D \subseteq C \setminus \left\{u\right\}\), protože \(D\) nemůže obsahovat \(z_e, z_f, u\) (vrcholy řezu), \(x, y\) (z definice \(D\)), ale \(u\) má nějakého souseda v \(D\) (podle pomocného tvrzení, \(u\) má sousedy ve všech komponentách řezu), takže v \(D\) ještě něco zbyde. Navíc ho tam mělo \(u\) i předtím, takže opravdu \(D \subseteq C \setminus \left\{u\right\}\). Tedy \(|D| < |C|\), což je spor s minimalitou.
{% endmath %}

- netvrdím, že \(D\) je nejmenší!

{% math theorem "Tutteova charakterizace 3-souvislých grafů" %} Graf \(G\) je 3-souvislý \(\iff\) existuje posloupnost \(K_4 \cong G_0,  G_1, \ldots, G_n \cong G\) t. ž. \(\forall i \in [n], G_{i - 1}\) vznikne z \(G_i\) kontrakcí hrany, navíc \(G_i\) má všechny vrcholy stupně \(\ge 3\).{% endmath %}

{% math proof %} \(\Rightarrow\) Induktivní aplikace lemmatu o kontrahovatelné hraně.

\(\Leftarrow\) Mějme \(G_0, \ldots, G_n\) dle předpokladu. Chceme, že \(G_n \cong G\) je 3-souvislý. Indukcí:
- \(K_4\) je 3-souvislý
- \(G_{i - 1}\) je 3-souvislý \(\Rightarrow G_i\) je 3-souvislý

<!---MARKDOWN-->

{:.rightFloatBox}
{% xopp 4 %}

<!---PDF
-->

Obměnou nechť \(G_i\) má vrcholový řez velikosti 2, označme ho \(R = \left\{x,y\right\}\). Pak každá komponenta \(G_i - R\) má alespoň 2 vrcholy (osamocený vrchol \(z\) mohl sousedit jen s řezem, ale ten je velikosti 2, což je spor se stupněm vrcholů \(\ge 3\) pro \(v\)).

Pak ale \(G_{i - 1}\) nebyl 3-souvislý, rozborem toho, kde vznikla hrana:
- \(e = \left\{x, y\right\} \Rightarrow G_{i - 1}\) má řez velikosti 1.
- \(e\) celá obsažená v komponentě \(\Rightarrow \left\{x, y\right\}\) je stále řez v \(G_{i - 1}\)
- \(e = \left\{z, y\right\}\) pro \(z\) z nějaké komponenty \(\Rightarrow \left\{zy, x\right\}\) je řez v \(G_{i - 1}\)
	- využíváme předchozí pozorování, že každá komponenta má alespoň \(2\) vrcholy -- kdyby ne, tak \(\left\{zy, x\right\}\) nemusí nic odříznout, pokud tam byla jednovrcholová komponenta
{% endmath %}

#### Minory

{% math definition "minor" %} Nechť \(H, G\) jsou grafy. Pak \(H\) je minor \(G\) (nebo že \(G \) obsahuje \(H\) jako minor), značíme \(H \preceq G\), pokud \(H\) lze získat z \(G\) posloupností mazání vrcholů, mazání hran nebo kontrakcí hran.{% endmath %}

- {% math observation %}\(\preceq\) je transitivní (prostě spojím posloupnosti operací){% endmath %}
- {% math observation %}\(H\) podgraf \(G \Rightarrow H\) minor \(G\){% endmath %}
	- podgraf vzniká přesně mazáním vrcholů a mazáním hran
- {% math observation "spíš fakt" %}\(G\) rovinný \(\Rightarrow\) jeho minory jsou také rovinné{% endmath %}
	- pro podgraf očividné, je jen potřeba si rozmyslet kontrakci (že nic topologicky nerozbije)

{% math theorem "Kuratowského" %} \(G\) rovinný \(\iff\) neobsahuje dělení \(K_5\) ani \(K_{3, 3}\){% endmath %}

{% math theorem "Kuratowski 1930, Warner 1937" %} Následující jsou ekvivalentní:{% endmath %}
1. \(G\) je rovinný
2. \(G\) neobsahuje dělení \(K_5\) ani \(K_{3, 3}\) jako podgraf
3. \(G\) neobsahuje \(K_5\) ani \(K_{3, 3}\) jako minor.

{% math proof %}
- *\(1 \Rightarrow 2\): z prváku, protože \(K_5\) ani \(K_{3, 3}\) nejsou rovinné
- \(3 \Rightarrow 2\): obměna: „obsahuje dělení jako podgraf“ \(\Rightarrow\) „obsahuje dělení jako minor“
- \(1 \Rightarrow 3\): je-li rovinný, tak i minor bude rovinný (fakt výše)
- *\(2 \Rightarrow 3\): na přednášce nebyl, k přečtení tady[^1] 
- *\(3 \Rightarrow 1\): indukcí podle \(|V(G)|\)
	- pro \(|V(G)| \le 4\) vše funguje
	- předpokládám \(G\) má alespoň 5 vrcholů a neobsahuje \(K_5\) ani \(K_{3, 3}\) jako minor. Rozeberu případy podle \(k_v(G)\) (vrcholová souvislost \(G\))
		- \(k_v(G) = 0\Rightarrow\) nesouvislý graf, použijeme indukci
		- \(k_v(G) = 1\Rightarrow\) artikulačním vrcholem \(x\) rozpojíme, podle IP nakreslíme
			- \(x\) musí být na vnější stěně, což umíme přes trik s projekcí z koule na rovinu
		- \(k_v(G) = 2\Rightarrow\), rozložení podél dvou vrcholů tvořících řez, ale opatrně -- musíme si rozmyslet, že můžeme obě části zkontrahovat do hrany mezi vrcholy, aby poté v nakreslení šly spojit
{% endmath %}

[^1]: Chceme ukázat, že obsahuje-li graf \(K_5\) nebo \(K_{3,3}\) jako minor, obsahuje i dělení nějakého z těchto grafů jako podgraf. Uvažme nejdřív obecně graf \(G\) obsahující jak podgraf dělení \(H'\) grafu \(H\). \(H'\) dostaneme z \(G\) posloupností mazání vrcholů a mazání hran. \(H\) pak dostaneme z \(H'\) posloupností operací inverzních k dělení hran, což jsou právě kontrakce hran, při nichž má výsledný vrchol stejný stupeň, jako jeden z kontrahovaných vrcholů (a zároveň nekontrahujeme vrchol stupně 1, což je ale to samé jako mazání). Všimněme si, že tento speciální tvar má mimo jiné každá kontrakce, při níž nevznikne větší stupeň než 3.  Co kdyby tedy \(G\) obsahoval minor \(K\) a navíc \(\Delta(K) \leq 3\)? Od \(G\) ke \(K\) se můžeme dostat posloupností mazání vrcholů, mazání hran a kontrakcí hran. Všimněme si ale, že nikdy nemusíme použít kontrakci, při které vznikne větší stupeň než 3, protože vzniklý vrchol musí být stejně následně smazán. To můžeme nahlédnout i tak, že v posloupnosti operací se mohou operace libovolně předbíhat (pokud je přitom patřičně pozměníme), a tedy všechny kontrakce si můžeme nechat nakonec. Z předchozích pozorování vidíme, že minory maximálního stupně nejvýše 3 a dělení jako podgrafy jsou generované stejnými typy operací a tedy speciálně obsahuje-li graf \(K_{3,3}\) jako minor, obsahuje i nějaké jeho dělení jako podgraf.  Zbytek důkazu pro \(K_5\) je lepší s obrázkem a lze najít [na tomhle odkazu](https://www.math.uni-hamburg.de/home/diestel/books/graph.theory/preview/Ch4.pdf) (Lemma 4.4.2).

Pokračování v další přednášce...

### 4. přednáška
- \(k_v(G) \ge 3\Rightarrow\) použijeme lemma o kontrahovatelné hraně: \(\exists e = \left\{x, y\right\}\) t. ž. \(G \setminus e = G'\) je \(3\)-souvislý
	- {% math observation %}\(G'\) nemůže obsahovat \(K_5\) ani \(K_{3, 3}\) jako minor (kontrakcí něčeho, co je nemělo, je nevytvoříme){% endmath %} 
	- \(\mathcal{G}' \ldots\) rovinné nakreslení \(G'\) (existuje z IP)
	- \(G'' = G' - v_e\) (vrchol vzniklý kontrakcí \(e\)) \( = G - \left\{x, y\right\}\)
		- {% math observation %}\(G''\) bude \(2\)-souvislý (protože \(G'\) je \(3\)-souvislý a \(G''\) vznikne odebráním vrcholu){% endmath %}
		- {% math observation %}taky rovinný (odebráním mi žádný minor nevznikne){% endmath %}
		- \(\mathcal{G}''\) nakreslení \(G''\) vzniklé z \(\mathcal{G}'\) odebráním \(v_e\)

Označme \(C\) kružnici ohraničující stěnu \(\mathcal{G}''\), v níž ležel (v \(\mathcal{G}'\) vrchol \(v_e\)) -- musí to být kružnice, protože v rovinném nakreslení každého \(2\)-souvislého grafu je každá stěna kružnice.

{% xopp tmp %}

- \(N(x)\) -- sousedi \(x\)
- \(N(y)\) -- sousedi \(y\)
- \(N(x) \cup N(y) \setminus \left\{x, y\right\} \subseteq C\) (každý soused \(x\) kromě \(y\) je i sousedem \(v_e\) v \(G'\), stejně pro \(y\)

3 případy:
- \(|N(x) \cap N(y)| \ge 3\) -- nenastane, protože kontrakcí dostanu \(K_5\), což je spor s předpokladem

{% xopp p1 %}

- \(\exists a_1, a_2 \in N(x) \cap C, \exists b_1, b_2 \in N(y) \cap C\), na \(C\) jsou v pořadí \(a_1, b_1, a_2, b_2\) -- nenastane, protože kontrakcí dostanu \(K_{3, 3}\)

{% xopp p2 %}

- zbytek -- nenasatane ani (1), ani (2)
	- označme \(a_1, \ldots, a_k \in N(x) \cap C\) v pořadí, jak se objevují na \(C\)
	- můžu nakreslit všechny hrany \(xa_1, \ldots xa_k\)
	- \(a_1, \ldots, a_k\) rozdělují \(C\) na vnitřně disjunktní cesty \(P_1, \ldots P_k\) (\(k \ge 2\) protože \(G\) je \(3\)-souvislý... \(x\) sousedí s \(y\) a s \(\ge 2\) dalšími vrcholy)
		- chceme: \(N(y) \setminus \left\{x\right\}\) patří do jediné \(P_i\) (pro nějaké \(i\)), jinak by nastaly předchozí případy
	- \(y\) nakreslím do té správně stěny, spojím s \(b_i\) a mám hotovo

{% xopp p3 %}
{% xopp p4 %}

#### Kreslení grafů na plochy
{% math definition %}Nechť \(X \subseteq \mathbb{R}^n, Y \subseteq \mathbb{R}^m\). Potom homeomorfismus z \(X\) na \(Y\) je funkce \(f: X \mapsto Y\), která je spojitá, bijekce a \(f^{-1}\) je spojitá. \(X, Y\) jsou homeomorfní (\(X \cong Y\)) pokud mezi nimi existuje homeomorfismus.{% endmath %}
- něco jako isomorfismus u grafů (\(X \cong Y\) znamená, že se chovají stejně)

{% math definition "plocha" %} kompaktní (uzavřená, omezená), souvislá (např. oblouková -- každé dva body můžu propojit obloukem), \(2\)-rozměrná varieta bez hranice (dostatečně malé okolí každého bodu je homeomorfní otevřenému okolí v \(\mathbb{R}^2\)).{% endmath %}
- např. sféra v \(\mathbb{R}^3\) nebo torus v \(\mathbb{R}^3\)
- není to např.
	- \(\mathbb{R}^2\), jelikož není kompaktní (omezená)
	- čtverec s hranici, jelikož pro každý krajní body není homeomorfní \(\mathbb{R}^2\)

Operace s plochami, přes které umíme všechny zkonstruovat:


<!---MARKDOWN-->

{:.rightFloatBox}
{% xopp o1 %}

<!---PDF
-->

- přidání ucha (od hrnku)
	- vyříznu dva kruhy
	- vezmu plášť pálce bez dna a vrchu
	- ohnu a přílepím jej na díry po kruzích
	- {% math observation %}teleport, do kterého když vejdeme, tak na druhé straně vyjdeme opačně („otočeně“){% endmath %} 

<!---MARKDOWN-->

{:.rightFloatBox}
{% xopp o2 %}

<!---PDF
-->

- přidání křížítka (cross-cupu):
	- {% math observation %}teleport, do kterého když vejdeme, tak nás to přesune naproti{% endmath %}

Pro \(g \in \left\{0, 1, \ldots\right\}\) nechť \(\sum_g\) značí plochu zvniklou ze sféry přidáním \(g\) uší, tak říkáme, že \(\sum g\) je **orientovatelná plocha** rodu \(g\).

Pro \(g \in \left\{1, 2, \ldots\right\}\) nechť \(\prod_g\) značí plochu zvniklou ze sféry přidáním \(g\) křížítek, tak říkáme, že \(\prod g\) je **neorientovatelná plocha** rodu \(g\).

{% math fact %}Každá plocha je homeomorfní právě jedné z posloupností \(\sum_0, \prod_1, \sum_1, \prod_2,\ldots\){% endmath %}
- máme tu skryté tvrzení, že žádné dvě z této posloupností nejsou homeomorfní.

{% math fact %}Přidám-li ke sféře (\(= \Sigma_0\)) \(k \ge 0\) uší a \(l \ge 1\) křížítek, vznikne **neorientovatelná plocha** homeomorfní \(\prod_{2k + l}\) (\(\approx\) „přidání dvou křížítek je jako přidání ucha,“ **pokud** už tam bylo \(\ge 1\) křížítko){% endmath %}

- \(\sum_0 \ldots\) sféra
- \(\prod_1 \ldots\) projektivní rovina
- \(\sum_1 \ldots\) torus
- \(\prod_2 \ldots\) kleinova láhev

### 5. přednáška
{% math definition "nakreslení grafu" %} \(G = (V, E)\) na plochu \(\Gamma\) je zobrazení \(\varphi\) t. ž.:
- každému vrcholu \(v \in V\) přiřadí bod \(\varphi(v) \in \Gamma\)
- každé hraně \(e \in E\) přiřadí prostou (neprotínající se) křivku \(\varphi(e) \in \Gamma\) spojující konce \(\varphi(x), \varphi(y)\)
- vrcholy se nepřekrývají: \(x, y \in V: x \neq y \Rightarrow \varphi(x) \neq \varphi(y)\)
- hrany se překrývají nejvýše ve sdílených vrcholech: \(e, f \in E: e \neq f \Rightarrow \varphi(e) \cap \varphi(f) = \left\{\varphi(x) \mid x \in e \cap f\right\}\)
- vrcholy, které neleží na hraně se s ní neprotínají: \(e \in E, x \in V: x \not\in e \Rightarrow \varphi(x) \not\in \varphi(e)\)
{% endmath %}

{% math definition "stěna nakreslení" %} souvislá komponenta \(\Gamma \setminus \left(\left(\bigcup_{e \in E}^{\varphi(e)}\right) \cup \left(\bigcup_{x \in V}^{\varphi(x)}\right)\right)\){% endmath %}
- prostě souvislé komponenty toho, když odeberu všechna nakreslení hran a vrcholů

{% math definition "buňkové nakreslení" %} každá stěna je homeomorfní otevřenému kruhu v \(\mathbb{R}^2\).{% endmath %}

{% xopp torus %}

{% math reminder %}\(G = (V, E)\) souvislý \(\Rightarrow\) v každém rovinném nakreslení platí \(|V| - |E| + S = 2\) {% endmath %}
- využíváme faktu, že rovinné nakreslení \(G\) je buňkové \(\iff G\) je souvislé
- \(2\) je speciální pro rovinu

{% math definition "Eulerova charakteristika plochy" %} charakteristika plochy \(\Gamma\) je

\[
\begin{aligned}
\Chi(\Gamma) &= \begin{cases} 2 - g & \Gamma \cong \prod (g \ge 1) \\ 2 - 2g & \Gamma \cong \sum (g \ge 0) \end{cases} \\
\            &= 2 - \text{\# křížítek} - 2 \cdot \text{\# uší}
\end{aligned}
\]
{% endmath %}

{% math theorem "zobecněná Eulerova formule" %}Nechť máme nakreslení grafu \(G = (V, E)\) na ploše \(\Gamma\), které má \(S\) stěn. Pak \(|V| - |E| + |S| \ge \Chi(\Gamma)\). Pokud je buňkové, tak dokonce \(|V| - |E| + |S| = \Chi(\Gamma)\).{% endmath %} 

{% math proof "rovnosti" %}idea je indukce podle rodu \(\Gamma\)
- \(\Gamma \cong \Sigma_0\) platí

<!---MARKDOWN-->

{:.rightFloatBox}
{% xopp s1 %}

<!---PDF
-->

Mějme buňkové nakreslení \(G = (V, E)\) na \(\Gamma \cong \Pi_g\)
- pro \(\Gamma \cong \Sigma_g\) se dělá analogicky, jen trháme obě ucha a vyjde to
- \(v(G), e(G), s(G)\) značíme počet vrcholů, hran a stěn

Nechť \(K\) je křížítko na \(\Gamma\), \(x_1, \ldots, x_k\) jsou body \(K\) (ne nutně vrcholy grafu), kde hrany \(G\) kříží \(K\)
- {% math observation %}\(k \ge 1\), jinak by stěna obsahující \(K\) nebyla buňka{% endmath %}
- rovněž předpokládám, že vrchol neleží přesně na křížítku, jinak bych ho mohl BUNO posunout

<!---MARKDOWN-->

{:.rightFloatBox}
{% xopp s2 %}

<!---PDF
-->

Vytvoříme \(G'\) přidáním dvou dělících vrcholů na každou hranu křížící \(K\) těsně vedle \(x_1, \ldots, x_k\) („před a za křížítkem“). Děláme to proto, že jedna hrana by mohla procházet křížítkem na více místech a bylo by to pak dost rozbitý.
- \(v(G') = v(G) + 2k\)
- \(e(G') = e(G) + 2k\)
- \(s(G') = s(G)\)
- tedy: \(L(G') = L(G)\) (kde \(L\) je levá strana)

<!---MARKDOWN-->

{:.rightFloatBox}
{% xopp s3 %}

<!---PDF
-->

Vytvoříme \(G''\) přidaním cest délky \(2\) k sousedním vrcholům z předchozího kroku. Vznikne tím kružnice \(C\) obcházející \(K\).
- \(v(G'') = v(G') + 2k\)
- \(e(G'') = e(G') + 4k\)
- \(s(G'') = s(G') + 2k\) (každou z \(k\) stěn dělím na \(3\) kusy)
- tedy: \(L(G'') = L(G')\)

<!---MARKDOWN-->

{:.rightFloatBox}
{% xopp s4 %}

<!---PDF
-->

Vytvoříme \(G'''\) odebráním všeho uvnitř \(C\).
- \(v(G''') = v(G'')\)
- \(e(G''') = e(G'') - k\) (\(k\) křížících-se hran uvnitř \(C\))
- \(s(G''') = s(G'') - k + 1\) („spojím“ \(k\) stěn do jedné)
- tedy: \(L(G''') = L(G'') + 1\)

\[L(G''') = \Chi(\Pi_{g - 1}) = \Chi(\Gamma) + 1 \qquad \mid \text{dle IP}\]
\[L(G''') - 1 = L(G'') = L(G') = L(G) \qquad \mid \text{z výpočtu}\]

Tedy \[\Chi(\Gamma) = L(G)\]
{% endmath %}

{% math consequence %}Každý graf \(G\) nakreslitelný na plochu \(\Gamma\) splní \(|E| \le 3|V| - 3\Chi(\Gamma)\), pokud \(|V| \ge 4\)
- důkaz přes to, že předpokládáme, že každá stěna je trojúhelník a dosadíme \(|S| = \frac{2}{3}|E|\), jelikož každá stěna je tvořena třemi hranami a zároveň je každá hrana ve dvou stěnách
- každý takový graf má průměrný stupeň \(\frac{2|E|}{|V|} \le 6 - \frac{6\Chi(\Gamma)}{|V|}\)
	- na žádnou zafixovanou plochu nelze nakreslit libovolně velký \(7\)-regulární graf
	- pro libovolně velký úplňák dokážeme vytvořit plochu, na kterou ho nakreslíme
{% endmath %}

{% math claim %}Nechť \(\Gamma\) je plocha, \(\Gamma \neq \Sigma_0\), nechť \(G\) je graf nakreslený na \(\Gamma\), potom \(G\) obsahuje vrchol stupně \(\le \left\lfloor \frac{5 + \sqrt{49 - 24\Chi(\Gamma)}}{2} \right\rfloor\){% endmath %}

{% math proof %}Mějme \(G\) podle předpokladu. Opět značíme \(v(G), e(G)\) jako počet vrcholů a hran. Rozlišíme \(3\) případy:
- \(\Chi(\Gamma) = 1\) (t.j. \(\Gamma \cong \prod_1\)), dosazením do předchozího důsledku dostáváme průměrný stupeň \(< 6\), tedy existuje vrchol stupně \(\le 5\), což jsme chtěli
- \(\Chi(\Gamma) = 0\) (t.j. \(\Gamma \cong \prod_2\) nebo \(\Gamma \cong \sum_1\)), průměrný stupeň \(\le 6 \Rightarrow \exists\) vrchol stupně \(\le 6\)
- \(\Chi(\Gamma) < 0 \ldots \delta(G) = \) min. stupeň \(G\); víme:
	- \(\delta(G) \le 6 - \frac{6 \Chi(\Gamma)}{v(G)}\)
	- \(\delta(G) \le v(G) - 1\) (žádný vrchol nemá víc než \(v(G) - 1\) sousedů)
	- chceme zjistit max. hodnotu \(\delta\), což je řešení dvou rovnic výše; dosazením a vyřešením kvadratické rovnice vyjde přesně výraz, který dokazujeme
{% endmath %}

{% math consequence "Heawoodova formule, 1890" %} Pokud \(\Gamma \not\cong \sum_0\), tak každý graf nakreslitelny na \(\Gamma\) je nejvýš \(H(\Gamma) = 1 + \left\lfloor \frac{5 + \sqrt{49 - 24 \Chi(\Gamma)}}{2} \right\rfloor = \left\lfloor \frac{7 + \sqrt{49 - 24 \Chi(\Gamma)}}{2} \right\rfloor\)-obarvitelný{% endmath %}
- vyplývá z předchozího důsledku -- pokud má graf stupeň nejvýše \(\delta\), tak je \(\delta+1\)-obarvitelný
- platí i pro stéru: věta o \(4\)-barvách
- tento odhad je těsný pro všechny plochy kromě \(\prod_2\)
- na každou plochu \(\Gamma \not\cong \prod_2\) lze kreslit kliku velikosti \(H(\Gamma)\)
	- (každý graf nakreslitelný na \(\prod_2\) je dokonce \(6\)-obarvitelný)

### 6. přednáška

#### Vrcholové barvení
- \(\Chi(G) =\) barevnost \(G = \) nejmenší počet barev, kterými lze (dobře) obarvit vrcholy \(G\)
- \(\Delta(G) = \) max. stupeň \(G = \), \(\delta(G) = \) min. stupeň \(G\)

{% math definition %}\(G\) je \(d\)-degenerovaný \(\equiv\) každý podgraf \(H\) grafu \(G\) má \(\delta(H) \le d\){% endmath %}
- \(=\) každý podgraf má vrchol stupně nejvýše \(d\)

{% math definition "eliminační pořadí" %}Alternativní definice \(d\)-degenerovanosti: graf je \(d\)-degenerovaný
\(\iff \exists\) pořadí vrcholů (eliminační) \(v_1, \ldots v_n\) t. ž. \(\forall i: G_i := G - \left\{v_1, \ldots, v_i\right\}: \delta(G_i) \le d\) a \(v_{i - 1}\) má \(\le d\) sousedů v \(G_i\)
- trháme vrcholy -- každý další odebraný má nejvýše \(d\) sousedů a graf je stále \(d\)-degenerovaný
- {% math observation %}\(G\) je \(d\)-degenerovaný \(\Rightarrow \Chi(G) \le d + 1\){% endmath %} (barvím indukcí v pořadí \(v_n, \ldots, v_1\))
{% endmath %}

![](/assets/kombinatorika-a-grafy-ii/degen.png)

- z minule: pokud \(G\) je nakreslitelný na \(\Gamma \Rightarrow G\) má vrchol stupně nejvýše \(H(\Gamma) - 1\) a \(G - v\) je stále nakreslitelný na \(\Gamma \Rightarrow G\) je \(\left(H(\Gamma) - 1\right)\)-degenerovaný \(\Rightarrow\) je \(H(\Gamma)\) obarvitelný

{% math observation %}\(G\) je \(\Delta(G)\)-degenerovaný (triviálně) \(\Rightarrow \Chi(G) \le \Delta(G) + 1\) (z pozorování výše){% endmath %}

- s rovností platí např. pro úplné grafy a liché cykly

{% math lemma %}\(G\) souvislý graf a \(\delta(G) < \Delta(G)\), pak \(\Chi(G) \le \Delta(G)\){% endmath %}
- když nás zajímá předchozí otázka, tak se stačí zaměřit na nějaký regulární graf

<!---MARKDOWN-->

{:.rightFloatBox}
{% xopp a1 %}

<!---PDF
-->

{% math proof %}Tvrdím, že \(G\) je (\(\Delta(G) - 1\))-degenerovaný. Volme \(H\) neprázdný podgraf \(G\) a dokazujeme, že v \(H\) existuje \(v\) stupně \(\le \Delta(G) - 1\) 
- pokud \(H\) obsahuje všechny vrcholy \(\Rightarrow\) předpoklad
- jinak \(\exists e = \left\{x, y\right\} \in G\) t. ž. \(x \in H\) a \(y \not\in H\)
	- \(\deg_H(x) \le \deg_G(x) - 1 \le \Delta(G) - 1\)
{% endmath %}

{% math theorem "Brooks, 1941" %}Nechť \(G\) je souvislý graf který není úplný a není lichá kružnice. Pak \[\Chi(G) \le \Delta(G)\]{% endmath %}

{% math proof %}nechť \(\Chi = \Chi(G), \Delta = \Delta(G)\) a navíc předpokládám, že \(G\) je \(\Delta\)-regulární (jinak viz. předchozí lemma.

- \(\Delta = 1\)
	- \(K_2\): zakázané
- \(\Delta = 2\)
	- \(C_{2k}\): \(\Chi = 2\)
	- \(C_{2k + 1}\): zakázané
- \(\Delta \ge 3\); označme \(k_V(G) = \) vrcholová souvislost \(G\) a opět rozebereme případy

1. \(k_V(G) = 1\)
	- máme artikulaci, vrchol artikulace \(v\) měl souseda v obou částech grafu, proto \(\deg_{G_1}(v), \deg_{G_2}(V) < \Delta\)
	- podle lemmatu (\(G_1\) a \(G_2\) nejsou regulární) lze \(G_1\) i \(G_2\) \(\Delta\)-obarvit a stačí přepermutovat barvy, aby měl v obou obarveních stejnou

2. \(k_V(G) = 2\)
	- dobré případy (lze slepit)
		- \(b_1(x) = b_1(y)\) a \(b_2(x) = b_2(y)\) 
		- \(b_1(x) \neq b_1(y)\) a \(b_2(x) \neq b_2(y)\) 
	- těžší případ -- na jedné straně stejné, na druhé různé
		- \(b_1(x) = b_1(y)\) a \(b_2(x) \neq b_2(y)\) 
			- pokud \(\deg_{G_1}(x)\) nebo \(\deg_{G_1}(y) \le \Delta - 2\), tak po přidání hrany půjde použít lemma a vrcholy budou mít různou barvu a máme dobrý případ
				- nemůže se stát, že by např. druhý měl \(\deg_{G_1} = \Delta\), protože musí vidět i do druhé komponenty
			- nebo \(\deg_{G_1}(x) = \deg_{G_1}(y) = \Delta - 1\)
				- pak musí \(\deg_{G_2}(x) = \deg_{G_2}(y) = 1\) (stupeň je celkově \(\Delta\))
				- z předpokladu máme k použití alespoň \(3\) barvy, přebarvím jimi \(x\) a \(y\) a máme dobrý případ

{% xopp cases %}

{:start="3"}
3. \(k_V(G) \ge 3\) -- použiji lemma o třešničce (souvislý graf, který není klika, obsahuje třešničku)
	- seřadím vrcholy jako \(v_1 = x, v_2 = y, \ldots, v_n = z\) tak, aby \(\forall v_i: 3 \le i \le n - 1\) měl alespoň jednoho souseda napravo a barvím (hladově):
		- umíme získat jako BFS vrstvy od \(z\), kromě \(x\) a \(y\)
		- \(3\)-souvislost využívám k tomu, že i po odstranění \(x\) a \(y\) graf bude stále nějakou kostru mít a bude tedy stále souvislý
		- \(b(x) = b(y) = 1\)
		- \(b(v_3)\ldots\) má \(\ge 1\) neobarveného souseda \(\Rightarrow\) je nějaká nepoužitá z \(\Delta\) barev
		- \(\ldots\)
		- \(b(v_n)\ldots\) všichni sousedé už obarvení, ale dva sousedé (\(x, y\)) mají stejnou barvu, tedy \(z\) vidí \(\le \Delta - 1\) barev a jedna je volná

{% xopp kooo %}

{% endmath %}

#### Pár poznámek

**Hadwigerova domněnka:** \(K_t \not\preceq_m G\) (není minor)\( \Rightarrow \Chi(G) < t\)
- \(t = 4 \ldots\) relativně jednoduché
- \(t = 5 \ldots\) zobecnění věty o \(4\) barvách
- \(t = 6 \ldots\) pomocí věty o \(4\) barvách + hodně práce
- \(t \ge 7 \ldots\) neví se

{% math claim %}\(G\) nakreslitelný na Kleinovu láhev \(\Rightarrow G\) je \(6\)-obarvitelný.{% endmath %}

{% math proof %}Z Eulerovy formule plyne, že platí jedno z následujících:
- \(\delta(G)\le 5 \Rightarrow \exists v: \deg(v) \le 5\){% endmath %}
	- \(G - v \ldots\)  obarvím z indukce, přidám \(v\) a mám volnou barvu
- \(G\) je \(6\)-regulární:
	- \(G \cong K_7\) -- nesmí, protože nejde nakreslit (je potřeba si rozmyslet)
	- \(G \not\cong K_7\) -- přímo Brooksova věta

#### Hranové obarvení
{% math definition %}\(b: E \mapsto B\) (barvy) t. ž. \(\forall e \neq f \in E, e \cap f \neq \emptyset \Rightarrow b(e) \neq b(f)\). Hranová barevnost \(G\) ("chromatic index") \(\Chi'(G)\) je min. počet barev pro hranové barvení \(G\).{% endmath %}

### 7. přednáška

{% math theorem "Vizing, 1964" %}Pro každý graf \(G\) platí, že \(\Delta(G) \le \Chi'(G) \le \Delta(G) + 1\){% endmath %}
- grafy Vizingovy třídy \(1\) jsou grafy \(\Chi'(G) = \Delta(G)\), třídy \(2\) jsou \(\Chi'(G) = \Delta(G) + 1\)
- je NP-úplné rozhodnout, zda daný graf \(G\) má VIzingovu třídu \(1\) (i pro grafy s \(\Delta(G) = 3\))
- důkaz jsem zpracoval do [YouTube videa](https://www.youtube.com/watch?v=OZWZpQmGp0g)

#### Perfektní grafy

{% math theorem "Slabá věta o perfektních grafech, 1972" %}\(G\) je perfektní \(\iff\) \(\bar{G}\) je perfektní.{% endmath %}
- důkaz jsem zpracoval do [YouTube videa](https://www.youtube.com/watch?v=Koc63QhxPgk)

### 8. přednáška

#### Chordální grafy

{% math definition "chordální graf" %}Graf je chordální, pokud neobsahuje \(C_k, k \ge 4\) jako in. podgraf.{% endmath %}
- alternativní pohled vycházející ze jména: každá kružnice má _chordu_ (tětivu)

{% math definition %}Nechť \(x, y\) dva nesousední vrcholy \(G\). \(R\) je \(x{\text -}y\)-řez, pokud je to řez takový, že \(x, y\) patří do různých komponent \(G \setminus R\).{% endmath %}

{% math claim %}\(G\) je chordální \(\iff\) pro každé dva nesousední vrcholy \(x, y \in V, x \neq y\) existuje \(x{\text -}y\)-řez, který je klika.{% endmath %}

{% math proof %} \(\Leftarrow\) nechť \(G\) není chordální, tedy obsahuje indukovanou kružnici \(C_4\). Uvážíme-li dva její nesousední vrcholy, tak jakýkoliv řez musí obsahovat vrcholy z horní a dolní cesty mezi \(x\) a \(y\). Ty nesousedí, tedy řez nebude klika.

\(\Rightarrow\) nechť \(G\) je chordální, \(x, y\) nesousední. Nechť \(R\) je \(x{\text -}y\)-řez s co nejméně vrcholy. Tvrdím, že \(R\) tvoří kliku.

Pro spor: \(R\) není klika \(\Rightarrow\) obsahuje \(u, v\) nesousedy. Protože \(R\) je nejmenší, má \(u\) i \(v\) sousedy na obou stranách. Jelikož jsou to komponenty souvislosti, tak tam bude existovat cesta. Vezmu nejkratší cesty \(P_x, P_y\) v komponentách \(G_x\), \(G_y\). Vrcholy \(P_x, P_y\) nesousedí (jinak by \(R\) nebyl řez), \(P_x-u-P_y-v\) tvoří indukovaný cyklus.

{% xopp another1 %}

{% endmath %}

{% math definition %}Vrchol \(x\) je v grafu \(G\) simpliciální, pokud jeho sousedství \(N_G(x)\) tvoří kliku \(G\).{% endmath %}

{% math theorem %}Každý chordální graf (kromě prázdného) obsahuje simpliciální vrchol.{% endmath %}
- dokážeme pomocí silnějšího tvrzení

{% math theorem %}Každý chordální graf je buď úplný, nebo obsahuje dva nesousední simpliciální vrcholy.{% endmath %}

{% math proof %}indukcí podle \(|V(G)|\)
- základ: \(|V(G)| = 1\) platí
- pro více vrcholů
	- \(G\) je úplný, platí
	- nebo nechť \(x, y\) nesousedi v \(G\) a \(R\) je \(x{\text -}y\)-řez tvořící kliku
		- \(G_x^+ = \left(\text{komponenta $G \setminus R$ obsahující $x$}\right) \cup R\), obdobně \(G_y^+\)
		- {% math observation %}pokud \(G\) byl chordální, pak \(H \le G\) je také chordalní{% endmath %}
		- použijeme IP na \(G_x^+\)
			- pokud \(G_x^+\) klika, vezmi jako \(s_x\) libovolný vrchol \(G_x\) (např. \(x\))
			- pokud \(G_x^+\) není klika, má dva simpliciální vrcholy; nejvýše jeden může ležet v \(R\), jelikož je to klika a za \(s_x\) zvolím ten druhý; analogicky pro \(G_y^+\)
			- {% math observation %}jelikož \(R\) je řez, tak se sousedství nezmění: \(N_{G_x^+}(s_x) = N_{G}(s_x)\) (proto vlastně děláme indukci přes \(G_x^+\), né jen přes \(G_x\){% endmath %} 

{% xopp another2 %}
{% endmath %}

<!---MARKDOWN-->

{:.rightFloatBox}
<div markdown="1">
![](/assets/kombinatorika-a-grafy-ii/dog.svg)
</div>

<!---PDF
\begin{wrapfigure}{R}{0.2\textwidth} 
\centering
\fbox{\includesvg{../assets/kombinatorika-a-grafy-ii/dog.svg}}
\end{wrapfigure}
-->
{% math definition "PES" %} Perfektní eliminační schéma (PES) grafu \(G\) je pořadí vrcholů \(v_1, \ldots, v_n\) t. ž. \(\forall i \in [n]\) platí, že leví sousedé \(v_i\) (\(= \left\{v_j \mid j < i, v_jv_i \in E\right\}\)) tvoří kliku.{% endmath %}

{% math theorem %}G je chordální \(\iff\) G má PES.{% endmath %}

{% math proof %}\(\Leftarrow\) obměnou nechť \(G\) není chordální a má tedy indukovanou kružnici velikosti alespoň \(4\). Pro spor nechť máme PES. Nejlevější vrchol špatné kružnice v PES nemá souseda na této kružnici, což je spor s definicí PES.

\(\Rightarrow\) nechť \(G\) je chordální. Má tedy simpliciální vrchol \(v_n\). Jeho sousedé tvoří kliku a \(G - v_n\) je opět chordální (indukovaný graf chordálního je opět chordální) a opakujeme, čímž vznikne PES pro \(G\).
{% endmath %}

{% math consequence %}pro daný graf \(G\) lze v polynomiálním čase rozhodnout, zda je chordální.{% endmath %}

{% math proof %}Trháme simpliciální vrcholy, které chordální graf musí vždy mít -- ty umíme v polynomiálním čase najít otestováním všech sousedů. Pokud simpliciální vrchol v nějakém bodě nenajdeme, tak graf chordální být nemohl.{% endmath %}

{% math consequence %}chordální grafy jsou perfektní.{% endmath %}

{% math proof %}Je-li graf \(G\) chordální, pak má PES, pomocí kterého ho umíme obarvit tak, aby měl nejvýše \(\omega(G)\). Jelikož je navíc každý indukovaný podgraf chordálního grafu také chordální, tak platí i pro indukované podgrafy, což potřebujeme pro perfektnost.{% endmath %}

{% math definition %}\(G\) je hamiltonovský, pokud má kružnici na \(n\) vrcholech (jako podgraf).{% endmath %}

{% math theorem "Bondyho-Chvátalova" %}Nechť \(G\) je graf na \(n \ge 3\) vrcholech. Nechť \(x,y\) jsou nesousedé t. ž. \(\deg_G(x) + \deg_G(y) \ge n\). Nechť \(G^+ = (V, E \cup \left\{xy\right\})\). Pak \(G\) je hamiltonovský \(\iff\) \(G^+\) je hamiltonovský.{% endmath %}

{% math proof %} \(\Rightarrow\) jasné

\(\Leftarrow\) nechť \(C\) je hamiltonovská kružnice \(G^+\) a \(x,y\) vrcholy splňující podmínku.
- pokud \(C\) neobsahuje \(xy\), pak \(C\) je hamiltonovská kružnice \(G\)
- jinak \(v_1, \ldots, v_n\) očíslujeme vrcholy \(C\) a navíc \(v_1 = x, v_n = y\)
	- chceme \(C' := \left(C \setminus \left\{xy, v_iv_{i + 1}\right\}\right) \cup \left\{v_iy, v_{i + 1}x\right\}\) je ham. kružnice v \(G\)
	- \(I_1 := \left\{i \in \left\{2, \ldots, n - 2\right\}\ \text{t. ž. }\left\{x, v_{i + 1}\right\} \in E\right\}\) (vrcholy dobré pro \(x\))
		- povoluji vrcholy \(v_3, \ldots, v_{n-1}\), viz. indexování
	- \(I_2 := \left\{i \in \left\{2, \ldots, n - 2\right\}\ \text{t. ž. }\left\{y, v_i\right\} \in E\right\}\) (vrcholy dobré pro \(y\))
		- povoluji vrcholy \(v_2, \ldots, v_{n - 2}\), viz. indexování
	- \(|I_1 \cup I_2| \le n - 3\) (pozor, indexování je posunuté!
	- \(|I_1| = \deg_G(x) - 1\) (nesmím použít \(v_2\))
	- \(|I_2| = \deg_G(y) - 1\) (nesmím použít \(v_{n - 1}\))
	- \(|I_1| + |I_2| = \deg_G(x) - 1 + \deg_G(y) - 1 \ge n - 2\) (z předpokladu)
	- \(|I_1 \cup I_2| \le 3\) ale \(|I_1 + I_2| \ge n - 2\) znamená, že se překrývají

{% xopp another3 %}
{% endmath %}

{% math theorem "Dirac" %}\(G\) graf na \(n \ge 3\) vrcholech s min. stupněm \(\ge n/2\) je hamiltonovský.{% endmath %}

{% math proof %}Z Bondy-Chvátalovy věty doplníme na \(K_n\), který je hamiltonovský.{% endmath %}

### 9. přednáška

#### Tutteův polynom

{% math definition: "multigraf" %} \(G = (V, E)\) kde \(V\) jsou vrcholy a \(E\) multimnožina prvků z \(V \cup \binom{V}{2}\){% endmath %}
- odstranění a kontrakce fungují intuitivně -- kontrakce nezahazuje hrany, protože máme multigraf

{% math definition "most" %}hrana \(e \in E\) je most, v multigrafu \(G\), pokud \(G - e\) má více komponent než \(G\){% endmath %}
- \(k(G) = k(V, E) = \) počet komponent

{% math definition: "hodnost/rank" %}\(E\) je \(r(E) := |V| - k(G)\){% endmath %}
- intuice: \(\sim\) velikost největší „neredundantní“ podmnožiny \(F \subseteq E\) (t. ž. \(k(G) = k(F)\))

{% math proof %}Chceme dokázat, že \(F\) neobsahuje cykly a že \(r(E) = r(F)\). Víme, že \(k(G) = k(F)\).

Postupné přidávání hran z \(F\) (právě tohle zaručuje, že nemáme cykly):
- snižuje počet komponent, vždy o \(1\), tedy \(k(F) = |V| - |F|\)
- zvyšuje rank vždy o \(1\) (nastává druhý případ z tabulky dole), tedy \(r(F) = |F|\)

Spojením dostáváme \(r(F) = |F| = |V| - k(F) = |V| - k(G) = r(E)\).
{% endmath %}

{% math proof "alternativní" %}Pokud je rank \(|V| - 1\), tak je graf souvislý a přesně to odpovídá počtu hran jeho kostry. Pokud má \(2\) komponenty souvislosti, tak bude mít \(|V| - 2\) hran, protože jednu hranu z kostry odebereme a graf tím roztrhneme. Pro více komponent souvislosti opakujeme a tedy \(r(E) = |V| - k(G)\)
{% endmath %}

{% math definition: "nulita" %}\(E\) je \(n(E) := |E| - r(E)\){% endmath %}
- intuice: velikost největší „redundantní“ podmnožiny \(F \subseteq E\) (t. ž. počet komponent se nezmění po jejím odebrání) -- to dává smysl, jelikož je to \(|E| - r(E)\) a jelikož rank udává počet těch užitečných, tak nulita těch neužitečných

{% math example %}\(G = (V, E)\)

| změna                                   | \(r(E)\)     | \(n(E)\)     |
| ---                                     | ---                               | ---                               |
| přidání hrany bez změny počtu komponent | \(r(E)\)     | \(n(E) + 1\) |
| přidání hrany se změnou počtu komponent | \(r(E) + 1\) | \(n(E)\)     |

- odpovídá intuici -- hrana, která se přidala ale nezměnila souvislost (byla tedy zbytečná), zvýší nulitu, kdežto užitečná hrana zvýší rank

{% endmath %}

{% math definition: "Tutteův polynom" %}multigrafu \(G = (V, E)\) je polynom proměnných \(x, y\) definovaný jako \[T_G(x, y) := \sum_{F \subseteq E} (x - 1)^{r(E) - r(F)} \cdot (y - 1)^{n(F)}\]{% endmath %}

{% math claim %}pro \(G\) souvislý je \(T_G(1, 1)\) počet koster \(G\){% endmath %}

{% math proof %}Dosadím do polynomu a získám \(0^{r(E) - r(F)} 0^{n(F)}\). Vím, že \(x^0 \equiv 1\), tedy výraz bude počet \(F\) takových, že \(r(E) = r(F)\) a \(n(F) = 0\).
- z předpokladu souvislosti je počet komponent \(1\)
	- \(F\) musí mít také pouze \(1\), protože \(r(E) = r(F)\)
- \(n(F) = 0\) znamená, že \(0 = |F| - |V| - 1\), tedy \(|F| = |V| - 1\)
- kombinace počtu hran a souvislosti dává, že je to strom a tedy kostra
{% endmath %}

{% math claim %}Nechť \(G_1 = (V_1, E_1), G_2 = (V_2, G_2)\) jsou multigrafy, t. ž. \(|V_1 \cap V_2| \le 1\), \(|E_1 \cap E_2| = 0\) (protínají se nejvýše v jednom vrcholu a v žádné hraně). Definujeme \(G = (V, E)\), kde \(V = V_1 \cup V_2\) a \(E = E_1 \cup E_2\). Potom \(T_G(x, y) = T_{G_1}(x, y) \cdot T_{G_2}(x, y)\)
{% endmath %}

{% math proof %}V definici kvantifikuji přes podmnožiny hran. Ty ale můžu vždy rozdělit na disjunktní sjednocení podle \(E_1\) a \(E_2\). Navíc:
- \(r(F) = r(F_1) + r(F_2)\) (z pohledu jako největší neredundantní množina hran)
- \(n(F) = n(F_1) + n(F_2)\) (analogicky, opět z intuice)

Pak rozepíšu:
\[
\begin{aligned}
	T_G(x, y) &= \sum_{F \subseteq E} (x - 1)^{r(E) - r(F)} (y - 1)^{n(F)} \\
	          &= \sum_{F_1 \subseteq E_1} \sum_{F_2 \subseteq E_2} (x - 1)^{r(E_1 \cup E_2) - r(F_1 \cup F_2)} (y - 1)^{n(F_1 \cup F_2)} \\
	          &= \sum_{F_1 \subseteq E_1} \sum_{F_2 \subseteq E_2} (x - 1)^{r(E_1) - r(F_1) + r(E_2) - r(F_2)} (y - 1)^{n(F_1) +n(F_2) } \\
	          &= \sum_{F_1 \subseteq E_1} \sum_{F_2 \subseteq E_2} (x - 1)^{r(E_1) - r(F_1)} (x - 1)^{r(E_2) - r(F_2)} (y - 1)^{n(F_1)} (y - 1)^{n(F_2)} \\
	          &= \sum_{F_1 \subseteq E_1} (x - 1)^{r(E_1) - r(F_1)}(y - 1)^{n(F_1)}  \left(\sum_{F_2 \subseteq E_2} (x - 1)^{r(E_2) - r(F_2)} (y - 1)^{n(F_2)}\right) \\
	          &= T_{G_1}(x, y) \cdot T_{G_2}(x, y) \\
\end{aligned}
\]
{% endmath %}

{% math consequence %}dva grafy se stejným Tutteovým polynomem nemusí být stejné.
- vyplývá přímo z předpokladu -- že se mohou protínat v nejvýše \(1\) vrcholu
- neobsahuje tedy informaci o počtu komponent či počtu vrcholů
{% endmath %}

{% math theorem %}Nechť \(G = (V, E)\) je multigraf. Potom \(T_G(x, y)\) je jednoznačně určen rekurencemi:
{% endmath %}

| \(E = \emptyset\) | \(T_G(x, y) = 1\)                                                         |
| most \(e\)        | \(T_G(x, y) = x \cdot T_{G - e}(x, y)= x \cdot T_{G \setminus e}(x, y)\)  |
|                                        | poslední rovnost: z důsledku výše                                                              |
| smyčka \(e\)      | \(T_G(x, y) = y \cdot T_{G - e}(x, y) = y \cdot T_{G \setminus e}(x, y)\) |
|                                        | poslední rovnost: odstranění smyčky je to stejné jako její kontrakce                           |
| jindy                                  | \(T_G(x, y) = T_{G - e}(x, y) + T_{G \setminus e}(x, y)\)           |

{% math proof %}Pro \(E = \emptyset\) jasné, jinak rozdělíme:

\[T_G(x, y) = \underbrace{\sum_{F \subseteq E, e \not\in F} (x - 1)^{r(E) - r(F)} \cdot (y - 1)^{n(F)}}_{s_1} + \underbrace{\sum_{F \subseteq E, e \in F} (x - 1)^{r(E) - r(F)} \cdot (y - 1)^{n(F)}}_{s_2}\]

Stačí dokázat následující (a dosazení do výrazu výše):
1. pokud \(e\) není most, tak \(s_1 = T_{G - e}(x, y)\)
	- \(e\) není most, jeho odebráním se rank nezmění, tedy \(r(E) = r(E \setminus \left\{x\right\})\)
2. pokud \(e\) je most, tak \(s_1 = (x - 1) \cdot T_{G - e}(x, y)\)
	- \(e\) je most, jeho odebráním se rank zmenší o \(1\), tedy \(r(E) = r(E \setminus \left\{x\right\}) + 1\)
3. pokud \(e\) není smyčka, tak \(s_2 = T_{G \setminus e}(x, y)\)
	- \(e\) není smyčka, kontrakce však zachová zbylé hrany (jsme v multigrafu) jako smyčky a nulita se tedy nezmění (jelikož, pokud to chápu správně, se spojením vlastně zmenší jak počet hran, tak vrcholů)
4. pokud \(e\) je smyčka, tak \(s_2 = (y - 1) \cdot T_{G \setminus e}(x, y)\)
	- \(e\) je smyčka, kontrakcí se nulita zmenší o \(1\), tedy \(\)

Poté pro větu stačí následující:
- \(e\) je most: (2) + (3)
- \(e\) je smyčka: (1) + (4)
- \(e\) není most ani smyčka: (1) + (3)

{% endmath %}

{% math definition: "chromatický polynom" %}multigrafu \(G = (V, E)\) je funkce \(\mathrm{ch}_G(b): \mathbb{N}_0 \mapsto \mathbb{N}_0\), kde pro \(b \in \mathbb{N}_0\) je \(\mathrm{ch}_G(b) := \) počet dobrých obarvení (posunutí udělá nové obarvení) \(G\) pomocí barev \(\left\{1, \ldots, b\right\}\).
{% endmath %}
- pokud \(G\) má smyčku, pak \(\mathrm{ch}_G(b) = 0, \forall b\)

{% math theorem %}Pro každý multigraf \(G = (V, E)\) platí
\[\mathrm{ch}_G(b) = \left(-1\right)^{|V| + k(G)} \cdot b^{k(G)} \cdot T_G(1 - b, 0)\]
{% endmath %}

### 10. přednáška

#### Formální mocniné řady
{% math definition %}Pro posloupnost reálných čísel \(a_0, a_1, \ldots\) je formální mocninná řada (FMŘ) zápis tvaru \(a_0 + a_1x^1 + a_2x^2 + \ldots = \sum_{i = 0}^{\infty} a_i x^i\){% endmath %}
- \(\mathbb{R} \llbracket x \rrbracket \ldots\) všechny FMŘ nad \(x\)
- pro \(A(x) = a_0 + a_1 x + a_2x^2 + \ldots\) je \([x^n]A(x) = a_n\)
- pro FMŘ \(A(x), B(x)\) je
	- \(A(x) + B(x) = (a_0 + b_0) + (a_1 + b_1)x + (a_2 + b_2)x^2 + \ldots\)
	- \(A(x) \cdot B(x) = c_0 + c_1x + c_2x^2 + \ldots\), kde \(c_n = a_0 b_n + a_1 b_{n - 1} + \ldots + a_{n - 1}b_1 + a_{n} b_0\) (konvoluce)

{% math fact %} \(\mathbb{R}\llbracket x \rrbracket\) tvoří (komutativní) okruh (máme \(+, \cdot, 0, 1\)){% endmath %}
- \(0 = A(x)\) s nulovými koeficienty
- \(1 = A(x)\) s \(a_0 = 1\) a zbytek nulové koeficienty

{% math fact %} \(\mathbb{R}\llbracket x \rrbracket\) tvoří vektorový postor (násobení konstantou je FMŘ pro \(a_0 = c\){% endmath %})

{% math definition "převrácená hodnota" %} FMŘ \(A(x)\) je taková FMŘ, že \(A(x) \cdot B(x) = 1\){% endmath %}

- \(A(x) = c \ldots B(x) = \frac{1}{c}\)
- \(A(x) = x \ldots B(x)\) není (muselo by být něco jako \(\frac{1}{x}\))
- \(A(x) = 1 - x \ldots B(x) = 1 + x + x^2 + \ldots\)
	- \(C(x) = A(x) \cdot B(x) = (1 + x + x^2 + \ldots) - (x + x^2 + x^3 + \ldots)\), kde \([x^n]C(x)\) bude nulové pro \(n \ge 1\) (požere se to), proto \((1 + x + x^2 + \ldots) = \frac{1}{1 - x}\)

{% math claim %}Nechť \(A(x) = \sum_{n = 0}^{\infty} a_n x^n\) je FMŘ. Potom \(\frac{1}{A(x)}\) existuje, právě když \(a_0 \neq 0\) (a pak je jednoznačně určena).{% endmath %}

{% math proof %}Hledejme inverz. Rozepsáním \(A(x) \cdot B(x) = 1 + 0x + 0x^2 + \ldots\) nám dává soustavu takovýchto rovnic, které mají jednoznačné řešení:

\[
\begin{aligned}
	a_0 b_0 = 1 &\qquad b_0 = \frac{1}{a_0} \\
	a_0 b_1 + a_1b_0 = 0 &\qquad b_1 = \frac{1}{a_0}(-a_1 b_0)\\
	a_0 b_2 + a_1b_1 + a_2b_0 = 0 &\qquad b_2 = \frac{1}{a_0} (-a_1 b_1 - a_2b_2) \\
	                          &\;\;\;\vdots \\
\end{aligned}
\]
{% endmath %}

{% math definition "složení" %}\(A(x) = \sum a_nx^n, B(x) = \sum b_nx^n\) jsou FMŘ. Složení je \(A(B(x)) = a_0B(x)^0 + a_1B(x)^1 + \ldots\) {% endmath %}. Obecně je problém to zadefinovat, potřeboval bych znát hodnotu součtu, ale jde to, když:

1. \(A(x)\) je polynom (\(\equiv \exists n_0 \in \mathbb{N}\) t. ž. \(\forall n \ge n_0: a_n = 0\))
\[a_0 B(x)^0 + a_1B(x)^1 + a_2B(x)^2 + \ldots + \underbrace{a_{n_0}B(x)^{n_0} + \ldots}_{= 0}\]
2. \(b_0 = 0\)
	- chci ukázat, že součet \(\left[x^n\right]A(B(x)) = \left[x^n\right]a_0B(x)^0 + \left[x^n\right]a_1B(x)^1 + \ldots\) je konečný
		- \(\left[x^0\right]B(x) = b_0 = 0\)
		- \(B(x) = x \tilde{B}(x)\) pro \(\tilde{B}(x)\) FMŘ
		- \(B(x)^k = x^k \tilde{B}(x)^k\), koeficient u \(x^{k - 1}, x^{k - 2}, \ldots, x^0\) je nulový, tedy všechny koeficienty \(\left[x^k\right] A(B(x))\) pro \(k > n\) jsou nulové

{% math definition: "derivace" %}FMŘ \(A(x)\) značená \(\frac{d}{dx}A(x) = \sum a_{n + 1}(n + 1)x^n = a_1 + 2a_2x + 3a_3x^3 + \ldots\){% endmath %}

{% math example %} Můžu mít také FMŘ více proměnných, např. \(A(x, y) = \sum_{n \ge 0, m \ge 0} a_{n, m} \cdot x^n \cdot y^m \in \mathbb{R}\llbracket x, y \rrbracket\)
{% endmath %}

#### Obyčejné vyvořující funkce
{% math definition "OVF" %}Nechť \(\mathcal{A}\) je množina, jejíž každý prvek \(\alpha \in \mathcal{A}\) má definovanou velikost \(|\alpha| \in \mathbb{N}_0\), předpokládáme že \(\forall n \in \mathbb{N}_0\) je v \(\mathcal{A}\) konečně mnoho prvků velikosti \(n\).
- \(\mathcal{A}_n = \left\{\alpha \in \mathcal{A} \mid |\alpha| = n\right\}, a_n = |\mathcal{A}_n|\)

Potom **obyčejná vytvořující funkce** pro \(\mathcal{A}\) je FMŘ \[\mathrm{OVF}(\mathcal{A}) = \sum_{n \ge 0} a_n x^n\]{% endmath %}

{% math example %} Jídla (\(\mathcal{J} = \mathcal{P} \cup \mathcal{H}\)):
- Polévky (\(\mathcal{P}\))
	- gulášová: \(30\)
	- knedlíčková: \(35\)
- Hlavní jídla (\(\mathcal{H}\))
	- guláš: \(100\)
	- řízek: \(100\)
	- smažák: \(90\)

- \(P(x) = \mathrm{OVF}(\mathcal{P}) = x^{30} + x^{35} \)
- \(H(x) = \mathrm{OVF}(\mathcal{H}) = x^{90} + 2x^{100} \)
- \(J(x) = P(x) + H(x)\)

- {% math observation %}\(\mathrm{OVF}(\mathcal{A} \cup \mathcal{B}) = \mathrm{OVF}(\mathcal{A}) + \mathrm{OVF}(\mathcal{B})\){% endmath %} 
- {% math observation %}\(\mathrm{OVF}(\mathcal{A}) \cdot \mathrm{OVF}(\mathcal{B}) = \mathrm{OVF}(\mathcal{A} \times \mathcal{B})\){% endmath %}
	- \(P(x) \cdot H(x) = \) kartézský součin dvojic (polívka, hlavní jídlo)
	- \([x^{130}](J(x) \cdot J(x)) = \) počet uspořádaných dvojic jídel, které se sečtou na \(130\)

{% endmath %}

### 11. přednáška
#### Exponenciální vytvořující funkce
Chci dojít k \(L(x)\), což bude vytvořující funkce pro počet lesů na \(n\) vrcholech, pomocí \(S(x)\) vytvořující funkce pro počet stromů na \(n\) vrcholech.

Nechť \(s_n\) je počet stromů na vrcholech \(\left\{1, \ldots, n\right\}\)
\[S(x) = \sum_{n \ge 0} s_n \cdot \frac{x^n}{n!} \qquad \in \mathbb{R}\llbracket x \rrbracket\]

Nechť \(k_n\) je počet kružnic na vrcholech \(\left\{1, \ldots, n\right\}\)
\[K(x) = \sum_{n \ge 0}  k_n \cdot \frac{x^n}{n!} \]

Definujeme \(A(x) = S(x) \cdot K(x)\) a \(a_0, a_1, \ldots\) tak, aby \(A(x) = \sum_{n \ge 0} a_n \cdot \frac{x^n}{n!} \)

Potom platí, že \(a_n = \sum_{j = 0}^{n} \binom{n}{j} \cdot s_j \cdot k_{n - j}\), tedy \(a_n = \) počet grafů na \(n\) vrcholech mající dvě komponenty souvislosti, z nichž jedna je strom a druhá kružnice:
\[
\begin{aligned}
	\left[x^n\right]\left(S(x) \cdot K(x)\right) &= \sum_{j = 0}^{n} \left(\left[x^j\right] S(x)\right) \cdot \left(\left[x^{n - j}\right] K(x)\right) \\
	&= \sum_{j = 0}^{n} \frac{s_j}{j!} \cdot \frac{k_{n - j}}{(n - j)!} \\
	&= \sum_{j = 0}^{n} \frac{n!}{j!(n - j)!} \cdot \frac{1}{n!} \cdot s_j k_{n - j} \\
	&= \frac{1}{n!}\sum_{j = 0}^{n} \binom{n}{j} s_j k_{n - j} \\
	&= \left[x^n\right] A(x)
\end{aligned}
\]

Definujeme \(B(x) = S(x)^2\) a \(b_0, b_1, \ldots\) tak, aby \(B(x) = \sum_{n \ge 0} b_n \cdot \frac{x^n}{n!}\)
- počet způsobů, jak rozdělit vrcholy na červené a modré a vytvořit strom na každé barvě
\[b_n = \sum_{j = 0}^{n} \binom{n}{j} \cdot s_j \cdot s_{n - j}\]

Dále definujeme hromadu dalších věcí:
- \(C(x)\) jako \(c_n = \frac{b_n}{2}\), abychom měli počet lesů se dvěma komponentami, tedy \(C(x) = \frac{1}{2} B(x) = \frac{1}{2} S^2(x)\).
- \(D(x) = S^k(x)\), tedy \(d_n\) je počet uspořádaných \(k\)-tic stromů tvořící rozklad vrcholů
- \(E(x) = \frac{S^k(x)}{k!}\), tedy \(e_x\) je počet lesů s \(k\) komponentami

Konečně vyjádříme \[L(x) = 1 + S(x) + \frac{S^2(x)}{2!} + \ldots = \sum_{n \ge 0} \frac{S^n(x)}{n!} = \mathrm{exp}(S(x)) = e^{S(x)}\]

---

V následujících definicích a pozorováních je _takovýhle text_ odkaz na to, co si pod tím představovat v rámci minulého příkladu.

{% math definition "EVF" %}Mějme množinu \(\mathcal{A}\) (_všechny konečné stromy s očíslovanými vrcholy_), předpokládejme:
1. každý prvek \(\alpha \in \mathcal{A}\) (_nějaký strom_) má množinu vrcholů (_vrcholů_) \(V(\alpha) \subseteq \mathbb{N}, V(\alpha)\) konečná
2. pro každou konečnou \(V \subseteq \mathbb{N}\) existuje konečně mnoho \(\alpha \in \mathcal{A}\) t. ž. \(V(\alpha) = V\) 
	- (_existuje konečné množství stromů_)
3. pro dvě konečné množiny \(V, W \subseteq \mathbb{N}\) t. ž. \(|V| = |W|\) platí, že počet \(\alpha \in \mathcal{A}\) t. ž. \(V(\alpha) = V\) je stejný jako \(\alpha \in \mathcal{A}\) t. ž. \(V(\alpha) = W\) (co do počtu, záleží jen na velikosti množiny vrcholů)
	- (_dvě stejně velké množiny vrcholů mají stejný počet stromů_)

Potom **exponenciální vytvořující funkce** pro \(\mathcal{A}\) je \[\mathrm{EVF(\mathcal{A})} = \sum_{n \ge 0} a_n \frac{x^n}{n!}\]kde \[a_n = \#\ \alpha \in \mathcal{A} \text{ t. ž. } V(\alpha) = \left\{1, \ldots, n\right\}\]
{% endmath %}

{% math observation %}Nechť \(A(x)\) je \(\mathrm{EVF(\mathcal{A})}, B(x) = \mathrm{EVF}(\mathcal{B})\), potom:
1. pokud \(\mathcal{A}, \mathcal{B}\) jsou disjunktní (příklad výše), pak \(A(x) + B(x)\) je \(\mathrm{EVF}(\mathcal{A} \cup \mathcal{B})\)
	- stejné jako u \(\mathrm{OFV}\), protože \(\left[x^n\right] \left(A(x) + B(x)\right) = \frac{a_n}{n!} + \frac{b_n}{n!} = \frac{a_n + b_n}{n!}\)
2. \(A(x) \cdot B(x) = \sum c_n \frac{x^n}{n!}\), kde \(c_n\) je počet uspořádaných dvojic \(\left(\alpha, \beta\right)\) t.ž. \(\alpha \in \mathcal{A}, \beta \in \mathcal{B}, V(\alpha) \cup V(\beta) = \left\{1, \ldots, n\right\}\) (tvoří rozklad)
3. \(A^k(x) = \sum d_n \frac{x^n}{n!}\), kde \(d_n\) je počet uspořádaných \(k\)-tic \((\alpha_1, \ldots, \alpha_k)\), kde
\[\alpha_1, \ldots, \alpha_k \in \mathcal{A} \text{ t.ž. } V(\alpha_1) \cup \ldots \cup V(\alpha_k) = \left\{1, \ldots, n\right\} \qquad \star\]
4. pokud \(V(\alpha) \neq \emptyset, \forall \alpha \in \mathcal{A}\), pak \[\frac{A^k(x)}{k!} = \sum e_n \frac{x^n}{n!}\]kde \(e_n\) je počet \(k\)-prvkových množin splňujících \(\star\)
5. pokud \(\forall \alpha \in \mathcal{A}: V(\alpha) \neq \emptyset\), pak \[\mathrm{exp}(\mathcal{A}(x)) = e^{A(x)} = 1 + A(x) + \frac{A^2(x)}{2} + \ldots = \sum_{n \ge 0} f_n \frac{x^n}{n!}\] kde \(f_n\) je počet množin \(\left\{\alpha_1, \ldots, \alpha_k\right\} \subseteq \mathcal{A}\), kde \(V(\alpha_1) \cup \ldots \cup V(\alpha_{k}) = \left\{1, \ldots, n\right\}\)

{% endmath %}

#### Groupy a Burnside
{% math definition "akce grupy" %}nechť \(A\) je množina, nechť \(\Gamma\) je grupa, \(1_\Gamma\) její neutrální prvek. Potom akce grupy \(\Gamma\) na množině \(A\) je binární operace \(\cdot: \Gamma \times A \mapsto A\) t.ž.
1. \(\forall x \in A: 1_\Gamma \cdot x = x\)
2. \(\forall \gamma, \delta \in \Gamma, \forall x \in A: \gamma \cdot (\delta \cdot x) = (\gamma \delta) \cdot x\)
	- pozor, \(\cdot\) a \(\gamma\delta\) jsou jiné operace
{% endmath %}

{% math observation %}Pokud \(\gamma \in \Gamma, \gamma^{-1}\) je inverzní prvek k \(\gamma\), potom \(\forall x, y \in A: \gamma \cdot x = y \iff \gamma^{-1} \cdot y = x\){% endmath %}

{% math consequence %}\(\forall p \in \Gamma:\) zobrazení \(x \mapsto p \cdot x\) je bijekce \(A \longleftrightarrow A\){% endmath %}

### 12. přednáška
{% math definition: "množina pevných bodů" %}\(\gamma \in \Gamma\), značená \(\mathrm{Fix}(\gamma) = \left\{x \in A \mid \gamma x = x\right\}\){% endmath %}

{% math definition: "stabilizátor" %} prvku \(x \in A\) je \(\mathrm{Stab}(x) = \left\{\gamma \in \Gamma \mid \gamma x = x\right\}\){% endmath %}

{% math observation %}\(\gamma \in \Gamma, x \in A: \gamma \in \mathrm{Stab}(x) \iff x \in \mathrm{Fix}(\gamma) \iff \gamma x = x\){% endmath %}

{% math observation %}\(\mathrm{Stab}(x)\) je podgrupa \(\Gamma\)
- \(1_\Gamma \in \mathrm{Stab}(x)\), protože \(1_\Gamma x = x\)
- \(\gamma \in \mathrm{Stab}(x) \Rightarrow \gamma^{-1} \in \mathrm{Stab}(x)\) z pozorování \(\gamma x = y \iff x = \gamma^{-1}y\)
- \(\gamma, \delta \in \mathrm{Stab}(x) \Rightarrow \gamma x = x, \delta x = x\), dosazením dostávám \(\gamma \delta x = x\)
{% endmath %}

Prvky \(x, y \in A\) jsou ekvivalentní (značím \(x \sim_{\Gamma} y\)), pokud \(\exists \gamma \in \Gamma\) t.ž. \(\gamma x = y\)
- {% math observation %}\(\sim_{\Gamma}\) je to ekvivalence:{% endmath %}
	- reflexivní -- \(x = 1_\Gamma x\)
	- symetrická -- \(\gamma x = y \iff \gamma^{-1}y = x\)
	- transitivní -- \(\gamma x = y \land \gamma y = z \Rightarrow (\delta \gamma)x = z\)

{% math definition: "orbita" %} obsahující prvek \(x \in A\) je množina \[\left[x\right]_{\Gamma} = \left\{y \in A \mid x \sim_\Gamma y\right\} = \left\{\gamma x \mid \gamma \in \Gamma\right\}\]
možinu orbit značíme \(A / \Gamma\).
{% endmath %}

{% math example %}Koláčky (mák, tvaroh, povidla).

\[\mathcal{K} = \left\{\boxed{a{b\atop c} d} \mid a, b, c, d \in \left\{T, M, P\right\}\right\} \qquad |\mathcal{K}| = 3^4 = 81\]

\[\Gamma = \left\{\text{otočení o násobky 90$\degree$ mod 360$\degree$}\right\} = \left\{0\degree, 90\degree, 180\degree, 270\degree \right\}\]

- akce odpovídají otočením koláčku.
- \(\mathrm{Fix}(180\degree) = \left\{\boxed{a{b\atop b} a} \mid a, b \in \left\{T, M, P\right\}\right\}\)
- \(\mathrm{Stab\left(\boxed{M{T\atop P} M}\right)} = \left\{0\degree\right\}\)
- \(\left[\boxed{M{T\atop P} M}\right] = \left\{\boxed{M{T\atop P} M}, \boxed{P{M\atop M} T}, \boxed{M{P\atop T} M}, \boxed{T{M\atop M} P}\right\}\)
{% endmath %}

{% math lemma "o orbitě stabilizátoru" %}Nechť \(\Gamma\) je konečná grupa s akcí na množině \(A\). Potom \[\forall x \in A: |\mathrm{Stab(x)}| \cdot |\left[x\right]| = |\Gamma|\] {% endmath %}

{% math proof %}Nechť množina \(\mathrm{Map}(x, y)\) je množina akcí \(a\), pro které \(a \cdot x = y\). Pro akce \(\sigma \in \mathrm{Map}(x, y)\) pomocí \(\sigma a \sigma^{-1}\) lze definovat bijekci mezi \(\mathrm{Map}(x, x)\). Poté \[\forall x \in A, |\Gamma| = \sum_{y \in [x]} |\mathrm{Map}(x, y)| = \sum_{y \in [x]} |\mathrm{Stab}(x)| = |[x]| |\mathrm{Stab}(x)|\]
{% endmath %}

{% math theorem "Burnsideovo lemma" %}Nechť \(\Gamma\) je konečná grupa s akcí na \(A\)
{% endmath %}
1. (jednoduchá) pokud \(A\) je konečná, pak \[|A / \Gamma| = \frac{1}{|\Gamma|} \sum_{\gamma \in \Gamma} |\mathrm{Fix}(\gamma)|\] \(=\) počet orbit je roven „průměrnému počtu pervných bodů“
2. Nechť každá orbita \(o \in A / \Gamma\) má přiřazenou váhu \(w(o)\). Potom \[\sum_{o \in A/\Gamma} w(o) = \frac{1}{|\Gamma|} \sum_{\gamma \in \Gamma} \sum_{x \in \mathrm{Fix}(\gamma)} w([x])\]

{% math proof %} \((2) \Rightarrow (1)\), když jsou váhy \(1\).

\((2)\) -- dvojím počítáním \(s := \sum_{\left(\gamma, x\right) \in \Gamma \times A, \gamma x = x} w([x])\)

\[s = \sum_{\gamma \in \Gamma} \sum_{x \in \mathrm{Fix}(\gamma)} w([x]) \qquad \text{z definice}\]

\[ \begin{aligned}
	s &= \sum_{x \in A} \sum_{\gamma \in \mathrm{Stab}(x)} w([x])  \qquad \text{počítání obráceně, přes $\mathrm{Stab}$} \\
	  &= \sum_{o \in A / \Gamma} \sum_{x \in o} \sum_{\gamma \in \mathrm{Stab}(x)} w(o) \qquad w([x])\text{ závisí pouze na váze orbity}\\
	  &= \sum_{o \in A / \Gamma} \sum_{x \in o} |\mathrm{Stab}(x)| w(o) \qquad \text{vnitřní suma závisí na $\mathrm{Stab}(x)$} \\
	  &= \sum_{o \in A / \Gamma} \sum_{x \in o} \frac{|\Gamma|}{|o|} w(o) \qquad \text{lemma o orbitě a stabilizátoru} \\
	  &= \sum_{o \in A / \Gamma} |o| \frac{|\Gamma|}{|o|} w(o) \qquad \text{obsah sumy závisí na velikosti orbity} \\
	  &= |\Gamma| \sum_{o \in A / \Gamma} w(o) \\
\end{aligned} \]
{% endmath %}

Poté první a druhý způsob dám do rovnosti, vydělím velikostí grupy a hotovo.

{% math example %}
Koláčky na steroidech: množina koláčků \(\mathcal{R}\), v každé části nezáporný počet rozinek, akce jsou stejné.

Pro \(k \in \mathbb{N}_0, a_k = \) počet orbit, jejichž koláčky mají celkem \(k\) rozinek. Cíl je získat vzorec pro \(A(x) = \sum_{n \ge 0} a_n x^n\)

Použijeme obecnější Burnsideovo lemma. Chceme, aby \[A(x) = \sum_{o \in A/\Gamma} w(o) = \frac{1}{|\Gamma|} \sum_{\gamma \in \Gamma} \sum_{x \in \mathrm{Fix}(\gamma)} w([x])\]

Váhu orbity s \(k\) rozinkami nastavíme na \(x^k\). Pro \(q \in \mathcal{R}\) označím \(r(q)\) počet rozinek v \(q\), \(w([q]) = x^{r(q)}\).

| \(\gamma\)                                   | \(1_\Gamma\)                       | \(90\degree\), \(270\degree\) | \(180\degree\)                       |
| ---                                                               | ---                                                     | ---                                                                     | ---                                                       |
| \(\mathrm{Fix}(\gamma)\)                     | \(\mathcal{R}\)                    | všude je stejný počet rozinek                                           | protější strany mají stejný počet rozinek                 |
| \(\sum_{q \in \mathrm{Fix}(\gamma)} w([q])\) | \(\left(\frac{1}{1 - x}\right)^4\) | \(\frac{1}{1 - x^4}\)                              | \(\left(\frac{1}{1 - x^2}\right)^2\) |

Vytvořující funkce z tabulky jsme odvodili následně:

\[\sum_{q \in \mathrm{Fix}(\gamma) = \mathcal{R}} = \sum_{q \in \mathcal{R}} x^{r(q)} = \sum_{(a, b, c, d) \in \mathbb{N}_0^4} x^{a + b + c + d} = \left(\sum_{a \in \mathbb{N}_0} x^a\right)^4 = \left(\frac{1}{1 - x}\right)^4\]
\[\sum_{q \in \mathrm{Fix}(\gamma) = \left\{(a, a, a, a) \mid a \in \mathbb{N}_0\right\}} = \sum_{a \in \mathbb{N}_0} x^{4a} = \frac{1}{1 - x^4}\]
\[\sum_{q \in \mathrm{Fix}(\gamma) = \left\{(a, b, a, b) \mid a, b \in \mathbb{N}_0\right\}} = \left(\sum_{a \in \mathbb{N}_0} x^{2a}\right) \left(\sum_{b \in \mathbb{N}_0} x^{2b}\right) = \left(\frac{1}{1 - x^2}\right)^2\]

Tedy dostáváme, že \[A(x) = \frac{1}{4} \left(\left(\frac{1}{1 - x}\right)^4 + 2 \left(\frac{1}{1-x^4}\right) + \left(\frac{1}{1 - x^2}\right)^2\right)\]

{% endmath %}

### 13. přednáška

#### Extremální teorie grafů a hypergrafů
{% math definition %}pro graf \(H\) označím \(\mathrm{ex}(n, H)\) největší \(m\) t.ž. existuje graf \(G\) s \(n\) vrcholy, \(m\) hranami a neobsahující \(H\) jako podgraf.
{% endmath %}
- \(\mathrm{ex}(n, K_3) = |E(K_{\left\lfloor \frac{n}{2} \right\rfloor, \left\lceil \frac{n}{2} \right\rceil})| = \left\lfloor \frac{n}{2} \right\rfloor \cdot \left\lceil \frac{n}{2} \right\rceil \cong n^2\)
- \(\mathrm{ex}(n, C_4) = \mathcal{O}(n^{3/2}) = \mathcal{O}(n \sqrt{n})\)
	- viz. poznámky z [Kombinatoriky a Grafů I](/lecture-notes/kombinatorika-a-grafy-i/#grafy-bez-ckc_kck)

{% math definition %}\(k, n \in \mathbb{N}\), označme \(T_k(n)\) úplný \(k\)-partitní graf na \(n\) vrcholech, jehož všechny partity mají velikost \(\left\lfloor \frac{n}{k} \right\rfloor\) nebo \(\left\lceil \frac{n}{k} \right\rceil\). Nechť \(t_k(n) = |E(T_k(n))|\){% endmath %}
- \(k\)-partitní je to samé jako \(k\)-obarvitelný (\(\Chi(G)\))
- partity mohou být i prázdné -- \(k\)-partitní je i \(k'\)-partitní, pro \(k' \ge k\)
- úplný \(k\)-partitní -- každé \(2\) partity jsou úplný bipartitní graf

{% math observation %}\(\forall r \in \mathbb{N}, r \ge 2: \mathrm{ex}(n, K_r) \ge t_{r - 1}(n)\), protože \(T_{r - 1}(n)\) neobsahuje \(K_r\) (z každé partity si klika vezme \(\le 1\) vrchol, tedy nejvýše \(r - 1\)) {% endmath %}

{% math lemma "1" %}Každý \(k\)-partitní graf na \(n\) vrcholech má nanejvýš \(t_{k}(n)\) hran.{% endmath %}
- \(=\) \(t_{k}(n)\) jsou mezi \(k\)-partitními nejlepší

{% math proof %}Nechť \(G = (V, E)\) je \(k\)-partitní, \(P_1, \ldots, P_k\) jsou jeho partity. Navíc \(|P_1| \le |P_2| \le \ldots \le |P_k|\)
- buď \(|P_k| \le |P_{1}| + 1\), pak \(G \cong T_k(n)\)
- jinak pro spor \(|P_k| \ge |P_1| + 2\)
	- idea důkazu je ta, že vezmeme vrchol z poslední partity a přesuneme ho do první
	- nechť \(x \in P_k\), nechť \(\tilde{G}\) je úplný \(k\)-partitní s partitami \(P_1 \cup \left\{x\right\}, P_2, P_3, \ldots, P_{k} \setminus \left\{x\right\}\); potom \(|E(\tilde{G})| > |E(G)|\), což je spor:
		- stupně pro \(P_2, \ldots, P_k\) se nemění (vrcholy stále vidí \(x\), jen je teď jinde)
		- stupně pro \(P_1\) klesne o \(1\) (vrcholy přestanou vidět \(x\))
		- stupně pro \(P_k \setminus \left\{x\right\}\) vzroste o \(1\) (vrcholy začnou vidět \(x\))
		- stupně pro \(x\) vzroste alespoň o \(1\) (\(x\) přestane vidět \(P_1\) a začne vidět \(P_k\))
{% endmath %}

{% math lemma "2" %}Nechť \(G = (V, E)\) je graf neobsahující \(K_r\) jako podgraf. Potom \(\exists H = (V, E_H)\) \((r-1)\)-partitní t.ž. \(\deg_G(x) \le \deg_H(x)\) (a tudíž \(|E(G)| \le |E(H)|\)){% endmath %}
- \(=\) pro graf neobsahující \(K_r\) jako podgraf jsou \((r-1)\)-partitní nejlepší

{% math proof %}indukcí podle \(r\)
- \(r = 2 \Rightarrow G\) neobsahuje \(K_2\) a je tedy nemá hrany; \(G = H\) splňuje tvrzení (celé tvoří jednu partitu)
- \(r > 2\): \(G\) neobsahuje \(K_r\):

Nechť \(x \in V(G)\) je vrchol max. stupně v \(G\)
- \(S = N_G(x)\) (sousedství)
- \(G_S = G\left[S\right]\) (podgraf indukovaný \(S\))
	- {% math observation %}\(G_S\) neobsahuje \(k_{r - 1}\), jinak \(G\left[S \cup \left\{x\right\}\right]\) obsahuje \(k_r\){% endmath %} 
	- využijeme IP: \(\exists (r - 2)\)-partitní graf \(H_S = (S, E_{H_{S}})\)
		- splňuje (dle IP), že \(\forall y \in s: \deg_{H_S} (y) \ge \deg_{G_S}(y)\)
		- \(V \setminus S\) zadefinuji jako (\((r-1)\).) partitu a vše patřičně spojím, čímž získám \(H\)

{% xopp lol %}

Ověříme \(\forall x \in V: \deg_G(x) \le \deg_H(x)\)
1. \(y \in V \setminus S: \deg_H(y) = |S| = \deg_H(x) = \deg_G(x) \ge \deg_G(y)\) (\(x\) je vrchol s největším stupněm)
2. \(y \in S: \deg_H(y) = \deg_{H_S}(y) + |V \setminus S| \overset{\mathrm{IP}}{\ge} \deg_{G_S}(y) + |V \setminus S| \ge \deg_G(y)\)
	- rozdělili jsme to na dva případy podle toho, co vidí uvnitř a co vně \(S\)
	- poslední nerovnost plyne z toho, že \(y\) v \(G\) vidí sousedy v \(G_S\) + nanejvýš všechny z \(V \setminus S\)

{% endmath %}

{% math theorem "Turán, 1941" %}\(\forall r \ge 2: \mathrm{ex}(n, K_r) = t_{r - 1}(n)\){% endmath %}

{% math proof %} Vezmu \(G\) nějaký graf bez \(K_r\).

- už jsme (v pozorování výše) viděli \(\mathrm{ex}(n, K_r) \ge t_{r - 1}(n)\) (protože \(T_{r - 1}(n)\) neobsahuje \(K_r\))
- dle tvrzení (2) \(\exists (r-1)\)-partitní graf \(H\) t.ž. \(|E(G) | \le |E(H)|\)
- dle tvrzení (1) je \(|E(H)| \le t_{r - 1} (n) \Rightarrow |E(G)| \le t_{r - 1}(n) \Rightarrow \mathrm{ex}(n, K_r) \le t_{r - 1}(n)\)

Spojení odhadů dává rovnost.
{% endmath %}

{% math remark %}\(t_k(n) = \frac{k-1}{k} \binom{n}{2} + \mathcal{O}(n) = \frac{k - 1}{2k} n^2 + \mathcal{O}(n)\){% endmath %}

---

{% math definition %}pro graf \(H: \mathrm{ex}_\preceq(n, H)\) je maximalní počet hran grafu \(G\) na \(n\) vrcholech bez \(H\) jako minoru.{% endmath %}

{% math observation %}\(\mathrm{ex}(n, H) \ge \mathrm{ex}_\preceq(n, H)\), protože graf bez \(H\)-minoru nemá ani \(H\)-podgraf{% endmath %}
- obráceně platit nemusí.

{% math observation %}\(\mathrm{ex}_\preceq(n, K_3) = n - 1\) (dostávám stromy!){% endmath %}

{% math theorem %}\(\forall r \ge 3 \exists c_r > 0: \forall n: \mathrm{ex}_\preceq(n, K_r) < c_r \cdot n\){% endmath %}
- jinými slovy: každý graf \(G = (V, E)\) s \(|E| \ge c_r \cdot n\) obsahuje \(K_r\)-minor
- ještě jinými slovy: grafy, kterým zakážeme \(K_r\)-minor mají lineární počet hran (pro nějakou konstantu \(c_r\) závisející pouze na \(r\))

{% math proof %}dokážeme pro \(c_r = 2^{r - 3}\), indukcí dle \(r\)
- základ \(r = 3\), což jsou lesy a víme, že platí
- \(r > 3\), sporem
	- \(\exists G = (V, E)\) neobsahující \(K_r\)-minor ale \(|E| \ge c_r \cdot |V|\) a zároveň min. pro \(|V| + |E|\)
	- pokud \(G' = (V', E')\) je vlastní minor \(G\), tak \(|E'| < c_r \cdot |V'|\), jinak bychom zvolili \(G'\)

**Pomocné tvrzení:** \(\forall \left\{x, y\right\} = e \in E\) platí \(|N(x) \cap N(y)| \ge c_r\)

{% math proof %}Vezmu \(G' = G.e\)
- \(|E| \ge c_r \cdot |V|\) (protože \(G\) je protipříklad)
- \(|E'| < c_r \cdot |V'| = c_r (|V| - 1)\) (protože \(G'\) není protipříklad)

Odečtem nerovností máme \(|E| - |E'| > c_r\). Navíc \(|E| - |E'| = 1 + |N(x) \cap N(y)|\) (zanikají hrany do společných sousedů a navíc hrana \(e\)), dosazením dostáváme hledanou nerovnost.
{% endmath %}

K důkazu původního vyberu \(x \in V(G)\), \(S = N_G(x), G_S = G\left[S\right]\).
- dle pomocného tvrzení \(\forall y \in S: \deg_{G_S}(y) \ge c_r\), jelikož všichni sousedé \(x\) leží v \(S\).
- \(|E(G_S)| \ge \frac{c_r}{2} \cdot |S| = \frac{2^{r - 3}}{2} |S| = c_{r - 1} |S|\)
	- dle IP musí \(G_S\) obsahovat \(K_{r - 1}\) minor a ten spolu s \(x\) tvoří v \(G\) \(K_r\)-minor, což je spor

{% math remark %}odhad byl dost hrubý, věta platí dokonce pro \(c_r = \mathcal{O}(r \cdot \sqrt{\log r}\)){% endmath %}
{% endmath %}

{% math definition %}\(k\)-uniformní hypergraf je dvojice \((V, E)\), kde \(E \subseteq \binom{V}{k}\){% endmath %}
- \(f(k, n) :=\) max. \(m\) t.ž. \(\exists\) \(k\)-uniformní hypergraf \(H = (V, E)\) t.ž. \(|V| = n, |E| = m\) a \(E\) je „pronikající systém množin“ (t.j. \(\forall e, e' \in E: e \cap e' \neq \emptyset\))
	- braní všech hran nemusí fungovat (musí se protínat všechny dvojice)!


<!---MARKDOWN-->

{:.rightFloatBox}
{% xopp slun %}

<!---PDF
-->

{% math observation %} rozebereme několik případů:
- \(k > n: f(k, n) = 0\), protože neexistují hyperhrany
- \(k \le n < 2k: f(k, n) = \binom{n}{k}\), protože každé dvě množiny z \(\binom{V}{k}\) se protínají
- \(n \ge 2k: f(k, n) \ge \binom{n - 1}{k - 1}\) -- konstrukce, kde \(E = \left\{\left\{1\right\} \cup e' \mid e' \in \binom{\left\{2, \ldots, n\right\}}{k - 1}\right\}\)
	- „slunečnicová“ proto, že vezmeme jeden střed a poté hrany na zbylých vrcholech
{% endmath %}

{% math theorem "Erdös-Ko-Rado, 196*" %}\(\forall k, n \in \mathbb{N}: n \ge 2k \Rightarrow f(k, n) = \binom{n - 1}{k - 1}\){% endmath %}

{% math proof %} dokazujeme dva odhady:

- dolní odhad \(f(k, n) \ge \binom{n - 1}{k - 1}\) ze slunečnicové konstrukce
- horní odhad \(f(k, n) \le \binom{n - 1}{k - 1}\): máme \(H = (V, E)\) \(k\)-uniformní hypergraf t.ž. \(E\) je protínající systém množin

{% math definition %}cyklické pořadí \(\left\{1, \ldots, n\right\}\) je nějaká \(1\)-cyklová permutace \(\left\{1, \ldots, n\right\}\){% endmath %}
- \(k\)-intervaly (v tomhle příkladě \(3\)-intervaly) permutace \(C = (3, 1, 5, 4, 2, 7, 6, 8)\) jsou \(315, 154, 542, 768, 683, 831\)

{% math observation %}intervalů daného pořadí \(C\) je \(n\){% endmath %}

{% math observation %}cyklických pořadí je \((n - 1)!\)
- kvůli tomu, že libovolnou permutaci můžu posunout o \(n\) míst a stále to bude stejný cyklus
{% endmath %}

{% math observation %}pokud \(e = \left\{a_1, \ldots, a_k\right\}\) je vůči \(C\) interval, pak \(\exists \le k - 1\) dalších hran \(e'\) t.ž. jsou intervaly vůči \(C\){% endmath %}

{% math proof %}Může nastat vždy právě jeden z následujících případů, protože z předpokladu je \(E\) pronikající systém množin (a \(e'\) s \(e''\) by byly disjunktní):

{% xopp slunnnn %}

Dvojic je tedy nejvýše \(r - 1\).
{% endmath %}

Důkaz věty bude dvojí počítání \((e, C)\) t.ž. \(e \in E, c\) cyklické pořadí a \(e\) tvoří v \(C\) interval.
1. vezmu \(e\) a chci tvořit cyklické pořadí t.ž. \(e\) tvoří interval: \(e\) zpermutuji \(k!\) způsoby a \(V \setminus e\) zpermutuji \((n - k)!\) způsoby, pro každou hranu, tedy \[\# (e, C) = |E| \cdot k! \cdot (n - k)!\]
2. vezmu \(C\): těch je \((n - 1)!\)
	- podle pozorování je \(e\) tvořících interval nanejvýš \(k\), tedy \[\# (e, C) \le k \cdot (n - 1)!\]

Spojením dostávám \[|E| \le \binom{n - 1}{k - 1}\]
{% endmath %}

### Zdroje/materiály
- [stránky přednášky](https://research.koutecky.name/db/teaching:kg22021_prednaska)
- [poznámky Václava Končického](https://kam.mff.cuni.cz/~koncicky/notes/kag2/pdf) z roku 2019

### Poděkování
- Eldaru Urmanovi za upozornění na několik překlepů/chyb v důkazech a definicích
- Matěji Kripnerovi za důkazy některých tvrzení a opravy překlepů
- Kateřině Sulkové za naprosto nesmyslný nápad přejmenovat Burnsideovo lemma na „Rumcajsovo“
