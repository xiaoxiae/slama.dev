---
language: cz
title: Příprava na státnice (MFF UK)
css: statnice
---

- .
{:toc}

_<strong>UPOZORNĚNÍ (7.6.2022):</strong> zdá se, že termíny vyvěšené na nástěnce <strong>platily pouze pro starou akreditaci.</strong> Všichni, kteří jsou aktuálně přihlášeni na státnice, by již termín (zoušky i obhajoby) měli mít zapsaný, termíny proto odstraňuji._

_<strong>UPOZORNĚNÍ (2.6.2022):</strong> pokud jste článek četli před 2.6.2022, tak u témat specifických pro obecnou informatiku bylo napsáno, že je třeba vybrat pouze jedno z prvních tří témat. <strong>Tomu tak není</strong> -- dokument byl 1.6.2022 upraven (přes to, že by podle dokumentu neměly úpravy v rozmezí měsíce před státnicemi přidávat požadavky)._

Tento článek obsahuje mou přípravu na státní zkoušky z **Obecné informatiky** pro akademický rok **2021/2022** (tj. nová akreditace).
Podrobné informace o všech specializacích jsou k dispozici v [tomto PDF](https://www.mff.cuni.cz/cs/studenti/bakalarske-studium/statni-zaverecne-zkousky/bakalarske-statni-zkousky-studijniho-programu-informatika/detailni-pozadavky.pdf) (informace na této stránce jsou z 1.6.2022 updatu tohoto dokumentu).

U každé časti tématu je jeden nebo více odkazů (🔗) na zdroje, ze kterých je možné se téma učit.
U celých předmětů jsou vždy odkazy na zdroje (ať už se jedná poznámky, slidy či skripta).
Pokud je u předmětu symbol kartičky (🃏), tak je zahrnut v [tomto Anki balíčku](https://github.com/xiaoxiae/AnkiMFF), ze kterého může být dobré si celý předmět zopakovat.

### Obecná

#### Matematika

{% sttopics %}
	{% sttopic Matalýza | Matalýza 1 [[skripta](/assets/priprava-na-statnice-mff-uk/ma1.pdf), [derivace](/assets/priprava-na-statnice-mff-uk/ma-derivate.pdf), [integrály](/assets/priprava-na-statnice-mff-uk/ma-integrate.pdf), [limity](/assets/priprava-na-statnice-mff-uk/ma-limits.pdf)] 🃏 %}
		{% stlink Reálná čísla | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.1 %}
		<ul>
			<li> odmocnina ze dvou je iracionální
			<li> \(\mathbb{R}\) je nespočetná množina
		</ul>
		{% stlink Posloupnosti reálných čísel a jejich limity | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.2 | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.3 %}
		<ul>
			<li> definice, aritmetika limit
			<li> věta o dvou policajtech, limity a uspořádání
		</ul>
		{% stlink Řady | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.2 | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.3 %}
		<ul>
			<li> definice částečného součtu a součtu
			<li> geometrická řada, harmonická řada
		</ul>
		{% stlink Reálné funkce jedné reálné proměnné. | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.4 %}
		<ul>
			{% stlink limita funkce v bodě | /assets/priprava-na-statnice-mff-uk/ma1.pdf#page=16 | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.6 %}
			<ul>
				<li> definice, aritmetika limit
				<li> vztah s uspořádáním
				<li> limita složené funkce
			</ul>
			{% stlink funkce spojité na intervalu | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.6 %}
			<ul>
				<li> nabývání mezihodnot
				<li> nabývání maxima
			</ul>
		</ul>
		{% stlink Derivace a její aplikace  | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.7 | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.8 | https://en.wikipedia.org/wiki/Weierstrass_function %}
		<ul>
			<li> definice a základní pravidla pro výpočet
			<li> l’Hospitalovo pravidlo
			<li> vyšetření průběhu funkcí: extrémy, monotonie a konvexita/konkavita
			{% stlink Taylorův polynom se zbytkem | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.9 | https://brilliant.org/wiki/taylor-series-error-bounds/ %}
		</ul>
		{% stlink Integrály a jejich aplikace | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.10 %}
		<ul>
			<li> primitivní funkce: definice a metody výpočtu (substituce, per-partes)
			<li> Riemannův integrál: definice, souvislost s primitivní funkcí (Newtonovým integrálem)
			<li> aplikace
			<ul>
				<li> odhady součtu řad (konečných i nekonečných)
				<li> obsahy rovinných útvarů
				<li> objemy a povrchy rotačních útvarů v prostoru
				<li> délka křivky
			</ul>
		</ul>
	{% endsttopic %}
	{% sttopic Algebra a lineární algebra | Lingebra 1 a 2 [[skripta](/assets/priprava-na-statnice-mff-uk/la.pdf)] 🃏 %}
		{% stlink Grupy a podgrupy (definice, příklady, komutativita) | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.4 %}
		{% stlink Tělesa (definice, charakteristika tělesa, konečná tělesa) | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.4 %}
		{% stlink Vektorové prostory a podprostory. | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.5 %}
		<ul>
			<li> vlastnosti a základní pojmy (lineární kombinace, lineární obal, generátory, lineární závislost a nezávislost, báze, dimenze, souřadnice) a jejich použití
			<li> praktická dovednost testování lineární závislosti a nezávislosti, nalezení báze, určení dimenze atp.
			<li> skalární součin a jeho vlastnosti
			<li> norma a vztah se skalárním součinem, příklady
			<li> kolmost, ortonormální báze, její vlastnosti a použití (nalezení souřadnic a projekce)
		</ul>
		{% stlink Skalární součin, norma. | /assets/priprava-na-statnice-mff-uk/la.pdf#section.8.1 %}
		{% stlink Kolmost, ortonormální báze. | /assets/priprava-na-statnice-mff-uk/la.pdf#section.8.2 | /assets/priprava-na-statnice-mff-uk/la.pdf#section.8.3 | /assets/priprava-na-statnice-mff-uk/la.pdf#section.8.4 %}
		{% stlink Soustavy lineárních rovnic a množina řešení. | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.2 %}
		<ul>
			<li> metody řešení, Gaussova a Gaussova-Jordanova eliminace, odstupňovaný tvar matice a jeho jednoznačnost (bez důkazu)
		</ul>
		{% stlink Matice a operace s maticemi (součet, součin, transpozice) | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.3 | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.9 | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.11 %}
		<ul>
			<li> interpretace součinu matic pomocí skládání lineárních zobrazení
			<li> hodnost matice a její transpozice
			{% stlink vlastní čísla a vlastní vektory matice a jejich geometrický význam a vlastnosti, vícenásobná vlastní čísla, spektrální poloměr | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.10 %}
			{% stlink charakteristický polynom, vztah vlastních čísel s kořeny polynomů | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.12 %}
		</ul>
	{% endsttopic %}
	{% sttopic Diskrétní matematika | Diskrétka [[poznámky](/poznamky-z-prednasky/diskretni-matematika/)] 🃏, Kombagra 1 [[poznámky](/poznamky-z-prednasky/kombinatorika-a-grafy-i/)] 🃏 %}
		{% stlink Relace. | /poznamky-z-prednasky/diskretni-matematika/#relace %}
		<ul>
			<li> vlastnosti binárních relací (reflexivita, symetrie, antisymetrie, tranzitivita)
		</ul>
		{% stlink Ekvivalence a rozkladové třídy. | /poznamky-z-prednasky/diskretni-matematika/#ekvivalence %}
		{% stlink Částečná uspořádání. | /poznamky-z-prednasky/diskretni-matematika/#uspořádání %}
		<ul>
			<li> základní pojmy
			{% stlink výška a šířka částečně uspořádané množiny, věta o dlouhém a širokém | /poznamky-z-prednasky/diskretni-matematika/#dlouh%C3%BD-a-%C5%A1irok%C3%BD %}
		</ul>
		{% stlink Funkce. | /poznamky-z-prednasky/diskretni-matematika/#funkce %}
		<ul>
			<li> typy funkcí (prostá, na, bijekce)
			<li> počty různých typů funkcí mezi dvěma konečnými množinami
		</ul>
		{% stlink Permutace a jejich základní vlastnosti (počet a pevný bod). | /poznamky-z-prednasky/diskretni-matematika/#segway-do-kombinatorického-počítání %}
		{% stlink Kombinační čísla a vztahy mezi nimi, binomická věta a její aplikace. | /poznamky-z-prednasky/diskretni-matematika/#kombinatorika %}
		{% stlink Princip inkluze a exkluze. | /poznamky-z-prednasky/diskretni-matematika/#princip-inkluzeexkluze %}
		<ul>
			<li> obecná formulace (a důkaz)
			<li> použití (problém šatnářky, Eulerova funkce pro počet dělitelů, počet surjekcí)
		</ul>
		{% stlink Hallova věta o systému různých reprezentantů, vztah k párování v bipartitním grafu. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#aplikace-tok%C5%AF-v-s%C3%ADt%C3%ADch %}
		<ul>
			<li> princip důkazu a algoritmické aspekty (polynomiální algoritmus pro nalezení SRR)
		</ul>
	{% endsttopic %}
	{% sttopic Teorie grafů | Diskrétka [[poznámky](/poznamky-z-prednasky/diskretni-matematika/)] 🃏, Kombagra 1 [[poznámky](/poznamky-z-prednasky/kombinatorika-a-grafy-i/)] 🃏 %}
		{% stlink Základní pojmy, základní příklady grafů. | /poznamky-z-prednasky/diskretni-matematika/#grafy %}
		{% stlink Souvislost grafů, komponenty souvislosti, vzdálenost v grafu. | /poznamky-z-prednasky/diskretni-matematika/#rozšiřování-grafů %}
		{% stlink Stromy. | /poznamky-z-prednasky/diskretni-matematika/#stromy %}
		<ul>
			<li> definice a základní vlastnosti (existence listů, počet hran stromu)
			<li> ekvivalentní charakteristiky stromů
		</ul>
		{% stlink Rovinné grafy. | /poznamky-z-prednasky/diskretni-matematika/#rovinné-nakreslení-grafu %}
		<ul>
			<li> definice a základní pojmy (rovinný graf a rovinné nakreslení grafu, stěny)
			<li> Eulerova formule a maximální počet hran rovinného grafu (důkaz a použití)
		</ul>
		{% stlink Barevnost grafů, klikovost grafů. | /poznamky-z-prednasky/diskretni-matematika/#barvení | /poznamky-z-prednasky/diskretni-matematika/#degenerovanost-klikovost-dualita %}
		<ul>
			<li> definice dobrého obarvení
			<li> vztah barevnosti a klikovosti grafu
		</ul>
		{% stlink Hranová a vrcholová souvislost grafů, Mengerovy věty. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#míra-souvislosti-neorientovaných-grafu  %}
		{% stlink Orientované grafy, silná a slabá souvislost. | /poznamky-z-prednasky/diskretni-matematika/#rozšiřování-grafů  %}
		{% stlink Toky v sítích. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#7-přednáška | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s14  %}
		<ul>
			<li> definice sítě a toku v ní
			<li> existence maximálního toku (bez důkazu)
			<li> princip hledání maximálního toku v síti s celočíselnými kapacitami (například pomocí Ford-Fulkersonova algoritmu)
		</ul>
	{% endsttopic %}
	{% sttopic Past | Diskrétka [[poznámky](/poznamky-z-prednasky/diskretni-matematika/)] 🃏, Past [[slidy](/assets/priprava-na-statnice-mff-uk/past/slides.pdf), [cheatsheet](/assets/priprava-na-statnice-mff-uk/past/cheatsheet.pdf), [příklady](/assets/priprava-na-statnice-mff-uk/past/examples.pdf)] 🃏 %}
		<li> Pravděpodobnostní prostor, náhodné jevy, pravděpodobnost
			<ul>
			<li> definice těchto pojmů, příklady
			<li> základní pravidla pro počítání s pravděpodobností
			<li> nezávislost náhodných jevů, podmíněná pravděpodobnost
			<li> Bayesův vzorec
			</ul>
		<li> Náhodné veličiny a jejich rozdělení
			<ul>
			<li> diskrétní i spojitý případ
			<li> popis pomocí distribuční funkce a pomocí pravděpodobnostní funkce/hustoty
			<li> střední hodnota
				<ul>
				<li> linearita střední hodnoty
				<li> střední hodnota součinu nezávislých veličin
				<li> Markovova nerovnost
				</ul>
			<li> rozptyl
				<ul>
				<li> definice
				<li> vzorec pro rozptyl součtu (závislých či nezávislých veličin)
				</ul>
			<li> práce s konkrétními rozděleními: geometrické, binomické, Poissonovo, normální, exponenciální
			</ul>
		<li> Limitní věty
			<ul>
			<li> zákon velkých čísel
			<li> centrální limitní věta
			</ul>
		<li> Bodové odhady
			<ul>
			<li> alespoň jedna metoda pro jejich tvorbu
			<li> vlastnosti
			</ul>
		<li> Intervalové odhady: metoda založená na aproximaci normálním rozdělením
		<li> Testování hypotéz
			<ul>
			<li> základní přístup
			<li> chyby 1. a 2. druhu
			<li> hladina významnosti
			</ul>
	{% endsttopic %}
	{% sttopic Logika | Výpal [[slidy](/assets/priprava-na-statnice-mff-uk/vypal.pdf)] 🃏 %}
		<li> Syntaxe
		<ul>
			<li> znalost a práce se základními pojmy syntaxe výrokové a predikátové logiky (jazyk, otevřená a uzavřená formule, instance formule, apod.)
			<li> normální tvary výrokových formulí
			<ul>
				<li> prenexní tvary formulí predikátové logiky
				<li> znalost základních normálních tvarů (CNF, DNF, PNF)
				<li> převody na normální tvary
				<li> použití pro algoritmy (SAT, rezoluce)
			</ul>
		</ul>
		<li> Sémantika
		<ul>
			<li> pojem modelu teorie
			<li> pravdivost, lživost, nezávislost formule vzhledem k teorii
			<li> splnitelnost, tautologie, důsledek
			<li> analýza výrokových teorií nad konečně mnoha prvovýroky
		</ul>
		<li> Extenze teorií
		<ul>
			<li> schopnost porovnat sílu teorií
			<li> konzervativnost, skolemizace
		</ul>
		<li> Dokazatelnost:
		<ul>
			<li> pojem formálního důkazu, zamítnutí
			<li> schopnost práce v některém z formálních dokazovacích systémů (např. tablo metoda, rezoluce, Hilbertovský kalkul)
		</ul>
		{% stlink Věty o kompaktnosti a úplnosti výrokové a predikátové logiky | /assets/priprava-na-statnice-mff-uk/autogramy/vypal.pdf#page=85 | /assets/priprava-na-statnice-mff-uk/autogramy/vypal.pdf#page=81 | /assets/priprava-na-statnice-mff-uk/autogramy/vypal.pdf#page=79 %}
		<ul>
			<li> znění a porozumění významu
			<li> použití na příkladech, důsledky
		</ul>
		{% stlink Rozhodnutelnost | /assets/priprava-na-statnice-mff-uk/autogramy/vypal.pdf#page=273 %}
		<ul>
			<li> pojem kompletnosti a její kritéria, význam pro rozhodnutelnost
			<li> příklady rozhodnutelných a nerozhodnutelných teorií
		</ul>
	{% endsttopic %}
{% endsttopics %}

#### Informatika

{% sttopics %}
	{% sttopic Automaty a jazyky | Autogramy [[skripta](/assets/priprava-na-statnice-mff-uk/autogramy/skripta.pdf), [slidy](/assets/priprava-na-statnice-mff-uk/autogramy/slidy.pdf)] 🃏 %}
		<li> Regulární jazyky.
		<ul>
			<li> regulární gramatiky
			<li> konečný automat, jazyk přijímaný konečným automatem
			<li> deterministický a nedeterministický automat, lambda přechody
			<li> regulární výrazy
			<li> Kleeneho věta
			<li> iterační (pumping) lemma pro konečné automaty
		</ul>
		<li> Uzávěrové vlastnosti
		<li> Bezkontextové jazyky.
		<ul>
			<li> bezkontextové gramatiky, jazyk generovaný gramatikou
			<li> zásobníkový automat, třída jazyků přijímaných zásobníkovými automaty
		</ul>
		<li> Turingův stroj.
		<ul>
			<li> gramatika typu 0
			<li> diagonální jazyk
			<li> univerzální jazyk
		</ul>
		<li> Chomského hierarchie.
		<ul>
			<li> určení ekvivalence či inkluze tříd jazyků generovaných výše uvedenými automaty a gramatikami
			<li> schopnost zařazení konkrétního jazyka do Chomského hierarchie (zpravidla sestrojení odpovídajícího automatu či gramatiky a důkaz iteračním lemmatem, že jazyk není v nižší třídě)
		</ul>
	{% endsttopic %}
	{% sttopic Algoritmy a datové stuktury | ADS 1 a 2 [[Průvodce](/assets/priprava-na-statnice-mff-uk/pruvodce.pdf), [GA](/assets/priprava-na-statnice-mff-uk/ga.pdf)] 🃏 %}
		{% stlink Časová a prostorová složitost algoritmů. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s2  %}
		<ul>
			<li> čas a prostor výpočtu pro konkrétní vstup
			<li> časová a prostorová složitost algoritmu
			<li> měření velikosti dat
			<li> složitost v nejlepším, nejhorším a průměrném případě
			<li> asymptotická notace
		</ul>
		{% stlink Třídy složitosti. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s19.3 | /assets/priprava-na-statnice-mff-uk/pvnp.png %}
		<ul>
			<li> třídy P a NP
			<li> převoditelnost problémů, NP-těžkost a NP-úplnost
			<li> příklady NP-úplných problémů a převodů mezi nimi
		</ul>
		{% stlink Metoda "rozděl a panuj". |  /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s10 %}
		<ul>
			<li> princip rekurzivního dělení problému na podproblémy
			<li> výpočet složitosti pomocí rekurentních rovnic
			<li> Master theorem (kuchařková věta)
			<li> aplikace
			<ul>
				<li> Mergesort
				<li> násobení dlouhých čísel
				<li> Strassenův algoritmus
			</ul>
		</ul>
		{% stlink Binarní vyhledávací stromy. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s8 %}
		<ul>
			<li> definice vyhledávacího stromu
			<li> operace s nevyvažovanými stromy
			<li> AVL stromy (definice)
		</ul>
		{% stlink Binární haldy. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s4.2 %}
		{% stlink Hešování s přihrádkami a s otevřenou adresací. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s11.3 %}
		{% stlink Třídící algoritmy. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s3  %}
		<ul>
			<li> primitivní třídicí algoritmy (Bubblesort, Insertsort)
			<li> třídění haldou (Heapsort)
			<li> Quicksort
			<li> dolní odhad složitosti porovnávacích třídicích algoritmů
			<li> přihrádkové třídění čísel a řetězců
		</ul>
		{% stlink Grafové algoritmy. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s5 | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s6| /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s7 %}
		<ul>
			{% stlink DFS, BFS a jejich aplikace. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s5 | https://stackoverflow.com/questions/20429310/why-is-depth-first-search-claimed-to-be-space-efficient %}
			{% stlink Nejkratší cesty (Dijkstra, BF). | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s6 %}
			{% stlink Minimální kostry (Jarník, Borůvka). | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s7 %}
			{% stlink Toky v sítích (FF). | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s14 | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#7-přednáška  %}
		</ul>
		{% stlink Euklidův algoritmus. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s1.3  %}
	{% endsttopic %}
	{% sttopic Programovací jazyky | Programko [[poznámky](/assets/priprava-na-statnice-mff-uk/prog2.pdf)], Java/C#/C++ [[C# poznámky](/lecture-notes/the-cs-programming-language/)] %}
	<li> Koncepty pro abstrakci, zapouzdření a polymorfismus.
		<ul>
		<li> související konstrukty programovacích jazyků
			<ul>
			<li> třídy, rozhraní, metody, datové položky, dědičnost, viditelnost
			</ul>
		<li> (dynamický) polymorfismus, statické a dynamické typování
		<li> jednoduchá dědičnost
			<ul>
			<li> virtuální a nevirtuální metody v C++ ~~a C#~~
			<li> ~~defaultní metody v Javě~~
			</ul>
		<li> ~~vícenásobná dědičnost a její problémy~~
			<ul>
			<li> ~~vícenásobná a virtuální dědičnost v C++~~
			<li> ~~interfaces v Javě a C++~~
			</ul>
		<li> implementace rozhraní (interface)
		</ul>
	<li> Primitivní a objektové typy a jejich reprezentace.
		<ul>
		<li> číselné a výčtové typy
		<li> ~~ukazatele a reference v C++~~
		<li> hodnotové a referenční typy v C#
		<li> imutabilní typy a boxing/unboxing v C# ~~a Javě~~
		</ul>
	<li> Generické typy a funkcionální prvky (procedurálních programovacích jazyků).
		<ul>
		<li> ~~šablony (templates) a statický polymorfismus v C++~~
		<li> generické typy v Javě a C# (bez omezení typových parametrů)
		<li> typy reprezentující funkce v ~~C++~~, C#, ~~nebo Javě~~
		<li> lambda funkce a funkcionální rozhraní
		</ul>
	<li> Manipulace se zdroji a mechanizmy pro ošetření chyb.
		<ul>
		<li> správa životního cyklu zdrojů v případě výskytu chyb
			<ul>
			<li> ~~RAII v C++~~, using v C#, ~~try-with-resources v Javě~~
			</ul>
		<li> konstrukce pro obsluhu a propagaci výjimek
		</ul>
	<li> Životní cyklus objektů a správa paměti.
		<ul>
		<li> alokace (alokace statická, na zásobníku, na haldě)
		<li> inicializace (konstruktory, volání zděděných konstruktorů)
		<li> destrukce (destruktory, finalizátory)
		<li> explicitní uvolňování objektů, reference counting, garbage collector
		</ul>
	<li> Vlákna a podpora synchronizace.
		<ul>
		<li> reprezentace vláken v programovacích jazycích
		<li> specifikace funkce vykonávané vláknem a základní operace na vlákny
		<li> časově závislé chyby a mechanizmy pro synchronizaci vláken
		</ul>
	<li> Implementace základních prvků objektových jazyků.
		<ul>
		<li> základní objektové koncepty v konkrétním jazyce (~~Java~~, ~~C++~~, C#)
		<li> implementace a interní reprezentace primitivních typů
		<li> implementace a interní reprezentace složených typů a objektů
		<li> implementace dynamického polymorfismu (tabulka virtuálních metod)
		</ul>
	<li> Nativní a interpretovaný běh, řízení překladu a sestavení programu.
		<ul>
		<li> reprezentace programu, bytecode, interpret jazyka
		<li> just-in-time (JIT) a ahead-of-time (AOT) překlad
		<li> proces sestavení programu, oddělený překlad, linkování
		<li> staticky a dynamicky linkované knihovny
		<li> běhové prostředí procesu a vazba na operační systém
		</ul>
	{% endsttopic %}
	{% sttopic Architektura počítačů a OS | Principy poč. [[poznámky](/poznamky-z-prednasky/principy-pocitacu/)] 🃏, Poč. systémy [[slidy](/assets/priprava-na-statnice-mff-uk/ps.pdf)] %}
		{% stlink Základní architektura počítače. | /poznamky-z-prednasky/principy-pocitacu/#zjednodu%C5%A1en%C3%A9-sch%C3%A9ma-po%C4%8D%C3%ADta%C4%8De | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=24 %}
		<ul>
			<li> reprezentace a přístup k datům v paměti, adresa, adresový prostor
			<li> ukládání jednoduchých a složených datových typů
			<li> základní aritmetické a logické operace
		</ul>
		{% stlink Reprezentace dat a programů. | /poznamky-z-prednasky/principy-pocitacu/#k%C3%B3dov%C3%A1n%C3%AD-informace-v-po%C4%8D%C3%ADta%C4%8Di | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=60 %}
		{% stlink Instrukční sada, vazba na vyšší programovací jazyky. | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=29 %}
		<ul>
			<li> Implementovat běžné programové konstrukce vyšších jazyků (přiřazení, podmínka, cyklus, volání funkce) pomocí instrukcí procesoru
			<li> Zapsat běžnou konstrukci vyššího jazyka (přiřazení, podmínka, cyklus, volání funkce), která odpovídá zadané sekvenci (vysvětlených) instrukcí procesoru
		</ul>
		{% stlink Podpora pro běh operačního systému. | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=97  %}
		<ul>
			<li> privilegovaný a neprivilegovaný režim procesoru
			<li> jádro operačního systému
		</ul>
		{% stlink Rozhraní periferních zařízení a jejich obsluha. | /poznamky-z-prednasky/principy-pocitacu/#otro%C4%8Dina | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=105  %}
		<ul>
			<li> Popsat roli řadiče zařízení při programem řízené obsluze zařízení (PIO), pro zadané adresy a funkce vstupních a výstupních portů implementovat programem řízenou obsluhu zadaného zařízení (myš, disk)
			<li> Popsat roli přerušení při programem řízené obsluze zařízení (PIO), na úrovni vykonávání instrukcí popsat reakci procesoru (hardware) a operačního systému (software) na žádost o přerušení
		</ul>
		{% stlink Základní abstrakce, rozhraní a mechanizmy OS pro běh programů, sdílení prostředků a vstup/výstup. | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=97  %}
		<ul>
			<li> neprivilegované (uživatelské) procesy
			<li> sdílení procesoru
			<ul>
				<li> procesy, vlákna, kontext procesu a vlákna
				<li> přepínání kontextu, kooperativní a preemptivní multitasking
				<li> plánování běhu procesů a vláken, stavy vlákna
			</ul>
			<li> sdílení paměti
			<ul>
				<li> Vysvětlit rozdíl mezi virtuální a fyzickou adresou a identifikovat, zda se v zadaném kontextu či fragmentu kódu používá virtuální nebo fyzická adresa
				<li> Na zadaném příkladu identifikovat a vysvětlit význam komponent virtuální a fyzické adresy (číslo stránky, číslo rámce, offset)
				<li> Pro konkrétní adresy a obsah jednoúrovňové stránkovací tabulky řešit úlohy překladu adres
				<li> Vysvětlit roli virtuálních adresových prostorů v ochraně paměti procesů a vláken
			</ul>
			<li> sdílení úložného prostoru
			<ul>
				<li> soubory, analogie s adresovým prostorem
				<li> abstrakce a rozhraní pro práci se soubory
			</ul>
		</ul>
		{% stlink Paralelismus, vlákna a rozhraní pro jejich správu, synchronizace vláken. | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=112 %}
		<ul>
			<li> časově závislé chyby (race conditions)
			<li> kritická sekce, vzájemné vyloučení
			<li> základní sychronizační primitiva, jejich rozhraní a použití
			<ul>
				<li> zámky
				<li> aktivní a pasivní čekání
			</ul>
		</ul>
	{% endsttopic %}
{% endsttopics %}

### Specifická
Z následujících témat je třeba umět **všechna** z 1-3 a **dvě** z 4-7 (vybírá se v SISu).

{% sttopics %}
	{% sttopic Kombinatorika | Kombagra 1 [[poznámky](/poznamky-z-prednasky/kombinatorika-a-grafy-i/)] 🃏 a 2 [[poznámky](/poznamky-z-prednasky/kombinatorika-a-grafy-ii/)] 🃏 %}
		{% stlink Vytvořující funkce. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#generuj%C3%ADc%C3%AD-funkce %}
		<ul>
			<li> použití vytvořujících funkcí k řešení lineárních rekurencí
			<li> zobecněná binomická věta (formulace)
			<li> Catalanova čísla (příklad kombinatorické interpretace, odvození vzorce)
		</ul>
		{% stlink Odhady faktoriálů a kombinačních čísel. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#odhady-faktori%C3%A1lu | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#odhady-binomických-koeficientů %}
		<ul>
			<li> \((n/e)^n \le n! \le n(n/e)^n\)
			<li> \((n/k)^k \le \binom{n}{k} \le (en/k)^k\)
			<li> \(2^{2m}/(2  \sqrt{m}) \le \binom{2m}{m} \le 2^{2m} / \sqrt{2m}\)
		</ul>
		{% stlink Ramseyova teorie. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#ramseyovy-barevn%C3%A9nekone%C4%8Dn%C3%A9-v%C4%9Bty %}
		<ul>
			<li> Ramseyova věta (formulace konečné a nekonečné verze pro p-tice, důkaz verze \(p=2\) pro 2 barvy)
			<li> Ramseyova čísla (definice, pro 2 barvy horní odhad z důkazu Ramseyovy věty a dolní odhad pravděpodobnostní konstrukcí)
		</ul>
		{% stlink Extremální kombinatorika | /poznamky-z-prednasky/kombinatorika-a-grafy-ii/#extrem%C3%A1ln%C3%AD-teorie-graf%C5%AF-a-hypergraf%C5%AF %}
		<ul>
			<li> obecné povědomí co extremální kombinatorika studuje
			<li> Turánova věta (formulace, Turánovy grafy)
			<li> Erdös-Ko-Radoova věta (formulace)
		</ul>
		{% stlink Samoopravné kódy. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#samoopravn%C3%A9-k%C3%B3dy %}
		<ul>
			<li> přehled o používané terminologii
			<li> vzdálenost kódu a její vztah k počtu opravitelných a detekovatelných chyb
			<li> Hammingův odhad (formulace a důkaz)
			<li> perfektní kódy (definice a příklady, Hammingův kód bez přesné konstrukce)
		</ul>{% endsttopic %}
	{% sttopic Základy sítí | Sítě [[slidy](/assets/priprava-na-statnice-mff-uk/site.pdf)] 🃏 %}
		<li> Taxonomie počítačových sítí.
		<li> Architektura ISO/OSI.
		<li> Přehled síťového modelu TCP/IP.
		<li> Směrování.
		<li> Koncept adresy, portu, socketu.
		<li> Architektura klient/server.
		<li> Základy fungování protokolů HTTP, FTP a SMTP.
	{% endsttopic %}
	{% sttopic Matalýza 2  | Matalýza 2 [[poznámky Pultr](/assets/priprava-na-statnice-mff-uk/ma2.pdf), [poznámky Klazar]([poznámky Pultr](/assets/priprava-na-statnice-mff-uk/ma2.pdf))] 🃏 %}
		<li> Riemannův integrál jedno- i vícerozměrný
		<li> Funkce více proměnných
			<ul>
			<li> parciální derivace: definice a výpočet
			<li> výpočet extrémů pomocí paricálních derivací
			<li> existence extrémů pro funkce několika reálných proměnných
			<li> vázané extrémy: výpočet pomocí Lagrangeových multiplikátorů
			</ul>
		<li> Metrický prostor
			<ul>
			<li> definice a základní příklady
			<li> otevřené a uzavřené množiny: definice, příklady
			<li> spojitost funkce na metrickém prostoru
			<li> kompaktnost: definice a důsledky pro extrémy funkcí více proměnných
			<li> stejnoměrná spojitost
			</ul>
	{% endsttopic %}
	{% sttopic Optimalizace | LP [[skripta](/assets/priprava-na-statnice-mff-uk/linprog.pdf)] 🃏, APX [[pozn.](/poznamky-z-prednasky/aproximacni-algoritmy/)] 🃏, Kombagra 2 [[pozn.](/poznamky-z-prednasky/kombinatorika-a-grafy-ii/)] 🃏, DSPO [[pozn.](/poznamky-z-prednasky/diskretni-a-spojita-optimalizace/)] %}
		<li> Základy lineárního a celočíselného programování.
		<ul>
			<li> dualita lineárního programování, Farkasovo lemma
			<li> simplexová metoda, pivotovací pravidla
		</ul>
		<li> Kombinatorická geometrie
		<ul>
			<li> konvexní obal objektů
			<li> mnohostěny
			<li> Minkowski-Weylova věta
		</ul>
		{% stlink Edmondsův algoritmus. | /poznamky-z-prednasky/kombinatorika-a-grafy-ii/#nejv%C4%9Bt%C5%A1%C3%AD-p%C3%A1rov%C3%A1n%C3%AD | https://www.youtube.com/watch?v=3roPs1Bvg1Q %}
		<li> Základy matematického programování
			<ul>
			<li>unimodularita, Königovo lemma, toky v sítích, souvislost s dualitou LP
			<li>vážené maximální párování v bipartitních grafech a jeho primárně-duální algoritmus
			</ul>
		<li> Celočíselné programování.
		<ul>
			{% stlink metoda řezů | https://en.wikipedia.org/wiki/Cutting-plane_method %}
		</ul>
		{% stlink Matroidy. | /poznamky-z-prednasky/diskretni-a-spojita-optimalizace/ %}
		<ul>
			<li> řádová funkce, existence a submodularita
			<li> hladový algoritmus
		</ul>
		{% stlink Aproximační algoritmy pro kombinatorické problémy: | /poznamky-z-prednasky/aproximacni-algoritmy/ %}
		<ul>
			<li> definice: aproximační poměr, aproximační schéma
			{% stlink splnitelnost | /lecture-notes/best-sat/ %}
			{% stlink nezávislé množiny | /poznamky-z-prednasky/aproximacni-algoritmy/#maximální-nezávislá-množina %}
			{% stlink množinové pokrytí | /poznamky-z-prednasky/aproximacni-algoritmy/#pokrývací-problémy %}
			{% stlink rozvrhování | /poznamky-z-prednasky/aproximacni-algoritmy/#rozvrhov%C3%A1n%C3%AD %}
		</ul>
		<li> Použití lineárního programování pro aproximační algoritmy.
		<ul>
			{% stlink algoritmy pro splnitelnost (MAXSAT, pravděpodobnostní zaokrouhlování) | /poznamky-z-prednasky/aproximacni-algoritmy/#lp-sat %}
			{% stlink vrcholové a množinové pokrytí (deterministické zaokrouhlování, primárně-duální algoritmus) | /poznamky-z-prednasky/aproximacni-algoritmy/#pokrývací-problémy %}
		</ul>
		<li> Využití pravděpodobnosti při návrhu algoritmů.
		<ul>
			{% stlink minimální globální řez v grafu | /poznamky-z-prednasky/aproximacni-algoritmy/#glob%C3%A1ln%C3%AD-minim%C3%A1ln%C3%AD-%C5%99ez %}
			{% stlink hashování a jeho využítí pro slovník s konstantním časem vyhledávání | /poznamky-z-prednasky/aproximacni-algoritmy/#hashovac%C3%AD-funkce %}
			{% stlink pravděpodobnostní testování maticových a polynomiálních identit | /poznamky-z-prednasky/aproximacni-algoritmy/#nulovost-polynom%C5%AF-polynomial-identity-testing %}
			{% stlink paralelní algoritmus pro hledání maximální nezávislé množiny | /poznamky-z-prednasky/aproximacni-algoritmy/#maxim%C3%A1ln%C3%AD-nez%C3%A1visl%C3%A1-mno%C5%BEina %}
			{% stlink paralelní algoritmy pro hledání párování (bipartitní grafy) | /poznamky-z-prednasky/aproximacni-algoritmy/#perfektn%C3%AD-p%C3%A1rov%C3%A1n%C3%AD %}
		</ul>
	{% endsttopic %}
	{% sttopic Pokročilé ADS | ADS 1 a 2 [[Průvodce](/assets/priprava-na-statnice-mff-uk/pruvodce.pdf), [GA](/assets/priprava-na-statnice-mff-uk/ga.pdf)] 🃏, APX [[poznámky](/poznamky-z-prednasky/aproximacni-algoritmy/)] 🃏, Algebra 1 [[skripta](/assets/priprava-na-statnice-mff-uk/algebra.pdf)] %}
		{% stlink Dynamické programování. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s12 %}
		<ul>
			<li> princip dynamického programování (řešení podproblémů od nejmenších k největším)
			{% stlink aplikace: nejdelší rostoucí podposloupnost, editační vzdálenost | /assets/priprava-na-statnice-mff-uk/lis.py | /assets/priprava-na-statnice-mff-uk/edit.py %}
		</ul>
		{% stlink Výpočetní model RAM. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s2.5 %}
		{% stlink Komponenty silné souvislosti orientovaných grafů. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s5.9 %}
		<ul>
			<li> tranzitivní uzávěr (Floyd-Warshal)
			<li> komponenty silné souvislosti orientovaných grafů
			<li> toky v sítích (Dinicův a Goldbergův algoritmus)
		</ul>
		{% stlink Toky v sítích (FF, Diniz, Goldberg). | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s14 | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#7-přednáška %}
		{% stlink Vyhledávání v textu (KMP, AC). | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s13 | /assets/priprava-na-statnice-mff-uk/kmp.py  %}
		<ul>
			<li> algoritmy Knuth-Morris-Pratt a Aho-Corasicková
		</ul>
		{% stlink Diskrétní Fourierova transformace, aplikace. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s17 | /assets/priprava-na-statnice-mff-uk/fft.py %}
		<ul>
			<li> diskrétní Fourierova transformace a její aplikace
			<li> výpočet Fourierovy transformace algoritmem FFT
		</ul>
		{% stlink RSA (šifrování, dešifrování a generování klíčů) | /assets/priprava-na-statnice-mff-uk/algebra.pdf#subsection.2.2 %}
		{% stlink Aproximační algoritmy a schémata (cestující, batoh). | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s19.6 | /poznamky-z-prednasky/aproximacni-algoritmy/#metrický-tsp %}
		<ul>
			<li> poměrová a relativní chyba
			<li> aproximační schémata
			<li> příklady: obchodní cestující, batoh
		</ul>
		{% stlink Paralelní třidění pomocí komparátorových sítí. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s15 %}
		<li> Červeno-černé stromy a jejich vyvažování
	{% endsttopic %}{% endsttopics %} <hr><div class="stignored"> {% sttopics 6 %}
	{% sttopic ❌ Geometrie ❌ | Základy KVG %}
		<li> Základní věty o konvexních množinách (Hellyho, Radonova, o oddělování).
		<li> Minkowského věta o mřížkách.
		<li> Konvexní mnohostěny (zákadní vlastnosti, V-mnohostěny, H-mnohostěny, kombinatorická složitost).
		<li> Geometrická dualita.
		<li> Voroného diagramy, arrangementy (komplexy) nadrovin, incidence bodů a přímek, základní algoritmy výpočetní geometrie (konstrukce arrangementu přímek v rovině, konstrukce konvexního obalu v rovině).
	{% endsttopic %}
	{% sttopic ❌ Pokročilá diskrétní matematika ❌ | Kombagra 2, Teorie množin %}
		<li> Barvení grafů (Brooksova a Vizingova věta).
		<li> Tutteova věta.
		<li> Extremální kombinatorika (Turánova věta, Erdös-Ko-Radoova věta).
		<li> Kreslení grafů na plochách.
		<li> Množiny a zobrazení.
		<li> Subvalence a ekvivalence množin.
		<li> Dobré uspořádání.
		<li> Axiom výběru (Zermelova věta, Zornovo lemma).
	{% endsttopic %}
{% endsttopics %}
</div>

### Poděkování
- **shrekofspeed** (Discord) za upozornění na [požadavky](https://www.mff.cuni.cz/cs/studenti/bakalarske-studium/statni-zaverecne-zkousky/bakalarske-statni-zkousky-studijniho-programu-informatika/detailni-pozadavky.pdf) a na Medvědovo [Grafové Algoritmy](/assets/priprava-na-statnice-mff-uk/ga.pdf)
