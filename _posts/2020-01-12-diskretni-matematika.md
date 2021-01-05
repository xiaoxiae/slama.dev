---
language: cz
title: Diskrétní Matematika
category: "lecture notes"
---

- .
{:toc}

### Úvodní informace
Tato stránka obsahuje moje poznámky z přednášky Martina Mareše z roku 2019/2020. Pokud by byla někde chyba/nejasnost, nebo byste rádi někam přidali obrázek/text, tak stránku můžete upravit [pull requestem](https://github.com/xiaoxiae/slama.dev/blob/master/_posts/) (případně mi dejte vědět, např. na mail).

### Relace
Definice: relace mezi množinami {% latex %}X, Y \equiv R \subseteq X \times Y{% endlatex %} (podmnožina kartézského součinu)

- prázdná: {% latex %}\emptyset{% endlatex %} (nic s ničím)
- univerzální: {% latex %}X \times Y{% endlatex %} (vše se vším)
- diagonální {% latex %}\Delta_X{% endlatex %}: {% latex %}\left\{\left(x, x\right) \mid x \in X\right\}{% endlatex %}
	- matice relace má 1 na diagonále

- inverzní {% latex %}R^{-1}{% endlatex %}: {% latex %}\left\{\left(y, x\right) \mid \left(x, y\right) \in R\right\}{% endlatex %}
	- pozor: nemusí to být funkce!

- složená: {% latex %}x \left(R \circ S\right) z \equiv\ \exists y \in Y: xRy \land ySz{% endlatex %}
	- tzn. tj. musí existovat cesta (když si to představíme jako grafy)

#### Funkce
Definice: relace {% latex %}f{% endlatex %} mezi {% latex %}X, Y{% endlatex %} je funkce (zobrazení) {% latex %}\ \equiv \forall x \in X \ \exists!\ y \in Y: x f y{% endlatex %}

- speciální druh relace, ve kterém se z {% latex %}X{% endlatex %} zobrazuje „jen jednou“	
- značíme {% latex %}f: X \mapsto Y{% endlatex %} nebo {% latex %}f\left(x\right) = y{% endlatex %}<br>

- **prostá:** {% latex %}\forall x, x' \in X, x \neq x': f\left(x\right) \neq f\left(x'\right){% endlatex %}
- **na:** {% latex %} \forall y \in Y\ \exists x \in X: f\left(x\right) = y{% endlatex %}
	- na každé {% latex %}y{% endlatex %} se něco zobrazí (klidně vícekrát!)
- **bijekce:** {% latex %}\forall y \in Y\ \exists!\ x \in X: f\left(x\right) = y{% endlatex %}
- pozn.: podle definice jdou všechny prvky z {% latex %}X{% endlatex %} někam do {% latex %}Y{% endlatex %}!


#### Vlastnosti relace
- **reflexivní**: {% latex %}\equiv \forall x \in X: xRx{% endlatex %} 
	- diagonála
- **symetrická**: {% latex %}\equiv \forall x, y \in X: xRy \iff yRx{% endlatex %}
	- pozn.: {% latex %}R^{-1} = R{% endlatex %}
- **antisymetrická**: {% latex %}\forall x, y \in X, x \neq y: xRy \implies \neg yRx{% endlatex %}
	- alternativně: {% latex %}\forall x, y \in X: xRy \land yRx \implies x = y{% endlatex %} (je z toho lépe vidět diagonála)
	- např. menší než... musí to být pouze jedním směrem
- **tranzitivní**: {% latex %}\forall x,y,z \in X: xRy \land yRz \implies xRz{% endlatex %} 
	- hezky vidět na grafech, špatně na maticích

#### Ekvivalence
Relace {% latex %}R{% endlatex %} na {% latex %}X{% endlatex %} je ekvivalence {% latex %}\ \equiv R{% endlatex %} je **tranzitivní, reflexivní** a **symetrická**.

- ekvivalenční třída {% latex %}R\left[x\right]{% endlatex %} prvku {% latex %}x := \left\{y \in X \mid xRy \right\}{% endlatex %} (jsou spolu mezi sebou všechny v relaci)

Věta: Nechť {% latex %}R{% endlatex %} je ekvivalence na {% latex %}X{% endlatex %}. Potom:
1. {% latex %}\forall x \in X: R[x] \neq \emptyset{% endlatex %}
	- vyplývá z reflexivity... {% latex %}x \in R\left[x\right]{% endlatex %}
2. {% latex %}\forall x, y \in X: {% endlatex %} buď {% latex %}R\left[x\right] = R\left[y\right] {% endlatex %} nebo {% latex %}R\left[x\right] \cap R\left[y\right] = \emptyset{% endlatex %}
	- pro {% latex %}R\left[x\right] \subseteq R\left[y\right]{% endlatex %}: uvažme {% latex %}z \in R\left[x\right]{% endlatex %}, tím pádem {% latex %}zRx{% endlatex %} (symetrie) a {% latex %}zRy{% endlatex %} (tranzitivita), proto i {% latex %}xRy{% endlatex %} a tedy {% latex %}z \in R\left[y\right]{% endlatex %} (pak stačí obrátit...)
	- {% latex %}xRy{% endlatex %} neplatí -- sporem dokážeme, že {% latex %}R\left[x\right] \cap R\left[y\right] = \emptyset{% endlatex %}... nechť existuje {% latex %}z \in R\left[x\right] \cap R\left[y\right]{% endlatex %}; potom {% latex %}xRz{% endlatex %} a {% latex %}zRy{% endlatex %} (tranzitivita), a tedy {% latex %}xRy{% endlatex %}, což je ↯
3. ekvivalenční třídy určují {% latex %}R{% endlatex %} jednoznačně
	- zřejmé... {% latex %}xRy{% endlatex %} právě když {% latex %}\left\{x, y\right\}\subseteq R\left[x\right]{% endlatex %}

#### Uspořádání
Relace {% latex %}R{% endlatex %} na {% latex %}X{% endlatex %} je uspořádání {% latex %}\ \equiv\ R{% endlatex %} je **reflexivní, antisymetrická** a **tranzitivní.**

- **lineární** {% latex %}\le{% endlatex %}: {% latex %}\forall x, y \in X: x \le y \lor y \le x{% endlatex %} (všechny {% latex %}x, y{% endlatex %} jsou porovnatelné)
- **částečné** = ne lineární
- **ostré**: pokud {% latex %}\le{% endlatex %} je uspořádání, pak {% latex %}x < y \equiv x \le y \land x \neq y{% endlatex %} je ostré uspořádání
- {% latex %}\ge\ :=\ \le^{-1}{% endlatex %} je také uspořádání (to samé platí pro ostré)

##### Hasseův diagram
Uvažme uspořadání {% latex %}\left(\left\{1, 2, 3\right\}, \subseteq\right){% endlatex %}. Jeho Hasseův diagram bude vypadat následně:

{% xopp hasse %}

- spojujeme **bezprostřední předky**, tj.: neexistuje {% latex %}t \in X{% endlatex %} mezi {% latex %}x, y{% endlatex %} takové, že {% latex %}x < t < y{% endlatex %}<br>
- {% latex %}x{% endlatex %} je **minimální** (maximální) prvek {% latex %}\ \equiv \nexists\ y: y < x{% endlatex %}
	- tzn. _neexistuje menší_
- {% latex %}x{% endlatex %} je **nejmenší** (největší) prvek {% latex %}\ \equiv \forall y: x \le y{% endlatex %}
	- tzn. _je menší než všechny ostatní_
	- silnější kritérium než minimální, jelikož musí se všemi být porovnatelný
	- nejmenší je rovněž minimální

##### Lexikografické uspořádání
Nechť {% latex %}X{% endlatex %} je abeceda a {% latex %}\le{% endlatex %} uspořadání na {% latex %}X{% endlatex %}. Pak:

{% latex %}\left(X^2, \le_{LEX}\right){% endlatex %}, {% latex %}\left(a, b\right) \le_{LEX} \left(a', b'\right) \equiv \left(a < a'\right) \lor \left(a = a' \land b \le b'\right){% endlatex %}
- nejprve se rozhoduje podle prvního, pak podle druhého
- lze generalizovat pro více (kartézský součin) množin

#### Dlouhý a široký
Definice: pro {% latex %}\left(X, \le\right){% endlatex %} ČUM: 
- {% latex %}A \subseteq X{% endlatex %} je _řetězec_ {% latex %}\forall a, b \in A{% endlatex %} jsou porovnatelné
	- {% latex %}\omega\left(X, \le\right) :={% endlatex %} délka nejdelšího řetězce
- {% latex %}A \subseteq X{% endlatex %} je _antiřetězec_ {% latex %}\equiv{% endlatex %} žádné 2 prvky nejsou porovnatelné (nezávislá množina)
	- {% latex %}\alpha\left(X, \le\right) :={% endlatex %} délka nejdelšího antiřetězce

Věta (o dlouhém a širokém): pro {% latex %}\left(X, \le\right){% endlatex %} konečnou ČUM: {% latex %}\alpha \omega \ge \left|X\right|{% endlatex %}

Důkaz: 
- {% latex %}M_1 := \left\{a \in X \mid a\ \text{je minimální v}\ \le\right\}{% endlatex %}
- {% latex %}X_1 := X \setminus M_1{% endlatex %}
- pokračujeme a vyjde nám, že {% latex %}\forall i: \left|M_i\right|  \le \alpha{% endlatex %} (všechny totiž musí být nezávislé); rovněž {% latex %}\exists a_k \in M_k, a_{k - 1} \in M_{k - 1} \ldots{% endlatex %} řetězec {% latex %}\implies k \le \omega{% endlatex %}
	- kombinací dojdeme k nerovnosti {% latex %}\left|X\right| = \sum_{i = 1}^{k} \left|M_i\right| \le \alpha \omega{% endlatex %}

---

Věta (Erdős-Szekeres): nechť {% latex %}x_1, \ldots, x_{n^2 + 1}{% endlatex %} jsou navzájem různé. Pak existuje buď rostoucí nebo neklesající posloupnost délky alespoň {% latex %}n + 1{% endlatex %}.

Důkaz: Na {% latex %}\left\{1, \ldots, n + 1\right\}{% endlatex %} definujme uspořádání {% latex %}i < j \iff i < j \land x_i < x_j{% endlatex %}. Rostoucí odpovídají řetězcům, klesající antiřetězcům.


#### Segway do kombinatorického počítání
Věta: je-li {% latex %}A{% endlatex %} {% latex %}a{% endlatex %}-prvkové a {% latex %}B{% endlatex %} {% latex %}b{% endlatex %}-prvkové, pak počet {% latex %}f: A \mapsto B = b^a{% endlatex %}

Důkaz: každý prvek z {% latex %}A{% endlatex %} můžeme (podle definice dokonce musíme) poslat do libovolného prvku z {% latex %}B{% endlatex %}. 

---

Věta: {% latex %}\left|2^X\right| = 2^{\left|X\right|}{% endlatex %}

Důkaz: pro {% latex %}Y \subseteq X{% endlatex %} zavedeme *charakteristickou funkci* {% latex %}C_Y: X \mapsto \left\{0, 1\right\}{% endlatex %}, kde 

{% latex display %}C_Y\left(x\right) \begin{cases} 1 & x \in Y \\ 0 & \text{jindy}\end{cases}{% endlatex %} 

Každá {% latex %}C_Y{% endlatex %} jasně určuje unikátní podmnožinu, tím pádem vlastně počítáme funkce z {% latex %}n{% endlatex %}-prvkové do {% latex %}2{% endlatex %}-prvkové množiny, kterých je {% latex %}2^n{% endlatex %} (viz předešlá věta). 

---

Věta: je-li {% latex %}A{% endlatex %} {% latex %}a{% endlatex %}-prvkové a {% latex %}B{% endlatex %} {% latex %}b{% endlatex %}-prvkové, pak počet {% latex %}f: A \mapsto B{% endlatex %} prostých je {% latex display %}\prod_{i = 0}^{a - 1}\left(b - i\right) = b ^ {\underline{a}}{% endlatex %}
Důkaz: 1. prvek z {% latex %}a{% endlatex %} má {% latex %}b{% endlatex %} možností, druhý {% latex %}b - 1{% endlatex %}, ...

---

Počítání dvojic: {% latex %}f: \left\{1, 2\right\} \mapsto X \equiv X^2{% endlatex %}
- prvky jsou dvojice {% latex %}\left(f\left(1\right), f\left(2\right)\right){% endlatex %}
- {% latex %}\left\{1, \ldots, k\right\}{% endlatex %} -- uspořádání {% latex %}k{% endlatex %}-tice
- {% latex %}\mathbb{N} \mapsto X{% endlatex %} -- nekonečné posloupnosti prvků z {% latex %}X{% endlatex %}

Počet k-tic různých prvků z {% latex %}X{% endlatex %}... {% latex %}f: \left\{1, \ldots, k\right\} \mapsto X{% endlatex %} je {% latex display %}n \cdot \left(n - 1\right) \cdot \left(n - 2\right) \cdot \ldots \cdot \left(n - k - 1\right){% endlatex %}
- {% latex %}n = \left|X\right|{% endlatex %} (stejné jako počítání prostých funkcí)

Počet bijekcí mezi {% latex %}X{% endlatex %} a {% latex %}X{% endlatex %} (permutací) {% latex %}= n \cdot \left(n - 1\right) \cdot \ldots \cdot 1 := n!{% endlatex %} (faktoriál)

### Kombinatorika
- pár definic na rozjezd:

{% latex display %}\binom{X}{k} := \left\{A \subseteq X \mid \left|A\right| = k\right\}{% endlatex %}

{% latex display %}\binom{n}{k} := \frac{n \cdot \left(n - 1\right) \cdot \left(n - 2\right) \cdot \ldots \cdot \left(n - k + 1\right)}{k \cdot \left(k - 1\right) \cdot \left(k - 2\right) \cdot \ldots \cdot 2 \cdot 1} = \frac{n!}{k! \cdot \left(n - k\right)!}{% endlatex %}

Věta: {% latex %}\left|\binom{X}{k}\right| = \binom{\left|X\right|}{k}{% endlatex %}

Důkaz (počítání dvěma způsoby): 
- \# uspořádaných {% latex %}k{% endlatex %}-tic různých prvků z {% latex %}X{% endlatex %} je stejný jako:
	- \# prostých funkcí z {% latex %}\left\{1, \ldots, k\right\} \mapsto X{% endlatex %}, kterých je {% latex %}n \cdot \left(n - 1\right) \cdot \ldots \cdot \left(n - k + 1\right){% endlatex %}
	- \# {% latex %}k{% endlatex %}-prvkových množin {% latex %} \cdot k!{% endlatex %} (zpermutováním)... {% latex %}\left|\binom{X}{k}\right| \cdot k!{% endlatex %}

#### Vlastnosti kombinačních čísel:
- počet prázdných podmnožin {% latex %}= 1 ={% endlatex %} počet „plných“ podmnožin: {% latex %}\binom{n}{0} = 1 = \binom{n}{n}{% endlatex %}
- počet 1-prvkových podmnožin{% latex %} = n = {% endlatex %}počet podmnožin, kde 1 prvek chybí: {% latex %}\binom{n}{1} = n = \binom{n}{n - 1}{% endlatex %}
- generalizace předchozích dvou vzorečků... počítání doplňků: {% latex %}\binom{n}{k} = \binom{n}{n - k}{% endlatex %}
- počet podmnožin dané množiny: {% latex %}\sum_{k=0}^{n} \binom{n}{k} = 2^n{% endlatex %}
	- vlastně {% latex %}n{% endlatex %}-bitové číslo -- patří/nepatří

{% latex display %}\binom{n}{k} = \binom{n - 1}{k} + \binom{n - 1}{k - 1}{% endlatex %}
- {% latex %}k{% endlatex %}-prvkové množiny obsahující/neobsahující {% latex %}n{% endlatex %}... když obsahují, tak máme zbylých {% latex %}k{% endlatex %} míst; když ne, tak {% latex %}k - 1{% endlatex %} (samotné {% latex %}n{% endlatex %} jedno zabírá)

#### Binomická věta
{% latex display %}\forall n \in \mathbb{N}, \forall a, b \in \mathbb{R}: \left(a + b\right)^n = \sum_{k = 0}^{n} \binom{n}{k} a^{n - k}b^k{% endlatex %}

Důkaz:
- pro {% latex %}0{% endlatex %} funguje
- jedná se o _součty součinů_, které si ze závorek vybírají {% latex %}a{% endlatex %} nebo {% latex %}b{% endlatex %}
	- {% latex %}a^{n - k}b^k{% endlatex %} -- musí jich být {% latex %}n{% endlatex %}
	- {% latex %}\binom{n}{k}{% endlatex %} -- kolika způsoby si lze z {% latex %}n{% endlatex %} závorek vybrat k znaků

Zajímavosti:
- {% latex %}\left(1 + 1\right)^n = 2^n = \sum_{k = 0}^{n}\binom{n}{k}{% endlatex %} -- součet řady Pascalova trojúhelníka
- {% latex %}\left(1 - 1\right)^n = 0 = \sum_{k = 0}^{n}\binom{n}{k} \left(-1\right)^k{% endlatex %} -- počet podmnožin sudé velikosti je roven počtu podmnožin velikosti liché

#### Odhady pro faktoriál
- hloupý: {% latex %}2^{n - 1} \le n! \le n^n{% endlatex %}
- rozumný: {% latex %}n^{n / 2} \le n! \le \left(\frac{n + 1}{2}\right)^n{% endlatex %}
- wtf: {% latex %}e \cdot \left(\frac{n}{e}\right)^n \le n! \le en \cdot \left(\frac{n}{e}\right)^n{% endlatex %}

Lemma -- a/g nerovnost: {% latex %} \sqrt{xy} \le \frac{x + y}{2} \qquad  \forall x, y \ge 0{% endlatex %}

{% latex display %}
\begin{aligned}
	\left(a - b\right)^2 &\ge 0 \\ 
	a^2 - 2ab + b^2 &\ge 0 \\ 
	a^2 + b^2 &\ge 2ab \\ 
	\frac{a^2 + b^2}{2} &\ge ab \\ 
	\frac{x + y}{2} &\ge \sqrt{xy}
\end{aligned}
{% endlatex %}

Důkaz rozumného:
- {% latex %}n! = \sqrt{\left(n!\right)^2} = \sqrt{1 \cdot 2 \cdot \ldots \cdot n \cdot 1 \cdot 2 \cdot \ldots \cdot n} = \sqrt{1 \cdot n} \cdot \sqrt{2 \cdot \left(n - 1\right)} \cdot \ldots \cdot \sqrt{n \cdot 1}{% endlatex %}
	- {% latex %}\sqrt{i \left(n - i + 1 \right)} \le^{\mathrm{AG}} \frac{i + n - i + 1}{2} = \left(\frac{n + 1}{2}\right)^n{% endlatex %} (je jich {% latex %}n{% endlatex %})
	- {% latex %}\sqrt{i \left(n - i + 1\right)} \ge \sqrt{n}^n{% endlatex %}... vevnitř je vždy alespoň {% latex %}n{% endlatex %}

Důkaz wtf (indukce):
- {% latex %}n = 1{% endlatex %}... {% latex %}e \cdot 1 \cdot \frac{1}{e} \le 1{% endlatex %}
- {% latex %}n - 1 \rightarrow n{% endlatex %}:
{% latex display %}\begin{aligned} n! = n \left(n - 1\right)! &\le^\mathrm{IP} en \left(n - 1\right) \left(\frac{n - 1}{e}\right)^{n - 1} \\ &= en \left(\frac{n}{e}\right)^n \left(\frac{e}{n}\right)^n \left(n - 1\right) \left(\frac{n - 1}{e}\right)^{n - 1} \\
&= en \left(\frac{n}{e}\right)^n \underbrace{\left(\frac{n - 1}{n}\right)^n e}_{\le 1}
\end{aligned}{% endlatex %}

Důkaz, toho proč ten výraz {% latex %}\le 1{% endlatex %}:

{% latex display %}
\begin{aligned} 
\left(1 - \frac{1}{n}\right)^n e &\le \left(e^{-\frac{1}{n}}\right)^n e = e^{-1} e = 1 \qquad 1 + x \le e^x
\end{aligned}
{% endlatex %}

- pozn.: {% latex %}a \le b \implies a = b c{% endlatex %} pro {% latex %}c \le 1{% endlatex %}, proto to vlastně děláme

#### Princip inkluze/exkluze
Nechť {% latex %}A_1, \ldots, A_n{% endlatex %} jsou konečné množiny. Potom:
{% latex display %}\left|\bigcup_{i = 0}^{n} A_i\right| = \sum_{k = 1}^{n} \left(-1\right)^{k + 1} \sum_{I \in \binom{\left[n\right]}{k}} \left|\bigcap_{i \in I} A_i\right|{% endlatex %}

Také lze zapsat jako
{% latex display %}\left|\bigcup_{i = 0}^{n} A_i\right| = \sum_{\emptyset \neq I \subseteq \left[n\right]} \left(-1\right)^{\left|I\right| + 1} \left|\bigcap_{i \in I} A_i\right|{% endlatex %}

Důkaz (počítací) -- kolikrát se prvek {% latex %}x{% endlatex %} nachází nalevo a napravo:
- nalevo: 1 (ve sjednocení je jednou právě)
- napravo:
	- předpokládejme, že se vyskytne v {% latex %}j{% endlatex %} množinách -- vyskytuje se tedy v každé {% latex %}k{% endlatex %}-tici... ({% latex %}k \le j{% endlatex %})
	- existuje {% latex %}\binom{j}{k}{% endlatex %} {% latex %}k{% endlatex %}-prvkových podmnožin {% latex %}j{% endlatex %}-prvkové množiny (a ve vzorci se znaménka střídají), lze počet výskytů vyjádřit následovně:
{% latex display %}j - \binom{j}{2} + \binom{j}{3} - \ldots + \left(-1\right)^{j - 1}\binom{j}{j} = 1{% endlatex %}

### Grafy
Definice: graf je _uspořádaná dvojice_ množin {% latex %}\left(V, E\right){% endlatex %}, kde {% latex %}V{% endlatex %} je _konečná, neprázdná_ množina vrcholů a {% latex %}E \subseteq \binom{V}{2}{% endlatex %} je množina hran.
- {% latex %}\left\{u, v\right\} \in E{% endlatex %}... mezi {% latex %}u, v{% endlatex %} vede hrana (jsou sousední)
- {% latex %}v \in e{% endlatex %} pro {% latex %}e \in E{% endlatex %}... vrchol leží v/na hraně

#### Odrudy
- **úplný** {% latex %}K_n \equiv \left(\left[n\right], \binom{V}{2}\right){% endlatex %}
	- opak je **diskrétní**
- **úplný bipartitní** {% latex %}K_{m, n}{% endlatex %}:
	- {% latex %}V\left(K_{m, n}\right) = \left\{a_1, \ldots, a_m, b_1, \ldots, b_n\right\}{% endlatex %} (rozdělíme na 2 části)
	- {% latex %}E\left(K_{m, n}\right) = \left\{\left\{a_i, b_j\right\} \mid i \in \left[m\right], j \in \left[n\right]\right\}{% endlatex %}
	- bipartitní -- {% latex %}E \subseteq\ {% endlatex %} úplného bipartitního
- **cesta** {% latex %}P_n \equiv \left(\left[n\right], \left\{\left\{i, i + 1\right\} \mid 0 \le i < n\right\}\right) {% endlatex %}
- **cyklus** {% latex %}C_n \equiv \left(\left[n\right], \left\{\left\{i, \left(i + 1\right)\ \mathrm{mod}\ n\right\} \mid 0 \le i \le n\right\}\right){% endlatex %}

#### Izomorfismus
Definice: grafy {% latex %}G{% endlatex %} a {% latex %}H{% endlatex %} jsou **izomorfní** {% latex %}\left(G \cong H\right) \equiv f: V\left(G\right) \mapsto V\left(H\right){% endlatex %} bijekce t. ž. {% latex %}\forall u, v \in V\left(G\right){% endlatex %} platí: {% latex %}\left\{u, v\right\} \in E\left(G\right) \iff \left\{f\left(u\right), f\left(v\right)\right\} \in E\left(H\right){% endlatex %}
- vlastně to je takové přejmenování vrcholů

#### Grafové odhady
Nechť {% latex %}V = \left\{v_1, \ldots, v_n\right\}{% endlatex %}. 
- počet _všech_ grafů na {% latex %}V{% endlatex %} je {% latex %}2^{\binom{n}{2}}{% endlatex %} (všechny možné dvojice; buďto tam jsou nebo nejsou)
- počet _neizomorfních_ grafů: počet všech grafů / počet tříd izomorfismu (ekvivalence)
	- izomorfismů je nejvýše {% latex %}n!{% endlatex %} (uvažujeme všechna přejmenování)
	- celkem tedy {% latex %}\ge 2^\binom{n}{2} / n!{% endlatex %}
	- není to tak špatný odhad:

{% latex display %}
\begin{aligned}
\log \frac{2^\binom{n}{2}}{n!}  &\ge \binom{n}{2} - n \log n \\
&= \frac{n \left(n - 1\right)}{2} - n \log n \\
& = \frac{n^2}{2} \left(1 - \frac{1}{n} - \frac{2 \cdot \log{2}{n}}{n}\right)
\end{aligned}
{% endlatex %}

#### Vlastnosti grafu
- **stupeň vrcholu** {% latex %}v{% endlatex %} grafu {% latex %}G{% endlatex %} je {% latex %}\mathrm{deg}_G\left(v\right) = \# w \in V(G): \left\{v, w\right\} \in E\left(G\right){% endlatex %}
	- tzn. kolik hran vede do vrcholu
	- {% latex %}k{% endlatex %}-regulární graf: stupeň všech vrcholů je {% latex %}k{% endlatex %}
- **skóre grafu** je uspořádaná {% latex %}n{% endlatex %}-tice stupňů všech vrcholů
	- typicky {% latex %}d_1 \le d_2 \le \ldots \le d_n{% endlatex %}
	- {% latex %}0 \le d_i < n - 1{% endlatex %}

Lemma: {% latex display %}\sum_{v \in V\left(G\right)} \mathrm{deg}\left(v\right) = 2 \cdot \left|E\left(G\right)\right|{% endlatex %}

Důkaz: nechť {% latex %}K{% endlatex %} je {% latex %}\left\{\left(v, e\right) \mid e \in E\left(G\right) \land v \in e\right\}{% endlatex %}; pak {% latex display %}\left|K\right| = 2 \cdot \left|E\left(G\right)\right| = \sum_{v} \mathrm{deg}(v){% endlatex %}
- první rovnost platí, jelikož každá hrana přispěje 2x
- druhá rovnost platí, jelikož každý vrchol přispěje všemi hranami, které do něj jdou (tj. svým stupňem)
- vyplývá z toho _princip sudosti_: počet vrcholů lichého stupně je sudý (jinak by se to nesečetlo na sudé číslo

---

Věta (testování skóre): Nechť {% latex %}d_1 \le d_2 \le \ldots \le d_n{% endlatex %} posloupnost přirozených čísel. Pak {% latex %}d_1', d_2', \ldots d_{n - 1}' {% endlatex %} vznikne smazáním posledního prvku a odečtením {% latex %}1{% endlatex %} od {% latex %}d_n{% endlatex %} předchozích. Pak {% latex %}d_1 \le d_2 \le \ldots d_n{% endlatex %} je skórem grafu, když {% latex %}d_1', d_2', \ldots d_{n - 1}' {% endlatex %} je skórem grafu.

Důkaz:
- {% latex %}\Rightarrow{% endlatex %}... víme, že {% latex %}d_1', d_2', \ldots d_{n - 1}' {% endlatex %} je skórem grafu, stačí tedy přilepit vrchol a propojit ho patřičnými hranamy k existujícímu grafu:
	- {% latex %}V\left(G\right) = \left\{v_1', \ldots, v_{n - 1}', v_n\right\}{% endlatex %}
	- {% latex %}E\left(G\right) = E\left(G'\right) \cup \left\{\left\{v'i, v_n\right\} \mid n - d_n \le i \le n - 1\right\}{% endlatex %}
	- pozor! opačně nefunguje, jelikož nemáme jistotu, že odebíráme od těch zprava
- {% latex %}\Leftarrow{% endlatex %}...
	- Nechť {% latex %}\mathcal{G} := \left\{G\ \text{na}\ \left\{v_1, \ldots, v_n\right\}, \mid \forall i: \mathrm{deg}_G\left(v_i\right) = d_i\right\}{% endlatex %}
		- = všechny možné grafy se správným tím skórem
	- lemma: {% latex %}\exists\ G \in \mathcal{G}: \forall j, n - d_n \le j < n: \left\{v_j, v_n\right\} \in E\left(G\right){% endlatex %} 
		- nechť {% latex %}j\left(G\right) := \mathrm{max}\left\{j \mid \left\{v_j, v_n\right\} \not\in E\left(G\right)\right\}{% endlatex %} (první díra zprava)

{% xopp score_1 %}
 
- nechť {% latex %}G \in \mathcal{G}{% endlatex %} má minimální {% latex %}j\left(G\right){% endlatex %}... pak {% latex %}j < n - d_n{% endlatex %}
	- důkaz sporem: kdyby {% latex %}j \ge n - d_n{% endlatex %}, pak {% latex %}\exists i{% endlatex %} a {% latex %}\exists k: \left\{v_j, v_k\right\} \in E\left(G\right) \land \left\{v_i, v_k\right\} \not\in E\left(G\right)	{% endlatex %}
		- pro {% latex %}d_i < d_j{% endlatex %} -- z {% latex %}v_j{% endlatex %} jich vede více než s {% latex %}d_i{% endlatex %} (takže do nějaké do které {% latex %}d_j{% endlatex %} vede {% latex %}d_i{% endlatex %} nevede)
		- {% latex %}d_i = d_j{% endlatex %} je taky ok... jedna z {% latex %}v_i{% endlatex %} vede do {% latex %}v_n{% endlatex %}

{% xopp score_2 %}

- škrtnutím vyrobíme graf, který má menší {% latex %}j{% endlatex %}... ↯

---

Graf {% latex %}H{% endlatex %} je _podgrafem_ grafu {% latex %}G \left(H \subseteq G\right) \equiv V\left(H\right) \subseteq V\left(G\right) \land E\left(H\right) \subseteq E\left(G\right){% endlatex %}.
- vznik tak, že z grafu odebíráme hrany/vrcholy

Graf {% latex %}H{% endlatex %} je _indukovaným podgrafem_ grafu {% latex %}G \left(H \subseteq G\right) \equiv V\left(H\right) \subseteq V\left(G\right) \land E\left(H\right) = E\left(G\right) \cup \binom{V\left(H\right)}{2}{% endlatex %}.
- vznik tak, že z grafu odebíráme pouze vrcholy (a s nimi spojené hrany)

_Cesta_ v grafu délky {% latex %}k{% endlatex %} je (2 pohledy):
1. {% latex %}H \subseteq G{% endlatex %} t. ž. {% latex %}H \cong P_k{% endlatex %}
2. {% latex %}v_0, e_1, v_1, \ldots, e_k, v_k{% endlatex %} t. ž.:
	- {% latex %}\forall i: v_i \in V\left(G\right){% endlatex %} + všechny {% latex %}v_i{% endlatex %} jsou různé vrcholy
	- {% latex %}\forall j: e_j \in E\left(G\right) \land e_j = \left\{v_{j - i}, v_j\right\}{% endlatex %}
- obdobně lze definovat kružnici, jen {% latex %}v_e = v_k{% endlatex %}

_Sled_ (procházka/walk) v grafu {% latex %}G{% endlatex %} je cesta, ve které se mohou vrcholy i hrany opakovat.

- lemma: pokud existuje sled z {% latex %}x{% endlatex %} do {% latex %}y{% endlatex %}, pak existuje i cesta:
	- zvolíme nejkratší ze všech sledů... to je cesta; kdyby ne, pak {% latex %}\exists{% endlatex %} vrchol, který se tam vyskytuje 2x (tím pádem jde sled zkrátit)

---

Graf {% latex %}G{% endlatex %} je _souvislý_ (drží pohromadě) {% latex %}\ \equiv \forall u, v \in V\left(G\right) \exists\ {% endlatex %} cesta v {% latex %}G{% endlatex %} z {% latex %}u{% endlatex %} do {% latex %}v{% endlatex %}
- relace dosažitelnosti: {% latex %}\sim{% endlatex %} na {% latex %}V\left(G\right){% endlatex %}: {% latex %}u \sim v \equiv \exists{% endlatex %} cesta z {% latex %}u{% endlatex %} do {% latex %}v{% endlatex %}
	- je to ekvivalence: je _reflexivní_ (cesta z {% latex %}u{% endlatex %} do {% latex %}u{% endlatex %} velikosti 0), _symetrická_ (graf je neorientovaný) i _tranzitivní_ (jen pozor na to, že to po slepení může být sled -- je potřeba to ošetřit)

V souvislém grafu {% latex %}G{% endlatex %} je vzdálenost vrcholu {% latex %}u, v{% endlatex %} _minimum_ z delek cest z {% latex %}u{% endlatex %} do {% latex %}v{% endlatex %} (značíme {% latex %}\rho\left(u, v\right){% endlatex %}).
- jedná se o _metriku_, jelikož splňuje následující:
	1. {% latex %}\forall u, v: \rho\left(u, v\right) \ge 0{% endlatex %} 
	2. {% latex %}\forall u, v: \rho\left(u, v\right) = 0 \iff u = v{% endlatex %} 
	3. {% latex %}\forall u, v: \rho\left(u, v\right) = \rho\left(v, u\right){% endlatex %} 
	4. {% latex %}\forall u, v, w: \rho\left(u, v\right) \le \rho\left(u, w\right) + \rho\left(w, v\right){% endlatex %} (trojúhelníková nerovnost)

---

#### Grafové operace
- _přidání_ hrany/vrcholu: {% latex %}G + v{% endlatex %}, {% latex %}G + h{% endlatex %}
- _smazání_ hrany/vrcholu:
	- {% latex %}G - e := G\left(V, E \setminus \left\{e\right\}\right){% endlatex %}
	- {% latex %}G - v := G\left(V \setminus v, E \setminus \left\{e \in E \mid v \not\in e\right\}\right){% endlatex %}
- _dělení_ hrany {% latex %}G\ \%\ e := \left(V \cup \left\{z\right\}, \left(E \setminus \left\{x, y\right\}\right) \cup \left(\left\{x, z\right\}, \left\{z, y\right\}\right)\right){% endlatex %}
- kontrakce hrany {% latex %} G/e := \left(\left(V \setminus \left\{x, y\right\}\right) \cup \left\{z\right\}, \\ \left\{e \in E \mid e \cap \left\{x, y\right\} \neq \emptyset\right\} \cup \left\{\left(e \setminus \left\{x, y\right\}\right) \cup \left\{z\right\} \mid e \in E \land \left|e \cup \left\{x, y\right\}\right| = 1\right\}\right) {% endlatex %}

#### Stromy
Základní definice:
- strom je _souvislý acyklický graf_
- les je _acyklický graf_ (soubor stromů)
- list -- vrchol stromu s {% latex %}\mathrm{deg}\left(v\right) = 1{% endlatex %}

##### Základní vlastnosti

Lemma: Strom s alespoň 2 vrcholy má alespoň 2 _listy_ (vrcholy, do kterých vede 1 hrana).

Důkaz: uvažme nejdelší cestu. Její krajní vrcholy jsou listy, jelikož:
- pokud z nich vede cesta někam zpět do sebe, tak graf není strom
- pokud z nich vede cesta někam, kde jsme ještě nebyli, tak není nejdelší

Lemma: nechť {% latex %}v{% endlatex %} je list grafu {% latex %}G{% endlatex %}. Pak {% latex %}G{% endlatex %} je strom {% latex %}\iff G - v{% endlatex %} je strom.

Důkaz:
- {% latex %}\Rightarrow{% endlatex %}... {% latex %}G-v{% endlatex %} je acyklický (cyklus jsme odstraněním nevytvořili) a souvislý (vedla přes něj pouze 1 cesta, a to ta do něj)
- {% latex %}\Leftarrow{% endlatex %}... po přilepení je také souvislý ( {% latex %}\forall x \in G - v \exists\ {% endlatex %} cesta z {% latex %}x{% endlatex %} do {% latex %}v{% endlatex %}) a acyklický (přilepený vrchol má stupeň 1, nemůže tedy tvořit cyklus)

##### Charakteristika stromu
Následující tvrzení jsou ekvivalentní:
1. {% latex %}G{% endlatex %} je souvislý a acyklický (standardní)
2. mezi každými vrcholem {% latex %}x, y{% endlatex %} vede _právě 1 cesta_ (jsou jednoznačně souvislé)
3. {% latex %}G{% endlatex %} je souvislý a {% latex %}\forall e \in E\left(G\right): G - e{% endlatex %} souvislý není (je minimálně souvislý)
4. {% latex %}G{% endlatex %} je acyklický a {% latex %}\forall e \in \binom{V\left(G\right)}{2} \setminus E\left(G\right): G + e{% endlatex %} obsahuje cyklus (je maximálné acyklický... přidáním libovolné hrany se vytvoří cyklus)
5. {% latex %}G{% endlatex %} je souvislý a {% latex %}\left|E\left(G\right)\right| = \left|V\left(G\right)\right| - 1{% endlatex %} (Eulerova formule)

{% latex %}1 \implies 5{% endlatex %}: indukcí:
- {% latex %}n = 1{% endlatex %} sedí (0 hran, 1 vrchol, je to strom)
- {% latex %}n \rightarrow n + 1{% endlatex %}... nechť {% latex %}G{% endlatex %} má {% latex %}n + 1{% endlatex %} vrcholů... 
	- {% latex %}G{% endlatex %} má list (lemma), jehož odtržením máme stále strom ({% latex %}G'{% endlatex %})... poštváním IP máme důkaz

{% latex %}1 \implies 2{% endlatex %}: indukcí:
- {% latex %}n = 1{% endlatex %} platí
- po přilepení:
	- zachová všechny staré cesty
	- {% latex %}\forall x \in V\left(G - v\right) \exists!{% endlatex %} cesta {% latex %}x \sim s{% endlatex %} a {% latex %}\forall{% endlatex %} cesty {% latex %}x \sim v{% endlatex %} jsou tvaru {% latex %}x \sim s \sim v{% endlatex %} (jsou jednoznačné)

{% latex %}1 \implies 3{% endlatex %}: indukcí:
- pro {% latex %}n = 2{% endlatex %} platí (odebráním hrany se vrcholy rozpadnou)
- indukce {% latex %}n + 1 \rightarrow n{% endlatex %}:
	- IP: graf {% latex %}n{% endlatex %} se rozpadne
	- po odebrání {% latex %}n+1{% endlatex %} hrany se graf také rozpadne

{% latex %}1 \implies 4{% endlatex %}: 
- acykličnost sedí
- přidáním hrany vytvoříme cyklus, jelikož tam již existuje cesta a tohle vytvoří druhou
	- pozor! neplést si s implikací {% latex %}4 \implies 1{% endlatex %}; tohle _není spor_

{% latex %}2 \implies 1{% endlatex %}: 
- je tím pádem souvislý
- kdyby existovala kružnice, pak existují 2 různé cesty

{% latex %}3 \implies 1{% endlatex %}: 
- souvislost sedí
- kdyby existoval cyklus, tak se odstraněním nestane nesouvislý

{% latex %}4 \implies 1{% endlatex %}: 
- acykličnost sedí
- kdyby nebyl souvislý, tak přidání nevytvoří cyklus

{% latex %}5 \implies 1{% endlatex %} -- indukcí podle počtu vrcholů: 
- existuje vrchol, který je list
- koukneme na skóre: {% latex %}\sum_{i = 1}^{n} d_i = 2 \cdot \left|E\left(G\right)\right| = 2n - 2{% endlatex %}
	- {% latex %}d_i \ge 1{% endlatex %} (souvislost) a alespoň 1 je 1 (kdyby ne, tak {% latex %}d_i > 1{% endlatex %}, což je ale alespoň {% latex %}2n{% endlatex %}... máme list, jehož odtržením máme podle IP strom, a po přilepení je to také strom


#### Kostra, sled, tahy
_Kostra_ grafu {% latex %}G{% endlatex %} je graf {% latex %}H \subseteq G: V\left(H\right) = V\left(G\right) \land H{% endlatex %} je strom
- nesouvislý graf nemá kostru

_Tah_ je _sled_, ve kterém se neopakují hrany.
- _uzavřený/otevřený_ -- koncové vrcholy tahu jsou/nejsou stejné
- _Eulerovské_ -- obsahují všechny vrcholy a hrany grafu

Věta: v grafu {% latex %}G{% endlatex %} existuje _uzavřený Eulerovský tah_ {% latex %}\iff{% endlatex %} je souvislý a {% latex %}\forall\ v \in G: \mathrm{deg}\left(v\right){% endlatex %} je sudý
- {% latex %}\Rightarrow{% endlatex %}: je souvislý (všude se lze dostat tahem) i sudý (všechny hrany vedoucí do daného vrcholu lze spárovat, protože do něj vcházíme a vycházíme)
- {% latex %}\Leftarrow{% endlatex %}: uvážíme _nejdelší možný tah:_
	- je _uzavřený_, jelikož kdyby nebyl, pak je počáteční i koncový vrchol tahu lichý, ale sudost znamená, že jsme nějaké hrany nevyužili... tah tedy není maximální
	- je _Eulerovský_, protože:
		- obsahuje všechny vrcholy; kdyby ne, tak jej lze připojit a vytvořit tak větší tah
		- obsahuje všechny hrany; víme, že obsahuje všechny vrcholy, proto je hrana mezi již nakreslenými vrcholy... tu ale lze také přidat
	- POZOR: je potřeba si dávat pozor na pořadí, ve kterém tuhle implikaci dokazuji -- záleží na něm

#### Rozšiřování grafů 
_Multigraf_ je uspořádaná trojice {% latex %}\left(V, E, K\right){% endlatex %}, kde:
- {% latex %}V{% endlatex %} jsou vrcholy ( {% latex %}V \neq \emptyset{% endlatex %})
- {% latex %}E{% endlatex %} jsou hrany
- {% latex %}K{% endlatex %} je zobrazení {% latex %}E \mapsto \binom{V}{2} \cup V{% endlatex %} (sjednocení kvůli existenci smyček)

_Orientovaný graf_ je {% latex %}\left(V, E\right){% endlatex %}, kde {% latex %}E \subseteq V^2 \setminus \Delta_V{% endlatex %} (lze u multigrafu rozšířit obdobně)
- hodí se rozlišovat vstupní ({% latex %}\mathrm{deg}^{\mathrm{in}}{% endlatex %}) a výstupní ({% latex %}\mathrm{deg}^{\mathrm{out}}{% endlatex %}) stupně

_Podkladový graf_:
- u orientovaného zapomeneme orientaci
- u multigrafu zrušíme opakování hran

Souvislost u grafů:
- _slabá_ -- dosažitelnost v podkladovém
- _silná_ -- {% latex %}\forall u, v \in V \exists{% endlatex %} cesta z  do {% latex %}v{% endlatex %}
 
Věta: pro _vyvážený_ orientovaný multigraf {% latex %}G{% endlatex %} je ekvivalentní:
1. {% latex %}G{% endlatex %} je slabě souvislý
2. {% latex %}G{% endlatex %} má uzavřený Eulerovský tah
3. {% latex %}G{% endlatex %} je silně souvislý

{% latex %}3 \implies 1{% endlatex %} již víme (podkladový je obecnější)

{% latex %}2 \implies 3{% endlatex %} tahem se dostaneme kdekoliv potřebujeme

{% latex %}1 \implies 2{% endlatex %} stejné jako důkaz u neorientovaného


#### Rovinné nakreslení grafu
- bod... prvek {% latex %}\mathbb{R}^2{% endlatex %}
- křivka... možina bodů; spojitá a prostá

{% xopp krivka %}

Definice: jednoduchá křivka (oblouk) je {% latex %}f: \left[0, 1\right] \mapsto \mathbb{R}^2{% endlatex %} spojitá a prostá.
- jednoduchá uzavřená křivka (kružnice): prostá až na {% latex %}f\left(0\right) = f\left(1\right){% endlatex %}

Definice: _Rovinné nakreslení multigrafu_ {% latex %}\left(V, E, K\right){% endlatex %}: {% latex %}\nu V \mapsto \mathbb{R}^2{% endlatex %} a {% latex %}\left\{C_e \mid e \in E\right\}{% endlatex %} množina oblouků/topologických kružnic t. ž.:
1. {% latex %}\forall e \in E: K\left(e\right) = \left\{u, v\right\}{% endlatex %}: {% latex %}C_e{% endlatex %} je oblouk s koncy {% latex %}\left\{\nu\left(u\right), \nu\left(v\right)\right\}{% endlatex %}
	- za každou hranu existuje oblouk
2. {% latex %}\forall e \in E: K\left(e\right) = u{% endlatex %}: {% latex %}C_e{% endlatex %} je kružnice obsahující {% latex %}\nu\left(u\right){% endlatex %}
	- smyčky
3. {% latex %}\forall e, f{% endlatex %} různé {% latex %}\in E: C_e \cap C_f = \nu\left[K\left(e\right) \cap K\left(f\right)\right]{% endlatex %}
	- průniky jsou jen vrcholy
4. {% latex %}\forall v \in V, \forall e \in E: \nu\left(v\right) \in C_e \implies v \in K\left(e\right){% endlatex %}
	- protíná-li kružnice vrchol, pak je vrchol na té hraně

Graf je _rovinný_, pokud existuje nějaké jeho rovinné nakreslení.
- cesta je rovinná
- kružnice je rovinná
- strom je rovinný... indukcí (přidáváním listů), jelikož vždy se lze posunout alespoň o kousek dále

_Topologický_ graf -- graf nakreslený do roviny.

Jordanová věta: Nechť {% latex %}T{% endlatex %} je topologická kružnice v {% latex %}\mathbb{R}^2{% endlatex %}. Pak {% latex %}\mathbb{R}^2 \setminus T{% endlatex %} má právě 2 komponenty obloukové souvislosti: 1 omezenou, 1 neomezenou a {% latex %}T{% endlatex %} je jejich společnou hranicní.
- těžké dokázat

---

Lemma: {% latex %}K_5{% endlatex %} není rovinná.

Důkaz: Po rovinném nakreslení {% latex %}K_4{% endlatex %} je zřejmé, že z každé stěny jsou dosažitelné právě 3 vrcholy -- {% latex %}K_5{% endlatex %} proto rovinná být nemůže.

---

Křížící číslo: min. počet křížení.

Stěny nakreslení: komponenty obloukové souvislosti {% latex %}\mathbb{R}^2 \setminus \left(\left\{\mu\left(v\right) \mid v \in V \right\} \bigcup_{e \in E} C(e)\right){% endlatex %} 

{% xopp komponenty %}

- nechová se jako izomorfismus!

{% xopp komponenty2 %}

---

Věta: hranice každé stěny souvislého grafu je nakreslením uzavřeného sledu, který každou hranu obsahuje max 2x

Důkaz: indukce podle počtu hran (počet vrcholů je pevný):
1. pro strom: počet hran = počet vrcholů - 1; nakreslení má právě 1 stěnu; sled je DFS
2. pro {% latex %}\left|E\right| > \left|V\right| - 1{% endlatex %}: obsahuje kružnici... nechť {% latex %}e = \left\{u, v\right\}{% endlatex %} leží na kružnici; rozdělíme ji na 2 sledy

---

Věta: {% latex %}G{% endlatex %} má nakreslení na sféru {% latex %}\iff G{% endlatex %} je rovinný.

Důkaz: uděláme _stereografickou projekci_... jedná se o bijekci
- pozor! je potřeba ji natočit tak, ať se netrefíme do grafu

{% xopp sfera %}

---

Věta (Kuratowského): {% latex %}G{% endlatex %} není rovinný {% latex %}\iff \exists H \cong G{% endlatex %} t. ž.: {% latex %}H \cong{% endlatex %} nějakému dělení {% latex %}K_5{% endlatex %} nebo {% latex %}K_{3, 3}{% endlatex %}

---

Věta (Eulerova formule): nechť {% latex %}G{% endlatex %} je souvislý graf nakreslený do roviny. Pak {% latex %}v + f = e + 2{% endlatex %}

Důkaz: fixujeme {% latex %}v{% endlatex %}, indukce podle {% latex %}e{% endlatex %}:
- graf je strom: {% latex %}e = v - 1; f =1{% endlatex %}... {% latex %}v + f = e + 2{% endlatex %}
- IK: uvažme {% latex %}h{% endlatex %} na kružnici a podívejme se na {% latex %}G - h{% endlatex %}
	- {% latex %}v' = v{% endlatex %}
	- {% latex %}e' = e - 1{% endlatex %} (odebrání hrany)
	- {% latex %}f' = f - 1{% endlatex %} (spojení dvou stěn)

---

Definice: {% latex %}G{% endlatex %} je maximálně rovinný {% latex %}\iff G{% endlatex %} je rovinný a {% latex %}G + e{% endlatex %} není rovinný {% latex %}\forall e \not\in E\left(G\right){% endlatex %}.

Věta: pro maximálné rovinný graf {% latex %}G{% endlatex %} s {% latex %}v \ge 3{% endlatex %} jsou všechny jeho stěny trojúhelníky.

Důkaz:
1. každý maximální graf je souvislý (pokud ne, tak lze nesouvislé komponenty spojit)
2. kdyby existovala stěna s hranicí {% latex %}C_n{% endlatex %} pro {% latex %}n > 3{% endlatex %}, pak můžeme v rámci stěny přidat hranu
3. strana, jejíž hranice není kružnice neexistuje (mohli bychom přidat stěnu)

---

Věta: Nechť {% latex %}G{% endlatex %} je maximálně rovinný s {% latex %}v \ge 3{% endlatex %} vrcholy. Pak {% latex %}e = 3f / 2{% endlatex %}.

Důkaz: Každá stěna je trojúhelník ({% latex %}3f{% endlatex %}) a patří právě do dvou stěn ({% latex %}/ 2{% endlatex %})... počítání dvěma způsoby.
- pozn.: můžeme dosadit do Eulerova vzorce (jelikož je zajisté souvislý) a dostaneme {% latex %}v + \frac{2}{3} e = e + 2 \implies e = 3v - 6{% endlatex %}
	- je z toho přímo vidět, že {% latex %}K_5{% endlatex %} není rovinná

---

Věta: v každém rovinném grafu existuje vrchol t. ž. {% latex %}\mathrm{deg}\left(v\right) \le 5{% endlatex %}

Důkaz:
- pro počet vrcholů {% latex %}\le 2{% endlatex %} triviální
- pro ostatní: {% latex %}e \le 3v - 6 \implies{% endlatex %} průměrný stupeň {% latex %}< 6{% endlatex %}
	- {% latex %}2e \le 6v - 12 \implies 2e < 6v \implies \frac{2e}{v} < 6{% endlatex %} ({% latex %}2e{% endlatex %} je součet všech stupňů)

---

Věta: Nechť {% latex %}G{% endlatex %} je maximálně rovinný vez trojúhelníků. Pak {% latex %}e \le 2v - 4{% endlatex %}.

Důkaz: počítání dvěma způsoby: {% latex %}e \ge 4f / 2{% endlatex %} (každá hrana patří do dvou stěn, které jsou tvořeny {% latex %}\ge{% endlatex %} 4 hranami. Dosazením do Eulera dostaneme nerovnost.

#### Barvení
Obarvení grafu {% latex %}G{% endlatex %} {% latex %}k{% endlatex %} barvami je funkce {% latex %}C: V\left(G\right) \mapsto \left\{1, \ldots, k\right\}{% endlatex %} t. ž. {% latex %}\forall u, v \in V\left(G\right): \left\{u, v\right\} \in E\left(G\right) \implies C\left(u\right) \neq C\left(v\right){% endlatex %}

Barevnost (chromatické číslo {% latex %}\chi\left(G\right){% endlatex %}) je nejmenší {% latex %}k{% endlatex %} t. ž. existuje obarvení grafu {% latex %}G{% endlatex %} {% latex %}k{% endlatex %} barvami.
- motivace: přidělování bez konfliktů
- {% latex %}\chi\left(P_n\right) = 2{% endlatex %} (pro {% latex %}n > 0{% endlatex %})
- {% latex %}\chi\left(C_n\right) = \begin{cases} 2 & n\ \text{sudé} \\ 3 & n\ \text{liché} \end{cases}{% endlatex %}
- {% latex %}\chi\left(K_n\right) = n{% endlatex %}
- {% latex %}H \subseteq G \implies \chi\left(H\right) \le \chi\left(G\right){% endlatex %}
- {% latex %}\chi\left(G\right) = 1 \iff G{% endlatex %} nemá hrany
- {% latex %}\chi\left(G\right) = 2 \iff G{% endlatex %} je bipartitní

---

Věta: pokud {% latex %}G{% endlatex %} nemá lichou kružnici, pak {% latex %}\chi\left(G\right) \le 2{% endlatex %}.

Důkaz: graf je souvislý {% latex %}\implies{% endlatex %} má kostru {% latex %}T{% endlatex %}. Nechť {% latex %}C{% endlatex %} je 2-obarvení {% latex %}T{% endlatex %}. Pokud by {% latex %}C{% endlatex %} nebylo obarvením {% latex %}G{% endlatex %}, pak {% latex %}\exists{% endlatex %} cesta sudé délky z vrcholu {% latex %}u{% endlatex %} do {% latex %}v{% endlatex %}, jejíž propojením dostáváme lichý cyklus. 
- pozor Tome, kolize vzniká při _stejných_ barvách :)

---

Lemma: Je-li T strom s alespoň 2 vrcholy. pak {% latex %}\chi\left(T\right) = 2{% endlatex %}

Důkaz: zakořeníme a barvíme po vrstvách.

---

##### Degenerovanost
Definice: graf {% latex %}G{% endlatex %} je {% latex %}d{% endlatex %}-degenerovaný {% latex %}\equiv \forall H \subseteq G\ \exists v \in V\left(H\right): \mathrm{deg}_H\left(v\right) \le d{% endlatex %}
- pozor! neříká to, že {% latex %}\forall v \in V\left(G\right): \mathrm{deg}\left(v\right) \le 5{% endlatex %}, jelikož podgrafy trhají vrcholy a hrany
- každý strom je 1-degenerovaný
- rovinné grafy jsou 5-degenerované (viz. důkaz kousek zpět -- stupně rovinných grafů)
- graf s max. stupněm {% latex %}\Delta{% endlatex %} je {% latex %}\Delta{% endlatex %}-degenerovaný
- obecně platí {% latex %}\chi\left(G\right) \le d + 1{% endlatex %}
	- důkaz indukcí: odstranění má obarvení a ke přidání zpět je potřeba alespoň 1 volná barva

{% xopp chi %}

---

Pro {% latex %}G{% endlatex %} _nakreslený do roviny_ definujeme {% latex %}G^*{% endlatex %} duální graf:
- ze stěny je vrchol (a obráceně)
- z hrany je hrana (bijekce)
- podle Eulerovy formule: {% latex %}v{% endlatex %} a {% latex %}f{% endlatex %} se _prohazuje_, {% latex %}e{% endlatex %} _zůstává_

{% xopp dual %}

_Klikovost_ {% latex %}\omega\left(G\right){% endlatex %} je maximální {% latex %}k{% endlatex %} t. ž. {% latex %}G{% endlatex %} obsahuje {% latex %}K_k{% endlatex %}.
- {% latex %}\chi\left(G\right) \ge \omega\left(G\right){% endlatex %} (na {% latex %}K_k{% endlatex %} je potřeba {% latex %}k{% endlatex %} barev...


##### 5-obarvitelnost
Věta: každý rovinný graf je 5-obarvitelný.

Důkaz:
- pro {% latex %}\left|V\right| \le 5{% endlatex %} lze triviálně (prostě přiřadíme všechny barvy)
- indukcí: uvažme {% latex %}v \in V\left(G\right){% endlatex %} s maximálním stupněm
	- pro {% latex %}\mathrm{deg}(v) \le 4{% endlatex %}... indukcí přiřadíme vrcholu zbylou barvu
	- {% latex %}\mathrm{deg}(v) > 5{% endlatex %} nenastane (vztah {% latex %}e = 3v - 6{% endlatex %})
	- pro {% latex %}\mathrm{deg}(v) = 5{% endlatex %}: uvažme zeleno-červený podgaf vycházející z vrcholu {% latex %}a{% endlatex %}... pro ten mohou nastat dva případy:
		1. pokud {% latex %}c{% endlatex %} nepatří do podgrafu, tak prohodíme _všechny barvy v podgrafu_ a jedné se tím na problematickém vrcholu zbavíme
		2. pokud patří, tak uděláme totéž s vrcholy {% latex %}b{% endlatex %} a {% latex %}d{% endlatex %}; oba případy najednou nastat nemohou, jelikož by se křížily v hraně (nelze -- poruší rovinnost) nebo ve vrcholu (nelze, ten už má barvu)

{% xopp 5-barevnost %}

### Pravděpodobnost
Diskrétní pravděpodobnostní prostor je {% latex %}\left(\Omega, P\right){% endlatex %}.
- {% latex %}\Omega{% endlatex %} je nejvýše spočetná množina _elementárních jevů_ (hod mincí/kostkou/...)
- {% latex %}P{% endlatex %} je funkce {% latex %}\Omega \mapsto \left[0, 1\right]{% endlatex %} („pravděpodobnost“) t. ž. {% latex %}\sum_{\omega \in \Omega} P(\omega) = 1{% endlatex %}
- klasický... {% latex %}\forall x, y {% endlatex %} el. jevy platí {% latex %}P\left(x\right) = P\left(y\right){% endlatex %}

_Jev_ {% latex %}X{% endlatex %} je množina elementárních jevů.
- {% latex %}P\left[X\right] = \sum_{\omega \in X} P\left(\omega\right){% endlatex %}
- {% latex %}P\left[\Omega\right] = 1{% endlatex %}
- {% latex %}P\left[\emptyset\right] = 0{% endlatex %}

#### Podmíněná pravděpodobnost
{% latex display %}P\left[A \mid B\right] := \frac{P\left[A \cap B\right]}{P\left[B\right]}{% endlatex %} 
- podmínkou vytváříme novou množinu elementárních jevů, která ale není normalizovaná (to zajišťuje dělení)
- vlastně to po přepsání na {% latex %}P\left[A \mid B\right] \cdot P\left[B\right] = P\left[A \cap B\right]{% endlatex %} znamená: pravděpodobnost {% latex %}B{% endlatex %} krát pravděpodobnost, že v rámci {% latex %}B{% endlatex %} nastane {% latex %}A{% endlatex %} je šance jejich průniku ({% latex %}P\left[A \cap B\right]{% endlatex %}):

{% xopp podminena %}

Věta o úplné pravděpodobnosti: nechť {% latex %}B_1, \ldots, B_k{% endlatex %} je rozklad {% latex %}\Omega{% endlatex %} a {% latex %}\forall i: P\left[B_i\right] \neq 0{% endlatex %}
{% latex display %}\forall A: P\left[A\right] = \sum_{i} \underbrace{P\left[A \mid B_i\right] \cdot P\left[B_i\right]}_{P\left[A \cap B_i\right]}{% endlatex %}

---

Věta (Bayesova): nechť {% latex %}B_1, \ldots, B_k{% endlatex %} je rozklad {% latex %}\Omega{% endlatex %} t. ž. {% latex %}\forall i: P\left[B_i\right] \neq 0{% endlatex %} a {% latex %}A{% endlatex %} je jev.

Potom {% latex %}\forall i{% endlatex %}:

{% latex display %}P\left[B_i \mid A\right] = \frac{P\left[A \mid B_i\right] \cdot P\left[B_i\right]}{\sum_{j} P\left[A \mid B_j\right] \cdot P\left[B_j\right]} = \frac{P\left[A \mid B_i\right] \cdot P\left[B_i\right]}{P\left[A\right]}{% endlatex %}

Důkaz (trochu pseudo): {% latex display %}P\left[B_i \mid A\right] \cdot P\left[A\right] = P\left[A \cap B_i\right] = P\left[B_i \cap A\right] = P\left[A \mid B_i\right] \cdot P\left[B_i\right]{% endlatex %}

---

Definice: jevy {% latex %}A, B{% endlatex %} jsou nezávislé ({% latex %}B{% endlatex %} neovlivňuje {% latex %}A{% endlatex %}), pokud (ekvivalentní výroky):
1. {% latex %}P\left[A \mid B\right] = P\left[A\right]{% endlatex %} 
2. {% latex %}P\left[A \cap B\right] = P\left[A\right] \cdot P\left[B\right]{% endlatex %}

Obecněji: jevy {% latex %}A_1, \ldots, A_n{% endlatex %} jsou po {% latex %}k{% endlatex %} nezávislé {% latex %}\iff \forall I \in \binom{\left[n\right]}{k}: P\left[\bigcap_{i \in I} A_i\right] = \prod_{i \in I} P\left[A_i\right]{% endlatex %}
- jevy jsou nezávislé {% latex %}\iff{% endlatex %} jsou po {% latex %}k{% endlatex %} nezávislé {% latex %}\forall k{% endlatex %}

Definice: _součin pravděpodobnostních prostorů_ {% latex %}P\left(\Omega_1, P_1\right){% endlatex %} a {% latex %}\left(\Omega_2, P_2\right){% endlatex %} je pravděpodobnostní prostor {% latex %}\left(\Omega, P\right){% endlatex %} t. ž.:
- {% latex %}\Omega := \Omega_1 \times \Omega_2{% endlatex %}
- {% latex %}P\left(\left(x_1, x_2\right)\right) = P_1\left(x_1\right) \cdot P_2\left(x_2\right){% endlatex %}
- pozn.: stále se pravděpodobnost sečte na jedničku: {% latex %}\sum_{x1, x2} P_1\left(x_1\right) P_2\left(x_2\right) = 1 \cdot 1 = 1{% endlatex %}

Definice: _náhodná veličina_ je {% latex %}f: \Omega \mapsto \mathbb{R}{% endlatex %} (ale klidně i do jiné množiny... je to dost jedno)
- {% latex %}P\left[f \ge 7\right] = \left\{\omega \in \Omega \mid f\left(\omega\right) \ge 7\right\}{% endlatex %}
- _střední hodnota_ náhodné veličiny {% latex %}X{% endlatex %} je {% latex %}\mathbb{E}\left[X\right] := \sum_{\omega \in \Omega}X\left(\omega\right) \cdot P\left(\omega\right){% endlatex %} 
- linearita střední hodnoty: {% latex %}\forall X, Y{% endlatex %} náhodné veličiny platí:
	- {% latex %}\mathbb{E}\left[X + Y\right] = \mathbb{E}\left[X\right] + \mathbb{E}\left[Y\right]{% endlatex %}
	- {% latex %}\mathbb{E}\left[\alpha X\right] = \alpha \mathbb{E}\left[X\right] \quad \forall \alpha \in \mathbb{R}{% endlatex %}
	- důkazy jsou přímočaré (dosazení do sumy)

Definice: _indikátor_ jevu {% latex %}J_i\left(\omega\right) = \begin{cases} 0 &\ \text{nenastal} \\ 1 &\ \text{nastal} \end{cases}{% endlatex %}
- {% latex %}J = \sum_{i} J_i{% endlatex %}

##### Pravděpodobnostní odhady
Věta (Markovova nerovnost): nechť {% latex %}X{% endlatex %} je náhodná _nezáporná_ veličina, která má střední hodnotu, a {% latex %}t \ge 1{% endlatex %}; potom platí, že {% latex display %}P\left[X \ge t \cdot \mathbb{E}\left[X\right]\right] \le \frac{1}{t}{% endlatex %}

Důkaz: vycházíme ze střední hodnoty; iterujeme přes všechna {% latex %}a \in R{% endlatex %}
{% latex display %}
\begin{aligned}
	\mathbb{E}\left[x\right] &= \sum_{a} P\left[x = a\right] \cdot a \\ 
	&\ge \sum_{a \ge k} P\left[x = a\right] \cdot a  \\
	&\ge \sum_{a \ge k} P\left[x = a\right] \cdot k \\
	&= k \cdot \sum_{a \ge k} P\left[x = a\right] \\
	&= k \cdot P\left[x \ge k\right]
\end{aligned}
{% endlatex %}
- dalšími úpravami (viz. začátek předešlých) a dosazením {% latex %}k := t \cdot \mathbb{E}\left[x\right]{% endlatex %} dostáváme nerovnost

---

Definice: {% latex %}\mathrm{var}\ X{% endlatex %} (variace = rozptyl) {% latex %}:= \mathbb{E}\left[\left(X - \mathbb{E}\left[X\right]\right)^2\right]{% endlatex %}
- {% latex %}\sqrt{\mathrm{var}\ X}{% endlatex %} je _střední hodnota odchylky_

Věta (Čebyševova nerovnost): nechť {% latex %}X{% endlatex %} je náhodná veličina, která má střední hodnotu, a {% latex %}t \ge 1{% endlatex %}; potom platí, že {% latex display %}P\left[\left|X - \mathbb{E}\left[X\right]\right| \ge t \cdot \sqrt{\mathrm{var}\ X}\right] \le \frac{1}{t^2}{% endlatex %}
Důkaz: dosazení do Markovovy nerovnosti (jen pozor na odmocňování nerovnosti -- abs. hodnota).
