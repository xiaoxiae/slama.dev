---
date: '2022-05-20'
title: Best-SAT
pdf: true
description: Expanded translation of my lecture notes from a Randomized and Approximation
  Algorithms course that I took, and a more detailed explanation of the topics covered
  in my video about BEST-SAT.
---


This post is an expanded translation of [my lecture notes](https://slama.dev/poznamky/aproximacni-algoritmy/) from a Randomized and Approximation Algorithms course that I took, and a more detailed explanation of the topics covered in my **[video about BEST-SAT](https://www.youtube.com/watch?v=OV82ab-C85w).**

### Basic definitions

{{% float_box %}}
An example problem could be minimum spanning trees:

- **input instances:** _set of all weighted graphs_
- **permissible inputs:** _spanning trees for the given weighted graph_
- **utility function:** _the spanning tree weight (sum of its edges)_
- we're **minimizing**
{{% /float_box %}}

{{< math "definition:" "Optimization problem" >}} is a tuple \(\mathcal{I}, \mathcal{F}, f, g\)
- set of all **input instances** \(\mathcal{I}\)
- sets of **permissible inputs** \(\forall I \in \mathcal{I}: \mathcal{F}(I)\)
- **utility function** \(\forall I \in \mathcal{I}, A \in \mathcal{F}(I): f(I, A)\)
- whether we're **maximizing** or **minimizing** (a single bit \(g\))
{{< /math >}}

{{< math "definition:" "NP-Optimization problem" >}} is an optimization problem \(\mathcal{I}, \mathcal{F}, f, g\), for which we additionally require that:
- the length of all permissible solutions is polynomial
- the language of \((I, A), I \in \mathcal{I}, A \in \mathcal{F}(I)\) is polynomial
	- _we can check the correctness of a solution in polynomial time_
- \(f\) is computable in polynomial time
{{< /math >}}

{{% float_box %}}
_For minimization problem, we ensure that the solution is always small enough._

_For maximization problem, we ensure that the solution is always large enough._
{{% /float_box %}}

{{< math "definition" >}}algorithm \(A\) is \(R\)-approximation, if:
- it computes the solution in polynomial time (in terms of \(|I|\))
- for minimization problem: \(\forall I: f(A) \le R \cdot \mathrm{OPT}(I)\)
- for maximization problem: \(\forall I: f(A) \ge \mathrm{OPT}(I) / R\)
{{< /math >}}

### MAX-SAT
- _Input:_ \(C_1 \land \ldots \land C_n\), each clause is a disjunction of \(k_j \ge 1\) literals
- _Output:_ evaluation \(a \in \left\{0, 1\right\}^n\) of the variables (sometimes called literals)
- _Goal:_ maximize the number of satisfied clauses \(\sum w_j\)

We also assume that:
- no literal repeats in a clause
- at most one of \(x_i, \overline{x}_i\) appears in a clause

### RAND-SAT
{{< math "algorithm" "RAND-SAT" >}}
1. choose all literals randomly (independently, for \(p = 1/2\))
2. profit?
{{< /math >}}

{{< math "theorem" >}}RAND-SAT is a \(2\)-approximation algorithm.{{< /math >}}

{{< math "proof" >}}we'll create an indicator variable \(Y_j\) for each clause
- the chance that \(C_j\) is not satisfied is \(\frac{1}{2^k}\)

Since the size of the clause \(k \ge 1\), we get \(\mathbb{E}\left[Y_j\right] = \mathrm{Pr}\left[C_j\ \text{is satistied}\right] = 1 - \frac{1}{2^k} \ge \frac{1}{2} \), thus
\[\mathbb{E}\left[\sum_{j = 1}^{n} Y_j\right] \overset{\text{linearity} \atop \text{of expectation}}{=} \sum_{j = 1}^{n} \mathbb{E}\left[Y_j\right] \ge \sum_{j = 1}^{n}\frac{1}{2} \ge \frac{1}{2}\mathrm{OPT} \]
{{< /math >}}

### LP-SAT

{{% float_box %}}
We're using the optimal solution to the linear program (and generally the formula, if we allow real values for literals) as a guide for our randomized algorithm.
{{% /float_box %}}

{{< math "algorithm" "LP-SAT" >}}
1. build an integer linear program:
	- variables will be:
		- \(y_i\) for _each literal_
		- \(z_j\) for _each clause_
	- inequalitites will be one for _each clause,_ in the form \[z_j \le \sum_{\text{positive}} y_i + \sum_{\text{negative}} (1 - y_i)\]
	- we'll _maximize_  the number of satisfied clauses \(\sum z_j\)
3. relax the program (allow real variables instead of integers) and calculate the optimum \(y^*, z^*\)
4. set literals \(x_i\) to \(1\) with probability \(y_i^*\)
{{< /math >}}

{{< math "theorem" >}}LP-SAT is a \(\left(1 - \frac{1}{e}\right)\)-approximation algorithm.{{< /math >}}

To prove this, we'll use a few lemmas/theorems that aren't difficult to prove, but aren't really interesting. I left links to (Wikipedia _and I don't feel bad about it_) articles with proofs for each, if you're interested.

---

{{< math "fact" "A - A/G mean inequality" >}} \[\prod_{i = 1}^{n} a_i^{\frac{1}{n}} \le \frac{1}{n} \sum_{i = 1}^{n} a_i\]{{< /math >}}

