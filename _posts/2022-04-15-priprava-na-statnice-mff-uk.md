---
language: cz
title: Příprava na státnice (MFF UK)
---

- .
{:toc}

Tento článek obsahuje mou přípravu na státní zkoušky z **Obecné informatiky** pro akademický rok **2021/2022** (tj. nová akreditace).

### Obecná

#### Matematika

{% sttopics %}
	{% sttopic Základy diferenciálního a integrálního počtu | [Matalýza 1]() %}
		<li> Posloupnosti reálných čísel a jejich vlastnosti.
		<li> Reálné funkce jedné reálné proměnné.
		<li> Spojitost, limita funkce v bodě.
		<li> Derivace: definice a základní pravidla, průběhy funkcí, Taylorův polynom se zbytkem.
		<li> Primitivní funkce: definice, jednoznačnost, existence, metody výpočtu.
	{% endsttopic %}
	{% sttopic Algebra a lineární algebra | [Lingebra 1](), [Lingebra 2]() %}
		<li> Grupy a podgrupy, tělesa.
		<li> Vektorové prostory a podprostory.
		<li> Skalární součin, norma.
		<li> Kolmost, ortonormální báze.
		<li> Soustavy lineárních rovnic, Gaussova a Gaussova-Jordanova eliminace.
		<li> Matice a operace s maticemi, hodnost matice.
		<li> Vlastní čísla a vlastní vektory matice.
		<li> Charakteristický polynom, vztah vlastních čísel s kořeny polynomů.
	{% endsttopic %}
	{% sttopic Diskrétní matematika | [Diskrétka](), [Kombagra 1]() %}
		<li> Relace, vlastnosti binárních relací.
		<li> Ekvivalence a rozkladové třídy.
		<li> Částečná uspořádání.
		<li> Funkce, typy funkcí.
		<li> Permutace a jejich základní vlastnosti.
		<li> Kombinační čísla, binomická věta.
		<li> Princip inkluze a exkluze.
		<li> Hallova věta o systému různých reprezentantů, párování v bipartitním grafu.
	{% endsttopic %}
	{% sttopic Teorie grafů | [Diskrétka](), [Kombagra 1]() %}
		<li> Základní pojmy, základní příklady grafů.
		<li> Souvislost grafů, komponenty souvislosti.
		<li> Stromy, jejich vlastnosti, ekvivalentní charakteristiky stromů.
		<li> Rovinné grafy, Eulerova formule a maximální počet hran rovinného grafu.
		<li> Barevnost grafů, klikovost grafů.
		<li> Hranová a vrcholová souvislost grafů, Mengerova věta.
		<li> Orientované grafy, silná a slabá souvislost.
		<li> Toky v sítích.
	{% endsttopic %}
	{% sttopic Pravděpodobnost a statistika | [Diskrétka](), [Past 1]() %}
		<li> Náhodné jevy, podmíněná pravděpodobnost, nezávislost náhodných jevů, Bayesův vzorec, aplikace.
		<li> Náhodné veličiny, střední hodnota, rozdělení náhodných veličin, geometrické, binomické a normální rozdělení.
		<li> Lineární kombinace náhodných veličin, linearita střední hodnoty.
		<li> Bodové odhady, intervaly spolehlivosti, testování hypotéz.
	{% endsttopic %}
	{% sttopic Logika | [Výpal]() %}
		<li> Syntaxe - jazyk, otevřená a uzavřená formule.
		<li> Normální tvary výrokových formulí, prenexní tvary formulí predikátové logiky, převody na normální tvary, použití pro algoritmy (SAT, rezoluce).
		<li> Sémantika, pravdivost, lživost, nezávislost formule vzhledem k teorii, splnitelnost, tautologie, důsledek, pojem modelu teorie, extenze teorií.
	{% endsttopic %}
{% endsttopics %}

#### Informatika

{% sttopics %}
	{% sttopic Automaty a jazyky | [Autogramy]() %}
		<li> Regulární jazyky, konečné automaty (deterministické, nedeterministické).
		<li> Kleeneho věta, iterační lemma, regulární gramatiky.
		<li> Bezkontextové jazyky, zásobníkové automaty, bezkontextové gramatiky.
		<li> Turingův stroj, gramatika typu 0, diagonální jazyk, univerzální jazyk.
		<li> Chomského hierarchie.
	{% endsttopic %}
	{% sttopic Algoritmy a datové stuktury | [ADS 1](), [ADS 2]() %}
		<li> Časová a prostorová složitost algoritmů, asymptotická notace.
		<li> Třídy složitosti P a NP, NP-těžkost a NP-úplnost.
		<li> Algoritmy "rozděl a panuj", výpočet časové složitosti těchto algoritmů, příklady.
		<li> Binarní vyhledávací stromy, AVL stromy.
		<li> Binární haldy.
		<li> Hešování s přihrádkami a s otevřenou adresací.
		<li> Třídící algoritmy.
		<li> DFS, BFS a jejich aplikace.
		<li> Nejkratší cesty.
		<li> Minimální kostry.
		<li> Toky v sítích.
		<li> Euklidův algoritmus.
	{% endsttopic %}
	{% sttopic Programovací jazyky | [Programko 1](), [Programko 2](), [Principy počítačů]() %}
		<li> Koncepty pro abstrakci, zapouzdření a polymorfizmus.
		<li> Primitivní a objektové typy a jejich reprezentace.
		<li> Generické typy a funkcionální prvky.
		<li> Práce s prostředky a mechanizmy pro ošetření chyb.
		<li> Životní cyklus objektů a správa paměti.
		<li> Vlákna a podpora synchronizace.
		<li> Implementace základních prvků objektových jazyků.
		<li> Nativní a interpretovaný běh, řízení překladu a sestavení programu.
	{% endsttopic %}
	{% sttopic Architektura počítačů a operačních systémů | [Principy počítačů](), [Počítačové systémy](), [Úvod do sítí](), [Linux]() %}
		<li> Základní architektura počítače, reprezentace dat a programů.
		<li> Instrukční sada jako rozhraní hardware a software, vazba na prvky vyšších programovacích jazyků.
		<li> Podpora pro běh operačního systému.
		<li> Rozhraní periferních zařízení a jejich obsluha.
		<li> Základní abstrakce, rozhraní a mechanizmy OS pro běh programů, sdílení prostředků a vstup/výstup.
		<li> Paralelismus, vlákna a rozhraní pro jejich správu, synchronizace vláken.
	{% endsttopic %}
{% endsttopics %}

