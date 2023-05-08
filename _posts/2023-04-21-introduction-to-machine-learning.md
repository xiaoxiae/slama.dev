---
title: Introduction to Machine Learning
category: "notes"
category_icon: /assets/category-icons/heidelberg.webp
pdf: true
---

- .
{:toc}

{% lecture_notes_preface_heidelberg Ullrich Köthe|2022/2023%}

_Note that the notes are a work in progress!_

_Also, special thanks to Lucia Zhang, some of the notes are shamelessly stolen from her._

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
- for classification, we want to use **Bayes rule** \[\boxed{\underbrace{p(Y = k \mid X)}_{\text{posterior}} = \frac{  \overbrace{p(X \mid Y = k)}^{\text{likelihood}}\ \overbrace{p(Y = k)}^{\text{prior}} }{\underbrace{p(X)}_{\text{marginal}}}}\]
	- **posterior** -- we want to update our judgement based on measuring the features
	- **prior** -- we know this (1% for a disease in the general population)
	- **likelihood** -- the likelihood of the disease given features (fever, cough)
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
	-  _if the test is positive, should you panic?_ \[\begin{aligned} p(Y = 1 \mid X = 1) &= \frac{p(X = 1 \mid Y = 1) p(Y = 1)}{p(X)} \\ &= \frac{0.99 \cdot 0.001}{0.99 \cdot 0.001 + 0.01 \cdot 0.999} \\ &\approx \mathbf{0.1}
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
	- **better idea** -- **perceptron loss:** weigh penalty by error magnitude (and use \(\mathrm{ReLU}\)) \[\mathcal{L}(\hat{Y}_i, Y^*_i) = \mathrm{ReLU}(-Y_i X_i \beta) = \begin{cases} 0 & \hat{Y}_i = Y^*_i \\ |X_i \beta| = -Y_i X_i \beta & \hat{Y}_i \neq Y^*_i \end{cases}\]
		- note that these are only for one instance, for all the average error is \[\frac{1}{N} \sum_{i = 1}^{N} \mathrm{ReLU} (-Y_i^* X_i \beta) = \frac{1}{N} \sum_{i: \hat{Y}_i \neq Y_i^*} -Y_i^* X_i \beta\]

Gradient descent looks as follows: \[\beta^{(t)} = \beta^{(t - 1)} - \tau \underbrace{\frac{\partial \mathcal{L}^{(t - 1)}}{\partial \beta}}_{\text{loss derivative}}\] for **learning rate** \(\tau \ll 1\) In our case, the derivative (for a single instance) is \[\frac{\partial \mathcal{L}^{(t - 1)}}{\partial \beta} = \frac{\partial \mathrm{ReLU} (-Y_i X_i \beta)}{\partial \beta} = \begin{cases} 0 & -Y_i^* X_i \beta < 0\ \ \text{(correct)} \\ -Y_i^* X_i^T & \text{otherwise} \end{cases}\]

##### Rosenblatt's algorithm

{% math ENalgorithm "Rosenblatt's algorithm" %}

1. initialzation of \(\beta^{(0)}\) -- random/uniform numbers
2. for \(t = 1, \ldots, T\) (or until convergence)
	- update \(\beta\) using the gradient descent formula above, with minor changes:
		- additionally, use \(\tau / N\) instead of \(\tau\) (so it doesn't change when learning set changes)
		- sum over only incorrect guesses from the previous iteration
\[\boxed{\beta^{(t)} = \beta^{(t - 1)} + \frac{\tau}{N} \sum_{i: \hat{Y}_i^{(t - 1)} \neq Y_i^*} Y_i^* X_i^T}\]
{% endmath %}

- only converges when the data is "linearly separable" (i.e. \(\exists \beta\) for loss \(0\))

![Linear classifier.](/assets/introduction-to-machine-learning/linear-classifier.svg)

- **(+)** first practical learning algorithm, established the gradient descent principle
- **(-)** only converges when the training set area linearly separable
- **(-)** tends to overfit, bad at generalization

##### (Linear) Support Vector Machine (LSVM)

Improved algorithm (popular around 1995): **(Linear) Support Vector Machine** (SVM)
- maintain a safety region around data where solution should not be
- closest points -- **support vectors**
- learns \(\hat{Y} = \argmax_k p(Y = k \mid X)\), which is LHS of Bayes -- is **discriminative**

Reminder: distance of a point \(X_i\) and plane \(\beta, b\) is \[d(X_i, (\beta, b)) = \left| \frac{ X_i \beta + b}{|| \beta ||} \right|\]
- notice that scaling \(\beta\) doesn't change the distance -- pairs \((\tau \beta, \tau b)\) define the same plane -- we can therefore define an equivalence class \[H = \left\{\beta', b' \mid \beta' = \tau \beta_H, b' = \tau b_H\right\}\] for \(\beta_H, b_H\) representatives (can be chosen arbitrarily)

Radius of the safety region (**margin**) is the **smallest distance** distance of a point to the decision plane (also called the "Hausdorff distance between H and TS"): \[m_H = \min_{i = 1}^N d(X_i, (\beta_H, b_H))\]

Let \(\hat{i}\) be the closest point. Then \[Y_{\hat{i}}^* (X_{\hat{i}} \beta_H + b_H) = m_H || \beta_H || \]
- we don't use minus because we want distance, not penalty (like perceptron)
- we again use the trick with multiplying by the label and brought the norm to the other side

Now we chose a representative such that the equation above is \(1\).
The decision plane is then correct when \[\forall i: Y_i^* (X_i \beta_H + b_H) \ge 1\] (specifically \(1\) for \(\hat{i}\)). To make it as general as possible, we want one that maximizes the distance \[
\begin{aligned}
	H &= \argmax_H m_H \\
	&= \argmax_H \left(\min_i \frac{Y_i^* (X_i \beta_H + b_H)}{ ||\beta_H ||}\right) \\
	&= \argmax_H \left(\frac{1}{|| \beta_H  ||} \min_i Y_i^* (X_i \beta_H + b_H))\right) \\
	&= \arg \max_H \frac{1}{|| \beta_H || }
\end{aligned}
\]

This yields an optimization problem: we want to \[\argmax_H \frac{1}{|| \beta_H || } \quad \text{s.t.} \quad \forall i:  Y_i^* (X_i \beta_H + b_H) \ge 1\]

This is inconvenient -- change to a more convenient equivalent optimization problem \[\argmin_H \frac{1}{2} \beta_H^T \beta_H \quad \text{s.t.} \quad \forall i:  Y_i^* (X_i \beta_H + b_H) \ge 1\]

Now we define slack variables \(\xi_i \ge 0\) that measure how much it was violated \[\argmin_H \frac{1}{2} \beta_H^T \beta_H \quad \text{s.t.} \quad \forall i:  Y_i^* (X_i \beta_H + b_H) \ge 1 - \xi_i\] and we also want to minimize those, which we'll do by using **Lagrange multipliers:** \[\boxed{\argmin_{H, \xi} \underbrace{\frac{1}{2} \beta_H^T \beta_H}_{\text{maximize margins}} + \underbrace{\frac{\lambda}{N} \sum_{i = 1}^{N} \mathrm{ReLU} (1 - Y_i^* (X_i \beta_H + b_H))}_{\text{minimize penalties for misclassified points}}}\]

- adjusting \(\lambda\) makes compromise between being right vs. robust (**hyperparameter tuning**):
	1. **approach:** 3 datasets -- training, validation, testing
		- pick a set of possible hyperparameters (\(\lambda \in \left\{10^{-2}, 10^{-1}, 1, 10, 100\right\}\))
		- train with each \(\lambda\) on the training set
		- measure accuracy on the validation set
		- keep the best \(\lambda\) on validation set, test again on the test set
		- validation is present because test set would otherwise be training too...
	2. **approach** (2 datasets): **cross-validation**
		- split training set into \(k\) pieces ("folds", typically \(k\) around \(5\) or \(10\))
			- _has to be randomly ordered, otherwise it won't work!_
		- use each fold as validation set in turn & train on the remaining \(k-1\) folds
		- special variation: \(n\)-fold (train on everything besides one instance)
			- expensive in practice, great in theory
- comparing with perceptron:
	- we introduced \(b\) (no normalization)
	- we now have a regularization term (no overfitting!)
	- we have \(1 - \ldots\): if you're barely right, you still pay small penalties!

We again optimize by derivative + gradient descent:

\[\frac{\partial \mathcal{L}}{\partial \beta} = \beta + \frac{\lambda }{N} \sum_{i = Y_i^* X_i \beta + b < 1}^{N} -Y_i^* X_i^T\]
\[\frac{\partial \mathcal{L}}{\partial b} = \frac{\lambda }{N} \sum_{i = Y_i^* X_i \beta + b < 1}^{N} -Y_i^*\]

The iteration step for \(\beta\) looks as follows: \[
\boxed{
\begin{aligned}
	\beta^{(t)} &= \beta^{(t - 1)} - \tau \left(\beta^{(t - 1)} + \frac{\lambda }{N} \sum_{i = Y_i^* X_i \beta + b < 1}^{N} -Y_i^* X_i^T\right) \\
	b^{(t)} &= b^{(t - 1)} - \tau \left(\frac{\lambda}{N} \sum_{i = Y_i^* X_i \beta + b < 1}^{N} -Y_i^*\right)
\end{aligned}
}
\]
- note that we can't get stuck in a minimum, since the objective function is convex

##### Linear Discriminant Analysis (LDA)
- idea: assume that features for each class form a cluster
	- assume they're elliptic and model each one as a Gaussian distribution
- is RHS of Bayes (**generative**) -- calculate the posterior from Bayes formula
- **Linear** -- clusters have the same shape
	- there is also a **Quadratic**, which permits different shapes but isn't linear

To get any ellipse, we start with a unit circle \(z\) and stretch (\(\lambda\)), rotate (\(Q\)) and shift (\(\mu\)) it: \[Q \lambda z + \mu = \begin{pmatrix} \cos \varphi & -\sin \varphi \\ \sin \varphi & \cos \varphi \end{pmatrix} \begin{pmatrix} x_1 & 0 \\ 0 & x_2 \end{pmatrix} z + \mu\]

![Derivation of an ellipse from a unit circle.](/assets/introduction-to-machine-learning/ellipses.svg)

Solving for \(z\) (and using the fact that \(Q\) is orthogonal), we get \[z = \lambda^{-1} Q^{-1} (X - \mu) = \lambda^{-1} Q^T (X - \mu)\]

**Gaussian distribution** can be defined as\[\mathcal{N}(x \mid \mu, \sigma) = \frac{1}{\sqrt{2 \pi \sigma^2}} \exp\left(-\frac{1}{2} \left((x - \mu)\sigma^{-1}\right)^2\right)\]
- for \(\mu \ldots\) **mean**, \(\sigma \ldots\) **variance**
- **standard normal distribution** is for \(\mu = 0\) and \(\sigma = 1\)

For higher dimensions (with our circle \(z\)), we get the generalized Gaussian \[\mathcal{N}(z \mid \mu, \Sigma) = \frac{1}{\sqrt{\det\left(2 \pi \Sigma\right)}} \exp\left(-\frac{1}{2} (x - \mu) \underbrace{Q^{-1}\lambda^{-1}\lambda^{-1}Q^{-T}}_{\Sigma^{-1}} (x - \mu)^T\right)\]
- \(\Sigma^{-1} = K\) is the **precision matrix**
- since \(\Sigma^{-1} = Q^{-1}\lambda^{-1}\lambda^{-1}Q^{-T}\), we see a decomposition to eigenvalues (correspond to square of radii of the ellipse) and eigenvectors (the corresponding radii vectors)

Let \(\left\{X-i\right\}_{i = 1}^{N_1}\) be features of class \(1\). Then \[N(X \mid \mu_1, \Sigma_1) = \frac{1}{\sqrt{\det(2 \pi \Sigma_1)}} \exp\left(-\frac{1}{2} (x_1 - \mu_1) \Sigma_1^{-1} (x_1 - \mu_1)^T\right)\]
- **learning:** find \(\mu_1\) and \(\Sigma_1\)

To derive the learning method, we'll use two things:
1. **maximum likelihood principle**: choose \(\mu_1\) and \(\Sigma_1\) such that TS will be a _typical outcome of the resulting model_ (i.e. best model maximizes the likelihood of TS)
2. **i.i.d. assumption:** training instances drawn independently from the same distribution
	- **i**ndependently -- joint distribution is the product
	- **i**dentically **d**istributed -- all instances come from the same distribution

For the probability, we get \[
\begin{aligned}
	p(\mathrm{TS}) &= p(X_1, \ldots, X_n) \\
	               &= \prod_{i = 1}^{N} p_i(X_i) \qquad \text{independently} \\
	               &= \prod_{i = 1}^{N} p(X_i) \qquad \text{identically distributed} \\
	               &= \prod_{i = 1}^{N} \mathcal{N(X_i \mid \mu, \Sigma)}
\end{aligned}\]

Using the maximum likelihood principle, the problem becomes \[\hat{\mu}, \hat{\Sigma} = \argmax_{\mu, \Sigma} p(\mathrm{TS})\]

It's mathematically simpler to minimize negative logarithm of \(p(\mathrm{TS})\) (applying monotonic function to an optimization problem doesn't change \(\argmin\) and \(\max = -\min\)). We get

