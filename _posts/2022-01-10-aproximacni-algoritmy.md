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
Pro minimalizační zajišťujeme, že naše je vždy dostatečně malé.

Pro maximalizační zajišťujeme, že je vždy dostatečně velké.
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

### Konflikty v distribuovaných systémech
- \(n\) procesorů se snaží o přístup k jednomu zdroji
- přímá komunikace není možná
- v každém cylku může každý procesor požadovat přístup
	- povede se pouze, když o něho žádá jeden

{% math algorithm %}
1. v každém cylku zkus s pravděpodobností \(p\) přistoupit ke zdroji
2. opakuj, dokud se ti to nepovede
{% endmath %}

{% math theorem %}algoritmus s \(p = \frac{1}{n}\) s pravděpodobností alespoň \(1 - \frac{1}{n}\) uspěje po \(t = 2 en \ln n\) cyklech.{% endmath %}

{% math proof %}
Modifikujme algoritmus, aby zkoušel přistupovat i po té, co ho získal (lehčí počítání, které pouze zhorší pravděpodobnost úspěchu).

Nechť \(A_{i, r}\) je jev, že \(i\)-tý proces upěl v \(r\)-tém cyklu. Pak
\[\mathrm{Pr}\left[A_{i, r}\right] = p \cdot \left(1 - p\right)^{n - 1} = \frac{1}{n} \left(1 - \frac{1}{n}\right)^{n - 1} \ge \frac{1}{en}\]

Nyní počítáme \(F_{i, t}\) které říká, že \(i\)-tý proces neuspěje v žádném z \(t = 2 en \ln n\) cyklů:
\[\mathrm{Pr}\left[F_{i, t}\right] = \prod_{r = 1}^{t} \left(1 - A_{i, r}\right) \le \left(1 - \frac{1}{en}\right)^t = \left(\left(1 - \frac{1}{en}\right)^{en}\right)^{\frac{t}{en}} \le n^{-2}\]

To, že neexistuje proces, který neuspěje, odhadneme jako
\[\mathrm{Pr}\left[\bigcup_{i = 1}^{n} F_{i, t}\right] \le \sum_{i = 1}^{n} \mathrm{Pr}\left[F_{i, t}\right] \le n \cdot n^{-2} = n^{-1} = \frac{1}{n}\]
{% endmath %}


### Globální minimální řez
- _Vstup:_ neorientovaný graf \((V, E)\)
- _Výstup:_ \(F \subseteq E\) tak, že \(V, E \setminus F\) není souvislý
- _Cíl:_ minimalizovat \(|F|\)

#### Přímočarý algoritmus
1. převedeme graf na ohodnocený s jednotkovými cenami
2. zafixujeme \(s\)
3. pro všechna \(t\) najdeme minimalní řez
4. vrátíme minimální, který jsme našli

- umíme vyřešit řádové v \(\mathcal{O}(n^3)\)

#### Spojující algoritmus
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

#### Largest Processing Time (LPT)
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

#### Odbočka: online algoritmy
- vstup přichází postupně
- řešení musíme konstruovat postupně po krocích a pak už neměníme
- **hladový** je online, **lokální prohledávání** není
- pro \(m = 2\): lepší než \(3/2\)-aproximační neexistuje (úlohy délky \(\left\{1, 1, 2\right\}\))
- pro \(m = 3\) je opět hladový nejlepší, ale pro více strojů to už tak není

#### Bin packing
- _Vstup:_ \(a_1, \ldots, a_n \ge 0\)
- _Výstup:_ rozklad \(\left\{1, \ldots, n\right\} = I_1 \cup \ldots \cup I_m\) tak, že \(\forall i: \sum_{j \in I_i} a_j \le 1\)
	- \(\equiv\) součet věcí v každém koši může být nejvýše \(1\)
- _Cíl:_ minimalizovat \(m\) (počet košů)

{% math algorithm "first fit" %}dej \(a_j\) do prvního koše, do kterého se vejde.{% endmath %}

{% math algorithm "best fit" %}dej \(a_j\) do nejplnějšího koše, do kterého se vejde.{% endmath %}

