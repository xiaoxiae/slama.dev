---
title: Introduction to Machine Learning
category: "notes"
category_icon: /assets/category-icons/heidelberg.webp
---

- .
{:toc}

{% lecture_notes_preface_heidelberg TODO|2023/2024%}

### Machine Learning Essentials

#### Introduction

Setting:
- **quantities \(Y\)** that we would like to know but can't easily measure
- **quantities \(X\)** that we can measure and are related to \(Y\)

Idea:
- learn a function \(\hat{y} = f(x)\) such that \(\hat{y}_i \approx y_i^*\) (we're close to the real value)

Traditional approach:
- ask an expert to figure out \(f(x)\), but for many approaches ML works better

Machine learning:
- choose a universal function family \(F\) with parameters \(\theta\)
	- ex. \(F = \left\{ax^2 + b + c\right\}, \theta = \left\{a, b, c\right\}\)
- find parameters \(\hat{\theta}\) that fit the data, so \[\hat{y} = f_{\hat{\thera}}(x) \qquad \text{and} \qquad \hat{y}_i \approx y_i^*\]

Basic ML workflow
1. **collect data** in two datasets: **training** dataset (TS) to train and **test** dataset to validate
	- extremely important, if you don't do this you die instantly
	- necessary for recognizing overfitting (\(F\) is polynomials and we fit points...)
2. **select function family** \(F\)
	- prior knowledge about what the data looks like
	- trial and error (there are tools to help you with this)
3. find the best \(\hat{\theta}\) by fitting \(F\) to the **training** set
4. validate the quality of \(f_{\hat{\theta}}(x)\) on the **test** set
5. **deploy** model in practice

Probabilistic prediction:
- reality is often more complicated
- no unique true response \(y^*\), instead set of possible values (possibly infinite)
- in that case we learn a conditional probability (instead of a function): \[\hat{y} \sim p(Y \mid X)\]
- to learn this, we define a "universal probability family" with parameters \(\theta\) and chose \(\hat{\theta}\) such that \[y \sim p_{\hat{\theta}}(Y \mid X)\] matches the data
- strict generalization: deterministic case is recovered by defining \(p(Y \mid X) = \delta(Y - f(X))\)
	- \(\delta\) distribution has only one value
- often we derive deterministic results from probabilistic predictions (eg. mode/median/random sample of the distribution)
	- generally, mode is the best, has some really nice properties

Problems:
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

- **features** vector \(X_i\) for each instance \(i \in 1 \ldots N\)
- **feature matrix** \(X\) (rows are instances, columns are features \(j \in 1 \ldots D\))
	- \(X \in \mathbb{R}^{N \times D}\)

| i\j   | \(1\) (name) | \(2\) (height) | \(3\) (gender) |
| ---   | ---          | ---            | ---            |
| \(1\) | Alice        | \(1.7\)m       | f              |
| \(2\) | Bob          | \(1.8\)m       | m              |
| \(3\) | Max          | \(1.9\)m       | m              |

We usually (when Programming) want a **float matrix:** drop names, discretize labels and use one-hot encoding.
- one-hot because there is only ones in the particular features

| i\j       | \(1\) (height) | \(2\) (f) | \(3\) (m) | \(4\) (d) |
| ---       | ---            | ---       | ---       | ---       |
| \(1\)     | \(1.7\)        | \(1\)     | \(0\)     | \(0\)     |
| \(2\)     | \(1.8\)        | \(0\)     | \(1\)     | \(0\)     |
| \(N = 3\) | \(1.9\)        | \(0\)     | \(1\)     | \(0\)     |

- **response** \(Y_i\) row vector for instance \(i\), response elements \(m \in 1 \ldots M\)
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
			- \(\tilde{X} = \Phi \mid X\) (ex. dimension reduction)
		2. **clustering** -- group similar instances into "clusters" with a single representative
4. **self-supervised learning** -- define an auxiliary task where \(Y_i\) are easy to determine
