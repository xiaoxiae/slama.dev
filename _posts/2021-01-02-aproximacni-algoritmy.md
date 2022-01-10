---
language: cz
title: Aproximační Algoritmy
category: "lecture notes"
---

- .
{:toc}

{% lecture_notes_preface Jiřího Sgalla|2021/2022%}

### 1. přednáška

#### Základní definice

{% math definition "Optimalizační problém" %} je \(\mathcal{I}, \mathcal{F}, f, g\)
- \(\mathcal{I} \ldots\) množina všech vstupů/instancí
- \(\forall I \in \mathcal{I}: \mathcal{F}(I) \ldots\) množina přípustných řešení
- \(\forall I \in \mathcal{I}, A \in \mathcal{F}(I): f(I, A) \ldots \) účelová funkce
- \(g \ldots\) bit (zda chceme maximalizovat nebo minimalizovat
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

### 2. přednáška

#### Metrický TSP
- _Vstup:_ metrika \(V, d\) na úplném ohodnoceném grafu
	- metrika \(\equiv\) vrcholy splňují následující:
		1. trojúhelníkova nerovnost
		2. symetrie
		3. \(d(x, y) = 0 \iff x = y\)
	- pokud by to nebyla metrika, tak poly algoritmus neexistuje (jde převést na normální TSP)
- _Výstup:_ cyklus \(C\) na všech vrcholech \(V\)
- _Cíl:_ minimalizovat \(d(C)\)

##### Kostrový algoritmus
1. najdeme minimální kostru
2. navštívíme všechny vrcholy (například přes DFS), čímž dostaneme tah přes všechny vrcholy
3. zkrátíme ji na cyklus tak, že vynecháme opakující-se vrcholy

{% math theorem %}Algoritmus je \(2\)-aproximační.{% endmath %}

{% math proof %}Kostra je nejvýše tak velká, jako optimální řešení a tenhle algoritmus je lepší než \(2\) kostry (díky trojúhelníkové nerovnosti a symetrii -- procházíme i tam i zpět){% endmath %}

##### Christofidesův algoritmus
{% math observation %}brát hrany dvakrát je plýtvání -- pospojujeme liché vrcholy přes minimální párování, abychom nemuseli chodit tam a zpět{% endmath %}

1. najdeme minimální kostru \(T\)
2. najdeme minimální perfektní párování \(M\) na vrcholech s lichými stupni v \(T\)
	- vždy existuje, jelikož máme úplný graf a vrcholů s lichým stupňem je sudý počet (všech je sudý)
3. zkrátíme na cyklus \(T \cup M\)

{% math theorem %}Algoritmus je \(3/2\)-aproximační.{% endmath %}

{% math proof %}\[\mathrm{ALG} \le d(T) + d(M) \le \mathrm{OPT} + \frac{1}{2}\mathrm{OPT}\]

Důkaz \(d(M) \le \frac{1}{2}\mathrm{OPT}\) uděláme obrázkem:

Alespoň jeden z párování v cylku bude \(\le \frac{1}{2} \mathrm{OPT}\).
{% endmath %}

{% math remark %}
- dnes umíme \(\frac{3}{2} - \varepsilon\).
- TSP v rovině: existuje \((1 + \varepsilon)\)-aproximační schéma (ale stále je \(\mathrm{NP}\) těžký)
{% endmath %}

#### Pravděpodobnost v algoritmech
1. algoritmy s chybou: někdy dělají chybu, ale většinou ji neudělají
2. bez chyb, běží v průměrném čase polynomiálním

- třída \(\mathrm{NP}\): jazyky, pro které existuje polynomiální algoritmus \(A\), který ověří správnost:
	- \(\forall a \in L\ \exists b: A(a, b) = 1\)
	- \(\forall a \not\in L\ \forall b: A(a, b) = 0\)

- třída \(\mathrm{RP}\): jazyky, pro které existuje polynomiální algoritmus \(A\), který ověří správnost:
	- \(\forall a \in L\ \mathrm{Pr}_b\left[A(a, b)\right] \ge \frac{1}{2}\)
	- \(\forall a \not\in L\ \mathrm{Pr}_b\left[A(a, b)\right] = 0\)

#### Quicksort
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

### 3. přednáška

TODO

### 4. přednáška

#### Globální minimální řez
- _Vstup:_ neorientovaný graf \((V, E)\)
- _Výstup:_ \(F \subseteq E\) tak, že \(V, E \setminus F\) není souvislý
- _Cíl:_ minimalizovat \(|F|\)

##### Klasický algoritmus
1. převedeme graf na ohodnocený s jednotkovými cenami
2. zafixujeme \(s\)
3. pro všechna \(t\) najdeme minimalní řez
4. vrátíme minimální, který jsme našli

- umíme vyřešit řádové v \(\mathcal{O}(n^3)\)

##### Náš algoritmus
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
	&= \frac{n - 2}{n} \frac{n - 3}{n - 1} \frac{n - 4}{n - 2} \ldots \frac{2}{4} \frac{1}{3}
\end{aligned}
\]

Pokrácením dostáváme \(\frac{2}{n \cdot (n - 1)} = \frac{1}{\binom{n}{2}}\).
{% endmath %}

{% math consequence %}Každý graf \(G\) má \(\le \binom{n}{2}\) globálních minimálních řezů.{% endmath %}
- jeden takový je například cyklus -- ten má opravdu řádově tolik řezů

{% math proof %}Každý běh algoritmu vystoupí právě jeden řez. Kdyby jich bylo více, tak nám pravděpodobnost nevychází (jevy jsou disjunktní).{% endmath %}

{% math theorem %}Pro \(n^2\) opakování algoritmu výše dostáváme nejmenší řez s pravděpodobností \(\ge \frac{1}{2}\){% endmath %}

{% math proof %}\(\mathrm{Pr}\left[\text{A uspěje}\right] \ge 1 - \left(1 - \frac{2}{n(n-1)}\right)^{n^2}\){% endmath %}

{% math remark %}Algoritmus můžeme vylepšit tak, že části, ve kterých se nejvíce dělají chyby (konkrétně ty pozdější) opakujeme vícekrát (a vezmeme minimum).{% endmath %}

#### Rozvrhování
