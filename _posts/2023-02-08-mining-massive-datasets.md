---
title: Mining Massive Datasets
category: "notes"
category_icon: /assets/category-icons/heidelberg.webp
pdf: false
---

- .
{:toc}

{% lecture_notes_preface_heidelberg Artur Andrzejak|2022/2023%}

_Note that the notes only cover the topics [required for the exam](exam.pdf)._

### Lecture overview

1. Spark architecture and RRDs [[slides](/assets/mining-massive-datasets/01.pdf)]
2. Spark Dataframes + Pipelines [[slides](/assets/mining-massive-datasets/02.pdf)]
3. Recommender Systems 1 [[slides](/assets/mining-massive-datasets/03.pdf)]
4. Recommender Systems 2 [[slides](/assets/mining-massive-datasets/04.pdf)]
5. Page Rank 1 [[slides](/assets/mining-massive-datasets/05.pdf)]
6. Page Rank 2 [[slides](/assets/mining-massive-datasets/06.pdf)]
7. Locality Sensitive Hashing 1 [[slides](/assets/mining-massive-datasets/07.pdf)]
8. Locality Sensitive Hashing 2 [[slides](/assets/mining-massive-datasets/08.pdf)]
9. Frequent itemsets + A-Priori algorithm [[slides](/assets/mining-massive-datasets/09.pdf)]
10. PCY extensions [[slides](/assets/mining-massive-datasets/10.pdf)]
10. Online bipartite matching + BALANCE [[slides](/assets/mining-massive-datasets/11.pdf)]
12. Mining data streams 1 [[slides](/assets/mining-massive-datasets/12.pdf)]
13. Mining data streams 2 [[slides](/assets/mining-massive-datasets/13.pdf)]

### Programming and Frameworks

### Recommender Systems
Problem: \(X\) as set of customers, \(S\) as set of items
- utility function \(u: X \times S \mapsto R\) (set of ratings)
	- \(R\) usually \(\in [0, 1]\)
	- can be stored in a **utility matrix**

Goal: **extrapolate unknown ratings from the known ones**.

#### Collaborative filtering (CF)

##### User-user CF
- consider user \(x\):
	- find set \(N\) of other users whos ratings are similar to \(x\)'s ratings
	- estimate \(x\)'s ratings based on ratings of users from \(N\)

