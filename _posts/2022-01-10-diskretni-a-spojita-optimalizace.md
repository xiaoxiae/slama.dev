---
language: cz
title: Diskrétní a spojitá optimalizace
category: "poznamky z prednasky"
category_noslug: "poznámky z přednášky"
redirect_from:
 - /lecture-notes/diskretni-a-spojita-optimalizace/
 - /poznámky-z-přednášky/diskretni-a-spojita-optimalizace/
---

- .
{:toc}

{:.center}
**Poznámky jsou aktuálně rozpracované, dokončené budou až o zkouškovém.**

{% lecture_notes_preface Martina Loebla a Milana Hladíka|2021/2022%}


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

### Poděkování
- Davidu Kubkovi za zápisky, ze kterých jsem poznámky vytvářel