\[
\begin{aligned}
	\hat{\mu}, \hat{\Sigma} &= \argmin_{\mu, \Sigma} -\log(p(\mathrm{TS})) \\ 
	                        &= - \sum_{i = 1}^{N} \left[\log \left(\frac{1}{\sqrt{\det(2 \pi \Sigma)}}\right) - \frac{1}{2} (X_i - \mu) \Sigma^{-1} (X_i - \mu)^T\right] \\
	                        &= \sum_{i = 1}^{N} \left[\log \left(\det(2 \pi \Sigma)\right) + (X_i - \mu) \Sigma^{-1} (X_i - \mu)^T\right] = \mathcal{L}(\mathrm{TS})
\end{aligned}
\]

This is our loss. We now do derivative and set it to \(0\), since that will find the optimum. First, we'll derivate by \(\mu\), which gets rid of the first part of loss completely and we get

\[
\begin{aligned}
	\frac{\partial \mathcal{L}}{ \partial \mu} = \sum_{i = 1}^{N} \overbrace{\Sigma^{-1} (X_i -\mu)^T}^{\frac{\partial vAv^T}{\partial v} = 2Av^T} &= 0 \\
	                                             \sum_{i = 1}^{N}             (X_i -\mu)^T &= 0 \\
	                                             \sum_{i = 1}^{N} X_i &= N \mu \\
	                                             \frac{1}{N} \sum_{i = 1}^{N} X_i &= \mu \\
\end{aligned}
\]