{% math theorem %}oba algoritmy jsou \(1.7\)-aproximační (a je to těsný odhad).{% endmath %}

{% math theorem %}Je NP těžké najít \(R\)-aproximační algoritmus pro \(R \le 3/2\){% endmath %}

{% math proof %}Je NP těžké rozhodnout, zda \(\mathrm{OPT} = 2\), jelikož pomocí něho můžeme přímočaře vyřešit problém dělení množiny na dvě časti se stejným součtem (nastavíme velikost košů na tenhle součet), což je NP těžké.{% endmath %}

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

{% math algorithm "hladový pro nejednotkovou kapacitu" %}
1. zvolíme \(\beta = \left\lceil m^{\frac{1}{c + 1}} \right\rceil\)
2. najdeme nejkratší cestu mezi nespojenou dvojicí (přes všechna \(i\))
	- pokud neexistuje nebo \(d(P_i) \ge \beta^c\), vystoupíme
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
- _Cíl:_ maximalizovat \(\sum w_i\)

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
- předpoklad: \(\forall i: \sum_{j: C_j = x_i} w_j \ge \sum_{j: C_j = \overline{x}_i} w_j\)
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
	\mathrm{Pr}\left[C_j\ \text{není splněná}\right] &= \overbrace{\prod_{i: x_i \in C_j} (1 - y^*_i)}^{\text{kladné}} \overbrace{\prod_{i: \overline{x}_i \in C_j} y^*_i}^{\text{záporné}} & \\
	&\overset{A}{=} \left[\frac{1}{k_j} \left(\sum_{i: x_i \in C_j} (1 - y^*_i) + \sum_{i: \overline{x}_i \in C_j} y^*_i\right)\right]^{k_j} & \\
	&= \left[1 - \frac{1}{k_j} \left(\sum_{i: x_i \in C_j} y^*_i + \sum_{i: \overline{x}_i \in C_j} (1 - y^*_i)\right)\right]^{k_j} & \\
	&\le \left(1 - \frac{z_j^*}{k_j}\right)^{k_j} \qquad & //\text{definice LP}
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
| \(\ge3\)   | \(\ge \frac{7}{8} z_j^*\)             | \(\ge\left(1 - \frac{1}{e}\right) \cdot z_j^*\) | \(> \frac{3}{4} z_j^*\)                                               |
{% endmath %}

##### Derandomizace metodou podmíněných pravděpodobností
Neformálně: postupně plníme klauzule tak, že náhodně vybíráme pravděpodobnosti. Jelikož počet splnění určuje to, jak hodnoty vybereme, tak je můžeme vybírat (_podmíněně_ se rozhodujeme, jak to dopadne, když \(x_i = 0\) nebo \(x_i = 1\) a vybereme si to lepší). Aproximační poměr si neshoršíme, jelikož vždy vybírám větší z pravděpodobností.

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
- _Vstup:_ množiny \(S_1, \ldots, S_m \subseteq \left\{1, \ldots, n\right\}\), ceny \(c_1, \ldots, c_m \ge 0\)
- _Výstup:_ \(I \subseteq \left\{1, \ldots, m\right\}\) t. ž. \(\bigcup_{i \in I} S_i = \left\{1, \ldots, n\right\}\)
- _Cíl:_ minimalizovat \(\sum_{i \in I} c_i\)

Pro rozbor budeme potřebovat ještě dva parametry:
- \(f = \max_{e = 1}^{n} |\left\{j \mid e \in S_j\right\}|\ \ \)(v kolika nejvíce množinách je nějaký prvek)
- \(g = \max_{j = 1}^{m} |S_j| \le n\ \ \) (velikost největší množiny)

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
	- podmínky jsou \(\forall e \in \left\{1, \ldots, n\right\}: \sum_{j \mid e \in S_i} x_j \ge 1\) (chceme pokrýt všechny prvky univerza)
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

**Význam duálu (procejce):** kolik můžu nejvíce účtovat za každou známku, aby byl obchod ochotný kupovat známky a tvořit z nich balíčky.
</div>

