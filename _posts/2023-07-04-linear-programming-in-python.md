---
title: Linear Programming in Python
category: YouTube
category_icon: /assets/category-icons/youtube.svg
end: "<a href='/linearni-programovani-v-pythonu'>Česká verze článku</a>"
excerpt: This post contains additional materials to my newly released video about linear programming, namely a number of practical examples of how it can be used to solve a variety of problems using Python and its `pulp` package.
---

- .
{:toc}

### Introduction
This post contains additional materials to my **[newly released video](https://youtu.be/E72DWgKP_1Y)** about linear programming, namely a number of practical examples of how it can be used to solve a variety of problems using Python and its `pulp` package.

### Practical examples

#### Farmer's problem
With the planting season steadily approaching, your farmer friend presents you with the following problem.

You have \(3\) tons of potato seeds and \(4\) tons of carrot seeds.
To grow the crops efficiently, you also have \(5\) tons of fertilizer, which has to be used when planting in a \(1:1\) ratio (i.e. \(1\) kilogram of potatoes or carrots requires \(1\) kilogram of fertilizer).
The profit is \(1.2\$/\mathrm{kg}\) for potato seeds and \(1.7\$/\mathrm{kg}\) for carrot seeds.

How much potatoes and carrots should you plant to maximize your profit this season?

<details>
	<summary class="code-summary">Source code</summary>
	<div markdown="1">
```py
{% include linear-programming-in-python/farmer.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Output</summary>
	<div markdown="1">
```
{% include linear-programming-in-python/farmer.out %}```
</div>
</details>

#### [Knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem)
Given \(n\) items, each with weight \(w_i\) and price \(p_i\), our task is to maximize the price of the items we take into our backpack without exceeding its carry weight \(M\).

<details>
	<summary class="code-summary">Source code</summary>
	<div markdown="1">
```py
{% include linear-programming-in-python/knapsack.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Output</summary>
	<div markdown="1">
```
{% include linear-programming-in-python/knapsack.out %}```
</div>
</details>

#### [Graph coloring](https://en.wikipedia.org/wiki/Graph_coloring)

We want to find a minimal \(k\) such that a graph \(G\) is [vertex \(k\)-colorable](https://en.wikipedia.org/wiki/Graph_coloring).

<details>
	<summary class="code-summary">Source code</summary>
	<div markdown="1">
```py
{% include linear-programming-in-python/vertex-coloring.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Output</summary>
	<div markdown="1">
```
{% include linear-programming-in-python/vertex-coloring.out %}```
</div>
</details>

#### [Traveling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem)
Given a weighted oriented graph \(G\), we want to find the longest Hamiltonian cycle.

<details>
	<summary class="code-summary">Source code</summary>
	<div markdown="1">
```py
{% include linear-programming-in-python/tsp.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Output</summary>
	<div markdown="1">
```
{% include linear-programming-in-python/tsp.out %}```
</div>
</details>

#### [Bin packing](https://en.wikipedia.org/wiki/Bin_packing_problem)
Given \(n\) items with weights \(w_1, \ldots, w_n\) and an arbitrary number of bins with maximum carry weight \(C\), determine the lowest number of bins that can contain all the items without exceeding their carry weight.

<details>
	<summary class="code-summary">Source code</summary>
	<div markdown="1">
```py
{% include linear-programming-in-python/bin.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Output</summary>
	<div markdown="1">
```
{% include linear-programming-in-python/bin.out %}```
</div>
</details>

#### [Partition problem](https://en.wikipedia.org/wiki/Partition_problem)
Given \(n\) items with weights \(w_1, \ldots, w_n\), split them into two parts such that the difference in their weights is minimized.

<details>
	<summary class="code-summary">Source code</summary>
	<div markdown="1">
```py
{% include linear-programming-in-python/partition.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Output</summary>
	<div markdown="1">
```
{% include linear-programming-in-python/partition.out %}```
</div>
</details>

#### [Maximum independent set](https://en.wikipedia.org/wiki/Independent_set_(graph_theory))
Given a graph \(G\), find the largest set of vertices such that no two share an edge.

<details>
	<summary class="code-summary">Source code</summary>
	<div markdown="1">
```py
{% include linear-programming-in-python/max-independent-set.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Output</summary>
	<div markdown="1">
```
{% include linear-programming-in-python/max-independent-set.out %}```
</div>
</details>

#### [Minimum vertex cover](https://en.wikipedia.org/wiki/Vertex_cover)
Given a graph \(G\), find the smallest set of vertices that cover all edges.

<details>
	<summary class="code-summary">Source code</summary>
	<div markdown="1">
```py
{% include linear-programming-in-python/min-vertex-cover.py %}```
</div>
</details>

<details>
	<summary class="code-summary">Output</summary>
	<div markdown="1">
```
{% include linear-programming-in-python/min-vertex-cover.out %}```
</div>
</details>


### Resources
Here are all the resources I used for data and documentation:
- [Hands-On Linear Programming: Optimization With Python](https://realpython.com/linear-programming-python/)
- [PuLP documentation](https://coin-or.github.io/pulp/)
- [Dataset for TSP](https://people.sc.fsu.edu/~jburkardt/datasets/tsp/tsp.html)
- [Dataset for knapsack](https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/knapsack_01.html)
- [Dataset for the partition problem](https://people.sc.fsu.edu/~jburkardt/datasets/partition_problem/partition_problem.html)