### Specifická
Z následujících 7 jsou 1-3 povinné a z 4-7 je třeba vybrat dvě témata.

{% sttopics %}
	{% sttopic Kombinatorika | [Kombagra 1](), [Kombagra 2]() %}
		{% stlink Vytvořující funkce. | https://slama.dev/poznamky-z-prednasky/kombinatorika-a-grafy-i/#generuj%C3%ADc%C3%AD-funkce %}
		{% stlink Odhady faktoriálů a kombinačních čísel. | https://slama.dev/poznamky-z-prednasky/kombinatorika-a-grafy-i/#odhady-faktori%C3%A1lu %}
		{% stlink Ramseyovy věty. | https://slama.dev/poznamky-z-prednasky/kombinatorika-a-grafy-i/#ramseyovy-barevn%C3%A9nekone%C4%8Dn%C3%A9-v%C4%9Bty %}
		{% stlink Samoopravné kódy. | https://slama.dev/poznamky-z-prednasky/kombinatorika-a-grafy-i/#samoopravn%C3%A9-k%C3%B3dy %}
	{% endsttopic %}
	{% sttopic Základy sítí | [Úvod do sítí]() %}
		<li> Taxonomie počítačových sítí.
		<li> Architektura ISO/OSI.
		<li> Přehled síťového modelu TCP/IP.
		<li> Směrování.
		<li> Koncept adresy, portu, socketu.
		<li> Architektura klient/server.
		<li> Základy fungování protokolů HTTP, FTP a SMTP.
	{% endsttopic %}
	{% sttopic Diferenciální a integrální počet ve více rozměrech  | [Matalýza 2]() %}
		<li> Riemannův integrál.
		<li> Extrémy funkcí více proměnných.
		<li> Metrický prostor, otevřené a uzavřené množiny, kompaktnost.
	{% endsttopic %}
	{% sttopic Optimalizace | [Linprog](), [Optimalizace]() %}
		<li> Mnohostěny, Minkowského-Weylova věta.
		<li> Základy lineárního programování, věty o dualitě, metody řešení.
		<li> Edmondsův algoritmus.
		<li> Celočíselné programování.
		<li> Aproximační algoritmy pro kombinatorické problémy (splnitelnost, nezávislé množiny, množinové pokrytí, rozvrhování).
		<li> Použití lineárního programování pro aproximační algoritmy.
		<li> Využití pravděpodobnosti při návrhu algoritmů.
	{% endsttopic %}
	{% sttopic Pokročilé Algoritmy a datové struktury | [ADS 1](), [ADS 2](), [Grafové algoritmy]() %}
		<li> Výpočetní model RAM.
		<li> Dynamické programování.
		<li> Komponenty silné souvislosti orientovaných grafů.
		<li> Maximální toky: algoritmy, aplikace.
		<li> Toky a cesty v celočíselně ohodnocených grafech.
		<li> Vyhledávání v textu.
		<li> Diskrétní Fourierova transformace a její aplikace.
		<li> Aproximační algoritmy a schémata.
		<li> Paralelní algoritmy v hradlových a komparátorových sítích.
	{% endsttopic %}
	{% sttopic ❌ Geometrie ❌ | [Základy KVG]() %}
		<li> Základní věty o konvexních množinách (Hellyho, Radonova, o oddělování).
		<li> Minkowského věta o mřížkách.
		<li> Konvexní mnohostěny (zákadní vlastnosti, V-mnohostěny, H-mnohostěny, kombinatorická složitost).
		<li> Geometrická dualita.
		<li> Voroného diagramy, arrangementy (komplexy) nadrovin, incidence bodů a přímek, základní algoritmy výpočetní geometrie (konstrukce arrangementu přímek v rovině, konstrukce konvexního obalu v rovině).
	{% endsttopic %}
	{% sttopic ❌ Pokročilá diskrétní matematika ❌ | [Kombagra 2](), [Teorie množin]() %}
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
