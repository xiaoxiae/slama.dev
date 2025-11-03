---
language: cz
title: Příprava na státnice (MFF UK)
category: "poznamky"
category_noslug: "poznámky"
category_icon: /assets/category-icons/mff.webp
css: statnice
excerpt: Příprava na státní zkoušky z Obecné informatiky pro akademický rok 2021/2022 (tj. nová akreditace).
---

- .
{:toc}

Tento článek obsahuje mou přípravu na státní zkoušky z **Obecné informatiky** pro akademický rok **2021/2022** (tj. nová akreditace).
Podrobné informace o všech specializacích jsou k dispozici v [tomto PDF](https://www.mff.cuni.cz/cs/studenti/bakalarske-studium/statni-zaverecne-zkousky/bakalarske-statni-zkousky-studijniho-programu-informatika/detailni-pozadavky.pdf) (informace na této stránce jsou z 1.6.2022 updatu tohoto dokumentu).

U každé časti tématu je jeden nebo více odkazů (🔗) na zdroje, ze kterých je možné se téma učit.
U celých předmětů jsou vždy odkazy na zdroje (ať už se jedná poznámky, slidy či skripta).
Pokud je u předmětu symbol kartičky (🃏), tak je zahrnut v [tomto Anki balíčku](https://github.com/xiaoxiae/AnkiMFF), ze kterého může být dobré si celý předmět zopakovat.

### Obecná

#### Matematika

{% sttopics %}
	{% sttopic Matalýza | Matalýza 1 [<a href="/assets/priprava-na-statnice-mff-uk/ma1.pdf">skripta</a>, <a href="/assets/priprava-na-statnice-mff-uk/ma-derivate.pdf">derivace</a>, <a href="/assets/priprava-na-statnice-mff-uk/ma-integrate.pdf">integrály</a>, <a href="/assets/priprava-na-statnice-mff-uk/ma-limits.pdf">limity</a>] 🃏 %}
		{% stlink Reálná čísla | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.1 %}
		<li style='list-style-type: none;'><ul>
			<li> odmocnina ze dvou je iracionální </li>
			<li> \(\mathbb{R}\) je nespočetná množina </li>
		</ul></li>
		{% stlink Posloupnosti reálných čísel a jejich limity | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.2 | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.3 %}
		<li style='list-style-type: none;'><ul>
			<li> definice, aritmetika limit </li>
			<li> věta o dvou policajtech, limity a uspořádání </li>
		</ul></li>
		{% stlink Řady | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.2 | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.3 %}
		<li style='list-style-type: none;'><ul>
			<li> definice částečného součtu a součtu </li>
			<li> geometrická řada, harmonická řada </li>
		</ul></li>
		{% stlink Reálné funkce jedné reálné proměnné. | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.4 %}
		<li style='list-style-type: none;'><ul>
			{% stlink limita funkce v bodě | /assets/priprava-na-statnice-mff-uk/ma1.pdf#page=16 | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.6 %}
			<li style='list-style-type: none;'><ul>
				<li> definice, aritmetika limit </li>
				<li> vztah s uspořádáním </li>
				<li> limita složené funkce </li>
			</ul></li>
			{% stlink funkce spojité na intervalu | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.6 %}
			<li style='list-style-type: none;'><ul>
				<li> nabývání mezihodnot </li>
				<li> nabývání maxima </li>
			</ul></li>
		</ul></li>
		{% stlink Derivace a její aplikace  | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.7 | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.8 | https://en.wikipedia.org/wiki/Weierstrass_function %}
		<li style='list-style-type: none;'><ul>
			<li> definice a základní pravidla pro výpočet </li>
			<li> l’Hospitalovo pravidlo </li>
			<li> vyšetření průběhu funkcí: extrémy, monotonie a konvexita/konkavita </li>
			{% stlink Taylorův polynom se zbytkem | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.9 | https://brilliant.org/wiki/taylor-series-error-bounds/ %}
		</ul></li>
		{% stlink Integrály a jejich aplikace | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.10 %}
		<li style='list-style-type: none;'><ul>
			<li> primitivní funkce: definice a metody výpočtu (substituce, per-partes) </li>
			<li> Riemannův integrál: definice, souvislost s primitivní funkcí (Newtonovým integrálem) </li>
			<li> aplikace </li>
			<li style='list-style-type: none;'><ul>
				<li> odhady součtu řad (konečných i nekonečných) </li>
				<li> obsahy rovinných útvarů </li>
				<li> objemy a povrchy rotačních útvarů v prostoru </li>
				<li> délka křivky </li>
			</ul></li>
		</ul></li>
	{% endsttopic %}
	{% sttopic Algebra a lineární algebra | Lingebra 1 a 2 [<a href="/assets/priprava-na-statnice-mff-uk/la.pdf">skripta</a>] 🃏 %}
		{% stlink Grupy a podgrupy (definice, příklady, komutativita) | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.4 %}
		{% stlink Tělesa (definice, charakteristika tělesa, konečná tělesa) | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.4 %}
		{% stlink Vektorové prostory a podprostory. | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.5 %}
		<li style='list-style-type: none;'><ul>
			<li> vlastnosti a základní pojmy (lineární kombinace, lineární obal, generátory, lineární závislost a nezávislost, báze, dimenze, souřadnice) a jejich použití </li>
			<li> praktická dovednost testování lineární závislosti a nezávislosti, nalezení báze, určení dimenze atp. </li>
			<li> skalární součin a jeho vlastnosti </li>
			<li> norma a vztah se skalárním součinem, příklady </li>
			<li> kolmost, ortonormální báze, její vlastnosti a použití (nalezení souřadnic a projekce) </li>
		</ul></li>
		{% stlink Skalární součin, norma. | /assets/priprava-na-statnice-mff-uk/la.pdf#section.8.1 %}
		{% stlink Kolmost, ortonormální báze. | /assets/priprava-na-statnice-mff-uk/la.pdf#section.8.2 | /assets/priprava-na-statnice-mff-uk/la.pdf#section.8.3 | /assets/priprava-na-statnice-mff-uk/la.pdf#section.8.4 %}
		{% stlink Soustavy lineárních rovnic a množina řešení. | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.2 %}
		<li style='list-style-type: none;'><ul>
			<li> metody řešení, Gaussova a Gaussova-Jordanova eliminace, odstupňovaný tvar matice a jeho jednoznačnost (bez důkazu) </li>
		</ul></li>
		{% stlink Matice a operace s maticemi (součet, součin, transpozice) | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.3 | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.9 | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.11 %}
		<li style='list-style-type: none;'><ul>
			<li> interpretace součinu matic pomocí skládání lineárních zobrazení </li>
			<li> hodnost matice a její transpozice </li>
			{% stlink vlastní čísla a vlastní vektory matice a jejich geometrický význam a vlastnosti, vícenásobná vlastní čísla, spektrální poloměr | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.10 %}
			{% stlink charakteristický polynom, vztah vlastních čísel s kořeny polynomů | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.12 %}
		</ul></li>
	{% endsttopic %}
	{% sttopic Diskrétní matematika | Diskrétka [<a href="/poznamky-z-prednasky/diskretni-matematika/">poznámky</a>] 🃏, Kombagra 1 [<a href="/poznamky-z-prednasky/kombinatorika-a-grafy-i/">poznámky</a>] 🃏 %}
		{% stlink Relace. | /poznamky-z-prednasky/diskretni-matematika/#relace %}
		<li style='list-style-type: none;'><ul>
			<li> vlastnosti binárních relací (reflexivita, symetrie, antisymetrie, tranzitivita) </li>
		</ul></li>
		{% stlink Ekvivalence a rozkladové třídy. | /poznamky-z-prednasky/diskretni-matematika/#ekvivalence %}
		{% stlink Částečná uspořádání. | /poznamky-z-prednasky/diskretni-matematika/#uspořádání %}
		<li style='list-style-type: none;'><ul>
			<li> základní pojmy </li>
			{% stlink výška a šířka částečně uspořádané množiny, věta o dlouhém a širokém | /poznamky-z-prednasky/diskretni-matematika/#dlouh%C3%BD-a-%C5%A1irok%C3%BD %}
		</ul></li>
		{% stlink Funkce. | /poznamky-z-prednasky/diskretni-matematika/#funkce %}
		<li style='list-style-type: none;'><ul>
			<li> typy funkcí (prostá, na, bijekce) </li>
			<li> počty různých typů funkcí mezi dvěma konečnými množinami </li>
		</ul></li>
		{% stlink Permutace a jejich základní vlastnosti (počet a pevný bod). | /poznamky-z-prednasky/diskretni-matematika/#segway-do-kombinatorického-počítání %}
		{% stlink Kombinační čísla a vztahy mezi nimi, binomická věta a její aplikace. | /poznamky-z-prednasky/diskretni-matematika/#kombinatorika %}
		{% stlink Princip inkluze a exkluze. | /poznamky-z-prednasky/diskretni-matematika/#princip-inkluzeexkluze %}
		<li style='list-style-type: none;'><ul>
			<li> obecná formulace (a důkaz) </li>
			<li> použití (problém šatnářky, Eulerova funkce pro počet dělitelů, počet surjekcí) </li>
		</ul></li>
		{% stlink Hallova věta o systému různých reprezentantů, vztah k párování v bipartitním grafu. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#aplikace-tok%C5%AF-v-s%C3%ADt%C3%ADch %}
		<li style='list-style-type: none;'><ul>
			<li> princip důkazu a algoritmické aspekty (polynomiální algoritmus pro nalezení SRR) </li>
		</ul></li>
	{% endsttopic %}
	{% sttopic Teorie grafů | Diskrétka [<a href="/poznamky-z-prednasky/diskretni-matematika/">poznámky</a>] 🃏, Kombagra 1 [<a href="/poznamky-z-prednasky/kombinatorika-a-grafy-i/">poznámky</a>] 🃏 %}
		{% stlink Základní pojmy, základní příklady grafů. | /poznamky-z-prednasky/diskretni-matematika/#grafy %}
		{% stlink Souvislost grafů, komponenty souvislosti, vzdálenost v grafu. | /poznamky-z-prednasky/diskretni-matematika/#rozšiřování-grafů %}
		{% stlink Stromy. | /poznamky-z-prednasky/diskretni-matematika/#stromy %}
		<li style='list-style-type: none;'><ul>
			<li> definice a základní vlastnosti (existence listů, počet hran stromu) </li>
			<li> ekvivalentní charakteristiky stromů </li>
		</ul></li>
		{% stlink Rovinné grafy. | /poznamky-z-prednasky/diskretni-matematika/#rovinné-nakreslení-grafu %}
		<li style='list-style-type: none;'><ul>
			<li> definice a základní pojmy (rovinný graf a rovinné nakreslení grafu, stěny) </li>
			<li> Eulerova formule a maximální počet hran rovinného grafu (důkaz a použití) </li>
		</ul></li>
		{% stlink Barevnost grafů, klikovost grafů. | /poznamky-z-prednasky/diskretni-matematika/#barvení | /poznamky-z-prednasky/diskretni-matematika/#degenerovanost-klikovost-dualita %}
		<li style='list-style-type: none;'><ul>
			<li> definice dobrého obarvení </li>
			<li> vztah barevnosti a klikovosti grafu </li>
		</ul></li>
		{% stlink Hranová a vrcholová souvislost grafů, Mengerovy věty. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#míra-souvislosti-neorientovaných-grafu  %}
		{% stlink Orientované grafy, silná a slabá souvislost. | /poznamky-z-prednasky/diskretni-matematika/#rozšiřování-grafů  %}
		{% stlink Toky v sítích. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#7-přednáška | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s14  %}
		<li style='list-style-type: none;'><ul>
			<li> definice sítě a toku v ní </li>
			<li> existence maximálního toku (bez důkazu) </li>
			<li> princip hledání maximálního toku v síti s celočíselnými kapacitami (například pomocí Ford-Fulkersonova algoritmu) </li>
		</ul></li>
	{% endsttopic %}
	{% sttopic Past | Diskrétka [<a href="/poznamky-z-prednasky/diskretni-matematika/">poznámky</a>] 🃏, Past [<a href="/assets/priprava-na-statnice-mff-uk/past/slides.pdf">slidy</a>, <a href="/assets/priprava-na-statnice-mff-uk/past/cheatsheet.pdf">cheatsheet</a>, <a href="/assets/priprava-na-statnice-mff-uk/past/examples.pdf">příklady</a>] 🃏 %}
		<li> Pravděpodobnostní prostor, náhodné jevy, pravděpodobnost </li>
		<li style='list-style-type: none;'><ul>
			<li> definice těchto pojmů, příklady </li>
			<li> základní pravidla pro počítání s pravděpodobností </li>
			<li> nezávislost náhodných jevů, podmíněná pravděpodobnost </li>
			<li> Bayesův vzorec </li>
		</ul></li>
		<li> Náhodné veličiny a jejich rozdělení </li>
		<li style='list-style-type: none;'><ul>
			<li> diskrétní i spojitý případ </li>
			<li> popis pomocí distribuční funkce a pomocí pravděpodobnostní funkce/hustoty </li>
			<li> střední hodnota </li>
			<li style='list-style-type: none;'><ul>
				<li> linearita střední hodnoty </li>
				<li> střední hodnota součinu nezávislých veličin </li>
				<li> Markovova nerovnost </li>
			</ul></li>
			<li> rozptyl </li>
			<li style='list-style-type: none;'><ul>
				<li> definice </li>
				<li> vzorec pro rozptyl součtu (závislých či nezávislých veličin) </li>
			</ul></li>
			<li> práce s konkrétními rozděleními: geometrické, binomické, Poissonovo, normální, exponenciální </li>
		</ul></li>
		<li> Limitní věty </li>
		<li style='list-style-type: none;'><ul>
			<li> zákon velkých čísel </li>
			<li> centrální limitní věta </li>
		</ul></li>
		<li> Bodové odhady </li>
		<li style='list-style-type: none;'><ul>
			<li> alespoň jedna metoda pro jejich tvorbu </li>
			<li> vlastnosti </li>
		</ul></li>
		<li> Intervalové odhady: metoda založená na aproximaci normálním rozdělením </li>
		<li> Testování hypotéz </li>
		<li style='list-style-type: none;'><ul>
			<li> základní přístup </li>
			<li> chyby 1. a 2. druhu </li>
			<li> hladina významnosti </li>
		</ul></li>
	{% endsttopic %}
	{% sttopic Logika | Výpal [<a href="/assets/priprava-na-statnice-mff-uk/vypal-cz.pdf">slidy CZ</a>, <a href="/assets/priprava-na-statnice-mff-uk/vypal-en.pdf">slidy </a>] 🃏 %}
		<li> Syntaxe </li>
		<li style='list-style-type: none;'><ul>
			<li> znalost a práce se základními pojmy syntaxe výrokové a predikátové logiky (jazyk, otevřená a uzavřená formule, instance formule, apod.) </li>
			<li> normální tvary výrokových formulí </li>
			<li style='list-style-type: none;'><ul>
				<li> prenexní tvary formulí predikátové logiky </li>
				<li> znalost základních normálních tvarů (CNF, DNF, PNF) </li>
				<li> převody na normální tvary </li>
				<li> použití pro algoritmy (SAT, rezoluce) </li>
			</ul></li>
		</ul></li>
		<li> Sémantika </li>
		<li style='list-style-type: none;'><ul>
			<li> pojem modelu teorie </li>
			<li> pravdivost, lživost, nezávislost formule vzhledem k teorii </li>
			<li> splnitelnost, tautologie, důsledek </li>
			<li> analýza výrokových teorií nad konečně mnoha prvovýroky </li>
		</ul></li>
		<li> Extenze teorií </li>
		<li style='list-style-type: none;'><ul>
			<li> schopnost porovnat sílu teorií </li>
			<li> konzervativnost, skolemizace </li>
		</ul></li>
		<li> Dokazatelnost: </li>
		<li style='list-style-type: none;'><ul>
			<li> pojem formálního důkazu, zamítnutí </li>
			<li> schopnost práce v některém z formálních dokazovacích systémů (např. tablo metoda, rezoluce, Hilbertovský kalkul) </li>
		</ul></li>
		{% stlink Věty o kompaktnosti a úplnosti výrokové a predikátové logiky | /assets/priprava-na-statnice-mff-uk/vypal-en.pdf#page=85 | /assets/priprava-na-statnice-mff-uk/vypal-en.pdf#page=81 | /assets/priprava-na-statnice-mff-uk/vypal-en.pdf#page=79 %}
		<li style='list-style-type: none;'><ul>
			<li> znění a porozumění významu </li>
			<li> použití na příkladech, důsledky </li>
		</ul></li>
		{% stlink Rozhodnutelnost | /assets/priprava-na-statnice-mff-uk/vypal-en.pdf#page=273 %}
		<li style='list-style-type: none;'><ul>
			<li> pojem kompletnosti a její kritéria, význam pro rozhodnutelnost </li>
			<li> příklady rozhodnutelných a nerozhodnutelných teorií </li>
		</ul></li>
	{% endsttopic %}
{% endsttopics %}

#### Informatika

{% sttopics %}
	{% sttopic Automaty a jazyky | Autogramy [<a href="/assets/priprava-na-statnice-mff-uk/autogramy/skripta.pdf">skripta</a>, <a href="/assets/priprava-na-statnice-mff-uk/autogramy/slidy.pdf">slidy</a>] 🃏 %}
		<li> Regulární jazyky. </li>
		<li style='list-style-type: none;'><ul>
			<li> regulární gramatiky </li>
			<li> konečný automat, jazyk přijímaný konečným automatem </li>
			<li> deterministický a nedeterministický automat, lambda přechody </li>
			<li> regulární výrazy </li>
			<li> Kleeneho věta </li>
			<li> iterační (pumping) lemma pro konečné automaty </li>
		</ul></li>
		<li> Uzávěrové vlastnosti </li>
		<li> Bezkontextové jazyky. </li>
		<li style='list-style-type: none;'><ul>
			<li> bezkontextové gramatiky, jazyk generovaný gramatikou </li>
			<li> zásobníkový automat, třída jazyků přijímaných zásobníkovými automaty </li>
		</ul></li>
		<li> Turingův stroj. </li>
		<li style='list-style-type: none;'><ul>
			<li> gramatika typu 0 </li>
			<li> diagonální jazyk </li>
			<li> univerzální jazyk </li>
		</ul></li>
		<li> Chomského hierarchie. </li>
		<li style='list-style-type: none;'><ul>
			<li> určení ekvivalence či inkluze tříd jazyků generovaných výše uvedenými automaty a gramatikami </li>
			<li> schopnost zařazení konkrétního jazyka do Chomského hierarchie (zpravidla sestrojení odpovídajícího automatu či gramatiky a důkaz iteračním lemmatem, že jazyk není v nižší třídě) </li>
		</ul></li>
	{% endsttopic %}
	{% sttopic Algoritmy a datové stuktury | ADS 1 a 2 [<a href="/assets/priprava-na-statnice-mff-uk/pruvodce.pdf">Průvodce</a>, <a href="/assets/priprava-na-statnice-mff-uk/ga.pdf">GA</a>] 🃏 %}
		{% stlink Časová a prostorová složitost algoritmů. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s2  %}
		<li style='list-style-type: none;'><ul>
			<li> čas a prostor výpočtu pro konkrétní vstup </li>
			<li> časová a prostorová složitost algoritmu </li>
			<li> měření velikosti dat </li>
			<li> složitost v nejlepším, nejhorším a průměrném případě </li>
			<li> asymptotická notace </li>
		</ul></li>
		{% stlink Třídy složitosti. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s19.3 | /assets/priprava-na-statnice-mff-uk/pvnp.webp %}
		<li style='list-style-type: none;'><ul>
			<li> třídy P a NP </li>
			<li> převoditelnost problémů, NP-těžkost a NP-úplnost </li>
			<li> příklady NP-úplných problémů a převodů mezi nimi </li>
		</ul></li>
		{% stlink Metoda "rozděl a panuj". |  /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s10 %}
		<li style='list-style-type: none;'><ul>
			<li> princip rekurzivního dělení problému na podproblémy </li>
			<li> výpočet složitosti pomocí rekurentních rovnic </li>
			<li> Master theorem (kuchařková věta) </li>
			<li> aplikace </li>
			<li style='list-style-type: none;'><ul>
				<li> Mergesort </li>
				<li> násobení dlouhých čísel </li>
				<li> Strassenův algoritmus </li>
			</ul></li>
		</ul></li>
		{% stlink Binarní vyhledávací stromy. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s8 %}
		<li style='list-style-type: none;'><ul>
			<li> definice vyhledávacího stromu </li>
			<li> operace s nevyvažovanými stromy </li>
			<li> AVL stromy (definice) </li>
		</ul></li>
		{% stlink Binární haldy. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s4.2 %}
		{% stlink Hešování s přihrádkami a s otevřenou adresací. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s11.3 %}
		{% stlink Třídící algoritmy. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s3  %}
		<li style='list-style-type: none;'><ul>
			<li> primitivní třídicí algoritmy (Bubblesort, Insertsort) </li>
			<li> třídění haldou (Heapsort) </li>
			<li> Quicksort </li>
			<li> dolní odhad složitosti porovnávacích třídicích algoritmů </li>
			<li> přihrádkové třídění čísel a řetězců </li>
		</ul></li>
		{% stlink Grafové algoritmy. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s5 | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s6| /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s7 %}
		<li style='list-style-type: none;'><ul>
			{% stlink DFS, BFS a jejich aplikace. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s5 | https://stackoverflow.com/questions/20429310/why-is-depth-first-search-claimed-to-be-space-efficient %}
			{% stlink Nejkratší cesty (Dijkstra, BF). | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s6 %}
			{% stlink Minimální kostry (Jarník, Borůvka). | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s7 %}
			{% stlink Toky v sítích (FF). | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s14 | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#7-přednáška  %}
		</ul></li>
		{% stlink Euklidův algoritmus. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s1.3  %}
	{% endsttopic %}
	{% sttopic Programovací jazyky | Programko [<a href="/assets/priprava-na-statnice-mff-uk/prog2.pdf">poznámky</a>], Java/C#/C++ [<a href="/lecture-notes/the-cs-programming-language/">C# poznámky</a>] %}
	<li> Koncepty pro abstrakci, zapouzdření a polymorfismus. </li>
		<li style='list-style-type: none;'><ul>
		<li> související konstrukty programovacích jazyků </li>
			<li style='list-style-type: none;'><ul>
			<li> třídy, rozhraní, metody, datové položky, dědičnost, viditelnost </li>
			</ul></li>
		<li> (dynamický) polymorfismus, statické a dynamické typování </li>
		<li> jednoduchá dědičnost </li>
			<li style='list-style-type: none;'><ul>
			<li> virtuální a nevirtuální metody v C++ <del>a C#</del> </li>
			<li> <del>defaultní metody v Javě</del> </li>
			</ul></li>
		<li> <del>vícenásobná dědičnost a její problémy</del> </li>
			<li style='list-style-type: none;'><ul>
			<li> <del>vícenásobná a virtuální dědičnost v C++</del> </li>
			<li> <del>interfaces v Javě a C++</del> </li>
			</ul></li>
		<li> implementace rozhraní (interface) </li>
		</ul></li>
	<li> Primitivní a objektové typy a jejich reprezentace. </li>
	<li style='list-style-type: none;'><ul>
		<li> číselné a výčtové typy </li>
		<li> <del>ukazatele a reference v C++</del> </li>
		<li> hodnotové a referenční typy v C# </li>
		<li> imutabilní typy a boxing/unboxing v C# <del>a Javě</del> </li>
	</ul></li>
	<li> Generické typy a funkcionální prvky (procedurálních programovacích jazyků). </li>
	<li style='list-style-type: none;'><ul>
		<li> <del>šablony (templates) a statický polymorfismus v C++</del> </li>
		<li> generické typy v Javě a C# (bez omezení typových parametrů) </li>
		<li> typy reprezentující funkce v <del>C++</del>, C#, <del>nebo Javě</del> </li>
		<li> lambda funkce a funkcionální rozhraní </li>
	</ul></li>
	<li> Manipulace se zdroji a mechanizmy pro ošetření chyb. </li>
	<li style='list-style-type: none;'><ul>
		<li> správa životního cyklu zdrojů v případě výskytu chyb </li>
		<li style='list-style-type: none;'><ul>
			<li> <del>RAII v C++</del>, using v C#, <del>try-with-resources v Javě</del> </li>
		</ul></li>
		<li> konstrukce pro obsluhu a propagaci výjimek </li>
	</ul></li>
	<li> Životní cyklus objektů a správa paměti. </li>
	<li style='list-style-type: none;'><ul>
		<li> alokace (alokace statická, na zásobníku, na haldě) </li>
		<li> inicializace (konstruktory, volání zděděných konstruktorů) </li>
		<li> destrukce (destruktory, finalizátory) </li>
		<li> explicitní uvolňování objektů, reference counting, garbage collector </li>
	</ul></li>
	<li> Vlákna a podpora synchronizace. </li>
	<li style='list-style-type: none;'><ul>
		<li> reprezentace vláken v programovacích jazycích </li>
		<li> specifikace funkce vykonávané vláknem a základní operace na vlákny </li>
		<li> časově závislé chyby a mechanizmy pro synchronizaci vláken </li>
	</ul></li>
	<li> Implementace základních prvků objektových jazyků. </li>
	<li style='list-style-type: none;'><ul>
		<li> základní objektové koncepty v konkrétním jazyce (<del>Java</del>, <del>C++</del>, C#) </li>
		<li> implementace a interní reprezentace primitivních typů </li>
		<li> implementace a interní reprezentace složených typů a objektů </li>
		<li> implementace dynamického polymorfismu (tabulka virtuálních metod) </li>
	</ul></li>
	<li> Nativní a interpretovaný běh, řízení překladu a sestavení programu. </li>
		<li style='list-style-type: none;'><ul>
		<li> reprezentace programu, bytecode, interpret jazyka </li>
		<li> just-in-time (JIT) a ahead-of-time (AOT) překlad </li>
		<li> proces sestavení programu, oddělený překlad, linkování </li>
		<li> staticky a dynamicky linkované knihovny </li>
		<li> běhové prostředí procesu a vazba na operační systém </li>
		</ul></li>
	{% endsttopic %}
	{% sttopic Architektura počítačů a OS | Principy poč. [<a href="/poznamky-z-prednasky/principy-pocitacu/">poznámky</a>] 🃏, Poč. systémy [<a href="/assets/priprava-na-statnice-mff-uk/ps.pdf">slidy</a>] %}
		{% stlink Základní architektura počítače. | /poznamky-z-prednasky/principy-pocitacu/#zjednodu%C5%A1en%C3%A9-sch%C3%A9ma-po%C4%8D%C3%ADta%C4%8De | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=24 %}
		<li style='list-style-type: none;'><ul>
			<li> reprezentace a přístup k datům v paměti, adresa, adresový prostor </li>
			<li> ukládání jednoduchých a složených datových typů </li>
			<li> základní aritmetické a logické operace </li>
		</ul></li>
		{% stlink Reprezentace dat a programů. | /poznamky-z-prednasky/principy-pocitacu/#k%C3%B3dov%C3%A1n%C3%AD-informace-v-po%C4%8D%C3%ADta%C4%8Di | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=60 %}
		{% stlink Instrukční sada, vazba na vyšší programovací jazyky. | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=29 %}
		<li style='list-style-type: none;'><ul>
			<li> Implementovat běžné programové konstrukce vyšších jazyků (přiřazení, podmínka, cyklus, volání funkce) pomocí instrukcí procesoru </li>
			<li> Zapsat běžnou konstrukci vyššího jazyka (přiřazení, podmínka, cyklus, volání funkce), která odpovídá zadané sekvenci (vysvětlených) instrukcí procesoru </li>
		</ul></li>
		{% stlink Podpora pro běh operačního systému. | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=97  %}
		<li style='list-style-type: none;'><ul>
			<li> privilegovaný a neprivilegovaný režim procesoru </li>
			<li> jádro operačního systému </li>
		</ul></li>
		{% stlink Rozhraní periferních zařízení a jejich obsluha. | /poznamky-z-prednasky/principy-pocitacu/#otro%C4%8Dina | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=105  %}
		<li style='list-style-type: none;'><ul>
			<li> Popsat roli řadiče zařízení při programem řízené obsluze zařízení (PIO), pro zadané adresy a funkce vstupních a výstupních portů implementovat programem řízenou obsluhu zadaného zařízení (myš, disk) </li>
			<li> Popsat roli přerušení při programem řízené obsluze zařízení (PIO), na úrovni vykonávání instrukcí popsat reakci procesoru (hardware) a operačního systému (software) na žádost o přerušení </li>
		</ul></li>
		{% stlink Základní abstrakce, rozhraní a mechanizmy OS pro běh programů, sdílení prostředků a vstup/výstup. | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=97  %}
		<li style='list-style-type: none;'><ul>
			<li> neprivilegované (uživatelské) procesy </li>
			<li> sdílení procesoru </li>
			<li style='list-style-type: none;'><ul>
				<li> procesy, vlákna, kontext procesu a vlákna </li>
				<li> přepínání kontextu, kooperativní a preemptivní multitasking </li>
				<li> plánování běhu procesů a vláken, stavy vlákna </li>
			</ul></li>
			<li> sdílení paměti </li>
			<li style='list-style-type: none;'><ul>
				<li> Vysvětlit rozdíl mezi virtuální a fyzickou adresou a identifikovat, zda se v zadaném kontextu či fragmentu kódu používá virtuální nebo fyzická adresa </li>
				<li> Na zadaném příkladu identifikovat a vysvětlit význam komponent virtuální a fyzické adresy (číslo stránky, číslo rámce, offset) </li>
				<li> Pro konkrétní adresy a obsah jednoúrovňové stránkovací tabulky řešit úlohy překladu adres </li>
				<li> Vysvětlit roli virtuálních adresových prostorů v ochraně paměti procesů a vláken </li>
			</ul></li>
			<li> sdílení úložného prostoru </li>
			<li style='list-style-type: none;'><ul>
				<li> soubory, analogie s adresovým prostorem </li>
				<li> abstrakce a rozhraní pro práci se soubory </li>
			</ul></li>
		</ul></li>
		{% stlink Paralelismus, vlákna a rozhraní pro jejich správu, synchronizace vláken. | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=112 %}
		<li style='list-style-type: none;'><ul>
			<li> časově závislé chyby (race conditions) </li>
			<li> kritická sekce, vzájemné vyloučení </li>
			<li> základní sychronizační primitiva, jejich rozhraní a použití </li>
			<li style='list-style-type: none;'><ul>
				<li> zámky </li>
				<li> aktivní a pasivní čekání </li>
			</ul></li>
		</ul></li>
	{% endsttopic %}
{% endsttopics %}

### Specifická
Z následujících témat je třeba umět **všechna** z 1-3 a **dvě** z 4-7 (vybírá se v SISu).

{% sttopics %}
	{% sttopic Kombinatorika | Kombagra 1 [<a href="/poznamky-z-prednasky/kombinatorika-a-grafy-i/">poznámky</a>] 🃏 a 2 [<a href="/poznamky-z-prednasky/kombinatorika-a-grafy-ii/">poznámky</a>] 🃏 %}
		{% stlink Vytvořující funkce. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#generuj%C3%ADc%C3%AD-funkce %}
		<li style='list-style-type: none;'><ul>
			<li> použití vytvořujících funkcí k řešení lineárních rekurencí </li>
			<li> zobecněná binomická věta (formulace) </li>
			<li> Catalanova čísla (příklad kombinatorické interpretace, odvození vzorce) </li>
		</ul></li>
		{% stlink Odhady faktoriálů a kombinačních čísel. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#odhady-faktori%C3%A1lu | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#odhady-binomických-koeficientů %}
		<li style='list-style-type: none;'><ul>
			<li> \((n/e)^n \le n! \le n(n/e)^n\) </li>
			<li> \((n/k)^k \le \binom{n}{k} \le (en/k)^k\) </li>
			<li> \(2^{2m}/(2  \sqrt{m}) \le \binom{2m}{m} \le 2^{2m} / \sqrt{2m}\) </li>
		</ul></li>
		{% stlink Ramseyova teorie. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#ramseyovy-barevn%C3%A9nekone%C4%8Dn%C3%A9-v%C4%9Bty %}
		<li style='list-style-type: none;'><ul>
			<li> Ramseyova věta (formulace konečné a nekonečné verze pro p-tice, důkaz verze \(p=2\) pro 2 barvy) </li>
			<li> Ramseyova čísla (definice, pro 2 barvy horní odhad z důkazu Ramseyovy věty a dolní odhad pravděpodobnostní konstrukcí) </li>
		</ul></li>
		{% stlink Extremální kombinatorika | /poznamky-z-prednasky/kombinatorika-a-grafy-ii/#extrem%C3%A1ln%C3%AD-teorie-graf%C5%AF-a-hypergraf%C5%AF %}
		<li style='list-style-type: none;'><ul>
			<li> obecné povědomí co extremální kombinatorika studuje </li>
			<li> Turánova věta (formulace, Turánovy grafy) </li>
			<li> Erdös-Ko-Radoova věta (formulace) </li>
		</ul></li>
		{% stlink Samoopravné kódy. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#samoopravn%C3%A9-k%C3%B3dy %}
		<li style='list-style-type: none;'><ul>
			<li> přehled o používané terminologii </li>
			<li> vzdálenost kódu a její vztah k počtu opravitelných a detekovatelných chyb </li>
			<li> Hammingův odhad (formulace a důkaz) </li>
			<li> perfektní kódy (definice a příklady, Hammingův kód bez přesné konstrukce) </li>
		</ul></li>
	{% endsttopic %}
	{% sttopic Základy sítí | Sítě [<a href="/assets/priprava-na-statnice-mff-uk/site.pdf">slidy</a>] 🃏 %}
		<li> Taxonomie počítačových sítí. </li>
		<li> Architektura ISO/OSI. </li>
		<li> Přehled síťového modelu TCP/IP. </li>
		<li> Směrování. </li>
		<li> Koncept adresy, portu, socketu. </li>
		<li> Architektura klient/server. </li>
		<li> Základy fungování protokolů HTTP, FTP a SMTP. </li>
	{% endsttopic %}
	{% sttopic Matalýza 2  | Matalýza 2 [<a href="/assets/priprava-na-statnice-mff-uk/ma2.pdf">poznámky Pultr</a>, <a href="/assets/priprava-na-statnice-mff-uk/ma2-klazar.pdf">poznámky Klazar</a>] 🃏 %}
		<li> Riemannův integrál jedno- i vícerozměrný </li>
		<li> Funkce více proměnných </li>
			<li style='list-style-type: none;'><ul>
			<li> parciální derivace: definice a výpočet </li>
			<li> výpočet extrémů pomocí paricálních derivací </li>
			<li> existence extrémů pro funkce několika reálných proměnných </li>
			<li> vázané extrémy: výpočet pomocí Lagrangeových multiplikátorů </li>
			</ul></li>
		<li> Metrický prostor </li>
			<li style='list-style-type: none;'><ul>
			<li> definice a základní příklady </li>
			<li> otevřené a uzavřené množiny: definice, příklady </li>
			<li> spojitost funkce na metrickém prostoru </li>
			<li> kompaktnost: definice a důsledky pro extrémy funkcí více proměnných </li>
			<li> stejnoměrná spojitost </li>
			</ul></li>
	{% endsttopic %}
	{% sttopic Optimalizace | LP [<a href="/assets/priprava-na-statnice-mff-uk/lp.pdf">skripta</a>] 🃏, APX [<a href="/poznamky-z-prednasky/aproximacni-algoritmy/">pozn.</a>] 🃏, Kombagra 2 [<a href="/poznamky-z-prednasky/kombinatorika-a-grafy-ii/">pozn.</a>] 🃏, DSPO [<a href="/poznamky-z-prednasky/diskretni-a-spojita-optimalizace/">pozn.</a>] %}
		<li> Základy lineárního a celočíselného programování. </li>
		<li style='list-style-type: none;'><ul>
			<li> dualita lineárního programování, Farkasovo lemma </li>
			{% stlink simplexová metoda, pivotovací pravidla | /assets/priprava-na-statnice-mff-uk/lp-simplex.pdf %}
		</ul></li>
		<li> Kombinatorická geometrie </li>
		<li style='list-style-type: none;'><ul>
			<li> konvexní obal objektů </li>
			<li> mnohostěny </li>
			<li> Minkowski-Weylova věta </li>
		</ul></li>
		{% stlink Edmondsův algoritmus. | /poznamky-z-prednasky/kombinatorika-a-grafy-ii/#nejv%C4%9Bt%C5%A1%C3%AD-p%C3%A1rov%C3%A1n%C3%AD | https://www.youtube.com/watch?v=3roPs1Bvg1Q %}
		<li> Základy matematického programování </li>
			<li style='list-style-type: none;'><ul>
			<li>unimodularita, Königovo lemma, toky v sítích, souvislost s dualitou LP </li>
			<li>vážené maximální párování v bipartitních grafech a jeho primárně-duální algoritmus </li>
			</ul></li>
		<li> Celočíselné programování. </li>
		<li style='list-style-type: none;'><ul>
			{% stlink metoda řezů | https://en.wikipedia.org/wiki/Cutting-plane_method %}
		</ul></li>
		{% stlink Matroidy. | /poznamky-z-prednasky/diskretni-a-spojita-optimalizace/ %}
		<li style='list-style-type: none;'><ul>
			<li> řádová funkce, existence a submodularita </li>
			<li> hladový algoritmus </li>
		</ul></li>
		{% stlink Aproximační algoritmy pro kombinatorické problémy: | /poznamky-z-prednasky/aproximacni-algoritmy/ %}
		<li style='list-style-type: none;'><ul>
			<li> definice: aproximační poměr, aproximační schéma </li>
			{% stlink splnitelnost | /lecture-notes/best-sat/ %}
			{% stlink nezávislé množiny | /poznamky-z-prednasky/aproximacni-algoritmy/#maximální-nezávislá-množina %}
			{% stlink množinové pokrytí | /poznamky-z-prednasky/aproximacni-algoritmy/#pokrývací-problémy %}
			{% stlink rozvrhování | /poznamky-z-prednasky/aproximacni-algoritmy/#rozvrhov%C3%A1n%C3%AD %}
		</ul></li>
		<li> Použití lineárního programování pro aproximační algoritmy. </li>
		<li style='list-style-type: none;'><ul>
			{% stlink algoritmy pro splnitelnost (MAXSAT, pravděpodobnostní zaokrouhlování) | /poznamky-z-prednasky/aproximacni-algoritmy/#lp-sat %}
			{% stlink vrcholové a množinové pokrytí (deterministické zaokrouhlování, primárně-duální algoritmus) | /poznamky-z-prednasky/aproximacni-algoritmy/#pokrývací-problémy %}
		</ul></li>
		<li> Využití pravděpodobnosti při návrhu algoritmů. </li>
		<li style='list-style-type: none;'><ul>
			{% stlink minimální globální řez v grafu | /poznamky-z-prednasky/aproximacni-algoritmy/#glob%C3%A1ln%C3%AD-minim%C3%A1ln%C3%AD-%C5%99ez %}
			{% stlink hashování a jeho využítí pro slovník s konstantním časem vyhledávání | /poznamky-z-prednasky/aproximacni-algoritmy/#hashovac%C3%AD-funkce %}
			{% stlink pravděpodobnostní testování maticových a polynomiálních identit | /poznamky-z-prednasky/aproximacni-algoritmy/#nulovost-polynom%C5%AF-polynomial-identity-testing %}
			{% stlink paralelní algoritmus pro hledání maximální nezávislé množiny | /poznamky-z-prednasky/aproximacni-algoritmy/#maxim%C3%A1ln%C3%AD-nez%C3%A1visl%C3%A1-mno%C5%BEina %}
			{% stlink paralelní algoritmy pro hledání párování (bipartitní grafy) | /poznamky-z-prednasky/aproximacni-algoritmy/#perfektn%C3%AD-p%C3%A1rov%C3%A1n%C3%AD %}
		</ul></li>
	{% endsttopic %}
	{% sttopic Pokročilé ADS | ADS 1 a 2 [<a href="/assets/priprava-na-statnice-mff-uk/pruvodce.pdf">Průvodce</a>, <a href="/assets/priprava-na-statnice-mff-uk/ga.pdf">GA</a>] 🃏, APX [<a href="/poznamky-z-prednasky/aproximacni-algoritmy/">poznámky</a>] 🃏, Algebra 1 [<a href="/assets/priprava-na-statnice-mff-uk/algebra.pdf">skripta</a>] %}
		{% stlink Dynamické programování. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s12 %}
		<li style='list-style-type: none;'><ul>
			<li> princip dynamického programování (řešení podproblémů od nejmenších k největším) </li>
			{% stlink aplikace: nejdelší rostoucí podposloupnost, editační vzdálenost | /assets/priprava-na-statnice-mff-uk/lis.py | /assets/priprava-na-statnice-mff-uk/edit.py %}
		</ul></li>
		{% stlink Výpočetní model RAM. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s2.5 %}
		{% stlink Komponenty silné souvislosti orientovaných grafů. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s5.9 %}
		<li style='list-style-type: none;'><ul>
			<li> tranzitivní uzávěr (Floyd-Warshal) </li>
			<li> komponenty silné souvislosti orientovaných grafů </li>
			<li> toky v sítích (Dinicův a Goldbergův algoritmus) </li>
		</ul></li>
		{% stlink Toky v sítích (FF, Diniz, Goldberg). | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s14 | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#7-přednáška %}
		{% stlink Vyhledávání v textu (KMP, AC). | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s13 | /assets/priprava-na-statnice-mff-uk/kmp.py  %}
		<li style='list-style-type: none;'><ul>
			<li> algoritmy Knuth-Morris-Pratt a Aho-Corasicková </li>
		</ul></li>
		{% stlink Diskrétní Fourierova transformace, aplikace. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s17 | /assets/priprava-na-statnice-mff-uk/fft.py %}
		<li style='list-style-type: none;'><ul>
			<li> diskrétní Fourierova transformace a její aplikace </li>
			<li> výpočet Fourierovy transformace algoritmem FFT </li>
		</ul></li>
		{% stlink RSA (šifrování, dešifrování a generování klíčů) | /assets/priprava-na-statnice-mff-uk/algebra.pdf#subsection.2.2 %}
		{% stlink Aproximační algoritmy a schémata (cestující, batoh). | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s19.6 | /poznamky-z-prednasky/aproximacni-algoritmy/#metrický-tsp %}
		<li style='list-style-type: none;'><ul>
			<li> poměrová a relativní chyba </li>
			<li> aproximační schémata </li>
			<li> příklady: obchodní cestující, batoh </li>
		</ul></li>
		{% stlink Paralelní třidění pomocí komparátorových sítí. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s15 %}
		<li> Červeno-černé stromy a jejich vyvažování </li>
	{% endsttopic %}{% endsttopics %} <hr><div class="stignored"> {% sttopics 6 %}
	{% sttopic ❌ Geometrie ❌ | Základy KVG %}
		<li> Základní věty o konvexních množinách (Hellyho, Radonova, o oddělování). </li>
		<li> Minkowského věta o mřížkách. </li>
		<li> Konvexní mnohostěny (zákadní vlastnosti, V-mnohostěny, H-mnohostěny, kombinatorická složitost). </li>
		<li> Geometrická dualita. </li>
		<li> Voroného diagramy, arrangementy (komplexy) nadrovin, incidence bodů a přímek, základní algoritmy výpočetní geometrie (konstrukce arrangementu přímek v rovině, konstrukce konvexního obalu v rovině). </li>
	{% endsttopic %}
	{% sttopic ❌ Pokročilá diskrétní matematika ❌ | Kombagra 2, Teorie množin %}
		<li> Barvení grafů (Brooksova a Vizingova věta). </li>
		<li> Tutteova věta. </li>
		<li> Extremální kombinatorika (Turánova věta, Erdös-Ko-Radoova věta). </li>
		<li> Kreslení grafů na plochách. </li>
		<li> Množiny a zobrazení. </li>
		<li> Subvalence a ekvivalence množin. </li>
		<li> Dobré uspořádání. </li>
		<li> Axiom výběru (Zermelova věta, Zornovo lemma). </li>
	{% endsttopic %}
{% endsttopics %}
</div>

### Poděkování
- **shrekofspeed** (Discord) za upozornění na [požadavky](https://www.mff.cuni.cz/cs/studenti/bakalarske-studium/statni-zaverecne-zkousky/bakalarske-statni-zkousky-studijniho-programu-informatika/detailni-pozadavky.pdf) a na Medvědovo [Grafové Algoritmy](/assets/priprava-na-statnice-mff-uk/ga.pdf)
