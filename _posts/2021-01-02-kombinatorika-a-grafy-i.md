---
language: cz
title: Kombinatorika a Grafy I
category: "lecture notes"
---

- .
{:toc}

### 1. přednáška

#### Odhady faktoriálu

**Věta (meh odhad):**
{% latex display %}n^{n/2} \le n! \le \left(\frac{n + 1}{2}\right)^n{% endlatex %}

**Důkaz $$\ge$$:**
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
{% latex %}\frac{2^{2m}}{2 \sqrt{m}} \le \binom{2m}{m} \le \frac{2^{2m}}{\sqrt{2m}}{% endlatex %}

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

#### Náhodné procházky (v {% latex %}\mathbb{Z}^1{% endlatex %})

**Definice náhodné procházky:** Náhodný proces, v každém kroku se panáček z bodu {% latex %}0{% endlatex %} posune doprava nebo doleva.

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
	              &= \sum_{i=1}^{\infty} \frac{1}{2 \sqrt{i}} && //\  \text{diverguje} \\
\end{aligned}
{% endlatex %}

- zajímavost: ve {% latex %}2D{% endlatex %} to také platí, ale ve {% latex %}3D{% endlatex %} už ne!

#### Generující funkce

**Definice (Mocninná řada):** nekonečná řada tvaru {% latex %}a(x) = a_0 + a_1x^1 + a_2x^2 + \ldots{% endlatex %}, kde {% latex %}a_0, a_1 \ldots \in \mathbb{R}{% endlatex %}.

**Příklad:** {% latex %}a_0 = a_1 = \ldots = 1 \mapsto 1 +x + x^2 + \ldots{% endlatex %}.
- pro {% latex %}|x| < 1{% endlatex %} řada konverguje k {% latex %}\frac{1}{1 - x}{% endlatex %}, můžeme tedy říct, že {% latex %}(1, 1, \ldots) \approx \frac{1}{1 - x}{% endlatex %}

**Tvrzení:** {% latex %}(a_0, a_1, a_2, \ldots){% endlatex %} reálná čísla. Předpoklad: pro nějaké {% latex %}K{% endlatex %} t. ž. {% latex %}|a_n| \le K^n{% endlatex %}. Poté řada {% latex %}a(x){% endlatex %} pro každé {% latex %}x \in \left(-\frac{1}{K}, \frac{1}{K}\right) {% endlatex %} konverguje (dává smysl). Funkce {% latex %}a(x){% endlatex %} je navíc jednoznačně určena hodnotami na okolí {% latex %}0{% endlatex %}.

**Definice (Vytvořující funkce):** nechť {% latex %}\left(a_0, a_1, \ldots\right){% endlatex %} je posloupnost reálných čísel. **Vytvořující funkce** této posloupnosti je mocninná řada {% latex %}a(x) = \sum_{i = 0}^{\infty} a_i x^i{% endlatex %}.
- také se jim někdy říká generující

##### Operace na funkcích

| operace                                      | řada                                                                                                                          | úprava                                               |
| ---                                          | ---                                                                                                                           | ---                                                  |
| součet                                       | {% latex %}a_0 + b_0, a_1 + b_1, a_2 + b_2, \ldots{% endlatex %}                                                              | {% latex %}a(x) + b(x){% endlatex %}                 |
| násobek                                      | {% latex %}\alpha a_0, \alpha a_1, \alpha a_2, \ldots {% endlatex %}                                                          | {% latex %}\alpha a(x){% endlatex %}                 |
| posun doprava                                | {% latex %}0, a_0, a_1, \ldots {% endlatex %}                                                                                 | {% latex %} \alpha xa(x){% endlatex %}               |
| posun doleva                                 | {% latex %}a_1, a_2, a_3, \ldots {% endlatex %}                                                                               | {% latex %}\alpha \frac{a(x) - a_0}{x}{% endlatex %} |
| substituce {% latex %}\alpha x{% endlatex %} | {% latex %}a_0, \alpha a_1, \alpha^2 a_2, \ldots {% endlatex %}                                                               | {% latex %} \alpha a(\alpha x){% endlatex %}         |
| substituce {% latex %}x^n{% endlatex %}      | {% latex %}a_0, 0, \overset{n - 1}{\ldots}, 0, a_1, 0, \overset{n - 1}{\ldots}, 0, a_2, \ldots {% endlatex %}                 | {% latex %} \alpha a(x^n){% endlatex %}              |
| derivace                                     | {% latex %}a_1, 2a_1, 3a_2, \ldots {% endlatex %}                                                                             | {% latex %} \alpha a'(x){% endlatex %}               |
| integrování                                  | {% latex %}0, a_1, a_2/2, a_3/3, \ldots {% endlatex %}                                                                        | {% latex %} \int_{0}^{x} a(t) dt{% endlatex %}       |

Všechny důkazy jsou jednoduché rozepsání z definice.

#### Zobecněná binomická věta

**Tvrzení:** {% latex %}r \in \mathbb{R}, k \in \mathbb{N}{% endlatex %}, def. {% latex %}\binom{r}{k} = \frac{r \cdot (r - 1) \cdot (r - 2) \cdot  \ldots  \cdot (r - k + 1)}{k!}{% endlatex %}
- pro {% latex %}r \in \mathbb{N}{% endlatex %} se shoduje s tím, co už známe
- vyplývá z toho, že funkce {% latex %}(1 + x)^r{% endlatex %} je vytvořující funkcí posloupnosti {% latex %}\left(\binom{r}{0}, \binom{r}{1}, \binom{r}{2}, \ldots\right){% endlatex %}
- (👀) pokud {% latex %}r{% endlatex %} je záporné celé, pak {% latex %}\binom{r}{k} = (-1)^k \binom{-r + k - 1}{k} = (-1)^k \binom{-r + k - 1}{-r - 1}{% endlatex %}, tedy {% latex %}\frac{1}{(1 - x)^n} = (1 - x)^{-n} = \binom{n - 1}{n - 1} + \binom{n}{n - 1}x + \binom{n + 1}{n - 1}x^2 + \ldots{% endlatex %}

**Příklad:** V krabici je {% latex %}30{% endlatex %} červených, {% latex %}40{% endlatex %} žlutých a {% latex %}50{% endlatex %} zelených míčků. Kolika způsoby lze vybrat {% latex %}70{% endlatex %}?

**Řešení:** 

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