{% math observation %}duál programu vypadá následně:
- proměnné jsou \(y_1, \ldots, y_n \ge 0\) pro každý **prvek**
- podmínky jsou \(\forall e \in \left\{1, \ldots, m\right\}: \sum_{e \in S_j} y_e \le c_j\)
- maximalizujeme \(\sum_{e \in S_j} y_e\)
{% endmath %}

{% math observation %}podmínky komplementarity:
- \(\forall j: x^*_j = 0 \lor \sum y_e^* = c_j\)
	- pokud by prodejce na obálce vydělal, tak ji sběratel nekoupí
	- pokud prodejce na známce nevydělává, tak ji sběratel koupí
- \(\forall e: y^*_e = 0 \lor \sum_{j \mid e \in S_j} x_j^* = 1\)
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
		- do algoritmu přidáme ty množiny, jejichž podmínky komplementarity jsme naplnili
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
	- \(\mathcal{q}\) je vektor indexovaný prvky, pomůže nám při analýze algoritmu
2. opakovaně ber „nejlepší“ množinu: přidáme množinu s minimálním \(\left(p_j = \frac{c_j}{|S_j \setminus E|}\right)\)
	- \(p_j\) odpovídá tomu, kolik zaplatíme za pokrytí nového prvku
	- \(\forall e \in S_j \setminus E: \mathcal{q}_e = p_j\) (uložíme cenu nově pokrytých prvků mezi to, kolik jich bylo)
	- \(I = I \cup \left\{j\right\}, E = E \cup S_j\) (přidáme tuto množinu a pokryté prvky)
{% endmath %}

{% math theorem %}algoritmus je \(\left(H_g \approx \ln g \le \ln n\right)\)-aproximační{% endmath %}

{% math observation %}algoritmus nemůže být lepší (viz následující protipříklad):{% endmath %}

{% xopp counter %}

{% math observation %}\(\mathrm{ALG} = \sum_{e = 1}^{n} \mathcal{q}_e\)
- vyplývá z toho, že jsme cenu \(p_j\) při přidávání rozdělili do \(\mathcal{q}_e\)
{% endmath %} 

{% math lemma %}\(\overline{\mathcal{q}} = \frac{1}{H_g} \cdot \mathcal{q}\) je přípustné řešení duálního LP{% endmath %}

{% math proof %}chceme dokázat, že \(\sum_{e \in S_j} \overline{\mathcal{q}_e} \le c_j\)
- nechť \(S_j = \left\{e_1, \ldots, e_k\right\}\)
	- očíslujeme tak, že \(e_k\) je první pokrytý, \(e_{k-1}\) druhý, až \(e_1\) poslední

{% math observation %} \(\mathcal{q}_{e_i} \le \frac{c_j}{i}\)
- v \(i\)-tém kroku ještě nejsou pokryté prvky \(1, \ldots, i\)
- z definice vybíráme nejlevnější možnou množinu
{% endmath %}

Nyní dostáváme
\[\sum_{e \in S_j} \mathcal{q}_e = \sum_{1}^{k} \mathcal{q}_{e_i} \le \frac{c_j}{1} + \frac{c_j}{2} + \ldots = H_k \cdot c_j \\
\sum_{e \in S_j} \overline{\mathcal{q}}_e = \frac{1}{H_g} \sum_{e \in S_j} \mathcal{q}_e \le \frac{1}{H_g} \cdot H_k \cdot c_j \le c_j
\]

{% endmath %}

#### Maximální nezávislá množina
- _Vstup:_ graf \(G = (V, E)\)
- _Výstup:_ \(I \subseteq V\) nezávislá množina, maximální **vzhledem k inkluzi**
	- největší moc dobře řešit nejde (ani aproximovat)

Nás zajímá najít rychlý paralelní algoritmus:
- operací chceme udělat řádově \(\mathcal{O}\left(\log n\right)\)
- k dispozici máme řádově \(m\) procesorů (každý vrchol/hrana má jeden)
- povolujeme procesorům najednou šahat na data a najednou měnit data **na stejnou věc**

