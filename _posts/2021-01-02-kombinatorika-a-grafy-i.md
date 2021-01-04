---
language: cz
title: Kombinatorika a Grafy I
category: "lecture notes"
---

- .
{:toc}

### Úvodní informace
Tato stránka obsahuje moje poznámky z přednášky Martina Kouteckého z roku 2020/2021. Pokud by byla někde chyba/nejasnost, tak ji prosím buďto [opravte pull requestem](https://github.com/xiaoxiae/slama.dev/blob/master/_posts/), nebo mi dejte vědět mailem.

### 1. přednáška

#### Odhady faktoriálu

**Věta (meh odhad):**
{% latex display %}n^{n/2} \le n! \le \left(\frac{n + 1}{2}\right)^n{% endlatex %}

**Důkaz {% latex %}\ge{% endlatex %}:**
{% latex display %}
\begin{aligned}
	\left(n!\right)^2 &= 1 \cdot 2 \cdot 3 \cdot \ldots \cdot n \cdot n \cdot (n - 1) \cdot \ldots \cdot 2 \cdot 1 \\
	&= \prod_{i = 1}^{n} \left(i \cdot (n - i + 1)\right) \\
	&\le \left(\frac{n + 1}{2}\right)^n \qquad //\qquad i\left(n - i + 1\right) \le \frac{n + 1}{2},\ \forall i \in \left[n\right] \\
\end{aligned}
{% endlatex %}

Kde u poslední úpravy využíváme A-G nerovnost:

{% latex display %}
\begin{aligned}
	\sqrt{ab} &\le \frac{a + b}{2} \\
	\sqrt{i (n + 1 - i)} &\le \frac{i + n + 1 - i}{2} = \frac{n + 1}{2}
\end{aligned}
{% endlatex %}

**Důkaz {% latex %}\le{% endlatex %}:**

{% latex %}n \le i (n - i + 1), \forall i \in [n]{% endlatex %}:
- {% latex %}i = 1{% endlatex %} platí
- {% latex %}i = 2 \rightarrow{% endlatex %}  jeden člen je vždy {% latex %}\ge 2{% endlatex %}, druhý {% latex %}\ge n/2{% endlatex %}

{% latex display %}
\begin{aligned}
	\left(n!\right)^2 &= \prod_{i = 1}^{n} i\left(n - i + 1\right) \ge \prod_{i = 1}^{n}n = n^n \\
	n! &\ge n^{n/2}
\end{aligned}
{% endlatex %}

**Věta (nice odhad):**
{% latex display %}
e\left(\frac{n}{e}\right)^n \le n! \le en \left(\frac{n}{e}\right)^n
{% endlatex %}

**Důkaz (indukcí):**
- {% latex %}n = 1{% endlatex %}... {% latex %}e \cdot 1 \cdot \frac{1}{e} \le 1{% endlatex %}
- {% latex %}n - 1 \rightarrow n{% endlatex %}:
{% latex %}\begin{aligned} n! = n \left(n - 1\right)! &\le^\mathrm{IP} en \left(n - 1\right) \left(\frac{n - 1}{e}\right)^{n - 1} \\ &= en \left(\frac{n}{e}\right)^n \left(\frac{e}{n}\right)^n \left(n - 1\right) \left(\frac{n - 1}{e}\right)^{n - 1} \\
&= en \left(\frac{n}{e}\right)^n \underbrace{\left(\frac{n - 1}{n}\right)^n e}_{\le 1}
\end{aligned}{% endlatex %}

Důkaz, toho proč ten výraz {% latex %}\le 1{% endlatex %}:

{% latex display %}
\begin{aligned} 
\left(1 - \frac{1}{n}\right)^n e &\le \left(e^{-\frac{1}{n}}\right)^n e = e^{-1} e = 1 \qquad 1 + x \le e^x
\end{aligned}
{% endlatex %}

- pozn.: {% latex %}a \le b \implies a = b c{% endlatex %} pro {% latex %}c \le 1{% endlatex %}, proto to vlastně děláme

**Věta (Stirlingova formule)** (bez důkazu):
{% latex display %}n! \cong \sqrt{2 \pi n} \left(\frac{n}{e}\right)^n{% endlatex %}

#### Odhady binomických koeficientů

(👀) pro malé {% latex %}k << n \ldots \binom{n}{k} = \frac{n!}{(n - k)! k!} = \frac{n \cdot (n - 1) \cdot \ldots \cdot (n - k + 1)}{k!} \le n^k{% endlatex %}

**Věta (hodně meh odhad):**
{% latex display %}\frac{2^n}{n + 1} \le \binom{n}{\left\lfloor n/2 \right\rfloor} \le 2^n{% endlatex %}


**Důkaz:**
- součet všech čísel v řádku je {% latex %}2^n{% endlatex %}, tak jistě to největší nebude větší
- největší sčítanec je rovněž alespoň tak velký jako průměrný

**Věta (nice odhad):**
{% latex display %}\frac{2^{2m}}{2 \sqrt{m}} \le \binom{2m}{m} \le \frac{2^{2m}}{\sqrt{2m}}{% endlatex %}

**Důkaz:**

Nejprve jedno kouzlo:
{% latex display %}
P = \frac{1 \cdot 3 \cdot 5 \cdot \ldots \cdot (2m - 1)}{2 \cdot 4 \cdot 6 \cdot \ldots \cdot 2m} = \frac{1 \cdot 3 \cdot 5 \cdot \ldots \cdot (2m - 1)}{2 \cdot 4 \cdot 6 \cdot \ldots \cdot 2m}\frac{2 \cdot 4 \cdot 6 \cdot \ldots \cdot 2m}{2 \cdot 4 \cdot 6 \cdot \ldots \cdot 2m} = \frac{(2m)!}{2^{2m} \left(m!\right)^2} = \frac{\binom{2m}{m}}{2^{2m}}
{% endlatex %}

Chceme tedy:
{% latex display %}
\frac{1}{2 \sqrt{m}} \le P \le \frac{1}{\sqrt{2m}}
{% endlatex %}

Pak ještě druhé kouzlo:
{% latex display %}
\begin{aligned} 
	\left(1 - \frac{1}{2^2}\right) \left(1 - \frac{1}{4^2}\right) \ldots \left(1 - \frac{1}{\left(2m\right)^2}\right) &= \left(\frac{1 \cdot 3}{2 \cdot 2}\right) \left(\frac{3 \cdot 5}{4 \cdot 4}\right) \ldots \left(\frac{(2m - 1)(2m + 1)}{\left(2m\right)^2}\right) \\
	&= P^2 (2m + 1) < 1 \qquad //\ \text{součin věcí $<1$} \\
\end{aligned}
{% endlatex %}

Máme tedy:
{% latex display %}
\begin{aligned} 
	P^2 &< \frac{1}{2m + 1} < \frac{1}{2m} \\
	P &< \frac{1}{\sqrt{2m}} \\
\end{aligned}
{% endlatex %}

Druhá strana analogicky.

### 2. přednáška

#### Náhodné procházky

**Definice náhodné procházky  (v {% latex %}\mathbb{Z}^1{% endlatex %}):** Náhodný proces, v každém kroku se panáček z bodu {% latex %}0{% endlatex %} posune doprava nebo doleva.

- kde bude po {% latex %}n{% endlatex %} krocích?
- {% latex %}\lim_{n \to \infty} \ldots{% endlatex %} že se po {% latex %}n{% endlatex %} krocích vrátil (někdy v průběhu) do počátku?
- {% latex %}\lim_{n \to \infty} \ldots{% endlatex %} {% latex %}\mathbb{E}[\#\text{návratů do počátku}]{% endlatex %}?
	- dokážeme, že jde k nekonečnu

Zadefinujeme si náhodnou veličinu {% latex %}X = I_{S_2} + I_{S_4} + \ldots + I_{S_n} {% endlatex %}:
- {% latex %}I_{S_{2n}}\ldots{% endlatex %} indikátor, že nastal jev „po {% latex %}2n{% endlatex %} krocích jsem v počátku“
- {% latex %}\mathbb{E}[X] = \mathbb{E}[\#\text{návratů do počátku}]{% endlatex %}.
- {% latex %}\mathrm{Pr}[\text{po $2n$ krocích jsem v počátku}] = \binom{2n}{n}/2^{2n}{% endlatex %}.
	- nahoře jsou možnosti vyrovnaných počtů kroků doprava/doleva
	- dole jsou všechny scénáře pro {% latex %}2n{% endlatex %} kroků

{% latex display %}
\frac{\binom{2n}{n}}{2^{2n}} \ge \frac{\frac{2^{2n}}{2 \sqrt{n}}}{2^{2n}} = \frac{1}{2 \sqrt{n}}
{% endlatex %}

{% latex display %}
\begin{aligned}
	\mathbb{E}[X] &= \mathbb{E}\left[\sum_{i=1}^{\infty} I_{S_{2i}}\right]&& \\
	              &= \sum_{i=1}^{\infty} \mathbb{E}\left[I_{S_{2i}}\right]&&//\ \text{linearita střední hodnoty}\\
	              &= \sum_{i=1}^{\infty} \mathrm{Pr}\left[I_{S_{2i}}\right] &&//\ \text{střední hodnota indikátoru je pravděpodobnost}\\
	              &= \sum_{i=1}^{\infty} \frac{1}{2 \sqrt{i}} && //\  \text{diverguje, odhadneme přes } \sum \frac{1}{n} \\
\end{aligned}
{% endlatex %}

- zajímavost: ve {% latex %}2D{% endlatex %} to také platí, ale ve {% latex %}3D{% endlatex %} už ne (konverguje k nějakému konstantnímu číslu)!

#### Generující funkce

**Definice (mocninná řada)** je nekonečná řada tvaru {% latex %}a(x) = a_0 + a_1x^1 + a_2x^2 + \ldots,{% endlatex %} kde {% latex %}a_0, a_1 \ldots \in \mathbb{R}{% endlatex %}.

**Příklad:** {% latex %}a_0 = a_1 = \ldots = 1 \mapsto 1 +x + x^2 + \ldots{% endlatex %}
- pro {% latex %}|x| < 1{% endlatex %} řada konverguje k {% latex %}\frac{1}{1 - x}{% endlatex %}, můžeme tedy říct, že {% latex %}(1, 1, \ldots) \approx \frac{1}{1 - x}{% endlatex %}

**Tvrzení:** {% latex %}(a_0, a_1, a_2, \ldots){% endlatex %} reálná čísla. Předpoklad: pro nějaké {% latex %}K{% endlatex %} t. ž. {% latex %}|a_n| \le K^n{% endlatex %}. Poté řada {% latex %}a(x){% endlatex %} pro každé {% latex %}x \in \left(-\frac{1}{K}, \frac{1}{K}\right) {% endlatex %} konverguje (dává smysl). Funkce {% latex %}a(x){% endlatex %} je navíc jednoznačně určena hodnotami na okolí {% latex %}0{% endlatex %}.

**Definice (vytvořující/generující funkce):** nechť {% latex %}\left(a_0, a_1, \ldots\right){% endlatex %} je posloupnost reálných čísel. Vytvořující funkce této posloupnosti je mocninná řada {% latex %}a(x) = \sum_{i = 0}^{\infty} a_i x^i{% endlatex %}.

##### Operace na funkcích

| operace                                      | řada                                                                                                                          | úprava                                               |
| ---                                          | ---                                                                                                                           | ---                                                  |
| součet                                       | {% latex %}a_0 + b_0, a_1 + b_1, a_2 + b_2, \ldots{% endlatex %}                                                              | {% latex %}a(x) + b(x){% endlatex %}                 |
| násobek                                      | {% latex %}\alpha a_0, \alpha a_1, \alpha a_2, \ldots {% endlatex %}                                                          | {% latex %}\alpha a(x){% endlatex %}                 |
|                                              |                                                                                                                               |                                                      |
| posun doprava                                | {% latex %}0, a_0, a_1, \ldots {% endlatex %}                                                                                 | {% latex %} \alpha xa(x){% endlatex %}               |
| posun doleva                                 | {% latex %}a_1, a_2, a_3, \ldots {% endlatex %}                                                                               | {% latex %}\alpha \frac{a(x) - a_0}{x}{% endlatex %} |
|                                              |                                                                                                                               |                                                      |
| substituce {% latex %}\alpha x{% endlatex %} | {% latex %}a_0, \alpha a_1, \alpha^2 a_2, \ldots {% endlatex %}                                                               | {% latex %} \alpha a(\alpha x){% endlatex %}         |
| substituce {% latex %}x^n{% endlatex %}      | {% latex %}a_0, 0, \overset{n - 1}{\ldots}, 0, a_1, 0, \overset{n - 1}{\ldots}, 0, a_2, \ldots {% endlatex %}                 | {% latex %} \alpha a(x^n){% endlatex %}              |
|                                              |                                                                                                                               |                                                      |
| derivace                                     | {% latex %}a_1, 2a_1, 3a_2, \ldots {% endlatex %}                                                                             | {% latex %} \alpha a'(x){% endlatex %}               |
| integrování                                  | {% latex %}0, a_1, a_2/2, a_3/3, \ldots {% endlatex %}                                                                        | {% latex %} \int_{0}^{x} a(t) dt{% endlatex %}       |
|                                              |                                                                                                                               |                                                      |
| konvoluce                                  | {% latex %} \sum_{k = 0}^{n} a_k \cdot b_{n - k} {% endlatex %}                                                               | {% latex %} a(x) \cdot b(c){% endlatex %}            |

Všechny důkazy jsou jednoduché rozepsání z definice.

#### Zobecněná binomická věta

**Tvrzení:** {% latex %}r \in \mathbb{R}, k \in \mathbb{N}{% endlatex %}, def. {% latex %}\binom{r}{k} = \frac{r \cdot (r - 1) \cdot (r - 2) \cdot  \ldots  \cdot (r - k + 1)}{k!}{% endlatex %}
- pro {% latex %}r \in \mathbb{N}{% endlatex %} se shoduje s tím, co už známe
- vyplývá z toho, že funkce {% latex %}(1 + x)^r{% endlatex %} je vytvořující funkcí posloupnosti {% latex %}\left(\binom{r}{0}, \binom{r}{1}, \binom{r}{2}, \ldots\right){% endlatex %}
- (👀) pokud {% latex %}r{% endlatex %} je záporné celé, pak {% latex %}\binom{r}{k} = (-1)^k \binom{-r + k - 1}{k} = (-1)^k \binom{-r + k - 1}{-r - 1}{% endlatex %}, tedy {% latex %}\frac{1}{(1 - x)^n} = (1 - x)^{-n} = \binom{n - 1}{n - 1} + \binom{n}{n - 1}x + \binom{n + 1}{n - 1}x^2 + \ldots{% endlatex %}

**Příklad:** V krabici je {% latex %}30{% endlatex %} červených, {% latex %}40{% endlatex %} žlutých a {% latex %}50{% endlatex %} zelených míčků. Kolika způsoby lze vybrat {% latex %}70{% endlatex %}?

{% latex display %}
\begin{aligned}
	&(1 + x + \ldots + x^{30})(1 + x + \ldots + x^{40})(1 + x + \ldots + x^{50}) =\\ 
	&= \frac{1 - x^{31}}{1 - x} \frac{1 - x^{41}}{1 - x}\frac{1 - x^{51}}{1 - x} \qquad //\ \text{posuneme o $31$ míst a odečteme}\\
	&= \frac{1}{\left(1 - x\right)^3} \left(1 - x^{31}\right)\left(1 - x^{41}\right)\left(1 - x^{51}\right) \\
	&= \left(\binom{2}{2} + \binom{3}{2}x + \binom{4}{2}x^2 + \ldots\right) \left(1 - x^{31}\right)\left(1 - x^{41}\right)\left(1 - x^{51}\right) \\
	&= 1 + \ldots + \left[\binom{72}{2} - \binom{72 - 31}{2} - \binom{72 - 41}{2} - \binom{72 - 51}{2}\right]x^{70} + \ldots\\
	&= 1061
\end{aligned}
{% endlatex %}

Kde poslední rovnost platí, protože:
- z posledních 3 závorek si vybereme {% latex %}1{% endlatex %} a z první závorky koeficient u {% latex %}70{% endlatex %}
- ze druhé {% latex %}x^{31}{% endlatex %} a z první koeficient u {% latex %}72 - 31{% endlatex %}
	- analogicky pro {% latex %}41{% endlatex %} a {% latex %}51{% endlatex %} ze třetí a čtvrté

### 3. přednáška

#### Fibonacciho čísla
**Definice:** {% latex %}F_0 = 0, F_1 = 1, F_n = F_{n - 1} + F_{n - 2}, \forall n \ge 2{% endlatex %}
- {% latex %}F(x) = F_0 + F_1x + F_2x^2 + F_3x^3{% endlatex %}

| {% latex %}F_0{% endlatex %} | {% latex %}F_1{% endlatex %} | {% latex %}F_2{% endlatex %}       | {% latex %}F_3{% endlatex %}       | {% latex %}F_4{% endlatex %}       | Vytvořující funkce                |
| ---                          | ---                          | ---                                | ---                                | ---                                | ---                               |
| {% latex %}0{% endlatex %}   | {% latex %}1{% endlatex %}   | {% latex %}F_0 + F_1{% endlatex %} | {% latex %}F_1 + F_2{% endlatex %} | {% latex %}F_2 + F_3{% endlatex %} | {% latex %}F(x){% endlatex %}     |
| {% latex %}0{% endlatex %}   | {% latex %}0{% endlatex %}   | {% latex %}F_1{% endlatex %}       | {% latex %}F_2{% endlatex %}       | {% latex %}F_3{% endlatex %}       | {% latex %}x F(x){% endlatex %}   |
| {% latex %}0{% endlatex %}   | {% latex %}0{% endlatex %}   | {% latex %}F_0{% endlatex %}       | {% latex %}F_1{% endlatex %}       | {% latex %}F_2{% endlatex %}       | {% latex %}x^2 F(x){% endlatex %} |
| {% latex %}0{% endlatex %}   | {% latex %}1{% endlatex %}   | {% latex %}0{% endlatex %}         | {% latex %}0{% endlatex %}         | {% latex %}0{% endlatex %}         | {% latex %}x{% endlatex %}        |

Algebraickou úpravou dostáváme:
{% latex display %}
\begin{aligned}
	F(x) &= \frac{x}{1 - x - x^2} \\
	&= \frac{x}{\left(1 - \frac{1 + \sqrt{5}}{2}\right)\left(1 - \frac{1 - \sqrt{5}}{2}\right)} \qquad //\ \text{parciální zlomky }\\
	&= \frac{\frac{1}{\sqrt{5}}}{1 - \frac{1 + \sqrt{5}}{2}x} - \frac{\frac{1}{\sqrt{5}}}{1 - \frac{1 - \sqrt{5}}{2}x}\\
	&= \frac{1}{\sqrt{5}}\left(\frac{1}{1 - \frac{1 + \sqrt{5}}{2}x} - \frac{1}{1 - \frac{1 - \sqrt{5}}{2}x}\right) \qquad //\ \text{tvary $\frac{\pm 1}{1 - \lambda_{1, 2} x}$}\\
\end{aligned}
{% endlatex %}

Pro daný koeficient vytvořující funkce tedy máme:
{% latex display %}
\begin{aligned}
	F_n &= \frac{1}{\sqrt{5}} \left[\left(\frac{1 + \sqrt{5}}{2}\right)^n - \underbrace{\left(\frac{1 - \sqrt{5}}{2}\right)^n}_{\text{jde k $0$}}\right] \\
	&= \left\lfloor \frac{1}{\sqrt{5}} \left(\frac{1 + \sqrt{5}}{2}\right)^n \right\rfloor \\
\end{aligned}
{% endlatex %}

#### Catalanova čísla
- {% latex %}b_n = {% endlatex %} počet binárních zakořeněných stromů na {% latex %}n{% endlatex %} vrcholech
	- {% latex %}b_n = \sum_{k = 0}^{n - 1} b_k \cdot b_{n - k + 1}{% endlatex %}, rekurzíme se na obě části
	- jde si rozmyslet, že {% latex %}b(x) = x \cdot b(x) \cdot b(x) + 1{% endlatex %}
		- {% latex %}x{% endlatex %} je tam kvůli posunu, aby vycházelo správně indexování (suma nejde do {% latex %}n{% endlatex %})
		- {% latex %}1{% endlatex %} je tam kvůli tomu, aby nultý člen správně vycházel

{% latex display %}
\begin{aligned}
	b(x) &= x \cdot b(x)^2 + 1 \\
	b(x)_{1, 2} &= \frac{1 \pm \sqrt{1 - 4x}}{2x} \qquad //\ \text{ten s $+$ nedává smysl, diverguje}\\
	\\
	b(x) &= \frac{1 - 1 - \sum_{k = 1}^{\infty}(-4)^k \binom{1/2}{k} x^k }{2x} \qquad //\ \sqrt{1 - 4k} \overset{\text{ZBV}}{=} \sum_{k = 0}^{\infty} (-4)^k \binom{1/2}{k} x^k\\
	&= -\frac{1}{2} \sum_{k = 1}^{\infty} (-4)^k \binom{1/2}{k} x^{k - 1}\\
	&= -\frac{1}{2} \sum_{k = 1}^{\infty} (-4)^{n + 1} \binom{1/2}{n + 1}\\
	\\
	b_n &= \frac{1}{2} (-1)^{n} 2^{2n + 2} \frac{\frac{1}{2} \cdot \left(\frac{1}{2} - 1\right) \cdot \ldots \cdot \left(\frac{1}{2} - n\right)}{\left(n + 1\right)!}\\
	&= \frac{1}{2} (-1)^{n} 2^{2n + 2} \frac{\frac{1}{2} \cdot \left(-\frac{1}{2}\right) \cdot \ldots \cdot \left(-\frac{2n - 1}{2}\right)}{\left(n + 1\right)!}\\
	&= \frac{1}{2} 2^{2n + 2} \frac{\frac{1}{2} \cdot \frac{1}{2} \cdot \ldots \cdot \frac{2n - 1}{2}}{\left(n + 1\right)!} \qquad //\ \text{krácení záporných čísel}\\
	&= 2^{n} \frac{1 \cdot 3 \cdot 5 \cdot \ldots \cdot (2n - 1)}{(n + 1)!} \cdot \frac{n!}{n!} \qquad //\ \text{krácení $2$}\\
	&= \frac{1 \cdot 3 \cdot 5 \cdot \ldots \cdot (2n - 1)}{(n + 1) n!} \cdot \frac{2 \cdot 4 \cdot 6 \cdot \ldots \cdot 2n}{n!} \qquad //\ \text{rozdistribuování $2$}\\
	&= \frac{1}{n + 1} \frac{(2n)!}{\left(n!\right)^2} \\
	&= \frac{1}{n + 1} \binom{2n}{n} \\
\end{aligned}
{% endlatex %}

#### Konečné projektivní roviny

{:.rightFloatBox}
<div markdown="1">
- {% latex %}x \in X{% endlatex %} je bod
- {% latex %}P \in \mathcal{P}{% endlatex %} je přímka
</div>

**Definice (KPR):** Nechť {% latex %}X{% endlatex %} je konečná množina, {% latex %}\mathcal{P}{% endlatex %} systém podmnožin množiny {% latex %}X{% endlatex %}. {% latex %}\left(X, \mathcal{P}\right){% endlatex %} je KPR pokud:
1. Existuje {% latex %}Č \subseteq X, |Č| = 4{% endlatex %} t. ž. {% latex %}\forall P \in \mathcal{P}: |P \cap Č| \le 2{% endlatex %}
	- „každá přímka obsahuje {% latex %}\le 2{% endlatex %} body z {% latex %}Č{% endlatex %}“
2. {% latex %}\forall P, Q \in \mathcal{P}, P \neq Q: \exists! x \in X{% endlatex %} t. ž. {% latex %}P \cap Q = \left\{x\right\}{% endlatex %}
	- „každé dvě přímky se protínají právě v {% latex %}1{% endlatex %} bodě“
3. {% latex %}\forall x, y \in X, x \neq y \exists! P \in \mathcal{P}{% endlatex %} t. ž. {% latex %}x, y \in \mathcal{P}{% endlatex %}
	- „každé dva body určují právě {% latex %}1{% endlatex %} přímku“

**Příklad (Fanova rovina):**

{:.center}
![Fanova rovina.](/assets/kombinatorika-a-grafy-i/fanova-rovina.svg)

##### Počet bodů a přímek

**Tvrzení:** „v KPR mají všechny přímky stejný počet bodů“

**Pomocné tvrzení:** {% latex %}\exists z \in X{% endlatex %}, které neleží ani na jedné z nich. Dokáže se přes to přes rozbor příkladů toho, jak vedou přímky přes {% latex %}Č{% endlatex %}:
- pokud nevedou přes všechny body z {% latex %}Č{% endlatex %}, pak máme vyhráno
- pokud vedou, tak existují dvě další přímky {% latex %}P_1{% endlatex %} a {% latex %}P_2{% endlatex %} vedoucí kolmo na naše přímky, jejich průnik je hledaný bod; původní přímky jím vést nemohou, protože pak by dvě přímky sdílely 2 body, což nelze

### 4. přednáška

**Důkaz původního tvrzení:** pro přímky {% latex %}P{% endlatex %}, {% latex %}P'{% endlatex %} a bod {% latex %}z{% endlatex %} (který nesdílí) budeme dělat bijekci tak, že budu tvořit přímky z bodu {% latex %}z{% endlatex %} na body z {% latex %}P{% endlatex %}, které budou rovněž protínat body z {% latex %}P'{% endlatex %}.

**Definice (řád KPR):** řádem {% latex %}(X, \mathcal{P}){% endlatex %} je {% latex %}h = |P| - 1{% endlatex %} pro jakoukoliv {% latex %}P \in \mathcal{P}{% endlatex %}

**Tvrzení:** nechť {% latex %}(X, \mathcal{P}){% endlatex %} je KPR řádu {% latex %}n{% endlatex %}. Pak:
1. každým bodem prochází {% latex %}n + 1{% endlatex %} přímek 
	- triviálně z definice
2. {% latex %}|X| = n^2 + n + 1{% endlatex %}
3. {% latex %}|\mathcal{P}| = n^2 + n + 1{% endlatex %}
	- přes dualitu později


**Důkaz:** vezměme libovolné {% latex %}x \in X{% endlatex %}.

**Pomocné tvrzení:** {% latex %}\exists P \in \mathcal{P}: x \not\in P{% endlatex %}
- důkaz přes {% latex %}a, b, c \in Č{% endlatex %}, protože přímka {% latex %}ab{% endlatex %} a {% latex %}ac{% endlatex %} nemohou mít další společný bod než {% latex %}a{% endlatex %} (došlo by ke sporu s některým z axiomů)

Poté stačí uvážit následující obrázek a spočítat body/přímky. Další body už neexistují, protože kdyby existoval, tak by jím musela procházet přímka z {% latex %}x{% endlatex %} a ta by rovněž někde protínala {% latex %}P{% endlatex %} (a nesplňovala tak axiomy.

{% xopp primky-v-kpr %}

Bodů na obrázku je {% latex %}\overbrace{1}^{x} + \underbrace{\left(n + 1\right)}_{P_0 \ldots P_n}\overbrace{n}^{\text{body $P_i$, bez $x$}} = n^2 + n + 1{% endlatex %}

#### Dualita KPR

**Definice:** {% latex %}(X, \mathcal{S}){% endlatex %} je množinový systém, jeho incidenční graf je bipartitní graf s {% latex %}V = X \cup \mathcal{S}{% endlatex %}, {% latex %}E = \left\{(X, S) \in X \times \mathcal{S}\ |\ x \in S\right\}{% endlatex %}.

**Definice:** {% latex %}(Y, \mathcal{T}){% endlatex %} je duál {% latex %}(X, \mathcal{S}){% endlatex %} pokud {% latex %}Y = \mathcal{S}{% endlatex %} a {% latex %}\mathcal{T} = \left\{\left\{s \in \mathcal{S}\ |\ x \in s\right\}\ |\ x \in X\right\}{% endlatex %}
- (👀) incidenční graf {% latex %}(Y, \mathcal{T}){% endlatex %} je incidenční graf {% latex %}(X, \mathcal{S}){% endlatex %} s prohozením stran

**Příklad (duál Fanovy roviny):**

{:.center}
![Duál Fanovy roviny.](/assets/kombinatorika-a-grafy-i/dual-fanovy-roviny.svg)

**Tvrzení:** duál KPR je KPR.

{:.rightFloatBox}
<div markdown="1">
1. „každá přímka obsahuje {% latex %}\le 2{% endlatex %} body z {% latex %}Č{% endlatex %}“
2. „každé dvě přímky se protínají právě v {% latex %}1{% endlatex %} bodě“
3. „každé dva body určují právě {% latex %}1{% endlatex %} přímku“
</div>

**Důkaz:** ověření axiomů v duálním světě:
1. {% latex %}\exists Č{% endlatex %} čtveřice přímek t. ž. {% latex %}\forall x \in X{% endlatex %} leží na nanejvýš {% latex %}2{% endlatex %} přímkách z {% latex %}Č{% endlatex %}
	- stejné jako „žádné {% latex %}3{% endlatex %} přímky z {% latex %}Č{% endlatex %} nemají společný bod“
	- zvolím {% latex %}Č = \left\{ab, cd, ad, bc\right\}{% endlatex %}, což funguje (zkusit si rozkreslit)
2. {% latex %}\forall x, y \in X, x \neq y: \exists! P \in \mathcal{P}{% endlatex %} t. ž. jimi prochází právě {% latex %}1{% endlatex %} přímka
	- stejné jako původní axiom o přímkách
3. analogicky viz. ^

**Důsledek:** {% latex %}(X, \mathcal{P}){% endlatex %} je řádu {% latex %}n \implies |X| = n^2 + n + 1{% endlatex %}
- duál {% latex %}(Y, \mathcal{T}){% endlatex %} je duál {% latex %}(X, \mathcal{P}){% endlatex %}, ten je stejného řádu a proto je i velikost {% latex %}|\mathcal{P}| = n^2 + n + 1{% endlatex %}

#### Konstrukce KPR

Pro KPR řádu {% latex %}p^k{% endlatex %}, {% latex %}p{% endlatex %} prvočíslo vezmu algebraické těleso {% latex %}\mathbb{K}{% endlatex %} řádu {% latex %}n{% endlatex %} (příklad {% latex %}\mathbb{K} = \mathbb{Z}_3{% endlatex %}.
- {% latex %}T = \mathbb{K}^3 \setminus \left(0, 0, 0\right){% endlatex %}
- na {% latex %}T{% endlatex %} zavedu ekvivalenci {% latex %}(x, y, t) \in T{% endlatex %} je ekvivalentní s {% latex %}(\lambda x, \lambda y, \lambda t), \forall \lambda \in \mathbb{K} \setminus {0}{% endlatex %}
- {% latex %}X{% endlatex %} jsou ekvivalenční třídy nad {% latex %}T{% endlatex %}.
- reprezentanti: poslední nenulová složka je {% latex %}1{% endlatex %}
	- trojice tvaru {% latex %}(x, y, 1), (x, 1, 0), (1, 0, 0){% endlatex %}
	- počet je {% latex %}n^2 + n + 1{% endlatex %}, což sedí
- {% latex %}\mathcal{P}{% endlatex %}: pro každou {% latex %}(a, b, c) \in T{% endlatex %} definujeme přímku {% latex %}P_{a, b, c}{% endlatex %} jako množinu bodů {% latex %}(x, y, t){% endlatex %} splňující {% latex %}ax + by + ct = 0{% endlatex %}
	- {% latex %}\forall (x, y, t) \in T, \forall \lambda \neq 0: (x, y, t){% endlatex %} splňuje {% latex %}\iff (\lambda x, \lambda y, \lambda t{% endlatex %} splňuje
	- {% latex %}\forall (a, b, c) \in T, \forall \lambda{% endlatex %} fixuji {% latex %}(x, y, t) \in T: ax + by + ct = 0 \iff \lambda ax + \lambda by + \lambda ct = 0 \implies{% endlatex %} přímky {% latex %}P_{a, b, c} = P_{\lambda a, \lambda b, \lambda c} \implies |\mathcal{P}| = |X|{% endlatex %} a mohu si opět zvolit reprezentanty

{:.rightFloatBox}
<div markdown="1">
1. „každá přímka obsahuje {% latex %}\le 2{% endlatex %} body z {% latex %}Č{% endlatex %}“
2. „každé dvě přímky se protínají právě v {% latex %}1{% endlatex %} bodě“
3. „každé dva body určují právě {% latex %}1{% endlatex %} přímku“
</div>

**Ověření axiomů:**
1. {% latex %}Č = \left\{(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)\right\}{% endlatex %}
	- jsou po třech lineárně nezávislé, proto tohle platí
2. dvojice přímek {% latex %}(a_1, b_1, c_1){% endlatex %} a {% latex %}(a_2, b_2, c_2){% endlatex %} určují jeden bod:
	- jsou lineárně nezávislé a dimenze jádra následující matice je tedy {% latex %}1{% endlatex %}:
{% latex display %} \begin{pmatrix} a_1 & b_1 & c_1 \\ a_2 & b_2 & c_2 \end{pmatrix} \begin{pmatrix} x \\ y \\ t \end{pmatrix} = 0 {% endlatex %}
3. analogické, protože role {% latex %}(x, y, t){% endlatex %} a {% latex %}(a, b, c){% endlatex %} je identická

### 5. přednáška

#### Latinské čtverce

**Definice (latinský čtverec)** řádu {% latex %}n{% endlatex %} je tabulka {% latex %}n \times n{% endlatex %} vyplněná čísly {% latex %}[n]{% endlatex %}, kde v žádném řádku či sloupci se symboly neopakují.

**Definice (ortogonalita)**: LČ {% latex %}A, B{% endlatex %} jsou ortogonální, pokud pro každou dvojici symbolů {% latex %}a, b \in [n]{% endlatex %} existují indexy {% latex %}i, j \in [n]{% endlatex %} t. ž. {% latex %}(A)_{i, j} = a, (B)_{i, j} = b{% endlatex %}.
- když přeložím čtverce přes sebe, najdu políčko {% latex %}(i, j){% endlatex %} obsahující dvojici {% latex %}(a, b){% endlatex %}
- (👀) počet dvojic symbolů {% latex %}n^2 = {% endlatex %} počtu políček
	- zobrazení je bijekce
	- {% latex %}\forall (a, b){% endlatex %} se objeví v OLČ právě jednou
- (👀) {% latex %}A{% endlatex %} je LČ {% latex %}\implies{% endlatex %} po následujících operacích je stále:
	- permutace symbolů
	- permutace sloupců/řádků
- (👀) {% latex %}A, B{% endlatex %} jsou NOLČ {% latex %}\implies{% endlatex %} pokud dělám operace z předchozího pozorování v obou čtvercích, tak ortogonalitu zachovávám, jinak nutně ne

**Příklad** dvou navzájem ortogonálních latinských čtverců stupně {% latex %}n{% endlatex %}:

{% latex display %}
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
{% endlatex %}

**Lemma:** pro daný řád {% latex %}n{% endlatex %} může existovat nejvýše {% latex %}n - 1{% endlatex %} NOLČ.

**Důkaz:** mějme maximální rodinu NOLČ {% latex %}L_1, \ldots, L_m{% endlatex %}. Permutuji symboly tak, aby každý první řádek byl {% latex %}1, 2, 3, \ldots, n{% endlatex %}. Uvažme políčko {% latex %}(2, 1){% endlatex %} -- jaké může obsahovat hodnoty?
- ne {% latex %}1{% endlatex %}, ta je na {% latex %}(1, 1){% endlatex %}
- ne nějaké {% latex %}k \in \left\{2, \ldots, n\right\}{% endlatex %} ve dvou čtvercích zároveň

Čtverců je dohromady tedy nejvýše {% latex %}n - 1{% endlatex %}.

**Tvrzení:** pokud {% latex %}L_1, \ldots, L_{n - 1}{% endlatex %} jsou NOLČ, potom {% latex %}\forall k, k', k \neq k', \forall l, l', l \neq l' \exists i: \left(L_i\right)_{k, l} = \left(L_i\right)_{k', l'}{% endlatex %}

**Důkaz:** zpermutujeme symboly tak, aby {% latex %}\forall i \left(L_i\right)_{k, l} = 1{% endlatex %}:

{% latex display %}
\underbrace{\begin{bmatrix} &   &   &   \\ & (1) &   &   \\ &   &   &   \\ &   & ? &   \end{bmatrix}
			\qquad
			\begin{bmatrix} &   &   &   \\ & (1) &   &   \\ &   &   &   \\ &   & ? &   \end{bmatrix}
			\qquad
			\ldots
			\qquad
			\begin{bmatrix} &   &   &   \\ & (1) &   &   \\ &   &   &   \\ &   & ? &   \end{bmatrix}}_{n - 1}
{% endlatex %}

Kde ve sloupci s otazníkem je {% latex %}1{% endlatex %}:
- ne v řádku s {% latex %}(1){% endlatex %}
- ne ve dvou čtvercích na stejném místě

Mám tedy {% latex %}n - 1{% endlatex %} možností a musím přijít na {% latex %}n - 1{% endlatex %} různých řešení. Jedno z nich tedy vyjde na {% latex %}?{% endlatex %}.

#### NOLČ {% latex %}\iff{% endlatex %} KPR

**Věta:** {% latex %}\exists L_1, \ldots, L_{n - 1}{% endlatex %} NOLČ {% latex %}\iff \exists KPR{% endlatex %} řádu {% latex %}n{% endlatex %}.

**Důkaz:** konstrukce {% latex %}\Rightarrow{% endlatex %}
- dány čtverce {% latex %}\exists L_1, \ldots, L_{n - 1}{% endlatex %}
- body: {% latex %}r, s, l_1, l_{n - 1}, m_{1, 1}, m_{1, 2}, \ldots, m_{1, n}, \ldots, m_{n, n}{% endlatex %}
- přímky:
	- {% latex %}\mathrm{I}: \left\{r, s, l_1, \ldots, l_n - 1\right\}{% endlatex %}
	- {% latex %}\mathrm{II}:{% endlatex %} řádky -- {% latex %}\forall i \in [n]: \left\{r, m_{i, 1}, m_{i, 2}, \ldots, m_{i, n}\right\}{% endlatex %}
	- {% latex %}\mathrm{III}:{% endlatex %} sloupce -- {% latex %}\forall i \in [n]: \left\{r, m_{1, i}, m_{2, i}, \ldots, m_{n, i}\right\}{% endlatex %}
	- {% latex %}\mathrm{IV}: \underbrace{\forall i \in [n]}_{\text{latinské čtverce}}, \underbrace{\forall j \in [n]}_{\text{symboly}}: \left\{l_i\right\} \cup \left\{m_{k, l}\ \mid\ \left(L_i\right)_{k, l} = j\right\}{% endlatex %}

{:.center}
![Latinský čtverec na KPR.](/assets/kombinatorika-a-grafy-i/kpr-to-lat.svg)

{:.rightFloatBox}
<div markdown="1">
1. „každá přímka obsahuje {% latex %}\le 2{% endlatex %} body z {% latex %}Č{% endlatex %}“
2. „každé dvě přímky se protínají právě v {% latex %}1{% endlatex %} bodě“
3. „každé dva body určují právě {% latex %}1{% endlatex %} přímku“
</div>

**Ověření axiomů:**
1. {% latex %}Č = \left\{r, s, m_{1, 1}, m_{2, 2}\right\}{% endlatex %}
2. mezi:
	- {% latex %}r, s, l_i \rightarrow \mathrm{I}{% endlatex %} 
	- {% latex %}r, m_{k, l} \rightarrow \mathrm{II}{% endlatex %} 
	- {% latex %}s, m_{k, l} \rightarrow \mathrm{III}{% endlatex %} 
	- {% latex %}l_{i}, m_{k, l} \rightarrow \mathrm{IV}{% endlatex %}, symbol {% latex %}\left(L_i\right)_{k, l}{% endlatex %} určuje, o kterou přímku z {% latex %}l_i{% endlatex %} jde
	- {% latex %}m_{k, l}, m_{k', l'} \rightarrow{% endlatex %}
		- stejný řádek: {% latex %}\mathrm{II}{% endlatex %}
		- stejný sloupec: {% latex %}\mathrm{III}{% endlatex %}
		- jinak: {% latex %}\mathrm{IV}{% endlatex %} a existuje, vycházíme z minulého pozorování
3. mezi:
	- {% latex %}I, II \rightarrow r{% endlatex %}
	- {% latex %}I, III \rightarrow s{% endlatex %}
	- {% latex %}I, IV \rightarrow l_i{% endlatex %}
	- {% latex %}II, II \rightarrow r{% endlatex %}
	- {% latex %}III, III \rightarrow s{% endlatex %}
	- {% latex %}II, III \rightarrow m_{k, l}{% endlatex %}
	- {% latex %}II, IV \rightarrow {% endlatex %} čtverec je latinský, na řádku se symbol někde vyskytuje
	- {% latex %}III, IV \rightarrow {% endlatex %} obdobně ^
	- {% latex %}IV, IV \rightarrow {% endlatex %} 
		- různé čtverce: přesně definice ortogonality (existuje dvojice souřadnic pro dvojici symbolů)
		- stejné čtverce: {% latex %}l_i{% endlatex %}

**Důkaz:** konstrukce {% latex %}\Leftarrow{% endlatex %}
- dána KPR {% latex %}(X, \mathcal{P}){% endlatex %}, hledáme {% latex %}L_1, \ldots, L_{n - 1}{% endlatex %}
	1. zvolíme libovolně přímku - označíme {% latex %}\mathrm{I}{% endlatex %} a její body {% latex %}\left\{r, s, l_1, \ldots, l_{n - 1}\right\}{% endlatex %}
	2. {% latex %}\exists n{% endlatex %} přímek protínající {% latex %}r{% endlatex %} -- typ {% latex %}\mathrm{II}{% endlatex %} a opět oindexuji body
	3. analogicky ^, typ {% latex %}\mathrm{III}{% endlatex %}, průsečíky jsou {% latex %}m_{k, l}{% endlatex %}
	4. pro bod {% latex %}l_i{% endlatex %} oindexuj přímky {% latex %}Q_1, \ldots, Q_n{% endlatex %}; čtverec {% latex %}L_i{% endlatex %} má {% latex %}1{% endlatex %} na indexech {% latex %}Q_1{% endlatex %}, {% latex %}2{% endlatex %} na {% latex %}Q_2{% endlatex %}, {% latex %}\ldots{% endlatex %}

Jsou NOLČ, protože:
- průsečíky {% latex %}\mathrm{IV}{% endlatex %} s {% latex %}\mathrm{II}, \mathrm{III}{% endlatex %} jsou jednoznačné {% latex %}\implies{% endlatex %} čtverce jsou latinské
- jednoznačnost průniku dvou přímek typu {% latex %}\mathrm{IV}{% endlatex %} -- dvě různé přímky typu {% latex %}\mathrm{IV}{% endlatex %} odpovídající dvěma různým čtvercům dávají souřadnici, kde se má dvojice symbolů nachází {% latex %}\implies{% endlatex %} ortogonalita

{:.center}
![KPR na latinský čtverec.](/assets/kombinatorika-a-grafy-i/lat-to-kpr.svg)

### 6. přednáška

#### Počítání dvěma způsoby

**Tvrzení:** počet podmnožin {% latex %}X = \left| \binom{X}{k}\right| = \binom{|X|}{k}{% endlatex %}

**Důkaz:** nechť máme bublinu s tečkami, každá reprezentuje uspořádanou {% latex %}k{% endlatex %}-tici prvků z {% latex %}X{% endlatex %}.
- počet teček {% latex %}= n (n -1) (n-2) \ldots (n - k + 1) = \frac{n!}{(n - k)!}{% endlatex %} (vyberu první prvek, druhý prvek,...)
- v každé buňce {% latex %}k{% endlatex %}-tic se stejnými prvky je {% latex %}k!{% endlatex %} prvků, počet buňek je to, co chceme (neuspořádaná {% latex %}k{% endlatex %}-tice)

{% latex display %}
\begin{aligned}
	\frac{n!}{(n - k)!} &= \left|\binom{X}{k}\right| \cdot k! \\
	\left|\binom{X}{k}\right|&=  \frac{n!}{(n - k)! k!} = \binom{n}{k} \\
\end{aligned}
{% endlatex %}

**Věta (Spernerova):** nechť {% latex %}(\mathcal{P}, \subseteq){% endlatex %} je částečné uspořádání, kde {% latex %}\mathcal{P}{% endlatex %} je množinový systém. Nechť {% latex %}\mathcal{M}{% endlatex %} je nevětši antiřetězec ({% latex %}\forall M_1, M_2 \in \mathcal{M}, M_1 \neq M_2: M_1 \subsetneq M_2 \land M_2 \subsetneq M_1{% endlatex %}). Pak {% latex %}|\mathcal{M}| \le \binom{n}{\left\lceil \frac{n}{2} \right\rceil}{% endlatex %}, kde {% latex %}n = |X|{% endlatex %}.

{:.center}
![Sperenerova věta.](/assets/kombinatorika-a-grafy-i/spernerova-veta.svg)

**Pomocné tvrzení:** {% latex %}\sum_{M \in \mathcal{M}} \left|M\right|! (n - \left|M\right|)! \le n!{% endlatex %}. Přes dvojí počítání počtu permutací na {% latex %}X{% endlatex %}:
- počet permutací {% latex %}= n!{% endlatex %} (očividné)
- počet permutací {% latex %}\ge \sum_{M \in \mathcal{M}} |M|! (n - |M|)! {% endlatex %}, protože:
	- pro každé {% latex %}M{% endlatex %} dostanu jinou množinu permutaci
	- {% latex %}M{% endlatex %} určuje množinu permutací takovou, že nejprve permutuji {% latex %}M{% endlatex %}, potom {% latex %}X \setminus M{% endlatex %}:

{% xopp sperner %}

- {% latex %}\emptyset \subseteq \left\{x_1\right\} \subseteq \left\{x_1, x_2\right\} \subseteq \ldots \subseteq M \subseteq \ldots \subseteq X{% endlatex %}
	- zajímá nás, kolik různých řetězců obsahuje {% latex %}M{% endlatex %}
- (👀) každý maximální řetězec obsahuje {% latex %}\le 1 M \in \mathcal{M}{% endlatex %} 

**Důkaz (přes pomocné tvrzení):**
{% latex display %}
\begin{aligned}
	\sum_{M \in \mathcal{M}} |M!| (n - |M|)! &\le n! \\
	\sum \binom{n}{\left\lceil \frac{n}{2} \right\rceil}^{-1} \le \sum_{M \in \mathcal{M}} \frac{|M!| (n - |M|)!}{n!} &\le 1 \qquad //\ \text{používáme větší kombinační číslo} \\
	\left|\mathcal{M}\right| &\le \binom{n}{\left\lceil \frac{n}{2} \right\rceil}  \\
\end{aligned}
{% endlatex %}

#### Grafy bez {% latex %}C_k{% endlatex %}

**Motivace:**
- kolik nejvíce hran má {% latex %}G{% endlatex %}, když nemá {% latex %}C_k, \forall k{% endlatex %}?
	- je to strom, tedy {% latex %}n - 1{% endlatex %}
- kolik nejvíce hran má {% latex %}G{% endlatex %}, když nemá {% latex %}C_3{% endlatex %}?
	- {% latex %}\mathcal{O}(n^2){% endlatex %}, uvažme bipartitní graf

**Věta:** graf {% latex %}G{% endlatex %} s {% latex %}n{% endlatex %} vrcholy bez {% latex %}C_4{% endlatex %} má nejvýše {% latex %}\frac{1}{2} \left(n^{3/2} + n\right){% endlatex %} hran.

**Důkaz:** dvojí počítání „vidliček“ (cest delky {% latex %}2{% endlatex %}):
1. pro pevnou dvojici {% latex %}\left\{u, u'\right\}{% endlatex %} mám nanejvýš 1 vidličku (dvě by tvořily čtyřcyklus), tedy {% latex %}\#\ \text{vidliček}\ \le \binom{n}{2}{% endlatex %}
2. pro pevný vrchol {% latex %}v{% endlatex %} máme {% latex %}\#\ \text{vidliček}\ = \binom{d(v)}{2}{% endlatex %}

{% latex display %}
\begin{aligned}
	\#\ \text{vidliček}\ &= \sum_{v \in V} \binom{d(v)}{2} = \sum_{i = 1}^{n} \binom{d_i}{2} \le \binom{n}{2} \\
	|E| &= \frac{1}{2} \sum_{i = 1}^{n} d_i \qquad //\ \text{princip sudosti}
\end{aligned}
{% endlatex %}

Předpoklad: nemáme izolované vrcholy ({% latex %}d_i \ge 1{% endlatex %}), jsou zbytečné. Pak {% latex %}\binom{d_i}{2} \ge \frac{(d_i - 1)^2}{2}{% endlatex %}.

{% latex display %}
\frac{n^2}{2} \ge \binom{n}{2} \ge \sum_{i = 1}^{n} \binom{d_i}{2} \ge \sum \frac{(d_i - 1)^2}{2} = \sum \frac{k_i^2}{2} \qquad //\ \text{substituce} \\
\sum k_i^2 \le n^2
{% endlatex %}

Využijeme Cauchy-Schwartzovu nerovnost na {% latex %}x = (k_1, \ldots, k_n), y = (1, \ldots, 1){% endlatex %}:
{% latex display %}
xy = \sum k_i = \sum d_i - 1 = 2|E| - n \\
|| x ||_2 = \sqrt{\sum k_i^2} \le \sqrt{n^2} = n \qquad || y ||_2 = \sqrt{\sum 1} =  \sqrt{n}
{% endlatex %}

{% latex display %}
\begin{aligned}
	2|E| - n &= xy \le ||x||_2 ||y||_2 = n^{3/2} \\
	|E| &\le \frac{1}{2} \left(n^{3/2} + n\right)
\end{aligned}
{% endlatex %}

#### Počítání koster

**Věta (Cayleyho formule):** počet koster úplného grafu {% latex %}\Kappa(n) = n^{n - 2}{% endlatex %}.
- pozor, počítám i izomorfní kostry!

**Důkaz:** počítání {% latex %}(T, r, č){% endlatex %}, kde:
- {% latex %}T{% endlatex %} je strom na {% latex %}n{% endlatex %} vrcholech
- {% latex %}r{% endlatex %} kořen (hrany vedou **do, ne z!**)
- {% latex %}č{% endlatex %} očíslování hran (nějaké), {% latex %}č: E \mapsto [n - 1]{% endlatex %}

1. {% latex %}\#(T, r, č) = \Kappa(n) \cdot n \cdot \left(n - 1\right)!{% endlatex %}
	- {% latex %}T{% endlatex %} je to, co hledáme
	- {% latex %}r{% endlatex %} volíme libovolně
	- {% latex %}č{% endlatex %} je prostě random očíslovaní
2. představa: přidávám hrany, až nakonec dojdu k {% latex %}(T, r, č){% endlatex %} a jsem v {% latex %}k{% endlatex %}-tém kroce:
	- (👀) nesmím vést hranu uvnitř komponenty (cykly)
	- (👀) musím vést hranu pouze z kořene dané komponenty (jeden vrchol by měl 2 rodiče)

	1. zvolím, kam šipka povede... {% latex %}n{% endlatex %} způsobů
	2. zvolím komponentu, ze které povede... {% latex %}n - k - 1{% endlatex %}

{% latex display %}
\begin{aligned}
	\#(T, r, č) &= \prod_{k = 0}^{ \overbrace{n - 2}^{\text{počet šipek}}} n ( n - k - 1) = n^{n - 1} (n -1)! \\
	\Kappa(n) \cdot n \cdot \left(n - 1\right)! &= n^{n - 1} (n -1)! \\
	\Kappa(n) &= n^{n - 2}
\end{aligned}
{% endlatex %}

### 7. přednáška

#### Toky

**Definice (síť)** je čtveřice {% latex %}(G, z, s, c){% endlatex %}, kde:
- {% latex %}G{% endlatex %} je orientovaný graf, {% latex %}z, s \in V(G){% endlatex %}
- {% latex %}c: E \mapsto \mathbb{R}_{\ge 0}{% endlatex %}

**Definice (tok)** v síti je {% latex %}f: E \mapsto \mathbb{R}_{\ge 0}{% endlatex %}, t. ž.:
1. {% latex %}\forall e \in E(G){% endlatex %} platí {% latex %}0 \le f(e) \le c(e){% endlatex %}
2. {% latex %}\forall v \in V(G){% endlatex %}, v \not\in \left\{z, s\right\} platí {% latex %}\sum f(x, v) = f(v, y){% endlatex %}

**Definice (velikost toku)** {% latex %}w(f) = \sum f(z, x) - \sum f(x, z){% endlatex %} (to, co teče ze zdroje)

**Důkaz:** existuje maximální tok. Nástin je takový, že množina toků je kompaktní a obsahuje tedy i maximum (nevznikne nám tam nějaká divnost)

**Definice (řez)** v síti je množina hran {% latex %}R \subseteq E(G){% endlatex %} taková, že v grafu {% latex %}(V, E \setminus R){% endlatex %} neexistuje cesta ze zdroje do stoku.
- **kapacita** řezu je {% latex %}c(R) = \sum_{e \in R} c(e){% endlatex %}, analogicky tok
- {% latex %}S(A, B) = \left\{(x, y) \in E\ |\ x \in A, y \in B\right\}{% endlatex %}
	- neobsahuje hrany z {% latex %}B{% endlatex %} do {% latex %}A{% endlatex %}!
	- je to **elementární** řez (vezmu dvě množiny vrcholů a všechny hrany mezi nimi)
		- každý v inkluzi minimální ({% latex %}R \ {e}{% endlatex %} není řez) řez je elementární

##### min flow, max cut

**Věta (min flow, max cut):** pro každou síť je maximální tok roven minimálnímu řezu.

**Lemma:** pro každou {% latex %}A \subseteq V{% endlatex %} t. ž. {% latex %}z \in A, s \not\in A{% endlatex %} a pro libovolný tok {% latex %}f{% endlatex %} platí: {% latex display %}w(f) = f(A, V \setminus A) - f(V \setminus A, A){% endlatex %}

**Důkaz:**
{% latex display %}
\begin{aligned}
	w(f) &= \sum_{u \in A} \left(\sum_{(u, x \in E)} f(u, x) - \sum_{(x, u) \in E} f(x, u)\right) \qquad //\ \text{pouze definice} \\
	&= \sum_{u \in A, v \not\in A} f(u, v) - \sum_{u \not\in A, v \in A} f(v, u) \qquad //\ \text{hrany v a přispějí jednou $+$ a jednou $-$} \\
	&= f(A, V \setminus A) - f(V \setminus A, A) \\
\end{aligned}
{% endlatex %}

**Důsledek:** {% latex %}w(f) \le c(R){% endlatex %}, protože
{% latex display %}w(f) = f(A, V \setminus A) - f(V \setminus A, A) \le f(A, V \setminus A) \le c(A, V \setminus A) \le c(R){% endlatex %}

**Definice (nasycená cesta)** je cesta, pokud {% latex %}\exists e{% endlatex %} na cestě t. ž. buďto:
- vede po směru a {% latex %}f(e) = c(e){% endlatex %}
- vede proti směru a {% latex %}f(e) = 0{% endlatex %}

**Tvrzení:** {% latex %}f{% endlatex %} je maximální {% latex %}\iff f{% endlatex %} je nasycený.
- důkaz sporem, že {% latex %}f{% endlatex %} maximální je nasycený
- je-li {% latex %}f{% endlatex %} nasycený, tak uvážíme množinu vrcholů, do kterých se lze dostat ze {% latex %}z{% endlatex %} po nasycené cestě -- {% latex %}A = \left\{v \in V\ |\ \exists\ \text{nenasycená cesta }\right\}{% endlatex %}
	- {% latex %}s \subsetneq A{% endlatex %} (jinak {% latex %}f{% endlatex %} není nasycený)
	- {% latex %}\forall e \in S(A, V \setminus A){% endlatex %} platí {% latex %}f(e) = c(e){% endlatex %} a {% latex %}\forall e \ in S(V \setminus A, A){% endlatex %} platí {% latex %}f(e) = 0{% endlatex %} (jinak bychom nenasycenou cestu mohli prodloužit

{% latex display %}
\begin{aligned}
	w(f) &= f(A, V \setminus A) - f(V \setminus A, A) \qquad //\ \text{lemma}\\
	&= c(A, V \setminus A) - 0 \qquad //\ \text{teď jsme dokázali} \\
	&= c(A, V \setminus A)
\end{aligned}
{% endlatex %}

##### Ford-fulkerson
1. {% latex %}f(e) = 0, \forall e \in E{% endlatex %}
2. dokud {% latex %}\exists{% endlatex %} zlepšující cesta {% latex %}P{% endlatex %}, zlepši tok přes {% latex %}P{% endlatex %}

**Tvrzení:** pokud jsou kapacity racionální, pak algoritmus doběhne. Pokud jsou přirozené, dá celočíselný tok.
- racionální: pronásobení LCM a důkaz pro přirozené
- přirozené: každé vylepšení cesty bude celočíselné a udělá to konečněkrát

### 8. přednáška

#### Aplikace toků v sítích

**Věta (Königova):** v bipartitním grafu: velikost maximálního párování {% latex %}={% endlatex %} velikost minimalního vrcholového pokrytí.
- {% latex %}M \subseteq E{% endlatex %} je **párování**, pokud {% latex %}\forall e, e' \in M, e \neq e': e \cap e' = \emptyset{% endlatex %} 
- {% latex %}U \subseteq V{% endlatex %} je **vrcholové pokrytí**, pokud {% latex %}\forall e \in E \exists u \in U: u \in e{% endlatex %}

**Důkaz:** přes toky, jako na následujícím obrázku na síti kapacit {% latex %}1{% endlatex %}:

{:.center}
![Königova věta.](/assets/kombinatorika-a-grafy-i/konig.svg)

Z toku mám maximální párování {% latex %}M{% endlatex %} velikosti {% latex %}k{% endlatex %} (protože tok byl maximální). Z toho umím sestrojit minimální řez. Ukážeme dvě implikace:

{% latex %}W{% endlatex %} je minimální vrcholové pokrytí {% latex %}G{% endlatex %}, tak:
- {% latex %}L, P ={% endlatex %} levá a pravá část grafu (bez zdroje a stoku)
- {% latex %}R = \left\{(z, u)\ |\ u \in W \cap L\right\} \cup \left\{(u, s)\ |\ u \in W \cap P\right\} {% endlatex %}
	- je řez (pro spor by existovala cesta, kterou by {% latex %}W{% endlatex %} nepokryl)

{% latex %}R{% endlatex %} je minimální {% latex %}z-s{% endlatex %} řez. Ten upravíme na řez {% latex %}R'{% endlatex %}, aby neobsahoval hrany původního grafu. To jde, protože hranu původního grafu mohu vyměnit za tu ze zdroje/stoku, protože ta je jediný způsob, jak se dostat do hrany z původního vrcholu.
- {% latex %}W = \left\{u \in L\ |\ (z, u) \in R'\right\} \cup \left\{v \in P\ |\ (v, s) \in R'\right\}{% endlatex %}
	- je vrcholové pokrytí, protože stejný argument jako u obrácené implikace

**Definice:**
- **množinový systém** na množině {% latex %}X{% endlatex %} je {% latex %}(M_i)_{i \in I}, M_i \subseteq X{% endlatex %}
- **systém různých reprezentantů** je funkce {% latex %}f: I \mapsto X{% endlatex %} splňující:
	1. {% latex %}\forall i \in I: f(i) \in M_i{% endlatex %}
	2. {% latex %}f{% endlatex %} je prostá (jeden prvek {% latex %}x \in X{% endlatex %} není reprezentantem dvou {% latex %}M{% endlatex %})


{:.rightFloatBox}
<div markdown="1">
Analogicky pro grafy: bipartitní graf {% latex %}G = (L \cup P, E){% endlatex %} má párování pokrývající {% latex %}P{% endlatex %} pokud {% latex %}\forall P' \subseteq P: \left|\bigcup_{v \in P'} N(v)\right| \ge |P'|{% endlatex %}. {% latex %}N{% endlatex %} je sousedství (to, co vrcholy zprava na levé straně „vidí“).
</div>
**Hallova věta:** SRR existuje {% latex %}\iff \forall J \subseteq I: \left|\bigcup_{i \in J} M_i\right| \ge |J|{% endlatex %}.

**Důkaz (SSR {% latex %}\Rightarrow{% endlatex %} Hall):** zvolím libovolnou {% latex %}J \subseteq I{% endlatex %}. {% latex %}\forall j \in J \exists p_j \in M_j, p_j = f(j){% endlatex %}, tak že prvky {% latex %}p_j{% endlatex %} jsou navzájem různé ({% latex %}f{% endlatex %} je prostá).
{% latex display %}|J| = \left|\left\{p_j\ |\ j \in J\right\}\right| \le |\bigcup_{j \in J} M_j|{% endlatex %}

**Důkaz (Hall {% latex %}\Leftarrow{% endlatex %} SSR):** opět najdu v grafu (celočíselný, jednotková síť) maximální tok. Najdu minimální řez z hran pouze ze zdroje/do stoku, {% latex %}|R| = |R'|{% endlatex %}. Uvážím následující obrázek:

{% xopp hall %}

- {% latex %}A = {% endlatex %} vrcholy incidentní s {% latex %}R'{% endlatex %} v {% latex %}I{% endlatex %}
- {% latex %}B = {% endlatex %} vrcholy incidentní s {% latex %}R'{% endlatex %} v {% latex %}X{% endlatex %}
- {% latex %}J = I \setminus A{% endlatex %}

Chceme najít systém různých reprezentantů. Dokážeme to tak, že {% latex %}|R'| = |I|{% endlatex %}, pak max. tok má velikost {% latex %}|I|{% endlatex %} a hrany s tokem {% latex %}1{% endlatex %} mi dají SRR.

(👀) hrany z {% latex %}J{% endlatex %} vedou pouze do {% latex %}B{% endlatex %}, protože jinak by existovala {% latex %}z-s{% endlatex %} cesta a nejednalo by se o řez, tedy {% latex %}\left|\bigcup_{j \in J} M_j\right| \subseteq B{% endlatex %}.

{% latex display %}
\begin{aligned}
	|R'| &= c(R') &&//\ \text{jednotkové kapacity}\\
	&= |A| + |B| \\
	&= \overbrace{|I| - |J|}^{|A|} + |B| \\
	&\ge |I| - |J| + \left|\bigcup_{j \in J} M_j\right| &&//\ \text{z pozorování}\\
	&\ge |I| - |J| + \left|J\right| &&//\ \text{z Hallovy podmínky}\\
	&= |I| &&// \implies\ \text{tok má velikost alespoň $|I|$} \\
\end{aligned}
{% endlatex %}

Definuji SRR jako {% latex %}f(i) = x \in X{% endlatex %}, pokud po hraně {% latex %}(i, x){% endlatex %} něco teče.

### 9. přednáška

**Důsledek:** nechť {% latex %}B = (V_1 \cup V_2, E){% endlatex %} je bipartitní graf, kde {% latex %}k_1 = \mathrm{min}\ \underset{v \in V_1}{\mathrm{deg}}\ v, k_2 = \mathrm{max}\ \underset{v \in V_2}{\mathrm{deg}}\ v {% endlatex %} a {% latex %}k_1 \ge k_2{% endlatex %}, pak je splněna Hallova podmínka.

**Důkaz:** Ověřím Hallovu podmínku (pozor, prohozené strany). Máme-li množinu {% latex %}J{% endlatex %} a každá vidí alespoň {% latex %}k_1{% endlatex %} hran, pak vidím {% latex %}\ge |J| k_1{% endlatex %} hran. Abych pohltil všechny tyto hrany, tak musí mapravo být alespoň {% latex %}k_2 |N[j]|{% endlatex %} vrcholů. Musí tedy platit:
{% latex display %}|J| k_1 \le \#\ \text{hran} \le k_2 |N[J]|{% endlatex %}

Protože {% latex %}k_1 \ge k_2{% endlatex %}, pak {% latex %}|N[j]| \ge |J|{% endlatex %}.

**Aplikace:** doplňování latinských obdélníků:

{:.center}
![Latinský obdelník.](/assets/kombinatorika-a-grafy-i/lat-rect.svg)

- stupně: každý sloupec má stupeň {% latex %}n - k{% endlatex %} (počet nepoužitých symbolů)
- symboly: každý symbol se vyskytuje v řádku právě jednou, tedy ještě není v {% latex %}n - k{% endlatex %} sloupcích

Máme tedy {% latex %}n - k{% endlatex %}-regulární graf, pro který {% latex %}\exists{% endlatex %} perfektní párování (použití minulého důsledku).

#### Míra souvislosti neorientovaných grafu

**Definice**
- **hranový řez** v grafu {% latex %}G{% endlatex %} je {% latex %}F \subseteq E{% endlatex %} t. ž. {% latex %}G' = (V, E \setminus F){% endlatex %} je nesouvislý.
- **vrcholový řez** v grafu {% latex %}G{% endlatex %} je {% latex %}A \subseteq V{% endlatex %} t. ž. {% latex %}G' = (V \setminus A, E \cap \binom{V \setminus A}{2}) = G\left[V \setminus A\right]{% endlatex %} je nesouvislý.
- **hranová souvislost** {% latex %}k_e(G) = \mathrm{min} \left\{|F|\ |\ F \subseteq E \text{ je hranový řez}\right\}{% endlatex %}
- **vrcholová souvislost** {% latex %}k_v(G) = \begin{cases}n - 1 & G \cong K_n \\ \mathrm{min} \left\{|A|\ |\ A \subseteq V \text{ je vrcholový řez}\right\} & \text{jindy} \end{cases}{% endlatex %}
- {% latex %}G{% endlatex %} je **hranově/vrcholově {% latex %}k{% endlatex %}-souvislý**, pokud {% latex %}k_{e/v}(G) \ge k{% endlatex %}
	- (👀) je-li {% latex %}3{% endlatex %}-souvislý, pak je i {% latex %}2{% endlatex %}-souvislý a {% latex %}1{% endlatex %}-souvislý
	- je **kriticky {% latex %}k{% endlatex %}-souvislý**, pokud odstranění libovolného vrcholu sníží stupeň souvislosti
		- stromy jsou hranově {% latex %}1{% endlatex %}-souvislé, vrcholově ne (co listy?)

**Lemma:** {% latex %}\forall G, \forall e \in E{% endlatex %} platí {% latex %}k_e(G) - 1 \le k_e(G - e) \le k_e(G){% endlatex %}
- zas tak triviální to není, u vrcholové může vzrůst (např. odstranění listu z kružnice)
- lemma říká, že se hranová chová slušně

**Důkaz:** vezmu minimální řez {% latex %}F \subseteq E, F' = F \setminus \left\{e\right\}{% endlatex %} jistě musí být řez v {% latex %}G - e{% endlatex %} (ne nutně minimální), pak:
{% latex display %}k_e(G - e) \le |F'| \le |F| = k_e(G){% endlatex %}

Co se druhé nerovnosti týče, vezmu min. řez {% latex %}B{% endlatex %} v {% latex %}G - e{% endlatex %}. Podobnou úvahou {% latex %}B' = B \cup \left\{e\right\}{% endlatex %} je řezem v {% latex %}G{% endlatex %}, pak:
{% latex display %}k_e(G) \le |B'| = |B| + 1 = k_e(G - e) + 1{% endlatex %}

**Lemma:** {% latex %}\forall G, \forall e \in E{% endlatex %} platí {% latex %}k_v(G) - 1 \le k_v(G - e) \le k_v(G){% endlatex %}

**Důkaz:** trochu přeformulujeme... pro {% latex %}H = G - e: k_v (H + e) \le k_v (H) + 1{% endlatex %}:

{:.rightFloatBox}
<div markdown="1">
Přidáváme hranu a sledujeme, co to dělá se souvislostí.
</div>

V {% latex %}H{% endlatex %} existuje vrcholový řez {% latex %}A \subseteq V(H){% endlatex %} t. ž. {% latex %}k_v(H) = |A|{% endlatex %}. Při odebrání {% latex %}A{% endlatex %} se {% latex %}H{% endlatex %} rozpadne na alespoň {% latex %}2{% endlatex %} komponenty:
1. alespoň {% latex %}1{% endlatex %} konec {% latex %}e{% endlatex %} leží v {% latex %}A{% endlatex %}:
	- přidání {% latex %}e{% endlatex %} nespojí žádné {% latex %}2{% endlatex %} komponenty, {% latex %}A{% endlatex %} je řezem i pro {% latex %}G = H + e{% endlatex %}
2. oba konce leží v {% latex %}1{% endlatex %} komponentě
	- stejný argument jako (1)
3. hrana {% latex %}e{% endlatex %} spojuje {% latex %}2{% endlatex %} komponenty
	- pokud je počet komponent {% latex %}\ge 3{% endlatex %}, tak je {% latex %}A{% endlatex %} stále řezem (po spojení jsou stále {% latex %}2{% endlatex %})
	- pokud není, tak:
		- {% latex %}|C_1| \ge 2{% endlatex %}; nechť {% latex %}e = xy{% endlatex %} a {% latex %}x{% endlatex %} leží v {% latex %}C_1{% endlatex %}, pak {% latex %}A \cup {x}{% endlatex %} je řezem, protože mi v obou komponentách něco zbylo
		- {% latex %}|C_1| = |C_2| = 1{% endlatex %}:
			- {% latex %}|V| = |A| + 2 \implies |A| = |V| - 2 = k_v(H){% endlatex %}
			- {% latex %}k_v(H + e) \le |V| - 1 = |V| - 2 + 1 = k_v(H) + 1{% endlatex %}

**Věta:** {% latex %}k_v(G) \le k_e(G){% endlatex %}: indukcí podle počtu hran:
- pokud {% latex %}|E| < |V| - 1{% endlatex %}, pak je {% latex %}G{% endlatex %} nesouvislý a {% latex %}k_v(G) = 0 = k_e(G){% endlatex %}
- nechť nadále {% latex %}k_e(G) > 0{% endlatex %}; vezmu min. hranový řez {% latex %}F \subseteq E{% endlatex %} a {% latex %}c \in F{% endlatex %}... {% latex %}G' = G - e{% endlatex %}
	- na {% latex %}G'{% endlatex %} použiju IP, tedy {% latex %}k_v(G') \le k_e(G'){% endlatex %}
	- z pomocných lemmat dostávám zbytek:
{% latex display %}k_v(G) - 1 \overset{\text{lemma o vrcholech}}{\le} k_v(G - e) \overset{\mathrm{IP}}{\le} k_e(G - e) \overset{F' = F \ \left\{e\right\}\text{ je řezem } G - e}{=} k_e(G) - 1{% endlatex %}

**Věta (Ford-Fulkerson):** {% latex %}\forall G{% endlatex %}, pokud {% latex %}k_e(G) \ge t{% endlatex %}, pak {% latex %}\forall u, v
{% endlatex %} mezi {% latex %}u, v \exists \ge t{% endlatex %} hranově disjunktních cest

**Důkaz ({% latex %}\Leftarrow{% endlatex %}):** sporem nechť existuje hranový řez {% latex %}F{% endlatex %} a {% latex %}|F| < t{% endlatex %}. {% latex %}G \setminus F{% endlatex %} je rozdělený na více komponent. Vezmi {% latex %}u \in C_1, v \in C_2{% endlatex %}. Mezi {% latex %}u, v{% endlatex %} vedlo {% latex %}t{% endlatex %} hranově disjunktních cest. {% latex %}F{% endlatex %} nemohl přerušit všechny z nich.

{:.rightFloatBox}
<div markdown="1">
- oboustraně zorientuji hrany
- nastavím kapacity na {% latex %}1{% endlatex %}
- vynuluji {% latex %}a \overset{1}{\underset{1}{\longleftrightarrow}} b{% endlatex %}
	- každou hranu využíváme {% latex %}1{% endlatex %}!
</div>

**Důkaz ({% latex %}\Rightarrow{% endlatex %}):** mějme {% latex %}k_e(G) \ge t{% endlatex %} a pro {% latex %}u, v{% endlatex %} hledám disjunktní cesty. Sestrojím jednotkovou síť, najdu tok z {% latex %}u{% endlatex %} do {% latex %}v{% endlatex %}. Pak vidím, že mám tok alespoň {% latex %}t{% endlatex %} (maximální tok je minimální řez) a začnu odčítat cesty.

**Věta (Mengerova):** {% latex %}k_v(G) \ge T \iff \forall u, v \in V \exists t{% endlatex %} vrcholově disjunktních cest

**Důkaz:** obdobný, jen rozpojíme každý vrchol na dva ({% latex %}\mathrm{deg}_{\mathrm{in}}, \mathrm{deg}_{\mathrm{out}}{% endlatex %})
- najdu max. celočíselny tok {% latex %}f{% endlatex %}
- chci min. řez {% latex %}R'{% endlatex %} takový, že obsahuje pouze pomocné hrany
	- vezmu řez {% latex %}R{% endlatex %} odpovídající {% latex %}F{% endlatex %} a vždy je posunu tak, aby podmínka platila

TODO: ještě doplnit na 10 přednášce

### Zdroje
- [https://research.koutecky.name/db/teaching:kg12021_prednaska]() -- stránka cvičení
	- odkaz na všechny obrázky, zdroje, nahrávky cvičení

