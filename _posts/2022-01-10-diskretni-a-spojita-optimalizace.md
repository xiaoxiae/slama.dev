---
language: cz
title: Diskrétní a spojitá optimalizace
category: "poznamky z prednasky"
category_noslug: "poznámky z přednášky"
pdf: true
redirect_from:
 - /lecture-notes/diskretni-a-spojita-optimalizace/
 - /poznámky-z-přednášky/diskretni-a-spojita-optimalizace/
---

- .
{:toc}

{:.center}
**Poznámky jsou aktuálně rozpracované, dokončené budou až o zkouškovém.**

{% lecture_notes_preface Martina Loebla a Milana Hladíka|2021/2022%}

TODO: dělení na diskrétní a spojitou část

### Základní definice

{% math definition "matroid" %}je dvojice \((X, \mathcal{S})\), kde \(X\) je konečná množina, \(\mathcal{S} \subseteq 2^X\) splňující
1. \(\emptyset \not \in \mathcal{S}\)
2. **dědičnost**: \((\forall A \in \mathcal{S}) A' \subseteq A \implies A' \in \mathcal{S}\)
3.  **výměnný axiom**: \((\forall U, V \in \mathcal{S}) |U| > |V| \implies (\exists u \in U \setminus V) V \cup \left\{u\right\} \in \mathcal{S}\)
	- \((3'):\) \(A \subseteq X \implies\) všechny maximální (\(\subseteq\)) podmnožiny \(A\) v \(\mathcal{S}\) mají stejnou velikost

Prvkům \(\mathcal{S}\) říkáme **nezávislé množiny**.
{% endmath %}

{% math lemma "stejná definice" %}Axiomy \((1, 2, 3)\) a \((1, 2, 3')\) definují stejný objekt.{% endmath %}

{% math proof %}\((3) \implies (3')\) sporem:

- nechť platí \((3)\) ale existuje \(A \subseteq X\) t. ž. pro nějaké \(U, V \subseteq \mathcal{S}\) platí \(U, V \subseteq A\) a zároveň \(U, V\) maximální je \(|U| > |V|\).
- díky \((3)\) \((\exists u \in U \setminus V)\) t. ž. \(V \cup \left\{u\right\} \in \mathcal{S} \) a navíc \(V \cup \left\{u\right\} \subseteq\), což je spor s maximalitou \(V\).
{% endmath %}

{% math proof %}\((3') \implies (3)\) sporem:
- nechť \(U, V \in \mathcal{S}\) a \(|U| > |V|\) a \(V\) je maximální
- definujme \(A = U \cup V \subseteq X\); pak \(V\) je maximální ale \(|U| > |V|\), což je spor
{% endmath %}

{% math example %}
1. **vektorový matroid**:
	- nechť \(M\) je matice nad tělesem \(\mathbb{F}\) s řádky \(C\)
	- \(\mathcal{V}_M = (C, \mathcal{S})\), kde
		- \(A \in \mathcal{S} \iff A \in C\) a \(A\) je lineárně nezávislé v \(\mathbb{F}\)
		- to, že je to matroid vyplívá ze Steinitzovy věty
2. **grafový matroid**:
	- mějme graf \(G = (V, E)\)
	- \(\mathcal{M}_G = (E, \mathcal{S})\), kde
		- \(A \in \mathcal{S} \iff A \subseteq E \) a \(A\) je acyklická
		- \((1):\) \(\emptyset \in \mathcal{S}\)
		- \((2):\) podmnožina acyklické je rovněž acyklická
		- \((3):\) počítání přes to, kolik hran je v komponentách souvislosti
{% endmath %}

{% math observation %}matroidy jsou _přesně_ **dědičné systémy**, kde lze definovat **řádová funkce**{% endmath %}

{% math definition "řádová funkc " %}mějme systém podmnožin \((\mathcal{Z}, \mathcal{M}), \mathcal{M} \subseteq 2^{\mathcal{Z}}\) a \(A \subseteq \mathcal{Z}\). Pak řádovou funkci \(r: 2^{\mathcal{Z}} \mapsto \mathbb{N}\) definujeme jako **velikost maximální podmnožiny patřící do** \(\mathcal{M}\):

\[r(A) = \max \left\{|X| \mid X \in 2^A \land X \in \mathcal{M}\right\}\]
{% endmath %}

{% math theorem "charakteristika řádové funkce" %}funkce \(r : 2^X \mapsto N\) je řádová funkce nějakého matroidu nad \(X\) \(\iff\) platí:
1. \(r(\emptyset) = 0\)
2. \(r(Y) \le r(Y \cup \left\{y\right\}) \le r(Y) + 1\)
3. \(r(Y \cup \left\{y\right\}) = r(Y \cup \left\{z\right\}) = r(Y) \implies r(Y) = r(Y \cup \left\{y ,z\right\})\)
{% endmath %}

{% math proof %} \(\implies\):

1. max. nezávislá podmnožina \(\emptyset\) je \(\emptyset\) a \(|\emptyset| = \emptyset\)
2. z definice řádové funkce a dědičnosti matroidu
3. TODO
{% endmath %}

#### Grafová odbočka

{% math algorithm "hladový" %}je-li dán souvislý graf \(G = (V, E)\) a váhová funkce \(w : E \mapsto \mathbb{Q}^+\), pak **MST** (minimum spanning tree) lze najít hladovým algoritmem (bereme vždy nejlehčí kterou můžeme přidat) v polynomiálním čase.{% endmath %}

{% math definition "sudá podmnožina hran" %} podmnožina hran \(E' \subseteq E\) je sudá, právě když \(H = (V, E')\) má pouze sudé stupně.{% endmath %}

{% math definition: "matice incidence" %} grafu \(G = (V, E)\) je matice \(I_G \in \mathbb{F}_2^{|V| \times |E|}\) t.ž. \[\left(I_G\right)_{v,e}=\begin{cases} 1 & v \in e \\ 0 & \text{jinak} \end{cases}\]{% endmath %}

---
![](/assets/diskretni-a-spojita-optimalizace/incidence-matrix.svg)

---

{% math definition "jádro matice incidence" %}pro matici incidence \(I_G\) definujeme jádro jako
\[\mathrm{Ker}_{\mathbb{F}_2} I_G = \left\{\mathbf{x} \in \mathbb{F}_2^{|E|} \mid I_G \mathbf{x} = \mathbf{0}\right\}\]
{% endmath %}

{% math definition "charakteristický vektor" %}mějme nosnou množinu \(X\) a podmnožinu \(A \subseteq X\). Charakteristický vektor \(A\) je \(\mathcal{X}_A \in \left\{0, 1\right\}^{|X|}\) t.ž. \[\left(\mathcal{X}_A\right)_{k} = \begin{cases} 1 & k \in A \\ 0 & k \not\in A \end{cases}\]{% endmath %}

{% math observation %}řádek matice incidence \(I_G\) indexovaný vrcholem \(w\) je roven \(\mathcal{X}_{\underbrace{|N(w)|}_{\text{okolí}}}\){% endmath %}

{% math observation "prostor cyklů" %}jádro matice můžeme ekvivalentně vyjádřit jako \[\mathrm{Ker}_{\mathbb{F}_2} I_G = \left\{x \in \mathbb{F}_2^{|E|} \mid x = \mathcal{X}_{E'}\ \text{pro}\ E'\ \text{sudou}\right\}\]{% endmath %}
Tuto množinu rovněž nazýváme **prostor cyklů.**

TODO: hodně přednášek

### Perfektní párování
{% math definition "párování" %}\(G = (V, E)\) graf; \(M \subseteq E\) párovaní, jestliže \(e, e' \in M \implies e=e'\) nebo \(e \cap e' = \emptyset\).{% endmath %}

{% math definition: "maximální párování" %} pokud \(|M|\) je maximální (co do velikosti).{% endmath %}

{% math observation %}neplatí, že maximální do velikosti je maximální do inkluze (můžeme si hrany vybrat špatně){% endmath %}

{% math definition "perfektní párování" %}pokud \(|M| = |V| / 2\){% endmath %}

{% math definition "pokrytí" %}vrchol je \(M\)-pokrytý, pokud je v nějaké hraně z párování, jinak je \(M\)-nepokrytý.{% endmath %}

{% math definition: "defekt" %} \(\mathrm{def}(M)\) je počet \(M\)-nepokrytých vrcholů{% endmath %}

{% math definition "alternující cesta" %}podgraf, který je cesta
- je **zlepšující**, pokud má krajní vrcholy \(M\)-nepokryté
{% endmath %}

{% math theorem %}graf \(G = (V, E)\), \(M\) párování. Pak \(M\) je maximální \(\iff\) \(G\) nemá zlepšující cestu.{% endmath %}

{% math proof %}
- \(\Leftarrow\) pokud má zlepšující cestu, tak párování můžeme zlepšit a není tedy maximální
- \(\Rightarrow\) pokud \(G\) není maximální tak existuje párování \(M'\) t. ž. \(M' > |M|\)
	- uvažme graf \(M \Delta M'\) -- stupně mají vrcholy nejvýše dva, komponenty jsou tedy buď alternující cykly nebo cesty
	- díky tomu, že nám jedna hrana přebývá, tak alespoň jedna komponenta je cesta
{% endmath %}

{% math observation %} \(G = (V, E), A \subseteq V\). Pak v libovolném párování musí být liché komponenty \(G \setminus A\) pokryté pouze z \(A\) a tedy
\[\mathrm{def}(M) \ge \mathrm{lc}(G \setminus A) - |A|\]
Kde \(\mathrm{lc}\) značí počet lichých komponent grafu.
{% endmath %}

{% math observation %} \(g = (V, E)\). Pak max. velikost párování \[\le \min_{A \subseteq V} \frac{1}{2} \left(|V| - \mathrm{lc}(G \setminus A) + |A|\right)\]{% endmath %}

{% math theorem "Tutte-Berge" %}Pro výše uvedené pozorování \(\max = \min\){% endmath %}

{% math proof %} stačí najít párování \(M\) t.ž. platí rovnost.

Najdeme algoritmem (Edmonds), který najde maximální párování

- postupně zvětšujeme párovaní \(M\):

1. \(M\) perfektní \(\implies\) je maximální a věta platí (\(A = \emptyset\))
2. \(M\) má \(M\)-nepokrytý vrchol \(r\): budujeme alternující strom \(T\) tím, že sřídavě přidáváme hrany:
	- \(B\)-vrcholy: vrcholy v sudé vzdálenosti od \(r\)
	- \(A\)-vrcholy: vrcholy v liché vzdálenosti od \(r\)
	- zastavíme se, když:
		- existuje \(w \not\in T, \{v, w\} \in E\) a \(w\) je nepokrytý -- pak jsme našli alternující cestu
		- neexistuje \(w\)
			1. všechny zbývající hrany z \(B\)-vrcholů vedou do \(A\)-vrcholů -- poté když uvážíme \(G \setminus A\), tak liché komponenty vedou pouze do \(A\) vrcholů ale \(B\) je o jedna více (máme \(r\)), tedy \(|B| = |A| + 1\) a \(G\) nemá perfektní párování a **našli jsme defektní vrchol**
			2. pokud je graf bipartitní, tak nemáme žádné \(B-B\) hrany

TODO: obrázek?

Pro **bipartitní grafy** můžeme algoritmus výše opakovat (opakovaně stavíme stromy z vrcholů, které nejsou v párování), najít všechny defektní vrcholy a věta výše platí (máme množinu defektních vrcholů a párování splňující rovnost).

Pro **nebipartitní grafy** může existovat hrana mezi \(B-B\) vrcholy (lichá kružnice).

{% math observation %}\(C\) lichá kružnice v \(G\), \(G'\) vznikne kontrakcí \(C\) do jednoho (pseudo)vrcholu, \(M'\) je párování v \(G'\). Potom existuje párování \(M\) v \(G\), že počet \(M'\)-nepokrytých vrcholů je stejný jako počet \(M\)-nepokrytých.
{% endmath %}

TODO: obrázek

Podgrafy \(G\) reprezentované pseudovycholy mají lichý počet vrcholů (chceme opět dostat \(M\) a \(A\), abychom větu dokázali). To platí, protože pseudovrcholy vzinkly kontrakcí liché kružnice na vrchol a tedy přišly o sudý počet vrcholů.

Postup pro \(B-B\) hrany je tedy ten, že zkontrahujeme \(C\), rekurzivně vyřešíme párování a odkontrahujeme.
{% endmath %}

{% math consequence "Tutte [47]" %}\(G\) má perfektní párování \(\iff \forall A \subset V: \mathrm{lc}(G \setminus A) \le |A|\){% endmath %}

{% math theorem "Edmonds-Gallai dekompozice" %}\(G\) graf, \(G = (V, E)\), \(B \subseteq V\) vrcholů nepokrytých nějakým maximálním párovaním. Nechť \(A \subseteq V \setminus B\) sousedé vrcholů z \(B\), \(C = V \setminus \left(B \cup A\right)\). Pak
1. každá komponenta \(G \setminus \left(A \cup C\right)\) je kritická (\(\forall v \in K: K \setminus \left\{v\right\}\) má PP)
	- \(G\) kritický \(\iff\) \(G\) lze zkonstruovat z liché kružnice lepením lichých uší
2. každé maximální párování \(M\) splňuje:
	- \(e \in M, e \cap A \neq \emptyset \implies |e \cap A| = 1\) a \(e\) vede do \(B\)
		- tohle nezamezuje, že by dvě hrany z \(A\) nevedly do jedné z \(B\)
	- do každé komponenty \(B\) vede \(\le 1\) hrana \(M\)

{% xopp dekompozice %}
{% endmath %}

{% math proof %}Uvažme poslední alternující les v Edmondsově algoritmu.

{% xopp strom %}

Každá hrana s koncem v \(A\) vede do \(B\) (s tím, že vrcholy v \(B\) jsou (pseudo)vrcholy vzniklé operací kontrakce. Defekt \(\mathrm{def}(M)\) je počet komponent v tomto lese.

Nepokryté vrcholy žádným maximálním párováním:
- ne v \(A\), jelikož všechny musí být pokryté každým maximálním párováním
- ne mimo \(A \cup B\), protože tam je PP

Takové vrcholy tedy mohou být pouze v \(B\), čímž jsme dokázali (1).

Část (2) rovněž plyne z Edmondsova algoritmu.
{% endmath %}

### ?

Nechť \(G = (V, E)\) rovinný, \(w : E \mapsto \mathbb{Q}\)
1. **maximální PP** -- najdi \(M\) PP t.ž. \(w(E)\) je maximální
	- polynomiální (pro všechny grafy)
2. **maximální hranový řez** -- najdi \(E'\) hranový řez t.ž. \(w(E')\) je maximální
	- obecně je NP-těžný, pro grafy na 2D plochách polynomiální

{% math definition "determinant" %}nechť \(A\) je reálná matice. Pak determinant je \[\mathrm{Det}(A) = \sum_{\pi} (-1)^{\mathrm{sign}(\pi)} \overbrace{\prod_{i = 1}^{n} A_{i, \pi(i)}}^{\text{transverzála}}\]
- polynomiální, jde řešit přes Gaussovu eliminaci
{% endmath %}

{% math definition "permanent" %}nechť \(A\) je reálná matice. Pak permanent je \[\mathrm{Per}(A) = \sum_{\pi} \prod_{i=1}^{n} A_{i, \pi(i)}\]
- \(\#P\)-complete (alespoň tak těžký jako \(NP\)-úplný), neumíme nic lepšího
{% endmath %}

{% math example %}\(G = (V_1, V_2, E\) bipartitní graf, \(A^{|V_1| \times |V_2|}\) \(0-1\) matice podle toho, jaké obsahuje hrany. Pak \(\mathrm{Per}(A)\) je počet perfektních párování \(G\).{% endmath %}

#### Generující funkce, které se hodí

\[\mathcal{P}(G, x, w) = \sum_{P\ \text{perf. pár.}} x^{w(P)}\]
\[\mathcal{E}(G, x, w) = \sum_{E'\ \text{sudá}} x^{w(E')}\]
\[\varphi(G, x, w) = \sum_{C\ \text{hranový řez}} x^{w(C)}\]

{% math theorem %}\(G\) rovinný. Pak \[\varphi(G) \equiv \mathcal{E}(G^*) \equiv \mathcal{P}(G_\Delta^*)\]
kde symbolem \(\equiv\) rozumíme vzhledem k vypočítatelnosti a \(G_\Delta\) následující operaci:

{% xopp delta %}

Rovněž předpokládáme \(w(e) \in \mathbb{Z}, |w(e)| \le |V(G)|^{c} \) pro \(c\) konstantu.
{% endmath %}

{% math theorem "Kasteleyn" %}Když \(G\) rovinný, pak \(\mathcal{P}(G, x, w)\) lze spočítat v polynomiálním čase.
{% endmath %}

{% math consequence %}
- umíme spočítat jak maximální párování, tak jejich počet (a počet všech ostatních párování s danými vahami)
- max. řez, max. perf. párování jsou pro rovinné grafy polynomiální
{% endmath %}

{% math proof "naznačení" %} pro \(D\) orientaci \(G\), \(M_0\) fixní PP definujeme „determinantní verzi“ \(\mathcal{P}\) následně: \[\mathcal{P(G, D, M_0, x, w)} = \sum_{P\ \text{perf. pár.}} \mathrm{sign}(D, M_0, P) x^{w(P)}\]
kde \[\mathrm{sign}(D, M_0, P) = (-1)^{\#\ \text{$D$-sudých cyklů $M_0\ \Delta\ P$}}\]
- \(D\)-sudý je, když v \(D\) má sudý počet hran orientovaných jedním směrem; nezáleží na tom, jakou stranou jdeme, jelikož symetrická diference perfektních párování tvoří jen sudé cykly

Postup důkazu:
- \(\mathcal{P}(G, D, M_0, x, w)\) lze pro obecné grafy spočítat variantou Gaussovské eliminace (Pfaffion)
- Existuje orientace \(D^K\), že všechna znaménka \(\mathrm{sign}(D^K, M_0, P)\) jsou stejná, tedy \[\mathcal{P}(G, D^K, M_0, *, w) = \pm \mathcal{P}(G, x, w)\]
- Tuhle \(D^K\) lze zkonstruovat v polynomiálním čase.
{% endmath %}

{% math reminder %}pro další plochy je to trochu komplikovanější, ale jde to dělat podobně.{% endmath %}

### Pošťáci a cestující
{% math definition %} \(G = (V, E)\) graf silniční sítě, \(l : E \mapsto \mathbb{Q}^+\):
- problém **čínského pošťáka:** najdi trasu minimální délky, která projde všechny _hrany_ a vrátí se do výchozího vrcholu (eulerovský tah)
	- polynomiální
- problém **obchodního cestujícího:** najdi trasu minimální délky, která projde všechny _vrcholy_ a vrátí se do výchozího vrcholu (hamiltonovskou kružnici)
	- NP-úplný
{% endmath %}

{% math problem "čínského pošťáka" %}
1. \(G = (V, E)\) má **všechny stupně sudé** \( \implies \) řešení je uzavřený eulerovský tah
	- {% math observation %}když \(H = (W, F)\) má všechny stupně sudé a \(F \neq \emptyset\) je neprázdná, pak \(F\) má cyklus; odstraněním cyklu má opět všechny stupně sudé; opakováním dostaneme disjunktní sjednocení cyklů, což jde do eulerovského tahu udělat trivialně{% endmath %}
2. nechť \(T = \left\{v \mid \mathrm{deg}_G(v)\ \text{lichý}\right\}\)

{% math observation %}\(|T|\) je sudé (počet vrcholů lichého stupně je sudý){% endmath %}
{% math definition %}\(E' \subseteq E\) je \(T\)-join, jestli graf \(G_T = (V, E')\) splňuje \[\left(\forall v \in V\right) \left(\mathrm{deg}_{G_T} (v)\ \text{lichý} \iff v \in T\right)\]{% endmath %}

{% math theorem %}nechť \(E' \subseteq E\) je množina hran min. trasy čínského pošťáka, které se projdou více než jednou. Pak
1. se projdou \(2\)-krát
2. \(E'\) je min. \(T\)-join (kde \(T\) je výše definovaná množina){% endmath %}
{% endmath %}

{% math proof %}
{% math observation %}nechť \(G'\) vznikne z \(G\) dodáním násobných hran, násobnost je podle počtu procházení minimální trasou \(P\). Potom \(G'\) má všechny stupně sudé.{% endmath %}
- \(F = E(G') - E(G)\) jsou dodané hrany
- \(F\) nemá násobné hrany, protože pak bychom je mohli (po dvou) vynechat

Z pozorování plyne (1), jelikož \(F\) spolu s původními hranami dává \(2\) průchody.

Navíc jelikož \(E(G') = E(G) \cup F\) je \(T\)-join, jelikož přesné splňuje definici (stupně budou liché v \(G'\), protože musí být sudé po přidaní do \(G\)). Navíc \(E(G) \cup \overline{F}\) rozhodně nebude lepší než minimální cesta čínského pošťáka a tedy naše \(F\).
{% endmath %}

{% math algorithm "čínský pošťák" %}
1. najdi minimální \(T\)-join
	- použij konstrukci (modifikovanou) Fischera z minulé přednášky (\(G \mapsto G_\Delta\)), o čemž víme, že je polynomiální
	- _(alternativně)_ uvažme pomocný graf \(H = \left(T, \binom{T}{2}\right)\) a váha \(w : \binom{T}{2} \mapsto \mathbb{Q}^+\), kde \(w(\left\{u, v\right\}) = \) délka nejkratší cesty mezi \(u, v\) v \(G\)
		- nechť \(M\) je min. PP v \(H\)
		- nechť \(F = \bigcup_{e \in M} P_e\), kde \(P_e\) je nejkratší cesta v \(G\) spojující vrcholy \(e\)
2. přidej zbylé hrany
3. profit?
{% endmath %}

{% math problem "obchodního cestujícího" %} předpokládáme
- \(G = K_n\) (pro neexistující hrany nastavíme váhu na nekonečno)
- nezáporné délky
- trojúhelníková nerovnost \(\left(\forall u, v, w \in V\right) l(u, v) + l(v, w) \ge l(u, w)\)
{% endmath %}

#### Christofidesova heuristika
- viz moje [poznámky z aproximačních algoritmů](https://slama.dev/poznamky-z-prednasky/aproximacni-algoritmy#christofides%C5%AFv-algoritmus)

### Poděkování
- Davidu Kubkovi za zápisky, ze kterých jsem čast z poznámek vytvářel
