---
language: cz
title: Kombinatorika a Grafy I
category: "lecture notes"
---

- .
{:toc}

{% lecture_notes_preface Martina Kouteckého|2020/2021%}

### 1. přednáška

#### Odhady faktoriálu

**Věta (meh odhad):**
\[n^{n/2} \le n! \le \left(\frac{n + 1}{2}\right)^n\]

**Důkaz \(\ge\):**
\[
\begin{aligned}
	\left(n!\right)^2 &= 1 \cdot 2 \cdot 3 \cdot \ldots \cdot n \cdot n \cdot (n - 1) \cdot \ldots \cdot 2 \cdot 1 \\
	&= \prod_{i = 1}^{n} \left(i \cdot (n - i + 1)\right)
\end{aligned}
\]

Využijeme A-G nerovnost:

\[
\begin{aligned}
	\sqrt{ab} &\le \frac{a + b}{2} \\
	\sqrt{i (n + 1 - i)} &\le \frac{i + n + 1 - i}{2} = \frac{n + 1}{2}
\end{aligned}
\]

Dostáváme:
\[n! = \prod_{i = 1}^{n} \sqrt{i \cdot (n - i + 1)}\le \left(\frac{n + 1}{2}\right)^n\]

**Důkaz \(\le\):**

\(n \le i (n - i + 1), \forall i \in [n]\):
- \(i = 1\) platí
- \(i = 2 \rightarrow\)  jeden člen je vždy \(\ge 2\), druhý \(\ge n/2\)

\[
\begin{aligned}
	\left(n!\right)^2 &= \prod_{i = 1}^{n} i\left(n - i + 1\right) \ge \prod_{i = 1}^{n}n = n^n \\
	n! &\ge n^{n/2}
\end{aligned}
\]

**Věta (nice odhad):**
\[
e\left(\frac{n}{e}\right)^n \le n! \le en \left(\frac{n}{e}\right)^n
\]

**Důkaz (indukcí):**
- \(n = 1\): \[1 \le e \cdot 1 \cdot \frac{1}{e}\]
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
- pro dolní mez postupujeme podobně, ale je potřeba indukční krok dokazovat pro
  \(n \rightarrow n+1\), místo \(n-1 \rightarrow n\).

**Věta (Stirlingova formule)** (bez důkazu):
\[n! \cong \sqrt{2 \pi n} \left(\frac{n}{e}\right)^n\]

#### Odhady binomických koeficientů

(👀) pro malé \(k << n \ldots \binom{n}{k} = \frac{n!}{(n - k)! k!} = \frac{n \cdot (n - 1) \cdot \ldots \cdot (n - k + 1)}{k!} \le n^k\)

**Věta (hodně meh odhad):**
\[\frac{2^n}{n + 1} \le \binom{n}{\left\lfloor n/2 \right\rfloor} \le 2^n\]


**Důkaz:**
- součet všech čísel v řádku je \(2^n\), tak jistě to největší nebude větší
- největší sčítanec je rovněž alespoň tak velký jako průměrný

**Věta (nice odhad):**
\[\frac{2^{2m}}{2 \sqrt{m}} \le \binom{2m}{m} \le \frac{2^{2m}}{\sqrt{2m}}\]

**Důkaz:**

Nejprve jedno kouzlo:
\[
P = \frac{1 \cdot 3 \cdot 5 \cdot \ldots \cdot (2m - 1)}{2 \cdot 4 \cdot 6 \cdot \ldots \cdot 2m} = \frac{1 \cdot 3 \cdot 5 \cdot \ldots \cdot (2m - 1)}{2 \cdot 4 \cdot 6 \cdot \ldots \cdot 2m}\frac{2 \cdot 4 \cdot 6 \cdot \ldots \cdot 2m}{2 \cdot 4 \cdot 6 \cdot \ldots \cdot 2m} = \frac{(2m)!}{2^{2m} \left(m!\right)^2} = \frac{\binom{2m}{m}}{2^{2m}}
\]

Chceme tedy:
\[
\frac{1}{2 \sqrt{m}} \le P \le \frac{1}{\sqrt{2m}}
\]

Pak ještě druhé kouzlo:
\[
\begin{aligned} 
	\left(1 - \frac{1}{2^2}\right) \left(1 - \frac{1}{4^2}\right) \ldots \left(1 - \frac{1}{\left(2m\right)^2}\right) &= \left(\frac{1 \cdot 3}{2 \cdot 2}\right) \left(\frac{3 \cdot 5}{4 \cdot 4}\right) \ldots \left(\frac{(2m - 1)(2m + 1)}{\left(2m\right)^2}\right) \\
	&= P^2 (2m + 1) < 1 \qquad //\ \text{součin věcí $<1$} \\
\end{aligned}
\]

Máme tedy:
\[
\begin{aligned} 
	P^2 &< \frac{1}{2m + 1} < \frac{1}{2m} \\
	P &< \frac{1}{\sqrt{2m}} \\
\end{aligned}
\]

Druhá strana analogicky (uvažujeme \(\left(1 - \frac{1}{3^2}\right)\left(1-\frac{1}{5^2}\right)\ldots = \left(\frac{2 \cdot 4}{3^2}\right)\left(\frac{4 \cdot 6}{5^2}\right)\ldots = \frac{1}{2 \left(2m\right) P^2}\)).

### 2. přednáška

#### Náhodné procházky

**Definice náhodné procházky  (v \(\mathbb{Z}^1\)):** Náhodný proces, v každém kroku se panáček začínající v bodu \(0\) posune ze své aktuální pozice doprava nebo doleva.

