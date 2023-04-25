---
title: Introduction to Machine Learning
category: "notes"
category_icon: /assets/category-icons/heidelberg.webp
---

- .
{:toc}

{% lecture_notes_preface_heidelberg Ullrich Köthe|2022/2023%}

_Note that the notes are a work in progress!_

### Machine Learning Essentials

#### Introduction

Setting:
- **quantities \(Y\)** that we would like to know but can't easily measure
- **quantities \(X\)** that we can measure and are related to \(Y\)

**Idea:**
- learn a function \(\hat{Y} = f(X)\) such that \(\hat{Y}_i \approx Y_i^*\) (we're close to the real value)

**Traditional approach:**
- ask an expert to figure out \(f(X)\), but for many approaches ML works better

**Machine learning:**
- choose a universal function family \(F\) with parameters \(\theta\)
	- ex. \(F = \left\{ax^2 + b + c\right\}, \theta = \left\{a, b, c\right\}\)
- find parameters \(\hat{\theta}\) that fit the data, so \[\hat{Y} = f_{\hat{\theta}}(X) \qquad \text{and} \qquad \hat{Y}_i \approx Y_i^*\]

**Basic ML workflow:**
1. **collect data** in two datasets: **training** dataset (TS) to train and **test** dataset to validate
	- extremely important, if you don't do this you die instantly
	- necessary for recognizing overfitting (\(F\) is polynomials and we fit points...)
2. **select function family** \(F\)
	- prior knowledge about what the data looks like
	- trial and error (there are tools to help you with this)
3. find the best \(\hat{\theta}\) by fitting \(F\) to the **training** set
4. validate the quality of \(f_{\hat{\theta}}(X)\) on the **test** set
5. **deploy** model in practice

**Probabilistic prediction:**
- reality is often more complicated
- no unique true response \(Y^*\), instead set of possible values (possibly infinite)
- in that case we learn a conditional probability (instead of a function): \[\hat{Y} \sim p(Y \mid X)\]
- to learn this, we define a "universal probability family" with parameters \(\theta\) and chose \(\hat{\theta}\) such that \[Y \sim p_{\hat{\theta}}(Y \mid X)\] matches the data
- strict generalization: deterministic case is recovered by defining \(p(Y \mid X) = \delta(Y - f(X))\)
	- \(\delta\) distribution has only one value
- often we derive deterministic results from probabilistic predictions (eg. mode/median/random sample of the distribution)
	- generally, mode is the best, has some really nice properties

**Problems:**
- nature is not fully predictable
	- _quantum physics_ (randomness)
	- _deterministic chaos_ (pendulum)
	- _combinatorial explosion_ (aminoacids)
- data:
	- finite
	- noisy
	- incomplete
	- ambiguous
- model:
	- function family is imperfect (too small)
	- may not have converged
	- nature has changed in the meantime
- goal:
	- disagreement about what is relevant (desirable)
- **handling uncertainty is central challenge of AI and ML**

#### Notation

- **features** vector \(X_i\) for each instance \(i \in 1, \ldots, N\)
- **feature matrix** \(X\) (rows are instances, columns are features \(j \in 1, \ldots, D\))
	- \(X \in \mathbb{R}^{N \times D}\)

| \(i \setminus j\) | \(1\) (name) | \(2\) (height) | \(3\) (gender) |
| ---               | ---          | ---            | ---            |
| \(1\)             | Alice        | \(1.7\)m       | f              |
| \(2\)             | Bob          | \(1.8\)m       | m              |
| \(3\)             | Max          | \(1.9\)m       | m              |

We usually (when Programming) want a **float matrix:** drop names, discretize labels and use one-hot encoding (one-hot because there is only ones in the particular features).

| \(i \setminus j\) | \(1\) (height) | \(2\) (f) | \(3\) (m) | \(4\) (o) |
| ---               | ---            | ---       | ---       | ---       |
| \(1\)             | \(1.7\)        | \(1\)     | \(0\)     | \(0\)     |
| \(2\)             | \(1.8\)        | \(0\)     | \(1\)     | \(0\)     |
| \(3\)         | \(1.9\)        | \(0\)     | \(1\)     | \(0\)     |

- **response** \(Y_i\) row vector for instance \(i\), response elements \(m \in 1, \ldots, M\)
	- most of the time, \(M = 1\) (scalar response)
	- exception is one-hot encoding of discrete labels
- **tasks** according to type of response
	- \(Y_i \in \mathbb{R}^M \ldots\)  \(Y \approx f_\theta(X)\) is **regression**
	- \(Y_i = k; k \in \left\{1, \ldots, C\right\}\) for \(C\) number of categories \(\ldots\) **classification**
		1. labels are _ordered_ ("tiny" < "small" < "medium" < "large") -- **ordinal classification**
		2. labels are _unordered_ ("apples", "oranges") -- **categorial classification**

- **training set** \(\mathrm{TS} = \left\{(X_i, Y_i)\right\}_{i = 1}^N\) -- **supervised learning**
	- \(Y_i\) is the known response for instance \(i\)

##### Types of learning approaches
1. **supervised learning** -- **true responses** are known in \(\mathrm{TS} = \left\{(X_i, Y_i)\right\}_{i = 1}^N\)
2. **weakly supervised learning**
	1. we have _some_ information (know \(Y_i\) for some instances)
	2. we have _worse_ information (there is a tumor but we don't know where)
3. **unsupervised learning** -- **only features** are known in \(\mathrm{TS} = \left\{X_i\right\}_{i = 1}^N\)
	- learning algorithm must find the structure in the data _on its own_ (data mining or, for humans, "research")
	- only a few solutions that are guaranteed to work (this is unsurprisingly difficult to do)
		1. **representation learning** -- compute new features that are _better to predict_
		2. **clustering** -- group similar instances into "clusters" with a single representative
4. **self-supervised learning** -- define an auxiliary task where \(Y_i\) are easy to determine

### Classification
- \(Y_i = k, k \in \left\{1, \ldots, C\right\}\)
	- common special case \(C = 2\), then \(k \in \left\{0, 1\right\}\) or \(k \in \left\{-1, 1\right\}\)
- **always supervised!**

#### Deterministic classifier
- one hard prediction for each \(i\) \[\hat{Y}_i = f(X_i) \quad \text{with} \quad \hat{Y}_i = Y_i^*\]


**Quality** measured by collecting the "confusion matrix"

| \(\hat{Y} \setminus Y^*\) | \(-1\)         | \(+1\)         |
| ---                       | ---            | ---            |
| \(-1\)                    | true negative  | false negative |
| \(+1\)                    | false positive | true positive  |

1. false positive/negative **fraction** -- "how many out of **all** events are false" \[\frac{\# \mathrm{FP}\ \text{or}\ \# \mathrm{FN}}{\mathrm{N}} \in \left[0, 1\right]\]
2. false positive/negative **rate** -- "how many out of **positive/negative** events are false" \[\frac{\# \mathrm{FP}}{\# \mathrm{FP} + \# \mathrm{TN}} \approx p(\hat{Y} = 1 \mid Y^* = -1) \qquad \frac{\# \mathrm{FN}}{\# \mathrm{FN} + \# \mathrm{TP}} \approx p(\hat{Y} = -1 \mid Y^* = 1)\]

#### Probabilistic classifier
- returns a probabilistic vector \(\in [0, 1]^C\) (soft response) for every label \(\equiv\) posterior distribution \[p(Y = k \mid X)\]
- more general than hard classification -- can recover decision function by returning the most probable label by using \(\arg \max\): \[p(Y = k \mid X) \implies f(X) = \arg \max_k\ p(Y = k \mid X)\]

**Quality** measured by "calibration"
- if \(p(Y = k \mid X) = v\), then label \(k\) should be correct \(v\%\) of the times
	- if actual accuracy is **higher**, then the classifier is "under confident"
	- otherwise it's "over confident" (often happens)

**Important:** calculate confusion matrix or calibration from **test set,** not train set (bias)!

#### Threshold classifier
- single feature \(X \in \mathbb{R}\)
	- usually not enough to predict the response reasonably
- \(\hat{Y} = \mathrm{sign}(X - T) = \begin{cases} 1 & X > T \\ -1 & X < T \end{cases} \quad\) for some threshold \(T\)
- three classical solutions for multiple features
	1. **design a formula** to combine features into single score (use BMI for obese/not obese)
		- hard and expensive for most problems, not to mention inaccurate
	2. **linear classification:** compute score as a linear combination and learn coefficients
		- \(S_i = \sum_{j = 1}^{D} \beta_j X_{ij} \implies \hat{Y}_i = \mathrm{sign}(S_i - T)\) 
		- less powerful than the first one (restricted to linear formulas)
		- we can learn so it usually performs better
	3. **nearest neighbour:** classify test instance \(X_{\text{test}}\) according to most similar training instance
		- \(\hat{i} = \arg \min_i\ \mathrm{dist(X_i, X_{\text{test}})}\)
		- then \(\hat{Y}_{\text{test}} = Y^*_{\hat{i}}\)
		- expensive -- to store the entire training set and scan it for every \(X_{\text{test}}\)
			- doesn't scale well for more features (generalized binary search)
		- hard to define the distance function to reflect true similarity
			- "metric learning" is a hard task of its own...

#### Bayes rule of conditional probability
- joint distribution of features and labels \(p(X, Y)\)
- can be decomposed by the chain rule to
	- \(p(X) p(Y \mid X)\) -- first measure features, then determine response
	- \(p(Y) p(X \mid Y)\) -- first determine response, then get compatible features
- for classification, we want \[\underbrace{p(Y = k \mid X)}_{\text{posterior}} = \frac{\overbrace{p(X \mid Y = k)}^{\text{likelyhood}} \overbrace{p(Y = k)}^{\text{prior}}}{\underbrace{p(X)}_{\text{marginal}}} \]
	- **prior** -- we know this (1% for a disease in the general population)
	- **posterior** -- we update our judgement based on measuring the features
	- **likelyhood** -- the likelyhood of the disease given features (fever, cough)
	- **marginal** -- can be recovered by summing over possibilities: \[p(X) = \sum_{k = 1}^{C} p(X \mid Y = k)\]