In other words, the **mean \(\mu\) is the average** (shocking, I know).

For \(\Sigma\), this will be a little more complicated. We'll do the partial derivation by \(\Sigma^{-1} = K\) instead, which gives the following:
\[
\begin{aligned}
	\frac{\partial \mathcal{L}}{ \partial K} = \sum_{i = 1}^{N} [ \overbrace{-(K^T)^{-1}}^{\frac{\partial \log \det K}{\partial K} = (K^T)^{-1}} + \overbrace{(X_i - \mu)^T (X_i - \mu)}^{\frac{\partial vAv^T}{\partial A} = v^Tv}] &= 0 \\
	                                          \sum_{i = 1}^{N} \left[ -K^{-1} + (X_i - \mu)^T (X_i - \mu)\right] &= 0 \qquad K\ \text{symmetric} \\
	                                          -N K^{-1} + \sum_{i = 1}^{N} (X_i - \mu)^T (X_i - \mu) &= 0 \\
	                                         \frac{1}{N} \sum_{i = 1}^{N} (X_i - \mu)^T (X_i - \mu) &= \Sigma \\
\end{aligned}
\]

Again, in other words, the **variance** is the average over the quared vectors offset by the mean, which too makes sense.

Now we have \(2\) clases but with same covariance (by assumption of LDA) and we can:
1. determine two means (\(\mu_1, \mu_{-1}\)) as \[\boxed{\mu_1 = \frac{1}{N_1} \sum_{i: Y_i^* = 1} X_i \qquad \mu_{-1} = \frac{1}{N_{-1}} \sum_{i: Y_i^* = -1}}\]
2. to calculate covariance (which is the same for both classes): \[\boxed{\Sigma = \frac{1}{N} \left(\sum_{i: Y_i^* = 1} (X_i - \mu_1)^T (X_i - \mu_1) + \sum_{i: Y_i^* = -1} (X_i - \mu_{-1})^T (X_i - \mu_{-1})\right)}\]
3. use Bayes RHS and our calculations to calculate the LHS: \[\boxed{\begin{aligned} \hat{Y}_i = \mathrm{sign}(X_i \beta + b) \quad \text{with} \quad &\beta = 2 \Sigma^{-1} (\mu_1 - \mu_{-1})^T \\ & b = \mu_{-1} \Sigma^{-1} \mu_{-1}^T - \mu_1 \Sigma^{-1} \mu_1^T \end{aligned}}\]

