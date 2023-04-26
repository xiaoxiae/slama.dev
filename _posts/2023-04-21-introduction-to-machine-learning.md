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
- for classification, we want \[\underbrace{p(Y = k \mid X)}_{\text{posterior}} = \frac{  \overbrace{p(X \mid Y = k)}^{\text{likelyhood}}\ \overbrace{p(Y = k)}^{\text{prior}} }{\underbrace{p(X)}_{\text{marginal}}} \]
	- **posterior** -- we want to update our judgement based on measuring the features
	- **prior** -- we know this (1% for a disease in the general population)
	- **likelyhood** -- the likelyhood of the disease given features (fever, cough)
	- **marginal** -- can be recovered by summing over possibilities: \[p(X) = \sum_{k = 1}^{C} p(X \mid Y = k)\]

Is hugely important for a number of reasons:
- fundamental equation for probabilistic machine learning
	- allows clean uncertainty handling (among others)
- puts model accuracy into perspective (what is good or bad)
- defines two fundamental _model types_:
	- **discriminative model:** learns \(p(Y = k \mid X)\) (right side)
		- answers the question "what class" directly
		- **(+)** relatively easy -- take the direct route, no detour
		- **(-)** often hard to interpret _how_ the model makes decisions (black box)
	- **generative model:** learns \(p(Y = k)\) and \(p(X \mid Y = k)\) (left side)
		- first learn how "the world" works, then use this to answer the question
			- \(p(X \mid Y = k)\) -- understand the mechanism how observations ("phenotypes") arise from hidden properties
		- **(-)** pretty hard -- need powerful models and a lot of data
		- **(+)** easily interpretable -- we can know why it was answered

- ex.: breast cancer screening: \(p(Y = 1) = 0.001, p(Y = -1) = 0.999\)
	- a test answers the following
		- correct diagnosis: \(p(X = 1 \mid Y = 1) = 0.99\)
		- false positive: \(p(X = 1 \mid Y = -1) = 0.01\)
	-  _if the test is positive, should you panic?_ \[\begin{aligned} p(Y = 1 \mid X = 1) &= \frac{p(X = 1 \mid Y = 1) p(Y = 1)}{p(X = 1 \mid Y = 1) p(Y = 1) + p(X = 1 \mid Y = -1) p(Y = -1)} \\ &= \frac{0.99 \cdot 0.001}{0.99 \cdot 0.001 + 0.01 \cdot 0.999} \\ &\approx \mathbf{0.1}
\end{aligned}\]
		- due to the very low probability of the disease, you're likely fine

Some history behind ML:
- traditional science seeks generative models (we can create synthetic data that are indistinguishable from real data)
	- physics understand the movement of an object, so a game can use this to appear real
- ~1930: ML researches realized that their models were too weak to do this \(\implies\) field switched to discriminative models
- ~2012: neural networks solved many hard discriminative tasks \(\implies\) the field is again interested in generative models (Midjourney, ChatGPT, etc.)
	- subfield "explainable/interpretable ML"

##### How good can it be?
{% math ENdefinition "Bayes classifier" %}uses Bayes rule (LHS or RHS) with true probabilities \(p^*\){% endmath %}
- we don't know \(p^*\), we want to get as close as possible

{% math ENtheorem %}no learned classifier using \(\hat{p}\) can be better than the Bayes classifier.{% endmath %}
- if our results are bad, we have to get better theory (more features)

##### How bad can it be?
- case 1: **all classes are equally probable** (\(p(Y = k) = \frac{1}{C}\))
	- worst classifier: pure guessing -- correct \(50\%\) of the time
- case 2: **unbalanced classes**
	- worst classifier: always return the majority label

#### Linear classification
1. use a linear formula to reduce all features to scaled score
2. apply threshold classifier to score (\(C = 2\) for now)

\[\hat{Y}_i = \mathrm{sign}\left(\sum_{j} \beta_j X_{ij} + b\right)\]
for feature weights \(\beta\) and intercept \(b\).

- learning means finding \(\hat{\beta}\) and \(\hat{b}\)
- we can also get rid of \(b\) by one of the following:
	1. if all classes are balanced (\(p(Y = k) = \frac{1}{C}\)) then we can centralize features 
\[\bar{X} = \frac{1}{N} \sum_{i = 1}^{N} X_i \qquad \overset{0}{X_i} = X_i - \bar{X}_i\]
	2. absorb \(b\) into \(X\): define new feature \(X_{i0} = 1\) (will then act as \(b\))
		- done quite often (\(X_{i0}\) is then called the "bias neuron")

##### Perceptron
- Rosenblatt, 1958
- first neural network (1 neuron)
- idea: improve \(\beta\) when model makes mistakes
	- **naive approach** -- **0/1 loss:** \[\mathcal{L}(\hat{Y}_i, Y^*_i) = \begin{cases} 0 & \hat{Y}_i = Y^*_i \\ 1 & \hat{Y}_i \neq Y^*_i \end{cases}\]
		- can be used to **evaluate** but **doesn't tell us how to improve** (and how)
	- **better idea** -- **perceptron loss:** weigh penalty by error magnitude \[\mathcal{L}(\hat{Y}_i, Y^*_i) = \begin{cases} 0 & \hat{Y}_i = Y^*_i \\ |X_i \beta| = -Y_i X_i \beta & \hat{Y}_i \neq Y^*_i \end{cases}\]
		- nowadays we use \(\mathrm{ReLu}(-Y_i X_i \beta)\) for \(\mathrm{ReLu}(t) = \begin{cases} 0 & t < 0 \\ t & \text{otherwise} \end{cases}\)
- gradient descent for our classifier looks as follows: \[\beta^{(t)} = \beta^{(t - 1)} - \tau \underbrace{\frac{\partial \mathcal{L}^{(t - 1)}}{\partial \beta}}_{\text{loss derivative}}\] for **learning rate** \(\tau \ll 1\)

In our case: \[\frac{\partial \mathcal{L}^{(t - 1)}}{\partial \beta} = \frac{\partial \mathrm{ReLu} (-Y_i X_i \beta)}{\partial \beta} = \begin{cases} 0 & -Y_i^* X_i \beta < 0\ \ \text{(correct)} \\ -Y_i^* X_i^T & \text{otherwise} \end{cases}\]

{% math ENalgorithm "Rosenblatt's algorithm" %}

1. initialzation of \(\beta^{(0)}\) -- random/uniform numbers
2. for \(t = 1, \ldots, T\) (or until convergence)
	- update \(\beta\) using the gradient descent formula above, with minor changes:
		- additionally, use \(\tau / N\) instead of \(\tau\) (so it doesn't change when learning set changes)
		- sum over only incorrect guesses from the previous iteration
\[\beta^{(t)} = \beta^{(t - 1)} + \frac{\tau}{N} \sum_{i: \hat{Y}_i^{(t - 1)} \neq Y_i^*} Y_i^* X_i^T\]
{% endmath %}

- only converges when the data is "linearly separable" (i.e. \(\exists \beta\) for loss \(0\))
- high-level overview: project points together (positive/negative), then "pull the line to the data"

![Linear classifier.](/assets/introduction-to-machine-learning/linear-classifier.svg)

- **(+)** first practical learning algorithm, established the gradient descent principle
- **(-)** only converges when the training set area linearly separable
- **(-)** tends to overfit, bad at generalization

Improved algorithm (popular around 1995): **(Linear) Support Vecor Machine**
- maintain a safety region around data where solution should not be
- if a solution intersects the safety region, it is forbidden \(\implies\) better at generalization