{% math ENalgorithm %}
1. let \(r_x\) be vector of user \(x\)'s ratings and \(N\) the set of \(k\) neighbors of \(x\)
2. predicted rating of user \(x\) for item \(i\) is \[\underbrace{r_{xi} = \frac{1}{k} \sum_{y \in N} r_{yi}}_{\text{naive version (just average)}} \qquad \underbrace{r_{xi} = \mathrm{avg}(r_x) +  \frac{\sum_{y \in N} \mathrm{sim}(x, y) \cdot (r_{yi} - \mathrm{avg}(r_x))}{ \sum_{y \in N} | \mathrm{sim}(x, y) |}}_{\text{improved, takes similarity into account, along with user's bias}}\]
{% endmath %}

To calculate similarity, we can use a few things:
- **Cosine similarity measure** (angle between vectors) \[\mathrm{sim}(x, y) = \mathrm{cos}(r_x, r_y) = \frac{r_x \cdot r_y}{ ||r_x|| \cdot ||r_y||}\]
	- problem 1: missing ratings become low ratings
	- problem 2: doesn't account for bias (some users rate higher on average)
- **Pearson similarity measure** (angle between normalized vectors without zero entries) \[\mathrm{sim}(x, y) = \frac{\sum_{s \in S_{xy}} (r_{xs} - \mathrm{avg}(r_x)) (r_{ys} - \mathrm{avg}(r_y))}{\sqrt{\sum_{s \in S_{xy}} \left(r_{xs} - \mathrm{avg}(r_x)\right)^2} \sqrt{\sum_{s \in S_{xy}} \left(r_{ys} - \mathrm{avg}(r_y)\right)^2}}\]
	- problem 1 fixed by only taking items rated by both users
	- problem 2 fixed by normalization

To caulcate neighbourhood, we can do a few things:
- set a threshold for similarity
- take the top \(k\) similar users

##### Item-item CF

TODO

##### Pros/Cons

- [+] **Works for any kind of item** (no feature extraction)
- [-] **Cold start** (needs user data)
- [-] **Sparsity** (user/rating matrix is sparse)
- [-] **First rater** (can't recommend an item that hasn't been rated)
- [-] **Popularity bias** (tends to recommend popular items)


#### Content-based recommendations
Main idea: recommend items similar to previous items rated highly (based on features)

- create an **item profile** for each item, which is a vector \(v\) of features
	- author, title, actor, director, important words
	- can be usually encoded as a binary vector with values getting fixed positions in the vector

TODO

#### Latent factor models

TODO: intro
TODO: finding latent factors
TODO: concept of regularization (no formulas)

### Link Analysis

#### Flow formulation
**Problem:** we have pages as a directed graph. We want to determine the importance of pages based on how many links lead to it. I.e. if page \(j\) of importance \(r_j\) has \(n\) outgoing links, each link gets importance \(r_j / n\).
Formally:
\[r_j = \sum_{i \rightarrow j} \frac{r_i}{ d^{\mathrm{out}}_i}\]

Can be expressed as a system of linear equations to be solved (Gaussian elimination, for example). If formulated as an adjacency matrix \(M\) (where \(M_{ji} = \frac{1}{d^{\mathrm{out}}_i}\)), then we can define the flow equation as \[Mr = r\]
meaning that we're looking for the **eigenvector** of the matrix.
Since the matrix is stochastic (columns sum to 1), its first eigenvector has eigenvalue 1 and we can find it using **power iteration.**

#### Matrix formulation

This, however, has two problems:

- **dead ends** (when a page has no out-links); makes the matrix non-stochastic!
- **spider traps** (when there is no way to get out of a part of the graph)

Both are solved using **teleports** -- during each visit, we have a probability of \(1 - \beta\) to jump to a random page (\(\beta\) usually \(0.8\)). In a dead-end, we teleport with probability \(1\).

Using this, we get the **Google PageRank equation:** \[\underbrace{r_j = \sum_{i \rightarrow j} \beta \frac{r_i}{d^{\mathrm{out}}_i} + (1 - \beta) \frac{1}{N}}_{\text{PageRank equation}} \qquad \underbrace{A = \beta M + (1 - \beta) \left[\frac{1}{N}\right]_{N \times N} \quad Ar = r}_{\text{Google Matrix A}}\]

#### Practical computation
To reduce the matrix operations, we can rearange the matrix equation and get \[r =\beta M \cdot r + \left[\frac{1 - \beta}{N}\right]_N\]

{% math ENalgorithm "PageRank" %}
- set \(r^{\mathrm{old}}_j = \frac{1}{N}\)
- repeat until \(\sum_{j} |r^{\mathrm{new}}_j - r^{\mathrm{old}}_j| < \varepsilon\):
	- _power method iteration:_ \(\forall j: r^{\mathrm{new}}_j = \sum_{i \rightarrow j} \beta \frac{r^{\mathrm{old}_i}}{d^{\mathrm{out}}_i}\), otherwise \(0\) if in-degree of \(j\) is \(0\)
	- _vector normalization:_ \(\forall j: r^{\mathrm{new}}_j = r^{\mathrm{new}}_j + \frac{1 - \sum_{j} r^{\mathrm{new}}_j}{N}\)
	- \(r^{\mathrm{old}} = r^{\mathrm{new}}\)
{% endmath %}

TODO: memory constraints

TODO: pagerank: topic-specific
TODO: pagerank: trustrank

### Locality Sensitive Hashing

TODO: word on has function and data structures
TODO: intro
TODO: shingling
TODO: minhashing
TODO: locality sensitive hashing

### Association Rule Discovery

### Online Advertising

### Mining Data Streams