The derivation of (3) looks as follows: assuming \(p(Y = 1) = p(Y = -1) = \frac{1}{2}\) for simpler computations and \(p(Y = -1 \mid X)\) being analogous:

\[
\begin{aligned}
 p(Y=1|X)&=\frac{p(Y=1|X){p(Y=1)}}{p(Y=1|X){p(Y=1)}+p(Y=-1|X){p(Y=-1)}}\\            
 &=\frac{p(Y=1|X)}{p(Y=1|X)+p(Y=-1|X)}\\                                              
 &=\frac{1}{1+\frac{p(X|Y=-1)}{p(X|Y=1)}}
\end{aligned}
\]

Now we substitute the Gaussian function:

\[
\begin{aligned}
 \frac{p(X_i|{Y=-1})}{p(X_i|{Y=1})}&=\frac{\cancel{\frac{1}{\sqrt{\det(2\pi\Sigma)}}}\exp(-\frac{1}{2}(X_i-\mu_{-1})\Sigma^{-1}(X_i-\mu_{-1})^T)}{\cancel{\frac{1}{\sqrt{\det(2\pi\Sigma)}}}\exp(-\frac{1}{2}(X_i-\mu_{1})\Sigma^{-1}(X_i-\mu_{1})^T)}\\
 &=\exp(-\frac{1}{2}(X_i-\mu_{-1})\Sigma^{-1}(X_i-\mu_{-1})^T+\frac{1}{2}(X_i-\mu_{1})\Sigma^{-1}(X_i-\mu_{1})^T) \\
 &=\exp(-\frac{1}{2}\left[\cancel{X\Sigma^{-1}X^T}-2X\Sigma^{-1}\mu_{-1}^T+\mu_{-1}\Sigma^{-1}\mu_{-1}^T-\cancel{X\Sigma^{-1}X^T}+2X\Sigma^{-1}\mu_1^T-\mu_1\Sigma^{-1}\mu_{1}^T\right])\\
 &=\exp(-X\underbrace{\Sigma^{-1}(\mu_1^T-\mu_{-1}^T)}_\beta-\frac{1}{2}\underbrace{(\mu_{-1}\Sigma^{-1}\mu_{-1}^T-\mu_1\Sigma^{-1}\mu_1^T)}_b)=\exp(-(X\beta+b))
\end{aligned}
\]

