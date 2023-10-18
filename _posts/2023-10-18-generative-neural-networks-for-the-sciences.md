---
title: Generative Neural Networks for the Sciences
category: "notes"
category_icon: /assets/category-icons/heidelberg.webp
excerpt: Lecture notes from the Generative Neural Networks for the Sciences course (Ullrich Köthe, 2023/2024).
---

- .
{:toc}
{% lecture_notes_preface_heidelberg Ullrich Köthe|2023/2024%}

### Introduction to generative modeling

- **assumption:**
    - "nature" works according to some hidden mechanisms (complicated probability distribution)
    - \(x\) is sampled from the true probability / generating process \(x \tilde p^*(X)\) (or \(\hat p\))
    - we have a training set \(TS = \left\{X_i \tilde p^*(X)\right\}_{i=1}^n\)
        - use \(TS\)A to learn \(p(X) \approx p^*(X)\)
- **goal:**
    - find approximation \(x \tilde p(X)\) (for \(\hat p\))
- **two aspects** of generative modeling (neural network can usually do both):
    1. **inference** -- given some data instance \(X_i\), calculate value of \(p(X_i)\)
    2. **generation** -- create synthetic data \(X \tilde p(X)\) which is indistinguishable from real data \(X \tilde p^*(X)\)
- **downstream benefits** of generative modelling
    - **powerful tool** for humans (e.g. chat bot as personal teacher)
        - great for things that are well-established
        - poor for things that aren't (tends to hallucinate)
    - helps to **produce insight**: identify important factors influencing the outcome
        - ex. "symbolic regression": find / learn analytic formulas to explain the reality (vanilla neural networks are black boxes)
    - use \(p(X)\) for decision making: is treatment \(A\) better than treatment \(B\) for patient \(X\)?

>  (Richard Feynman)