{% math algorithm "rychlý paralelní" %}
1. \(I = \emptyset\)
2. dokud \(V \neq \emptyset\)
	1. \(\forall v \in E\) pokud je stupeň \(0\), pak přidáme do \(I\) a vymažeme z \(V\)
	2. \(\forall v \in E\) označ \(v\) (přidej do \(S\)) s pravděpodobností \(\frac{1}{2 d_v}\) (nezávisle)
	3. \(\forall u, v \in E\) pokud \(u\) i \(v\) jsou označené, odeber značku nižšího stupně
	4. přidej označené vrcholy do \(I\) a odeber je **a jejich sousedy** (a odpovídající hrany) z \(V\)
		- sousedy množiny \(S\) značíme \(N(S)\)
{% endmath %}

{% math definition %}vrchol je **dobrý**, jestliže má \(\ge \frac{d_v}{3}\) sousedů stupně \(\le d_v\)
- má velkou pravděpodobnost, že ho vyřešíme výběrem souseda, protože má hodně sousedů malého stupně
- analogicky špatný vrchol a dobrá (obsahuje dobrý vrchol) a špatná hrana
{% endmath %}

{% math lemma %}alespoň polovina hran je dobrá.{% endmath %}

{% math proof %}hrany zorientujeme od menšího k většímu stupni (rovnost řešíme libovolně)
- \(v\) špatný \(\implies d_v^{\mathrm{in}} < \frac{d_v}{3}\)
	- z definice -- vstupující jsou stejného menšího stupně, takže by jinak byl dobrý
	- tedy \(\ge \frac{2 d_v}{3}\) vstupuje a platí \(d_v^{\mathrm{in}} \le \frac{1}{2} d_v^{\mathrm{out}}\)

Nyní počítáme
\[
\begin{aligned}
	|\text{špatné hrany}| &\le \sum_{v\ \text{špatný}} d_v^{\mathrm{in}} &\qquad //\text{špatná hrana jde do špatného vrcholu} \\
	&\le \sum_{v\ \text{špatný}} \frac{1}{2} d_v^{\mathrm{out}} &\qquad //\text{nerovnost výše} \\
	&\le \frac{1}{2}|E| &\qquad //\text{posčítáním přes všechny vrcholy platí}
\end{aligned}
\]
{% endmath %}

{:.rightFloatBox}
<div markdown="1">
Pravděpodobnost, že dobrý vrchol odstraním (buď označením toho vrcholu samotného nebo nějakého jeho souseda) je nějaká konstanta.
</div>

{% math lemma %}existuje \(\alpha > 0\) t. ž. \(\forall v\) **dobrý** platí \[\mathrm{Pr}\left[v \in S \cup N(S)\right] \ge \alpha\]
{% endmath %}

{% math proof %}
Pro dobrý vrchol \(v\) platí následující:
\[
\begin{aligned}
	\mathrm{Pr}\left[v\ \text{má souseda označeného v kroku 2}\right] &\ge 1 - \prod_{w \in N(v)} \overbrace{\left(1 - \frac{1}{2d_w}\right)}^{\text{neoznačíme souseda}} \\
	& \ge 1 - \left(1 - \frac{1}{2d_v}\right)^{\frac{d_v}{3}} \qquad // \text{lemma výše}\\
	& = \text{konstanta} \\
\end{aligned}
\]

Pro libovolný vrchol \(v\) platí následující (jen pozor, v \(\mathrm{Pr}\) používáme podmíněně, že \(v\) byl označený):
\[
\begin{aligned}
	\mathrm{Pr}\left[\text{odstraníme značku u}\ v\right] &= \mathrm{Pr}\left[\exists u \in N(v): d_u \ge d_w \land u\ \text{byl označený}\right] \\
	&\le \sum_{u \in N(v) \mid d_u \ge d_v} \mathrm{Pr}\left[u\ \text{byl označený}\right] \\
	&\le \sum_{w \in N(v)} d_w \cdot \frac{1}{2d_w} \le \frac{1}{2}
\end{aligned}
\]

{% endmath %}

TODO: tohle dodělat (že to nakonec vyjde logaritmicky, protože dobrých vrcholů odstraňuju konstantní část)

