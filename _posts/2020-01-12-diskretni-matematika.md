---
language: cz
title: Diskrétní Matematika
category: "lecture notes"
pdf: true
---

- .
{:toc}

{% lecture_notes_preface Martina Mareše | 2019/2020 %}

### Relace
Definice: relace mezi množinami \(X, Y \equiv R \subseteq X \times Y\) (podmnožina kartézského součinu)

- prázdná: \(\emptyset\) (nic s ničím)
- univerzální: \(X \times Y\) (vše se vším)
- diagonální \(\Delta_X\): \(\left\{\left(x, x\right) \mid x \in X\right\}\)
	- matice relace má 1 na diagonále

- inverzní \(R^{-1}\): \(\left\{\left(y, x\right) \mid \left(x, y\right) \in R\right\}\)
	- pozor: nemusí to být funkce!

- složená: \(x \left(R \circ S\right) z \equiv\ \exists y \in Y: xRy \land ySz\)
	- tzn. tj. musí existovat cesta (když si to představíme jako grafy)

#### Funkce
Definice: relace \(f\) mezi \(X, Y\) je funkce (zobrazení) \(\ \equiv \forall x \in X \ \exists!\ y \in Y: x f y\)

- speciální druh relace, ve kterém se z \(X\) zobrazuje „jen jednou“	
- značíme \(f: X \mapsto Y\) nebo \(f\left(x\right) = y\)<br>