Plugging the result into the previous equation, we obtain the sigmoid function \(\sigma\):

\[p(Y = 1 \mid X) = \frac{1}{1 + \mathrm{exp}(-(X \beta + b))} \qquad \sigma(t) = \frac{1}{1 + \exp(-t)}\]

Two of its properties will be helpful for us: \[\sigma(-t) = 1 - \sigma(t) \qquad \frac{\partial \sigma(t)}{\partial t} = \sigma(t) \sigma(-t)\]

Doing an analogous derivation for \(p(Y = -1 \mid X)\), we get \[
\begin{aligned}
\hat y=\arg\max_k p(Y=k|X) \Longleftrightarrow& \begin{cases}1 &\text{if } \sigma(X\beta+b)>\frac{1}{2}\\ -1 &\text{if } \sigma(X\beta+b)<\frac{1}{2}\end{cases}\\
\Longleftrightarrow& \begin{cases}1 &\text{if } X\beta+b>0\\ -1 &\text{if } X\beta+b<0\end{cases}\\
\Longleftrightarrow& \text{sign}(X\beta+b)
\end{aligned}\]


**Alternatives to training beta and b:**
1. fit mean and covariance of clusters
2. least-squares regression: \(\mathcal{L}(Y_i^*, \hat{Y}_i) = (Y_i^* - (X \beta + b))^2\) (same solution as \(1\))
3. Fisher's idea: define 1D scores \(Z_i = X_i \beta\) and chose \(\beta\) such that a threshold on \(Z_i\) has minimum error
	- define projection of the means \(\hat{\mu_{1}} = \mu_1 \beta, \hat{\mu_{-1}} = \mu_{-1}\beta\)
	- **intuition:** \(\hat{\mu}_1\) and \(\hat{\mu_{-1}}\) should be as far away as possible \[\beta = \argmax_\beta (\hat{\mu}_1 - \hat{\mu}_{-1})^2\]
	- doesn't quite work, because \(\tau \beta \implies \tau^2 (\hat{\mu}_{1} \hat{\mu}_{-1})\)
	- solution: scale by the variance \(\hat{\sigma}\): \(\hat{\sigma}_1 = \mathrm{Var}\left(Z_1 \mid Y_i^* = 1\right), \hat{\sigma}_{-1} \mathrm{Var}\left(Z_i \mid Y_i^* = -1\right)\), then we get \[\hat{\beta} = \argmax_{\beta} \frac{\left(\hat{\mu}_1 - \hat{\mu_{-1}}\right)^2}{\hat{\sigma}_1^2 + \hat{\sigma}_{-1}^2}\]
	- again gives the same solution as \(1\) and \(2\)
