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

{% lecture_notes_preface Martina Loebla a Milana Hladíka|2021/2022%}

### Diskrétní optimalizace

#### Matroidy

{:.rightFloatBox}
<div markdown="1">
Při definici matroidu je dobré si predstavit graf -- \(\mathcal{X}\) je tu množina hran a \(S\) všechny acyklické podgrafy.
</div>

{% math definition "matroid" %}je dvojice \((X, \mathcal{S})\), kde \(X\) je konečná množina, \(\mathcal{S} \subseteq 2^X\) splňující
1. \(\emptyset \in \mathcal{S}\)
2. **dědičnost**: \((\forall A \in \mathcal{S}) A' \subseteq A \implies A' \in \mathcal{S}\)
3.  **výměnný axiom**: \((\forall U, V \in \mathcal{S})\ |U| > |V| \implies (\exists u \in U \setminus V) V \cup \left\{u\right\} \in \mathcal{S}\)
	- \((3'):\) \(A \subseteq X \implies\) všechny maximální (\(\subseteq\)) podmnožiny \(A\) v \(\mathcal{S}\) mají stejnou velikost

- prvkům \(\mathcal{S}\) říkáme **nezávislé množiny**
- největším nezávislým množinám (do inkluze) říkáme **báze**

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
		- to, že je to matroid vyplývá ze Steinitzovy věty
2. **grafový matroid**:
	- mějme graf \(G = (V, E)\)
	- \(\mathcal{M}_G = (E, \mathcal{S})\), kde
		- \(A \in \mathcal{S} \iff A \subseteq E \) a \(A\) je acyklická
		- \((1):\) \(\emptyset \in \mathcal{S}\)
		- \((2):\) podmnožina acyklické je rovněž acyklická
		- \((3):\) počítání přes to, kolik hran je v komponentách souvislosti
{% endmath %}

##### Řádové funkce

{:.rightFloatBox}
<div markdown="1">
V řeči grafů chceme pro libovolnou množinu hran (prvků podmnožin) vrátit největší acyklický podgraf (prvek matroidu).
</div>

{% math definition "řádová funkce" %}mějme systém podmnožin \((X, \mathcal{S}), \mathcal{S} \subseteq 2^{X}\) a \(A \subseteq X\). Pak řádovou funkci \(r: 2^{X} \mapsto \mathbb{N}\) definujeme jako **velikost maximální podmnožiny patřící do** \(\mathcal{S}\):

\[r(A) = \max \left\{|X| \mid X \in 2^A \land X \in \mathcal{S}\right\}\]
{% endmath %}

{% math theorem "charakteristika řádové funkce" %}funkce \(r : 2^X \mapsto N\) je řádová funkce nějakého matroidu nad \(X\) právě tehdy, když platí:
- \((\mathrm{R1})\): \(r(\emptyset) = 0\)
- \((\mathrm{R2})\): \(r(Y) \le r(Y \cup \left\{y\right\}) \le r(Y) + 1\)
- \((\mathrm{R3})\): \(r(Y \cup \left\{y\right\}) = r(Y \cup \left\{z\right\}) = r(Y) \implies r(Y) = r(Y \cup \left\{y ,z\right\})\)
{% endmath %}

{% math proof "\(\Rightarrow\)" %} ukážeme přímo:

- \((\mathrm{R1})\): max. nezávislá podmnožina \(\emptyset\) je \(\emptyset\) a \(|\emptyset| = \emptyset\)
- \((\mathrm{R2})\): z definice řádové funkce a dědičnosti matroidu
- \((\mathrm{R3})\): TODO
{% endmath %}

{% math proof "\(\Leftarrow\)" %} 
konstruujeme matroid s řádovou funkcí \(r\).
Definujme \[X, \mathcal{S}\quad\text{t.ž.}\quad A \in \mathcal{S} \iff |A| = r(A)\]

Ukážeme, že \(\left(X, \mathcal{S}\right)\) je matroid:
1. \(\emptyset \in \mathcal{S}\) (triviálně)
2. pro spor předpokládejme, že dědičnost neplatí
	- existuje tedy \(A \in \mathcal{S}, B \subseteq A\) t.ž. \(B \not\in \mathcal{S}\) ale \(|B| > r(B)\)
\[\begin{aligned}
	r(A) &\le r(B) + |A \setminus B| & \quad \text{R2} \\
	&< |B| + |A \setminus B| \\
	&= |A| \implies A \not\in \mathcal{S} & ↯ \\
\end{aligned}\]
1. pro spor předpokládejme, že \(\exists U, V \in \mathcal{S}\) t.ž. \(|U| > |V|\) ale \(\forall x \in U \setminus V: V \cup \left\{x\right\} \not\in \mathcal{S}\)
	- přes \(\mathrm{R3}\) získáváme \((\forall x, y \in U \setminus V)\):
\[\begin{aligned}
r(V) &= r(V \cup \left\{x\right\}) = r(V \cup \left\{y\right\}) \\
&\Rightarrow r(V \cup \left\{x, y\right\}) & \mathrm{R3}\\
&\Rightarrow r(V \cup (U \setminus V)) \\
\end{aligned}\]

Tedy
\[|V| = r(V) = r(\underbrace{V \cup (U \setminus V)}_{U \cup V}) \overset{\mathrm{R2}}{\ge} r(U) = |U| ↯\]
{% endmath %}

{% math theorem "řádová funkce a submodularita" %} \(r : 2^X \mapsto \mathbb{N}\) je řádová funkce \(\iff\)
- \((\mathrm{R1'}): \forall Y \in X: 0 \le r(Y) \le |Y|\)
- \((\mathrm{R2'}\ \text{-- monotonie}): Z \subseteq Y \subseteq X \implies R(Z) \le R(Y)\)
- \((\mathrm{R3'}\ \text{-- submodularita}): r(Y \cup Z) + r(Y \cap Z) \le r(Y) + r(Z)\)
{% endmath %}

{% math proof %}TODO{% endmath %}

{% math observation %}matroidy jsou systémy podmnožiny, kde řádová funkce je **monotonní** a **submodulární**.{% endmath %}

{% math definition "marginální hodnota" %}
Mějme množinu \(X\) a funkce \(f: 2^X \mapsto \mathbb{N} \). Pak \(\forall x \in X\) definujeme \(\Delta f_x : 2^X \mapsto \mathbb{Z}\) tak, že
\[T \subseteq X \implies \Delta f_x (T) = f(T \cup \left\{x\right\}) f(T)\]
- funkce určuje, „jak si cením přidání \(x\), když už mám \(T\)“
{% endmath %}

{% math theorem "marginální hodnota a submodularita" %} \(f: 2^X \mapsto \mathbb{N}\) je submodulární \(\iff \forall x \in X: \Delta f_x\) je nerostoucí
- nerostoucí myslíme následně: \(T' \subseteq T, x \not\in T \implies \Delta f_x(T') \ge \Delta f_x(T)\)
	- dává to smysl -- při odebrání věci nechceme, aby ohodnocení stoupalo
{% endmath %}

{% math proof %}TODO{% endmath %}

##### Grafy a matroidy

{% math algorithm "hladový" %}je-li dán souvislý graf \(G = (V, E)\) a váhová funkce \(w : E \mapsto \mathbb{Q}^+\), pak **MST** (minimum spanning tree) lze najít hladovým algoritmem (bereme vždy nejlehčí kterou můžeme přidat) v polynomiálním čase.{% endmath %}

{% math definition "sudá podmnožina hran" %} podmnožina hran \(E' \subseteq E\) je sudá, právě když \(H = (V, E')\) má pouze sudé stupně.{% endmath %}

{% math definition: "matice incidence" %} grafu \(G = (V, E)\) je matice \(I_G \in \mathbb{F}_2^{|V| \times |E|}\) t.ž. \[\left(I_G\right)_{v,e}=\begin{cases} 1 & v \in e \\ 0 & \text{jinak} \end{cases}\]{% endmath %}

![](/assets/diskretni-a-spojita-optimalizace/incidence-matrix.svg)

{% math definition "jádro matice incidence" %}pro matici incidence \(I_G\) definujeme jádro jako
\[\mathrm{Ker}_{\mathbb{F}_2} I_G = \left\{\mathbf{x} \in \mathbb{F}_2^{|E|} \mid I_G \mathbf{x} = \mathbf{0}\right\}\]
{% endmath %}

{% math definition "charakteristický vektor" %}mějme nosnou množinu \(X\) a podmnožinu \(A \subseteq X\). Charakteristický vektor \(A\) je \(\mathcal{X}_A \in \left\{0, 1\right\}^{|X|}\) t.ž. \[\left(\mathcal{X}_A\right)_{k} = \begin{cases} 1 & k \in A \\ 0 & k \not\in A \end{cases}\]{% endmath %}

{% math observation %}řádek matice incidence \(I_G\) indexovaný vrcholem \(w\) je roven \(\mathcal{X}_{\underbrace{|N(w)|}_{\text{okolí}}}\){% endmath %}

{% math observation "prostor cyklů" %}jádro matice můžeme ekvivalentně vyjádřit jako \[\mathrm{Ker}_{\mathbb{F}_2} I_G = \left\{x \in \mathbb{F}_2^{|E|} \mid x = \mathcal{X}_{E'}\ \text{pro}\ E'\ \text{sudou}\right\}\]{% endmath %}
Tuto množinu rovněž nazýváme **prostor cyklů.**

##### Hladový algoritmus

{% math definition "úloha kombinatorické optimalizace" %}je dán možinový systém \((X, \mathcal{S})\) a váhová funkce \(w : X \mapsto \mathbb{Q}\). **Úloha kombinatorické optimalizace** je najít \(A \in \mathcal{S}\) t.ž. \[w(A) = \sum_{v \in A} w(v) = w^T \chi_A\] je minimální. \(\chi_A\) je charakteristický vektor \(A\), který je \(1\) pro \(v \in A\) a \(0\) jindy.{% endmath %}

{% math example %}
1. maximální párování v \(G\)
2. minimální Hamiltonovská kružnice
3. minimální hranový řez
{% endmath %}

{% math algorithm "hladový" %} nechť že \(w_1 \ge \ldots \ge w_n\) a \(m = \max \left\{i \in X \mid w_i \ge 0\right\}\); pak:
1. nastav \(J = \emptyset\)
2. pro \(i = \left\{1, \ldots, n\right\}\)
	- je-li \(J \cup \left\{i\right\} \in \mathcal{S}\), pak \(i\) přidej do \(J\)
3. vrať \(J\)
{% endmath %}

{% math observation %}pro výše uvedené příklady nemusí algoritmus vrátit optimální řešení.{% endmath %}

{% math theorem "hladový algoritmus na matroidech" %}nechť \((X, \mathcal{S})\) je dědičný množinový systém a \(\emptyset \in \mathcal{S}\). Pak hladový algoritmus vyřeší správně úlohu kombinatorické optimalizace pro **každou funkci** \(w \iff (X, \mathcal{S})\) je matroid.{% endmath %}

{% math proof %}TODO{% endmath %}

##### Operace na matroidech

{:.rightFloatBox}
<div markdown="1">
Mazání hran v grafu.
</div>

**Mazání** -- pro matroid \(\mathcal{M} = (X, \mathcal{S})\) a \(Y \subseteq X\):
\[\mathcal{M} - Y = (X - Y, \left\{A - Y \mid A \in \mathcal{S}\right\})\]
je opět matroid.

**Součet** -- pro matroidy \(\mathcal{M_1} = (X_1, \mathcal{S}_1), \mathcal{M_2} = (X_2, \mathcal{S}_2), X_1 \cap X_2 = \emptyset\)
\[\mathcal{M}_1 + \mathcal{M}_2 = (X = X_1 \cup X_2, \left\{A \in X \mid A \cap X_1 \in \mathcal{S}_1 \land A \cap X_2 \in \mathcal{S}_2\right\})\]

{:.rightFloatBox}
<div markdown="1">
Příklad je matroid bipartitního grafu, který vznikne součtem obou stran.
</div>

**Partition matroid** -- nechť \(X_1, \ldots, X_n\) jsou disjunktní množiny a \(\mathcal{S}_i = \left\{A \subseteq X_i \mid |A| \le 1\right\}\). Pak \(\sum_{i} (X_i, \mathcal{S}_i)\) je partiční matroid.

{:.rightFloatBox}
<div markdown="1">
Podobně jako mazání, ale chová se dost jinak (viz kontrakce/mazání hran v grafu). Na mostech se ale chová stejně.
</div>

**Kontrakce** -- nechť \(\mathcal{M} = (X, \mathcal{S})\) je matroid, \(A \subseteq X\) a \(J \in \mathcal{S}\) je max. nezávislá množina v \(A\). Pak
\[\mathcal{M} \setminus A = \left((X - A), \left\{Z \subseteq X \mid Z \cup J \in \mathcal{S} \right\}\right)\]

{% math theorem "kontrakce matroidu je matroid" %} nechť \(\mathcal{M} = (X, \mathcal{S})\) je matroid a \(A \subseteq X\). Pak \(M \setminus A\) je matroid s řádovou funkcí
\[Z \subseteq X \setminus A \implies r'(Z) = r(Z \cup A) - r(A)\]
{% endmath %}

{% math proof %}TODO{% endmath %}

{% math theorem "Edmondsova MiniMaxová" %}nechť \(\mathcal{M}_1 = \left(X, \mathcal{S}_1\right)\) a \(\mathcal{M_2} = \left(X_2, \mathcal{S_2}\right)\) jsou matroidy. Pak
\[\max \left\{|Y| \mid Y \in \mathcal{S_1} \cap \mathcal{S}_2\right\} = \min_{A \subseteq X} r_1(A) + r_2(X - A)\]
{% endmath %}

{% math proof %}TODO{% endmath %}

{% math theorem "sjednocení matroidů je matroid)" %} sjednocení matroidů (i pro nedisjunktní \(X_i\)) je matroid s řádovou funkcí \[r(U) = \min_{T \subseteq TODO} \left\{|U - T| + r_1(T \cap X_1) + \ldots + r_k(T \cap X_k)\right\}\]
{% endmath %}

##### Dualita matroidu


{:.rightFloatBox}
<div markdown="1">
Tady pozor na to, že definujeme báze a né nezávislé množiny (divil jsem se, jak může duál obsahovat \(\emptyset\)).
</div>

{% math definition "duální matroid" %}nechť \(\mathcal{M} = \left(X, \mathcal{S}\right)\) je matroid. Definujeme duální matroid jako \(\mathcal{M}^* = (X, \mathcal{S}^*)\) t.ž. \(B^*\) je báze \(\mathcal{M}^* \iff (X - B^*)\) je báze \(\mathcal{M}\).
{% endmath %}

{% math theorem "duální matroid je matroid" %}nechť \(\mathcal{M}\) je matroid. Pak \(\mathcal{M}^*\) je také matroid a navíc platí \[r^*(A) = |A| - r(X) + r(X - A)\]
{% endmath %}

{% math proof %} stačí dokázat \(3'\), jelikož \(1\) a \(2\) platí triviálně z toho, že jsme definovali pouze báze.

TODO: zbytek...
{% endmath %}

{% math definition "Cobáze, conezávislost" %}nechť \(\mathcal{M}\) je matroid a \(\mathcal{M}^*\) jeho duální matroid. Pak \(Y \subseteq X\) je
- **cobáze**, pokud je báze v \(M^*\)
- **conezávislá**, pokud je nezávislá v \(M^*\){% endmath %}

![](/assets/diskretni-a-spojita-optimalizace/baze-dualita.svg)

{:.rightFloatBox}
<div markdown="1">
U grafů jsou to opravdu kružnice.
</div>

{% math definition "kružnice" %}nechť \(\mathcal{M}\) je matroid. Pak \(Y \subseteq X\) je kružnice, je-li minimální (\(\subseteq\)) **závislá** množina.{% endmath %}

{% math theorem %}\(Y \subseteq X\) je cokružnice (kružnice v duálu) \(\iff Y\) je min (\(\subseteq\)) protínající **každou bázi**.{% endmath %}


{% math proof %}
![](/assets/diskretni-a-spojita-optimalizace/baze-dukaz.svg)
{% endmath %}

{% math consequence %}nechť \(G\) graf souvislý. Pak cokružnice \(\mathcal{M}_G\) jsou přesně **minimální hranové řezy**. {% endmath %}

#### Perfektní párování
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
	- uvažme graf \(M \Delta M'\) -- stupně mají vrcholy nejvýše dva, komponenty jsou tedy buď alternující cykly nebo cesty -- díky tomu, že nám jedna hrana přebývá, tak alespoň jedna komponenta je cesta
{% endmath %}

{% math observation %} \(G = (V, E), A \subseteq V\). Pak v libovolném párování \(M\) musí být liché komponenty \(G \setminus A\) pokryté pouze z \(A\) a tedy
\[\mathrm{def}(M) \ge \mathrm{lc}(G \setminus A) - |A|\]
Kde \(\mathrm{lc}\) značí počet lichých komponent grafu.
{% endmath %}

{% math observation %} \(g = (V, E)\). Pak \[\max_{M} |\text{párování}\ M| = \min_{M} \frac{1}{2} \left(|V| - \mathrm{def}(M)\right) \le \min_{A \subseteq V} \frac{1}{2} \left(|V| - \mathrm{lc}(G \setminus A) + |A|\right)\]{% endmath %}

{% math theorem "Tutte-Berge" %}Pro výše uvedené pozorování platí rovnost.{% endmath %}

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
1. každá komponenta \(G \setminus \left(A \cup C\right)\) je kritická (\(\forall v \in K: K \setminus \left\{v\right\}\) má perfektní párování)
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
- ne mimo \(A \cup B\), protože tam je perfektní párování

Takové vrcholy tedy mohou být pouze v \(B\), čímž jsme dokázali (1).

Část (2) rovněž plyne z Edmondsova algoritmu.
{% endmath %}

#### Generující funkce magic

Nechť \(G = (V, E)\) rovinný, \(w : E \mapsto \mathbb{Q}\) váhová funkce
1. **maximální perfektní párování** -- najdi \(M\) perfektní párování t.ž. \(w(E)\) je maximální
	- polynomiální (pro všechny grafy)
2. **maximální hranový řez** -- najdi \(E'\) hranový řez t.ž. \(w(E')\) je maximální
	- obecně je NP-těžný, pro grafy na 2D plochách polynomiální

{% math definition "determinant" %}nechť \(A\) je reálná matice. Pak determinant je \[\mathrm{Det}(A) = \sum_{\pi} (-1)^{\mathrm{sign}(\pi)} \overbrace{\prod_{i = 1}^{n} A_{i, \pi(i)}}^{\text{transverzála}}\]
- polynomiální, jde řešit přes Gaussovu eliminaci
{% endmath %}

{% math definition "permanent" %}nechť \(A\) je reálná matice. Pak permanent je \[\mathrm{Per}(A) = \sum_{\pi} \prod_{i=1}^{n} A_{i, \pi(i)}\]
- \(\#P\)-complete (alespoň tak těžký jako \(NP\)-úplný), neumíme nic lepšího
{% endmath %}

{% math example %}\(G = (V_1, V_2, E)\) bipartitní graf, \(A^{|V_1| \times |V_2|}\) \(0/1\) matice podle toho, jaké obsahuje hrany. Pak \(\mathrm{Per}(A)\) je počet perfektních párování \(G\).{% endmath %}

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

{% math proof "naznačení" %} pro \(D\) orientaci \(G\), \(M_0\) fixní perfektní párování definujeme „determinantní verzi“ \(\mathcal{P}\) následně: \[\mathcal{P(G, D, M_0, x, w)} = \sum_{P\ \text{perf. pár.}} \mathrm{sign}(D, M_0, P) x^{w(P)}\]
kde \[\mathrm{sign}(D, M_0, P) = (-1)^{\#\ \text{$D$-sudých cyklů $M_0\ \Delta\ P$}}\]
- \(D\)-sudý je, když v \(D\) má sudý počet hran orientovaných jedním směrem; nezáleží na tom, jakou stranou jdeme, jelikož symetrická diference perfektních párování tvoří jen sudé cykly

Postup důkazu:
- \(\mathcal{P}(G, D, M_0, x, w)\) lze pro obecné grafy spočítat variantou Gaussovské eliminace (Pfaffaon)
- Existuje orientace \(D^K\), že všechna znaménka \(\mathrm{sign}(D^K, M_0, P)\) jsou stejná, tedy \[\mathcal{P}(G, D^K, M_0, *, w) = \pm \mathcal{P}(G, x, w)\]
- Tuhle \(D^K\) lze zkonstruovat v polynomiálním čase.
{% endmath %}

{% math reminder %}pro další plochy je to trochu komplikovanější, ale jde to dělat podobně.{% endmath %}

#### Pošťáci a cestující
{% math definition %} \(G = (V, E)\) graf silniční sítě, \(l : E \mapsto \mathbb{Q}^+\) váhová funkce:
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

{% math definition "T-join" %}\(E' \subseteq E\) je \(T\)-join, jestli graf \(G_T = (V, E')\) splňuje \[\left(\forall v \in V\right) \left(\mathrm{deg}_{G_T} (v)\ \text{lichý} \iff v \in T\right)\]{% endmath %}

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
		- nechť \(M\) je min. perfektní párování v \(H\)
		- nechť \(F = \bigcup_{e \in M} P_e\), kde \(P_e\) je nejkratší cesta v \(G\) spojující vrcholy \(e\)
2. přidej zbylé hrany
3. profit?
{% endmath %}

{% math problem "obchodního cestujícího" %} předpokládáme
- \(G = K_n\) (pro neexistující hrany nastavíme váhu na nekonečno)
- nezáporné délky
- trojúhelníková nerovnost \(\left(\forall u, v, w \in V\right) l(u, v) + l(v, w) \ge l(u, w)\)
{% endmath %}

{% math algorithm "Christofidesova heuristika" %} viz moje [poznámky z aproximačních algoritmů](https://slama.dev/poznamky-z-prednasky/aproximacni-algoritmy#christofides%C5%AFv-algoritmus){% endmath %}

### [Spojitá optimalizace](/assets/diskretni-a-spojita-optimalizace/spojita.pdf)

### Poděkování
- Davidu Kubkovi za zápisky, ze kterých jsem čast z poznámek vytvářel.
