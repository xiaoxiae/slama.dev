---
language: cz
title: Advent of Kačka
layout: default
permalink: /aok/
css: aok
---

> Nazdar lemro.
> 
> Jelikož jsi AoC letos nedělala (Matlab je pain), tak jsem vánoční dárek schoval za pár problémů, které musíš vyřešit před tím než ho dostaneš. \*ďábelský smích\*
> 
> Miluju tě <span class="nostyle">❤️</span>.

Sedíš ve svém oblíbeném [Starbucksu na severním pólu](https://www.starbucks.com/store-locator/store/1011975/safeway-north-pole-1821-301-n-santa-claus-lane-north-pole-ak-997056081-us), piješ Mocha Cookie Crumble Frappuccino a pročítáš abstrakt článku o rakovině 2.0 kterou nedávno vydal Apple.
Je pátek ráno a všichni ostatní (kromě Elfů, kteří ti uvařili kafe) ještě spí.

<span class="quote">"Řešil už někdo účetnictví? Santa dorazí každou chvíli."</span>, prohlásí elf Jep.

<span class="quote">"Já ho řešil minulý rok, neměl ho řešit Jax?"</span>, odpoví elf Ron.

<span class="quote">"Na mě to neházejte, já sčítat neumím..."</span> pokračuje hádka.

Po chvíli se elfové přestanou hádat a všichni odejdou do skladu, ze kterého přinesou několik hromad papírů obsahujících účetnictví.
Z jejich výrazů a nepořádku v papírech je nejspíš čeká dlouhý den.

<span class="quote">"Kde je ta tabulka s výdaji na jídlo pro soby? Aktualizoval někdo seznam těch, kdo pořizují nové herní konzole? Kolik stála oprava toho stroje na zmrzlinu?"</span>, čas od času zaslechneš.

Je očividné, že účetnictví není jejich silná stránka (kafe zato dělají výborné).
Jelikož máš zrovna hodně věcí na práci, tak se rozhodneš prokrastinovat a elfům s jejich situací pomoci.

<span class="quote">"Vše v pořádku?"</span>, zeptáš se.

<span class="quote">"Ne! Santa je na cestě a v našem účetnictví je naprostý chaos! Pokud ho do Santova příjezdu nevyřešíme, tak z nás udělá klobásy!"</span>, elfové zoufale prohlásí.

<span class="quote">"Nechte to na mě -- je důvod, proč mi říkají MatematiKačka."</span> odpovíš. Je na čase sčítat.

---

### 1. problém 💰

Elfové ti ukáží dlouhý seznam čísel, který obsahuje příjmy a výdaje za tuto [polární noc](https://en.wikipedia.org/wiki/Polar_night).
K tomu, aby jej šlo uzavřít, je třeba spočítat **celkový zisk**, který je roven **součtu** všech příjmů a výdajů.

Například pro seznam

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>+46 'Bottled Evolution Fresh Organic Strawberry Lemonade'
+53 'Iced Very Berry Hibiscus Refreshers Beverage'
+98 'Doubleshot Energy Hazelnut Drink Frappuccino'
-25 'Soudní Spor (Smrt Zákazníka)'
+31 'Iced White Chocolate Mocha'
-13 'Čivava'
-88 'Daň Satanovi'
+12 'Iced Caramel Brule Latte Frappuccino'
-26 'Tsunami'
+75 'Vanilla Latte'
</code></pre></div></div>

můžeme položky sečíst

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class='green'>+46</span> <span class="gray">'Bottled Evolution Fresh Organic Strawberry Lemonade'</span>
<span class='green'>+53</span> <span class="gray">'Iced Very Berry Hibiscus Refreshers Beverage'</span>
<span class='green'>+98</span> <span class="gray">'Doubleshot Energy Hazelnut Drink Frappuccino'</span>
<span class='red'>-25</span> <span class="gray">'Soudní Spor (Smrt Zákazníka)'</span>
<span class='green'>+31</span> <span class="gray">'Iced White Chocolate Mocha'</span>
<span class='red'>-13</span> <span class="gray">'Čivava'</span>
<span class='red'>-88</span> <span class="gray">'Daň Satanovi'</span>
<span class='green'>+12</span> <span class="gray">'Iced Caramel Brule Latte Frappuccino'</span>
<span class='red'>-26</span> <span class="gray">'Tsunami'</span>
<span class='green'>+75</span> <span class="gray">'Vanilla Latte'</span>
---
163
</code></pre></div></div>

a dostaneme celkový zisk **`163`**.

**Jaký je celkový zisk?** [[klikni sem pro vstup](/aok/acka.in)]

---

_Další část vždy najdeš na <code class="language-plaintext highlighter-rouge">https://slama.dev/aok/<strong>&lt;řešení problému&gt;</strong></code>._