4. **Logistic regression (LR):** same posterior as LDA, but learn LHS of Bayes rule
	- gives different solution to LDA

##### Logistic regression (LR)

We again have i.i.d. assumptions -- all labels are drawn independently form the same posterior: \[p\left(\left(Y_i^*\right)_{i = 1}^N \mid \left(X_i\right)_{i = 1}^N\right) = \prod_{i = 1}^{N} p(Y_i^* \mid X_i)\]
- as a reminder, this was **swapped for LDA** (we had \(p(X \mid Y)\))
- use **maximum likelihood**: choose \(\hat{\beta}, \hat{b}\) such that posterior of TS is maximized: \[
\begin{aligned}
&\hat\beta,\hat b=\argmax_{\beta,b}\prod^N_{i=1}p(Y^*_i|X_i)\\
\Longleftrightarrow&\hat\beta,\hat b=\arg\min_{\beta,b}-\sum^N_{i=1}\log p(Y^*_i|X_i) \qquad \min + \log \text{ trick}
\end{aligned}\]

For LR, \(Y^*_i \in \left\{0, 1\right\}\), which allows us to rewrite (with the \(\sigma\) results from LDA) like so: \[
\boxed{\ \hat{\beta}, \hat{b}=\arg\min_{\beta, b}-\sum_{i=1}^N\Big[Y_i^* \log \sigma\left(X\beta+b\right)+\left(1-Y_i^*\right) \log \left(\sigma\left(-\left(X\beta+b\right)\right)\Big]\right.\ }
\]
- no analytic solution but **is convex** (local extreme = global extreme, solve via GD)

Here we have \(-\log(\sigma(-t)) = \log(1 + \exp(t))\), which is called the **softplus** function:

![ReLu + Softplus graphs.](/assets/introduction-to-machine-learning/relu-softplus.svg)

Simplifying for \(b = 0\) and using the following properties:

\[
\begin{aligned}
\frac{\partial \sigma\left(X\beta\right)}{\partial \beta}&=\sigma^{\prime}\left(X\beta\right) X=\sigma(X \beta) \sigma\left(-X\beta\right) \cdot X \\
\frac{\partial \log \sigma\left(X\beta\right)}{\partial \beta}&=\frac{1}{\sigma\left(X\beta\right)} \sigma\left(X\beta\right) \sigma\left(-X\beta\right) \cdot X=\sigma\left(X\beta\right) \cdot X \\
\frac{\partial \log \sigma\left(-X\beta\right)}{\partial \beta}&=\frac{1}{\sigma\left(-X\beta\right)} \sigma\left(X\beta\right) \sigma\left(-X\beta\right) \cdot(-X)=-\sigma\left(X\beta\right) \cdot X
\end{aligned}
\]

We get the derivatives \(\beta\):
\[
\begin{aligned}
\frac{\partial \mathcal Loss(T S)}{\partial \beta}&=-\sum_{i=1}^N\left[Y_i^* \underbrace{\sigma\left(-X_i \beta\right)}_{1-\sigma\left(X_i \beta\right)} \cdot X_i+\left(1-Y_i^*\right) \sigma\left(X_{i \beta}\right) \cdot\left(-X_i\right)\right] \\
& =-\sum_{i=1}^N\left[Y_i^* X_i-\cancel{Y_i^* \sigma\left(X_i \beta\right) X_i}-\sigma\left(X_i \beta\right) X_i+\cancel{Y_i^* \sigma\left(X_i \beta\right) X_i}\right]
\end{aligned}
\]

obtaining

\[
\boxed{\ \frac{\partial \mathcal Loss(T S)}{\partial \beta}=\sum_{i=1}^N(\underbrace{\sigma\left(X_i \beta\right)-Y_i^*}_{\text {error }}) \cdot X_i \stackrel{!}{=} 0\ }
\]

The four cases that can occur are as follows:

| Real value \ Classifier result | \(\sigma(X_i\beta)\approx 1\)                               | \(\sigma(X_i\beta)\approx 0\)                               |
| ---                            | ---                                                         | ---                                                         |
| \(Y^*_i=1\)                    | no correction                                               | error \(\approx-1\): pulls \(\sigma(X_i\beta)\rightarrow1\) |
| \(Y^*_i=0\)                    | error \(\approx 1\): pulls \(\sigma(X_i\beta)\rightarrow0\) | no correction                                               |