{{< math "proof" >}} [https://en.wikipedia.org/wiki/Inequality_of_arithmetic_and_geometric_means](https://en.wikipedia.org/wiki/Inequality_of_arithmetic_and_geometric_means)
{{< /math >}}


{{< math "fact" "B - Jensen's inequality" >}}if a function is concave on the interval \(\left[0, 1\right]\) and \(f(0) = a, f(1) = a + b\), then \[\forall x \in \left[0, 1\right]: f(x) \ge a + bx\]{{< /math >}}

{{< math "proof" >}} [https://en.wikipedia.org/wiki/Jensen%27s_inequality](https://en.wikipedia.org/wiki/Jensen%27s_inequality)
{{< /math >}}


{{< math "fact" "C - 1/e inequality" >}}\[\left(1 - \frac{1}{n}\right)^n \le \frac{1}{e}\]{{< /math >}}

{{< math "proof" >}} [https://en.wikipedia.org/wiki/E_(mathematical_constant)#Inequalities](https://en.wikipedia.org/wiki/E_(mathematical_constant)#Inequalities)
{{< /math >}}

---

{{< math "proof" "of the main theorem" >}} consider \(y^*, z^*\) and \(C_j\) with \(k_j\) literals; then

\[
\begin{aligned}
	\mathrm{Pr}\left[C_j\ \text{is not satisfied}\right] &= \overbrace{\prod_{i:\ x_i \in C_j} (1 - y^*_i)}^{\text{positive}} \overbrace{\prod_{i:\ \overline{x}_i \in C_j} y^*_i}^{\text{negative}} & \\
	&\overset{A}{\le} \left[\frac{1}{k_j} \left(\sum_{i:\ x_i \in C_j} (1 - y^*_i) + \sum_{i:\ \overline{x}_i \in C_j} y^*_i\right)\right]^{k_j} & \\
	&= \left[1 - \frac{1}{k_j} \left(\sum_{i:\ x_i \in C_j} y^*_i + \sum_{i:\ \overline{x}_i \in C_j} (1 - y^*_i)\right)\right]^{k_j} & \\
	&\le \left(1 - \frac{z_j^*}{k_j}\right)^{k_j}
\end{aligned}
\]

We're interested in the satisfied ones, so
\[
\begin{aligned}
	\mathrm{Pr}\left[C_j\ \text{is satisfied}\right] &\ge \overbrace{1 - \left(1 - \frac{z_j^*}{k_j}\right)^{k_j}}^{\text{our function}\ f(z_j^*)} \\
	& \overset{B}{\ge} \left[1 - \left(1 - \frac{1}{k_j}\right)^{k_j}\right] z_j^*
	& \overset{C}{\ge} \left(1 - \frac{1}{e}\right) z_j^*
\end{aligned}
\]

To use fact \(B\), we observed that \(a = f(0) = 0\) and that the second derivative is non-positive (so the function is concave). Now to formally count how many our program satisfies:
\[
\begin{aligned}
	\mathbb{E}\left[\sum_{j = 1}^{m} Y_j\right] &= \sum_{j = 1}^{m} \mathbb{E}\left[Y_j\right] \\
	&\ge \sum_{j \in U} \mathrm{Pr}\left[C_j\ \text{is satisfied}\right] \\
	&\ge \sum_{j \in U} \left(1 - \frac{1}{e}\right) z_j^* \\
	&= \left(1 - \frac{1}{e}\right) \mathrm{OPT}\\
\end{aligned}
\]
{{< /math >}}

### BEST-SAT
{{< math "algorithm" "BEST-SAT" >}}
1. assign a value of a literal using RAND-SAT with probability \(1/2\), else use BEST-SAT
2. have an existential crisis about the fact that this works and is asymptotically optimal
{{< /math >}}

{{< math "theorem" >}}BEST-SAT is \(\frac{3}{4}\)-approximation.{{< /math >}}

{{< math "proof" >}} we want to prove that \( \mathrm{Pr}\left[C_j\ \text{is satisfied}\right] \ge \frac{3}{4} z^*_j \).

Let's look at the probability that each algorithm satisfies a clause of \(k\) variables:
- RAND-SAT: \(1 - \frac{1}{2^k}\) (at least one literal must be satisfied)
- LP-SAT: \(\left[1 - \left(1 - \frac{1}{k}\right)^{k}\right] z_j^*\) (the formula right before using fact C)

Now the proof boils down to the following table:

| \(k_j\) | RAND-SAT                              | LP-SAT                                       | BEST-SAT                                                              |
| ---     | ---                                   | ---                                          | ---                                                                   |
| \(1\)   | \(\frac{1}{2} \ge \frac{1}{2} z_j^*\) | \(1 \cdot z_j^*\)                            | \(\frac{1}{2} \frac{1}{2} + \frac{1}{2} z_j^* \ge \frac{3}{4} z_j^*\) |
| \(2\)   | \(\ge \frac{3}{4} z_j^*\)             | \(\frac{3}{4} \cdot z_j^*\)                  | \(\ge \frac{3}{4} z_j^*\)                                             |
| \(\ge3\)   | \(\ge \frac{7}{8} z_j^*\)             | \(\ge\left(1 - \frac{1}{e}\right) \cdot z_j^*\) | \(> \frac{3}{4} z_j^*\)                                               |
{{< /math >}}
