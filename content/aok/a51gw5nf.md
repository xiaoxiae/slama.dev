---
noHeading: true
title: "Advent of Kačka: 2. problém 🖥️ (pokračování)"
noindex: true
---

### 2. problém 🖥️ (pokračování)

Po zadání hesla do počítače se na obrazovce objeví okno s textem **`"ŠPATNÉ HESLO!"`**.

To, že heslo bylo třeba zkrátit, ti přijde podezřelé.
Po chvíli přemýšlení si uvědomíš, že po **rozdělení na řádky po 7 znacích** se jedná o **stejný problém.**

Pro papír který jsme již viděli:

<div class="highlight"><pre><code><span class="gray">y6r</span>b<span class="blue">rqq</span>
<span class="blue">rqq</span>1<span class="orange">l7u</span>
<span class="orange">l7u</span>4<span class="blue">yi5</span>
<span class="blue">yi5</span>h<span class="orange">0u4</span>
<span class="orange">0u4</span>1<span class="blue">i7a</span>
<span class="blue">i7a</span>y<span class="orange">jz9</span>
<span class="orange">jz9</span>3<span class="blue">ltk</span>
<span class="blue">ltk</span>1<span class="orange">w5v</span>
<span class="orange">w5v</span>y<span class="blue">2y2</span>
<span class="blue">2y2</span>3<span class="orange">q8o</span>
<span class="orange">q8o</span>i<span class="blue">f3v</span>
<span class="blue">f3v</span>v<span class="orange">5ma</span>
<span class="orange">5ma</span>z<span class="blue">djr</span>
<span class="blue">djr</span>x<span class="gray">84x</span>
</code></pre></div>

dostáváme po odstranění překryvů text `b14h1y31y3ivzx`. Ten můžeme rozdělit po 7 znacích:

<div class="highlight"><pre><code><span class="gray">b14</span><strong>h</strong><span class="blue">1y3</span>
<span class="blue">1y3</span><strong>i</strong><span class="gray">vzx</span>
</code></pre></div>

a po odstranění překryvů dostáváme **`hi`**, což už na skupiny po 7 znacích dělit nejde.

Budeme-li tento proces opakovat dokud je text rozdělitelný na skupiny po 7 znacích, **jaké je heslo po odstranění všech překryvů?** [[vstup je stále stejný](/aok/12368642.in)]