- kde bude po \(n\) krocích?
- \(\lim_{n \to \infty} \ldots\) že se po \(n\) krocích vrátil (někdy v průběhu) do počátku?
- \(\lim_{n \to \infty} \ldots\) \(\mathbb{E}[\#\text{návratů do počátku}]\)?
	- dokážeme, že jde k nekonečnu

Zadefinujeme si náhodnou veličinu \(X = I_{S_2} + I_{S_4} + \ldots + I_{S_{2n}} \):
- \(I_{S_{2n}}\ldots\) indikátor, že nastal jev „po \(2n\) krocích jsem v počátku“
- \(\mathbb{E}[X] = \mathbb{E}[\#\text{návratů do počátku}]\).
- \(\Pr[\text{po $2n$ krocích jsem v počátku}] = \binom{2n}{n}/2^{2n}\).
	- nahoře jsou možnosti vyrovnaných počtů kroků doprava/doleva
	- dole jsou všechny scénáře pro \(2n\) kroků

\[
\frac{\binom{2n}{n}}{2^{2n}} \ge \frac{\frac{2^{2n}}{2 \sqrt{n}}}{2^{2n}} = \frac{1}{2 \sqrt{n}}
\]

\[
\begin{aligned}
	\mathbb{E}[X] &= \mathbb{E}\left[\sum_{i=1}^{\infty} I_{S_{2i}}\right]&& \\
	              &= \sum_{i=1}^{\infty} \mathbb{E}\left[I_{S_{2i}}\right]&&//\ \text{linearita střední hodnoty}\\
	              &= \sum_{i=1}^{\infty} \Pr\left[I_{S_{2i}}\right] &&//\ \text{střední hodnota indikátoru je pravděpodobnost}\\
	              &\ge \sum_{i=1}^{\infty} \frac{1}{2 \sqrt{i}} && //\  \text{použití odhadu výše; diverguje} \\
\end{aligned}
\]

- zajímavost: ve \(2D\) to také platí, ale ve \(3D\) už ne (konverguje k nějakému konstantnímu číslu)!

#### Generující funkce

**Definice (mocninná řada)** je nekonečná řada tvaru \(a(x) = a_0 + a_1x^1 + a_2x^2 + \ldots,\) kde \(a_0, a_1 \ldots \in \mathbb{R}\).

**Příklad:** \(a_0 = a_1 = \ldots = 1 \mapsto 1 +x + x^2 + \ldots\)
- pro \(|x| < 1\) řada konverguje k \(\frac{1}{1 - x}\), můžeme tedy říct, že \((1, 1, \ldots) \approx \frac{1}{1 - x}\)

**Tvrzení:** \((a_0, a_1, a_2, \ldots)\) reálná čísla. Předpoklad: pro nějaké \(K\) t. ž. \(|a_n| \le K^n\). Poté řada \(a(x)\) pro každé \(x \in \left(-\frac{1}{K}, \frac{1}{K}\right) \) konverguje (dává smysl). Funkce \(a(x)\) je navíc jednoznačně určena hodnotami na okolí \(0\).

**Definice (vytvořující/generující funkce):** nechť \(\left(a_0, a_1, \ldots\right)\) je posloupnost reálných čísel. Vytvořující funkce této posloupnosti je mocninná řada \(a(x) = \sum_{i = 0}^{\infty} a_i x^i\).

##### Operace na funkcích

| operace                                      | řada                                                                                                                          | úprava                                               |
| ---                                          | ---                                                                                                                           | ---                                                  |
| součet                                       | \(a_0 + b_0, a_1 + b_1, a_2 + b_2, \ldots\)                                                              | \(a(x) + b(x)\)                 |
| násobek                                      | \(\alpha a_0, \alpha a_1, \alpha a_2, \ldots \)                                                          | \(\alpha a(x)\)                 |
|                                              |                                                                                                                               |                                                      |
| posun doprava                                | \(0, a_0, a_1, \ldots \)                                                                                 | \(xa(x)\)               |
| posun doleva                                 | \(a_1, a_2, a_3, \ldots \)                                                                               | \(\frac{a(x) - a_0}{x}\) |
|                                              |                                                                                                                               |                                                      |
| substituce \(\alpha x\) | \(a_0, \alpha a_1, \alpha^2 a_2, \ldots \)                                                               | \(a(\alpha x)\)         |
| substituce \(x^n\)      | \(a_0, 0, \overset{n - 1}{\ldots}, 0, a_1, 0, \overset{n - 1}{\ldots}, 0, a_2, \ldots \)                 | \(a(x^n)\)              |
|                                              |                                                                                                                               |                                                      |
| derivace                                     | \(a_1, 2a_2, 3a_3, \ldots \)                                                                             | \( a'(x)\)               |
| integrování                                  | \(0, a_1, a_2/2, a_3/3, \ldots \)                                                                        | \( \int_{0}^{x} a(t) dt\)       |
|                                              |                                                                                                                               |                                                      |
| konvoluce                                  | \( \sum_{k = 0}^{n} a_k \cdot b_{n - k} \)                                                               | \( a(x) \cdot b(x)\)            |

Všechny důkazy jsou jednoduché rozepsání z definice.

#### Zobecněná binomická věta

**Tvrzení:** \(r \in \mathbb{R}, k \in \mathbb{N}\), def. \(\binom{r}{k} = \frac{r \cdot (r - 1) \cdot (r - 2) \cdot  \ldots  \cdot (r - k + 1)}{k!}\)
- pro \(r \in \mathbb{N}\) se shoduje s tím, co už známe
- vyplývá z toho, že funkce \((1 + x)^r\) je vytvořující funkcí posloupnosti \(\left(\binom{r}{0}, \binom{r}{1}, \binom{r}{2}, \ldots\right)\)
- (👀) pokud \(r\) je záporné celé, pak \(\binom{r}{k} = (-1)^k \binom{-r + k - 1}{k} = (-1)^k \binom{-r + k - 1}{-r - 1}\), tedy \(\frac{1}{(1 - x)^n} = (1 - x)^{-n} = \binom{n - 1}{n - 1} + \binom{n}{n - 1}x + \binom{n + 1}{n - 1}x^2 + \ldots\)

**Příklad:** V krabici je \(30\) červených, \(40\) žlutých a \(50\) zelených míčků. Kolika způsoby lze vybrat \(70\)?

\[
\begin{aligned}
	&(1 + x + \ldots + x^{30})(1 + x + \ldots + x^{40})(1 + x + \ldots + x^{50}) =\\ 
	&= \frac{1 - x^{31}}{1 - x} \frac{1 - x^{41}}{1 - x}\frac{1 - x^{51}}{1 - x} \qquad //\ \text{posuneme o $31$ míst a odečteme}\\
	&= \frac{1}{\left(1 - x\right)^3} \left(1 - x^{31}\right)\left(1 - x^{41}\right)\left(1 - x^{51}\right) \\
	&= \left(\binom{2}{2} + \binom{3}{2}x + \binom{4}{2}x^2 + \ldots\right) \left(1 - x^{31}\right)\left(1 - x^{41}\right)\left(1 - x^{51}\right) \\
	&= 1 + \ldots + \left[\binom{72}{2} - \binom{72 - 31}{2} - \binom{72 - 41}{2} - \binom{72 - 51}{2}\right]x^{70} + \ldots\\
	&= 1061
\end{aligned}
\]

Kde poslední rovnost platí, protože:
- z posledních 3 závorek si vybereme \(1\) a z první závorky koeficient u \(70\)
- ze druhé \(x^{31}\) a z první koeficient u \(72 - 31\)
	- analogicky pro \(41\) a \(51\) ze třetí a čtvrté

### 3. přednáška

#### Fibonacciho čísla
**Definice:** \(F_0 = 0, F_1 = 1, F_n = F_{n - 1} + F_{n - 2}, \forall n \ge 2\)
- \(F(x) = F_0 + F_1x + F_2x^2 + F_3x^3\)

| \(F_0\) | \(F_1\) | \(F_2\)       | \(F_3\)       | \(F_4\)       | Vytvořující funkce                |
| ---                          | ---                          | ---                                | ---                                | ---                                | ---                               |
| \(0\)   | \(1\)   | \(F_0 + F_1\) | \(F_1 + F_2\) | \(F_2 + F_3\) | \(F(x)\)     |
| \(0\)   | \(0\)   | \(F_1\)       | \(F_2\)       | \(F_3\)       | \(x F(x)\)   |
| \(0\)   | \(0\)   | \(F_0\)       | \(F_1\)       | \(F_2\)       | \(x^2 F(x)\) |
| \(0\)   | \(1\)   | \(0\)         | \(0\)         | \(0\)         | \(x\)        |

Algebraickou úpravou dostáváme:
\[
\begin{aligned}
	F(x) &= \frac{x}{1 - x - x^2} \\
	&= \frac{x}{\left(1 - \frac{1 + \sqrt{5}}{2}x\right)\left(1 - \frac{1 - \sqrt{5}}{2}x\right)} \qquad //\ \text{algebra}\\
	&= \frac{\frac{1}{\sqrt{5}}}{1 - \frac{1 + \sqrt{5}}{2}x} - \frac{\frac{1}{\sqrt{5}}}{1 - \frac{1 - \sqrt{5}}{2}x}  \qquad //\ \text{parciální zlomky }\\
	&= \frac{1}{\sqrt{5}}\left(\frac{1}{1 - \frac{1 + \sqrt{5}}{2}x} - \frac{1}{1 - \frac{1 - \sqrt{5}}{2}x}\right) \qquad //\ \text{tvary $\frac{\pm 1}{1 - \lambda_{1, 2} x}$}\\
\end{aligned}
\]

Pro daný koeficient vytvořující funkce tedy máme:
\[
\begin{aligned}
	F_n &= \frac{1}{\sqrt{5}} \left[\left(\frac{1 + \sqrt{5}}{2}\right)^n - \underbrace{\left(\frac{1 - \sqrt{5}}{2}\right)^n}_{\text{jde k $0$}}\right] \\
	&= \left\lfloor \frac{1}{\sqrt{5}} \left(\frac{1 + \sqrt{5}}{2}\right)^n \right\rfloor \\
\end{aligned}
\]

#### Catalanova čísla
- \(b_n = \) počet binárních zakořeněných stromů na \(n\) vrcholech
	- \(b_n = \sum_{k = 0}^{n - 1} b_k \cdot b_{n - k + 1}\), rekurzíme se na obě části
	- jde si rozmyslet, že \(b(x) = x \cdot b(x) \cdot b(x) + 1\)
		- \(x\) je tam kvůli posunu, aby vycházelo správně indexování (suma nejde do \(n\))
		- \(1\) je tam kvůli tomu, aby nultý člen správně vycházel

Rekurence pro \(b_n\) vypadá skoro jako konvoluce sama sebe, takže by
se nám líbilo něco jako \(b(x) = b(x)^2\). Jenže narozdíl od
konvoluce pronásobujeme jen prvních \(n-1\) prvků. Uvažme
tedy posloupnost \(0, b_0, b_1, b_2, \ldots\) generovanou funkcí
\(x b(x)\). Ta je již skoro konvolucí sama sebe -- \(n\)-tý prvek se v sumě požere s nulou.
Jediná nepřesnost je u \(b_0\), protože podle
definice konvoluce \(b_0 = 0 \cdot b_0 + b_0 \cdot 0 = 0\), ale my
víme \(b_0 = 1\). Stačí tedy přičíst jedničku posunutou o
jedna doprava, čímž dostaneme \(x b(x) = (x b(x))^2 + x\).
Jinými slovy \(b(x) = x b(x)^2 + 1\).

\[
\begin{aligned}
	b(x) &= x \cdot b(x)^2 + 1 \\
	b(x)_{1, 2} &= \frac{1 \pm \sqrt{1 - 4x}}{2x} \qquad //\ \text{ten s $+$ nedává smysl, diverguje}\\
	\\
	b(x) &= \frac{1 - 1 - \sum_{k = 1}^{\infty}(-4)^k \binom{1/2}{k} x^k }{2x} \qquad //\ \sqrt{1 - 4k} \overset{\text{ZBV}}{=} \sum_{k = 0}^{\infty} (-4)^k \binom{1/2}{k} x^k\\
	&= -\frac{1}{2} \sum_{k = 1}^{\infty} (-4)^k \binom{1/2}{k} x^{k - 1}\\
	\\
	b_n &= -\frac{1}{2} (-4)^{n + 1} \binom{1/2}{n + 1}\qquad //\ \text{konkrétní koeficient}\\
	&= \frac{1}{2} (-1)^{n} 2^{2n + 2} \frac{\frac{1}{2} \cdot \left(\frac{1}{2} - 1\right) \cdot \overset{n + 1}{\ldots} \cdot \left(\frac{1}{2} - n\right)}{\left(n + 1\right)!}\\
	&= \frac{1}{2} (-1)^{n} 2^{2n + 2} \frac{\frac{1}{2} \cdot \left(-\frac{1}{2}\right) \cdot \overset{n + 1}{\ldots} \cdot \left(-\frac{2n - 1}{2}\right)}{\left(n + 1\right)!}\\
	&= \frac{1}{2} 2^{2n + 2} \frac{\frac{1}{2} \cdot \frac{1}{2} \cdot \ldots \cdot \frac{2n - 1}{2}}{\left(n + 1\right)!} \qquad //\ \text{krácení záporných čísel}\\
	&= 2^{n} \frac{1 \cdot 3 \cdot 5 \cdot \ldots \cdot (2n - 1)}{(n + 1)!} \cdot \frac{n!}{n!} \qquad //\ \text{krácení $2$}\\
	&= \frac{1 \cdot 3 \cdot 5 \cdot \ldots \cdot (2n - 1)}{(n + 1) n!} \cdot \frac{2 \cdot 4 \cdot 6 \cdot \ldots \cdot 2n}{n!} \qquad //\ \text{rozdistribuování $2$}\\
	&= \frac{1}{n + 1} \frac{(2n)!}{\left(n!\right)^2} \\
	&= \frac{1}{n + 1} \binom{2n}{n} \\
\end{aligned}
\]

#### Konečné projektivní roviny

{:.rightFloatBox}
<div markdown="1">
První axiom zajišťuje netrivialitu. Není těžké si rozmyslet, že lze nahradit
axiomem _"Existují alespoň 2 různé přímky, z nichž každá má alespoň 3 body"_.
Bez některé z těchto podmínek by definici vyhovovala např. libovolně velká
množina bodů s právě jednou přímkou, která by všechny body spojovala. Případně
by k tomuto schématu šel přidat ještě jeden bod, který by s každým dalším byl
spojen dvoubodovou přímkou.
</div>

**Definice (KPR):** Nechť \(X\) je konečná množina, \(\mathcal{P}\) systém podmnožin množiny \(X\). \(\left(X, \mathcal{P}\right)\) je KPR pokud:
1. Existuje \(Č \subseteq X, |Č| = 4\) t. ž. \(\forall P \in \mathcal{P}: |P \cap Č| \le 2\)
	- „každá přímka obsahuje \(\le 2\) body z \(Č\)“
2. \(\forall P, Q \in \mathcal{P}, P \neq Q: \exists! x \in X\) t. ž. \(P \cap Q = \left\{x\right\}\)
	- „každé dvě přímky se protínají právě v \(1\) bodě“
3. \(\forall x, y \in X, x \neq y \exists! P \in \mathcal{P}\) t. ž. \(x, y \in \mathcal{P}\)
	- „každé dva body určují právě \(1\) přímku“

- \(x \in X\) je bod
- \(P \in \mathcal{P}\) je přímka

**Příklad (Fanova rovina):**

{:.center}
![Fanova rovina.](/assets/kombinatorika-a-grafy-i/fanova-rovina.svg)

##### Počet bodů a přímek

**Tvrzení:** „v KPR mají všechny přímky stejný počet bodů“

**Pomocné tvrzení:** \(\forall P, P' \in \mathcal{P} \exists z \in X\), které neleží ani na jedné z nich.

Dokáže se přes to přes rozbor příkladů toho, jak vedou přímky přes \(Č\):
- pokud nevedou přes všechny body z \(Č\), pak máme vyhráno
- pokud vedou, tak existují dvě další přímky \(P_1\) a \(P_2\) vedoucí kolmo na naše přímky, jejich průnik je hledaný bod; původní přímky jím vést nemohou, protože pak by dvě přímky sdílely 2 body, což nelze
- \(P_1 \neq P\), protože pak by \(P\)
  obsahovala alespoň 3 body z \(Č\). Podobně ostatní
  nerovnosti.

{:.center}
![](/assets/kombinatorika-a-grafy-i/bod-na-primce.svg)

### 4. přednáška

**Důkaz původního tvrzení:** pro přímky \(P\), \(P'\) a bod \(z\) (který nesdílí) budeme dělat bijekci tak, že budu tvořit přímky z bodu \(z\) na body z \(P\), které budou rovněž protínat body z \(P'\).

{:.center}
![](/assets/kombinatorika-a-grafy-i/kpr-bijekce.svg)


**Definice (řád KPR):** řádem \((X, \mathcal{P})\) je \(n = |P| - 1\) pro jakoukoliv \(P \in \mathcal{P}\).

**Tvrzení:** nechť \((X, \mathcal{P})\) je KPR řádu \(n\). Pak:
1. každým bodem prochází \(n + 1\) přímek 
2. \(|X| = n^2 + n + 1\)
3. \(|\mathcal{P}| = n^2 + n + 1\)

**Důkaz:**

{:.rightFloatBox}
<div markdown="1">
Explicitní důkaz (3): Pro každý bod započítejme všechny přímky jím
procházející. Dostaneme tak \((n^2+n+1)(n+1)\) přímek. Ale
každou jsme započítali \((n+1)\)-krát -- jednou pro každý z
jejích bodů.
</div>

1. triviálně z definice.
2. viz. níže.
3. vychází z duality (viz. další kapitola).

Vezměme libovolné \(x \in X\). Pak \(\exists P \in \mathcal{P}: x \not\in P\), protože vezmeme-li body \(a, b, c \in Č\), pak přímky \(ab\) a \(ac\) nemohou mít další společný bod než \(a\) (došlo by ke sporu s některým z axiomů).

Poté stačí uvážit následující obrázek a spočítat body/přímky. Další bod už neexistuje, protože kdyby existoval, tak by jím musela procházet přímka z \(x\) a ta by rovněž někde protínala \(P\) (a nesplňovala tak axiomy).

{:.center}
![](/assets/kombinatorika-a-grafy-i/kpr-pocet.svg)

Bodů na obrázku je \(\overbrace{1}^{x} + \underbrace{\left(n + 1\right)}_{P_0 \ldots P_n}\overbrace{n}^{\text{body $P_i$, bez $x$}} = n^2 + n + 1\).

#### Dualita KPR

{:.rightFloatBox}
{% xopp xins %}

**Definice (incidenční graf):** nechť \((X, \mathcal{S})\) je množinový systém (\(\mathcal{S} \subseteq 2^X\)). Jeho incidenční graf je bipartitní graf \[\left(V = X \cup \mathcal{S}, E = \left\{(x, s) \in X \times \mathcal{S}\ |\ x \in s\right\}\right)\]

**Definice (duál grafu):** \((Y, \mathcal{T})\) je duál \((X, \mathcal{S})\) pokud \(Y = \mathcal{S}\) a \(\mathcal{T} = \left\{\left\{s \in \mathcal{S}\ |\ x \in s\right\}\ |\ x \in X\right\}\)
- (👀) incidenční graf \((Y, \mathcal{T})\) je incidenční graf \((X, \mathcal{S})\) s prohozením stran

**Příklad (duál Fanovy roviny):**

{:.center}
![Duál Fanovy roviny.](/assets/kombinatorika-a-grafy-i/dual-fanovy-roviny.svg)

**Tvrzení:** duál KPR je KPR.

{:.rightFloatBox}
<div markdown="1">
1. „každá přímka obsahuje \(\le 2\) body z \(Č\)“
2. „každé dvě přímky se protínají právě v \(1\) bodě“
3. „každé dva body určují právě \(1\) přímku“
</div>

**Důkaz:** ověření axiomů v duálním světě:
1. \(\exists Č\) čtveřice přímek t. ž. \(\forall x \in X\) leží na nanejvýš \(2\) přímkách z \(Č\)
	- stejné jako „žádné \(3\) přímky z \(Č\) nemají společný bod“
	- zvolím \(Č = \left\{ab, cd, ad, bc\right\}\), což funguje (zkusit si rozkreslit)
2. \(\forall x, y \in X, x \neq y: \exists! P \in \mathcal{P}\) t. ž. jimi prochází právě \(1\) přímka
	- stejné jako původní axiom o přímkách
3. analogicky viz. ^

**Důsledek:** \((X, \mathcal{P})\) je řádu \(n \implies |\mathcal{P}| = n^2 + n + 1\)
- duál \((Y, \mathcal{T})\) je duál \((X, \mathcal{P})\), ten je stejného řádu a proto je i velikost \(|\mathcal{P}| = n^2 + n + 1\)

#### Konstrukce KPR

Pro KPR řádu \(p^k\), \(p\) prvočíslo vezmu algebraické těleso \(\mathbb{K}\) řádu \(n\) (příklad \(\mathbb{K} = \mathbb{Z}_3\)).
- \(T = \mathbb{K}^3 \setminus \left(0, 0, 0\right)\)
- na \(T\) zavedu ekvivalenci \((x, y, t) \in T\) je ekvivalentní s \((\lambda x, \lambda y, \lambda t), \forall \lambda \in \mathbb{K} \setminus {0}\)
- body \(X\) jsou ekvivalenční třídy nad \(T\)
- reprezentanti: poslední nenulová složka je \(1\)
	- trojice tvaru \((x, y, 1), (x, 1, 0), (1, 0, 0)\)
	- můžu si to dovolit, na reprezentanta převedu prostým pronásobením
	- počet je \(n^2 + n + 1\), což sedí
- přímky \(\mathcal{P}\): pro každou \((a, b, c) \in T\) definujeme přímku \(P_{a, b, c}\) jako množinu bodů \((x, y, t)\) splňující \(ax + by + ct = 0\)
	- \(\forall (x, y, t) \in T, \forall \lambda \neq 0: (x, y, t)\) splňuje \(\iff (\lambda x, \lambda y, \lambda t)\) splňuje
	- \(\forall (a, b, c) \in T, \forall \lambda\) fixuji \((x, y, t) \in T: ax + by + ct = 0 \iff \lambda ax + \lambda by + \lambda ct = 0 \implies\) přímky \(P_{a, b, c} = P_{\lambda a, \lambda b, \lambda c} \implies |\mathcal{P}| = |X|\) a mohu si opět zvolit reprezentanty

{:.center}
![](/assets/kombinatorika-a-grafy-i/kpr-alg.svg)

{:.rightFloatBox}
<div markdown="1">
1. „každá přímka obsahuje \(\le 2\) body z \(Č\)“
2. „každé dvě přímky se protínají právě v \(1\) bodě“
3. „každé dva body určují právě \(1\) přímku“
</div>

**Ověření axiomů:**
1. \(Č = \left\{(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)\right\}\)
	- jsou po třech lineárně nezávislé, proto \((1)\) platí
2. dvojice přímek \((a_1, b_1, c_1)\) a \((a_2, b_2, c_2)\) určují jeden bod:
	- jsou lineárně nezávislé a dimenze jádra následující matice je tedy \(1\) a určují jeden bod (až na \(\alpha\)-násobek, což je definice bodů)
\[ \begin{pmatrix} a_1 & b_1 & c_1 \\ a_2 & b_2 & c_2 \end{pmatrix} \begin{pmatrix} x \\ y \\ t \end{pmatrix} = 0 \]
3. analogické, protože role \((x, y, t)\) a \((a, b, c)\) je identická

### 5. přednáška

#### Latinské čtverce

**Definice (latinský čtverec)** řádu \(n\) je tabulka \(n \times n\) vyplněná čísly \([n]\), kde v žádném řádku či sloupci se symboly neopakují.
- (👀) \(A\) je LČ \(\implies\) po následujících operacích je stále:
	- permutace symbolů
	- permutace sloupců/řádků

**Definice (ortogonalita)**: LČ \(A, B\) jsou ortogonální, pokud pro každou dvojici symbolů \(a, b \in [n]\) existují indexy \(i, j \in [n]\) t. ž. \((A)_{i, j} = a, (B)_{i, j} = b\).
- když přeložím čtverce přes sebe, najdu políčko \((i, j)\) obsahující dvojici \((a, b)\)
- (👀) počet dvojic symbolů \(n^2 = \) počtu políček
	- zobrazení je bijekce
	- \(\forall (a, b)\) se objeví v OLČ právě jednou
- (👀) \(A, B\) jsou NOLČ \(\implies\) pokud dělám operace z předchozího pozorování v obou čtvercích, tak ortogonalitu zachovávám, jinak nutně ne

**Příklad** dvou navzájem ortogonálních latinských čtverců stupně \(n\):

\[
\begin{matrix}
	1 & 2 & 3 & 4 \\
	2 & 1 & 4 & 3 \\
	3 & 4 & 1 & 2 \\
	4 & 3 & 2 & 1 
\end{matrix} \qquad \begin{matrix}
	1 & 2 & 3 & 4 \\
	3 & 4 & 1 & 2 \\
	4 & 3 & 2 & 1 \\
	2 & 1 & 4 & 3 
\end{matrix}
\]

**Lemma:** pro daný řád \(n\) může existovat nejvýše \(n - 1\) NOLČ.

**Důkaz:** mějme maximální rodinu NOLČ \(L_1, \ldots, L_m\) a permutujme symboly tak, aby každý první řádek byl \(1, 2, 3, \ldots, n\); uvažme symbol na pozici \((2, 1)\):
- není \(1\), ta je na pozici \((1, 1)\)
- není nějaké \(k \in \left\{2, \ldots, n\right\}\) ve dvou čtvercích zároveň

Čtverců je dohromady tedy nejvýše \(n - 1\).

{:.rightFloatBox}
<div markdown="1">
Pro libovolné dvě pozice (které se liší v řádku a sloupci) existuje čtverec, který na nich má stejné hodnoty.
</div>

**Tvrzení:** pokud \(L_1, \ldots, L_{n - 1}\) jsou NOLČ, potom \(\forall k, k', k \neq k', \forall l, l', l \neq l' \exists i: \left(L_i\right)_{k, l} = \left(L_i\right)_{k', l'}\)

**Důkaz:** zpermutujeme symboly tak, aby \(\forall i \left(L_i\right)_{k, l} = 1\):

\[
\underbrace{\begin{bmatrix} &   &   &   \\ & (1) &   &   \\ &   &   &   \\ &   & ? &   \end{bmatrix}
			\qquad
			\begin{bmatrix} &   &   &   \\ & (1) &   &   \\ &   &   &   \\ &   & ? &   \end{bmatrix}
			\qquad
			\ldots
			\qquad
			\begin{bmatrix} &   &   &   \\ & (1) &   &   \\ &   &   &   \\ &   & ? &   \end{bmatrix}}_{n - 1}
\]

Ve sloupci s otazníkem nemůže symbol \(1\) být:
- v řádku s \((1)\)
- ve dvou čtvercích na stejném místě

Mám tedy \(n - 1\) možností a musím přijít na \(n - 1\) různých řešení. Jedno z nich tedy vyjde na \(?\).

#### NOLČ \(\iff\) KPR

**Věta:** \(\exists L_1, \ldots, L_{n - 1}\) NOLČ \(\iff \exists KPR\) řádu \(n\).

**Důkaz:** konstrukce \(\Rightarrow\)
- dány čtverce \(L_1, \ldots, L_{n - 1}\)
- body: \(r, s, l_1, l_{n - 1}, m_{1, 1}, m_{1, 2}, \ldots, m_{1, n}, \ldots, m_{n, n}\)
- přímky:
	- \(\mathrm{I}: \left\{r, s, l_1, \ldots, l_n - 1\right\}\)
	- \(\mathrm{II}:\) řádky -- \(\forall i \in [n]: \left\{r, m_{i, 1}, m_{i, 2}, \ldots, m_{i, n}\right\}\)
	- \(\mathrm{III}:\) sloupce -- \(\forall i \in [n]: \left\{s, m_{1, i}, m_{2, i}, \ldots, m_{n, i}\right\}\)
	- \(\mathrm{IV}: \underbrace{\forall i \in [n]}_{\text{latinské čtverce}}, \underbrace{\forall j \in [n]}_{\text{symboly}}: \left\{l_i\right\} \cup \left\{m_{k, l}\ \mid\ \left(L_i\right)_{k, l} = j\right\}\)

{:.center}
![Latinský čtverec na KPR.](/assets/kombinatorika-a-grafy-i/kpr-to-lat.svg)

{:.rightFloatBox}
<div markdown="1">
1. „každá přímka obsahuje \(\le 2\) body z \(Č\)“
2. „každé dvě přímky se protínají právě v \(1\) bodě“
3. „každé dva body určují právě \(1\) přímku“
</div>

**Ověření axiomů:**
1. \(Č = \left\{r, s, m_{1, 1}, m_{2, 2}\right\}\)
2. mezi:
	- \(I, II \rightarrow r\)
	- \(I, III \rightarrow s\)
	- \(I, IV \rightarrow l_i\)
	- \(II, II \rightarrow r\)
	- \(III, III \rightarrow s\)
	- \(II, III \rightarrow m_{k, l}\)
	- \(II, IV \rightarrow \) čtverec je latinský, na řádku se symbol někde vyskytuje
	- \(III, IV \rightarrow \) obdobně ^
	- \(IV, IV \rightarrow \) 
		- různé čtverce: přesně definice ortogonality (existuje dvojice souřadnic pro dvojici symbolů)
		- stejné čtverce: \(l_i\)
3. mezi:
	- \(r, s, l_i \rightarrow \mathrm{I}\) 
	- \(r, m_{k, l} \rightarrow \mathrm{II}\) 
	- \(s, m_{k, l} \rightarrow \mathrm{III}\) 
	- \(l_{i}, m_{k, l} \rightarrow \mathrm{IV}\), symbol \(\left(L_i\right)_{k, l}\) určuje, o kterou přímku z \(l_i\) jde
	- \(m_{k, l}, m_{k', l'} \rightarrow\)
		- stejný řádek: \(\mathrm{II}\)
		- stejný sloupec: \(\mathrm{III}\)
		- jinak: \(\mathrm{IV}\) a existuje, vycházíme z minulého pozorování

**Důkaz:** konstrukce \(\Leftarrow\)
- dána KPR \((X, \mathcal{P})\), hledáme \(L_1, \ldots, L_{n - 1}\)
	1. zvolíme libovolně přímku \(I = \left\{r, s, l_1, \ldots, l_{n - 1}\right\}\)
	2. \(\exists n\) přímek protínající \(r\) -- typ \(\mathrm{II}\) a opět oindexuji body
	3. analogicky ^, typ \(\mathrm{III}\), průsečíky jsou \(m_{k, l}\)
	4. pro bod \(l_i\) oindexuj přímky \(Q_1, \ldots, Q_n\); čtverec \(L_i\) má \(1\) na indexech \(Q_1\), \(2\) na \(Q_2\), \(\ldots\)

Jsou NOLČ, protože:
- průsečíky \(\mathrm{IV}\) s \(\mathrm{II}, \mathrm{III}\) jsou jednoznačné \(\implies\) čtverce jsou latinské
- jednoznačnost průniku dvou přímek typu \(\mathrm{IV}\) -- dvě různé přímky typu \(\mathrm{IV}\) odpovídající dvěma různým čtvercům dávají souřadnici, kde se má dvojice symbolů nachází \(\implies\) ortogonalita

{:.center}
![KPR na latinský čtverec.](/assets/kombinatorika-a-grafy-i/lat-to-kpr.svg)

### 6. přednáška

#### Počítání dvěma způsoby

**Tvrzení:** počet podmnožin \(X = \left| \binom{X}{k}\right| = \binom{|X|}{k}\)

**Důkaz:** nechť máme bublinu s tečkami, každá reprezentuje uspořádanou \(k\)-tici prvků z \(X\).
- počet teček \(= n (n -1) (n-2) \ldots (n - k + 1) = \frac{n!}{(n - k)!}\) (vyberu \(1.\) prvek, \(2.\) prvek,...)
- v každé buňce \(k\)-tic (ekvivalenční třídě přes příslušnou relaci) se stejnými prvky je \(k!\) prvků, počet buňek je to, co chceme (neuspořádaná \(k\)-tice)

\[
\begin{aligned}
	\frac{n!}{(n - k)!} &= \left|\binom{X}{k}\right| \cdot k! \\
	\left|\binom{X}{k}\right|&=  \frac{n!}{(n - k)! k!} = \binom{n}{k} \\
\end{aligned}
\]

**Věta (Spernerova):** nechť \((\mathcal{P}, \subseteq)\) je částečné uspořádání, kde \(\mathcal{P}\) je množinový systém. Nechť \(\mathcal{M}\) je největší antiřetězec (\(\forall M_1, M_2 \in \mathcal{M}, M_1 \neq M_2: M_1 \nsubseteq M_2 \land M_2 \nsubseteq M_1\)). Pak \(|\mathcal{M}| \le \binom{n}{\left\lceil \frac{n}{2} \right\rceil}\), kde \(n = |X|\).

{:.center}
![Sperenerova věta.](/assets/kombinatorika-a-grafy-i/spernerova-veta.svg)

**Pomocné tvrzení:** \(\sum_{M \in \mathcal{M}} \left|M\right|! (n - \left|M\right|)! \le n!\). Přes dvojí počítání počtu permutací na \(X\):
- počet permutací \(= n!\) (očividné)
- počet permutací \(\ge \sum_{M \in \mathcal{M}} |M|! (n - |M|)! \), protože:
	- pro každé \(M\) dostanu jinou množinu permutaci
	- \(M\) určuje množinu permutací takovou, že nejprve permutuji \(M\), potom \(X \setminus M\):

{% xopp sperner %}

- \(\emptyset \subseteq \left\{x_1\right\} \subseteq \left\{x_1, x_2\right\} \subseteq \ldots \subseteq M \subseteq \ldots \subseteq X\)
	- zajímá nás, kolik různých řetězců obsahuje \(M\)
- (👀) každý maximální řetězec obsahuje \(\le 1\ M \in \mathcal{M}\) 

**Důkaz (přes pomocné tvrzení):**
\[
\begin{aligned}
	\sum_{M \in \mathcal{M}} |M!| (n - |M|)! &\le n! \\
	\sum \binom{n}{\left\lceil \frac{n}{2} \right\rceil}^{-1} \le \sum_{M \in \mathcal{M}} \frac{|M!| (n - |M|)!}{n!} &\le 1 \qquad //\ \text{používáme větší kombinační číslo} \\
	\left|\mathcal{M}\right| &\le \binom{n}{\left\lceil \frac{n}{2} \right\rceil}  \\
\end{aligned}
\]

#### Grafy bez \(C_k\)

**Motivace:**
- kolik nejvíce hran má \(G\), když nemá \(C_k, \forall k\)?
	- je to strom, tedy \(n - 1\)
- kolik nejvíce hran má \(G\), když nemá \(C_3\)?
	- \(\mathcal{O}(n^2)\), uvažme bipartitní graf

**Věta:** graf \(G\) s \(n\) vrcholy bez \(C_4\) má nejvýše \(\frac{1}{2} \left(n^{3/2} + n\right)\) hran.

{:.rightFloatBox}
![Vidlička.](/assets/kombinatorika-a-grafy-i/vidlicka.svg)

**Důkaz:** dvojí počítání „vidliček“ (cest delky \(2\)):
1. pro pevnou dvojici \(\left\{u, u'\right\}\) mám nanejvýš 1 vidličku (dvě by tvořily čtyřcyklus), tedy \(\#\ \text{vidliček}\ \le \binom{n}{2}\)
2. pro pevný vrchol \(v\) máme \(\#\ \text{vidliček}\ = \binom{d_i}{2}\)

\[
	\#\ \text{vidliček}\ = \sum_{i = 1}^{n} \binom{d_i}{2} \le \binom{n}{2}
\]

Také víme (z principu sudosti), že:

\[
	|E| = \frac{1}{2} \sum_{i = 1}^{n} d_i
\]

Předpoklad: nemáme izolované vrcholy (\(d_i \ge 1\)), jsou zbytečné. Pak \(\binom{d_i}{2} \ge \frac{(d_i - 1)^2}{2}\).

\[
\frac{n^2}{2} \ge \binom{n}{2} \ge \sum_{i = 1}^{n} \binom{d_i}{2} \ge \sum \frac{(d_i - 1)^2}{2} = \sum \frac{k_i^2}{2} \qquad //\ \text{substituce} \\
\sum k_i^2 \le n^2
\]

Využijeme Cauchy-Schwartzovu nerovnost na \(x = (k_1, \ldots, k_n), y = (1, \ldots, 1)\):
\[
xy = \sum k_i = \sum \left(d_i - 1\right) = 2|E| - n \\
|| x ||_2 = \sqrt{\sum k_i^2} \le \sqrt{n^2} = n \qquad || y ||_2 = \sqrt{\sum 1} =  \sqrt{n}
\]

\[
\begin{aligned}
	2|E| - n &= xy \le ||x||_2 ||y||_2 = n^{3/2} \\
	|E| &\le \frac{1}{2} \left(n^{3/2} + n\right)
\end{aligned}
\]

#### Počítání koster

**Věta (Cayleyho formule):** počet koster úplného grafu \(\kappa(n) = n^{n - 2}\).
- pozor, počítám i izomorfní kostry!

{:.rightFloatBox}
{% xopp kostry %}

**Důkaz:** počítání \((T, r, č)\), kde:
- \(T\) je strom na \(n\) vrcholech
- \(r\) kořen (hrany vedou do kořene, ne z něho)
- \(č\) očíslování hran (nějaké), \(č: E \mapsto [n - 1]\)

1. \(\#(T, r, č) = \kappa(n) \cdot n \cdot \left(n - 1\right)!\)
	- \(T\) je to, co hledáme
	- \(r\) volíme libovolně z \(n\) vrcholů
	- \(č\) je prostě random očíslovaní na \(n - 1\) hranách
2. představa: přidávám hrany, až nakonec dojdu k \((T, r, č)\) a jsem v \(k\)-tém kroce:
	- (👀) nesmím vést hranu uvnitř komponenty (cykly)
	- (👀) musím vést hranu pouze z kořene dané komponenty (jeden vrchol by měl 2 rodiče)

	1. zvolím, kam šipka povede... \(n\) způsobů
	2. zvolím komponentu, ze které povede... \(n - k - 1\)
		- máme \(n - k\) komponent a \(1\) je blokovaná

\[
\begin{aligned}
	\#(T, r, č) &= \prod_{k = 0}^{ \overbrace{n - 2}^{\text{počet šipek je $n - 1$}}} n ( n - k - 1) = n^{n - 1} (n -1)! \\
	\kappa(n) \cdot n \cdot \left(n - 1\right)! &= n^{n - 1} (n -1)! \\
	\kappa(n) &= n^{n - 2}
\end{aligned}
\]

### 7. přednáška

#### Toky

**Definice (síť)** je čtveřice \((G, z, s, c)\), kde:
- \(G\) je orientovaný graf, \(z, s \in V(G)\)
- \(c: E \mapsto \mathbb{R}_{\ge 0}\)

{:.rightFloatBox}
<div markdown="1">
1. omezení shora kapacitami
2. Kirchhoff
</div>
**Definice (tok)** v síti je \(f: E \mapsto \mathbb{R}_{\ge 0}\), t. ž.:
1. \(\forall e \in E(G)\) platí \(0 \le f(e) \le c(e)\)
2. \(\forall v \in V(G), v \not\in \left\{z, s\right\}\) platí \(\sum f(x, v) = \sum f(v, y)\)

{:.rightFloatBox}
<div markdown="1">
To, co teče ven ze zdroje.
</div>

**Definice (velikost toku)** \(w(f) = \sum f(z, x) - \sum f(x, z)\) 

**Věta:** existuje maximální tok.

**Nástin důkazu:** Nástin je takový, že množina toků je kompaktní a obsahuje tedy i maximum (nevznikne nám tam nějaká divnost).

**Definice (řez)** v síti je množina hran \(R \subseteq E(G)\) taková, že v grafu \((V, E \setminus R)\) neexistuje cesta ze zdroje do stoku.
- **kapacita** řezu je \(c(R) = \sum_{e \in R} c(e)\), analogicky tok
- \(S(A, B) = \left\{(x, y) \in E\ |\ x \in A, y \in B\right\}\)
	- neobsahuje hrany z \(B\) do \(A\)!
	- je to **elementární** řez (vezmu dvě množiny vrcholů a všechny hrany mezi nimi)
		- každý v inkluzi minimální (\(R \setminus {e}\) není řez) řez je elementární

##### max flow, min cut

**Věta (max flow, min cut):** pro každou síť je maximální tok roven minimálnímu řezu.

**Lemma:** pro každou \(A \subseteq V\) t. ž. \(z \in A, s \not\in A\) a pro libovolný tok \(f\) platí: \[w(f) = f(A, V \setminus A) - f(V \setminus A, A)\]

**Důkaz:**
\[
\begin{aligned}
	w(f) &= \sum_{u \in A} \left(\sum_{(u, x) \in E} f(u, x) - \sum_{(x, u) \in E} f(x, u)\right) \qquad //\ \text{pouze definice} \\
	&= \sum_{u \in A, v \not\in A} f(u, v) - \sum_{u \not\in A, v \in A} f(v, u) \qquad //\ \text{hrany uvnitř A přispějí jednou $+$ a jednou $-$} \\
	&= f(A, V \setminus A) - f(V \setminus A, A) \\
\end{aligned}
\]

**Důsledek:** \(w(f) \le c(R)\), protože
\[w(f) = f(A, V \setminus A) - f(V \setminus A, A) \le f(A, V \setminus A) \le c(A, V \setminus A) \le c(R)\]

**Definice (nasycená cesta)** je (neorientovaná) cesta, pokud \(\exists e\) na cestě t. ž. buďto:
- vede po směru a \(f(e) = c(e)\)
- vede proti směru a \(f(e) = 0\)

**Definice (nasycený tok)** je tok takový, že každá (neorientovaná) cesta ze \(z\) do \(s\) je nasycená.

**Tvrzení:** \(f\) je maximální \(\iff f\) je nasycený.

**Důkaz:** sporem, že \(f\) maximální je nasycený.
- předpokládáme maximální \(f\), který není nasycený, tedy existuje nenasycená cesta \(P\)
	- \(\varepsilon_1 = min \left\{c(e)-f(e)\ |e \in P \text{ po směru } \right\}\)
	- \(\varepsilon_2 = min \left\{f(e)\ |e \in P \text{ proti směru } \right\}\)
	- \(\varepsilon_P = min \left\{\varepsilon_1, \varepsilon_2 \right\} > 0 \), protože \(P\) není nasycená
- sestrojme tok \(f'\) tak, že:
	- \(f'(e) = f(e) + \varepsilon_P\) pro \(e \in P\) po směru
	- \(f'(e) = f(e) - \varepsilon_P\) pro \(e \in P\) proti směru
	- \(f'(e) = f(e)\) pro \(e \notin P\)
\[w(f') = \sum f'(z,x) - f'(x,z) = w(f) + \varepsilon_P\]
- \(f\) nebyl maximální, spor

**Důkaz:** že \(f\) nasycený je maximální.
- tak uvážíme množinu vrcholů, do kterých se lze dostat ze \(z\) po nenasycené cestě -- \(A = \left\{v \in V\ |\ \exists\ \text{nenasycená cesta }\right\}\)
	- \(s \notin A\) (jinak \(f\) není nasycený)
	- \(\forall e \in S(A, V \setminus A)\) platí \(f(e) = c(e)\)
	- \(\forall e \in S(V \setminus A, A)\) platí \(f(e) = 0\) (jinak bychom nenasycenou cestu mohli prodloužit

\[
\begin{aligned}
	w(f) &= f(A, V \setminus A) - f(V \setminus A, A) \qquad //\ \text{předešlé lemma}\\
	&= c(A, V \setminus A) - 0\\
	&= c(f)
\end{aligned}
\]

##### Ford-Fulkerson
1. \(f(e) = 0, \forall e \in E\)
2. dokud \(\exists\) zlepšující cesta \(P\), zlepši tok přes \(P\)

**Tvrzení:** pokud jsou kapacity racionální, pak algoritmus doběhne. Pokud jsou přirozené, dá celočíselný tok.
- racionální: pronásobení LCM a důkaz pro přirozené
- přirozené: každé vylepšení cesty bude celočíselné a udělá to konečněkrát

(👀) Celočíselný tok lze rozdělit na celočíselný součet cest a cyklů.

**Důkaz:** Plyne z běhu F-F algoritmu. Tok je součtem zlepšujících cest a cyklů.

### 8. přednáška

#### Aplikace toků v sítích

**Věta (Königova):** v bipartitním grafu: velikost maximálního párování \(=\) velikost minimalního vrcholového pokrytí.
- \(M \subseteq E\) je **párování**, pokud \(\forall e, e' \in M, e \neq e': e \cap e' = \emptyset\) 
- \(U \subseteq V\) je **vrcholové pokrytí**, pokud \(\forall e \in E \exists u \in U: u \in e\)

**Důkaz:** přes toky, jako na následujícím obrázku na síti kapacit \(1\):

{:.center}
![Königova věta.](/assets/kombinatorika-a-grafy-i/konig.svg)

- \(R\) je minimální \(z-s\) řez
- \(C\) je minimální vrcholové pokrytí
- \(f\) je maximální tok
	- hrany v původním grafu jsou maximální párování
- \(L, P =\) levá a pravá část grafu (bez zdroje a stoku)

Z toku mám maximální párování \(M\) velikosti \(k\), ze kterého sestrojím minimální řez \(R\).

\(R\) je minimální \(z-s\) řez. Ten upravíme na minimální řez \(R'\), aby neobsahoval hrany původního grafu. To jde, protože hranu původního grafu mohu vyměnit za tu ze zdroje/stoku, protože ta je jediný způsob, jak se dostat do hrany z původního vrcholu.
- \(W = \left\{u \in L\ |\ (z, u) \in R'\right\} \cup \left\{v \in P\ |\ (v, s) \in R'\right\}\)
	- je vrcholové pokrytí, v původním grafu by jinak existovala \(z-s\) cesta a nejednalo se o řez

\(W\) je minimální vrcholové pokrytí \(G\):
- \(R = \left\{(z, u)\ |\ u \in W \cap L\right\} \cup \left\{(u, s)\ |\ u \in W \cap P\right\} \)
	- je řez (pro spor by existovala cesta, kterou by \(W\) nepokryl)

Dostáváme tedy, že min. řez je roven nějakému pokrytí, a že min. pokrytí je rovno nějakému řezu, tedy že min. pokrytí je rovno min. řezu.

**Definice:**
- **množinový systém** na množině \(X\) je \((M_i)_{i \in I}, M_i \subseteq X\)
- **systém různých reprezentantů** je funkce \(f: I \mapsto X\) splňující:
	1. \(\forall i \in I: f(i) \in M_i\)
	2. \(f\) je prostá (jeden prvek \(x \in X\) není reprezentantem dvou \(M\))


{:.rightFloatBox}
<div markdown="1">
Analogicky pro grafy: bipartitní graf \(G = (L \cup P, E)\) má párování pokrývající \(P\) pokud \(\forall P' \subseteq P: \left|\bigcup_{v \in P'} N(v)\right| \ge |P'|\). \(N\) je sousedství (to, co vrcholy zprava na levé straně „vidí“).
</div>
**Hallova věta:** SRR existuje \(\iff \forall J \subseteq I: \left|\bigcup_{i \in J} M_i\right| \ge |J|\).

**Důkaz (SSR \(\Rightarrow\) Hall):** zvolím libovolnou \(J \subseteq I\). \(\forall j \in J \exists p_j \in M_j, p_j = f(j)\), tak že prvky \(p_j\) jsou navzájem různé (\(f\) je prostá).
\[|J| = \left|\left\{p_j\ |\ j \in J\right\}\right| \le |\bigcup_{j \in J} M_j|\]

**Důkaz (SSR \(\Leftarrow\) Hall):** opět najdu v grafu (celočíselný, jednotková síť) maximální tok. Najdu minimální řez z hran pouze ze zdroje/do stoku, \(|R| = |R'|\). Uvážím následující obrázek:

{% xopp hall %}

- \(A = \) vrcholy incidentní s \(R'\) v \(I\)
- \(B = \) vrcholy incidentní s \(R'\) v \(X\)
- \(J = I \setminus A\)

Chceme najít systém různých reprezentantů. Dokážeme to tak, že \(|R'| = |I|\), pak max. tok má velikost \(|I|\) a hrany s tokem \(1\) mi dají SRR.

(👀) hrany z \(J\) vedou pouze do \(B\), protože jinak by existovala \(z-s\) cesta a nejednalo by se o řez, tedy \(\left|\bigcup_{j \in J} M_j\right| \subseteq B\).

\[
\begin{aligned}
	|R'| &= c(R') &&//\ \text{jednotkové kapacity}\\
	&= |A| + |B| \\
	&= \overbrace{|I| - |J|}^{|A|} + |B| \\
	&\ge |I| - |J| + \left|\bigcup_{j \in J} M_j\right| &&//\ \text{z pozorování}\\
	&\ge |I| - |J| + \left|J\right| &&//\ \text{z Hallovy podmínky}\\
	&= |I| &&// \implies\ \text{tok má velikost alespoň $|I|$} \\
\end{aligned}
\]

Definuji SRR jako \(f(i) = x \in X\), pokud po hraně \((i, x)\) něco teče.

### 9. přednáška

**Důsledek:** nechť \(B = (V_1 \cup V_2, E)\) je bipartitní graf, kde \(k_1 = \mathrm{min}\ \underset{v \in V_1}{\deg}\ v, k_2 = \mathrm{max}\ \underset{v \in V_2}{\deg}\ v \) a \(k_1 \ge k_2\), pak je splněna Hallova podmínka.

**Důkaz:** Ověřím Hallovu podmínku (pozor, prohozené strany). Máme-li množinu \(J\) a každá vidí alespoň \(k_1\) hran, pak vidím \(\ge |J| k_1\) hran. Abych pohltil všechny tyto hrany, tak musí napravo být alespoň \(k_2 |N[j]|\) vrcholů. Musí tedy platit:
\[|J| k_1 \le \#\ \text{hran} \le k_2 |N[J]|\]

Protože \(k_1 \ge k_2\), pak \(|N[j]| \ge |J|\).

**Aplikace:** doplňování latinských obdélníků:

{:.center}
![Latinský obdelník.](/assets/kombinatorika-a-grafy-i/lat-rect.svg)

- stupně: každý sloupec má stupeň \(n - k\) (počet nepoužitých symbolů)
- symboly: každý symbol se vyskytuje v řádku právě jednou, tedy ještě není v \(n - k\) sloupcích

Máme tedy \(\left(n - k\right)\)-regulární graf, pro který \(\exists\) perfektní párování (použití minulého důsledku).

#### Míra souvislosti neorientovaných grafu

**Definice**
- **hranový řez** v grafu \(G\) je \(F \subseteq E\) t. ž. \(G' = (V, E \setminus F)\) je nesouvislý.
- **vrcholový řez** v grafu \(G\) je \(A \subseteq V\) t. ž. \(G' = (V \setminus A, E \cap \binom{V \setminus A}{2}) = G\left[V \setminus A\right]\) je nesouvislý.
- **hranová souvislost** \(k_e(G) = \mathrm{min} \left\{|F|\ |\ F \subseteq E \text{ je hranový řez}\right\}\)
- **vrcholová souvislost** \(k_v(G) = \begin{cases}n - 1 & G \cong K_n \\ \mathrm{min} \left\{|A|\ |\ A \subseteq V \text{ je vrcholový řez}\right\} & \text{jindy} \end{cases}\)
- \(G\) je **hranově/vrcholově \(k\)-souvislý**, pokud \(k_{e/v}(G) \ge k\)
	- „potřebuješ useknout alespoň \(k\) hran/vrcholů na to, aby se graf rozpadl“
	- (👀) je-li \(3\)-souvislý, pak je i \(2\)-souvislý a \(1\)-souvislý
	- je **kriticky** \(k\)-souvislý, pokud odstranění libovolného vrcholu sníží stupeň souvislosti
		- stromy jsou hranově \(1\)-souvislé, vrcholově ne (co listy?)

**Lemma:** \(\forall G, \forall e \in E\) platí \(k_e(G) - 1 \le k_e(G - e) \le k_e(G)\)
- zas tak triviální to není, u vrcholové může (odstraněním vrcholu) vzrůst (listy z kružnice)
- lemma říká, že se hranová souvislost „chová slušně“

{:.rightFloatBox}
<div markdown="1">
Tomovo poznámka: V důkazu \(k_e(G) \le k_v(G)\) se tohle lemma nepoužívá (alespoň tak, jak to chápu). Jsem trochu zmatený z toho, proč Martin říkal, že ano.
</div>

**Důkaz (\(\le\)):** vezmu minimální řez \(F \subseteq E\) v \(G\), \(F' = F \setminus \left\{e\right\}\) jistě musí být řez v \(G - e\); pak:
\[k_e(G - e) \le |F'| \le |F| = k_e(G)\]

**Důkaz (\(\ge\)):** vezmu minimální řez \(B\) v \(G - e\) \(B' = B \cup \left\{e\right\}\) je řezem v \(G\), pak:
\[
\begin{aligned}
	k_e(G) \le |B'| &= |B| + 1 = k_e(G - e) + 1\\
	k_e(G) - 1 &\le k_e(G - e)
\end{aligned}
\]

**Lemma:** \(\forall G, \forall e \in E\) platí \(k_v(G) - 1 \le k_v(G - e) \le k_v(G)\)

**Důkaz:** trochu přeformulujeme... pro \(H = G - e: k_v (H + e) \le k_v (H) + 1\):

V \(H\) existuje vrcholový řez \(A \subseteq V(H), k_v(H) = |A|\). Při odebrání \(A\) se \(H\) rozpadne na alespoň \(2\) komponenty. Sledujeme (rozebíráme případy), co se se souvislostí stane, když přidáme do grafu hranu \(e\):
- alespoň \(1\) konec \(e\) leží v \(A\):
	- přidání \(e\) nespojí žádné \(2\) komponenty, \(A\) je řezem i pro \(G = H + e\)
- oba konce leží v \(1\) komponentě
	- stejný argument jako (1)
- hrana \(e\) spojuje \(2\) komponenty
	- pokud je počet komponent \(\ge 3\), tak je \(A\) stále řezem (po spojení jsou stále \(2\))
	- pokud není, tak:
		- BUNO \(|C_1| \ge 2\); nechť \(e = xy\) a \(x\) leží v \(C_1\), pak \(A \cup {x}\) je řezem, protože mi v obou komponentách něco zbylo
		- \(|C_1| = |C_2| = 1\):
			- \(|V| = |A| + 2 \implies |A| = |V| - 2 = k_v(H)\)
			- \(k_v(H + e) \overset{\text{def.}}{\le} |V| - 1 = k_v(H) + 1\)

**Věta:** \(k_v(G) \le k_e(G)\): indukcí podle počtu hran:
- pokud \(|E| < |V| - 1\), pak je \(G\) nesouvislý a \(k_v(G) = 0 = k_e(G)\)
- nechť nadále \(k_e(G) > 0\); vezmu min. hranový řez \(F \subseteq E\) a \(e \in F\); také \(G' = G - e\)
	- na \(G'\) použiju IP, tedy \(k_v(G') \le k_e(G')\)
	- z lemmatu o souvislosti vrcholů (a přičtení jedničky) víme:
\[k_v(G) - 1 \le k_v(G - e) \overset{\mathrm{IP}}{\le} k_e(G - e) = k_e(G) - 1\]

Kde poslední rovnost platí, protože \(F' = F \setminus {e}\) je (z definice) řezem \(G - e\).

**Věta (Ford-Fulkerson):** \(\forall G\), pokud \(k_e(G) \ge t\), pak \(\forall u, v
\) mezi \(u, v\) existuje alespoň \(t\) hranově disjunktních cest

**Důkaz (\(\Leftarrow\)):** sporem nechť existuje hranový řez \(F\) a \(|F| < t\). \(G \setminus F\) je rozdělený na více komponent. Vezmi \(u \in C_1, v \in C_2\). Mezi \(u, v\) vedlo \(t\) hranově disjunktních cest. \(F\) nemohl přerušit všechny z nich.

{:.rightFloatBox}
<div markdown="1">
- oboustraně zorientuji hrany
- nastavím kapacity na \(1\)
- vynuluji \(a \overset{1}{\underset{1}{\longleftrightarrow}} b\)
	- každou hranu využíváme \(1\)!
</div>

**Důkaz (\(\Rightarrow\)):** mějme \(k_e(G) \ge t\) a pro \(u, v\) hledám disjunktní cesty. Sestrojím jednotkovou síť, najdu tok z \(u\) do \(v\). Pak vidím, že mám tok alespoň \(t\) (maximální tok je minimální řez) a začnu odčítat cesty.

**Věta (Mengerova):** \(k_v(G) \ge T \iff \forall u, v \in V \exists t\) vrcholově disjunktních cest

**Důkaz (\(\Leftarrow\)):** stejný jako FF, jen nahraď „hrany“ za „vrcholy“.

**Důkaz (\(\Rightarrow\)):** uděláme trik s dělením vrcholů na dva (\(\deg_{\mathrm{in}}, \deg_{\mathrm{out}}\)) a v libovolném řezu nahradíme hrany vedoucí do/z vrcholů za hranu spojující vrcholy. 

### 10. přednáška

#### Lepení uší

**Věta:** graf je \(2\)-souvislý právě tehdy, když jej lze vytvořit  z \(K_3\) posloupností:
- dělení hran
- přidávání hran

**Důkaz (\(\Rightarrow\)):**
- zvolme \(G_0\) libovolně (kružnici mít musí, jinak není \(2\)-souvislý).
- předpokládejme, že \(G_j, j \le i\) jsou definovány jako výše
- pokud \(G_i = G\), tak jsme hotovi
- jinak \(E_i \neq E\), \(G\) je souvislý
	- \(\exists e = \left\{v, v'\right\} \in E \setminus E_i\), která se dotýká původního grafu (\(e \cap V_i \neq \emptyset\))
		- pokud oba vrcholy \(e\) patří do \(V_i\), tak ji přidám (\(G_{i + 1} = G_i + e\))
		- pokud ne: \(G - v\) musí stále být souvislý (\(G\) je \(2\)-souvislý) -- prostě vezmeme nejkratší cestu zpět do nějakého \(G_j\)

{:.center}
![Lepení uší.](/assets/kombinatorika-a-grafy-i/ears.svg)

**Důkaz (\(\Leftarrow\)):** stačí vidět, že nikdy nevznikne artikulace, protože uši lepím mezi \(2\) různé vrcholy.

#### Samoopravné kódy

**Hammingův kód:** vycházíme z fannovy roviny a o přímkách uvažujeme jako o prvcích \(\mathbb{Z}_2^7\)

\[H = \underbrace{\left\{\text{char. vektory přímek}\right\}}_{P_1 = \left\{1, 2, 4\right\} = (1\ 1\ 0\ 1\ 0\ 0\ 0)} \cup \underbrace{\left\{\text{char. vektory doplňků přímek}\right\}}_{P_1 + (1\ \ldots\ 1) = (0\ 0\ 1\ 0\ 1\ 1\ 1)} \cup \left\{(0\ \ldots\ 0), (1\ \ldots\ 1)\right\}\]
- \(|H| = 7 + 7 + 2 = 16\)
- \(c \in H\) je **kódové slovo**
- \(H\) je **kód**
- (👀) \(\forall c, c' \in H\) se liší v alespoň třech souřadnicích
	- vychází z KPR, později dokážeme obecně
- (👀)  \(\forall v \in \mathbb{Z}_2^7 \exists! c \in H\) t. ž. \(d(v, c) \le 1\)
	- dostáváme z toho dekódovací pravidlo -- dekóduj na nejbližší slovo!

**Protokol:**
1. vezmi kódovou zprávu
2. rozděl na \(4\)-bitové bloky
3. zakóduj přes Hammingův kód
	- nějak rozumně očísluj kódová slova!
4. profit?

**Výsledek:**
- zpráva je o \(7/4\) delší
- \(\Pr\left[\text{jeden blok se správně rozkóduje}\right] = \overbrace{(1 - p)^7}^{\text{vše ok}} + \overbrace{7p(1 - p)^6}^{\text{jeden špatně}} = (1-p)^6(1 + 6p)\)
- \(\Pr\left[\text{celá zpráva se správně dekóduje}\right] = \left((1-p)^6(1 + 6p)\right)^{n/4}\)
	- pro \(n = 100, p = 0.01\) vyjde \(95\%\), což je nice!

---

**Definice:**
- \(\Sigma \ldots\) abeceda
	- \(s \in \Sigma^n \ldots\) slovo (vstup)
- \(C \subseteq \Sigma^n \ldots\) kód
	- \(c \in C \ldots\) kódové slovo (naše special slova)
	- \(|C| \ldots\) velikost kódu (počet kódových slov)
	- \(n \ldots\) délka kódu (kolikaznakové slova máme)
	- \(k = \log |C| \ldots\) dimenze kódu (bude se hodit později)
- pro \(x, y \in \Sigma^n: d_H (x, y) = d(x, y)\ldots\)  počet souřadnic, ve kterých se liší
	- \(d = \Delta(C) = \underset{x, y \in C}{\mathrm{min}}\ d(x, y) \ldots\) (min.) vzdálenost \(C\)
		- \(d = 1 \ldots\) nepoznám chybu
		- \(d = 2 \ldots\) poznám, že došlo k chybě
		- \(d = 3 \ldots\) umím opravit \(1\) chybu
		- \(\Delta(C) \ge 2t + 1\) znamená, že „\(C\) má schopnost opravit \(t\) chyb“
- kód s vlastnostmi \(n, k, d\) se označuje \((n,k,d)-\) kód

**Příklady kódů:**
1. totální kód \(C = \Sigma^n\) (nic se nekóduje)
	- délka \( = n\)
	- velikost \(= 2^n \implies k = \log |C| = n\)
	- \(\Delta(C) = 1\)
	- \(\implies (n, n, 1)-\)kód
2. opakovací kód délky \(n\) (pozor, \(n\) je délka slova)
	- délka \(= n\)
	- velikost \(= 2 \implies k = 1\)
	- \(\Delta(C) = n\)
	- \(\implies (n, 1, n)-\)kód
3. paritní kód \(C \subseteq \Sigma^n\) t. ž. \(x \in C: \sum_{x_i} = 0\) (počet jedniček je sudý)
	- délka \(= n\)
	- velikost \(= 2^{n - 1} \implies k = n - 1\)
	- \(\Delta(C) = 2\), protože změna bitů mění paritu
	- \(\implies (n,  n - 1, 2)-\)kód
4. Hammingův kód
	- \(\implies (7,  4, 3)-\)kód

### 11. přednáška

#### Jak nejefektivněji můžeme kódovat?

{:.rightFloatBox}
<div markdown="1">
Maximální dimenze kódu (logaritmus počtu kódových slov), když určím délku a vzdálenost.
</div>

- \(A(n, d) = \underset{C}{\mathrm{max}} \log |C|\)
	- \(C\) jsou binární kódy délky \(n\) s min. vzdáleností \(\ge d\)
	- \(A(n, 1) = n\) (triviální kód)
	- \(A(n, 2) \ge n - 1\) (paritní kód má \(|C| = 2^{n -1}, d = 2\))

(👀) \(\forall d \le n, d \ge 2: A(n, d) \le A(n - 1, d - 1)\)
- po odstranění bitu vzdálenost slov klesne nejvýše o \(1\) (pokud se slova v bytu liší); velikost nového kódu \(|C'| = |C|\) (díky předpokladu funguje, žádná slova se nesloučí)

{:.rightFloatBox}
<div markdown="1">
Není to Simpletonův, ale Singletonův (viz. [Wikipedia](https://en.wikipedia.org/wiki/Singleton_bound)). Byť je ten odhad docela triviální 🙂.
</div>

**Věta (Singletonův odhad):** \(\forall d \le n\) platí \(A(n, d) \le n - d + 1\)
- \(A(n, d) \le A(n - 1, d - 1) \le \ldots \le A(n - d + 1, 1) = n - d + 1\)
- rovněž dostávám \(A(n, 2) \le A(n - 1, 1) = n - 1\) a vím, že \(A(n, 2) \ge n - 1\), tedy rovnost

**Tvrzení:** pro každé sudé \(d \le n\) je \(A(n, d) = A(n - 1, d - 1)\)

**Důkaz:** nechť \(C\) je \((n - 1, k, d - 1)\)-kód. Přidáním paritního bitu ke každému slovu vytvořím \((n, k, d)-\)kód, protože slova \(c\) v liché vzdálenosti (speciálně \(d - 1\)) v \(C'\) mají vzdálenost o 1 větší (liší se jejich paritní symboly).
- \(\implies\) nejzajímavější jsou kódy s lichým \(d\) (na sudé lze triviálně rozšířit)

#### Lineární kódy

**Definice:** kód \(C\) nad \(\mathbb{Z}_2^n\) je lineární kód, pokud tvoří vektorový podprostor.
- \(\forall c, c' \in C: c + c' \in C\)
- \(\forall \alpha \in \mathbb{Z}_2: \alpha c \in C\)

(👀) pokud \(C\) je dimenze \(k\), pak má \(2^k\) prvků, ale k jeho popisu stačí nějaká báze \(C \equiv k\) slov t. ž. ostatní dostanu lineárními kombinacemi.

**Příklad:** Hammingův kód \(\mathcal{H}\) je lineární a generuje ho **generujicí matice**
\[
\begin{matrix}
	v_1 \\
	v_2 \\
	v_3 \\
	v_4
\end{matrix}
\begin{pmatrix}
	1 & 1 & 0 & 1 & 0 & 0 & 0 \\
	0 & 1 & 1 & 0 & 1 & 0 & 0 \\
	0 & 0 & 1 & 1 & 0 & 1 & 0 \\
	0 & 0 & 0 & 1 & 1 & 0 & 1
\end{pmatrix}\]

- generující matice kódu \(H\)
- \(\left\{v_1, \ldots, v_4\right\}\) je báze \(H\)
- \(\forall c \in H\ \exists \alpha_1, \ldots, \alpha_4 \in \mathbb{Z}_2\) t. ž. \(c = \sum_{i = 1}^{4} \alpha_i v_i \)

(👀) \(\forall x, y, z \in C: d(x, y) = d(x + z, y + z)\)
- „posunutí nějakým směrem“
- platí pro všechny kódy, ale hodí se jen u lineárních kódů, protože díky tomu, že tvoří VP je součet také kódové slovo
- \(x + z, y + z \in C\) (lineární kódy)
	- \(d(x, y) = d(0, y - x)\)
	- \(\Delta(C) = \underset{x, y \in C}{\mathrm{min}}\ d(0, y - x) \implies \underset{x \in C}{\mathrm{min}}\ d(0, x)\), což je počet nenulových souřadnic

---

- \(\langle x, y \rangle = \sum_{i = 1}^{n} x_i \cdot y_i\)
	- něco jako skalární součin
	- nemusí platit, že \(x \neq 0 \implies \langle x, x \rangle \neq 0\) (např. pro \((1\ 1\ 0\ 0)\))

**Definice (duální kód)** \(C\) je ortogonální doplněk \(C^\perp = \left\{x\ |\ \langle x, y \rangle = 0, \forall y \in C\right\}\)
- může být \(C \cap C^\perp \neq \left\{0\right\}\), ale platí \(\dim C + \dim C^\perp = n\)

(👀) \(C^\perp\) je opět vektorový podprostor, je to tedy taky kód
- má také generující matici \(M\) (tzv. **paritní/kontrolní**)
- platí \(C = \left\{x\ |\ Mx = 0\right\}\) (z definice naší „ortogonality“)
	- stačí ověřit ortogonalitu na bázové vektory

(👀) nechť \(G\) je generující matice kódu \(C\)
- \(G\) můžu zgausoeliminovat na \(G'\), která stále generuje \(C\)
- ke kódování daného slova stačí sečíst příslušné řádky \(G'\), protože se jedná o jediný způsob, jak dostat bity slova

\[c = (1\ 1\ 0\ 1) \qquad x = (\underbrace{1\ 1\ 0\ 1}_{\text{informační bity}} \overbrace{\ldots\ldots\ldots}^{\text{kontrolní/paritní bity}})\]

##### Dekódování

Mějme \(C\) lineární kód délky \(n\) nad \(\mathbb{Z}_2^4\). Bylo odesláno slovo \(x \in C\) a přijato slovo \(\tilde{x}\).
- mohly nastat chyby \(e = \tilde{x} - x\) (chybový vektor)
	- chceme ho objevit, abychom rozluštili \(x\)

\(P\) je paritní matice kódu \(C\), tzn. \(C = \left\{x\ |\ Px = 0\right\}\).

**Definice (syndrom)** slova \(z\) je \(Pz\), kde \(P\) je paritní matice kódu \(C\).
- (👀) kódová slova \(\equiv\) slova se syndromem \(0\) (viz. definice \(P\)...)

**Předpoklad:** chybový vektor \(e\) je slovo s nejmenší vahou ve své třídě
- **třída** \(= \left\{e'\ |\ Pe' = P\tilde{x} = P(x + e) = Px + Pe = Pe\right\}\) (slova se stejným syndromem)
- pro syndrom \(s \in Z_2^k\) je slovo \(m(s) \in Z_2^n\) t. ž. \(P m(s) = s\) a \(w(m(s))\) je minimální tzv. **reprezentant**

**Dekódování:**
- vezmu \(s = P\tilde{x}\)
- najdu reprezentanta \(m(s)\)
- výsledek dekódování \(y = \tilde{x} - m(s) = \tilde{x} - m(P\tilde{x})\)
	- (👀)  \(y\) má mezi kódovými slovy nejmenší vzdálenost od \(\tilde{x}\)

**Příklad:**
- \(G = \begin{matrix} v_1 \\ v_2 \end{matrix} \begin{pmatrix} 1 & 1 & 1 & 0 & 0 \\ 0 & 0 & 1 & 1 & 1 \end{pmatrix}\)
- \(k = 2\), máme \(4\) slova \(\left\{v_1, v_2, (0\ \ldots\ 0), v_1 + v_2\right\}\)
- \(\Delta(C) = 3\) (počet jedniček vektoru báze)
- jedná se o \((5, 2, 3)-\)kód
- \(P = \begin{pmatrix} 1 & 1 & 0 & 0 & 0 \\ 0 & 1 & 1 & 1 & 0 \\ 0 & 0 & 0 & 1 & 1 \end{pmatrix}\)

1. \(\tilde{x} = v_1 = (1\ 1\ 1\ 0\ 0)\), \(P\tilde{x} = \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix}\) (nulový syndrom, což je správně)
2. \(\tilde{x} = (0\ 0\ 1\ 0\ 1)\), \(P\tilde{x} = \begin{pmatrix} 0 \\ 1 \\ 1 \end{pmatrix}\) (nějaký syndrom)
	- podíváme se do tabulky syndromů (vybruteforcená)
	- dostaneme ze syndromu reprezentanta \(m(s) = (0\ 0\ 0\ 1\ 0)\)
	- spočítáme \(x = \tilde{x} - e = (0\ 0\ 1\ 1\ 1)\)
	- protože došlo k chybě v \(1\) pozici a jedná se o \((5, 2, 3)\)-kód, \(x\) je správné dekódování
3. pro \(\tilde{x} = (0\ 1\ 1\ 0\ 1)\) dostáváme váhu syndromu \(2\) a to už neopravíme

##### Hammingovy kódy
(👀) nechť \(P\) je kontrolní matice \(C\). Pak \(\Delta(C) = \) maximální \(d\) t. ž. \(\forall d - 1\) sloupců \(P\) je lineárně nezávislých.

**Důkaz:** kódová slova \(\equiv Pc = 0\). Nechť sloupce \(P\) jsou \(p_1, \ldots, p_n\). Pak
\[\sum_{i = 1}^{n} c_i p_i = 0\]

Pro spor nechť \(\exists x\) t. ž. \(\sum x_i p_i = 0\) (je tedy kódové slovo) a \(w(x) < d \rightarrow\). To je spor, \(\Delta(C) = d\) ale tohle slovo má \(w(x) < d\). To musí nutně znamenat, že \(\forall x: w(x) < d \rightarrow \sum_{i = 1}^{n}x_i p_i \neq 0 \rightarrow\) každých \(\le d - 1\) sloupců je tedy lineárně nezávislých.

**Důsledek:** pokud chci \(d = 3\), potřebuji co největší matici \(P\) t. ž. \(\forall 2\) sloupce jsou lineárně nezávislé. To v \(\mathbb{Z}_2\) znamená, že musí být různé a žádný z nich není nulový.

\[
P = \underbrace{\begin{pmatrix}
	0      & 0      & 0      & \cdots & 1 \\
	\vdots & \vdots & \vdots & \ddots  & 1 \\
	0      & 1      & 1      &        & 1 \\
	1      & 0      & 1      &        & 1
\end{pmatrix}}_{\text{$2^r - 1$ nenulových $r$-dim. vektorů}}
\]

Jedná se o binární zápisy čísel \(1 \ldots 2^{r} - 1\). Nechť \(C\) je generovaný \(P\) a \(\mathcal{H}_r = C^\perp\) (\(P\) je paritní matice \(\mathcal{H}_r\)). Má délku \(n = 2^{r} - 1\) a \(\dim \mathcal{H}_r = n - r = 2^{r} - r - 1\).
- \(n - r\) funguje, protože mají komplementární dimenze

Z pozorování (nezávislé sloupce) dostáváme, že \(\Delta(\mathcal{H}_r) = 3\).

**Věta:** pro každé \(r \ge 2\) je \(\mathcal{H}_r \left[2^{r} - 1, 2^r - r - 1, 3\right]\)-kód.

### 12. přednáška
- (👀)  \(G = \left[I_k\ |\ P\right] \implies M = \begin{bmatrix} -P \\ I_{n - k} \end{bmatrix}^T\)

#### Dekódování Hammingova kódu
- předpoklad: \(e\) má nejvýše \(1\) jedničku
	- došlo k \(\le 1\) chybě
- \(M\) je ve tvaru uvedeném výše (binární zápisy čísel \(1 \ldots 2^{r} - 1\))
	- pozorování: syndrom \(M \tilde{x} = Me\) je \(y_i \equiv\) binární zápis \(i \iff\) došlo k chybě na pozici \(i\)

#### Perfektnost kódu
Pokud pro \(C\) platí \(\Delta(C) = 2t + 1\), pak pro každé slovo \(x \in \mathbb{Z}^n_2\) je nejvýše jedno kódové slovo ve vzdálenosti \(\le t\) od \(x\). jsou to tedy **symetrické koule** se středem \(x\) a poloměrem \(t\), \(B(x, t) = \left\{z \in \mathbb{Z}_2^n\ |\ d(x, z) \le t\right\}\); jsou pro různá \(x \in C\) disjunktní.

**Věta (Hammingův odhad):** pro binární kód s \(\Delta(C) \ge 2t + 1\) platí \[|C| \le \frac{2^n}{V(n, t)} \]
- \(2^n\) je počet všech slov
- \(V(n, t)\) je objem kombinatorické koule dimenze \(n\) o poloměru \(t\) \(= \sum_{i = 0}^{t} \binom{n}{i}\) (vždy způsoby, jak si vybrat \(i\) bitů a flipnout je)

**Důkaz:** mám na \(2^n\) prvcích \(|C|\) disjunktních koulí objemu \(V(n, t)\)... koule pokrývají \(|C| \cdot V(n, t)\) prvků, což je \(\le 2^n\) (méně nebo rovno všem prvkům -- nevím, jestli se nepřekrývají) a vydělím.

---

{:.center}
![](/assets/kombinatorika-a-grafy-i/komb-koule.svg)

---

**Definice:** kód \(C\) je perfektní, pokud pro něj platí Hammingův odhad s rovností.

**Příklady perfektních kódů:**
- totální (koule o poloměru 1)
- opakovací kód liché délky 
- jednoprvkový kód (koule zaplňuje celý prostor)

**Tvrzení:** Hammingův kód je perfektní

**Důkaz:** \(\mathcal{H}_r = \left[2^r - 1, 2^r - r - 1, 3\right]\)-kód.
- \(3 = 2t + 1 \implies t = 1, V(n, t) = V(2^r - 1, 1) = 2^r\)
	- poslední rovnost je počet vektorů lišící se v \(1\) souřadnici, \(+\) střed koule

- \(k = \text{dimenze} = 2^r - r - 1\)
- \(|C| = 2^k = 2^{2^r - r - 1}\)

\[\frac{2^n}{V(n, t)} = \frac{2^{2^r - 1}}{2^r} = 2^{2^r - r - 1} = |C|\]

#### Hadamardův kód
- **duál Hammingova kódu** (prohození generující matice s paritní maticí pro Hammingův kód \(G \longleftrightarrow K\) dává Hadamardův kód)

- \(x \ldots\) zpráva délky \(r\)
- \(c = (c_1, \ldots, c_{2^r - 1})\)
	- \(c_i = \langle x, y_i \rangle\), kde \(y_i\) jsou binární zápisy čísla \(i\)

**Tvrzení:** Hadamardův kód je \(\left[2^r, r, 2^{r - 1}\right]\)-kód.

(👀) \(\langle x, y_i \rangle\) nenese informaci o \(x_1\), pokud první bit \(y\) je \(0 \implies\) stačí brát \(y_i, i \in \left(2^{r - 1} , 2^r - 1\right)\)
- jedná se o **rozšířený Hadamardův kód** \(\left[2^r, r + 1, 2^{r - 1}\right]\)

#### Ramseyova teorie

**Motivace:** party o \(6\) lidech::

{:.center}
![](/assets/kombinatorika-a-grafy-i/ramsey-motivace.svg)

**Věta:** pro každý graf na \(\ge 6\) vrcholech \(\exists\) podrgraf \(E_3\) (prázdný graf) nebo \(K_3\).
- \(\omega(G) \ge 3\) -- velikost maximální kliky
- \(\alpha(G) \ge 3\) -- velikost maximální nezávislé množiny

{:.rightFloatBox}
![](/assets/kombinatorika-a-grafy-i/ramsey-obr.svg)

**Důkaz:** vyberu libovolný vrchol \(u\). Podívám se na vrcholy \(A\), se kterými nesousedí, zbytek nechť je \(B\).

1. \(|A| \ge 3, A \supseteq \left\{x, y, z\right\} \)
	- všichni mezi sebou mají hranu, pak máme \(K_3\)
	- BUNO \(\exists\) nehrana \(xy\), pak \(\left\{u, x, y\right\}\) tvoří \(E_3\)
2. symetricky

**Věta (obecnější Ramseyova):** nechť \(G\) má \(\ge \binom{k + l - 2}{k - 1}\) vrcholů \(\implies \omega(G) \ge k\)  nebo \(\alpha(G) \ge l\).
- (👀) ze symetrie kombinačních  čísel máme symetrii v \(k, l\), protože \(\binom{k + l - 2}{k - 1} = \binom{k + l - 2}{l - 1}\)

**Důkaz:** indukcí podle \(k + l\)
- pro \(k = 1, l = 1\) a \(k = 2, l = 2\) jednoduché (vždy existuje hrana/nehrana)
- pro \(k, l \ge 2\) a tvrzení platí pro \(k, l - 1\) a \(k-1, l\)
	- \(n_1 = \binom{k + l - 3}{k - 1}\) a \(n_2 = \binom{k + l - 3}{l - 1 = k - 2}\) (dřívější odhady)
		- (👀) platí, že \(n = n_1 + n_2\)

Zvolím \(u \in G\) libovolně a opět rozdělím graf na nesousedy \(A\) a sousedy \(B\) vrcholu \(u\). Z principu holubníku ([Dirichletův princip](https://mathworld.wolfram.com/DirichletsBoxPrinciple.html)) je \(|A| \ge n_1\) nebo  \(|B| \ge n_2\) (jsou-li ostře menší, tak dají \(n - 2\)).
1. \(|A| \ge n_1\), použiji indukci na \(A\):
	- \(\omega(G[A]) \ge k\) a jsem hotov
	- \(\alpha(G[A]) \ge l - 1\), pak tato nezávislá množina spolu s \(u\) dává nezávislou mnozinu velikosti \(\ge l\)
2. analogicky: \(|B| \ge n_2\), použiji indukci na \(B\):
	- \(\omega(G[B]) \ge k - 1\), pak tato klika spolu s \(u\) dává kliku velikosti \(\ge k\)
	- \(\alpha(G[B]) \ge l\) a jsem hotov

**Důsledek:** \(\forall k, l \exists r(k, l)\) t. ž. \(\forall G: \omega(G) \ge k\) nebo \(\alpha(G) \ge l\).
- \(r(k, l) = \mathrm{min}\ N\) t. ž. platí \(\forall G\) velikosti \(N\) platí výše uvedené
- podle věty nahoře máme \(r(k, l) \le \binom{k + l - 2}{k - 1}\)

**Pár hodnot:**
- \(r(1, l) = 1\)
- \(r(k, 1) = 1\)
- \(r(2, l) = l\)
- \(r(k, 2) = k\)
- dříve jsme dokázali, že \(r(3, 3) \le 6 \) a z \(C_5\) víme, že \(r(3, 3) > 5\), tedy \(r(3, 3) = 6\)

**Definice \(r(k, k)\)** symetrické Ramseyovo číslo, říká se mu \(r(n) = r(n, n)\). „Jak velký musí být graf, abych tam našel buď \(E_n\) nebo \(K_n\)“.

**Věta:** \(k, n \in \mathbb{N}\) t. ž. \(\binom{n}{k} 2^{1 - \binom{k}{2}} < 1 \implies r(k) > n\).

Co jsou čísla zač? Použijeme odhad:
- \(\binom{n}{k} \le \frac{n^k}{k!} < \frac{n^k}{2^{k/2 + 1}}\)

\[\binom{n}{k}2^{1 - \binom{k}{2}} < \frac{n^k}{2^{k/2 + 1}} 2^{1 - k(k - 1) / 2} = \left(\frac{n}{2^{k / 2}}\right)^k\]

Kde poslední \(=\) platí, protože:
\[\frac{1}{2^{k/2 + 1}} 2^{1 - k(k - 1)/2} = \frac{1}{2 \cdot 2^{k/2}} \frac{2}{2^{k(k - 1)/2}} = \frac{1}{2^{k/2 (1 + k - 1)}} = \left(\frac{1}{2^{k/2}}\right)^k\]

**Důsledek:** \(\forall k \ge 3: r(k) > 2^{k/2}\)
- dosadíme \(n = 2^{k/2}\) do předchozího (předchozí je ostrý odhad, takže \(1^k < 1\) funguje)

**Důkaz:** vezmu náhodný graf \(G\) t. ž. každá z \(\binom{n}{2}\) hran má pravděpodobnost \(1/2\), nezávisle na ostatních. Nechť \(K \subseteq V, |K| = k\). \(A_K \ldots\) jev, že \(G[K]\) je klika. \(\Pr[A_K] = \left(\frac{1}{2}\right)^{\binom{k}{2}} = 2^{-\binom{k}{2}}\). Obdobně \(B_K\) jev, že vznikla nezávislá množina a \(C_K \ldots A_K \cup B_K \ldots \Pr[C_K] = 2 \cdot 2^{-\binom{k}{2}} = 2^{1 - \binom{k}{2}}\). \(p \ldots\) pravděpodobnost, že \(\exists K \subseteq V\) t. ž. nastal jev \(C_K\). Je ji těžké určit, protože jevy nejsou nezavislé (množiny se mohou překrývat), nám ale stačí odhad který předpokládá, že jsou jevy nezávislé:

\[\Pr[C] \le \sum_{K \in V, |K| = k} \Pr[C_K] = \binom{n}{k} \cdot 2^{1 - \binom{k}{2}} < 1\]
- předposlední rovnost je z definice -- všechny možné \(K\)-tice
- poslední nerovnost je předpoklad věty
- máme, že pravděpodobnost, že nějaká \(K\)-prvková množina bude tvořit buďto kliku nebo nezávislou množinu velikosti \(k\) je \(< 1\), tedy pravděpodobnost, že to nenastane je \(> 0\), tedy \(\exists\) nějaký z náhodných grafů, který tohle nesplňuje
	- pokud pravděpodobnost je nenulová, tak musí existovat nějaké množství grafů, které tenhle jev mají (protože jinak by nerovnost nebyla ostrá)

**Jiný důkaz:**
Někomu může použití pravděpodobnosti připadat trochu magické.
Důkaz lze ale přeformulovat explicitněji.

Uvažme všechny grafy na \(n\) vrcholech. Těch je \(2^{\binom{n}{2}}\).
Kolik z nich obsahuje kliku nebo nezávislou množinu velikosti alespoň \(k\)? Tedy,
kolik z nich je "dobrých"?
Začněme jednodušeji -- označme množinu vrcholů \(V\) a mějme \(K \subseteq V, |K| = k\).
V kolika grafech tvoří \(K\) kliku? Hrany uvnitř \(K\) jsou fixované, ostatní můžeme nastavovat libovolně.
Odpověď je tedy \(2^{\binom{n}{2}-\binom{k}{2}}\). Případ nezávislé množiny je
symetrický, tudíž v \(2 \, 2^{\binom{n}{2}-\binom{k}{2}} = 2^{\binom{n}{2}-\binom{k}{2}+1}\) grafech
bude \(K\) klika nebo nezávislá množina.

Nyní zásadní krok: V součtu \(\binom{n}{k} 2^{\binom{n}{2}-\binom{k}{2}+1}\) přes všechny takové
množiny \(K\) jsme započítali každý dobrý graf (nejspíše vícekrát, ale to nevadí). Každý dobrý
graf totiž obsahuje kliku nebo nezávislou množinu velikosti **přesně** \(k\).
Tento součet je tedy horní mezí pro počet dobrých grafů.

A jsme hotovi. Předpoklad věty je totiž po přenásobení ekvivalentní nerovnosti:

\[\binom{n}{k} 2^{\binom{n}{2}-\binom{k}{2}+1} < 2^\binom{n}{2}\]

A z té díky našemu odhadu tranzitivně plyne, že počet dobrých grafů je menší než počet všech grafů. Tedy
existuje nedobrý graf na \(n\) vrcholech a \(r(k,k) > n\).

### 13. přednáška

#### Ramseyovy barevné/nekonečné věty

{:.rightFloatBox}
<div markdown="1">
„Pokud mám alespoň \(\ge N\) prvků a dávám je do \(t\) holubníků, pak bude existovat holubník s alespoň \(k\) prvky.“
</div>

**Věta (princip holubníku):** pro každé \(t, k \in \mathbb{N} \exists N\) t. ž. \(\forall c: [n] \mapsto [t]\) platí, že \(\forall n \ge N \exists A \subseteq [n], |A| = k\), na níž je funkce \(c\) konstantní.

**Důkaz:** \(N = t (k - 1) + 1\).

**Věta (nekonečný princip holubníku):** pro každé \(t \in \mathbb{N}\) a každé \(c: \mathbb{N} \mapsto [t]\) existuje nekonečná množina \(A \subseteq \mathbb{N}\), pro níž je funkce \(c\) konstantní.
- z „existuje holubník s hodně holuby“ máme „existuje holubník s nekonečně holuby“

**Důkaz:** rozdělím \(\mathbb{N}\) na \(B_1, \ldots, B_t\), kde \(B_i = \left\{m \in \mathbb{N}\ |\ c(m) = i\right\}\). Protože sjednocením je nekonečná množina pak alespoň jedna musí být nekonečná.

**Věta (nekonečná Ramseyova (vícebarevná) věta):** pro každé \(t \in \mathbb{N}, \forall c: \binom{\mathbb{N}}{2} \mapsto [t] \exists\) nekonečná množina \(A \subseteq \mathbb{N}\), pro níž je funkce \(c\) na hranách \(\binom{A}{2}\) (nekonečný úplný graf) konstantní.

{:.rightFloatBox}
<div markdown="1">
sanity check: \(A_1 \supset A_2 \supset \ldots \)
</div>

**Důkaz:** sestrojím posloupnost nekonečných množin \(A_1 = \mathbb{N}\) a pro \(i = 1, 2, \ldots\) opakujeme:
- vybereme \(v_i \in A_i\)
- rozdělíme \(A\) na \(B_i^1, B_i^2\ldots, B_i^t\) podle toho, jakou barvu má hrana, která množinu spojuje s \(v_i\)
	- jelikož \(A_i\) je nekonečná, tak \(\exists B_i^j\) pro nějakou barvu, která je také nekonečná
- položme \(A_{i + 1} = B_i^j\)

(👀) posloupnost vrcholů \(v_1, v_2, \ldots\) má vlastnost, že pokud \(i < j\), pak \(\left\{v_i, v_j\right\}\) má barvu \(b_i\)
- v každém kroku se zanořuju, ale při zanoření už platí, že všichni sousedi jsou k \(v_i\) spojeni hranou dané barvy
- \(\implies\) barva hrany \(\left\{v_i, v_j\right\}\) závisí pouze na \(i\), ne na \(j\)
- mám posloupnost barev \(b_1, b_2, b_3, \ldots\)
	- je nekonečná, ale opakuje se tu konečně mnoho hodnot
	- aplikuji nekonečný holubník \(\implies \exists j \in [t]\) opakující-se nekonečněkrát a takové vrcholy vyberu, jednota barev vychází z pozorování

{:.rightFloatBox}
<div markdown="1">
„Pokud \(n \ge N\), tak každé obarvení \(K_n\) \(t\) barvami obsahuje jednobarevný \(K_k\) jako podgraf.“
</div>

**Věta (Ramseyova vícebarevná věta):** \(\forall t, k \in \mathbb{N}\) (\(t\) počet barev, \(k\) velikost kliky) \(\exists N \in \mathbb{N}\) t. ž. \(\forall c: \binom{[n]}{2} \mapsto [t], \forall n \ge N\) (obarvení \(K_n\) \(t\) barvami) existuje množina \(A \subseteq [n], |A| = k\), pro níž je funkce \(c\) na \(\binom{A}{2}\) konstantní.


**Důkaz:** adaptujeme nekonečný na konečný případ -- chtěli bychom posloupnost barev \(b_1, \ldots, b_{tk}\) -- když do toho praštíme holubníkem, tak máme barvu, která je tam \(k\)-krát. 
- upravím konstrukci množin \(A_i\): beru vždy největší třídu
	- \(|A_{i + 1}| \ge \frac{|A_i| - 1}{t}\) (max. je větší/roven průměru)
	- potřebuji, aby konstrukce běžela alespoň \(tk\) kroků
	- potřebuji, aby \(|A_{tk}| \ge 1, |A_{tk - 1}| \ge t + 1, \ldots, |A_1| \ge \sum_{i = 0}^{tk} t^i = \frac{t^{tk + 1} - 1}{t - 1}\)
		- na zkoušce nebude -- jen bychom měli vědět, že se to takhle dá umlátit

**Definice (hypergraf)** je zobecněný graf, kde:
- hrany jsou libovolné množiny (místo dvojic, jako v normálním grafu)
- **uniformní** hypergraf -- hrany jsou \(p\)-prvkové množiny
- \(p\) je arita hran (velikost množin), \(t, k\) jsou stejné


**Věta (nekonečná Ramseyova věta pro \(p\)-tice):** \(\forall p, t \in \mathbb{N}\) a \(\forall c: \binom{\mathbb{N}}{p} \mapsto [t] \exists A \subseteq \mathbb{N}\) nekonečná t. ž. \(c\) je na \(\binom{A}{p}\) konstantní.

**Důkaz:** indukcí podle \(p\), pro \(p=1\) je to nekonečný holubník (pro \(p = 2\) je to Ramsey)
- IP: věta platí pro \(p - 1\)
- opět konstruuji nekonečnou posloupnost \(A_i\)
- v kroku \(i\) vyberu \(v_i \in A_i\), nechť \(A_i' = A_i \setminus \left\{v_i\right\}\)

{:.rightFloatBox}
<div markdown="1">
Pomocné obarvení \((p-1)\)-tic stejnými barvami, jako byla \(p\)-tice s vrcholem \(v_i\).
</div>

- definuji obarvení \((p - 1)\)-tic \(A_i'\): \(c_i'(Q) = c(Q \cup \left\{v_i\right\})\), \(Q \subseteq A_i'\), \(|Q| = p - 1\)
- z IP pro \(A_i'\) máme, že \(\exists B_i \subseteq A_i'\), na jejichž \((p-1)\)-ticích je obarvení \(c_i'\) konstantní \( = b_i \in [t]\) a \(A_{i + 1} = B_i\) si vezmu do dalšího kroku

(👀) barva \(p\)-tice \(\left\{v_{i_1}, \ldots, v_{i_p}\right\}\) (vzhledem k vzniklé posloupnosti \(v_1, v_2, \ldots\)), kde \(i_1 < i_2 < i_3 < i_p\) závisí pouze na barvě prvku \(v_{i_1}\)
- vyberu z barev nějakou opakující-se nekonečněkrát a vrcholy s příslušnými indexy tvoří \(A\)

**Věta (Ramseyova věta pro \(p\)-tice):** \(\forall p, t, k \in \mathbb{N} \exists N \in \mathbb{N}\) t. ž. \(\forall n \ge N, \forall c: \binom{[n]}{p} \mapsto [t]\ \exists A \subseteq [n], |A| = k\) t. ž. \(c\) je na \(\binom{A}{p}\) konstantní.

**Důkaz:** mějme \(p, k, t\) z předpokladu věty. Uvážíme \(c_i: \binom{[n]}{p} \mapsto [t]\). To je _dobré_, pokud \(\exists \) \(k\)-prvková jednobarevná podmnožina, jinak je _špatné_. Věta tedy tvrdí, že \(n \ge N\) jsou všechna \(c\) _dobrá_.

Sporem: předpokládejme, že pro nekonečně mnoho \(n\) \(\exists\) _špatné_ obarvení.

(👀) Pokud \(S_n\) je množina _špatných_ obarvení a \(S_n\) je neprázdné, pak \(S_{n - 1}\) je neprázdné, protože mám-li _špatné_ obarvení \(p\)-tic nad \(n\), tak mohu zapomenout na \(n\)-tý prvek a tak dostanu _špatné_ obarvení i na \(n - 1\).
- **zůžení** \(z(c)(Q) = c(Q), Q \subseteq [n - 1], |Q| = p\) (prostě odeberu vrchol)

Strukturu _špatných_ obarvení popíšeme stromem, kde hladiny jsou obarvení \(S_n\); platí:
- všechny hladiny jsou neprázdné (předpoklad pro spor)
- všechny hladiny jsou konečné (nad \(S_n\) může být only so much obarvení)

**Lemma (Königovo):** nekonečný zakořeněný strom s konečnými stupni obsahuje nekonečnou cestu z kořene.

**Důkaz:** pokud máme vrcholy \(v_1, v_2, \ldots, v_{i - 1}\) na cestě, tak \(v_i\) vezmu jako kořen podstromu, který je nekonečný a opakuju.

Díky tomuto lemmatu víme, že \(\exists\) nekonečná cesta z \(S_0\). Z nekonečné Ramseyovy věty ale víme, že kdyby tomu tak bylo, tak neplatí, protože by existovalo nekonečné obarvení přirozených čísel (podle nekonečné cesty v tomto stromu).

### [Forma zkoušky](/assets/kombinatorika-a-grafy-i/okruhy_kg1.pdf)

### Zdroje/materiály
- [https://research.koutecky.name/db/teaching:kg12021_prednaska](https://research.koutecky.name/db/teaching:kg12021_prednaska) -- stránka cvičení
	- odkaz na všechny obrázky, zdroje, nahrávky cvičení
- [Poznámky Václava Končického](https://kam.mff.cuni.cz/~koncicky/notes/kag2/pdf) z roku 2019.
- [https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols](https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols) -- \(\LaTeX\)ové matematické symboly

### Poděkování
- Matěji Kripnerovi za řadu PR opravujících chyby a přidávajících dodatečné informace.
- Filipu Peškovi za upozornění na několik překlepů/chyb v důkazech a definicích.
- Vojtěchu Kočandrlemu za PR a upozornění na překlepy.
