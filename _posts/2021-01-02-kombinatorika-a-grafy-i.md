---
language: cz
title: Kombinatorika a Grafy I
category: "lecture notes"
---

- .
{:toc}

### Úvodní informace
Tato stránka obsahuje moje poznámky z přednášky Martina Kouteckého z roku 2020/2021. Pokud by byla někde chyba/nejasnost, nebo byste rádi někam přidali obrázek/text, tak stránku můžete upravit [pull requestem](https://github.com/xiaoxiae/slama.dev/blob/master/_posts/) (případně mi dejte vědět, např. na mail).

### 1. přednáška

#### Odhady faktoriálu

**Věta (meh odhad):**
{% latex display %}n^{n/2} \le n! \le \left(\frac{n + 1}{2}\right)^n{% endlatex %}

**Důkaz {% latex %}\ge{% endlatex %}:**
{% latex display %}
\begin{aligned}
	\left(n!\right)^2 &= 1 \cdot 2 \cdot 3 \cdot \ldots \cdot n \cdot n \cdot (n - 1) \cdot \ldots \cdot 2 \cdot 1 \\
	&= \prod_{i = 1}^{n} \left(i \cdot (n - i + 1)\right)
\end{aligned}
{% endlatex %}

Využijeme A-G nerovnost:

{% latex display %}
\begin{aligned}
	\sqrt{ab} &\le \frac{a + b}{2} \\
	\sqrt{i (n + 1 - i)} &\le \frac{i + n + 1 - i}{2} = \frac{n + 1}{2}
\end{aligned}
{% endlatex %}

Dostáváme:
{% latex display %}n! = \prod_{i = 1}^{n} \sqrt{i \cdot (n - i + 1)}\le \left(\frac{n + 1}{2}\right)^n{% endlatex %}

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
- {% latex %}n = 1{% endlatex %}: {% latex display%}1 \le e \cdot 1 \cdot \frac{1}{e}{% endlatex %}
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

Druhá strana analogicky (uvažujeme {% latex %}\left(1 - \frac{1}{3^2}\right)\left(1-\frac{1}{5^2}\right)\ldots = \left(\frac{2 \cdot 4}{3^2}\right)\left(\frac{4 \cdot 6}{5^2}\right)\ldots = \frac{1}{2 \left(2m\right) P^2}{% endlatex %}).

### 2. přednáška

#### Náhodné procházky

**Definice náhodné procházky  (v {% latex %}\mathbb{Z}^1{% endlatex %}):** Náhodný proces, v každém kroku se panáček začínající v bodu {% latex %}0{% endlatex %} posune ze své aktuální pozice doprava nebo doleva.

- kde bude po {% latex %}n{% endlatex %} krocích?
- {% latex %}\lim_{n \to \infty} \ldots{% endlatex %} že se po {% latex %}n{% endlatex %} krocích vrátil (někdy v průběhu) do počátku?
- {% latex %}\lim_{n \to \infty} \ldots{% endlatex %} {% latex %}\mathbb{E}[\#\text{návratů do počátku}]{% endlatex %}?
	- dokážeme, že jde k nekonečnu

Zadefinujeme si náhodnou veličinu {% latex %}X = I_{S_2} + I_{S_4} + \ldots + I_{S_{2n}} {% endlatex %}:
- {% latex %}I_{S_{2n}}\ldots{% endlatex %} indikátor, že nastal jev „po {% latex %}2n{% endlatex %} krocích jsem v počátku“
- {% latex %}\mathbb{E}[X] = \mathbb{E}[\#\text{návratů do počátku}]{% endlatex %}.
- {% latex %}\Pr[\text{po $2n$ krocích jsem v počátku}] = \binom{2n}{n}/2^{2n}{% endlatex %}.
	- nahoře jsou možnosti vyrovnaných počtů kroků doprava/doleva
	- dole jsou všechny scénáře pro {% latex %}2n{% endlatex %} kroků

{% latex display %}
\frac{\binom{2n}{n}}{2^{2n}} \ge \frac{\frac{2^{2n}}{2 \sqrt{n}}}{2^{2n}} = \frac{1}{2 \sqrt{n}}
{% endlatex %}

{% latex display %}
\begin{aligned}
	\mathbb{E}[X] &= \mathbb{E}\left[\sum_{i=1}^{\infty} I_{S_{2i}}\right]&& \\
	              &= \sum_{i=1}^{\infty} \mathbb{E}\left[I_{S_{2i}}\right]&&//\ \text{linearita střední hodnoty}\\
	              &= \sum_{i=1}^{\infty} \Pr\left[I_{S_{2i}}\right] &&//\ \text{střední hodnota indikátoru je pravděpodobnost}\\
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
| substituce {% latex %}x^n{% endlatex %}      | {% latex %}a_0, 0, \overset{n - 1}{\ldots}, 0, a_1, 0, \overset{n - 1}{\ldots}, 0, a_2, \ldots {% endlatex %}                 | {% latex %} a(x^n){% endlatex %}              |
|                                              |                                                                                                                               |                                                      |
| derivace                                     | {% latex %}a_1, 2a_1, 3a_2, \ldots {% endlatex %}                                                                             | {% latex %} \alpha a'(x){% endlatex %}               |
| integrování                                  | {% latex %}0, a_1, a_2/2, a_3/3, \ldots {% endlatex %}                                                                        | {% latex %} \int_{0}^{x} a(t) dt{% endlatex %}       |
|                                              |                                                                                                                               |                                                      |
| konvoluce                                  | {% latex %} \sum_{k = 0}^{n} a_k \cdot b_{n - k} {% endlatex %}                                                               | {% latex %} a(x) \cdot b(x){% endlatex %}            |

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
	&= \frac{x}{\left(1 - \frac{1 + \sqrt{5}}{2}x\right)\left(1 - \frac{1 - \sqrt{5}}{2}x\right)} \qquad //\ \text{algebra}\\
	&= \frac{\frac{1}{\sqrt{5}}}{1 - \frac{1 + \sqrt{5}}{2}x} - \frac{\frac{1}{\sqrt{5}}}{1 - \frac{1 - \sqrt{5}}{2}x}  \qquad //\ \text{parciální zlomky }\\
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

Rekurence pro {% latex %}b_n{% endlatex %} vypadá skoro jako konvoluce sama sebe, takže by
se nám líbilo něco jako {% latex %}b(x) = b(x)^2{% endlatex %}. Jenže narozdíl od
konvoluce pronásobujeme jen prvních {% latex %}n-1{% endlatex %} prvků. Uvažme
tedy posloupnost {% latex %}0, b_0, b_1, b_2, \ldots{% endlatex %} generovanou funkcí
{% latex %}x b(x){% endlatex %}. Ta je již skoro konvolucí sama sebe -- {% latex %}n{% endlatex %}-tý prvek se v sumě požere s nulou.
Jediná nepřesnost je u {% latex %}b_0{% endlatex %}, protože podle
definice konvoluce {% latex %}b_0 = 0 \cdot b_0 + b_0 \cdot 0 = 0{% endlatex %}, ale my
víme {% latex %}b_0 = 1{% endlatex %}. Stačí tedy přičíst jedničku posunutou o
jedna doprava, čímž dostaneme {% latex %}x b(x) = (x b(x))^2 + x{% endlatex %}.
Jinými slovy {% latex %}b(x) = x b(x)^2 + 1{% endlatex %}.

{% latex display %}
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

**Pomocné tvrzení:** {% latex %}\forall P, P' \in \mathcal{P} \exists z \in X{% endlatex %}, které neleží ani na jedné z nich.

Dokáže se přes to přes rozbor příkladů toho, jak vedou přímky přes {% latex %}Č{% endlatex %}:
- pokud nevedou přes všechny body z {% latex %}Č{% endlatex %}, pak máme vyhráno
- pokud vedou, tak existují dvě další přímky {% latex %}P_1{% endlatex %} a {% latex %}P_2{% endlatex %} vedoucí kolmo na naše přímky, jejich průnik je hledaný bod; původní přímky jím vést nemohou, protože pak by dvě přímky sdílely 2 body, což nelze
- {% latex %}P_1 \neq P{% endlatex %}, protože pak by {% latex %}P{% endlatex %}
  obsahovala alespoň 3 body z {% latex %}Č{% endlatex %}. Podobně ostatní
  nerovnosti.

{:.center}
![](/assets/kombinatorika-a-grafy-i/bod-na-primce.svg)

### 4. přednáška

**Důkaz původního tvrzení:** pro přímky {% latex %}P{% endlatex %}, {% latex %}P'{% endlatex %} a bod {% latex %}z{% endlatex %} (který nesdílí) budeme dělat bijekci tak, že budu tvořit přímky z bodu {% latex %}z{% endlatex %} na body z {% latex %}P{% endlatex %}, které budou rovněž protínat body z {% latex %}P'{% endlatex %}.

{:.center}
![](/assets/kombinatorika-a-grafy-i/kpr-bijekce.svg)


**Definice (řád KPR):** řádem {% latex %}(X, \mathcal{P}){% endlatex %} je {% latex %}h = |P| - 1{% endlatex %} pro jakoukoliv {% latex %}P \in \mathcal{P}{% endlatex %}.

**Tvrzení:** nechť {% latex %}(X, \mathcal{P}){% endlatex %} je KPR řádu {% latex %}p{% endlatex %}. Pak:
1. každým bodem prochází {% latex %}n + 1{% endlatex %} přímek 
2. {% latex %}|X| = n^2 + n + 1{% endlatex %}
3. {% latex %}|\mathcal{P}| = n^2 + n + 1{% endlatex %}

**Důkaz:**

{:.rightFloatBox}
<div markdown="1">
Explicitní důkaz (3): Pro každý bod započítejme všechny přímky jím
procházející. Dostaneme tak {% latex %}(n^2+n+1)(n+1){% endlatex %} přímek. Ale
každou jsme započítali {% latex %}(n+1){% endlatex %}-krát -- jednou pro každý z
jejích bodů.
</div>

1. triviálně z definice.
2. viz. níže.
3. vychází z duality (viz. další kapitola).

Vezměme libovolné {% latex %}x \in X{% endlatex %}. Pak {% latex %}\exists P \in \mathcal{P}: x \not\in P{% endlatex %}, protože vezmeme-li vody, {% latex %}a, b, c \in Č{% endlatex %}, pak přímky {% latex %}ab{% endlatex %} a {% latex %}ac{% endlatex %} nemohou mít další společný bod než {% latex %}a{% endlatex %} (došlo by ke sporu s některým z axiomů).

Poté stačí uvážit následující obrázek a spočítat body/přímky. Další body už neexistují, protože kdyby existoval, tak by jím musela procházet přímka z {% latex %}x{% endlatex %} a ta by rovněž někde protínala {% latex %}P{% endlatex %} (a nesplňovala tak axiomy).

{:.center}
![](/assets/kombinatorika-a-grafy-i/kpr-pocet.svg)

Bodů na obrázku je {% latex %}\overbrace{1}^{x} + \underbrace{\left(n + 1\right)}_{P_0 \ldots P_n}\overbrace{n}^{\text{body $P_i$, bez $x$}} = n^2 + n + 1{% endlatex %}.

#### Dualita KPR

{:.rightFloatBox}
{% xopp xins %}

**Definice (incidenční graf):** {% latex %}(X, \mathcal{S}){% endlatex %} je množinový systém. Jeho incidenční graf je bipartitní graf {% latex display %}\left(V = X \cup \mathcal{S}, E = \left\{(x, s) \in X \times \mathcal{S}\ |\ x \in s\right\}\right){% endlatex %}

**Definice (duál grafu):** {% latex %}(Y, \mathcal{T}){% endlatex %} je duál {% latex %}(X, \mathcal{S}){% endlatex %} pokud {% latex %}Y = \mathcal{S}{% endlatex %} a {% latex %}\mathcal{T} = \left\{\left\{s \in \mathcal{S}\ |\ x \in s\right\}\ |\ x \in X\right\}{% endlatex %}
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

Pro KPR řádu {% latex %}p^k{% endlatex %}, {% latex %}p{% endlatex %} prvočíslo vezmu algebraické těleso {% latex %}\mathbb{K}{% endlatex %} řádu {% latex %}n{% endlatex %} (příklad {% latex %}\mathbb{K} = \mathbb{Z}_3{% endlatex %}).
- {% latex %}T = \mathbb{K}^3 \setminus \left(0, 0, 0\right){% endlatex %}
- na {% latex %}T{% endlatex %} zavedu ekvivalenci {% latex %}(x, y, t) \in T{% endlatex %} je ekvivalentní s {% latex %}(\lambda x, \lambda y, \lambda t), \forall \lambda \in \mathbb{K} \setminus {0}{% endlatex %}
- body {% latex %}X{% endlatex %} jsou ekvivalenční třídy nad {% latex %}T{% endlatex %}
- reprezentanti: poslední nenulová složka je {% latex %}1{% endlatex %}
	- trojice tvaru {% latex %}(x, y, 1), (x, 1, 0), (1, 0, 0){% endlatex %}
	- můžu si to dovolit, na reprezentanta převedu prostým pronásobením
	- počet je {% latex %}n^2 + n + 1{% endlatex %}, což sedí
- přímky {% latex %}\mathcal{P}{% endlatex %}: pro každou {% latex %}(a, b, c) \in T{% endlatex %} definujeme přímku {% latex %}P_{a, b, c}{% endlatex %} jako množinu bodů {% latex %}(x, y, t){% endlatex %} splňující {% latex %}ax + by + ct = 0{% endlatex %}
	- {% latex %}\forall (x, y, t) \in T, \forall \lambda \neq 0: (x, y, t){% endlatex %} splňuje {% latex %}\iff (\lambda x, \lambda y, \lambda t){% endlatex %} splňuje
	- {% latex %}\forall (a, b, c) \in T, \forall \lambda{% endlatex %} fixuji {% latex %}(x, y, t) \in T: ax + by + ct = 0 \iff \lambda ax + \lambda by + \lambda ct = 0 \implies{% endlatex %} přímky {% latex %}P_{a, b, c} = P_{\lambda a, \lambda b, \lambda c} \implies |\mathcal{P}| = |X|{% endlatex %} a mohu si opět zvolit reprezentanty

{:.center}
![](/assets/kombinatorika-a-grafy-i/kpr-alg.svg)

{:.rightFloatBox}
<div markdown="1">
1. „každá přímka obsahuje {% latex %}\le 2{% endlatex %} body z {% latex %}Č{% endlatex %}“
2. „každé dvě přímky se protínají právě v {% latex %}1{% endlatex %} bodě“
3. „každé dva body určují právě {% latex %}1{% endlatex %} přímku“
</div>

**Ověření axiomů:**
1. {% latex %}Č = \left\{(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)\right\}{% endlatex %}
	- jsou po třech lineárně nezávislé, proto {% latex %}(1){% endlatex %} platí
2. dvojice přímek {% latex %}(a_1, b_1, c_1){% endlatex %} a {% latex %}(a_2, b_2, c_2){% endlatex %} určují jeden bod:
	- jsou lineárně nezávislé a dimenze jádra následující matice je tedy {% latex %}1{% endlatex %} a určují jeden bod (až na {% latex %}\alpha{% endlatex %}-násobek, což je definice bodů)
{% latex display %} \begin{pmatrix} a_1 & b_1 & c_1 \\ a_2 & b_2 & c_2 \end{pmatrix} \begin{pmatrix} x \\ y \\ t \end{pmatrix} = 0 {% endlatex %}
3. analogické, protože role {% latex %}(x, y, t){% endlatex %} a {% latex %}(a, b, c){% endlatex %} je identická

### 5. přednáška

#### Latinské čtverce

**Definice (latinský čtverec)** řádu {% latex %}n{% endlatex %} je tabulka {% latex %}n \times n{% endlatex %} vyplněná čísly {% latex %}[n]{% endlatex %}, kde v žádném řádku či sloupci se symboly neopakují.
- (👀) {% latex %}A{% endlatex %} je LČ {% latex %}\implies{% endlatex %} po následujících operacích je stále:
	- permutace symbolů
	- permutace sloupců/řádků

**Definice (ortogonalita)**: LČ {% latex %}A, B{% endlatex %} jsou ortogonální, pokud pro každou dvojici symbolů {% latex %}a, b \in [n]{% endlatex %} existují indexy {% latex %}i, j \in [n]{% endlatex %} t. ž. {% latex %}(A)_{i, j} = a, (B)_{i, j} = b{% endlatex %}.
- když přeložím čtverce přes sebe, najdu políčko {% latex %}(i, j){% endlatex %} obsahující dvojici {% latex %}(a, b){% endlatex %}
- (👀) počet dvojic symbolů {% latex %}n^2 = {% endlatex %} počtu políček
	- zobrazení je bijekce
	- {% latex %}\forall (a, b){% endlatex %} se objeví v OLČ právě jednou
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

**Důkaz:** mějme maximální rodinu NOLČ {% latex %}L_1, \ldots, L_m{% endlatex %} a permutujme symboly tak, aby každý první řádek byl {% latex %}1, 2, 3, \ldots, n{% endlatex %}; uvažme symbol na pozici {% latex %}(2, 1){% endlatex %}:
- není {% latex %}1{% endlatex %}, ta je na pozici {% latex %}(1, 1){% endlatex %}
- není nějaké {% latex %}k \in \left\{2, \ldots, n\right\}{% endlatex %} ve dvou čtvercích zároveň

Čtverců je dohromady tedy nejvýše {% latex %}n - 1{% endlatex %}.

{:.rightFloatBox}
<div markdown="1">
Pro libovolné dvě pozice (které se liší v řádku a sloupci) existuje čtverec, který na nich má stejné hodnoty.
</div>

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

Ve sloupci s otazníkem nemůže symbol {% latex %}1{% endlatex %} být:
- v řádku s {% latex %}(1){% endlatex %}
- ve dvou čtvercích na stejném místě

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
	1. zvolíme libovolně přímku {% latex %}I = \left\{r, s, l_1, \ldots, l_{n - 1}\right\}{% endlatex %}
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
- počet teček {% latex %}= n (n -1) (n-2) \ldots (n - k + 1) = \frac{n!}{(n - k)!}{% endlatex %} (vyberu {% latex %}1.{% endlatex %} prvek, {% latex %}2.{% endlatex %} prvek,...)
- v každé buňce {% latex %}k{% endlatex %}-tic (ekvivalenční třídě přes příslušnou relaci) se stejnými prvky je {% latex %}k!{% endlatex %} prvků, počet buňek je to, co chceme (neuspořádaná {% latex %}k{% endlatex %}-tice)

{% latex display %}
\begin{aligned}
	\frac{n!}{(n - k)!} &= \left|\binom{X}{k}\right| \cdot k! \\
	\left|\binom{X}{k}\right|&=  \frac{n!}{(n - k)! k!} = \binom{n}{k} \\
\end{aligned}
{% endlatex %}

**Věta (Spernerova):** nechť {% latex %}(\mathcal{P}, \subseteq){% endlatex %} je částečné uspořádání, kde {% latex %}\mathcal{P}{% endlatex %} je množinový systém. Nechť {% latex %}\mathcal{M}{% endlatex %} je největší antiřetězec ({% latex %}\forall M_1, M_2 \in \mathcal{M}, M_1 \neq M_2: M_1 \nsubseteq M_2 \land M_2 \nsubseteq M_1{% endlatex %}). Pak {% latex %}|\mathcal{M}| \le \binom{n}{\left\lceil \frac{n}{2} \right\rceil}{% endlatex %}, kde {% latex %}n = |X|{% endlatex %}.

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
- (👀) každý maximální řetězec obsahuje {% latex %}\le 1\ M \in \mathcal{M}{% endlatex %} 

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

{:.rightFloatBox}
![Vidlička.](/assets/kombinatorika-a-grafy-i/vidlicka.svg)

**Důkaz:** dvojí počítání „vidliček“ (cest delky {% latex %}2{% endlatex %}):
1. pro pevnou dvojici {% latex %}\left\{u, u'\right\}{% endlatex %} mám nanejvýš 1 vidličku (dvě by tvořily čtyřcyklus), tedy {% latex %}\#\ \text{vidliček}\ \le \binom{n}{2}{% endlatex %}
2. pro pevný vrchol {% latex %}v{% endlatex %} máme {% latex %}\#\ \text{vidliček}\ = \binom{d_i}{2}{% endlatex %}

{% latex display %}
	\#\ \text{vidliček}\ = \sum_{i = 1}^{n} \binom{d_i}{2} \le \binom{n}{2}
{% endlatex %}

Také víme (z principu sudosti), že:

{% latex display %}
	|E| = \frac{1}{2} \sum_{i = 1}^{n} d_i
{% endlatex %}

Předpoklad: nemáme izolované vrcholy ({% latex %}d_i \ge 1{% endlatex %}), jsou zbytečné. Pak {% latex %}\binom{d_i}{2} \ge \frac{(d_i - 1)^2}{2}{% endlatex %}.

{% latex display %}
\frac{n^2}{2} \ge \binom{n}{2} \ge \sum_{i = 1}^{n} \binom{d_i}{2} \ge \sum \frac{(d_i - 1)^2}{2} = \sum \frac{k_i^2}{2} \qquad //\ \text{substituce} \\
\sum k_i^2 \le n^2
{% endlatex %}

Využijeme Cauchy-Schwartzovu nerovnost na {% latex %}x = (k_1, \ldots, k_n), y = (1, \ldots, 1){% endlatex %}:
{% latex display %}
xy = \sum k_i = \sum \left(d_i - 1\right) = 2|E| - n \\
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

{:.rightFloatBox}
{% xopp kostry %}

**Důkaz:** počítání {% latex %}(T, r, č){% endlatex %}, kde:
- {% latex %}T{% endlatex %} je strom na {% latex %}n{% endlatex %} vrcholech
- {% latex %}r{% endlatex %} kořen (hrany vedou do kořene, ne z něho)
- {% latex %}č{% endlatex %} očíslování hran (nějaké), {% latex %}č: E \mapsto [n - 1]{% endlatex %}

1. {% latex %}\#(T, r, č) = \Kappa(n) \cdot n \cdot \left(n - 1\right)!{% endlatex %}
	- {% latex %}T{% endlatex %} je to, co hledáme
	- {% latex %}r{% endlatex %} volíme libovolně z {% latex %}n{% endlatex %} vrcholů
	- {% latex %}č{% endlatex %} je prostě random očíslovaní na {% latex %}n - 1{% endlatex %} hranách
2. představa: přidávám hrany, až nakonec dojdu k {% latex %}(T, r, č){% endlatex %} a jsem v {% latex %}k{% endlatex %}-tém kroce:
	- (👀) nesmím vést hranu uvnitř komponenty (cykly)
	- (👀) musím vést hranu pouze z kořene dané komponenty (jeden vrchol by měl 2 rodiče)

	1. zvolím, kam šipka povede... {% latex %}n{% endlatex %} způsobů
	2. zvolím komponentu, ze které povede... {% latex %}n - k - 1{% endlatex %}
		- máme {% latex %}n - k{% endlatex %} komponent a {% latex %}1{% endlatex %} je blokovaná

{% latex display %}
\begin{aligned}
	\#(T, r, č) &= \prod_{k = 0}^{ \overbrace{n - 2}^{\text{počet šipek je $n - 1$}}} n ( n - k - 1) = n^{n - 1} (n -1)! \\
	\Kappa(n) \cdot n \cdot \left(n - 1\right)! &= n^{n - 1} (n -1)! \\
	\Kappa(n) &= n^{n - 2}
\end{aligned}
{% endlatex %}

### 7. přednáška

#### Toky

**Definice (síť)** je čtveřice {% latex %}(G, z, s, c){% endlatex %}, kde:
- {% latex %}G{% endlatex %} je orientovaný graf, {% latex %}z, s \in V(G){% endlatex %}
- {% latex %}c: E \mapsto \mathbb{R}_{\ge 0}{% endlatex %}

{:.rightFloatBox}
<div markdown="1">
1. omezení shora kapacitami
2. Kirchhoff
</div>
**Definice (tok)** v síti je {% latex %}f: E \mapsto \mathbb{R}_{\ge 0}{% endlatex %}, t. ž.:
1. {% latex %}\forall e \in E(G){% endlatex %} platí {% latex %}0 \le f(e) \le c(e){% endlatex %}
2. {% latex %}\forall v \in V(G), v \not\in \left\{z, s\right\}{% endlatex %} platí {% latex %}\sum f(x, v) = \sum f(v, y){% endlatex %}

{:.rightFloatBox}
<div markdown="1">
To, co teče ven ze zdroje.
</div>

**Definice (velikost toku)** {% latex %}w(f) = \sum f(z, x) - \sum f(x, z){% endlatex %} 

**Věta:** existuje maximální tok.

**Nástin důkazu:** Nástin je takový, že množina toků je kompaktní a obsahuje tedy i maximum (nevznikne nám tam nějaká divnost).

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

**Důkaz:** sporem, že {% latex %}f{% endlatex %} maximální je nasycený.
- tak uvážíme množinu vrcholů, do kterých se lze dostat ze {% latex %}z{% endlatex %} po nasycené cestě -- {% latex %}A = \left\{v \in V\ |\ \exists\ \text{nenasycená cesta }\right\}{% endlatex %}
	- {% latex %}s \nsubseteq A{% endlatex %} (jinak {% latex %}f{% endlatex %} není nasycený)
	- {% latex %}\forall e \in S(A, V \setminus A){% endlatex %} platí {% latex %}f(e) = c(e){% endlatex %}
	- {% latex %}\forall e \in S(V \setminus A, A){% endlatex %} platí {% latex %}f(e) = 0{% endlatex %} (jinak bychom nenasycenou cestu mohli prodloužit

{% latex display %}
\begin{aligned}
	w(f) &= f(A, V \setminus A) - f(V \setminus A, A) \qquad //\ \text{předešlé lemma}\\
	&= c(A, V \setminus A) - 0\\
	&= c(f)
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

- {% latex %}R{% endlatex %} je minimální {% latex %}z-s{% endlatex %} řez
- {% latex %}C{% endlatex %} je minimální vrcholové pokrytí
- {% latex %}f{% endlatex %} je maximální tok
	- hrany v původním grafu jsou maximální párování
- {% latex %}L, P ={% endlatex %} levá a pravá část grafu (bez zdroje a stoku)

Z toku mám maximální párování {% latex %}M{% endlatex %} velikosti {% latex %}k{% endlatex %}, ze kterého sestrojím minimální řez {% latex %}R{% endlatex %}.

{% latex %}R{% endlatex %} je minimální {% latex %}z-s{% endlatex %} řez. Ten upravíme na minimální řez {% latex %}R'{% endlatex %}, aby neobsahoval hrany původního grafu. To jde, protože hranu původního grafu mohu vyměnit za tu ze zdroje/stoku, protože ta je jediný způsob, jak se dostat do hrany z původního vrcholu.
- {% latex %}W = \left\{u \in L\ |\ (z, u) \in R'\right\} \cup \left\{v \in P\ |\ (v, s) \in R'\right\}{% endlatex %}
	- je vrcholové pokrytí, v původním grafu by jinak existovala {% latex %}z-s{% endlatex %} cesta a nejednalo se o řez

{% latex %}W{% endlatex %} je minimální vrcholové pokrytí {% latex %}G{% endlatex %}:
- {% latex %}R = \left\{(z, u)\ |\ u \in W \cap L\right\} \cup \left\{(u, s)\ |\ u \in W \cap P\right\} {% endlatex %}
	- je řez (pro spor by existovala cesta, kterou by {% latex %}W{% endlatex %} nepokryl)

Dostáváme tedy, že min. řez je roven nějakému pokrytí, a že min. pokrytí je rovno nějakému řezu, tedy že min. pokrytí je rovno min. řezu.

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

**Důsledek:** nechť {% latex %}B = (V_1 \cup V_2, E){% endlatex %} je bipartitní graf, kde {% latex %}k_1 = \mathrm{min}\ \underset{v \in V_1}{\deg}\ v, k_2 = \mathrm{max}\ \underset{v \in V_2}{\deg}\ v {% endlatex %} a {% latex %}k_1 \ge k_2{% endlatex %}, pak je splněna Hallova podmínka.

**Důkaz:** Ověřím Hallovu podmínku (pozor, prohozené strany). Máme-li množinu {% latex %}J{% endlatex %} a každá vidí alespoň {% latex %}k_1{% endlatex %} hran, pak vidím {% latex %}\ge |J| k_1{% endlatex %} hran. Abych pohltil všechny tyto hrany, tak musí napravo být alespoň {% latex %}k_2 |N[j]|{% endlatex %} vrcholů. Musí tedy platit:
{% latex display %}|J| k_1 \le \#\ \text{hran} \le k_2 |N[J]|{% endlatex %}

Protože {% latex %}k_1 \ge k_2{% endlatex %}, pak {% latex %}|N[j]| \ge |J|{% endlatex %}.

**Aplikace:** doplňování latinských obdélníků:

{:.center}
![Latinský obdelník.](/assets/kombinatorika-a-grafy-i/lat-rect.svg)

- stupně: každý sloupec má stupeň {% latex %}n - k{% endlatex %} (počet nepoužitých symbolů)
- symboly: každý symbol se vyskytuje v řádku právě jednou, tedy ještě není v {% latex %}n - k{% endlatex %} sloupcích

Máme tedy {% latex %}\left(n - k\right){% endlatex %}-regulární graf, pro který {% latex %}\exists{% endlatex %} perfektní párování (použití minulého důsledku).

#### Míra souvislosti neorientovaných grafu

**Definice**
- **hranový řez** v grafu {% latex %}G{% endlatex %} je {% latex %}F \subseteq E{% endlatex %} t. ž. {% latex %}G' = (V, E \setminus F){% endlatex %} je nesouvislý.
- **vrcholový řez** v grafu {% latex %}G{% endlatex %} je {% latex %}A \subseteq V{% endlatex %} t. ž. {% latex %}G' = (V \setminus A, E \cap \binom{V \setminus A}{2}) = G\left[V \setminus A\right]{% endlatex %} je nesouvislý.
- **hranová souvislost** {% latex %}k_e(G) = \mathrm{min} \left\{|F|\ |\ F \subseteq E \text{ je hranový řez}\right\}{% endlatex %}
- **vrcholová souvislost** {% latex %}k_v(G) = \begin{cases}n - 1 & G \cong K_n \\ \mathrm{min} \left\{|A|\ |\ A \subseteq V \text{ je vrcholový řez}\right\} & \text{jindy} \end{cases}{% endlatex %}
- {% latex %}G{% endlatex %} je **hranově/vrcholově {% latex %}k{% endlatex %}-souvislý**, pokud {% latex %}k_{e/v}(G) \ge k{% endlatex %}
	- „potřebuješ useknout alespoň {% latex %}k{% endlatex %} hran/vrcholů na to, aby se graf rozpadl“
	- (👀) je-li {% latex %}3{% endlatex %}-souvislý, pak je i {% latex %}2{% endlatex %}-souvislý a {% latex %}1{% endlatex %}-souvislý
	- je **kriticky** {% latex %}k{% endlatex %}-souvislý, pokud odstranění libovolného vrcholu sníží stupeň souvislosti
		- stromy jsou hranově {% latex %}1{% endlatex %}-souvislé, vrcholově ne (co listy?)

**Lemma:** {% latex %}\forall G, \forall e \in E{% endlatex %} platí {% latex %}k_e(G) - 1 \le k_e(G - e) \le k_e(G){% endlatex %}
- zas tak triviální to není, u vrcholové může (odstraněním vrcholu) vzrůst (listy z kružnice)
- lemma říká, že se hranová souvislost „chová slušně“

{:.rightFloatBox}
<div markdown="1">
Tomovo poznámka: V důkazu {% latex %}k_e(G) \le k_v(G){% endlatex %} se tohle lemma nepoužívá (alespoň tak, jak to chápu). Jsem trochu zmatený z toho, proč Martin říkal, že ano.
</div>

**Důkaz ({% latex %}\le{% endlatex %}):** vezmu minimální řez {% latex %}F \subseteq E{% endlatex %} v {% latex %}G{% endlatex %}, {% latex %}F' = F \setminus \left\{e\right\}{% endlatex %} jistě musí být řez v {% latex %}G - e{% endlatex %}; pak:
{% latex display %}k_e(G - e) \le |F'| \le |F| = k_e(G){% endlatex %}

**Důkaz ({% latex %}\ge{% endlatex %}):** vezmu minimální řez {% latex %}B{% endlatex %} v {% latex %}G - e{% endlatex %} {% latex %}B' = B \cup \left\{e\right\}{% endlatex %} je řezem v {% latex %}G{% endlatex %}, pak:
{% latex display %}
\begin{aligned}
	k_e(G) \le |B'| &= |B| + 1 = k_e(G - e) + 1\\
	k_e(G) - 1 &\le k_e(G - e)
\end{aligned}
{% endlatex %}

**Lemma:** {% latex %}\forall G, \forall e \in E{% endlatex %} platí {% latex %}k_v(G) - 1 \le k_v(G - e) \le k_v(G){% endlatex %}

**Důkaz:** trochu přeformulujeme... pro {% latex %}H = G - e: k_v (H + e) \le k_v (H) + 1{% endlatex %}:

V {% latex %}H{% endlatex %} existuje vrcholový řez {% latex %}A \subseteq V(H), k_v(H) = |A|{% endlatex %}. Při odebrání {% latex %}A{% endlatex %} se {% latex %}H{% endlatex %} rozpadne na alespoň {% latex %}2{% endlatex %} komponenty. Sledujeme (rozebíráme případy), co se se souvislostí stane, když přidáme do grafu hranu {% latex %}e{% endlatex %}:
- alespoň {% latex %}1{% endlatex %} konec {% latex %}e{% endlatex %} leží v {% latex %}A{% endlatex %}:
	- přidání {% latex %}e{% endlatex %} nespojí žádné {% latex %}2{% endlatex %} komponenty, {% latex %}A{% endlatex %} je řezem i pro {% latex %}G = H + e{% endlatex %}
- oba konce leží v {% latex %}1{% endlatex %} komponentě
	- stejný argument jako (1)
- hrana {% latex %}e{% endlatex %} spojuje {% latex %}2{% endlatex %} komponenty
	- pokud je počet komponent {% latex %}\ge 3{% endlatex %}, tak je {% latex %}A{% endlatex %} stále řezem (po spojení jsou stále {% latex %}2{% endlatex %})
	- pokud není, tak:
		- BUNO {% latex %}|C_1| \ge 2{% endlatex %}; nechť {% latex %}e = xy{% endlatex %} a {% latex %}x{% endlatex %} leží v {% latex %}C_1{% endlatex %}, pak {% latex %}A \cup {x}{% endlatex %} je řezem, protože mi v obou komponentách něco zbylo
		- {% latex %}|C_1| = |C_2| = 1{% endlatex %}:
			- {% latex %}|V| = |A| + 2 \implies |A| = |V| - 2 = k_v(H){% endlatex %}
			- {% latex %}k_v(H + e) \overset{\text{def.}}{\le} |V| - 1 = k_v(H) + 1{% endlatex %}

**Věta:** {% latex %}k_v(G) \le k_e(G){% endlatex %}: indukcí podle počtu hran:
- pokud {% latex %}|E| < |V| - 1{% endlatex %}, pak je {% latex %}G{% endlatex %} nesouvislý a {% latex %}k_v(G) = 0 = k_e(G){% endlatex %}
- nechť nadále {% latex %}k_e(G) > 0{% endlatex %}; vezmu min. hranový řez {% latex %}F \subseteq E{% endlatex %} a {% latex %}e \in F{% endlatex %}; také {% latex %}G' = G - e{% endlatex %}
	- na {% latex %}G'{% endlatex %} použiju IP, tedy {% latex %}k_v(G') \le k_e(G'){% endlatex %}
	- z lemmatu o souvislosti vrcholů (a přičtení jedničky) víme:
{% latex display %}k_v(G) - 1 \le k_v(G - e) \overset{\mathrm{IP}}{\le} k_e(G - e) = k_e(G) - 1{% endlatex %}

Kde poslední rovnost platí, protože {% latex %}F' = F \setminus {e}{% endlatex %} je (z definice) řezem {% latex %}G - e{% endlatex %}.

**Věta (Ford-Fulkerson):** {% latex %}\forall G{% endlatex %}, pokud {% latex %}k_e(G) \ge t{% endlatex %}, pak {% latex %}\forall u, v
{% endlatex %} mezi {% latex %}u, v{% endlatex %} existuje alespoň {% latex %}t{% endlatex %} hranově disjunktních cest

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

**Důkaz ({% latex %}\Leftarrow{% endlatex %}):** stejný jako FF, jen nahraď „hrany“ za „vrcholy“.

**Důkaz ({% latex %}\Rightarrow{% endlatex %}):** uděláme trik s dělením vrcholů na dva ({% latex %}\deg_{\mathrm{in}}, \deg_{\mathrm{out}}{% endlatex %}) a v libovolném řezu nahradíme hrany vedoucí do/z vrcholů za hranu spojující vrcholy. 

### 10. přednáška

#### Lepení uší

**Věta:** graf je {% latex %}2{% endlatex %}-souvislý právě tehdy, když jej lze vytvořit  z {% latex %}K_3{% endlatex %} posloupností:
- dělení hran
- přidávání hran

**Důkaz ({% latex %}\Rightarrow{% endlatex %}):**
- zvolme {% latex %}G_0{% endlatex %} libovolně (kružnici mít musí, jinak není {% latex %}2{% endlatex %}-souvislý).
- předpokládejme, že {% latex %}G_j, j \le i{% endlatex %} jsou definovány jako výše
- pokud {% latex %}G_i = G{% endlatex %}, tak jsme hotovi
- jinak {% latex %}E_i \neq E{% endlatex %}, {% latex %}G{% endlatex %} je souvislý
	- {% latex %}\exists e = \left\{v, v'\right\} \in E \setminus E_i{% endlatex %}, která se dotýká původního grafu ({% latex %}e \cap V_i \neq \emptyset{% endlatex %})
		- pokud oba vrcholy {% latex %}e{% endlatex %} patří do {% latex %}V_i{% endlatex %}, tak ji přidám ({% latex %}G_{i + 1} = G_i + e{% endlatex %})
		- pokud ne: {% latex %}G - v{% endlatex %} musí stále být souvislý ({% latex %}G{% endlatex %} je {% latex %}2{% endlatex %}-souvislý) -- prostě vezmeme nejkratší cestu zpět do nějakého {% latex %}G_j{% endlatex %}

{:.center}
![Lepení uší.](/assets/kombinatorika-a-grafy-i/ears.svg)

**Důkaz ({% latex %}\Leftarrow{% endlatex %}):** stačí vidět, že nikdy nevznikne artikulace, protože uši lepím mezi {% latex %}2{% endlatex %} různé vrcholy.

#### Samoopravné kódy

**Hammingův kód:** vycházíme z fannovy roviny a o přímkách uvažujeme jako o prvcích {% latex %}\mathbb{Z}_2^7{% endlatex %}

{% latex display %}H = \underbrace{\left\{\text{char. vektory přímek}\right\}}_{P_1 = \left\{1, 2, 4\right\} = (1\ 1\ 0\ 1\ 0\ 0\ 0)} \cup \underbrace{\left\{\text{char. vektory doplňků přímek}\right\}}_{P_1 + (1\ \ldots\ 1) = (0\ 0\ 1\ 0\ 1\ 1\ 1)} \cup \left\{(0\ \ldots\ 0), (1\ \ldots\ 1)\right\}{% endlatex %}
- {% latex %}|H| = 7 + 7 + 2 = 16{% endlatex %}
- {% latex %}c \in H{% endlatex %} je **kódové slovo**
- {% latex %}H{% endlatex %} je **kód**
- (👀) {% latex %}\forall c, c' \in H{% endlatex %} se liší v alespoň třech souřadnicích
	- vychází z KPR, později dokážeme obecně
- (👀)  {% latex %}\forall v \in \mathbb{Z}_2^7 \exists! c \in H{% endlatex %} t. ž. {% latex %}d(v, c) \le 1{% endlatex %}
	- dostáváme z toho dekódovací pravidlo -- dekóduj na nejbližší slovo!

**Protokol:**
1. vezmi kódovou zprávu
2. rozděl na {% latex %}4{% endlatex %}-bitové bloky
3. zakóduj přes Hammingův kód
	- nějak rozumně očísluj kódová slova!
4. profit?

**Výsledek:**
- zpráva je o {% latex %}7/4{% endlatex %} delší
- {% latex %}\Pr\left[\text{jeden blok se správně rozkóduje}\right] = \overbrace{(1 - p)^7}^{\text{vše ok}} + \overbrace{7p(1 - p)^6}^{\text{jeden špatně}} = (1-p)^6(1 + 6p){% endlatex %}
- {% latex %}\Pr\left[\text{celá zpráva se správně dekóduje}\right] = \left((1-p)^6(1 + 6p)\right)^{n/4}{% endlatex %}
	- pro {% latex %}n = 100, p = 0.01{% endlatex %} vyjde {% latex %}95\%{% endlatex %}, což je nice!

---

**Definice:**
- {% latex %}\Sigma \ldots{% endlatex %} abeceda
	- {% latex %}s \in \Sigma^n \ldots{% endlatex %} slovo (vstup)
- {% latex %}C \subseteq \Sigma^n \ldots{% endlatex %} kód
	- {% latex %}c \in C \ldots{% endlatex %} kódové slovo (naše special slova)
	- {% latex %}|C| \ldots{% endlatex %} velikost kódu (počet kódových slov)
	- {% latex %}n \ldots{% endlatex %} délka kódu (kolikaznakové slova máme)
	- {% latex %}k = \log |C| \ldots{% endlatex %} dimenze kódu (bude se hodit později)
- pro {% latex %}x, y \in \Sigma^n: d_H (x, y) = d(x, y)\ldots{% endlatex %}  počet souřadnic, ve kterých se liší
	- {% latex %}d = \Delta(C) = \underset{x, y \in C}{\mathrm{min}}\ d(x, y) \ldots{% endlatex %} (min.) vzdálenost {% latex %}C{% endlatex %}
		- {% latex %}d = 1 \ldots{% endlatex %} nepoznám chybu
		- {% latex %}d = 2 \ldots{% endlatex %} poznám, že došlo k chybě
		- {% latex %}d = 3 \ldots{% endlatex %} umím opravit {% latex %}1{% endlatex %} chybu
		- {% latex %}\Delta(C) \ge 2t + 1{% endlatex %} znamená, že „{% latex %}C{% endlatex %} má schopnost opravit {% latex %}t{% endlatex %} chyb“
- kód s vlastnostmi {% latex %}n, k, d{% endlatex %} se označuje {% latex %}(n,k,d)-{% endlatex %} kód

**Příklady kódů:**
1. totální kód {% latex %}C = \Sigma^n{% endlatex %} (nic se nekóduje)
	- délka {% latex %} = n{% endlatex %}
	- velikost {% latex %}= 2^n \implies k = \log |C| = n{% endlatex %}
	- {% latex %}\Delta(C) = 1{% endlatex %}
	- {% latex %}\implies (n, n, 1)-{% endlatex %}kód
2. opakovací kód délky {% latex %}n{% endlatex %} (pozor, {% latex %}n{% endlatex %} je délka slova)
	- délka {% latex %}= n{% endlatex %}
	- velikost {% latex %}= 2 \implies k = 1{% endlatex %}
	- {% latex %}\Delta(C) = n{% endlatex %}
	- {% latex %}\implies (n, 1, n)-{% endlatex %}kód
3. paritní kód {% latex %}C \subseteq \Sigma^n{% endlatex %} t. ž. {% latex %}x \in C: \sum_{x_i} = 0{% endlatex %} (počet jedniček je sudý)
	- délka {% latex %}= n{% endlatex %}
	- velikost {% latex %}= 2^{n - 1} \implies k = n - 1{% endlatex %}
	- {% latex %}\Delta(C) = 2{% endlatex %}, protože změna bitů mění paritu
	- {% latex %}\implies (n,  n - 1, 2)-{% endlatex %}kód
4. Hammingův kód
	- {% latex %}\implies (7,  4, 3)-{% endlatex %}kód

### 11. přednáška

#### Jak nejefektivněji můžeme kódovat?

{:.rightFloatBox}
<div markdown="1">
Maximální velikost kódu (počet kódových slov), když určím délku a vzdálenost.
</div>

- {% latex %}A(n, d) = \underset{C}{\mathrm{max}} \log |C|{% endlatex %}
	- {% latex %}C{% endlatex %} jsou binární kódy délky {% latex %}n{% endlatex %} s min. vzdáleností {% latex %}\ge d{% endlatex %}
	- {% latex %}A(n, 1) = n{% endlatex %} (triviální kód)
	- {% latex %}A(n, 2) \ge n - 1{% endlatex %} (paritní kód má {% latex %}|C| = 2^{n -1}, d = 2{% endlatex %})

(👀) {% latex %}\forall d \le n, d \ge 2: A(n, d) \le A(n - 1, d - 1){% endlatex %}
- po odstranění bitu vzdálenost slov klesne nejvýše o {% latex %}1{% endlatex %} (pokud se slova v bytu liší); velikost nového kódu {% latex %}|C'| = |C|{% endlatex %} (díky předpokladu funguje, žádná slova se nesloučí)

**Věta (Simpletonův odhad):** {% latex %}\forall d \le n{% endlatex %} platí {% latex %}A(n, d) \le n - d + 1{% endlatex %}
- {% latex %}A(n, d) \le A(n - 1, d - 1) \le \ldots \le A(n - d + 1, 1) = n - d + 1{% endlatex %}
- rovněž dostávám {% latex %}A(n, 2) \le A(n - 1, 1) = n - 1{% endlatex %} a vím, že {% latex %}A(n, 2) \ge n - 1{% endlatex %}, tedy rovnost

**Tvrzení:** pro každé sudé {% latex %}d \le n{% endlatex %} je {% latex %}A(n, d) = A(n - 1, d - 1){% endlatex %}

**Důkaz:** nechť {% latex %}C{% endlatex %} je {% latex %}(n - 1, k, d - 1){% endlatex %}-kód. Přidáním paritního bitu ke každému slovu vytvořím {% latex %}(n, k, d)-{% endlatex %}kód, protože slova {% latex %}c{% endlatex %} v liché vzdálenosti (speciálně {% latex %}d - 1{% endlatex %}) v {% latex %}C'{% endlatex %} mají vzdálenost o 1 větší (liší se jejich paritní symboly).
- {% latex %}\implies{% endlatex %} nejzajímavější jsou kódy s lichým {% latex %}d{% endlatex %} (na sudé lze triviálně rozšířit)

#### Lineární kódy

**Definice:** kód {% latex %}C{% endlatex %} nad {% latex %}\mathbb{Z}_2^n{% endlatex %} je lineární kód, pokud tvoří vektorový podprostor.
- {% latex %}\forall c, c' \in C: c + c' \in C{% endlatex %}
- {% latex %}\forall \alpha \in \mathbb{Z}_2: \alpha c \in C{% endlatex %}

(👀) pokud {% latex %}C{% endlatex %} je dimenze {% latex %}k{% endlatex %}, pak má {% latex %}2^k{% endlatex %} prvků, ale k jeho popisu stačí nějaká báze {% latex %}C \equiv k{% endlatex %} slov t. ž. ostatní dostanu lineárními kombinacemi.

**Příklad:** Hammingův kód {% latex %}\mathcal{H}{% endlatex %} je lineární a generuje ho **generujicí matice**
{% latex display %}
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
\end{pmatrix}{% endlatex %}

- generující matice kódu {% latex %}H{% endlatex %}
- {% latex %}\left\{v_1, \ldots, v_4\right\}{% endlatex %} je báze {% latex %}H{% endlatex %}
- {% latex %}\forall c \in H\ \exists \alpha_1, \ldots, \alpha_4 \in \mathbb{Z}_2{% endlatex %} t. ž. {% latex %}c = \sum_{i = 1}^{4} \alpha_i v_i {% endlatex %}

(👀) {% latex %}\forall x, y, z \in C: d(x, y) = d(x + z, y + z){% endlatex %}
- „posunutí nějakým směrem“
- platí pro všechny kódy, ale hodí se jen u lineárních kódů, protože díky tomu, že tvoří VP je součet také kódové slovo
- {% latex %}x + z, y + z \in C{% endlatex %} (lineární kódy)
	- {% latex %}d(x, y) = d(0, y - x){% endlatex %}
	- {% latex %}\Delta(C) = \underset{x, y \in C}{\mathrm{min}}\ d(0, y - x) \implies \underset{x \in C}{\mathrm{min}}\ d(0, x){% endlatex %}, což je počet nenulových souřadnic

---

- {% latex %}\langle x, y \rangle \sum_{i = 1}^{n} x_i \cdot y_i{% endlatex %} -- něco jako skalární součin
	- nemusí platit, že {% latex %}x \neq 0 \implies \langle x, x \rangle \neq 0{% endlatex %} (např. pro {% latex %}(1\ 1\ 0\ 0){% endlatex %})

**Definice (duální kód)** {% latex %}C{% endlatex %} je ortogonální doplněk {% latex %}C^\perp = \left\{x\ |\ \langle x, y \rangle = 0, \forall y \in C\right\}{% endlatex %}
- může být {% latex %}C \cap C^\perp \neq \left\{0\right\}{% endlatex %}, ale platí {% latex %}\dim C + \dim C^\perp = n{% endlatex %}

(👀) {% latex %}C^\perp{% endlatex %} je opět vektorový podprostor, je to tedy taky kód
- má také generující matici {% latex %}M{% endlatex %} (tzv. **paritní/kontrolní**)
- platí {% latex %}C = \left\{x\ |\ Mx = 0\right\}{% endlatex %} (z definice naší „ortogonality“)
	- stačí ověřit ortogonalitu na bázové vektory

(👀) nechť {% latex %}G{% endlatex %} je generující matice kódu {% latex %}C{% endlatex %}
- {% latex %}G{% endlatex %} můžu zgausoeliminovat na {% latex %}G'{% endlatex %}, která stále generuje {% latex %}C{% endlatex %}
- ke kódování daného slova stačí sečíst příslušné řádky {% latex %}G'{% endlatex %}, protože se jedná o jediný způsob, jak dostat bity slova

{% latex display %}c = (1\ 1\ 0\ 1) \qquad x = (\underbrace{1\ 1\ 0\ 1}_{\text{informační bity}} \overbrace{\ldots\ldots\ldots}^{\text{kontrolní/paritní bity}}){% endlatex %}

##### Dekódování

Mějme {% latex %}C{% endlatex %} lineární kód délky {% latex %}n{% endlatex %} nad {% latex %}\mathbb{Z}_2^4{% endlatex %}. Bylo odesláno slovo {% latex %}x \in C{% endlatex %} a přijato slovo {% latex %}\tilde{x}{% endlatex %}.
- mohly nastat chyby {% latex %}e = \tilde{x} - x{% endlatex %} (chybový vektor)
	- chceme ho objevit, abychom rozluštili {% latex %}x{% endlatex %}

{% latex %}P{% endlatex %} je paritní matice kódu {% latex %}C{% endlatex %}, tzn. {% latex %}C = \left\{x\ |\ Px = 0\right\}{% endlatex %}.

**Definice (syndrom)** slova {% latex %}z{% endlatex %} je {% latex %}Pz{% endlatex %}, kde {% latex %}P{% endlatex %} je paritní matice kódu {% latex %}C{% endlatex %}.
- (👀) kódová slova {% latex %}\equiv{% endlatex %} slova se syndromem {% latex %}0{% endlatex %} (viz. definice {% latex %}P{% endlatex %}...)

**Předpoklad:** chybový vektor {% latex %}e{% endlatex %} je slovo s nejmenší vahou ve své třídě
- **třída** {% latex %}= \left\{e'\ |\ Pe' = P\tilde{x} = P(x + e) = Px + Pe = Pe\right\}{% endlatex %} (slova se stejným syndromem)
- **reprezentant** třídy {% latex %}s \in Z_2^k{% endlatex %} je slovo {% latex %}m(s) \in Z_2^n{% endlatex %} t. ž. {% latex %}P m(s) = s{% endlatex %} t. ž. {% latex %}w(m(s){% endlatex %} je minimální

**Dekódování:**
- vezmu {% latex %}s = P\tilde{x}{% endlatex %}
- najdu reprezentanta {% latex %}m(s){% endlatex %}
- výsledek dekódování {% latex %}y = \tilde{x} - m(s) = \tilde{x} - m(P\tilde{x}){% endlatex %}
	- (👀)  {% latex %}y{% endlatex %} má mezi kódovými slovy nejmenší vzdálenost od {% latex %}\tilde{x}{% endlatex %}

**Příklad:**
- {% latex %}G = \begin{matrix} v_1 \\ v_2 \end{matrix} \begin{pmatrix} 1 & 1 & 1 & 0 & 0 \\ 0 & 0 & 1 & 1 & 1 \end{pmatrix}{% endlatex %}
- {% latex %}k = 2{% endlatex %}, máme {% latex %}4{% endlatex %} slova {% latex %}\left\{v_1, v_2, (0\ \ldots\ 0), v_1 + v_2\right\}{% endlatex %}
- {% latex %}\Delta(C) = 3{% endlatex %} (počet jedniček vektoru báze)
- jedná se o {% latex %}(5, 2, 3)-{% endlatex %}kód
- {% latex %}P = \begin{pmatrix} 1 & 1 & 0 & 0 & 0 \\ 0 & 1 & 1 & 1 & 0 \\ 0 & 0 & 0 & 1 & 1 \end{pmatrix}{% endlatex %}

1. {% latex %}\tilde{x} = v_1 = (1\ 1\ 1\ 0\ 0){% endlatex %}, {% latex %}P\tilde{x} = \begin{pmatrix} 0 \\ 0 \\ 0 \end{pmatrix}{% endlatex %} (nulový syndrom, což je správně)
2. {% latex %}\tilde{x} = (0\ 0\ 1\ 0\ 1){% endlatex %}, {% latex %}P\tilde{x} = \begin{pmatrix} 0 \\ 1 \\ 1 \end{pmatrix}{% endlatex %} (nějaký syndrom)
	- podíváme se do tabulky syndromů (vybruteforcená)
	- dostaneme ze syndromu reprezentanta {% latex %}m(s) = (0\ 0\ 0\ 1\ 0){% endlatex %}
	- spočítáme {% latex %}x = \tilde{x} - e = (0\ 0\ 1\ 1\ 1){% endlatex %}
	- protože došlo k chybě v {% latex %}1{% endlatex %} pozici a jedná se o {% latex %}(5, 2, 3){% endlatex %}-kód, {% latex %}x{% endlatex %} je správné dekódování
3. pro {% latex %}\tilde{x} = (0\ 1\ 1\ 0\ 1){% endlatex %} dostáváme váhu syndromu {% latex %}2{% endlatex %} a to už neopravíme

##### Hammingovy kódy
(👀) nechť {% latex %}P{% endlatex %} je kontrolní matice {% latex %}C{% endlatex %}. Pak {% latex %}\Delta(C) = {% endlatex %} maximální {% latex %}d{% endlatex %} t. ž. {% latex %}\forall d - 1{% endlatex %} sloupců {% latex %}P{% endlatex %} je lineárně nezávislých.

**Důkaz:** kódová slova {% latex %}\equiv Pc = 0{% endlatex %}. Nechť sloupce {% latex %}P{% endlatex %} jsou {% latex %}p_1, \ldots, p_n{% endlatex %}. Pak
{% latex display %}\sum_{i = 1}^{n} c_i p_i = 0{% endlatex %}

Pro spor nechť {% latex %}\exists x{% endlatex %} t. ž. {% latex %}\sum x_i p_i = 0{% endlatex %} (je tedy kódové slovo) a {% latex %}w(x) < d \rightarrow{% endlatex %}. To je spor, {% latex %}\Delta(C) = d{% endlatex %} ale tohle slovo má {% latex %}w(x) < d{% endlatex %}. To musí nutně znamenat, že {% latex %}\forall x: w(x) < d \rightarrow \sum_{i = 1}^{n}x_i p_i \neq 0 \rightarrow{% endlatex %} každých {% latex %}\le d - 1{% endlatex %} sloupců je tedy lineárně nezávislých.

**Důsledek:** pokud chci {% latex %}d = 3{% endlatex %}, potřebuji co největší matici {% latex %}P{% endlatex %} t. ž. {% latex %}\forall 2{% endlatex %} sloupce jsou lineárně nezávislé. To v {% latex %}\mathbb{Z}_2{% endlatex %} znamená, že musí být buď stejné, nebo jeden z nich nulový.

{% latex display %}
P = \underbrace{\begin{pmatrix}
	0      & 0      & 0      & \cdots & 1 \\
	\vdots & \vdots & \vdots & \ddots  & 1 \\
	0      & 1      & 1      &        & 1 \\
	1      & 0      & 1      &        & 1
\end{pmatrix}}_{\text{$2^r - 1$ nenulových $r$-dim. vektorů}}
{% endlatex %}

Jedná se o binární zápisy čísel {% latex %}1 \ldots 2^{r} - 1{% endlatex %}. Nechť {% latex %}C{% endlatex %} je generovaný {% latex %}P{% endlatex %} a {% latex %}\mathcal{H}_r = C^\perp{% endlatex %} ({% latex %}P{% endlatex %} je paritní matice {% latex %}\mathcal{H}_r{% endlatex %}). Má délku {% latex %}n = 2^{r} - 1{% endlatex %} a {% latex %}\dim \mathcal{H}_r = n - r = 2^{r} - r - 1{% endlatex %}.

Z pozorování (nezávislé sloupce) dostáváme, že {% latex %}\Delta(\mathcal{H}_r) = 3{% endlatex %}.

**Věta:** pro každé {% latex %}r \ge 2{% endlatex %} je {% latex %}\mathcal{H}_r \left[2^{r} - 1, 2^r - r - 1, 3\right]{% endlatex %}-kód.

### 12. přednáška
- (👀)  {% latex %}G = \left[I_k\ |\ P\right] \implies M = \begin{bmatrix} -P \\ I_{n - k} \end{bmatrix}^T{% endlatex %}

#### Dekódování Hammingova kódu
- předpoklad: {% latex %}e{% endlatex %} má nejvýše {% latex %}1{% endlatex %} jedničku
	- došlo k {% latex %}\le 1{% endlatex %} chybě
- {% latex %}M{% endlatex %} je ve tvaru uvedeném výše (binární zápisy čísel {% latex %}1 \ldots 2^{r} - 1{% endlatex %})
	- pozorování: syndrom {% latex %}M \tilde{x} = Me{% endlatex %} je {% latex %}y_i \equiv{% endlatex %} binární zápis {% latex %}i \iff{% endlatex %} došlo k chybě na pozici {% latex %}i{% endlatex %}

#### Perfektnost kódu
Pokud pro {% latex %}C{% endlatex %} platí {% latex %}\Delta(C) = 2t + 1{% endlatex %}, pak pro každé slovo {% latex %}x \in \mathbb{Z}^n_2{% endlatex %} je nejvýše jedno kódové slovo ve vzdálenosti {% latex %}\le t{% endlatex %} od {% latex %}x{% endlatex %}. jsou to tedy **symetrické koule** se středem {% latex %}x{% endlatex %} a poloměrem {% latex %}t{% endlatex %}, {% latex %}B(x, t) = \left\{z \in \mathbb{Z}_2^n\ |\ d(x, z) \le t\right\}{% endlatex %}; jsou pro různá {% latex %}x \in C{% endlatex %} disjunktní.

**Věta (Hammingův odhad):** pro binární kód s {% latex %}\Delta(C) \ge 2t + 1{% endlatex %} platí {% latex display %}|C| \le \frac{2^n}{V(n, t)} {% endlatex %}
- {% latex %}2^n{% endlatex %} je počet všech slov
- {% latex %}V(n, t){% endlatex %} je objem kombinatorické koule dimenze {% latex %}n{% endlatex %} o poloměru {% latex %}t{% endlatex %} {% latex %}= \sum_{i = 0}^{t} \binom{n}{i}{% endlatex %} (vždy způsoby, jak si vybrat {% latex %}i{% endlatex %} bitů a flipnout je)

**Důkaz:** mám na {% latex %}2^n{% endlatex %} prvcích {% latex %}|C|{% endlatex %} disjunktních koulí objemu {% latex %}V(n, t){% endlatex %}... koule pokrývají {% latex %}|C| \cdot V(n, t){% endlatex %} prvků, což je {% latex %}\le 2^n{% endlatex %} (méně nebo rovno všem prvkům -- nevím, jestli se nepřekrývají) a vydělím.

---

{:.center}
![](/assets/kombinatorika-a-grafy-i/komb-koule.svg)

---

**Definice:** kód {% latex %}C{% endlatex %} je perfektní, pokud pro něj platí Hammingův odhad s rovností.

**Příklady perfektních kódů:**
- totální (koule o poloměru 1)
- opakovací kód liché délky 
- jednoprvkový kód (koule zaplňuje celý prostor)

**Tvrzení:** Hammingův kód je perfektní

**Důkaz:** {% latex %}\mathcal{H}_r = \left[2^r - 1, 2^r - r - 1, 3\right]{% endlatex %}-kód.
- {% latex %}3 = 2t + 1 \implies t = 1, V(n, t) = V(2^r - 1, 1) = 2^r{% endlatex %}
	- poslední rovnost je počet vektorů lišící se v {% latex %}1{% endlatex %} souřadnici, {% latex %}+{% endlatex %} střed koule

- {% latex %}k = \text{dimenze} = 2^r - r - 1{% endlatex %}
- {% latex %}|C| = 2^k = 2^{2^r - r - 1}{% endlatex %}

{% latex display %}\frac{2^n}{V(n, t)} = \frac{2^{2^r - 1}}{2^r} = 2^{2^r - r - 1} = |C|{% endlatex %}

#### Hadamardův kód
- **duál Hammingova kódu** (prohození generující matice s paritní maticí pro Hammingův kód {% latex %}G \longleftrightarrow K{% endlatex %} dává Hadamardův kód)

- {% latex %}x \ldots{% endlatex %} zpráva délky {% latex %}r{% endlatex %}
- {% latex %}c = (c_1, \ldots, c_{2^r - 1}){% endlatex %}
	- {% latex %}c_i = \langle x, y_i \rangle{% endlatex %}, kde {% latex %}y_i{% endlatex %} jsou binární zápisy čísla {% latex %}i{% endlatex %}

**Tvrzení:** Hadamardův kód je {% latex %}\left[2^r, r, 2^{r - 1}\right]{% endlatex %}-kód.

(👀) {% latex %}\langle x, y_i \rangle{% endlatex %} nenese informaci o {% latex %}x_1{% endlatex %}, pokud první bit {% latex %}y{% endlatex %} je {% latex %}0 \implies{% endlatex %} stačí brát {% latex %}y_i, i \in \left(2^{r - 1} , 2^r - 1\right){% endlatex %}
- jedná se o **rozšířený Hadamardův kód** {% latex %}\left[2^r, r + 1, 2^{r - 1}\right]{% endlatex %}

#### Ramseyova teorie

**Motivace:** party o {% latex %}6{% endlatex %} lidech::

{:.center}
![](/assets/kombinatorika-a-grafy-i/ramsey-motivace.svg)

**Věta:** pro každý graf na {% latex %}\ge 6{% endlatex %} vrcholech {% latex %}\exists{% endlatex %} podrgraf {% latex %}E_3{% endlatex %} (prázdný graf) nebo {% latex %}K_3{% endlatex %}.
- {% latex %}\omega(G) \ge 3{% endlatex %} -- velikost maximální kliky
- {% latex %}\alpha(G) \ge 3{% endlatex %} -- velikost maximální nezávislé množiny

{:.rightFloatBox}
![](/assets/kombinatorika-a-grafy-i/ramsey-obr.svg)

**Důkaz:** vyberu libovolný vrchol {% latex %}u{% endlatex %}. Podívám se na vrcholy {% latex %}A{% endlatex %}, se kterými nesousedí, zbytek nechť je {% latex %}B{% endlatex %}.

1. {% latex %}|A| \ge 3, A \supseteq \left\{x, y, z\right\} {% endlatex %}
	- všichni mezi sebou mají hranu, pak máme {% latex %}K_3{% endlatex %}
	- BUNO {% latex %}\exists{% endlatex %} nehrana {% latex %}xy{% endlatex %}, pak {% latex %}\left\{u, x, y\right\}{% endlatex %} tvoří {% latex %}E_3{% endlatex %}
2. symetricky

**Věta (obecnější Ramseyova):** nechť {% latex %}G{% endlatex %} má {% latex %}\ge \binom{k + l - 2}{k - 1}{% endlatex %} vrcholů {% latex %}\implies \omega(G) \ge k{% endlatex %}  nebo {% latex %}\alpha(G) \ge l{% endlatex %}.
- (👀) ze symetrie kombinačních  čísel máme symetrii v {% latex %}k, l{% endlatex %}, protože {% latex %}\binom{k + l - 2}{k - 1} = \binom{k + l - 2}{l - 1}{% endlatex %}

**Důkaz:** indukcí podle {% latex %}k + l{% endlatex %}
- pro {% latex %}k = 1, l = 1{% endlatex %} a {% latex %}k = 2, l = 2{% endlatex %} jednoduché (vždy existuje hrana/nehrana)
- pro {% latex %}k, l \ge 2{% endlatex %} a tvrzení platí pro {% latex %}k, l - 1{% endlatex %} a {% latex %}k-1, l{% endlatex %}
	- {% latex %}n_1 = \binom{k + l - 3}{k - 1}{% endlatex %} a {% latex %}n_2 = \binom{k + l - 3}{l - 1 = k - 2}{% endlatex %} (dřívější odhady)
		- (👀) platí, že {% latex %}n = n_1 + n_2{% endlatex %}

Zvolím {% latex %}u \in G{% endlatex %} libovolně a opět rozdělím graf na sousedy {% latex %}A{% endlatex %} a nesousedy {% latex %}B{% endlatex %} vrcholu {% latex %}u{% endlatex %}. Z principu holubníku ([Dirichletův princip](https://mathworld.wolfram.com/DirichletsBoxPrinciple.html)) je {% latex %}|A| \ge n_1{% endlatex %} nebo  {% latex %}|B| \ge n_2{% endlatex %} (jsou-li ostře menší, tak dají {% latex %}n - 2{% endlatex %}).
1. {% latex %}|A| \ge n_1{% endlatex %}, použiji indukci na {% latex %}A{% endlatex %}:
	- {% latex %}\omega(G[A]) \ge k{% endlatex %} a jsem hotov
	- {% latex %}\alpha(G[A]) \ge l - 1{% endlatex %}, pak tato nezávislá množina spolu s {% latex %}u{% endlatex %} dává nezávislou mnozinu velikosti {% latex %}\ge l{% endlatex %}
2. analogicky: {% latex %}|B| \ge n_2{% endlatex %}, použiji indukci na {% latex %}B{% endlatex %}:
	- {% latex %}\omega(G[A]) \ge l{% endlatex %}, pak tato klika spolu s {% latex %}u{% endlatex %} dává kliku velikosti {% latex %}\ge k{% endlatex %}
	- {% latex %}\alpha(G[A]) \ge l{% endlatex %} a jsem hotov

**Důsledek:** {% latex %}\forall k, l \exists r(k, l){% endlatex %} t. ž. {% latex %}\forall G: \omega(G) \ge k{% endlatex %} nebo {% latex %}\alpha(G) \ge l{% endlatex %}.
- {% latex %}r(k, l) = \mathrm{min}\ N{% endlatex %} t. ž. platí {% latex %}\forall G{% endlatex %} velikosti {% latex %}N{% endlatex %} platí výše uvedené
- podle věty nahoře máme {% latex %}r(k, l) \le \binom{k + l - 2}{k - 1}{% endlatex %}

**Pár hodnot:**
- {% latex %}r(1, l) = 1{% endlatex %}
- {% latex %}r(k, 1) = 1{% endlatex %}
- {% latex %}r(2, l) = l{% endlatex %}
- {% latex %}r(k, 2) = k{% endlatex %}
- dříve jsme dokázali, že {% latex %}r(3, 3) \le 6 {% endlatex %} a z {% latex %}C_5{% endlatex %} víme, že {% latex %}r(3, 3) > 5{% endlatex %}, tedy {% latex %}r(3, 3) = 6{% endlatex %}

**Definice {% latex %}r(k, k){% endlatex %}** symetrické Ramseyovo číslo, říká se mu {% latex %}r(n) = r(n, n){% endlatex %}. „Jak velký musí být graf, abych tam našel buď {% latex %}E_n{% endlatex %} nebo {% latex %}K_n{% endlatex %}“.

**Věta:** {% latex %}k, n \in \mathbb{N}{% endlatex %} t. ž. {% latex %}\binom{n}{k} 2^{1 - \binom{k}{2}} < 1 \implies r(k) > n{% endlatex %}.

Co jsou čísla zač? Použijeme odhad:
- {% latex %}\binom{n}{k} \le \frac{n^k}{k!} < \frac{n^k}{2^{k/2 + 1}}{% endlatex %}

{% latex display %}\binom{n}{k}2^{1 - \binom{k}{2}} < \frac{n^k}{2^{k/2 + 1}} 2^{1 - k(k - 1) / 2} = \left(\frac{n}{2^{k / 2}}\right)^k{% endlatex %}

Kde poslední {% latex %}={% endlatex %} platí, protože:
{% latex display %}\frac{1}{2^{k/2 + 1}} 2^{1 - k(k - 1)/2} = \frac{1}{2 \cdot 2^{k/2}} \frac{2}{2^{k(k - 1)/2}} = \frac{1}{2^{k/2 (1 + k - 1)}} = \left(\frac{1}{2^{k/2}}\right){% endlatex %}

**Důsledek:** {% latex %}\forall k \ge 3: r(k) > 2^{k/2}{% endlatex %}
- dosadíme {% latex %}n = 2^{k/2}{% endlatex %} do předchozího (předchozí je ostrý odhad, takže {% latex %}1^k < 1{% endlatex %} funguje)

**Důkaz:** vezmu náhodný graf {% latex %}G{% endlatex %} t. ž. každá z {% latex %}\binom{n}{2}{% endlatex %} má pravděpodobnost {% latex %}1/2{% endlatex %}, nezávisle na ostatních. Nechť {% latex %}K \subseteq V, |K| = k{% endlatex %}. {% latex %}A_K \ldots{% endlatex %} jev, že {% latex %}G[K]{% endlatex %} je klika. {% latex %}\Pr[A_K] = \left(\frac{1}{2}\right)^{\binom{k}{2}} = 2^{-\binom{k}{2}}{% endlatex %}. Obdobně {% latex %}B_K{% endlatex %} jev, že vznikla nezávislá množina a {% latex %}C_K \ldots A_K \cup B_K \ldots \Pr[C_K] = 2 \cdot 2^{-\binom{k}{2}} = 2^{1 - \binom{k}{2}}{% endlatex %}. {% latex %}p \ldots{% endlatex %} pravděpodobnost, že {% latex %}\exists K \subseteq V{% endlatex %} t. ž. nastal jev {% latex %}C_K{% endlatex %}. Je ji těžké určit, protože jevy nejsou nezavislé (množiny se mohou překrývat), nám ale stačí odhad který předpokládá, že jsou jevy nezávislé:

{% latex display %}\Pr[C] \le \sum_{K \in V, |K| = k} \Pr[C_K] = \binom{n}{k} \cdot 2^{1 - \binom{k}{s}} < 1{% endlatex %}
- předposlední rovnost je z definice -- všechny možné {% latex %}K{% endlatex %}-tice
- poslední rovnost je předpoklad věty
- máme, že pravděpodobnost, že nějaká {% latex %}K{% endlatex %}-prvková množina bude tvořit buďto kliku nebo nezávislou množinu velikosti {% latex %}k{% endlatex %} je {% latex %}< 1{% endlatex %}, tedy pravděpodobnost, že to nenastane je {% latex %}> 0{% endlatex %}, tedy {% latex %}\exists{% endlatex %} nějaký z náhodných grafů, který tohle nesplňuje
	- pokud pravděpodobnost je nenulová, tak musí existovat nějaké množství grafů, které tenhle jev mají (protože jinak by nerovnost nebyla ostrá

{:.rightFloatBox}
<div markdown="1">
Díky Matěji Kripnerovi za PR!
</div>

**Jiný důkaz:**
Někomu může použití pravděpodobnosti připadat trochu magické.
Důkaz lze ale přeformulovat explicitněji.

Uvažme všechny grafy na {% latex %}n{% endlatex %} vrcholech. Těch je {% latex %}2^{\binom{n}{2}}{% endlatex %}.
Kolik z nich obsahuje kliku nebo nezávislou množinu velikosti alespoň {% latex %}k{% endlatex %}? Tedy,
kolik z nich je "dobrých"?
Začněme jednodušeji -- označme množinu vrcholů {% latex %}V{% endlatex %} a mějme {% latex %}K \subseteq V, |K| = k{% endlatex %}.
V kolika grafech tvoří {% latex %}K{% endlatex %} kliku? Hrany uvnitř {% latex %}K{% endlatex %} jsou fixované, ostatní můžeme nastavovat libovolně.
Odpověď je tedy {% latex %}2^{\binom{n}{2}-\binom{k}{2}}{% endlatex %}. Případ nezávislé množiny je
symetrický, tudíž v {% latex %}2 \, 2^{\binom{n}{2}-\binom{k}{2}} = 2^{\binom{n}{2}-\binom{k}{2}+1}{% endlatex %} grafech
bude {% latex %}K{% endlatex %} klika nebo nezávislá množina.

Nyní zásadní krok: V součtu {% latex %}\binom{n}{k} 2^{\binom{n}{2}-\binom{k}{2}+1}{% endlatex %} přes všechny takové
množiny {% latex %}K{% endlatex %} jsme započítali každý dobrý graf (nejspíše vícekrát, ale to nevadí). Každý dobrý
graf totiž obsahuje kliku nebo nezávislou množinu velikosti **přesně** {% latex %}k{% endlatex %}.
Tento součet je tedy horní mezí pro počet dobrých grafů.

A jsme hotovi. Předpoklad věty je totiž po přenásobení ekvivalentní nerovnosti:

{% latex display %}\binom{n}{k} 2^{\binom{n}{2}-\binom{k}{2}+1} < 2^\binom{n}{2}{% endlatex %}

A z té díky našemu odhadu tranzitivně plyne, že počet dobrých grafů je menší než počet všech grafů. Tedy
existuje nedobrý graf na {% latex %}n{% endlatex %} vrcholech a {% latex %}r(k,k) > n{% endlatex %}.

### 13. přednáška

#### Ramseyovy barevné/nekonečné věty

{:.rightFloatBox}
<div markdown="1">
„Pokud mám alespoň {% latex %}\ge N{% endlatex %} prvků a dávám je do {% latex %}t{% endlatex %} holubníků, pak bude existovat holubník s alespoň {% latex %}k{% endlatex %} prvky.“
</div>

**Věta (princip holubníku):** pro každé {% latex %}t, k \in \mathbb{N} \exists N{% endlatex %} t. ž. {% latex %}\forall c: [n] \mapsto [t]{% endlatex %} platí, že {% latex %}\forall n \ge N \exists A \subseteq [n]{% endlatex %}, na níž je funkce {% latex %}c{% endlatex %} konstantní.

**Důkaz:** {% latex %}N = t (k - 1) + 1{% endlatex %}.

**Věta (nekonečný princip holubníku):** pro každé {% latex %}t \in \mathbb{N}{% endlatex %} a každé {% latex %}c: \mathbb{N} \mapsto [t]{% endlatex %} existuje nekonečná množina {% latex %}A \subseteq \mathbb{N}{% endlatex %}, pro níž je funkce {% latex %}c{% endlatex %} konstantní.
- z „existuje holubník s hodně holuby“ máme „existuje holubník s nekonečně holuby“

**Důkaz:** rozdělím {% latex %}\mathbb{N}{% endlatex %} na {% latex %}B_1, \ldots, B_t{% endlatex %}, kde {% latex %}B_i = \left\{m \in \mathbb{N}\ |\ c(m) = i\right\}{% endlatex %}. Protože sjednocením je nekonečná množina pak alespoň jedna musí být nekonečná.

**Věta (nekonečná Ramseyova (vícebarevná) věta):** pro každé {% latex %}t \in \mathbb{N}, \forall c: \binom{\mathbb{N}}{2} \mapsto [t] \exists{% endlatex %} nekonečna množina {% latex %}A \subseteq \mathbb{N}{% endlatex %}, pro níž je funkce {% latex %}c{% endlatex %} na hranách {% latex %}\binom{A}{2}{% endlatex %} (nekonečný úplný graf) konstantní.

{:.rightFloatBox}
<div markdown="1">
sanity check: {% latex %}A_1 \supset A_2 \supset \ldots {% endlatex %}
</div>

**Důkaz:** sestrojím posloupnost nekonečných množin {% latex %}A_1 = \mathbb{N}, \ldots{% endlatex %} a pro {% latex %}i = 1, 2, \ldots{% endlatex %} opakujeme:
- vybereme {% latex %}v_i \in A_i{% endlatex %}
- rozdělíme {% latex %}A{% endlatex %} na {% latex %}B_i^1, B_i^2\ldots, B_i^t{% endlatex %} podle toho, jakou barvu má hrana, která množinu spojuje s {% latex %}v_i{% endlatex %}
	- jelikož {% latex %}A_i{% endlatex %} je nekonečná, tak {% latex %}\exists B_i^j{% endlatex %} pro nějakou barvu, která je také nekonečná
- položme {% latex %}A_{i + 1} = B_i^j{% endlatex %}

(👀) posloupnost vrcholů {% latex %}v_1, v_2, \ldots{% endlatex %} má vlastnost, že pokud {% latex %}i < j{% endlatex %}, pak {% latex %}\left\{v_i, v_j\right\}{% endlatex %} má barvu {% latex %}b_i{% endlatex %}
- v každém kroku se zanořuju, ale při zanoření už platí, že všichni sousedi jsou k {% latex %}v_i{% endlatex %} spojeni hranou dané barvy
- {% latex %}\implies{% endlatex %} barva hrany {% latex %}\left\{v_i, v_j\right\}{% endlatex %} závisí pouze na {% latex %}i{% endlatex %}, ne na {% latex %}j{% endlatex %}
- mám posloupnost barev {% latex %}b_1, b_2, b_3, \ldots{% endlatex %}
	- je nekonečná, ale opakuje se tu konečně mnoho hodnot
	- aplikuji nekonečný holubník {% latex %}\implies \exists j \in [t]{% endlatex %} opakující-se nekonečněkrát a takové vrcholy vyberu, jednota barev vychází z pozorování

{:.rightFloatBox}
<div markdown="1">
„Pokud {% latex %}n \ge N{% endlatex %}, tak každé obarvení {% latex %}K_n{% endlatex %} {% latex %}t{% endlatex %} barvami obsahuje jednobarevný {% latex %}K_k{% endlatex %} jako podgraf.“
</div>

**Věta (Ramseyova vícebarevná věta):** {% latex %}\forall t, k \in \mathbb{N}{% endlatex %} ({% latex %}t{% endlatex %} počet barev, {% latex %}k{% endlatex %} velikost kliky) {% latex %}\exists N \in \mathbb{N}{% endlatex %} t. ž. {% latex %}\forall c: \binom{[n]}{2} \mapsto [t], \forall n \ge N{% endlatex %} (obarvení {% latex %}K_n{% endlatex %} {% latex %}t{% endlatex %} barvami) existuje množina {% latex %}A \subseteq [n], |A| = k{% endlatex %}, pro níž je funkce {% latex %}c{% endlatex %} na {% latex %}\binom{A}{2}{% endlatex %} konstantní.


**Důkaz:** adaptujeme nekonečný na konečný případ -- chtěli bychom posloupnost barev {% latex %}b_1, \ldots, b_{tk}{% endlatex %} -- když do toho praštíme holubníkem, tak máme barvu, která je tam {% latex %}k{% endlatex %}-krát. 
- upravím konstrukci množin {% latex %}A_i{% endlatex %}: beru vždy největší třídu
	- {% latex %}|A_{i + 1}| \ge \frac{|A_i| - 1}{t}{% endlatex %} (max. je větší/roven průměru)
	- potřebuji, aby konstrukce běžela alespoň {% latex %}tk{% endlatex %} kroků
	- potřebuji, aby {% latex %}|A_{tk}| \ge 1, |A_{tk - 1}| \ge t + 1, \ldots, |A_1| \ge \sum_{i = 0}^{tk} t^i = \frac{t^{tk + 1} - 1}{t - 1}{% endlatex %}
		- na zkoušce nebude -- jen bychom měli vědět, že se to takhle dá umlátit

**Definice (hypergraf)** je zobecněný graf, kde:
- hrany jsou libovolné množiny (místo dvojic, jako v normálním grafu)
- **uniformní** hypergraf -- hrany jsou {% latex %}p{% endlatex %}-prvkové množiny
- {% latex %}p{% endlatex %} je arita hran (velikost množin), {% latex %}t, k{% endlatex %} jsou stejné


**Věta (nekonečná Ramseyova věta pro {% latex %}p{% endlatex %}-tice):** {% latex %}\forall p, t \in \mathbb{N}{% endlatex %} a {% latex %}\forall c: \binom{\mathbb{N}}{p} \mapsto [t] \exists A \subseteq \mathbb{N}{% endlatex %} nekonečná t. ž. {% latex %}c{% endlatex %} je na {% latex %}\binom{A}{p}{% endlatex %} konstantní.

**Důkaz:** indukcí podle {% latex %}p{% endlatex %}, pro {% latex %}p=1{% endlatex %} je to nekonečný holubník (pro {% latex %}p = 2{% endlatex %} je to Ramsey)
- IP: věta platí pro {% latex %}p - 1{% endlatex %}
- opět konstruuji nekonečnou posloupnost {% latex %}A_i{% endlatex %}
- v kroku {% latex %}i{% endlatex %} vyberu {% latex %}v_i \in A_i{% endlatex %}, nechť {% latex %}A_i' = A_i \setminus \left\{v_i\right\}{% endlatex %}

{:.rightFloatBox}
<div markdown="1">
Pomocné obarvení {% latex %}(p-1){% endlatex %}-tic stejnými barvami, jako byla {% latex %}p{% endlatex %}-tice s vrcholem {% latex %}v_i{% endlatex %}.
</div>

- definuji obarvení {% latex %}(p - 1){% endlatex %}-tic {% latex %}A_i'{% endlatex %} {% latex %}c_i'(Q) = c(Q \cup \left\{v_i\right\}){% endlatex %}, {% latex %}Q \subseteq A_i'{% endlatex %}, {% latex %}|Q| = p - 1{% endlatex %}
- z IP pro {% latex %}A_i'{% endlatex %} máme, že {% latex %}\exists B_i \subseteq A_i'{% endlatex %}, na jejichž {% latex %}(p-1){% endlatex %}-ticích je obarvení {% latex %}c_i'{% endlatex %} konstantní {% latex %} = b_i \in [t]{% endlatex %} a {% latex %}A_{i + 1} = B_i{% endlatex %} si vezmu do dalšího kroku

(👀) barva {% latex %}p{% endlatex %}-tice {% latex %}\left\{v_{i_1}, \ldots, v_{i_p}\right\}{% endlatex %} (vzhledem k vzniklé posloupnosti {% latex %}v_1, v_2, \ldots{% endlatex %}), kde {% latex %}i_1 < i_2 < i_3 < i_p{% endlatex %} závisí pouze na barvě prvku {% latex %}v_{i_1}{% endlatex %}
- vyberu z barev nějakou opakující-se nekonečněkrát a vrcholy s příslušnými indexy tvoří {% latex %}A{% endlatex %}

**Věta (Ramseyova věta pro {% latex %}p{% endlatex %}-tice):** {% latex %}\forall p, t, k \in \mathbb{N} \exists N \in \mathbb{N}{% endlatex %} t. ž. {% latex %}\forall n \ge N \exists A \subseteq [n], |A| = k{% endlatex %} t. ž. {% latex %}c{% endlatex %} je konstantní na {% latex %}\binom{A}{p}{% endlatex %}.

**Důkaz:** mějme {% latex %}p, k, t{% endlatex %} z předpokladu věty. Uvážíme {% latex %}c_i: \binom{[n]}{p} \mapsto [t]{% endlatex %}. To je _dobré_, pokud {% latex %}\exists {% endlatex %} {% latex %}k{% endlatex %}-prvková jednobarevná podmnožina, jinak je _špatné_. Věta tedy tvrdí, že {% latex %}n \ge N{% endlatex %} jsou všechna {% latex %}c{% endlatex %} _dobrá_.

Sporem: předpokládejme, že pro nekonečně mnoho {% latex %}n \exists{% endlatex %} _špatné_ obarvení.

(👀) Pokud {% latex %}S_n{% endlatex %} je množina _špatných_ obarvení a {% latex %}S_n{% endlatex %} je neprázdné, pak {% latex %}S_{n - 1}{% endlatex %} je neprázdné, protože mám-li _špatné_ obarvení {% latex %}p{% endlatex %}-tic nad {% latex %}n{% endlatex %}, tak mohu zapomenout na {% latex %}n{% endlatex %}-tý prvek a tak dostanu _špatné_ obarvení i na {% latex %}n - 1{% endlatex %}.
- **zůžení** {% latex %}z(c)(Q) = c(Q), Q \subseteq [n - 1], |Q| = p{% endlatex %} (prostě odeberu vrchol)

Strukturu _špatných_ obarvení popíšeme stromem, kde hladiny jsou obarvení {% latex %}S_n{% endlatex %}; platí:
- všechny hladiny jsou neprázdné (předpoklad pro spor)
- všechny hladiny jsou konečné (nad {% latex %}S_n{% endlatex %} může být only so much obarvení)

**Lemma (Königovo):** nekonečný zakořeněný strom s konečnými stupni obsahuje nekonečnou cestu z kořene.

**Důkaz:** pokud máme vrcholy {% latex %}v_1, v_2, \ldots, v_{i - 1}{% endlatex %} na cestě, tak {% latex %}v_i{% endlatex %} vezmu jako kořen podstromu, který je nekonečný a opakuju.

Díky tomuto lemmatu víme, že {% latex %}\exists{% endlatex %} nekonečná cesta z {% latex %}S_0{% endlatex %}. Z nekonečné Ramseyovy věty ale víme, že kdyby tomu tak bylo, tak neplatí, protože by existovalo nekonečné obarvení přirozených čísel (podle nekonečné cesty v tomto stromu).

### [Forma zkoušky](/assets/kombinatorika-a-grafy-i/okruhy_kg1.pdf)

### Zdroje
- [https://research.koutecky.name/db/teaching:kg12021_prednaska](https://research.koutecky.name/db/teaching:kg12021_prednaska) -- stránka cvičení
	- odkaz na všechny obrázky, zdroje, nahrávky cvičení
- [https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols](https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols) -- {% latex %}\LaTeX{% endlatex %}ové matematické symboly