- **prostá:** \(\forall x, x' \in X, x \neq x': f\left(x\right) \neq f\left(x'\right)\)
- **na:** \( \forall y \in Y\ \exists x \in X: f\left(x\right) = y\)
	- na každé \(y\) se něco zobrazí (klidně vícekrát!)
- **bijekce:** \(\forall y \in Y\ \exists!\ x \in X: f\left(x\right) = y\)
- pozn.: podle definice jdou všechny prvky z \(X\) někam do \(Y\)!


#### Vlastnosti relace
- **reflexivní**: \(\equiv \forall x \in X: xRx\) 
	- diagonála
- **symetrická**: \(\equiv \forall x, y \in X: xRy \iff yRx\)
	- pozn.: \(R^{-1} = R\)
- **antisymetrická**: \(\forall x, y \in X, x \neq y: xRy \implies \neg yRx\)
	- alternativně: \(\forall x, y \in X: xRy \land yRx \implies x = y\) (je z toho lépe vidět diagonála)
	- např. menší než... musí to být pouze jedním směrem
- **tranzitivní**: \(\forall x,y,z \in X: xRy \land yRz \implies xRz\) 
	- hezky vidět na grafech, špatně na maticích

#### Ekvivalence
Relace \(R\) na \(X\) je ekvivalence \(\ \equiv R\) je **tranzitivní, reflexivní** a **symetrická**.

- ekvivalenční třída \(R\left[x\right]\) prvku \(x := \left\{y \in X \mid xRy \right\}\) (jsou spolu mezi sebou všechny v relaci)

Věta: Nechť \(R\) je ekvivalence na \(X\). Potom:
1. \(\forall x \in X: R[x] \neq \emptyset\)
	- vyplývá z reflexivity... \(x \in R\left[x\right]\)
2. \(\forall x, y \in X: \) buď \(R\left[x\right] = R\left[y\right] \) nebo \(R\left[x\right] \cap R\left[y\right] = \emptyset\)
	- pro \(R\left[x\right] \subseteq R\left[y\right]\): uvažme \(z \in R\left[x\right]\), tím pádem \(zRx\) (symetrie) a \(zRy\) (tranzitivita), proto i \(xRy\) a tedy \(z \in R\left[y\right]\) (pak stačí obrátit...)
	- \(xRy\) neplatí -- sporem dokážeme, že \(R\left[x\right] \cap R\left[y\right] = \emptyset\)... nechť existuje \(z \in R\left[x\right] \cap R\left[y\right]\); potom \(xRz\) a \(zRy\) (tranzitivita), a tedy \(xRy\), což je ↯
3. ekvivalenční třídy určují \(R\) jednoznačně
	- zřejmé... \(xRy\) právě když \(\left\{x, y\right\}\subseteq R\left[x\right]\)

#### Uspořádání
Relace \(R\) na \(X\) je uspořádání \(\ \equiv\ R\) je **reflexivní, antisymetrická** a **tranzitivní.**

- **lineární** \(\le\): \(\forall x, y \in X: x \le y \lor y \le x\) (všechny \(x, y\) jsou porovnatelné)
- **částečné** = ne lineární
- **ostré**: pokud \(\le\) je uspořádání, pak \(x < y \equiv x \le y \land x \neq y\) je ostré uspořádání
- \(\ge\ :=\ \le^{-1}\) je také uspořádání (to samé platí pro ostré)

##### Hasseův diagram
Uvažme uspořadání \(\left(\left\{1, 2, 3\right\}, \subseteq\right)\). Jeho Hasseův diagram bude vypadat následně:

{% xopp hasse %}

- spojujeme **bezprostřední předky**, tj.: neexistuje \(t \in X\) mezi \(x, y\) takové, že \(x < t < y\)<br>
- \(x\) je **minimální** (maximální) prvek \(\ \equiv \nexists\ y: y < x\)
	- tzn. _neexistuje menší_
- \(x\) je **nejmenší** (největší) prvek \(\ \equiv \forall y: x \le y\)
	- tzn. _je menší než všechny ostatní_
	- silnější kritérium než minimální, jelikož musí se všemi být porovnatelný
	- nejmenší je rovněž minimální

##### Lexikografické uspořádání
Nechť \(X\) je abeceda a \(\le\) uspořadání na \(X\). Pak:

\(\left(X^2, \le_{LEX}\right)\), \(\left(a, b\right) \le_{LEX} \left(a', b'\right) \equiv \left(a < a'\right) \lor \left(a = a' \land b \le b'\right)\)
- nejprve se rozhoduje podle prvního, pak podle druhého
- lze generalizovat pro více (kartézský součin) množin

#### Dlouhý a široký
Definice: pro \(\left(X, \le\right)\) ČUM: 
- \(A \subseteq X\) je _řetězec_ \(\forall a, b \in A\) jsou porovnatelné
	- \(\omega\left(X, \le\right) :=\) délka nejdelšího řetězce
- \(A \subseteq X\) je _antiřetězec_ \(\equiv\) žádné 2 prvky nejsou porovnatelné (nezávislá množina)
	- \(\alpha\left(X, \le\right) :=\) délka nejdelšího antiřetězce

Věta (o dlouhém a širokém): pro \(\left(X, \le\right)\) konečnou ČUM: \(\alpha \omega \ge \left|X\right|\)

Důkaz: 
- \(M_1 := \left\{a \in X \mid a\ \text{je minimální v}\ \le\right\}\)
- \(X_1 := X \setminus M_1\)
- pokračujeme a vyjde nám, že \(\forall i: \left|M_i\right|  \le \alpha\) (všechny totiž musí být nezávislé); rovněž \(\exists a_k \in M_k, a_{k - 1} \in M_{k - 1} \ldots\) řetězec \(\implies k \le \omega\)
	- kombinací dojdeme k nerovnosti \(\left|X\right| = \sum_{i = 1}^{k} \left|M_i\right| \le \alpha \omega\)

---

Věta (Erdős-Szekeres): nechť \(x_1, \ldots, x_{n^2 + 1}\) jsou navzájem různé. Pak existuje buď rostoucí nebo neklesající posloupnost délky alespoň \(n + 1\).

Důkaz: Na \(\left\{1, \ldots, n + 1\right\}\) definujme uspořádání \(i < j \iff i < j \land x_i < x_j\). Rostoucí odpovídají řetězcům, klesající antiřetězcům.


#### Segway do kombinatorického počítání
Věta: je-li \(A\) \(a\)-prvkové a \(B\) \(b\)-prvkové, pak počet \(f: A \mapsto B = b^a\)

Důkaz: každý prvek z \(A\) můžeme (podle definice dokonce musíme) poslat do libovolného prvku z \(B\). 

---

Věta: \(\left|2^X\right| = 2^{\left|X\right|}\)

Důkaz: pro \(Y \subseteq X\) zavedeme *charakteristickou funkci* \(C_Y: X \mapsto \left\{0, 1\right\}\), kde 

\[C_Y\left(x\right) \begin{cases} 1 & x \in Y \\ 0 & \text{jindy}\end{cases}\] 

Každá \(C_Y\) jasně určuje unikátní podmnožinu, tím pádem vlastně počítáme funkce z \(n\)-prvkové do \(2\)-prvkové množiny, kterých je \(2^n\) (viz předešlá věta). 

---

Věta: je-li \(A\) \(a\)-prvkové a \(B\) \(b\)-prvkové, pak počet \(f: A \mapsto B\) prostých je \[\prod_{i = 0}^{a - 1}\left(b - i\right) = b ^ {\underline{a}}\]
Důkaz: 1. prvek z \(a\) má \(b\) možností, druhý \(b - 1\), ...

---

Počítání dvojic: \(f: \left\{1, 2\right\} \mapsto X \equiv X^2\)
- prvky jsou dvojice \(\left(f\left(1\right), f\left(2\right)\right)\)
- \(\left\{1, \ldots, k\right\}\) -- uspořádání \(k\)-tice
- \(\mathbb{N} \mapsto X\) -- nekonečné posloupnosti prvků z \(X\)

Počet k-tic různých prvků z \(X\)... \(f: \left\{1, \ldots, k\right\} \mapsto X\) je \[n \cdot \left(n - 1\right) \cdot \left(n - 2\right) \cdot \ldots \cdot \left(n - k - 1\right)\]
- \(n = \left|X\right|\) (stejné jako počítání prostých funkcí)

Počet bijekcí mezi \(X\) a \(X\) (permutací) \(= n \cdot \left(n - 1\right) \cdot \ldots \cdot 1 := n!\) (faktoriál)

### Kombinatorika
- pár definic na rozjezd:

\[\binom{X}{k} := \left\{A \subseteq X \mid \left|A\right| = k\right\}\]

\[\binom{n}{k} := \frac{n \cdot \left(n - 1\right) \cdot \left(n - 2\right) \cdot \ldots \cdot \left(n - k + 1\right)}{k \cdot \left(k - 1\right) \cdot \left(k - 2\right) \cdot \ldots \cdot 2 \cdot 1} = \frac{n!}{k! \cdot \left(n - k\right)!}\]

Věta: \(\left|\binom{X}{k}\right| = \binom{\left|X\right|}{k}\)

Důkaz (počítání dvěma způsoby): 
- \# uspořádaných \(k\)-tic různých prvků z \(X\) je stejný jako:
	- \# prostých funkcí z \(\left\{1, \ldots, k\right\} \mapsto X\), kterých je \(n \cdot \left(n - 1\right) \cdot \ldots \cdot \left(n - k + 1\right)\)
	- \# \(k\)-prvkových množin \( \cdot k!\) (zpermutováním)... \(\left|\binom{X}{k}\right| \cdot k!\)

#### Vlastnosti kombinačních čísel:
- počet prázdných podmnožin \(= 1 =\) počet „plných“ podmnožin: \(\binom{n}{0} = 1 = \binom{n}{n}\)
- počet 1-prvkových podmnožin\( = n = \)počet podmnožin, kde 1 prvek chybí: \(\binom{n}{1} = n = \binom{n}{n - 1}\)
- generalizace předchozích dvou vzorečků... počítání doplňků: \(\binom{n}{k} = \binom{n}{n - k}\)
- počet podmnožin dané množiny: \(\sum_{k=0}^{n} \binom{n}{k} = 2^n\)
	- vlastně \(n\)-bitové číslo -- patří/nepatří

\[\binom{n}{k} = \binom{n - 1}{k} + \binom{n - 1}{k - 1}\]
- \(k\)-prvkové množiny obsahující/neobsahující \(n\)... když obsahují, tak máme zbylých \(k\) míst; když ne, tak \(k - 1\) (samotné \(n\) jedno zabírá)

#### Binomická věta
\[\forall n \in \mathbb{N}, \forall a, b \in \mathbb{R}: \left(a + b\right)^n = \sum_{k = 0}^{n} \binom{n}{k} a^{n - k}b^k\]

Důkaz:
- pro \(0\) funguje
- jedná se o _součty součinů_, které si ze závorek vybírají \(a\) nebo \(b\)
	- \(a^{n - k}b^k\) -- musí jich být \(n\)
	- \(\binom{n}{k}\) -- kolika způsoby si lze z \(n\) závorek vybrat k znaků

Zajímavosti:
- \(\left(1 + 1\right)^n = 2^n = \sum_{k = 0}^{n}\binom{n}{k}\) -- součet řady Pascalova trojúhelníka
- \(\left(1 - 1\right)^n = 0 = \sum_{k = 0}^{n}\binom{n}{k} \left(-1\right)^k\) -- počet podmnožin sudé velikosti je roven počtu podmnožin velikosti liché

#### Odhady pro faktoriál
- hloupý: \(2^{n - 1} \le n! \le n^n\)
- rozumný: \(n^{n / 2} \le n! \le \left(\frac{n + 1}{2}\right)^n\)
- wtf: \(e \cdot \left(\frac{n}{e}\right)^n \le n! \le en \cdot \left(\frac{n}{e}\right)^n\)

Lemma -- a/g nerovnost: \( \sqrt{xy} \le \frac{x + y}{2} \qquad  \forall x, y \ge 0\)

\[
\begin{aligned}
	\left(a - b\right)^2 &\ge 0 \\ 
	a^2 - 2ab + b^2 &\ge 0 \\ 
	a^2 + b^2 &\ge 2ab \\ 
	\frac{a^2 + b^2}{2} &\ge ab \\ 
	\frac{x + y}{2} &\ge \sqrt{xy}
\end{aligned}
\]

Důkaz rozumného:
- \(n! = \sqrt{\left(n!\right)^2} = \sqrt{1 \cdot 2 \cdot \ldots \cdot n \cdot 1 \cdot 2 \cdot \ldots \cdot n} = \sqrt{1 \cdot n} \cdot \sqrt{2 \cdot \left(n - 1\right)} \cdot \ldots \cdot \sqrt{n \cdot 1}\)
	- \(\sqrt{i \left(n - i + 1 \right)} \le^{\mathrm{AG}} \frac{i + n - i + 1}{2} = \left(\frac{n + 1}{2}\right)^n\) (je jich \(n\))
	- \(\sqrt{i \left(n - i + 1\right)} \ge \sqrt{n}^n\)... vevnitř je vždy alespoň \(n\)

Důkaz wtf (indukce):
- \(n = 1\)... \(e \cdot 1 \cdot \frac{1}{e} \le 1\)
- \(n - 1 \rightarrow n\):
\[\begin{aligned} n! = n \left(n - 1\right)! &\le^\mathrm{IP} en \left(n - 1\right) \left(\frac{n - 1}{e}\right)^{n - 1} \\ &= en \left(\frac{n}{e}\right)^n \left(\frac{e}{n}\right)^n \left(n - 1\right) \left(\frac{n - 1}{e}\right)^{n - 1} \\
&= en \left(\frac{n}{e}\right)^n \underbrace{\left(\frac{n - 1}{n}\right)^n e}_{\le 1}
\end{aligned}\]

Důkaz, toho proč ten výraz \(\le 1\):

\[
\begin{aligned} 
\left(1 - \frac{1}{n}\right)^n e &\le \left(e^{-\frac{1}{n}}\right)^n e = e^{-1} e = 1 \qquad 1 + x \le e^x
\end{aligned}
\]

- pozn.: \(a \le b \implies a = b c\) pro \(c \le 1\), proto to vlastně děláme

#### Princip inkluze/exkluze
Nechť \(A_1, \ldots, A_n\) jsou konečné množiny. Potom:
\[\left|\bigcup_{i = 0}^{n} A_i\right| = \sum_{k = 1}^{n} \left(-1\right)^{k + 1} \sum_{I \in \binom{\left[n\right]}{k}} \left|\bigcap_{i \in I} A_i\right|\]

Také lze zapsat jako
\[\left|\bigcup_{i = 0}^{n} A_i\right| = \sum_{\emptyset \neq I \subseteq \left[n\right]} \left(-1\right)^{\left|I\right| + 1} \left|\bigcap_{i \in I} A_i\right|\]

Důkaz (počítací) -- kolikrát se prvek \(x\) nachází nalevo a napravo:
- nalevo: 1 (ve sjednocení je jednou právě)
- napravo:
	- předpokládejme, že se vyskytne v \(j\) množinách -- vyskytuje se tedy v každé \(k\)-tici... (\(k \le j\))
	- existuje \(\binom{j}{k}\) \(k\)-prvkových podmnožin \(j\)-prvkové množiny (a ve vzorci se znaménka střídají), lze počet výskytů vyjádřit následovně:
\[j - \binom{j}{2} + \binom{j}{3} - \ldots + \left(-1\right)^{j - 1}\binom{j}{j} = 1\]

### Grafy
Definice: graf je _uspořádaná dvojice_ množin \(\left(V, E\right)\), kde \(V\) je _konečná, neprázdná_ množina vrcholů a \(E \subseteq \binom{V}{2}\) je množina hran.
- \(\left\{u, v\right\} \in E\)... mezi \(u, v\) vede hrana (jsou sousední)
- \(v \in e\) pro \(e \in E\)... vrchol leží v/na hraně

#### Odrudy
- **úplný** \(K_n \equiv \left(\left[n\right], \binom{V}{2}\right)\)
	- opak je **diskrétní**
- **úplný bipartitní** \(K_{m, n}\):
	- \(V\left(K_{m, n}\right) = \left\{a_1, \ldots, a_m, b_1, \ldots, b_n\right\}\) (rozdělíme na 2 části)
	- \(E\left(K_{m, n}\right) = \left\{\left\{a_i, b_j\right\} \mid i \in \left[m\right], j \in \left[n\right]\right\}\)
	- bipartitní -- \(E \subseteq\ \) úplného bipartitního
- **cesta** \(P_n \equiv \left(\left[n\right], \left\{\left\{i, i + 1\right\} \mid 0 \le i < n\right\}\right) \)
- **cyklus** \(C_n \equiv \left(\left[n\right], \left\{\left\{i, \left(i + 1\right)\ \mathrm{mod}\ n\right\} \mid 0 \le i \le n\right\}\right)\)

#### Izomorfismus
Definice: grafy \(G\) a \(H\) jsou **izomorfní** \(\left(G \cong H\right) \equiv f: V\left(G\right) \mapsto V\left(H\right)\) bijekce t. ž. \(\forall u, v \in V\left(G\right)\) platí: \(\left\{u, v\right\} \in E\left(G\right) \iff \left\{f\left(u\right), f\left(v\right)\right\} \in E\left(H\right)\)
- vlastně to je takové přejmenování vrcholů

#### Grafové odhady
Nechť \(V = \left\{v_1, \ldots, v_n\right\}\). 
- počet _všech_ grafů na \(V\) je \(2^{\binom{n}{2}}\) (všechny možné dvojice; buďto tam jsou nebo nejsou)
- počet _neizomorfních_ grafů: počet všech grafů / počet tříd izomorfismu (ekvivalence)
	- izomorfismů je nejvýše \(n!\) (uvažujeme všechna přejmenování)
	- celkem tedy \(\ge 2^\binom{n}{2} / n!\)
	- není to tak špatný odhad:

\[
\begin{aligned}
\log \frac{2^\binom{n}{2}}{n!}  &\ge \binom{n}{2} - n \log n \\
&= \frac{n \left(n - 1\right)}{2} - n \log n \\
& = \frac{n^2}{2} \left(1 - \frac{1}{n} - \frac{2 \cdot \log{2}{n}}{n}\right)
\end{aligned}
\]

#### Vlastnosti grafu
- **stupeň vrcholu** \(v\) grafu \(G\) je \(\mathrm{deg}_G\left(v\right) = \# w \in V(G): \left\{v, w\right\} \in E\left(G\right)\)
	- tzn. kolik hran vede do vrcholu
	- \(k\)-regulární graf: stupeň všech vrcholů je \(k\)
- **skóre grafu** je uspořádaná \(n\)-tice stupňů všech vrcholů
	- typicky \(d_1 \le d_2 \le \ldots \le d_n\)
	- \(0 \le d_i < n - 1\)

Lemma: \[\sum_{v \in V\left(G\right)} \mathrm{deg}\left(v\right) = 2 \cdot \left|E\left(G\right)\right|\]

Důkaz: nechť \(K\) je \(\left\{\left(v, e\right) \mid e \in E\left(G\right) \land v \in e\right\}\); pak \[\left|K\right| = 2 \cdot \left|E\left(G\right)\right| = \sum_{v} \mathrm{deg}(v)\]
- první rovnost platí, jelikož každá hrana přispěje 2x
- druhá rovnost platí, jelikož každý vrchol přispěje všemi hranami, které do něj jdou (tj. svým stupňem)
- vyplývá z toho _princip sudosti_: počet vrcholů lichého stupně je sudý (jinak by se to nesečetlo na sudé číslo

---

Věta (testování skóre): Nechť \(d_1 \le d_2 \le \ldots \le d_n\) posloupnost přirozených čísel. Pak \(d_1', d_2', \ldots d_{n - 1}' \) vznikne smazáním posledního prvku a odečtením \(1\) od \(d_n\) předchozích. Pak \(d_1 \le d_2 \le \ldots d_n\) je skórem grafu, když \(d_1', d_2', \ldots d_{n - 1}' \) je skórem grafu.

Důkaz:
- \(\Rightarrow\)... víme, že \(d_1', d_2', \ldots d_{n - 1}' \) je skórem grafu, stačí tedy přilepit vrchol a propojit ho patřičnými hranamy k existujícímu grafu:
	- \(V\left(G\right) = \left\{v_1', \ldots, v_{n - 1}', v_n\right\}\)
	- \(E\left(G\right) = E\left(G'\right) \cup \left\{\left\{v'i, v_n\right\} \mid n - d_n \le i \le n - 1\right\}\)
	- pozor! opačně nefunguje, jelikož nemáme jistotu, že odebíráme od těch zprava
- \(\Leftarrow\)...
	- Nechť \(\mathcal{G} := \left\{G\ \text{na}\ \left\{v_1, \ldots, v_n\right\}, \mid \forall i: \mathrm{deg}_G\left(v_i\right) = d_i\right\}\)
		- = všechny možné grafy se správným tím skórem
	- lemma: \(\exists\ G \in \mathcal{G}: \forall j, n - d_n \le j < n: \left\{v_j, v_n\right\} \in E\left(G\right)\) 
		- nechť \(j\left(G\right) := \mathrm{max}\left\{j \mid \left\{v_j, v_n\right\} \not\in E\left(G\right)\right\}\) (první díra zprava)

{% xopp score_1 %}
 
- nechť \(G \in \mathcal{G}\) má minimální \(j\left(G\right)\)... pak \(j < n - d_n\)
	- důkaz sporem: kdyby \(j \ge n - d_n\), pak \(\exists i\) a \(\exists k: \left\{v_j, v_k\right\} \in E\left(G\right) \land \left\{v_i, v_k\right\} \not\in E\left(G\right)	\)
		- pro \(d_i < d_j\) -- z \(v_j\) jich vede více než s \(d_i\) (takže do nějaké do které \(d_j\) vede \(d_i\) nevede)
		- \(d_i = d_j\) je taky ok... jedna z \(v_i\) vede do \(v_n\)

{% xopp score_2 %}

- škrtnutím vyrobíme graf, který má menší \(j\)... ↯

---

Graf \(H\) je _podgrafem_ grafu \(G \left(H \subseteq G\right) \equiv V\left(H\right) \subseteq V\left(G\right) \land E\left(H\right) \subseteq E\left(G\right)\).
- vznik tak, že z grafu odebíráme hrany/vrcholy

Graf \(H\) je _indukovaným podgrafem_ grafu \(G \left(H \subseteq G\right) \equiv V\left(H\right) \subseteq V\left(G\right) \land E\left(H\right) = E\left(G\right) \cup \binom{V\left(H\right)}{2}\).
- vznik tak, že z grafu odebíráme pouze vrcholy (a s nimi spojené hrany)

_Cesta_ v grafu délky \(k\) je (2 pohledy):
1. \(H \subseteq G\) t. ž. \(H \cong P_k\)
2. \(v_0, e_1, v_1, \ldots, e_k, v_k\) t. ž.:
	- \(\forall i: v_i \in V\left(G\right)\) + všechny \(v_i\) jsou různé vrcholy
	- \(\forall j: e_j \in E\left(G\right) \land e_j = \left\{v_{j - i}, v_j\right\}\)
- obdobně lze definovat kružnici, jen \(v_e = v_k\)

_Sled_ (procházka/walk) v grafu \(G\) je cesta, ve které se mohou vrcholy i hrany opakovat.

- lemma: pokud existuje sled z \(x\) do \(y\), pak existuje i cesta:
	- zvolíme nejkratší ze všech sledů... to je cesta; kdyby ne, pak \(\exists\) vrchol, který se tam vyskytuje 2x (tím pádem jde sled zkrátit)

---

Graf \(G\) je _souvislý_ (drží pohromadě) \(\ \equiv \forall u, v \in V\left(G\right) \exists\ \) cesta v \(G\) z \(u\) do \(v\)
- relace dosažitelnosti: \(\sim\) na \(V\left(G\right)\): \(u \sim v \equiv \exists\) cesta z \(u\) do \(v\)
	- je to ekvivalence: je _reflexivní_ (cesta z \(u\) do \(u\) velikosti 0), _symetrická_ (graf je neorientovaný) i _tranzitivní_ (jen pozor na to, že to po slepení může být sled -- je potřeba to ošetřit)

V souvislém grafu \(G\) je vzdálenost vrcholu \(u, v\) _minimum_ z delek cest z \(u\) do \(v\) (značíme \(\rho\left(u, v\right)\)).
- jedná se o _metriku_, jelikož splňuje následující:
	1. \(\forall u, v: \rho\left(u, v\right) \ge 0\) 
	2. \(\forall u, v: \rho\left(u, v\right) = 0 \iff u = v\) 
	3. \(\forall u, v: \rho\left(u, v\right) = \rho\left(v, u\right)\) 
	4. \(\forall u, v, w: \rho\left(u, v\right) \le \rho\left(u, w\right) + \rho\left(w, v\right)\) (trojúhelníková nerovnost)

---

#### Grafové operace
- _přidání_ hrany/vrcholu: \(G + v\), \(G + h\)
- _smazání_ hrany/vrcholu:
	- \(G - e := G\left(V, E \setminus \left\{e\right\}\right)\)
	- \(G - v := G\left(V \setminus v, E \setminus \left\{e \in E \mid v \not\in e\right\}\right)\)
- _dělení_ hrany \(G\ \%\ e := \left(V \cup \left\{z\right\}, \left(E \setminus \left\{x, y\right\}\right) \cup \left(\left\{x, z\right\}, \left\{z, y\right\}\right)\right)\)
- kontrakce hrany \( G/e := \left(\left(V \setminus \left\{x, y\right\}\right) \cup \left\{z\right\}, \\ \left\{e \in E \mid e \cap \left\{x, y\right\} \neq \emptyset\right\} \cup \left\{\left(e \setminus \left\{x, y\right\}\right) \cup \left\{z\right\} \mid e \in E \land \left|e \cup \left\{x, y\right\}\right| = 1\right\}\right) \)

#### Stromy
Základní definice:
- strom je _souvislý acyklický graf_
- les je _acyklický graf_ (soubor stromů)
- list -- vrchol stromu s \(\mathrm{deg}\left(v\right) = 1\)

##### Základní vlastnosti

Lemma: Strom s alespoň 2 vrcholy má alespoň 2 _listy_ (vrcholy, do kterých vede 1 hrana).

Důkaz: uvažme nejdelší cestu. Její krajní vrcholy jsou listy, jelikož:
- pokud z nich vede cesta někam zpět do sebe, tak graf není strom
- pokud z nich vede cesta někam, kde jsme ještě nebyli, tak není nejdelší

Lemma: nechť \(v\) je list grafu \(G\). Pak \(G\) je strom \(\iff G - v\) je strom.

Důkaz:
- \(\Rightarrow\)... \(G-v\) je acyklický (cyklus jsme odstraněním nevytvořili) a souvislý (vedla přes něj pouze 1 cesta, a to ta do něj)
- \(\Leftarrow\)... po přilepení je také souvislý ( \(\forall x \in G - v \exists\ \) cesta z \(x\) do \(v\)) a acyklický (přilepený vrchol má stupeň 1, nemůže tedy tvořit cyklus)

##### Charakteristika stromu
Následující tvrzení jsou ekvivalentní:
1. \(G\) je souvislý a acyklický (standardní)
2. mezi každými vrcholem \(x, y\) vede _právě 1 cesta_ (jsou jednoznačně souvislé)
3. \(G\) je souvislý a \(\forall e \in E\left(G\right): G - e\) souvislý není (je minimálně souvislý)
4. \(G\) je acyklický a \(\forall e \in \binom{V\left(G\right)}{2} \setminus E\left(G\right): G + e\) obsahuje cyklus (je maximálné acyklický... přidáním libovolné hrany se vytvoří cyklus)
5. \(G\) je souvislý a \(\left|E\left(G\right)\right| = \left|V\left(G\right)\right| - 1\) (Eulerova formule)

\(1 \implies 5\): indukcí:
- \(n = 1\) sedí (0 hran, 1 vrchol, je to strom)
- \(n \rightarrow n + 1\)... nechť \(G\) má \(n + 1\) vrcholů... 
	- \(G\) má list (lemma), jehož odtržením máme stále strom (\(G'\))... poštváním IP máme důkaz

\(1 \implies 2\): indukcí:
- \(n = 1\) platí
- po přilepení:
	- zachová všechny staré cesty
	- \(\forall x \in V\left(G - v\right) \exists!\) cesta \(x \sim s\) a \(\forall\) cesty \(x \sim v\) jsou tvaru \(x \sim s \sim v\) (jsou jednoznačné)

\(1 \implies 3\): indukcí:
- pro \(n = 2\) platí (odebráním hrany se vrcholy rozpadnou)
- indukce \(n + 1 \rightarrow n\):
	- IP: graf \(n\) se rozpadne
	- po odebrání \(n+1\) hrany se graf také rozpadne

\(1 \implies 4\): 
- acykličnost sedí
- přidáním hrany vytvoříme cyklus, jelikož tam již existuje cesta a tohle vytvoří druhou
	- pozor! neplést si s implikací \(4 \implies 1\); tohle _není spor_

\(2 \implies 1\): 
- je tím pádem souvislý
- kdyby existovala kružnice, pak existují 2 různé cesty

\(3 \implies 1\): 
- souvislost sedí
- kdyby existoval cyklus, tak se odstraněním nestane nesouvislý

\(4 \implies 1\): 
- acykličnost sedí
- kdyby nebyl souvislý, tak přidání nevytvoří cyklus

\(5 \implies 1\) -- indukcí podle počtu vrcholů: 
- existuje vrchol, který je list
- koukneme na skóre: \(\sum_{i = 1}^{n} d_i = 2 \cdot \left|E\left(G\right)\right| = 2n - 2\)
	- \(d_i \ge 1\) (souvislost) a alespoň 1 je 1 (kdyby ne, tak \(d_i > 1\), což je ale alespoň \(2n\)... máme list, jehož odtržením máme podle IP strom, a po přilepení je to také strom


#### Kostra, sled, tahy
_Kostra_ grafu \(G\) je graf \(H \subseteq G: V\left(H\right) = V\left(G\right) \land H\) je strom
- nesouvislý graf nemá kostru

_Tah_ je _sled_, ve kterém se neopakují hrany.
- _uzavřený/otevřený_ -- koncové vrcholy tahu jsou/nejsou stejné
- _Eulerovské_ -- obsahují všechny vrcholy a hrany grafu

Věta: v grafu \(G\) existuje _uzavřený Eulerovský tah_ \(\iff\) je souvislý a \(\forall\ v \in G: \mathrm{deg}\left(v\right)\) je sudý
- \(\Rightarrow\): je souvislý (všude se lze dostat tahem) i sudý (všechny hrany vedoucí do daného vrcholu lze spárovat, protože do něj vcházíme a vycházíme)
- \(\Leftarrow\): uvážíme _nejdelší možný tah:_
	- je _uzavřený_, jelikož kdyby nebyl, pak je počáteční i koncový vrchol tahu lichý, ale sudost znamená, že jsme nějaké hrany nevyužili... tah tedy není maximální
	- je _Eulerovský_, protože:
		- obsahuje všechny vrcholy; kdyby ne, tak jej lze připojit a vytvořit tak větší tah
		- obsahuje všechny hrany; víme, že obsahuje všechny vrcholy, proto je hrana mezi již nakreslenými vrcholy... tu ale lze také přidat
	- POZOR: je potřeba si dávat pozor na pořadí, ve kterém tuhle implikaci dokazuji -- záleží na něm

#### Rozšiřování grafů 
_Multigraf_ je uspořádaná trojice \(\left(V, E, K\right)\), kde:
- \(V\) jsou vrcholy ( \(V \neq \emptyset\))
- \(E\) jsou hrany
- \(K\) je zobrazení \(E \mapsto \binom{V}{2} \cup V\) (sjednocení kvůli existenci smyček)

_Orientovaný graf_ je \(\left(V, E\right)\), kde \(E \subseteq V^2 \setminus \Delta_V\) (lze u multigrafu rozšířit obdobně)
- hodí se rozlišovat vstupní (\(\mathrm{deg}^{\mathrm{in}}\)) a výstupní (\(\mathrm{deg}^{\mathrm{out}}\)) stupně

_Podkladový graf_:
- u orientovaného zapomeneme orientaci
- u multigrafu zrušíme opakování hran

Souvislost u grafů:
- _slabá_ -- dosažitelnost v podkladovém
- _silná_ -- \(\forall u, v \in V \exists\) cesta z  do \(v\)
 
Věta: pro _vyvážený_ orientovaný multigraf \(G\) je ekvivalentní:
1. \(G\) je slabě souvislý
2. \(G\) má uzavřený Eulerovský tah
3. \(G\) je silně souvislý

\(3 \implies 1\) již víme (podkladový je obecnější)

\(2 \implies 3\) tahem se dostaneme kdekoliv potřebujeme

\(1 \implies 2\) stejné jako důkaz u neorientovaného


#### Rovinné nakreslení grafu
- bod... prvek \(\mathbb{R}^2\)
- křivka... možina bodů; spojitá a prostá

{% xopp krivka %}

Definice: jednoduchá křivka (oblouk) je \(f: \left[0, 1\right] \mapsto \mathbb{R}^2\) spojitá a prostá.
- jednoduchá uzavřená křivka (kružnice): prostá až na \(f\left(0\right) = f\left(1\right)\)

Definice: _Rovinné nakreslení multigrafu_ \(\left(V, E, K\right)\): \(\nu V \mapsto \mathbb{R}^2\) a \(\left\{C_e \mid e \in E\right\}\) množina oblouků/topologických kružnic t. ž.:
1. \(\forall e \in E: K\left(e\right) = \left\{u, v\right\}\): \(C_e\) je oblouk s koncy \(\left\{\nu\left(u\right), \nu\left(v\right)\right\}\)
	- za každou hranu existuje oblouk
2. \(\forall e \in E: K\left(e\right) = u\): \(C_e\) je kružnice obsahující \(\nu\left(u\right)\)
	- smyčky
3. \(\forall e, f\) různé \(\in E: C_e \cap C_f = \nu\left[K\left(e\right) \cap K\left(f\right)\right]\)
	- průniky jsou jen vrcholy
4. \(\forall v \in V, \forall e \in E: \nu\left(v\right) \in C_e \implies v \in K\left(e\right)\)
	- protíná-li kružnice vrchol, pak je vrchol na té hraně

Graf je _rovinný_, pokud existuje nějaké jeho rovinné nakreslení.
- cesta je rovinná
- kružnice je rovinná
- strom je rovinný... indukcí (přidáváním listů), jelikož vždy se lze posunout alespoň o kousek dále

_Topologický_ graf -- graf nakreslený do roviny.

Jordanová věta: Nechť \(T\) je topologická kružnice v \(\mathbb{R}^2\). Pak \(\mathbb{R}^2 \setminus T\) má právě 2 komponenty obloukové souvislosti: 1 omezenou, 1 neomezenou a \(T\) je jejich společnou hranicní.
- těžké dokázat

---

Lemma: \(K_5\) není rovinná.

Důkaz: Po rovinném nakreslení \(K_4\) je zřejmé, že z každé stěny jsou dosažitelné právě 3 vrcholy -- \(K_5\) proto rovinná být nemůže.

---

Křížící číslo: min. počet křížení.

Stěny nakreslení: komponenty obloukové souvislosti \(\mathbb{R}^2 \setminus \left(\left\{\mu\left(v\right) \mid v \in V \right\} \bigcup_{e \in E} C(e)\right)\) 

{% xopp komponenty %}

- nechová se jako izomorfismus!

{% xopp komponenty2 %}

---

Věta: hranice každé stěny souvislého grafu je nakreslením uzavřeného sledu, který každou hranu obsahuje max 2x

Důkaz: indukce podle počtu hran (počet vrcholů je pevný):
1. pro strom: počet hran = počet vrcholů - 1; nakreslení má právě 1 stěnu; sled je DFS
2. pro \(\left|E\right| > \left|V\right| - 1\): obsahuje kružnici... nechť \(e = \left\{u, v\right\}\) leží na kružnici; rozdělíme ji na 2 sledy

---

Věta: \(G\) má nakreslení na sféru \(\iff G\) je rovinný.

Důkaz: uděláme _stereografickou projekci_... jedná se o bijekci
- pozor! je potřeba ji natočit tak, ať se netrefíme do grafu

{% xopp sfera %}

---

Věta (Kuratowského): \(G\) není rovinný \(\iff \exists H \cong G\) t. ž.: \(H \cong\) nějakému dělení \(K_5\) nebo \(K_{3, 3}\)

---

Věta (Eulerova formule): nechť \(G\) je souvislý graf nakreslený do roviny. Pak \(v + f = e + 2\)

Důkaz: fixujeme \(v\), indukce podle \(e\):
- graf je strom: \(e = v - 1; f =1\)... \(v + f = e + 2\)
- IK: uvažme \(h\) na kružnici a podívejme se na \(G - h\)
	- \(v' = v\)
	- \(e' = e - 1\) (odebrání hrany)
	- \(f' = f - 1\) (spojení dvou stěn)

---

Definice: \(G\) je maximálně rovinný \(\iff G\) je rovinný a \(G + e\) není rovinný \(\forall e \not\in E\left(G\right)\).

Věta: pro maximálné rovinný graf \(G\) s \(v \ge 3\) jsou všechny jeho stěny trojúhelníky.

Důkaz:
1. každý maximální graf je souvislý (pokud ne, tak lze nesouvislé komponenty spojit)
2. kdyby existovala stěna s hranicí \(C_n\) pro \(n > 3\), pak můžeme v rámci stěny přidat hranu
3. strana, jejíž hranice není kružnice neexistuje (mohli bychom přidat stěnu)

---

Věta: Nechť \(G\) je maximálně rovinný s \(v \ge 3\) vrcholy. Pak \(e = 3f / 2\).

Důkaz: Každá stěna je trojúhelník (\(3f\)) a patří právě do dvou stěn (\(/ 2\))... počítání dvěma způsoby.
- pozn.: můžeme dosadit do Eulerova vzorce (jelikož je zajisté souvislý) a dostaneme \(v + \frac{2}{3} e = e + 2 \implies e = 3v - 6\)
	- je z toho přímo vidět, že \(K_5\) není rovinná

---

Věta: v každém rovinném grafu existuje vrchol t. ž. \(\mathrm{deg}\left(v\right) \le 5\)

Důkaz:
- pro počet vrcholů \(\le 2\) triviální
- pro ostatní: \(e \le 3v - 6 \implies\) průměrný stupeň \(< 6\)
	- \(2e \le 6v - 12 \implies 2e < 6v \implies \frac{2e}{v} < 6\) (\(2e\) je součet všech stupňů)

---

Věta: Nechť \(G\) je maximálně rovinný vez trojúhelníků. Pak \(e \le 2v - 4\).

Důkaz: počítání dvěma způsoby: \(e \ge 4f / 2\) (každá hrana patří do dvou stěn, které jsou tvořeny \(\ge\) 4 hranami. Dosazením do Eulera dostaneme nerovnost.

#### Barvení
Obarvení grafu \(G\) \(k\) barvami je funkce \(C: V\left(G\right) \mapsto \left\{1, \ldots, k\right\}\) t. ž. \(\forall u, v \in V\left(G\right): \left\{u, v\right\} \in E\left(G\right) \implies C\left(u\right) \neq C\left(v\right)\)

Barevnost (chromatické číslo \(\chi\left(G\right)\)) je nejmenší \(k\) t. ž. existuje obarvení grafu \(G\) \(k\) barvami.
- motivace: přidělování bez konfliktů
- \(\chi\left(P_n\right) = 2\) (pro \(n > 0\))
- \(\chi\left(C_n\right) = \begin{cases} 2 & n\ \text{sudé} \\ 3 & n\ \text{liché} \end{cases}\)
- \(\chi\left(K_n\right) = n\)
- \(H \subseteq G \implies \chi\left(H\right) \le \chi\left(G\right)\)
- \(\chi\left(G\right) = 1 \iff G\) nemá hrany
- \(\chi\left(G\right) = 2 \iff G\) je bipartitní

---

Věta: pokud \(G\) nemá lichou kružnici, pak \(\chi\left(G\right) \le 2\).

Důkaz: graf je souvislý \(\implies\) má kostru \(T\). Nechť \(C\) je 2-obarvení \(T\). Pokud by \(C\) nebylo obarvením \(G\), pak \(\exists\) cesta sudé délky z vrcholu \(u\) do \(v\), jejíž propojením dostáváme lichý cyklus. 
- pozor Tome, kolize vzniká při _stejných_ barvách :)

---

Lemma: Je-li T strom s alespoň 2 vrcholy. pak \(\chi\left(T\right) = 2\)

Důkaz: zakořeníme a barvíme po vrstvách.

---

##### Degenerovanost
Definice: graf \(G\) je \(d\)-degenerovaný \(\equiv \forall H \subseteq G\ \exists v \in V\left(H\right): \mathrm{deg}_H\left(v\right) \le d\)
- pozor! neříká to, že \(\forall v \in V\left(G\right): \mathrm{deg}\left(v\right) \le 5\), jelikož podgrafy trhají vrcholy a hrany
- každý strom je 1-degenerovaný
- rovinné grafy jsou 5-degenerované (viz. důkaz kousek zpět -- stupně rovinných grafů)
- graf s max. stupněm \(\Delta\) je \(\Delta\)-degenerovaný
- obecně platí \(\chi\left(G\right) \le d + 1\)
	- důkaz indukcí: odstranění má obarvení a ke přidání zpět je potřeba alespoň 1 volná barva

{% xopp chi %}

---

Pro \(G\) _nakreslený do roviny_ definujeme \(G^*\) duální graf:
- ze stěny je vrchol (a obráceně)
- z hrany je hrana (bijekce)
- podle Eulerovy formule: \(v\) a \(f\) se _prohazuje_, \(e\) _zůstává_

{% xopp dual %}

_Klikovost_ \(\omega\left(G\right)\) je maximální \(k\) t. ž. \(G\) obsahuje \(K_k\).
- \(\chi\left(G\right) \ge \omega\left(G\right)\) (na \(K_k\) je potřeba \(k\) barev...


##### 5-obarvitelnost
Věta: každý rovinný graf je 5-obarvitelný.

Důkaz:
- pro \(\left|V\right| \le 5\) lze triviálně (prostě přiřadíme všechny barvy)
- indukcí: uvažme \(v \in V\left(G\right)\) s maximálním stupněm
	- pro \(\mathrm{deg}(v) \le 4\)... indukcí přiřadíme vrcholu zbylou barvu
	- \(\mathrm{deg}(v) > 5\) nenastane (vztah \(e = 3v - 6\))
	- pro \(\mathrm{deg}(v) = 5\): uvažme zeleno-červený podgaf vycházející z vrcholu \(a\)... pro ten mohou nastat dva případy:
		1. pokud \(c\) nepatří do podgrafu, tak prohodíme _všechny barvy v podgrafu_ a jedné se tím na problematickém vrcholu zbavíme
		2. pokud patří, tak uděláme totéž s vrcholy \(b\) a \(d\); oba případy najednou nastat nemohou, jelikož by se křížily v hraně (nelze -- poruší rovinnost) nebo ve vrcholu (nelze, ten už má barvu)

{% xopp 5-barevnost %}

### Pravděpodobnost
Diskrétní pravděpodobnostní prostor je \(\left(\Omega, P\right)\).
- \(\Omega\) je nejvýše spočetná množina _elementárních jevů_ (hod mincí/kostkou/...)
- \(P\) je funkce \(\Omega \mapsto \left[0, 1\right]\) („pravděpodobnost“) t. ž. \(\sum_{\omega \in \Omega} P(\omega) = 1\)
- klasický... \(\forall x, y \) el. jevy platí \(P\left(x\right) = P\left(y\right)\)

_Jev_ \(X\) je množina elementárních jevů.
- \(P\left[X\right] = \sum_{\omega \in X} P\left(\omega\right)\)
- \(P\left[\Omega\right] = 1\)
- \(P\left[\emptyset\right] = 0\)

#### Podmíněná pravděpodobnost
\[P\left[A \mid B\right] := \frac{P\left[A \cap B\right]}{P\left[B\right]}\] 
- podmínkou vytváříme novou množinu elementárních jevů, která ale není normalizovaná (to zajišťuje dělení)
- vlastně to po přepsání na \(P\left[A \mid B\right] \cdot P\left[B\right] = P\left[A \cap B\right]\) znamená: pravděpodobnost \(B\) krát pravděpodobnost, že v rámci \(B\) nastane \(A\) je šance jejich průniku (\(P\left[A \cap B\right]\)):

{% xopp podminena %}

Věta o úplné pravděpodobnosti: nechť \(B_1, \ldots, B_k\) je rozklad \(\Omega\) a \(\forall i: P\left[B_i\right] \neq 0\)
\[\forall A: P\left[A\right] = \sum_{i} \underbrace{P\left[A \mid B_i\right] \cdot P\left[B_i\right]}_{P\left[A \cap B_i\right]}\]

---

Věta (Bayesova): nechť \(B_1, \ldots, B_k\) je rozklad \(\Omega\) t. ž. \(\forall i: P\left[B_i\right] \neq 0\) a \(A\) je jev.

Potom \(\forall i\):

\[P\left[B_i \mid A\right] = \frac{P\left[A \mid B_i\right] \cdot P\left[B_i\right]}{\sum_{j} P\left[A \mid B_j\right] \cdot P\left[B_j\right]} = \frac{P\left[A \mid B_i\right] \cdot P\left[B_i\right]}{P\left[A\right]}\]

Důkaz (trochu pseudo): \[P\left[B_i \mid A\right] \cdot P\left[A\right] = P\left[A \cap B_i\right] = P\left[B_i \cap A\right] = P\left[A \mid B_i\right] \cdot P\left[B_i\right]\]

---

Definice: jevy \(A, B\) jsou nezávislé (\(B\) neovlivňuje \(A\)), pokud (ekvivalentní výroky):
1. \(P\left[A \mid B\right] = P\left[A\right]\) 
2. \(P\left[A \cap B\right] = P\left[A\right] \cdot P\left[B\right]\)

Obecněji: jevy \(A_1, \ldots, A_n\) jsou po \(k\) nezávislé \(\iff \forall I \in \binom{\left[n\right]}{k}: P\left[\bigcap_{i \in I} A_i\right] = \prod_{i \in I} P\left[A_i\right]\)
- jevy jsou nezávislé \(\iff\) jsou po \(k\) nezávislé \(\forall k\)

Definice: _součin pravděpodobnostních prostorů_ \(P\left(\Omega_1, P_1\right)\) a \(\left(\Omega_2, P_2\right)\) je pravděpodobnostní prostor \(\left(\Omega, P\right)\) t. ž.:
- \(\Omega := \Omega_1 \times \Omega_2\)
- \(P\left(\left(x_1, x_2\right)\right) = P_1\left(x_1\right) \cdot P_2\left(x_2\right)\)
- pozn.: stále se pravděpodobnost sečte na jedničku: \(\sum_{x1, x2} P_1\left(x_1\right) P_2\left(x_2\right) = 1 \cdot 1 = 1\)

Definice: _náhodná veličina_ je \(f: \Omega \mapsto \mathbb{R}\) (ale klidně i do jiné množiny... je to dost jedno)
- \(P\left[f \ge 7\right] = \left\{\omega \in \Omega \mid f\left(\omega\right) \ge 7\right\}\)
- _střední hodnota_ náhodné veličiny \(X\) je \(\mathbb{E}\left[X\right] := \sum_{\omega \in \Omega}X\left(\omega\right) \cdot P\left(\omega\right)\) 
- linearita střední hodnoty: \(\forall X, Y\) náhodné veličiny platí:
	- \(\mathbb{E}\left[X + Y\right] = \mathbb{E}\left[X\right] + \mathbb{E}\left[Y\right]\)
	- \(\mathbb{E}\left[\alpha X\right] = \alpha \mathbb{E}\left[X\right] \quad \forall \alpha \in \mathbb{R}\)
	- důkazy jsou přímočaré (dosazení do sumy)

Definice: _indikátor_ jevu \(J_i\left(\omega\right) = \begin{cases} 0 &\ \text{nenastal} \\ 1 &\ \text{nastal} \end{cases}\)
- \(J = \sum_{i} J_i\)

##### Pravděpodobnostní odhady
Věta (Markovova nerovnost): nechť \(X\) je náhodná _nezáporná_ veličina, která má střední hodnotu, a \(t \ge 1\); potom platí, že \[P\left[X \ge t \cdot \mathbb{E}\left[X\right]\right] \le \frac{1}{t}\]

Důkaz: vycházíme ze střední hodnoty; iterujeme přes všechna \(a \in R\)
\[
\begin{aligned}
	\mathbb{E}\left[x\right] &= \sum_{a} P\left[x = a\right] \cdot a \\ 
	&\ge \sum_{a \ge k} P\left[x = a\right] \cdot a  \\
	&\ge \sum_{a \ge k} P\left[x = a\right] \cdot k \\
	&= k \cdot \sum_{a \ge k} P\left[x = a\right] \\
	&= k \cdot P\left[x \ge k\right]
\end{aligned}
\]
- dalšími úpravami (viz. začátek předešlých) a dosazením \(k := t \cdot \mathbb{E}\left[x\right]\) dostáváme nerovnost

---

Definice: \(\mathrm{var}\ X\) (variace = rozptyl) \(:= \mathbb{E}\left[\left(X - \mathbb{E}\left[X\right]\right)^2\right]\)
- \(\sqrt{\mathrm{var}\ X}\) je _střední hodnota odchylky_

Věta (Čebyševova nerovnost): nechť \(X\) je náhodná veličina, která má střední hodnotu, a \(t \ge 1\); potom platí, že \[P\left[\left|X - \mathbb{E}\left[X\right]\right| \ge t \cdot \sqrt{\mathrm{var}\ X}\right] \le \frac{1}{t^2}\]
Důkaz: dosazení do Markovovy nerovnosti (jen pozor na odmocňování nerovnosti -- abs. hodnota).
