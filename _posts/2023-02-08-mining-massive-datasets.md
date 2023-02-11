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
	- can be stored in a **utility matrix:**

|           | Alice   | Bob     | Carol   | David   |
| Star Wars | \(1\)   |         | \(0.2\) |         |
| Matrix    |         | \(0.5\) |         | \(0.3\) |
| Avatar    | \(0.2\) |         | \(1\)   |         |
| Pirates   |         |         |         | \(0.4\) |

Goal: **extrapolate unknown ratings from the known ones**.

#### Collaborative filtering (CF)

##### User-user CF
- consider user \(x\):
	- find set \(N\) of other users whos ratings are similar to \(x\)'s ratings
	- estimate \(x\)'s ratings based on ratings of users from \(N\)

{% math ENalgorithm %}
1. let \(r_x\) be vector of user \(x\)'s ratings and \(N\) the set of \(k\) neighbors of \(x\)
2. predicted rating of user \(x\) for item \(i\) is \[\underbrace{r_{xi} = \frac{1}{k} \sum_{y \in N} r_{yi}}_{\text{naive version (just average)}} \qquad \underbrace{r_{xi} = \mathrm{avg}(r_x) +  \frac{\sum_{y \in N} \mathrm{sim}(x, y) \cdot (r_{yi} - \mathrm{avg}(r_x))}{ \sum_{y \in N} \mathrm{sim}(x, y)}}_{\text{improved, takes similarity of users into account, along with bias}}\]
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
Analogous to User-user: for rating item \(i\), we're find items rated by user \(x\) that are similar (as in rated similarly by other users). To do this, we can again use \(\mathrm{sim}\), obtaining \[r_{xi} = \frac{\sum_{j \in N} \mathrm{sim}(i, j) \cdot r_{xj}}{\sum_{j \in N} \mathrm{sim}(i, j)}\]

The improved version has a slightly different baseline, namely  \[r_{xi} = b_{xi} + \frac{\sum_{j \in N} \mathrm{sim}(i, j) \cdot (r_{xj} - b_{xj})}{\sum_{j \in N} \mathrm{sim}(i, j)}\]
where \(b_{xi} =\) mean item rating \(+\) rating deviation of user \(x\) \(+\) rating deviation of item \(i\).

##### Pros/Cons

- [+] **Works for any kind of item** (no feature extraction)
- [-] **Cold start** (needs user data)
- [-] **Sparsity** (user/rating matrix is sparse)
- [-] **First rater** (can't recommend an item that hasn't been rated)
- [-] **Popularity bias** (tends to recommend popular items)


#### Content-based recommendations
Main idea: create **item profiles** for each item, which is a vector \(v\) of features:
- author, title, actor, director, important words
- can be usually encoded as a binary vector with values getting fixed positions in the vector

For creating **user profiles,** we can do a weighted average (by rating) of their item profiles.

For matching User and Item, we can use **cosine similarity.**

#### Latent factor models
Merges Content-Based and CF -- use user data to create the item profiles!
We'll do this by factorizing the matrix into user matrix \(P\) and item matrix \(Q\) such that we minimize SSE \[\min_{P, Q} \sum_{\left(i, x\right) \in R} (r_{xi} - q_{i} \cdot p_x)^2\]

![Latent factors illustration.](/assets/mining-massive-datasets/lf.svg)

What we want to do is **split the data** into a training set, which we use to create the matrices, and the testing set, on which the matrices need to perform well.
To do this well, we'll use **regularization**, which controls for when the data is rich and when it's scarce (lots of zeroes in \(p_x\)s and \(q_i\)s): \[\min_{P, Q} \underbrace{\sum_{\left(x, i\right) \in R} \left(r_{xi} - q_i p_x\right)^2}_{\text{error}} + \underbrace{\lambda_1 \sum_{x} ||p_x||^2 + \lambda_2 \sum_{i} ||q_i||^2}_{\text{„length“}}\]
for \(\lambda_1, \lambda_2\) user-set regularization parameters.

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

When we don't have enough RAM to fit the whole matrix \(M\), we can read and update it by vertices (it's sparse so we'd likely be storing it as a dictionary):

| Source | Degree | Destination        |
| ---    | ---    | ---                |
| \(0\) | \(3\) | \(1, 5, 6\)          |
| \(1\) | \(4\) | \(17, 64, 113, 116\) |
| \(2\) | \(2\) | \(13, 23\)           |

I.e. do \(r^{\mathrm{new}}_{\mathrm{dest}_j} += \beta r^{\mathrm{old}}_i / d_i\).

