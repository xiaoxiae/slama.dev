---
language: cz
title: Aproximační Algoritmy
category: "poznámky z přednášky"
---

- .
{:toc}

{% lecture_notes_preface Jiřího Sgalla|2021/2022%}

### Základní definice

{% math definition "Optimalizační problém" %} je \(\mathcal{I}, \mathcal{F}, f, g\)
- \(\mathcal{I} \ldots\) množina všech vstupů/instancí
	- _množina všech ohodnocených grafů_
- \(\forall I \in \mathcal{I}: \mathcal{F}(I) \ldots\) množina přípustných řešení
	- _pro daný ohodnocený graf všechny kostry_
- \(\forall I \in \mathcal{I}, A \in \mathcal{F}(I): f(I, A) \ldots \) účelová funkce
	- _součet hran na kostře_
- \(g \ldots\) bit (zda chceme maximalizovat nebo minimalizovat
	- _maximalizujeme_
{% endmath %}

{% math definition "NP-Optimalizační problém" %}je \(\mathcal{I}, \mathcal{F}, f, g\), pro které platí stejné věci jako pro normální optimalizační problémy, ale navíc
- délka přípustných řešení \(\le \mathrm{poly}(|I|)\).
- jazyk dvojic \((I, A), I \in \mathcal{I}, A \in \mathcal{F}(I)\) je v \(P\) (rychle umíme ověřit, zda je řešení přípustné)
- \(f\) počitatelná v polynomiálním čase
{% endmath %}

{:.rightFloatBox}
<div markdown="1">
Pro minimalizační zajišťujeme, že naše je vždy dostatečně malé (ne větší než \(R \cdot \mathrm{OPT}\). Pro maximalizační zajišťujeme, že je vždy dost velké (ne menší než \(\mathrm{OPT} / R\)).
</div>

{% math definition %}Algoritmus \(A\) je \(R\)-aproximační alg., pokud:
- v polynomiálním čase v \(|I|\) na vstupu \(I\) najde \(A \in \mathcal{F}(I)\)
- pro minimalizační problém: \(\forall I: f(A) \le R \cdot \mathrm{OPT}(I)\)
- pro maximalizační problém: \(\forall I: f(A) \ge \mathrm{OPT}(I) / R\)
{% endmath %} 

### Metrický TSP
- _Vstup:_ metrika \(V, d\) na úplném ohodnoceném grafu
	- metrika \(\equiv\) vrcholy splňují následující:
		1. trojúhelníkova nerovnost
		2. symetrie
		3. \(d(x, y) = 0 \iff x = y\)
	- pokud by to nebyla metrika, tak poly algoritmus neexistuje (jde převést na normální TSP)
- _Výstup:_ cyklus \(C\) na všech vrcholech \(V\)
- _Cíl:_ minimalizovat \(d(C)\)

#### Kostrový algoritmus
1. najdeme minimální kostru
2. navštívíme všechny vrcholy (například přes DFS), čímž dostaneme tah přes všechny vrcholy
3. zkrátíme ji na cyklus tak, že vynecháme opakující-se vrcholy

{% math theorem %}algoritmus je \(2\)-aproximační.{% endmath %}

{% math proof %}Kostra je nejvýše tak velká, jako optimální řešení a tenhle algoritmus je lepší než \(2\) kostry (díky trojúhelníkové nerovnosti a symetrii -- procházíme i tam i zpět){% endmath %}

#### Christofidesův algoritmus
{% math observation %}brát hrany dvakrát je plýtvání -- pospojujeme liché vrcholy přes minimální párování, abychom nemuseli chodit tam a zpět{% endmath %}

1. najdeme minimální kostru \(T\)
2. najdeme minimální perfektní párování \(M\) na vrcholech s lichými stupni v \(T\)
	- vždy existuje, jelikož máme úplný graf a vrcholů s lichým stupňem je sudý počet (všech je sudý)
3. zkrátíme na cyklus \(T \cup M\)

{% math theorem %}algoritmus je \(3/2\)-aproximační.{% endmath %}

{% math proof %}\[\mathrm{ALG} \le d(T) + d(M) \le \mathrm{OPT} + \frac{1}{2}\mathrm{OPT}\]

Důkaz \(d(M) \le \frac{1}{2}\mathrm{OPT}\) uděláme obrázkem:

{% xopp christof %}

Alespoň jeden z párování v cylku bude \(\le \frac{1}{2} \mathrm{OPT}\).
{% endmath %}

{% math remark %}
- dnes umíme \(\frac{3}{2} - \varepsilon\).
- TSP v rovině: existuje \((1 + \varepsilon)\)-aproximační schéma (ale stále je \(\mathrm{NP}\) těžký)
{% endmath %}

### Pravděpodobnost v algoritmech
1. algoritmy s chybou: někdy dělají chybu, ale většinou ji neudělají
2. bez chyb, běží v průměrném čase polynomiálním

- třída \(\mathrm{NP}\): jazyky, pro které existuje polynomiální algoritmus \(A\), který ověří správnost:
	- \(\forall a \in L\ \exists b: A(a, b) = 1\)
	- \(\forall a \not\in L\ \forall b: A(a, b) = 0\)

- třída \(\mathrm{RP}\): jazyky, pro které existuje polynomiální algoritmus \(A\), který ověří správnost:
	- \(\forall a \in L\ \mathrm{Pr}_b\left[A(a, b)\right] \ge \frac{1}{2}\)
	- \(\forall a \not\in L\ \mathrm{Pr}_b\left[A(a, b)\right] = 0\)

### Quicksort
- rekurzivně třídíme posloupnost přes pivoty:
	1. \(|S| \le 1 \ldots\) konec, vystoupíme \(S\)
	2. vybereme uniformě náhodně \(p \in S\)
	3. \(A = \left\{x \in S \mid x < p\right\}, B = \left\{x \in S \mid x > p\right\}\)
		- posloupnost má všechny prvky rozdílné
	4. rekurzivně se zavoláme na \(A, B\)
	5. vystoupíme \(A, p, B\)

{% math theorem %}Quicksort má průměrnou časovou složitost \(n \cdot \log n\).{% endmath %}

{:.rightFloatBox}
<div markdown="1">
Pro připomenutí:
- \(\mathbb{E}\left[X_{i, j}\right] = \mathrm{Pr}\left[A_{i, j}\right]\) (indikátorová veličina)
- \(\mathbb{E}\left[X + Y\right] = \mathbb{E}\left[X\right] + \mathbb{E}\left[Y\right]\)
</div>

{% math proof %}
- počítáme \(A_{i, j} = \mathrm{Pr}\left[\text{porovnáme $i$-tý a $j$-tý prvek}\right]\)
- \(X_{i, j} = \begin{cases}1 & A_{i, j} \text{nastane} \\ 0 & \text{jinak}\end{cases}\)

{% math lemma %}Nechť \(i < j\). Pak \(\mathrm{Pr}\left[A_{i, j}\right] = \frac{2}{j - i + 1}\){% endmath %}

{% math proof %}To, že se dva prvky porovnají musí znamentat, že jeden z jich byl pivot, ale žádný mezi nimi pivot nebyl (jelikož by je to rozdělilo). Musíme tedy vybrat právě jeden z těchto dvou z intervalu \(\left[i, j\right]\), kde je celkově \(j - i + 1\) čísel.{% endmath %}

\[
\begin{aligned}
	\mathbb{E}\left[\#\ \text{porovnání}\right] &= \sum_{i = 1}^{n - 1} \sum_{j = i + 1}^{n} X_{i, j} \\
	&= \sum_{i = 1}^{n - 1} \sum_{j = i + 1}^{n} \frac{2}{j - i + 1} \\
	& = \sum_{i = 1}^{n - 1} \sum_{k = 2}^{n - i} \frac{2}{k} \\
	& \cong n \cdot H_n  \qquad H_n \ldots \text{harmonická posloupnost}\\
	& \cong n \cdot \log n
\end{aligned}
\]
{% endmath %}

TODO: 3. přednáška

### Globální minimální řez
- _Vstup:_ neorientovaný graf \((V, E)\)
- _Výstup:_ \(F \subseteq E\) tak, že \(V, E \setminus F\) není souvislý
- _Cíl:_ minimalizovat \(|F|\)

#### Klasický algoritmus
1. převedeme graf na ohodnocený s jednotkovými cenami
2. zafixujeme \(s\)
3. pro všechna \(t\) najdeme minimalní řez
4. vrátíme minimální, který jsme našli

- umíme vyřešit řádové v \(\mathcal{O}(n^3)\)

#### Náš algoritmus
1. vybereme náhodnou hranu a její vrcholy spojíme do jednoho
2. opakujeme, dokud nemáme pouze dva vrcholy
3. zbylé hrany na konci jsou náš řez

- idea je to, že hran v minimálním řezu je málo a nejspíš se do nich netrefím
- pracujeme s multigrafy -- při kontrakci **zachováváme hrany**
- umíme ho implementovat rychle (řádově \(\mathcal{O}(n^2 \cdot \log n)\))
- opravdu produkuje řez, protože vrcholy mezi výslednými komponentami danými vrcholy nemizí

{% math lemma %}Multigraf s \(n\) vrcholy a min. řezem velikosti \(k\) má alespoň \(kn/2\) hran.{% endmath %}

{% math proof %}\(\forall v\), hrany incidentní s \(v\) tvoří řez, proto musí platit \(\forall v: d_v \ge k\). Dosazením dostáváme \(|E| = \frac{1}{2} \sum_{v} d_v \ge \frac{1}{2} nk \){% endmath %}

{% math theorem %}Pravděpodobnost, že najdeme daný minimální řez \(C\) je alespoň \(\frac{2}{n \cdot (n - 1)}\).{% endmath %}

{% math proof %}
Nechť \(A_i\) jev, že v prvních \(i\) iteracích jsme nevybrali hranu z \(C\).

- \(\mathrm{Pr}[A_0] = 1\) (žádnou jsme ještě nevybrali)
- \(\mathrm{Pr}[A_1] \ge 1 - \frac{k}{nk / 2} = 1 - \frac{2}{n}\)
- \(\mathrm{Pr}[A_2 \mid A_1] \ge 1 - \frac{2}{n - 1}\)
- \(\mathrm{Pr}[A_2] = \mathrm{Pr}[A_2 \mid A_1] \cdot \mathrm{Pr}\left[A_1\right] \), z čehož vyplývá:

\[
\begin{aligned}
	\mathrm{Pr}[A_{n - 2}] & \ge \left(1 - \frac{2}{n}\right) \left(1 - \frac{2}{n -1}\right) \ldots \left(1 - \frac{2}{3}\right)  \\
	&= \frac{n - 2}{n} \frac{n - 3}{n - 1} \frac{n - 4}{n - 2} \ldots \frac{2}{4} \frac{1}{3} \\
	&= \frac{2}{n \cdot (n - 1)} = \frac{1}{\binom{n}{2}}
\end{aligned}
\]
{% endmath %}

{% math consequence %}Každý graf \(G\) má \(\le \binom{n}{2}\) globálních minimálních řezů.{% endmath %}
- jeden takový je například cyklus -- ten má opravdu řádově tolik řezů

{% math proof %}Každý běh algoritmu vystoupí právě jeden řez. Kdyby jich bylo více, tak nám pravděpodobnost nevychází (jevy jsou disjunktní).{% endmath %}

{% math theorem %}Pro \(n^2\) opakování algoritmu výše dostáváme nejmenší řez s pravděpodobností \(\ge \frac{1}{2}\){% endmath %}

{% math proof %}\(\mathrm{Pr}\left[\text{A uspěje}\right] \ge 1 - \left(1 - \frac{2}{n(n-1)}\right)^{n^2}\){% endmath %}

{% math remark %}Algoritmus můžeme vylepšit tak, že části, ve kterých se nejvíce dělají chyby (konkrétně ty pozdější) opakujeme vícekrát (a vezmeme minimum).{% endmath %}

### Rozvrhování
- _Vstup:_ \(m\) strojů, \(n\) úloh, každá o délce \(p_i\)
- _Výstup:_ rozklad \(\left\{1, \ldots, n\right\} = I_1 \cup I_2 \cup \ldots \cup I_m\) (rozvržení úloh na stroje)
- _Cíl:_ minimalizovat \(\max_{i=1}^{m} \sum_{j \in I_i}^{p_j}\) (délka nejdelšího stroje)

#### Hladový algoritmus
{% math algorithm "hladový" %}
1. úlohu přidej vždy tam, kde jich je zatím nejméně
2. profit?
{% endmath %}

{% math theorem "slabší odhad" %}Hladový rozvrhovací algoritmus je \(2\)-aproximační.{% endmath %}

{% math proof %}Obrázkem:

{% xopp rozvrh %}

Z obrázku vyplývá:
- \(T \le \mathrm{OPT}\) (optimum muselo úlohy také někam dát)
- \(p_j \le \mathrm{OPT}\) (optimum \(p_j\) muselo použít)

Spojením dostáváme \(\mathrm{ALG} = T + p_j \le 2 \cdot \mathrm{OPT}\)

{% endmath %}

{% math theorem "silnější odhad" %}Hladový rozvrhovací algoritmus je \(\left(2 - \frac{1}{m}\right)\)-aproximační.{% endmath %}

{% math proof %}
- \(\frac{1}{m} \sum_{k = 1}^{n} p_k \le \mathrm{OPT}\)
	- lépe, než rovnoměrně všechny úlohy rozvrhnout nemůžeme
- \(\sum_{k = 1}^{n} p_k \ge m \cdot T + p_j\)
	- součet všech úloh je alespoň součet před \(T + \) posledí úloha (vynéchám „ocásky“)

Kombinací nerovností dostávám \(T + \frac{p_j}{m} \le \mathrm{OPT}\).

Nyní místo odhadu \(T \le \mathrm{OPT}\) použijeme tyto dva odhady:

\[
\begin{aligned}
	T + \frac{p_j}{m} &\le \mathrm{OPT} \\
	(p_j &\le \mathrm{OPT}) \cdot \left(1 - \frac{1}{m}\right)
\end{aligned}
\]

Součtem dostáváme

\[
\begin{aligned}
	T + \frac{p_j}{m} + \left(1 - \frac{1}{m}\right) p_j &\le \mathrm{OPT} + \left(1 - \frac{1}{m}\right) \mathrm{OPT} \\
	\mathrm{ALG} &\le \left(2 - \frac{1}{m}\right) \mathrm{OPT}
\end{aligned}
\]
{% endmath %}

#### Algoritmus lokálního prohledávání
Pro lokální algoritmus potřebujeme s rozvrhem pracovat formálněji:

- _Vstup:_ \(m\) strojů, \(n\) úloh, každá o délce \(p_i\)
- _Výstup:_ funkce přiřazující každé úloze startovní čas \(s_i\), koncový čas \(c_i\) a stroj \(i\)
	- musí platit že \(c_i = s_i + p_i\) a že se úlohy nepřekrývají
- _Cíl:_ minimalizovat \(\max_{i=1}^{m} \sum_{j \in I_i}^{p_j}\) (délka nejdelšího stroje)

{:.rightFloatBox}
<div markdown="1">
Prostě přesouváme stroje, které končí nejpozději někam, aby začínaly dříve a zlepšujeme tím maximum.
</div>

{% math algorithm "lokální prohledávání" %}
1. najdi libovolný rozvrh **bez mezer** (i na začátku)
2. vezmi libovolné \(j\) s maximálním \(c_j\)
	- pokud existuje stroj \(i\) s délkou rozvrhu \(< s_j\), tak přesuň \(j\) na \(i\) **s minimální délkou**
	- jinak vystup aktuální rozvrh
{% endmath %}

{% math observation %}\(c_{\min} neklesá\){% endmath %}

{% math observation %}Každou úlohu přesuneme nejvýše jednou.{% endmath %}

{% math proof %}Jelikož ji přesouváme na stroj s minimální délkou, tak by musel existovat nějaký s ještě menší, což by byl spor s tím, jak algoritmus funguje (dáváme na nejmenší).{% endmath %}

{% math consequence %}algoritmus je polynomiální.{% endmath %}

{% math theorem "silnější odhad pro lokální algoritmus" %}algoritmus je \(\left(2 - \frac{1}{m}\right)\)-aproximační.{% endmath %}

#### Odbočka: online algoritmy
- vstup přichází postupně
- řešení musíme konstruovat postupně po krocích a pak už neměníme
- **hladový** je online, **lokální prohledávání** není
- pro \(m = 2\): lepší než \(3/2\)-aproximační neexistuje (úlohy délky \(\left\{1, 1, 2\right\}\))
- pro \(m = 3\) je opět hladový nejlepší, ale pro více strojů to už tak není

#### Odbočka: LPT (largest processing time)
{% math algorithm "LPT" %}
1. úlohy uspořádáme tak, že \(p_1 \ge p_2 \ge \ldots \ge p_n\)
2. použijeme hladový algoritmus
{% endmath %}

{% math theorem %}LPT je \(\left(\frac{4}{3} - \frac{1}{3m}\right)\)-aproximační algoritmus.{% endmath %}

{% math proof %}
BUNO předpokládejme, že \(p_n\) určuje délku rozvrhu (kdyby ne tak na další úlohy zapomenu a řešení se tím nezmění). Rozlišíme \(2\) případy:
- \(p_n \le \frac{1}{3} \mathrm{OPT}\) -- stejný výpočet jako předtím, jen silnější nerovnost:
	- \(\mathrm{ALG} = T + p_n\), \(T + \frac{p_n}{m} \le \mathrm{OPT}\)
	- stejným výpočtem jako předtím máme \(\mathrm{ALG} \le \mathrm{OPT} + \left(1 - \frac{1}{m}\right) \frac{1}{3} \mathrm{OPT}\)
- \(p_n > \frac{1}{3} \mathrm{OPT}\) -- LPT vygeneruje optimální rozvrh
	- víme, že délka poslední, a tedy **každé** úlohy je alespoň \(\mathrm{OPT} / 3\)
	- žádný počítač nebude mít 3 úlohy, jelikož by pak byl větší než optimum
	- chceme argumentovat, že LPT udělá stejné dvojice jako optimální rozvrh:
		- \(p_m + p_{m + 1} \le \mathrm{OPT}\) -- uvážíme-li pouze prvních \(m + 1\) úloh, tak optimální rozvrh bude mít alespoň \(2\) na jednom počítači a ty rozhodně nebudou kratší než dvě nejkratší
			- tento rozvrh s méně úlohami je jistě \(\le \mathrm{OPT}\), proto nerovnost platí
		- \(p_{m - 1} + p_{m + 2} \le \mathrm{OPT}\) -- v optimálním rozvrhu budou mít alespoň \(2\) počítače dvojici úloh; v jedné z nich bude čtvrtá nejmenší (\(p_{m - 1}\)), která tam bude s nejmenší (\(p_{m + 2}\))
		- obdobně dostaneme všechny další dolní odhady...

{% xopp lpt %}

{% endmath %}

#### Bin packing
- _Vstup:_ \(a_1, \ldots, a_n \ge 0\)
- _Výstup:_ rozklad \(\left\{1, \ldots, n\right\} = I_1 \cup \ldots \cup I_m\) tak, že \(\forall i: \sum_{j \in I_i} a_j \le 1\)
	- \(\equiv\) součet věcí v každém koši může být nejvýše \(1\)
- _Cíl:_ minimalizovat \(m\) (počet košů)

{% math algorithm "first fit" %}dej \(a_j\) do prvního koše, do kterého se vejde.{% endmath %}

{% math algorithm "best fit" %}dej \(a_j\) do nejplnějšího koše, do kterého se vejde.{% endmath %}

{% math theorem %}oba algoritmy jsou \(1.7\)-aproximační (a je to těsný odhad).{% endmath %}

{% math theorem %}Je NP těžké najít \(R\)-aproximační algoritmus pro \(R \le 3/2\){% endmath %}

{% math proof %}Je NP těžké rozhodnout, zda \(\mathrm{OPT} = 2\), jelikož to můžeme přímočaře převést na problém, kde dělím množinu na dvě časti se stejným součtem.{% endmath %}

{% math theorem %}Existuje asymptotické aproximační schéma, t. j. \[(\forall \varepsilon) (\exists \mathrm{ALG}) (\forall I) \mathrm{ALG}(I) \le (1 + \varepsilon)\mathrm{OPT}(I) + 1\]{% endmath %}

{% math algorithm "any fit" %}dej \(a_j\) do nějakého neprázdného koše; pokud nelze, dej ho do nového.
- zahrnuje jak best fit, tak first fit
{% endmath %}

{% math theorem %}Každý any fit algoritmus má aproximační poměr \(\le 2\).{% endmath %}

{% math proof %}Pro \(\mathrm{OPT} = 1\) triviální. Jinak nechť \(B_i = \sum_{j \in I_i} a_j\). Musí platit, že \((\forall i, j, i \neq j) B_i + B_j > 1\) (jinak spor s během algoritmu). Posčítáním pro všechny dvojice dostáváme \[\frac{m}{2} < \sum_{i = 1}^{m} B_i = \sum_{j = 1}^{n} a_j \le \mathrm{OPT}\]
{% endmath %}

### Hledání disjunktních cest
- _Vstup:_
	- graf \(G = (V, E)\) (orientovaný/neorientovaný)
	- dvojice vrcholů \((s, t), \ldots, (s_k, t_k)\)
	- kapacita hran \(c\)
- _Výstup:_
	- \(I \subseteq \left\{1, \ldots, k\right\}\) (dvojice které spojíme cestou)
	- cesty \(P_i, i \in I, P_i\) cesta z \(s_i\) do \(t_i\) tak, že každá hrana \(e \in E\) leží na nejvýše \(c\) cestách \(P_i\)
- _Cíl:_ minimalizovat \(|I|\)

#### Jednotkové kapacity
{% math algorithm "hladový" %}
1. najdeme nejkratší cestu mezi nespojenou dvojicí (přes všechna \(i\))
	- pokud neexistuje, tak vystoupíme
2. odebereme použité hrany
{% endmath %}

{% math observation %}hladový algoritmus nemá aproximační poměr \(\le \mathcal{O}(\sqrt{m})\):

{% xopp bad_path %}

- \(s_1 \mapsto t_1\): délka \(\mathcal{O}(k)\)
	- abychom zvolili tuto cestu, musejí mít ostatní alespoň \(\mathcal{O}(k)\) hran, celkově jich tedy musí být řádově \(\mathcal{O}(k^2)\)

{% endmath %}

{% math theorem %}Hladový algoritmus s \(c = 1\) je \(\mathcal{O}\left(\sqrt{m}\right)\)-aproximační.{% endmath %}

{% math proof %} BUNO optimum \(\ge 1\) (jinak bychom hned skončili)
- pak \(|I| = \mathrm{ALG} \ge 1\) (také nějakou najdeme)

Nechť \(I^*, \left\{P_i^* \mid i \in I^*\right\}\) je optimum. Počítejme cesty:
- dlouhé cesty: \(|P_i^*| > \sqrt{m}\)
	- je jich \(\le \sqrt{m}\) (jinak bych měl více než \(m\) hran)
	- ty mi tedy nic nekazí, jelikož nám stačí, že algoritmus najde nějakou cestu
- krátké cesty:
	- \(i \in I \ldots\ \) vše ok
	- \(i \not\in I \ldots\ P_i^*\) má nějakou společnou hranu s nějakou cestou \(P_j\) t. ž. \(|P_j| \le \sqrt{m}\)
		- ve chvíli, kdy algoritmus poprvé vybral cestu delší než \(\sqrt{m}\) už nemohl vybrat \(P_i^*\), protože tu blokovala nějaká cesta, kterou již předtím zvolil (a ta musí být krátká)

Tedy počet krátkých cest \(P_i^* \le |I| \left(\sqrt{m} + 1\right)\)
- \(1\) -- náš algoritmus a optimum vybrali stejnou cestu
- \(\sqrt{m}\) -- krátká cesta v našem řešení zablokuje nejvýše \(\sqrt{m}\) ostatních krátkých
\[\mathrm{OPT} = |I^*| \le \underbrace{\sqrt{m}}_{dlouhé} + \underbrace{|I| \left(\sqrt{m} + 1\right)}_{krátké} \le \mathcal{O}(\sqrt{m}) |I| = \mathcal{O}(\sqrt{m}) \mathrm{ALG} \]

{% endmath %}

#### Nejednotkové kapacity

{:.rightFloatBox}
<div markdown="1">
\(\beta^c = m^{\frac{c}{c+ 1}}\), což je zhruba \(m / \beta\)
</div>
{% math algorithm "hladový pro nejednotkovou kapacitu" %}
1. zvolíme \(\beta = \left\lceil m^{\frac{1}{c + 1}} \right\rceil\)
2. najdeme nejkratší cestu mezi nespojenou dvojicí (přes všechna \(i\))
	- pokud neexistuje **nebo** \(d(P_i) \ge \beta^c\), vystoupíme
3. přenásobíme délku hran nejkratší cesty faktorem \(\beta\) a opakujeme
{% endmath %}

{% math observation %}algoritmus nepoužije \(e\) s \(d(e) \ge m\){% endmath %}

{% math consequence %}výsledné řešení je připustné
- po \(c\) použitích hrany \(e\) je \(d(e) = \beta^c \approx m^{\frac{c}{c + 1}} < m\), dále algoritmus hranu nepoužívá{% endmath %}

{% math consequence %}algoritmus je polynomiální.{% endmath %}

{% math theorem %}Hladový algoritmus je \(\mathcal{O}\left(\beta\right)\)-aproximační.{% endmath %}

{% math proof %} BUNO optimum \(\ge 1\) (jinak bychom hned skončili)
- pak \(|I| = \mathrm{ALG} \ge 1\) (také nějakou najdeme)

- \(i \in I \ldots\ \) vše ok
- \(i \not\in I \ldots\ \) na konci algoritmu je \(d(P_i^*) \ge \beta^c\) (jinak by ji algoritmus použil)

Nejprve zesdola odhadneme \(d(E)\) na konci algoritmu:
- \(\beta^c (|OPT| - |I|)\): dolní odhad na délku cest, které algoritmus nespojil ale optimální ano
	- každá cesta má na konci delku alespoň \(\beta^c\) a je jich alespoň \(|\mathrm{OPT}| - |I|\)
- \(c \cdot d(E) \ge \beta^c (|\mathrm{OPT}| - |I|)\): každou hranu můžeme použít \(c\)-krát

Poté odhadneme \(d(E)\) zeshora (opět na konci algoritmu):
- na začátku \(d(E) = m\) (délky hran jsou jednotkové)
- po výběru \(P_i \ldots\ d(P_i) \le \beta^c \cdot \beta = \beta^{c + 1}\)
- na konci \(d(E) \le m + |I| \beta^{c + 1} \le \left(|I| + 1\right) \beta^{c + 1}\)
	- \(|I|\) je počet kroků, v každém jsme zvětšili délku vybrané cesty na \(\beta^{c + 1}\)
	- druhá úprava je pouze z definice

Po spojení nerovnic dostáváme:
\[
\begin{aligned}
	\beta^c \left(|\mathrm{OPT}| - |I|\right) &\le c \cdot d(E) \le c\left(|I| + 1\right) \beta^{c + 1} \\
	|\mathrm{OPT}| - |I| &\le \beta c (|I| + 1) \\
	|\mathrm{OPT}| &\le \mathcal{O}(\beta) |I| \\
\end{aligned}
\]
{% endmath %}

### Splnitelnost (MAX-SAT)
- _Vstup:_ \(C_1 \land \ldots \land C_m\), každá klauzule je disjunkcí \(k_j \ge 1\) literálů
	- každá \(C_j\) má váhu \(w_j\) (\(= 1\) by default)
- _Výstup:_ ohodnocení \(a \in \left\{0, 1\right\}^n\) (libovolné, i nesplnitelné!)
- _Cíl:_ maximalizovat \sum w_i

{% math remark %}
- MAX-3SAT: \(k_j \le 3\): NP těžké
- 2SAT: orientovaný graf, ve kterém různé literály implikují jiné
	- \(x_1 \land x_2\) implikuje \(\overline{x}_1 \implies x_2\) (a obrácené)
	- testujeme tedy, zda graf neobsahuje cyklus (protože by pak nešel splnit)
- MAX-2SAT: NP těžké
{% endmath %}

Předpokládáme:
- žádný literál se v klauzuli neopakuje
- nejvýše jeden z \(x_i, \overline{x}_i\) se vyskytuje v klauzuli

#### RAND-SAT
{% math algorithm "RAND-SAT" %}
1. vybereme nezávisle náhodně všechny literály (\(p = 1/2\))
2. profit?
{% endmath %}

{% math theorem %}RAND-SAT je \(2\)-aproximační algoritmus.{% endmath %}

{% math proof %}pro každou klauzuli zavedeme indikátorovou proměnnou \(Y_j\).
- pravděpodobnost, že \(C_j\) není splňená je \(\frac{1}{2^k}\)

Díky tomu, že \(k \ge 1\) máme \(\mathbb{E}\left[Y_j\right] = \mathrm{Pr}\left[C_j\ \text{is satistied}\right] = 1 - \frac{1}{2^k} \ge \frac{1}{2} \) a tedy:
\[\mathbb{E}\left[\sum_{j = 1}^{m} w_j Y_j\right] \overset{\text{linearita}}{=} \frac{1}{2} \sum_{j = 1}^{m} w_j \ge \frac{1}{2}\mathrm{OPT} \]
{% endmath %}

{% math remark %}pro \(k = 3\) dostáváme po dosazení \(\frac{8}{7}\)-aproximaci
- \(\forall \varepsilon > 0: \left(\frac{8}{7} - \varepsilon\right)\)-aproximace MAX-3SATu ne NP úplná {% endmath %}

{:.rightFloatBox}
<div markdown="1">
Předchozí algoritmus měl problémy s krátkými klauzulemi, jelikož je menší šance, že nějakou splní. Zkusíme to napravit tím, že jim budeme dávat preferenci.
</div>

#### BIASED-SAT
{% math algorithm "BIASED-SAT" %}
- předpoklad: \(\forall i: \sum_{j: C_j = x_i} w_j \ge \sum_{j: C_j = \overline{x}_i}\)
	- pokud nevychází, tak literál všude znegujeme

1. vybereme nezávisle náhodně všechny literály
	- true: \(p > \frac{1}{2}\), jinak false; hodnotu \(p\) najdeme později
{% endmath %}

{% math theorem %}BIASED-SAT je \(\left(\phi = \frac{\sqrt{5} - 1}{2}\right)\)-aproximační algoritmus.{% endmath %}

Uvažme \(C_j\) (a opět indikátorové veličiny \(Y_j\)):
- kladný literál: \(Y_j = p\)
- \(k_j \ge 2\): \(Y_j = 1 - p^a (1 - p)^b \overset{p > \frac{1}{2}}{\ge} 1-p^{a + b} \overset{k_j \ge 2}{\ge} 1 - p^2\)
	- \(a\) je počet kladných a \(b\) počet záporných literálů

Po vyřešení \(p = 1 - p^2\) dostáváme \(p = \phi = \frac{\sqrt{5} - 1}{2}\)!

Nechť \(U\) množina klauzulí bez záporných jednotkových.

{% math observation %}\(\mathrm{OPT} \le \sum_{j \in U} w_j\)
- zde používáme předpoklad -- kladné literály je splňovat lepší než záporné
{% endmath %}

\[
\begin{aligned}
	\mathbb{E}\left[\sum_{j = 1}^{m} w_j Y_j\right] &= \sum_{j = 1}^{m} w_j \mathbb{E}\left[Y_j\right] \\
	&\ge \sum_{j \in U} w_j \cdot \mathrm{Pr}\left[C_j\ \text{je splněná}\right] \\
	&\ge \sum_{j \in U} w_j \cdot p \\
	&\ge p \cdot \mathrm{OPT}
\end{aligned}
\]

#### LP-SAT
{% math algorithm "LP-SAT" %}
1. pro každou proměnnou si pořídíme binární proměnnou \(y_i\), pro každou klauzuli binární proměnnou \(z_j\)
2. postavíme lineární program s těmito proměnnými
	- negaci zachytíme jako \(1 - y_i\)
	- pro každou klauzuli chceme \(z_j \le \sum_{\text{kladné}} y_i + \sum_{\text{záporné}} (1 - y_i)\)
	- maximalizujeme \(\sum z_j\)
3. zrelaxujeme program a vyřešíme ho (dostaneme optimum \(y^*, z^*\))
4. nastavíme proměnné \(x_i\) na ture s pravděpodobností \(y_i^*\)
{% endmath %}

{% math theorem %}LP-SAT je \(\left(1 - \frac{1}{e}\right)\)-aproximační algoritmus.{% endmath %}

{% math fact "A" "A/G nerovnost" %}\(\prod_{i = 1}^{n} a_i^{\frac{1}{n}} \le \frac{1}{n} \sum_{i = 1}^{n} a_i\){% endmath %}

{% math fact "B" %}pokud je funkce na \(\left[0, 1\right]\) konkávní a \(f(0) = a, f(1) = a + b\), pak \[\forall x \in \left[0, 1\right]: f(x) \ge a + bx\]{% endmath %}

{% xopp aplusb %}

{% math fact "C" %}\(\left(1 - \frac{1}{n}\right)^n \le \frac{1}{e}\){% endmath %}

{% math proof %} uvažme \(y^*, z^*\) a \(C_j\) s délkou \(k_j\); pak

\[
\begin{aligned}
	\mathrm{Pr}\left[C_j\ \text{není splněná}\right] &= \overbrace{\prod_{i: x_i \in C_j} (1 - y^*_i)}^{\text{kladné}} \overbrace{\prod_{i: \overline{x}_i \in C_j} y^*_i}^{\text{záporné}} \\
	&\overset{A}{=} \left[\frac{1}{k_j} \left(\sum_{i: x_i \in C_j} (1 - y^*_i) + \sum_{i: \overline{x}_i \in C_j} y^*_i\right)\right]^{k_j} \\
	&= \left[1 - \frac{1}{k_j} \left(\sum_{i: x_i \in C_j} y^*_i + \sum_{i: \overline{x}_i \in C_j} (1 - y^*_i)\right)\right]^{k_j} \\
	&\le \left(1 - \frac{z_j^*}{k_j}\right)^k_j
\end{aligned}
\]

Nás zajímá splnění, tedy:
\[
\begin{aligned}
	\mathrm{Pr}\left[C_j\ \text{je splněná}\right] &\ge \overbrace{1 - \left(1 - \frac{z_j^*}{k_j}\right)^{k_j}}^{f(z_j^*)} \\
	& \overset{B}{\ge} \left[1 - \left(1 - \frac{1}{k_j}\right)^{k_j}\right] z_j^*
	& \overset{C}{\ge} \left(1 - \frac{1}{e}\right) z_j^*
\end{aligned}
\]

Pro fakt \(B\) jsme pozorovali, že \(a = f(0) = 0\) a také že druhá derivace je nekladná. Posčítáním přes všechny klauzule dostáváme
\[
\begin{aligned}
	\mathbb{E}\left[\sum_{j = 1}^{m} w_j Y_j\right] &= \sum_{j = 1}^{m} w_j \mathbb{E}\left[Y_j\right] \\
	&\ge \sum_{j \in U} w_j \cdot \mathrm{Pr}\left[C_j\ \text{je splněná}\right] \\
	&\ge \sum_{j \in U} w_j \cdot \left(1 - \frac{1}{e}\right) z_j^* \\
	&= \left(1 - \frac{1}{e}\right) \mathrm{OPT}\\
\end{aligned}
\]
{% endmath %}

#### BEST-SAT
{% math algorithm "BEST-SAT" %}
1. při přizazení s pravděpodobností \(1/2\) použijeme RAND-SAT, jinak použijeme BEST-SAT
2. wtf?
{% endmath %}

{% math theorem %}BEST-SAT je \(\frac{3}{4}\)-aproximační.{% endmath %}

{% math proof %} chceme dokázat, že \( \mathrm{Pr}\left[C_j\ \text{je splněná}\right] \ge \frac{3}{4} z^*_j \).

Podívejme se, s jakou pravděpodobností splní klauzuli algoritmy:
- RAND-SAT: \(1 - \frac{1}{2^k}\) (alespoň jedna musí být splněná a volíme s \(p = 1\))
- LP-SAT: \(\left[1 - \left(1 - \frac{1}{k}\right)^{k}\right] z_j^*\) (formulka z minulého důkazu těsně před odhadem)

| \(k_j\) | RAND-SAT                              | LP-SAT                                       | BEST-SAT                                                              |
| ---     | ---                                   | ---                                          | ---                                                                   |
| \(1\)   | \(\frac{1}{2} \ge \frac{1}{2} z_j^*\) | \(1 \cdot z_j^*\)                            | \(\frac{1}{2} \frac{1}{2} + \frac{1}{2} z_j^* \ge \frac{3}{4} z_j^*\) |
| \(2\)   | \(\ge \frac{3}{4} z_j^*\)             | \(\frac{3}{4} \cdot z_j^*\)                  | \(\ge \frac{3}{4} z_j^*\)                                             |
| \(3\)   | \(\ge \frac{7}{8} z_j^*\)             | \(\left(1 - \frac{1}{e}\right) \cdot z_j^*\) | \(> \frac{3}{4} z_j^*\)                                               |
{% endmath %}

##### Derandomizace metodou podmíněných pravděpodobností
TODO?

### Pokrývací problémy

#### Vrcholové pokrytí
- _Vstup:_ graf \(G\), ceny vrcholů \(c_v \ge 0\)
- _Výstup:_ \(W \subseteq V\) tak, že \(\forall e \in E: e \cap W \neq 0\)
- _Cíl:_ minimalizovat \(c(W) = \sum_{v \in W} c_v\)

{% math algorithm "LP relaxace" %}
1. vytvoř celočíselný lineární program:
	- proměnné jsou binární podle vrcholů, které vybíráme
	- podmínky jsou \(\forall (u, v) \in E: x_u + x_v \ge 1\) (chceme pokrýt všechny hrany)
	- minimalizujeme \(\sum_{v \in V} x_v c_v\)
2. zrelaxuj lineární program (proměnné jsou teď reálné)
3. použij ho při řešení -- zvol \(v\) když \(x_v \ge \frac{1}{2}\)
	- dává správné řešení, jelikož pro splnění podmínek je vždy alespoň jeden z \((x_u, x_v) \ge \frac{1}{2}\)
{% endmath %}

{% math theorem %}algoritmus je \(2\)-aproximační.{% endmath %}

{% math proof %}proměnné jsme z \(\ge \frac{1}{2}\) zaokrlouhlovali na \(1\), čímž jsme řešení max. zdvojnásobili.{% endmath %}

#### Množinové pokrytí
- _Vstup:_ množiny \(S_1, \ldots, S_n \subseteq \left\{1, \ldots, n\right\}\), ceny \(c_1, \ldots, c_m \ge 0\)
- _Výstup:_ \(I \subseteq \left\{1, \ldots, m\right\}\) t. ž. \(\bigcup_{i \in I} S_i = \left\{1, \ldots, n\right\}\)
- _Cíl:_ minimalizovat \(\sum_{i \in I} c_i\)

Pro rozbor budeme potřebovat ještě dva parametry:
- \(g = \max_{j = 1}^{m} |S_j| \le n\) (velikost největší množiny)
- \(f = \max_{e = 1}^{n} |\left\{j \mid e \in S_j\right\}| \)(v kolika nejvíce množinách je nějaký prvek)

{% math observation %}vrcholové pokrytí je množinové pokrytí s \(f \le 2\){% endmath %}

{:.rightFloatBox}
<div markdown="1">
Program pro vrcholové pokrytí:
- proměnné jsou binární podle vrcholů, které vybíráme
- podmínky jsou \(\forall (u, v) \in E: x_u + x_v \ge 1\) (chceme pokrýt všechny hrany)
- minimalizujeme \(\sum_{v \in V} x_v c_v\)
</div>

##### \(f\)-aproximační algoritmy

{% math algorithm "LP relaxace" %}
1. vytvoř celočíselný lineární program:
	- proměnné jsou \(x_1, \ldots, x_m \ge 0\) podle **množin**
	- podmínky jsou \(\forall e \in \left\{1, \ldots, n\right\}: \sum_{j \mid e \in S_i}^{x_j} \ge 1\) (chceme pokrýt všechny **prvky** univerza)
	- minimalizujeme \(\sum_{i \in \left\{1, \ldots, m\right\}} x_i c_i\)
2. zrelaxuj lineární program (proměnné jsou teď reálné)
3. použij ho při řešení -- zvol \(v\) když \(x_v \ge \frac{1}{f}\)
	- dává správné řešení -- argument je stejný jako u vrcholového pokrytí
{% endmath %}

{% math theorem %}algoritmus je \(f\)-aproximační.{% endmath %}

{% math proof %}proměnné opět zvětšuji z \(\frac{1}{f}\) na \(1\), řešení tedy zhorším nejvýše \(f\)-krát.{% endmath %}

{:.rightFloatBox}
<div markdown="1">
**Význam primáru (sběratel):** jak můžu nejlevněji nakoupit balíčky známek tak, abych měl všechny známky.

**Význam duálu (procejce):** kolik můžu nejvíce účtovat za každou známku, aby byl sběratel ochotný balíčky koupit.
</div>

{% math observation %}duál programu vypadá následně:
- proměnné jsou \(y_1, \ldots, y_n \ge 0\) pro každý **prvek**
- podmínky jsou \(\forall e \in \left\{1, \ldots, m\right\}: \sum_{e \in S_j} y_e \le c_j\)
- maximalizujeme \(\sum_{e \in S_j} y_e\)
{% endmath %}

{% math observation %}podmínky komplementarity:
- \(\forall j: x^*_j = 0 \lor \sum y_e = c_j\)
	- pokud by prodejce na obálce vydělal, tak ji sběratel nekoupí
	- pokud prodejce na známce nevydělává, tak ji sběratel koupí
- \(\forall e: y^*_e = 0 \lor \sum_{j \mid e \in S_j} x_j = 1\)
	- pokud prodejce prodává známku zdarma, tak jí sběratel nakoupí trochu více
	- pokud prodejce známku zdarma neprodává, tak jí sběratel nekoupí víc než potřeba
{% endmath %}

{% math algorithm "primárně-duální algoritmus" %}
1. \(y_1, \ldots, y_n = 0; I = \emptyset, E = \emptyset\)
2. dokud existuje nepokryté \(e \not\in E\), tak zvyšíme \(y_e\) „co nejvíce“:
	- \(\delta = \min_{j \mid e \in S_j} \left(c_j - \sum_{e \in S_j} y_e\right)\)
		- zvyšujeme tak, abychom splnili tu nejpřísnější duální podmínku
	- \(y_e = y_e + \delta\)
	- \(\forall j: e \in S_j \) a \(\sum_{e \in S_j} y_e = c_j\) přidám \(j\) do pokrytí (\(I = I \cup \left\{j\right\}\)) a \(E = E \cup S_j\)
		- do algoritmu přidáme ty množiny, které jsme splnili ostře
{% endmath %}

{% math observation %}po přidání do algoritmu se \(y_e\) prvku nezmění (ostře splníme nějakou rovnost){% endmath %}

{% math theorem %}algoritmus je \(f\)-aproximační.{% endmath %}

{% math proof %}
\[
\begin{aligned}
	\mathrm{ALG} &= \sum_{j \in I} c_j & // \text{definice} \\
	&= \sum_{j \in I} \sum_{e \in S_j} y_e & // \text{definice} \\
	&\le \sum_{e = 1}^{n} f \cdot y_e & // \text{prohození sumy + definice $f$} \\
	&\le f \cdot \mathrm{OPT} & // \text{hodnota duálního řešení} \\
\end{aligned}
\]
{% endmath %}

##### \(g\)-aproximační algoritmy
{% math algorithm "hladový" %}
1. \(I = \emptyset, E = \emptyset, \mathcal{q}_e = 0\)
	- \(\mathcal{q}\) je vektor indexovaný množinami, pomůže nám při analýze algoritmu
2. opakovaně ber „nejlepší“ množinu: přidáme množinu s minimálním \(\left(p_j = \frac{c_j}{|S_j \setminus E}|\right)\)
	- \(p_j\) odpovídá tomu, kolik zaplatíme za pokrytí nového prvku
	- \(\forall e \in S_j \setminus E: \mathcal{q}_e = p_j\) (uložíme cenu nově pokrytých prvků)
	- \(I = I \cup \left\{j\right\}, E = E \cup S_j\)
{% endmath %}

{% math theorem %}algoritmus je \(\left(H_g \approx \ln g \le \ln n\right)\)-aproximační{% endmath %}

{% math observation %}algoritmus nemůže být lepší{% endmath %}

TODO: obrázek

{% math observation %}\(\mathrm{ALG} = \sum_{e = 1}^{n} \mathcal{q}_e\)
- vyplývá z toho, že jsme cenu \(p_j\) při přidávání rozdělili do \(\mathcal{q}_e\)
{% endmath %} 

{% math lemma %}\(\overline{\mathcal{q}} = \frac{1}{H_g} \cdot \mathcal{q}\) je přípustné řešení duálního LP{% endmath %}

{% math proof %}chceme dokázat, že \(\sum_{e \in S_j} \overline{\mathcal{q}_e} \le c_j\){% endmath %}
