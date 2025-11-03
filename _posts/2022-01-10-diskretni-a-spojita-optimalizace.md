---
language: cz
title: Diskrétní a spojitá optimalizace
category: "poznamky"
category_noslug: "poznámky"
category_icon: /assets/category-icons/mff.webp
pdf: true
excerpt: Poznámky z přednášky Diskrétní a spojitá optimalizace (Martin Loebl + Milan Hladík, 2021/2022).
---

- .
{:toc}

{% lecture_notes_preface Martina Loebla a Milana Hladíka | 2021/2022 | MFF %}

### Diskrétní optimalizace

#### Matroidy


{% math definition "matroid" %}je dvojice \((X, \mathcal{S})\), kde \(X\) je konečná množina, \(\mathcal{S} \subseteq 2^X\) splňující
1. \(\emptyset \in \mathcal{S}\)
2. **dědičnost**: \((\forall A \in \mathcal{S}) A' \subseteq A \implies A' \in \mathcal{S}\)
3.  **výměnný axiom**: \((\forall U, V \in \mathcal{S})\ |U| > |V| \implies (\exists u \in U \setminus V) V \cup \left\{u\right\} \in \mathcal{S}\)
	- \((3'):\) \(A \subseteq X \implies\) všechny maximální (\(\subseteq\)) podmnožiny \(A\) v \(\mathcal{S}\) mají stejnou velikost

- prvkům \(\mathcal{S}\) říkáme **nezávislé množiny**
- **maximálním** nezávislým množinám (co do inkluze) říkáme **báze**
{% endmath %}

{% math remark %}
Při definici matroidu je dobré si predstavit graf. \(X\) je tu množina hran a \(\mathcal{S}\) všechny acyklické podgrafy.
Pak podmínka dědičnosti říká, že acyklické podgrafy jsou rovněž acyklické a axiom \(3'\) to, že maximální kostry (co do inkluze) mají stejnou velikost.
{% endmath %}

{% math lemma "stejná definice" %}Axiomy \((1, 2, 3)\) a \((1, 2, 3')\) definují stejný objekt.{% endmath %}

{% math proof %}\((3) \implies (3')\) sporem:

- nechť platí \((3)\) ale existuje \(A \subseteq X\) t. ž. pro nějaké \(U, V \subseteq \mathcal{S}\) platí \(U, V \subseteq A\), \(U, V\) jsou do inkluze maximální ale \(|U| > |V|\)
- díky \((3)\) \((\exists u \in U \setminus V)\) t. ž. \(V \cup \left\{u\right\} \in \mathcal{S}\), což je spor s maximalitou \(V\).
{% endmath %}

{% math proof %}\((3') \implies (3)\) sporem:
- nechť \(U, V \in \mathcal{S}\) a \(|U| > |V|\) a \(V\) je maximální (negace výměnného axiomu)
- definujme \(A = U \cup V \subseteq X\); pak \(V\) je maximální ale \(|U| > |V|\), což je spor
{% endmath %}

{% math example %}
1. **vektorový matroid**:
	- nechť \(M\) je matice nad tělesem \(\mathbb{F}\) s řádky \(C\)
	- \(\mathcal{V}_M = (C, \mathcal{S})\), kde
		- \(A \in \mathcal{S} \iff A \subseteq C\) je lineárně nezávislá v \(\mathbb{F}\)
		- 3' vyplývá přímo ze Steinitzovy věty o výměně, zbytek přímo z definice
2. **grafový matroid**:
	- mějme graf \(G = (V, E)\)
	- \(\mathcal{M}_G = (E, \mathcal{S})\), kde
		- \(A \in \mathcal{S} \iff A \subseteq E \) a \(A\) je acyklická
		- \((1):\) \(\emptyset \in \mathcal{S}\)
		- \((2):\) podmnožina acyklické je rovněž acyklická
		- \((3):\) počítání přes to, kolik hran je v komponentách souvislosti
3. **Fanova rovina**:
	- za \(X\) uvážíme body Fanovy roviny a za báze trojprvkové množiny bodů neležící na jedné přímce (v rámci Fanovy roviny -- kružnice uprostřed je také přímka)

![](/assets/diskretni-a-spojita-optimalizace/fano.svg)
{% endmath %}

##### Grafy a matroidy

{% math definition "sudá podmnožina hran" %} podmnožina hran \(E' \subseteq E\) je sudá, právě když \(H = (V, E')\) má pouze sudé stupně.{% endmath %}

{% math definition: "matice incidence" %} grafu \(G = (V, E)\) je matice \(I_G \in \mathbb{F}_2^{|V| \times |E|}\) t.ž. \[\left(I_G\right)_{v,e}=\begin{cases} 1 & v \in e \\ 0 & \text{jinak} \end{cases}\]{% endmath %}

![](/assets/diskretni-a-spojita-optimalizace/incidence-matrix.svg)

{% math definition "jádro matice incidence" %}pro matici incidence \(I_G\) definujeme jádro jako
\[\mathrm{Ker}_{\mathbb{F}_2} I_G = \left\{\mathbf{x} \in \mathbb{F}_2^{|E|} \mid I_G \mathbf{x} = \mathbf{0}\right\}\]
{% endmath %}

{% math definition "charakteristický vektor" %}mějme nosnou množinu \(X\) a podmnožinu \(A \subseteq X\). Charakteristický vektor \(A\) je \(\chi_A \in \left\{0, 1\right\}^{|X|}\) t.ž. \[\left(\chi_A\right)_{k} = \begin{cases} 1 & k \in A \\ 0 & k \not\in A \end{cases}\]{% endmath %}

{% math observation %}řádek matice incidence \(I_G\) indexovaný vrcholem \(w\) je roven \(\chi_{\underbrace{|N(w)|}_{\text{okolí}}}\){% endmath %}

{% math observation "prostor cyklů" %}jádro matice můžeme ekvivalentně vyjádřit jako \[\mathrm{Ker}_{\mathbb{F}_2} I_G = \left\{x \in \mathbb{F}_2^{|E|} \mid x = \chi_{E'}\ \text{pro}\ E'\ \text{sudou}\right\}\]{% endmath %}
Tuto množinu rovněž nazýváme **prostor cyklů.**

##### Řádové funkce

{:.rightFloatBox}
<div markdown="1">
V řeči grafů chceme pro libovolnou množinu hran (prvků podmnožin) vrátit největší acyklický podgraf (prvek matroidu).
</div>

{% math definition "řádová funkce" %}mějme systém podmnožin \((X, \mathcal{S}), \mathcal{S} \subseteq 2^{X}\) a \(A \subseteq X\). Pak řádovou funkci \(r: 2^{X} \mapsto \mathbb{N}\) definujeme jako **velikost maximální podmnožiny patřící do** \(\mathcal{S}\):

\[r(A) = \max \left\{|X| \mid X \in 2^A \land X \in \mathcal{S}\right\}\]
{% endmath %}

{% math theorem "řádová funkce matroidu" %}funkce \(r : 2^X \mapsto \mathbb{N}\) je řádová funkce nějakého matroidu nad \(X\) právě tehdy, když platí:
- \((\mathrm{R1})\): \(r(\emptyset) = 0\)
- \((\mathrm{R2})\): \(r(Y) \le r(Y \cup \left\{y\right\}) \le r(Y) + 1\)
- \((\mathrm{R3})\): \(r(Y \cup \left\{y\right\}) = r(Y \cup \left\{z\right\}) = r(Y) \implies r(Y) = r(Y \cup \left\{y ,z\right\})\)
{% endmath %}

{% math proof "\(\Rightarrow\)" %} ukážeme přímo:

- \((\mathrm{R1})\): max. nezávislá podmnožina \(\emptyset\) je \(\emptyset\) a \(|\emptyset| = \emptyset\)
- \((\mathrm{R2})\): z definice řádové funkce a dědičnosti matroidu
- \((\mathrm{R3})\): nechť \(B\) je max. nez. podmn. \(Y\) a \(\tilde{B}\) je max. nez. podmn. \(Y \cup \left\{y, z\right\}\) t.ž. \(B \subseteq \tilde{B}\)

![](/assets/diskretni-a-spojita-optimalizace/charakteristika-proof.svg)

Pokud \(|B| = |\tilde{B}|\), pak platí \(\mathrm{R3}\)
- jinak \(B \subsetneq \tilde{B}\), BUNO například \(y \in \tilde{B}\)
   - \(B \cup \left\{y\right\}\) je nezávislá a \(r(Y) < r(Y \cup \left\{y\right\})\) a předpoklad implikace v \(\mathrm{R3}\) neplatí
{% endmath %}

{% math proof "\(\Leftarrow\)" %}
z \(X\) konstruujeme matroid s řádovou funkcí \(r\).
Matroid definujme jako \[\mathcal{M} = \left(X, \mathcal{S}\right)\quad\text{t.ž.}\quad A \in \mathcal{S} \iff |A| = r(A)\]

Ukážeme, že \(\left(X, \mathcal{S}\right)\) je matroid:
1. \(\emptyset \in \mathcal{S}\) (triviálně)
2. pro spor předpokládejme, že dědičnost neplatí
	- existuje tedy \(A \in \mathcal{S}, A' \subseteq A\) ale \(|A'| > r(A')\) (menší nemůže být z definice řádové funkce, jelikož je pro množinu definována jako velikost nějaké její podmnožiny)
\[\begin{aligned}
	r(A) &\le r(A') + |A \setminus A'| & \quad \text{R2} \\
	&< |A'| + |A \setminus A'| \\
	&= |A| \implies A \not\in \mathcal{S} & ↯
\end{aligned}\]
3. pro spor předpokládejme, že \(\exists U, V \in \mathcal{S}\) t.ž. \(|U| > |V|\) ale \(\forall x \in U \setminus V: V \cup \left\{x\right\} \not\in \mathcal{S}\)
	- přes \(\mathrm{R3}\) získáváme \((\forall x, y \in U \setminus V)\):
\[\begin{aligned}
r(V) &= r(V \cup \left\{x\right\}) = r(V \cup \left\{y\right\}) \\
&\Rightarrow r(V \cup \left\{x, y\right\}) & \quad \mathrm{R3}\\
&\Rightarrow r(V \cup (U \setminus V)) = r(U \cup V) \ge r(U) = |U| & ↯
\end{aligned}\]

{% math remark "alternativní znění důkazu 2" %}díky R2 víme, že odebráním prvku z \(A\) se může \(r(A)\) buď o 1 snížit, nebo zůstat stejný. Zůstat stejný být však nemůže (z definice řádové funkce), musí se tedy o \(1\) snížit a v tom případě je rovněž v \(\mathcal{S}\).
{% endmath %}

{% endmath %}

{% math theorem "řádová funkce a submodularita" %} \(r : 2^X \mapsto \mathbb{N}\) je řádová funkce matroidu \(\iff\)
- \((\mathrm{R1'}): \forall Y \in X: 0 \le r(Y) \le |Y|\)
- \((\mathrm{R2'}\ \text{-- monotonie}): Z \subseteq Y \subseteq X \implies r(Z) \le r(Y)\)
- \((\mathrm{R3'}\ \text{-- submodularita}): r(Y \cup Z) + r(Y \cap Z) \le r(Y) + r(Z)\)
{% endmath %}

{% math proof "\(\Rightarrow\) R1' a R2'" %}
- \((\mathrm{R1'})\): mějme \(Y \subseteq X\)
	- \(r(Y) \ge 0\) (funkce je definována na \(\mathbb{N}\))
	- \(r(Y) \le |Y|\) (max. nezávislá množina je z definice menší než její množina)
- \((\mathrm{R2'})\): přímo vylývá z R2 (\(r(A) \le r(A \cup \left\{x\right\})\))
{% endmath %}

{% math proof "\(\Rightarrow\) R3'" %}
- \(A\) -- maximální nezávislá množina v \(Y \cap Z\)
- \(A_Y\) -- maximální nezávislá množina v \(Y\) t.ž. \(A \subseteq A_Y\) (nějaká taková existuje)
- \(A_Z\) -- maximální nezávislá množina v \(Y\) t.ž. \(A \subseteq A_Z\) (nějaká taková existuje)

![](/assets/diskretni-a-spojita-optimalizace/sub-proof-1.svg)

Máme \[\begin{aligned}
	r(Y) + r(Z) &= |A_Y| + |A_Z| & \quad \text{definice} \\
	            &= |A_Y \cap A_Z| + |A_Y \cup A_Z| & \quad \text{inkluze/exkluze} \\
	            &\ge r(Y \cap Z) + |A_Y \cup A_Z| & \quad A \subseteq A_Y \cap A_Z
\end{aligned}\]
K důkazu tvrzení zbývá ukázat, že \(|A_Y \cup A_Z| \ge r(Y \cup Z)\).

{% math observation %}\(A_Y\) nemůže být rozšířené víče než \(A_Z \setminus Y\) prvky na nezávislou množinu v \(Y \cup Z\){% endmath %}

![](/assets/diskretni-a-spojita-optimalizace/sub-proof-2.svg)

- pro spor předpokládejme, že \(W \subseteq Z \setminus Y\) maximální, \(A_Y \cup W\) je nezávislá a \(|W| > |A_Z \setminus Y|\); pak ale \(|W \cup A| > |A_Z|\), což je spor s maximalitou \(A_Z\)

Nyní můžeme dokončit důkaz:
\[\begin{aligned}
	r(Y \cup Z) &\le |A_Y| + |A_Z \setminus Y| \\
	& \le |A_Y \cup A_Z|
\end{aligned}\]
{% endmath %}

{% math proof "matroid \(\Leftarrow\) R1', R2', R3'" %}ukážeme \(\mathrm{R1, R2, R3}\)
- \((\mathrm{R1})\): dokazujeme \(r(\emptyset) = 0\)
	- nechť pro spor \(r(\emptyset) > 0\); pak \(|\emptyset| \ge r(\emptyset) > 0\), což je spor
- \((\mathrm{R2})\): dokazujeme \(r(Y) \le r(Y \cup \left\{y\right\}) \le r(Y) + 1\)
	- mějme \(Y \subseteq X\), \(y \in X\) a \(y \not\in Y\) (jinak platí triviálně)
		- první nerovnost (z monotonie): \[Y  \subseteq Y \cup \left\{y\right\} \implies r(Y) \le r(Y \cup \left\{y\right\})\]
		- druhá nerovnost (ze submodularity): \[r(Y \cup \left\{y\right\}) + \overbrace{r(\underbrace{Y \cap \left\{y\right\}}_{\emptyset})}^{0} \le r(Y) + r(\left\{y\right\}) \le r(Y) + 1\]
- \((\mathrm{R3})\): dokazujeme \(r(Y \cup \left\{y\right\}) = r(Y \cup \left\{z\right\}) = r(Y) \implies r(Y) = r(Y \cup \left\{y ,z\right\})\)
	- z monotonie dostáváme první část: \(Y \subseteq Y \cup \left\{y, z\right\} \implies r(Y) \le r(Y \cup \left\{y, z\right\})\)
	- nyní použijeme submodularitu na \(A = Y \cup \left\{y\right\}, B = Y \cup \left\{z\right\}\)
		- předpokládáme, že \(y \neq z\) a že \(x, y \not\in Y\), jinak platí triválně \[r(\underbrace{Y \cup \left\{y, z\right\}}_{A \cup B}) + r(\underbrace{Y}_{A \cap B}) \le r(\underbrace{Y \cup \left\{y\right\}}_{A}) + r(\underbrace{Y \cup \left\{z\right\}}_{B})\]
		- pokud tedy platí \(r(Y) \cup \left\{y\right\} = r(Y \cup \left\{z\right\}) = r(Y)\), tak dostáváme druhou část:
\[r(Y \cup \left\{y, z\right\}) \le r(Y)\]
{% endmath %}

{% math observation %}matroidy jsou systémy podmnožiny, kde řádová funkce je **monotonní** a **submodulární**.{% endmath %}


{:.rightFloatBox}
<div markdown="1">
„Jak cením přidání \(x\), když mám \(T\).“
</div>

{% math definition "marginální hodnota" %}
Mějme množinu \(X\) a funkce \(f: 2^X \mapsto \mathbb{N} \). Pak \(\forall x \in X\) definujeme \(\Delta f_x : 2^X \mapsto \mathbb{Z}\):
\[T \subseteq X \implies \Delta f_x (T) = f(T \cup \left\{x\right\}) - f(T)\]
{% endmath %}

{% math theorem "marginální hodnota a submodularita" %} \(f: 2^X \mapsto \mathbb{N}\) je submodulární \(\iff \forall x \in X: \Delta f_x\) je nerostoucí
- nerostoucí myslíme následně: \(T' \subseteq T, x \not\in T \implies \Delta f_x(T') \ge \Delta f_x(T)\)
	- menším množinám záleží (oproti větším) víc na přidání prvku, který nemají
{% endmath %}

{% math proof %}Je-li \(f\) nerostoucí, pak \(\forall U, y, z\) platí \[\underbrace{f(U \cup \left\{y, z\right\}) - f(U \cup \left\{y\right\})}_{\Delta f_z(U \cup \left\{y\right\})} \le \underbrace{f(U \cup \left\{z\right\}) - f(U)}_{\Delta f_z(U)}\]

Tedy \(f\) je nerostoucí \(\iff \forall U \subseteq X\) a \(y, z \in X \setminus U\) platí \[f(\underbrace{U \cup \left\{y\right\}}_{A}) + f(\underbrace{U \cup \left\{z\right\}}_{B}) \ge f(\underbrace{U \cup \left\{y, z\right\}}_{A \cup B}) + f(\underbrace{U}_{A \cap B}) \qquad *\]

To je skoro submodularita!

{% math proof "\(\Rightarrow\)" %}platí přímo z definice submodularity (prostě tam dosadíme){% endmath %}

{% math proof "\(\Leftarrow\)" %}dokazujeme \(* \implies\) submodularita. Chceme \[f(Y) + f(Z) \ge f(Y \cup Z) + f(Y \cap Z)\]

- definujme \(S = Y \cap Z\), \(A = Y \setminus S\) a \(B = Z \setminus S\), pak

  - \(Y = S \cup A\)
  - \(Z = S \cup B\)
  - \(Y \cup Z = S \cup A \cup B\)
  - \(Y \cap Z = S\)

- zkonstruujeme \(f(Y)\) a \(f(Z)\) z \(f(S)\) za pomocí posloupností marginálních hodnot:
  - rozepišme definici marginální hodnoty jako \(f(X \cup \{y_1\}) = f(X) + \Delta f_{y_1}(X)\)
    - dvojím rozepsáním dostaneme:
      \[ f(X \cup \{y_1,y_2\}) = f(X \cup \{y_1\}) + \Delta f_{y_2}(X \cup \{y_1\}) = f(X) + \Delta f_{y_1}(X) + \Delta(X \cup \{y_1\}) \]
    - opakovaným rozepsáním pro \(Y = \{y_1, y_2, \dots , y_k\}\) dostaneme: \[ f(X \cup Y) = f(X) + \sum_{i = 1}^k f_{y_i}(X \cup \{y_1, \dots y_{i-1}\}) \]
  - zafixujme pořadí prvků v \(A \cup B\): \(a_1, a_2, \dots , a_k) a BÚNO (A = \{a_1, \dots , a_r\}) a (B = \{a_{r+1}, \dots, a_k\}\), potom:
    \[ \begin{aligned}
    f(Y) = f(S \cup A) &= f(S) + \sum_{i=1}^r \Delta f_{a_i}(S \cup\{a_1, \dots a_{i-1}\}) \\
    f(Z) = f(S \cup B) &= f(S) + \sum_{i=r+1}^k \Delta f_{a_i}(S \cup\{a_{r+1}, \dots a_{i-1}\}) \\
    f(Y \cup Z) = f(S \cup A \cup B) &= f(S) + \sum_{i=1}^k \Delta f_{a_i}(S \cup \{a_1, \dots , a_{i-1}\})
    \end{aligned} \]
  - pro každé \(i = 1, \dots , r\) platí, že \(S \cup \{a_1, \dots , a_{i-1}\} \subseteq S \cup \{a_{1}, \dots, a_{i-1}\} \cup \{a_{r+1}, \dots , a_{k}\}\), takže:
    \[
    \Delta f_{a_i}(S \cup \{a_1, \dots , a_{i-1}\}) \ge \Delta f_{a_i}(S \cup \{a_1, \dots a_{i-1}, a_{r+1}, \dots , a_k\})
    \]
  - stejně pro každé \(i = r+1, \dots , k\) máme:
    \[
    \Delta f_{a_i}(S \cup \{a_{r+1}, \dots , a_{i-1}\}) \ge \Delta f_{a_i}(S \cup \{a_1, \dots a_{i-1}\})
    \]
  - součtem obou stran dostaneme:
    \[ \begin{aligned}
    f(Y) + f(Z) &= f(S \cup A) + f(S \cup B) \\
    &= f(S) + \sum_{i=1}^r \Delta f_{a_i}(S \cup\{a_1, \dots a_{i-1}\}) \\
    &+ f(S) + \sum_{i=r+1}^k \Delta f_{a_i}(S \cup\{a_{r+1}, \dots a_{i-1}\}) \\
    &\ge f(S) + \sum_{i=1}^k\Delta f_{a_i}(S \cup \{a_1, \dots , a_{i-1}\}) + f(S) \\
    &= f(S \cup A \cup B) + f(B) \\ \\
    &= f(Y \cup Z) + f(Y \cup Z)
    \end{aligned} \]

{% endmath %}

{% endmath %}

##### Hladový algoritmus

{% math definition "úloha kombinatorické optimalizace" %}je dán možinový systém \((X, \mathcal{S})\) a váhová funkce \(w : X \mapsto \mathbb{Q}\). **Úloha kombinatorické optimalizace** je najít \(A \in \mathcal{S}\) t.ž. \[w(A) = \sum_{v \in A} w(v) = w^T \chi_A\] je **maximální** (\(\chi_A\) je charakteristický vektor \(A\), který je \(1\) pro \(v \in A\) a \(0\) jindy).{% endmath %}

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

{% math observation %}algoritmus je polynomiální (pro rozumné předpoklady na reprezentaci matroidu).{% endmath %}

{% math observation %}pro výše uvedené příklady nemusí algoritmus vrátit optimální řešení.{% endmath %}

{% math theorem "hladový algoritmus na matroidech" %}nechť \((X, \mathcal{S})\) je dědičný množinový systém a \(\emptyset \in \mathcal{S}\). Pak hladový algoritmus vyřeší správně úlohu kombinatorické optimalizace pro **každou funkci** \(w \iff (X, \mathcal{S})\) je matroid.{% endmath %}

{% math proof "\(\Rightarrow\)" %}obměnou: nechť \((X, \mathcal{S})\) není matroid \(\implies\) HA nefunguje. Zkonstruujeme \(w : X \mapsto \mathbb{Q}\), na které algoritmus selže.

Jelikož \((X, \mathcal{S})\) není matroid, tak neplatí \(3, 3'\) a tedy \(\exists U, V \in \mathcal{S}, |U| > |V|\) a \(U, V\) jsou max. nezávislé množiny. Pak definujeme \(w\) následně (pro \(b, a \in \mathbb{Q}, b > a > 0\)):

![](/assets/diskretni-a-spojita-optimalizace/ha-spor.svg)

V takovém případě hladový algoritmus najde \(U\), ikdyž \(V\) je větší.
{% endmath %}

{% math proof "\(\Leftarrow\)" %} nejprve dokážeme pomocné lemma.

{% math lemma %}mějme \(w_1 \ge \ldots \ge w_n\), \(m \le n\) maximální t.ž. \(w_m > 0\), množiny \(T_i \subseteq \left\{0, 1\right\}^i\) a \(z'\) je **charakteristický vektor výsledku HA** (rozumíme tím, že je to \(0/1\) vektor podle toho, které prvky HA vybral s tím, že jsou setřízené podle \(w\)). Pak \(\forall i\) platí \[z'(T_i) = \sum_{i \in T_i} z'_i = r(T_i)\]
{% endmath %}

{% math proof %}
Ukážeme, že HA najde v každém kroku největší nezávislou množinu z uvažovaných prvků.

Pro spor nechť \(\exists i\) t.ž. \(z'(T_i) < r(T_i)\).
Vezměme nejmenší takové \(i\):

![](/assets/diskretni-a-spojita-optimalizace/ha-nespor.svg)

Platí, že \(z'(T_{i - 1}) = r(T_{i - 1})\) (jelikož \(i\) je nejmenší protipříklad). Pokud HA další prvek přidá, tak je vše v pořádku a \(z'(T_{i}) = r(T_{i})\) platí. Jinak to znamená, že \(z'(T_{i})\) je co do inkluze maximální množina v \(T_i\), což je spor s \(3'\).

{% endmath %}

Nyní k původnímu důkazu: označíme \(z^*\) charakteristický vektor optima. Pak

\[\begin{aligned}
	w^T z^* &= \sum w_i \cdot z^*_i \\
	&= \sum w_i (z^*(T_i) - z^*(T_{i - 1})) & \qquad T_0 = \emptyset, * \\
	&= \sum \underbrace{(w_i - w_{i + 1})}_{\ge 0} z^* (T_i) + \underbrace{w_m}_{> 0} z^*(T_m) & ** \\
	&\le \sum (w_i - w_{i + 1}) r (T_i)_i + w_m r(T_m) \\
	&= \sum (w_i - w_{i + 1}) z' (T_i)_i + w_m z'(T_m) & \text{lemma výše} \\
	&= w^T z' \\
\end{aligned}\]

\(*\) rovnost \(z_i^* = z_i^*(T_i) - z_i^*(T_{i - 1})\) platí, protože \(z_i^*(T_i)\) se zvýší právě tehdy, když charakteristický vektor získá novou \(1\) (konkrétně tu na pozici \(z_i^*\)).

\(**\) tohle vypadá magicky, ale dává to smysl -- \(z^*(T_i)\) v jednom cyklu smyčky přičítáme a ve druhém odčítáme, tak jsme to jen posunuli do \(w_i - w_{i + 1}\), navíc také započteme poslední část součtu, na který se nedostane. Navíc právě v tomhle kroku používáme **předpoklad setřízenosti.**

Jelikož navíc triviálně \(w^T z* \ge w^T z'\) (je to optimum), tak věta platí.
{% endmath %}

{% math consequence "grafy" %}poštvání HA na grafový matroid vrátí maximální (minimální pro \(-w\)) kostru. Poštvání na duál vrátí maximální množinu hran, kterou když odstraníme tak graf zůstane souvislý.{% endmath %}

{% math consequence "lineární programy" %}nechť \((X, \mathcal{S})\) je matroid a \(w \in \mathbb{Q}^X\). Pak HA vyřeší následující lineární program \[\max \sum_{i \in X} w_i z_i\] za podmínek \(z(A) \le r(A), z \ge 0\) pro \(\forall A \subseteq X\)
{% endmath %}

##### Operace na matroidech

**Součet** -- pro matroidy \(\mathcal{M_1} = (X_1, \mathcal{S}_1), \mathcal{M_2} = (X_2, \mathcal{S}_2), X_1 \cap X_2 = \emptyset\)
\[\mathcal{M}_1 + \mathcal{M}_2 = (X = X_1 \cup X_2, \left\{A \in X \mid A \cap X_1 \in \mathcal{S}_1 \land A \cap X_2 \in \mathcal{S}_2\right\})\]

{% math example "mazání a kontrakce v grafovém matroidu" %}
![](/assets/diskretni-a-spojita-optimalizace/sumcontex.svg)
{% endmath %}

**Sjednocení** -- zobecnění součtu. Definice je stejná, ale nepředpokládáme různé \(X_1, X_2\).

{% math theorem "sjednocení matroidů je matroid)" %} sjednocení matroidů je matroid s řádovou funkcí \[r(U) = \min_{T \subseteq U} \left\{|U - T| + r_1(T \cap X_1) + \ldots + r_k(T \cap X_k)\right\}\]{% endmath %}

{% math proof "náznak" %}matroidy zdisjunktníme (\(X'_i = X_i
\times \left\{i\right\}\)), sečteme a pak zobrazíme.{% endmath %}

{:.rightFloatBox}
<div markdown="1">
Mazání hran v grafu.
</div>

**Mazání** -- pro matroid \(\mathcal{M} = (X, \mathcal{S})\) a \(Y \subseteq X\):
\[\mathcal{M} - Y = (X - Y, \left\{A - Y \mid A \in \mathcal{S}\right\})\]
je opět matroid.

{:.rightFloatBox}
<div markdown="1">
Podobné jako mazání, ale chová se dost jinak (viz kontrakce/mazání hran v grafu). Např. na mostech grafu se ale chová stejně.
</div>

**Kontrakce** -- nechť \(\mathcal{M} = (X, \mathcal{S})\) je matroid, \(A \subseteq X\) a \(J \in \mathcal{S}\) je max. nezávislá množina v \(A\). Pak
\[\mathcal{M} \setminus A = \left(X - A, \left\{Z \subseteq X \mid Z \cup J \in \mathcal{S} \right\}\right)\]

{% math theorem "kontrakce matroidu je matroid" %} nechť \(\mathcal{M} = (X, \mathcal{S})\) je matroid a \(A \subseteq X\). Pak \(\mathcal{M} \setminus A\) je matroid s řádovou funkcí
\[r'(Z) = r(Z \cup A) - r(A)\]
{% endmath %}

{% math proof %}nechť \(J\) je max. nz. mn v \(A\) (viz definice kontrakce); ověříme axiomy
1. \(\emptyset \in \mathcal{S} \iff \emptyset \cup J = J \in \mathcal{S}\), platí
2. mějme \(Y \in \mathcal{S}'\) a \(Y' \subseteq Y\). Z definice víme \(Y \in \mathcal{S}' \implies Y \cup J \in \mathcal{S}\). Díky tomu, že \(Y' \cup J \subseteq Y \cup J \in \mathcal{S}\), tak rovněž \(Y' \cup J \in \mathcal{S}\) (definice matroidu) a tedy \(Y' \in \mathcal{S}'\)
3. nechť \(Z \subseteq X \setminus A\), \(B \subseteq Z\) je max. nez. mn. v \(\mathcal{M} \setminus A\) a \(J\) max. nez. mn. v \(A\)

![](/assets/diskretni-a-spojita-optimalizace/contproof.svg)

\(B \cup J\) je max. nezávislá podmnožina \(Z \cup A\) v \(\mathcal{M}\) a tedy \[\begin{aligned}
   	|B| + |J| &= r(Z \cup A) \\
   	|B| &= r(Z \cup A) - |J|  \\
   	r'(Z) &= \underbrace{r(Z \cup A) - r(A)}_{\text{určený jednoznačně}}
   \end{aligned}\]
{% endmath %}

**Partition matroid** -- nechť \(X_1, \ldots, X_n\) jsou disjunktní množiny a \(\mathcal{S}_i = \left\{A \subseteq X_i \mid |A| \le 1\right\}\). Pak \(\sum_{i} (X_i, \mathcal{S}_i)\) je partiční matroid.

{% math theorem "Edmondsova MiniMaxová o průniku matroidů" %}nechť \(\mathcal{M}_1 = \left(X, \mathcal{S}_1\right)\) a \(\mathcal{M_2} = \left(X_{1}, \mathcal{S_2}\right)\) jsou matroidy. Pak
\[\max \left\{|Y| \mid Y \in \mathcal{S_1} \cap \mathcal{S}_2\right\} = \min_{A \subseteq X} r_1(A) + r_2(X \setminus A)\]
{% endmath %}

{% math proof "\(\le\)" %}Nechť \(J \in \mathcal{S}_1 \cap \mathcal{S}_2\). Pak \(\forall A \subseteq X\)
\[\begin{aligned}
	J \cap A &\in \mathcal{S}_1 \implies |J \cap A| \le r_1(A) \\
	J \cap (X \setminus A) &\in \mathcal{S}_2 \implies |J \cap (X \setminus A)| \le r_2(X \setminus A)
\end{aligned}\]
A tedy
\[|J| = |J \cap A| + |J \cap (X \setminus A) | \le r_1(A) + r_2(X \setminus A)\]
{% endmath %}

{% math proof "\(\ge\)" %}TODO, tenhle důkaz je naprosto brutální{% endmath %}

{% math consequence "obraz matroidu je matroid" %}mějme matroid \(\mathcal{M}' = (X', \mathcal{S}')\) a funkci \(f: X' \implies X\). Definujme \[\mathcal{S} = \left\{f[I] \mid I \in \mathcal{S}'\right\}\]
Potom \((X, \mathcal{S})\) je také matroid a navíc pro \(U \subseteq T\) platí \[r(U) = \min_{T \subseteq U} \left\{|U - T| + r'(f^{-1} (T))\right\}\]{% endmath %}

![](/assets/diskretni-a-spojita-optimalizace/matroid-obraz.svg)

{% math remark %}tvrzení by platilo triviálně, pokud by se jednalo o prostou funkci (tedy pouze přejmenování prvků matriodu). Zajímavé je to, že některé prvky se mohou zobrazit na jiné a nezávislé množiny se tak zmenší, ale matroidnost se zachová.
{% endmath %}

##### Dualita matroidu

{:.rightFloatBox}
<div markdown="1">
Duální matroid grafového matroidu je matroid množin hran, které když odebereme tak graf zůstane spojitý.
</div>

{% math definition "duální matroid" %}nechť \(\mathcal{M} = \left(X, \mathcal{S}\right)\) je matroid. Definujeme duální matroid jako \(\mathcal{M}^* = (X, \mathcal{S}^*)\) t.ž. \(B^*\) je báze \(\mathcal{M}^* \iff (X - B^*)\) je báze \(\mathcal{M}\) (s tím, že \(\mathcal{S}^*\) jsou všechny podmnožiny bází).
{% endmath %}

{% math observation %}nechť \(\mathcal{M}\) je matroid, \(\mathcal{M}^*\) jeho duál a \(A \subseteq X\). Pak \[r(X) = r(X \setminus A) \ \iff \ A \in \mathcal{S}^*\]
{% endmath %}

{% math proof %}\(A\) můžeme rozšířit na bázi \(B^*\) duálu, přičemž bude stále platit \(r(X - B^*) = r(X)\), protože \(X - B^*\) je báze \(\mathcal{M}\). Tohle můžeme dělat ikdyž jsme další větu ještě nedokázali, jelikož pro \(\mathcal{M}^*\) platí axiomy 1 a 2 matroidu, jelikož jsme ho definovali jako báze.{% endmath %}

{% math theorem "duální matroid je matroid" %}nechť \(\mathcal{M}\) je matroid. Pak \(\mathcal{M}^*\) je také matroid a navíc platí \[r^*(A) = |A| - r(X) + r(X - A)\]
{% endmath %}

![](/assets/diskretni-a-spojita-optimalizace/baze-dualita.svg)

{% math proof %} stačí dokázat \(3'\) (pro dané \(A\) mají všechny nezávislé množiny stejnou velikost), jelikož \(1\) a \(2\) platí triviálně z toho, že jsme definovali pouze báze. Uvažme libovolné \(A\) a následující obrázek

![](/assets/diskretni-a-spojita-optimalizace/dualita-proof.svg)

Nechť \(B\) je báze \(\mathcal{M}\) t.ž. \(Z \subseteq B\) a \(B \subseteq X - J\) (existuje, protože \(r(X) = r(X - J)\))

Jestli existuje \(x \in (A - J) - B\), pak \(r(X - (J \cup \left\{x\right\})) = r(X)\) a \(J \cup \left\{x\right\} \in \mathcal{S}^*\) a \(J\) není maximální, díky čemuž \(J = A - B\). Rovněž platí \(Z = B - A\) (jinak můžeme rozšířit, což je spor) a tedy \[\begin{aligned}
	r^*(A) = |J| &= |A - B| \\
	             &= |A| - |B \cap A| \\
	             &= |A| - |B \cap (B - Z)| \\
	    &= |A| - |B| + |Z| \\
	    &= |A| - r(X) + r(X - A)
\end{aligned}\]
{% endmath %}

{% math remark %}Matroid může být [duální sám sobě](https://en.wikipedia.org/wiki/Dual_matroid#Self-dual_matroids) (v tom smyslu, že \(\mathcal{M}_1\) a \(\mathcal{M}_2\) jsou izomorfní).{% endmath %}

{% math definition "Cobáze, conezávislost" %}nechť \(\mathcal{M}\) je matroid a \(\mathcal{M}^*\) jeho duální matroid. Pak \(Y \subseteq X\) je
- **cobáze**, pokud je báze v \(M^*\)
- **conezávislá**, pokud je nezávislá v \(M^*\){% endmath %}

{:.rightFloatBox}
<div markdown="1">
V grafu jsou to kružnice.
</div>

{% math definition "kružnice" %}nechť \(\mathcal{M}\) je matroid. Pak \(Y \subseteq X\) je kružnice, je-li minimální (\(\subseteq\)) **závislá** množina.{% endmath %}

{% math theorem %}\(Y \subseteq X\) je cokružnice (kružnice v duálu) \(\iff Y\) je min (\(\subseteq\)) protínající **každou bázi**.{% endmath %}


{% math proof "\(\Rightarrow\)" %}sporem nechť \(Y \subseteq X\) je cokružnice ale \(\exists B\) báze \(\mathcal{M}\) t.ž. \(Y \cap B = \emptyset\). Pak \(Y \subseteq X - B\) ale z definice je \(X - B\) báze \(\mathcal{M}^*\), což je spor se závislostí \(Y\) v \(\mathcal{M^*}\). Navíc kružnice je do inkluze minimální, takže minimalitu splňujeme taky.
{% endmath %}

{% math proof "\(\Leftarrow\)" %}opět sporem nechť \(Y\) je minimální množina (do inkluze) protínající každou bázi, ale není cokružnice. Rozebereme případy toho, co může být (chceme, aby byla minimálně nezávislá):
- \(Y\) je nezávislá v \(M^*\) (a tedy \(r(X) = r(X - Y)\))
	- pak existuje báze \(B \subseteq X - Y\) v \(\mathcal{M}\), což je spor s tím, že protíná každou bázi
- \(Y\) není minimálně nezávislá (tedy \(\exists y \in Y\) t.ž. \(Y \setminus \left\{y\right\}\) je závislá v \(M^*\)):
	- \((Y \setminus \left\{y\right\}) \not\in \mathcal{S}^*\)
	- \(r(X) > r(X - (Y \setminus \left\{y\right\}))\)
	- \(Y \setminus \left\{y\right\}\) protíná každou bázi, což je spor s minimalitou
{% endmath %}

{% math consequence %}nechť \(G\) graf souvislý. Pak cokružnice \(\mathcal{M}_G\) jsou přesně **minimální hranové řezy**. {% endmath %}

#### Perfektní párování
{% math remark %}o tomto tématu jsem vytvořil [YouTube video](https://www.youtube.com/watch?v=3roPs1Bvg1Q), které algoritmus shrnuje.{% endmath %}

{% math definition "párování" %}nechť \(G = (V, E)\) graf. Pak \(M \subseteq E\) je párovaní \(\iff \forall e \neq e' \in M\) platí \(e \cap e' = \emptyset\).{% endmath %}

{% math definition: "největší párování" %} pokud \(|M|\) je maximální.{% endmath %}

{% math observation %}je rozdíl mezi **maximálním** párováním (počítá se do **inkluze**) a **největším** (počítá se do **velikosti**), jelikož si hrany můžeme hladově vybrat špatně (viz lichá cesta).{% endmath %}

{% math definition "perfektní párování" %}pokud \(|M| = |V| / 2\){% endmath %}

{% math definition "pokrytí" %}vrchol je \(M\)-pokrytý, pokud je v nějaké hraně z párování.{% endmath %}

{% math definition: "defekt" %} \(\mathrm{def}(M)\) je počet \(M\)-nepokrytých vrcholů{% endmath %}

{% math definition "alternující cesta" %}podgraf, který je cesta
- je **zlepšující**, pokud má krajní vrcholy \(M\)-nepokryté
{% endmath %}

{% math theorem %}graf \(G = (V, E)\), \(M\) párování. Pak \(M\) je největší \(\iff\) \(G\) nemá zlepšující cestu.{% endmath %}

{% math proof %}
- \(\Leftarrow\) pokud má zlepšující cestu, tak párování můžeme zlepšit a není tedy maximální
- \(\Rightarrow\) pokud \(G\) není maximální tak existuje párování \(M'\) t. ž. \(M' > |M|\)
	- uvažme graf \(M \Delta M'\) -- stupně mají vrcholy nejvýše dva, komponenty jsou tedy buď alternující cykly nebo cesty -- díky tomu, že nám jedna hrana přebývá, tak alespoň jedna komponenta je cesta
{% endmath %}

{% math observation %} \(G = (V, E), A \subseteq V\). Pak v libovolném párování \(M\) musí být liché komponenty \(G - A\) pokryté pouze z \(A\) (i v nejlepším zpárování v nich zbyde alespoň jeden volný vrchol) a tedy
\[\mathrm{def}(M) \ge \mathrm{lc}(G - A) - |A|\]
Kde \(\mathrm{lc}\) značí počet lichých komponent grafu.
{% endmath %}

{% math observation %} \(G = (V, E)\). Pak \[\max_{\text{párování}\ M} |M| = \min_{\text{párování}\ M} \frac{1}{2} \left(|V| - \mathrm{def}(M)\right) \le \min_{A \subseteq V} \frac{1}{2} \left(|V| - \mathrm{lc}(G - A) + |A|\right)\]
kde první nerovnost plyne z úvahy, že největší párování minimalizuje defekt a druhá z dosazení pozorování výše.
{% endmath %}

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
			- pokud je graf bipartitní, tak nemáme žádné \(B-B\) hrany a všechny zbývající hrany z \(B\)-vrcholů vedou do \(A\)-vrcholů -- poté když uvážíme \(G - A\), tak liché komponenty vedou pouze do \(A\) vrcholů ale \(B\) je o jedna více (máme \(r\)), tedy \(|B| = |A| + 1\) a \(G\) nemá perfektní párování a **našli jsme defektní vrchol**

Pro **bipartitní grafy** můžeme algoritmus výše opakovat (opakovaně stavíme stromy z vrcholů, které nejsou v párování), najít všechny defektní vrcholy a věta výše platí (máme množinu defektních vrcholů a párování splňující rovnost).

Pro **nebipartitní grafy** může existovat hrana mezi \(B-B\) vrcholy (lichá kružnice).

{% math observation %}nechť \(C\) lichá kružnice v \(G\), \(G'\) vznikne kontrakcí \(C\) do jednoho (pseudo)vrcholu a \(M'\) je párování v \(G'\). Potom existuje párování \(M\) v \(G\), že počet \(M'\)-nepokrytých vrcholů je stejný jako počet \(M\)-nepokrytých.
{% endmath %}

Podgrafy \(G\) reprezentované pseudovycholy mají lichý počet vrcholů (chceme opět dostat \(M\) a \(A\), abychom větu dokázali). To platí, protože pseudovrcholy vznikly kontrakcí liché kružnice na vrchol a tedy přišly o sudý počet vrcholů.

Postup pro \(B-B\) hrany je tedy ten, že zkontrahujeme \(C\), vyřešíme párování a odkontrahujeme.
{% endmath %}

{:.rightFloatBox}
<div markdown="1">
\(A\) může být i prázdné (eliminuje grafy s lichým počtem vrcholů).
</div>

{% math consequence "Tutte" %}\(G\) má perfektní párování právě tehdy, když \[\forall A \subseteq V: \mathrm{lc}(G - A) \le |A|\]{% endmath %}

{% math proof %}vychází přímo z Tutte-Berge dosazením \(|M| = |V|/2\) (jedná se  o perfektní párování).{% endmath %}

{% math theorem "Edmonds-Gallai dekompozice" %}\(G\) graf, \(G = (V, E)\), \(B \subseteq V\) vrcholů nepokrytých nějakým maximálním párovaním. Nechť \(A \subseteq V - B\) sousedé vrcholů z \(B\), \(C = V - \left(B \cup A\right)\). Pak
1. každá komponenta \(G - \left(A \cup C\right)\) je kritická (\(\forall v \in K: K - \left\{v\right\}\) má perfektní párování)
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

{% math observation %}\(|T|\) je sudé (součet stupňů je sudý){% endmath %}

{:.rightFloatBox}
<div markdown="1">
Je to taková množina vrcholů a hran, na kterou když se omezíme, tak všechny stupně vrcholů v \(T\) jsou liché a ostatní jsou sudé.
</div>

{% math definition "T-join" %}\(E' \subseteq E\) je \(T\)-join (pro množinu vrcholů \(T\)), pokud \(G_T = (V, E')\) platí \[\left(\forall v \in V\right) \left(\mathrm{deg}_{G_T} (v)\ \text{lichý} \iff v \in T\right)\]{% endmath %}

{% math theorem %}nechť \(E' \subseteq E\) je množina hran min. trasy čínského pošťáka, které se projdou více než jednou. Pak se projdou **právě \(2\)-krát** a \(E'\) je **min. \(T\)-join** (kde \(T\) je výše definovaná množina).{% endmath %}
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

### Spojitá optimalizace
Má [pěkná skripta](/assets/diskretni-a-spojita-optimalizace/spojita.pdf).

### Zkouška
Na obou částech jsem si vytáhl okruh, o kterém jsem napsal co vím a pak jsem to se zkoušejícím probíral.

#### Diskrétní část

**Zkušební okruhy:**
1. Matroidy: základní definice, příklady.
2. Řádová funkce a submodularita.
3. Kontrakce, dualita.
4. Hladový algoritmus.
5. Průnik matroidů, obraz, sjednocení.
6. Edmondsův algoritmus na maximální párování, Tuttova věta.
7. Problém Obchodního cestujícího a Čínského pošťáka.

#### Spojitá část
- z webových stránek přednášky: „Na zkoušce se probírá jen teorie.“

### Odkazy
- Web diskrétní části: [https://kam.mff.cuni.cz/~loebl/dsopt22.html](https://kam.mff.cuni.cz/~loebl/dsopt22.html)
- Web spojité části: [https://kam.mff.cuni.cz/~hladik/DSO/](https://kam.mff.cuni.cz/~hladik/DSO/)

### Poděkování
- Davidu Kubkovi za zápisky, ze kterých jsem první polovinu poznámek vytvářel (včetně obrázků).