When we can't even fit \(r^{\mathrm{new}}\) into memory, we can break it into \(k\) blocks that do fit into memory and scan \(M\) and \(r^{\mathrm{old}}\). This, however, is pretty inefficient -- we can instead use the **block-stripe** algorithm, which breaks \(M\) by destinations instead so we don't need to repeatedly scan it!

#### Topic-Specific PageRank
We can bias the random page walk to teleport to to relevant pages (from set \(S\)). For each teleport set \(S\), we get different vector \(r_S\). This changes the PageRank formulation like so:

\[A_{ij} = \beta M_{ij} + \begin{cases} (1 - \beta) / |S| & i \in S \\ 0 & \text{otherwise} \end{cases}\]

#### TrustRank
Adresses issues with spam farms, which are pages that just point to one another.
The general idea to fix this is to use a set of **seed pages** from the web and identify the ones that are „good“, i.e. **trusted**.
Then perform topic-specific pagerank with \(S =\) trusted pages, which propagates the trust to other pages.
After this, websites with trust below a certain threshold are spam.

- to pick seed pages, we can use PageRank and pick the top \(k\), or use trusted domains

### Locality Sensitive Hashing
We want to find near-neighbors in high-dimensional spaces:
- points in the same cluster
- pages with similar words

{% math ENdefinition "hash function" %}function \(h: D \mapsto R\), where \(D\) is a large domain space and \(R\) a small range space (usually integers).{% endmath %}
- for example \(h(x) = x \mod b\) with \(b\) prime

General steps:
- **Shingling:** convert items (in our case documents) into _sets_
- **Min-hashing:** convert large sets into shorter _signatures_
- **Locality-Sensitive Hashing:** identify pairs of signatures _likely to be similar_
- **Final filtering:** get the final few candidate pairs and _compare them pairwise_

#### Shingling
For a document, take a sliding window of size \(k\).
Then \(k\)-shingles for the given document are all sequences of \(k\) consecutive tokens from the document.
- if the shingles are long, they can also be compressed using some hash function

#### Min-hashing
The shingling sets are very large, so we have to find a way to measure how similar they are.
What we want to measure is their **Jaccard similarity**, which is \[\mathrm{sim}(S_1, S_2) = |S_1 \cap S_2|\ /\ |S_1 \cup S_2|\]

To do this, we'll compute **signatures**: to compute a signature, we take many random hash function (for example random permutations), hash all values from the set of shingles and take the minimum.
Then the list of all those minimal values is the signature.
- in practice, we do \(((a \cdot x + b) \mod p) \mod N\) for \(a, b\) random integers, \(p\) prime and \(N\) size of shingles

For example:
- permutation \(\pi = (2, 3, 7, 6, 1, 5, 4)\)
- set of shingles (as bit array) \((1, 1, 0, 0, 0, 1, 1)\)
- resulting min-hash: \(2\) (by shingle \(1\) mapping to index \(2\))

It turns out that \(\mathrm{Pr}\left[h_\pi (S_1) = h_pi (S_2)\right] = \mathrm{sim}(S_1, S_2)\)

**Intuition** is that if the sets of shingles are very similar, randomly shuffling them in the same way and then taking the minimum value should, with a high probability, be equal.

#### Locality-Sensitive Hashing
Our goal now is to find documents with Jaccard similarity at least \(s\) (e.g. \(0.8\)).
To do this, we will **hash parts of the signature matrix:**
- take matrix \(M\) and divide it into \(b\) _bands_ of \(r\) _rows_
- for each band, hash its portion of each column to a hash table with \(k\) buckets
- candidate column pairs are those that hash to the same bucket for \(\ge 1\) band

![Locality-Sensitive Hashing example.](/assets/mining-massive-datasets/lsh.svg)

We want to tune \(b\) and \(r\) to catch most similar pairs but few non-similar pairs:
- let \(s = 0.8\) and \(b = 20, r = 5\)
- \(S_1, S_2\) are \(80\%\) similar:
	- then the probability for one band is \(0.8^{5} = 0.328\)
	- probability that \(S_1\) and \(S_2\) are not similar is \((1 - 0.328)^{20} = 0.00035\)
- \(S_1, S_2\) are \(30\%\) similar:
	- then the probability for one band is \(0.3^{5} = 0.00243\)
	- probability that \(S_1\) and \(S_2\) ARE similar is \(1 - (1 - 0.00243)^{20} = 0.047\)
		- i.e. \(4.74%\) pairs of docs with similarity \(0.3\) become candidate pairs

![S-Curve illustration.](/assets/mining-massive-datasets/s-curve.svg)

### Association Rule Discovery

### Online Advertising

### Mining Data Streams