TODO: derandomizace pomocí 2-nezávislých proměnných

### Hashovací funkce

{:.rightFloatBox}
<div markdown="1">
**2-Univerzalita:** pro dva rozdílné prvky máme pro náhodnou hashovací funkci z rodiny omezenou pravděpodobnost, že se namatchují na stejnou hodnotu.

**Silná 2-univerzalita:** zahashované hodnoty \(x_1, x_2\) tvoří dvě náhodné po dvou nezávislé veličiny. Takže kromě toho, že jsou univerzální (když zafixuju jeden, tak se tím druhým trefím s pravděpodobností \(\frac{1}{n}\) to platí i pro libovolnou dvojici, na kterou prvky mapuju.
</div>
{% math definition %}nechť \(M, |M| = m, N, |N| = n, H \subseteq \left\{f \mid f : M \mapsto N\right\}\)
- systém \(H\) je \(2\)-univerzální, jestliže
\[\left(\forall x_1, x_2 \in M, x_1 \neq x_2\right)\\
\mathrm{Pr}_{h \in H} \left[h(x_1) = h(x_2)\right] \le 1 / n\]

- systém \(H\) je **silně** \(2\)-univerzální, jestliže
\[\left(\forall x_1, x_2 \in M, x_1 \neq x_2\right) \left(\forall y_1, y_2 \in N\right)\\
\mathrm{Pr}_{h \in H} \left[h(x_1) = y_1 \land h(x_2) = y_2\right] = 1/n^2\]

{% endmath %}

{% math example %}pro \(M = N\) je těleso máme silně 2-univerzální systém
\[H = \left\{h_{a,b} \mid a, b \in N\right\} \quad h_{a, b}: x \mapsto ax + b\]
{% endmath %}

{% math example %}pro \(|M| \gg |N|\) můžeme vzít \(\overline{H} \subseteq \left\{f \mid f: M \mapsto M\right\}\) a vytvořit z něho \(H \subseteq \left\{f \mid f: M \mapsto N\right\}\) tím, že budeme brát funkce \(\mathrm{mod} n\)
- \(\overline{H}\) silně \(2\)-univerzální \(\implies H\) univerzální
	- pokud \(n \mid m\), tak máme silnou univerzalitu
{% endmath %}

#### Dynamický slovník
{% math example "dynamický slovník" %} universum \(M\), \(|M| = 2^d\), slovník \(S \subseteq M, |S| = s\)
- reprezentujeme \(S\) tabulkou \(N, |N| = n = \mathcal{O}(s)\)
- operace (trvá průměrně \(\mathcal{O}(1)\)):
	- vložení do \(S\)
	- vyhledávání \(x\) v \(S\)
	- vymazání \(x\) z \(S\)

Zvolíme \(n \in \left[s, 2s\right], H, h \in H\) náhodně uniformně:
- \(h(x)\) je očekávaná pozice v poli
- kolize se přidávají do spojového seznamu pole (\(n_i\) je počet prvků)
{% endmath %}

{% math lemma %}pokud \(n = \mathcal{O}(s)\), tak průměrná doba operace je \(\mathcal{O}(1)\){% endmath %}

{% math proof %}chceme (\(\forall x \in S)\ \mathbb{E}\left[n_{h(x)}\right] = \mathcal{O}(1)\). Budeme počítat počet kolizí na jeden prvek:
- nechť \(X_y = \begin{cases} 1 & h(y) = h(x) \\ 0 & \text{jinak} \end{cases}\)
- jelikož \((\forall x, y, x \neq y)\ h(x), h(y)\) jsou nezávislé, tak \(\mathbb{E}\left[X_y\right] = \frac{1}{n}\):

\[\mathbb{E}\left[n_{h(x)}\right] = \overset{\text{prvek}\ x}{1} + \overbrace{\sum_{y \neq x} \mathbb{E}\left[X_y\right]}^{\#\ \text{kolizí} = \text{délka}\ n_{h(x)}} = 1 + \frac{s - 1}{n} = \mathcal{O}(1)\]
{% endmath %}

#### Statický slovník
{% math example "statický slovník" %} \(S\) je dáno předem
- vytvoříme datastrukturu v polynomiálním čase
- chceme, aby operace vyhledání běžela v **maximálním** čase \(\mathcal{O}\left(1\right)\)
	- to jsme předtím neměli -- seznam mohl být dlouhý a maximální počet operací velký
- použijeme tabulky dvě:
	- hashujeme dvakrát -- jednou pro index do první tabulky, ta určí funkci pro druhé hashování
	- v první budeme chtít \(\le n\) kolizí, ve druhé \(= 0\)

{% xopp static %}

- vybereme \(h \in H\) tak, že má \(\le n\) kolizí
	- kolize \(C = \left\{\left\{x, y\right\} \mid x, y \in M, x \neq y, h(x) = h(y)\right\}\)

{% math lemma %}taková \(h \in H\) existuje{% endmath %}

{% math proof %} \(\mathbb{E}\left[|C|\right] \overset{2-\text{univ}}{=} \binom{S}{2} \frac{1}{n} \overset{n \ge s}{=} \binom{n}{2} \cdot \frac{1}{n} \le \frac{n}{2}\){% endmath %}
- jelikož je průměrný počet kolizí \(\le \frac{n}{2}\), tak musí existovat hodně takových, že \(\le \frac{n}{2}\)

{% math lemma %}taková \(h_i \in H_i\) existuje{% endmath %}

- vybereme \(h_i \in H_i\) tak, že má \(0\) kolizí

{% math proof %} \(\mathbb{E}\left[|C_{n_i}|\right] = \binom{n_i}{2} \cdot \frac{1}{n_i^2} \le \frac{1}{2}\){% endmath %}
- jelikož je průměrný počet kolizí \(\le \frac{1}{2}\), tak musí existovat hodně takových, že \(0\)
{% endmath %}

{% math observation %}\(|C| = \sum_{i = 1}^{n} \binom{n_i}{2} =	\sum \frac{n_i^2}{2} - \sum \frac{n_i}{2}\)
- počet prvků kolidující do daného políčka je \(n_i\), počet dvojic je tedy výraz nahoře

Výpočtem dostáváme \(\sum n_i^2 \le 2 |C| + \sum n_i \le 2s + s = \mathcal{O}(s)\)
{% endmath %}

### Testování

#### Násobení matic
- pomalé násobení: \(\mathcal{O}(n^3)\)
- nejlepší známé: \(\mathcal{O}(n^{\omega})\)
	- \(\omega = 2.37\)

- _Vstup:_ \(A, B, C \subseteq K^{n \times n}\) (pro těleso \(K\))
- _Výstup:_ ANO, pokud \(A \cdot B = C\), jinak NE

{% math lemma %}nechť \(\vec{a} \in K^n, \vec{a} \neq 0\) a \(\vec{x} \in \left\{0, 1\right\}^n\) uniformně náhodný. Pak \[\mathrm{Pr}_{\vec{x}} \left[\vec{a}^T \cdot \vec{x} \neq 0\right] \ge \frac{1}{2}\]{% endmath %}

{% math proof %}uvažme poslední nenulovou souřadnici \(\vec{a}_k\). Ta má hodnotu \(0\) nebo \(\vec{a}_k\), podle vybraného bitu. \(0\) bude tedy právě tehdy, když součet předchozích vyšel \(a_k\) (a opakujeme s \(k-1, \ldots\)).{% endmath %}

{% math theorem %}existuje pravděpodobnostní algoritmus s jednostrannou chybou pro testování maticového násobení v čase \(\mathcal{O}\left(n^2\right)\)
- když platí, tak vždy řekne že platí
- když neplatí, tak se netrefí s nějakou pravděpodobností (konkrétně \(\ge \frac{1}{2}\))
{% endmath %}

{% math algorithm %}
1. vezmi náhodný \(\vec{x} \in \left\{0, 1\right\}^n\)
2. vstup ANO, jestliže \(A \cdot B \cdot \vec{x} = C \cdot \vec{x}\), jinak NE
{% endmath %}

{% math observation %}algoritmus trvá \(\mathcal{O}(n^2)\) kroků{% endmath %}

{% math observation %}algoritmus řekne ano \(\iff \left(A \cdot B - C\right) \cdot \vec{x} = D \cdot \vec{x} = \vec{0}\)
- \(D\) je nenulová matice (jelikož \(A \cdot B \neq C\)), má tedy **nenulový řádek**
	- podle lemmatu platí \(\mathrm{Pr}_{\vec{x}} \left[D \cdot \vec{x} \neq 0\right] \ge \frac{1}{2}\)
{% endmath %}

#### Nulovost polynomů (Polynomial Identity Testing)
- nezajímá nás, jestli je identicky nulový, ale zda je nulový **v tělese**, ve kterém pracujeme
- uvažujeme více proměnných
	- \(d \ldots\ \) celkový stupeň (t. j. součet stupňů v nějakém nenulovém monomu)
- převeditelné na to, zda je výrok tautologie (jdou na sebe převést) \(\implies\) NP těžké

Budeme používat trochu divný vstup:
- _Vstup:_ matice polynomů proměnných, determinant určuje náš polynom
- _Výstup:_ ANO, jestliže je polynom identicky nulový, jinak NE

{% math lemma %}nechť \(P(x_1, \ldots, x_n)\) je nenulový polynom nad \(K\) stupně \(\le d_i\) a \(S \subseteq K\) konečná. Nechť \(x_1, \ldots, x_n \in S\) unif. náhodně. Pak \[\mathrm{Pr}_{\vec{x}} \left[P(\vec{x}) = 0\right] \le \frac{d}{|S|}\]
- \(n = 1 \ldots\ \) polynom má nejvýše \(d\) kořenů, ať zvolíme \(s\) jakkoliv
- je to dost šikovné, protože podle \(|S|\) si volíme přesnost algoritmu (pro \(|S| \ge 2d\) máme \(\ge \frac{1}{2}\))
{% endmath %}

{% math proof %}pro \(n =1\) platí. Nyní indukcí podle \(n\). Rozdělíme polynom na \(A\) a \(B\), kde stupeň v \(B\) je ostře menší \(k\). To umíme tím, že vytkneme nějakou proměnnou:
- \(P(\vec{x}) = x_1^k \cdot A(x_2, \ldots, x_n) + B(\vec{x})\)
	- \(A\) je identicky nulový (podle IP) s pravděpodobností \(\le \frac{d - k}{|S|}\)
	- chci dokázat, že \(\mathrm{Pr}\left[P(\vec{x}) = 0 \mid A(x_2, \ldots, x_n) \neq 0\right] \le \frac{k}{|S|}\)
		- při konkrétních hodnotách \(x_2, \ldots, x_n\) se mi polynom vyhodnotí na nějaké číslo a zbytek polynomu \(P(\vec{x})\) bude \(\alpha x_1^k + \beta\), což nebude mít více než \(k\) kořenů
{% endmath %}

Nyní si uvědomíme, že \[\mathrm{Pr}\left[P(\vec{x}) = 0\right] \le \alpha + \beta \le \frac{d - k}{|S|} + \frac{k}{|S|} = \frac{d}{|S|}\]

### Perfektní párování
Nechť \((U, V, E)\) je bipartitní graf, \(n = |U| = |V|\). Pak Edmondsova matice grafu je \(n \times n\) matice \(B\) s
\[B_{u, v} = \begin{cases} x_{u, v} & uv \in E \\ 0 & uv \not\in E \end{cases}\]
- za každou hranu bude v matici jedna proměnná

{% math observation %}\(\det(B)\) je polynom, jehož monomy vzájemně jednoznačně odpovídají perfektním párovaním.
- sčítáme součin permutace matice a když se zrovna trefíme do párovaní, tak máme monom
{% endmath %}

{% math algorithm "test existence PP" %}
1. zvolme uniformně náhodně nezávisle \(x_{u, v} \in \left\{1, \ldots, 2n\right\}\)
	- \(2n\) kvůli tomu, aby nám vyšlo NE správně s pravděpodobností \(\ge \frac{1}{2}\)
2. spočítáme determinant
	- pokud je nenulový, párování určitě existuje
	- pokud je nulový, tak párování neexistuje s pravděpodobností \(\ge \frac{1}{2}\)
{% endmath %}

#### Izolující lemma

{:.rightFloatBox}
<div markdown="1">
Prvky \(a_i\) budou hrany v grafu a množiny \(S_j\) budou perfektní párování.

Chceme nějak zvolit váhy a ukázat, že nám nějak jednoznačně identifikují nějakou z množin (tedy perfektních párování).
</div>

{% math theorem %}Nechť máme systém množin \(S_1, \ldots, S_n \subseteq \left\{a_1, \ldots, a_m\right\}\) s náhodně zvolenými vahami \(w(a_1), \ldots, w(a_m) \in R\). Pak \[\mathrm{Pr}\left[\exists\ \text{právě jedinná}\ S_j\ \text{s minimální}\ w(S_j)\right] \ge 1 - \frac{m}{r}\]
{% endmath %}

{% math proof %}\(A_i \ldots\ \) jev, že existují \(S_k, S_l\) tak, ze \(w(S_k) = w(S_l) = \min_j w(S_j)\) a \(a_i \not\in S_k, a_i \in S_l\)
- existují dvě minimální množiny, které se liší v prvku \(i\) (špatný jev)
- když nenastane žádný s jevů \(A_i\), pak máme vyhráno, jelikož dvě minimální neexistují
	- máme systém množin -- nestane se, že by dvě stejnoprvkové množiny měly stejnou váhu

Ukážeme, že \(\mathrm{Pr}\left[A_i\right] \le \frac{1}{r}\)

\(S_1, \ldots, S_n\) rozdělím na 
- \(\mathcal{S}_0 = \left\{j \mid a_i \not\in S_j\right\}\)
- \(\mathcal{S}_1 = \left\{j \mid a_i \in S_j\right\}\)

Pokud \(A_i\) nastane, pak platí 
- pro \(S_k\): \(k \in \mathcal{S}_0, w(S_k) = \min_{j \in \mathcal{S}_0} w(S_j)\)
- pro \(S_l\): \(l \in \mathcal{S}_1, w(S_l) = \min_{j \in \mathcal{S}_1} w(S_j)\)

Pak (když zafixujeme všechny váhy a vybíráme váhu \(a_i\)) platí \[\mathrm{Pr}_{w(a_i) \in R}\left[w(S_k) = w(S_l) \mid w(a_i'), i' \neq i\ \text{vybrána}\right] \le \frac{1}{r}\]
{% endmath %}

{% math algorithm "rychlý paralelní algoritmus pro PP" %}
1. zvolíme rovnoměrně náhodně váhy \(w(uv) \in \left\{1, \ldots, 2m\right\}\) pro každou hranu
2. zasubstituujeme do Edmondsovy matice následně: \(x_{uv} = 2^{w(uv)}\)
	- \(\mathrm{det}(C)\ldots\ \) příspěvek PP je \(\pm 2^{w(M)} = \pm \prod_{uv \in M} 2^{w(uv)}\)
		- z definice determinantu (permutace nějakých indexů matice)
3. najdeme \(W\) tak, že \(2^W\) je maximální číslo tvaru \(2^{\alpha}\) dělící \(\mathrm{det}(C)\)
	- zajímá nás **poslední index, kde má determinant jedničku**, jelikož to odpovídá unikátnímu PP (všechny PP jsou ve tvaru \(0b1\underbrace{0000}_{w(uv)}\)
4. pro \(uv \in E\) spočítáme \(d = \mathcal{\mathrm{det}(C^{uv})}\)
	- jestliže \(2^{W - w(uv)}\) je max. číslo tvaru \(2^{\alpha}\) dělící \(d\), pak přidáme \(uv\) do \(M\)
		- odpovídá tomu, zda párování přežilo odstranění hrany -- pokud ne, tak ho přidáme
6. zkontrolujeme, že \(M\) je PP (mohli jsme vygenerovat nesmysl)
{% endmath %}
