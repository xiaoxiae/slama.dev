---
language: cz
title: Příprava na státnice (MFF UK)
css: statnice
---

- .
{:toc}

Tento článek obsahuje mou přípravu na státní zkoušky z **Obecné informatiky** pro akademický rok **2021/2022** (tj. nová akreditace).

U každé časti tématu je jeden a více odkazů (🔗) na zdroje, ze kterých se téma učím.
U předmětů jsou vždy odkazy na zdroje (ať už poznámky, slidy či skripta).
Pokud je u předmětu symbol kartičky (🃏), tak je zahrnut v [tomto Anki balíčku](https://github.com/xiaoxiae/AnkiMFF), ze kterého může být dobré si předmět zopakovat.

Symbol políčka 🟩/🟧 ignorujte -- jedná se o mé značení znalosti procházených témat.

### Obecná

#### Matematika

{% sttopics %}
	{% sttopic Základy diferenciálního a integrálního počtu | Matalýza 1 [[skripta](/assets/priprava-na-statnice-mff-uk/ma1.pdf)] 🃏 %}
		{% stlink Posloupnosti reálných čísel a jejich vlastnosti. | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.2 | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.3 %}
		{% stlink Reálné funkce jedné reálné proměnné. | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.4 %}
		{% stlink Spojitost, limita funkce v bodě. | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.5 | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.6 %}
		{% stlink Derivace: definice a základní pravidla, průběhy, Taylorův polynom se zbytkem.  | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.7 | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.8 %}
		{% stlink Primitivní funkce: definice, jednoznačnost, existence, metody výpočtu. | /assets/priprava-na-statnice-mff-uk/ma1.pdf#chapter.9 %}
	{% endsttopic %}
	{% sttopic Algebra a lineární algebra | Lingebra 1 a 2 [[skripta](/assets/priprava-na-statnice-mff-uk/la.pdf)] 🃏 %}
		{% stlink Grupy a podgrupy, tělesa. | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.4 %}
		{% stlink Vektorové prostory a podprostory. | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.5 %}
		{% stlink Skalární součin, norma. | /assets/priprava-na-statnice-mff-uk/la.pdf#section.8.1 %}
		{% stlink Kolmost, ortonormální báze. | /assets/priprava-na-statnice-mff-uk/la.pdf#section.8.2 | /assets/priprava-na-statnice-mff-uk/la.pdf#section.8.3 | /assets/priprava-na-statnice-mff-uk/la.pdf#section.8.4 %}
		{% stlink Soustavy lineárních rovnic, Gaussova a Gaussova-Jordanova eliminace. | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.2 %}
		{% stlink Matice a operace s maticemi, hodnost matice. | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.3 | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.9 | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.11 %}
		{% stlink Vlastní čísla a vlastní vektory matice. | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.10 %}
		{% stlink Charakteristický polynom, vztah vlastních čísel s kořeny polynomů. | /assets/priprava-na-statnice-mff-uk/la.pdf#chapter.12 %}
	{% endsttopic %}
	{% sttopic Diskrétní matematika | Diskrétka [[poznámky](/poznamky-z-prednasky/diskretni-matematika/)] 🃏, Kombagra 1 [[poznámky](/poznamky-z-prednasky/kombinatorika-a-grafy-i/)] 🃏 %}
		{% stlink 🟩 Relace, vlastnosti binárních relací. | /poznamky-z-prednasky/diskretni-matematika/#relace %}
		{% stlink 🟩 Ekvivalence a rozkladové třídy. | /poznamky-z-prednasky/diskretni-matematika/#ekvivalence %}
		{% stlink 🟩 Částečná uspořádání. | /poznamky-z-prednasky/diskretni-matematika/#uspořádání %}
		{% stlink 🟩 Funkce, typy funkcí. | /poznamky-z-prednasky/diskretni-matematika/#funkce %}
		{% stlink Permutace a jejich základní vlastnosti. | /poznamky-z-prednasky/diskretni-matematika/#segway-do-kombinatorického-počítání %}
		{% stlink Kombinační čísla, binomická věta. | /poznamky-z-prednasky/diskretni-matematika/#kombinatorika %}
		{% stlink 🟩 Princip inkluze a exkluze. | /poznamky-z-prednasky/diskretni-matematika/#princip-inkluzeexkluze %}
		{% stlink Hallova věta o systému různých reprezentantů, párování v bipartitním grafu. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#aplikace-tok%C5%AF-v-s%C3%ADt%C3%ADch %}
	{% endsttopic %}
	{% sttopic Teorie grafů | Diskrétka [[poznámky](/poznamky-z-prednasky/diskretni-matematika/)] 🃏, Kombagra 1 [[poznámky](/poznamky-z-prednasky/kombinatorika-a-grafy-i/)] 🃏 %}
		{% stlink 🟩 Základní pojmy, základní příklady grafů. | /poznamky-z-prednasky/diskretni-matematika/#grafy %}
		{% stlink 🟩 Souvislost grafů, komponenty souvislosti. | /poznamky-z-prednasky/diskretni-matematika/#rozšiřování-grafů %}
		{% stlink 🟩 Stromy, jejich vlastnosti, ekvivalentní charakteristiky stromů. | /poznamky-z-prednasky/diskretni-matematika/#stromy %}
		{% stlink 🟩 Rovinné grafy, Eulerova formule a maximální počet hran rovinného grafu. | /poznamky-z-prednasky/diskretni-matematika/#rovinné-nakreslení-grafu %}
		{% stlink 🟩 Barevnost grafů, klikovost grafů. | /poznamky-z-prednasky/diskretni-matematika/#barvení | /poznamky-z-prednasky/diskretni-matematika/#degenerovanost-klikovost-dualita %}
		{% stlink 🟧 Hranová a vrcholová souvislost grafů, Mengerova věta. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#míra-souvislosti-neorientovaných-grafu  %}
		{% stlink 🟩 Orientované grafy, silná a slabá souvislost. | /poznamky-z-prednasky/diskretni-matematika/#rozšiřování-grafů  %}
		{% stlink 🟧 Toky v sítích (min-flow/max-cut). | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#7-přednáška | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s14  %}
	{% endsttopic %}
	{% sttopic Pravděpodobnost a statistika | Diskrétka [[poznámky](/poznamky-z-prednasky/diskretni-matematika/)] 🃏, Past [[slidy](/assets/priprava-na-statnice-mff-uk/past/slides.pdf), [cheatsheet](/assets/priprava-na-statnice-mff-uk/past/cheatsheet.pdf)] 🃏 %}
		<li> Náhodné jevy, podmíněná pravděpodobnost, nezávislost náhodných jevů
		<li> Bayesův vzorec, aplikace.
		<li> Náhodné veličiny, střední hodnota, rozdělení náhodných veličin.
		<li> Geometrické, binomické a normální rozdělení.
		<li> Lineární kombinace náhodných veličin, linearita střední hodnoty.
		<li> Bodové odhady.
		<li> Intervaly spolehlivosti.
		<li> Testování hypotéz.
	{% endsttopic %}
	{% sttopic Logika | Výpal [[slidy](/assets/priprava-na-statnice-mff-uk/vypal.pdf)] 🃏 %}
		<li> Syntaxe - jazyk, otevřená a uzavřená formule.
		<li> Normální tvary výrokových formulí.
		<li> Prenexní tvary formulí predikátové logiky.
		<li> Převody na normální tvary, použití pro algoritmy (SAT, rezoluce).
		<li> Sémantika, pravdivost, lživost.
		<li> Nezávislost formule vzhledem k teorii, splnitelnost, tautologie.
		<li> Důsledek, pojem modelu teorie, extenze teorií.
	{% endsttopic %}
{% endsttopics %}

#### Informatika

{% sttopics %}
	{% sttopic Automaty a jazyky | Autogramy [[skripta](/assets/priprava-na-statnice-mff-uk/autogramy/skripta.pdf), [slidy](/assets/priprava-na-statnice-mff-uk/autogramy/slidy.pdf)] 🃏 %}
		{% stlink 🟩 Regulární jazyky, konečné automaty (deterministické, nedeterministické). | /assets/priprava-na-statnice-mff-uk/autogramy/skripta.pdf#page=2 %}
		{% stlink 🟧 Kleeneho věta, iterační lemma, regulární gramatiky. | /assets/priprava-na-statnice-mff-uk/autogramy/skripta.pdf#page=15 | /assets/priprava-na-statnice-mff-uk/autogramy/skripta.pdf#page=6 | /assets/priprava-na-statnice-mff-uk/autogramy/skripta.pdf#page=20 %}
		{% stlink Uzávěrové vlastnosti | /assets/priprava-na-statnice-mff-uk/autogramy/slidy.pdf#page=203 %}
		{% stlink Bezkontextové jazyky, zásobníkové automaty, bezkontextové gramatiky. | /assets/priprava-na-statnice-mff-uk/autogramy/skripta.pdf#page=19 | /assets/priprava-na-statnice-mff-uk/autogramy/slidy.pdf#page=141 | /assets/priprava-na-statnice-mff-uk/autogramy/skripta.pdf#page=24 %}
		{% stlink Turingův stroj, gramatika typu 0, diagonální jazyk, univerzální jazyk. | /assets/priprava-na-statnice-mff-uk/autogramy/slidy.pdf#page=214 | /assets/priprava-na-statnice-mff-uk/autogramy/slidy.pdf#page=248 | /assets/priprava-na-statnice-mff-uk/autogramy/slidy.pdf#page=252  %}
		{% stlink Chomského hierarchie. | /assets/priprava-na-statnice-mff-uk/autogramy/slidy.pdf#page=113 | /assets/priprava-na-statnice-mff-uk/autogramy/slidy.pdf#page=187 %}
	{% endsttopic %}
	{% sttopic Algoritmy a datové stuktury | ADS 1 a 2 [[Průvodce](/assets/priprava-na-statnice-mff-uk/pruvodce.pdf)] 🃏 %}
		{% stlink 🟩 Časová a prostorová složitost algoritmů, asymptotická notace. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s2  %}
		{% stlink 🟩 Třídy složitosti P a NP, NP-těžkost a NP-úplnost. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s19.3 | /assets/priprava-na-statnice-mff-uk/pvnp.png %}
		{% stlink 🟩 Algoritmy "rozděl a panuj", výpočet časové složitosti těchto algoritmů, příklady. |  /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s10 %}
		{% stlink 🟩 Binarní vyhledávací stromy, AVL stromy. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s8 %}
		{% stlink 🟩 Binární haldy. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s4.2 %}
		{% stlink 🟩 Hešování s přihrádkami a s otevřenou adresací. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s11.3 %}
		{% stlink 🟩 Třídící algoritmy. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s3  %}
		{% stlink 🟩 DFS, BFS a jejich aplikace. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s5 | https://stackoverflow.com/questions/20429310/why-is-depth-first-search-claimed-to-be-space-efficient %}
		{% stlink 🟩 Nejkratší cesty. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s6 %}
		{% stlink 🟩 Minimální kostry. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s7 %}
		{% stlink 🟧 Toky v sítích (základní algoritmy). | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s14 | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#7-přednáška  %}
		{% stlink 🟩 Euklidův algoritmus. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s1.3  %}
	{% endsttopic %}
	{% sttopic Programovací jazyky | Programko [[poznámky](/assets/priprava-na-statnice-mff-uk/prog2.pdf), [C#](/lecture-notes/the-cs-programming-language/)], Neprocko, Principy poč. [[poznámky](/poznamky-z-prednasky/principy-pocitacu/)] 🃏 %}
		<li> Koncepty pro abstrakci, zapouzdření a polymorfizmus.
		{% stlink Primitivní a objektové typy a jejich reprezentace. | /lecture-notes/the-cs-programming-language/#cil-type-system %}
		{% stlink Generické typy a funkcionální prvky. | /assets/priprava-na-statnice-mff-uk/prog2.pdf#page=20 %}
		{% stlink Práce s prostředky a mechanizmy pro ošetření chyb. | /lecture-notes/the-cs-programming-language/#exceptions %}
		{% stlink Životní cyklus objektů a správa paměti. | /lecture-notes/the-cs-programming-language/#heaps-and-gc %}
		<li> Vlákna a podpora synchronizace.
		<li> Implementace základních prvků objektových jazyků.
		<li> Nativní a interpretovaný běh, řízení překladu a sestavení programu.
	{% endsttopic %}
	{% sttopic Architektura počítačů a OS | Principy poč. [[poznámky](/poznamky-z-prednasky/principy-pocitacu/)] 🃏, Poč. systémy [[slidy](/assets/priprava-na-statnice-mff-uk/ps.pdf)] %}
		{% stlink Základní architektura počítače. | /poznamky-z-prednasky/principy-pocitacu/#zjednodu%C5%A1en%C3%A9-sch%C3%A9ma-po%C4%8D%C3%ADta%C4%8De | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=24 %}
		{% stlink Reprezentace dat a programů. | /poznamky-z-prednasky/principy-pocitacu/#k%C3%B3dov%C3%A1n%C3%AD-informace-v-po%C4%8D%C3%ADta%C4%8Di | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=60 %}
		{% stlink Instrukční sada, vazba na vyšší programovací jazyky. | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=29 %}
		{% stlink Podpora pro běh operačního systému. | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=97  %}
		{% stlink Rozhraní periferních zařízení a jejich obsluha. | /poznamky-z-prednasky/principy-pocitacu/#otro%C4%8Dina | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=105  %}
		{% stlink Základní abstrakce, rozhraní a mechanizmy OS pro běh programů, sdílení prostředků a vstup/výstup. | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=97  %}
		{% stlink Paralelismus, vlákna a rozhraní pro jejich správu, synchronizace vláken. | /assets/priprava-na-statnice-mff-uk/ps.pdf#page=112 %}
	{% endsttopic %}
{% endsttopics %}

### Specifická
Z následujících 7 jsou 1-3 povinné a z 4-7 je třeba vybrat dvě témata (ta moje jsou 4, 5).

{% sttopics %}
	{% sttopic Kombinatorika | Kombagra 1 [[poznámky](/poznamky-z-prednasky/kombinatorika-a-grafy-i/)] 🃏 a 2 [[poznámky](/poznamky-z-prednasky/kombinatorika-a-grafy-ii/)] 🃏 %}
		{% stlink Vytvořující funkce. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#generuj%C3%ADc%C3%AD-funkce %}
		{% stlink Odhady faktoriálů a kombinačních čísel. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#odhady-faktori%C3%A1lu %}
		{% stlink Ramseyovy věty. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#ramseyovy-barevn%C3%A9nekone%C4%8Dn%C3%A9-v%C4%9Bty %}
		{% stlink Samoopravné kódy. | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#samoopravn%C3%A9-k%C3%B3dy %}
	{% endsttopic %}
	{% sttopic Základy sítí | Sítě [[slidy](/assets/priprava-na-statnice-mff-uk/site.pdf)] 🃏 %}
		<li> Taxonomie počítačových sítí.
		<li> Architektura ISO/OSI.
		<li> Přehled síťového modelu TCP/IP.
		<li> Směrování.
		<li> Koncept adresy, portu, socketu.
		<li> Architektura klient/server.
		<li> Základy fungování protokolů HTTP, FTP a SMTP.
	{% endsttopic %}
	{% sttopic Diferenciální a integrální počet ve více rozměrech  | Matalýza 2 [[skripta](/assets/priprava-na-statnice-mff-uk/ma2.pdf)] 🃏 %}
		{% stlink Riemannův integrál. | /assets/priprava-na-statnice-mff-uk/ma2.pdf#section.8 | /assets/priprava-na-statnice-mff-uk/ma2.pdf#section.9 %}
		{% stlink Extrémy funkcí více proměnných. | /assets/priprava-na-statnice-mff-uk/ma2.pdf#section.5 %}
		{% stlink Metrický prostor, otevřené a uzavřené množiny, kompaktnost. | /assets/priprava-na-statnice-mff-uk/ma2.pdf#section.1 | /assets/priprava-na-statnice-mff-uk/ma2.pdf#section.3 %}
	{% endsttopic %}
	{% sttopic Optimalizace | Linprog [[skripta](/assets/priprava-na-statnice-mff-uk/linprog.pdf)] 🃏, Aprox. alg. [[poznámky](/poznamky-z-prednasky/aproximacni-algoritmy/)] 🃏, Kombagra 2 [[poznámky](/poznamky-z-prednasky/kombinatorika-a-grafy-ii/)] 🃏 %}
		{% stlink Mnohostěny, Minkowského-Weylova věta. | /assets/priprava-na-statnice-mff-uk/linprog.pdf#section.4 | /assets/priprava-na-statnice-mff-uk/linprog.pdf#page=12 %}
		{% stlink Základy lineárního programování, věty o dualitě, metody řešení. | /assets/priprava-na-statnice-mff-uk/linprog.pdf#section.2 | /assets/priprava-na-statnice-mff-uk/linprog.pdf#subsection.7.1 | /assets/priprava-na-statnice-mff-uk/linprog.pdf#section.5 %}
		{% stlink 🟩 Edmondsův algoritmus. | /poznamky-z-prednasky/kombinatorika-a-grafy-ii/#nejv%C4%9Bt%C5%A1%C3%AD-p%C3%A1rov%C3%A1n%C3%AD | https://www.youtube.com/watch?v=3roPs1Bvg1Q %}
		{% stlink Celočíselné programování. | /assets/priprava-na-statnice-mff-uk/linprog.pdf#page=4 %}
		{% stlink Aproximační algoritmy pro kombinatorické problémy: | /poznamky-z-prednasky/aproximacni-algoritmy/ %}
		<ul>
			{% stlink 🟩 splnitelnost | /lecture-notes/best-sat/ %}
			{% stlink nezávislé množiny | /poznamky-z-prednasky/aproximacni-algoritmy/#maximální-nezávislá-množina %}
			{% stlink množinové pokrytí | /poznamky-z-prednasky/aproximacni-algoritmy/#pokrývací-problémy %}
			{% stlink 🟩 rozvrhování | /poznamky-z-prednasky/aproximacni-algoritmy/#rozvrhov%C3%A1n%C3%AD %}
		</ul>
		{% stlink 🟧 Použití lineárního programování pro aproximační algoritmy. | /poznamky-z-prednasky/aproximacni-algoritmy/#lp-sat | /poznamky-z-prednasky/aproximacni-algoritmy/#pokrývací-problémy %}
		{% stlink 🟧 Využití pravděpodobnosti při návrhu algoritmů. | /lecture-notes/best-sat/  | /poznamky-z-prednasky/aproximacni-algoritmy/#nulovost-polynom%C5%AF-polynomial-identity-testing %}
	{% endsttopic %}
	{% sttopic Pokročilé Algoritmy a datové struktury | ADS 1 a 2 [[Průvodce](/assets/priprava-na-statnice-mff-uk/pruvodce.pdf)] 🃏 %}
		{% stlink 🟩 Výpočetní model RAM. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s2.5 %}
		{% stlink 🟩 Dynamické programování. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s12 %}
		{% stlink 🟩 Komponenty silné souvislosti orientovaných grafů. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s5.9 %}
		{% stlink 🟧 Toky v sítích (pokročilé algoritmy). | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s14 | /poznamky-z-prednasky/kombinatorika-a-grafy-i/#7-přednáška %}
		{% stlink 🟩 Vyhledávání v textu. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s13 %}
		{% stlink 🟧 Diskrétní Fourierova transformace a její aplikace. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s17 | /assets/priprava-na-statnice-mff-uk/fft.py %}
		{% stlink 🟧 Aproximační algoritmy a schémata. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s19.6 %}
		{% stlink 🟩 Paralelní algoritmy v hradlových a komparátorových sítích. | /assets/priprava-na-statnice-mff-uk/pruvodce.pdf#s15 %}
	{% endsttopic %}
	<hr>
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
