---
title: GPU Computing
category: "notes"
category_icon: /assets/category-icons/heidelberg.webp
---

- .
{:toc}

{% lecture_notes_preface_heidelberg Kazem Shekofteh|2022/2023%}

### Lecture overview

1. Introduction [[slides](/assets/gpu-computing/01.pdf)]
2. CUDA Programming [[slides](/assets/gpu-computing/02.pdf)]
3. TODO [[slides](/assets/gpu-computing/03.pdf)]
4. TODO [[slides](/assets/gpu-computing/04.pdf)]
5. TODO [[slides](/assets/gpu-computing/05.pdf)]
6. TODO [[slides](/assets/gpu-computing/06.pdf)]
7. TODO [[slides](/assets/gpu-computing/07.pdf)]
8. TODO [[slides](/assets/gpu-computing/08.pdf)]
9. TODO [[slides](/assets/gpu-computing/09.pdf)]
10. TODO [[slides](/assets/gpu-computing/10.pdf)]
11. TODO [[slides](/assets/gpu-computing/11.pdf)]
12. TODO [[slides](/assets/gpu-computing/12.pdf)]
13. TODO [[slides](/assets/gpu-computing/13.pdf)]

### Bulk-Synchronous Parallel (BSP) model
- established in 1990
- attempt to describe GPU computing
- parallel programs are split into **supersteps**
	1. _compute_ something
	2. _communicate_ what you did
	3. _synchronize_ with other processors
- **parallel slackness:** number of virtual processors \(v\), physical processors \(p\)
	- \(v = 1\): not viable
	- \(v = p\): unpromising wrt. optimality
	- \(v \gg p\): leverages slack to schedule and pipeline computation

### Scaling rules

#### Moore's law
- 1965: **number of transistors will double each year**
- 1975: every two years
- _other variants exist:_
	- CPU performance will double every 18 months,
	- memory size four times every three years, etc.

#### Amdahl's law
We want to find the **maximum possible improvement**, when given
- \(P\) parallel time of the task, \(S\) serial time of the task, \(P + S = 1\)
- \(N\) parallel execution units

\[\mathrm{Speedup} = \frac{1}{S + \frac{P}{N}}\]

