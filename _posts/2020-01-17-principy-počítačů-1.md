---
layout: post
language: cz
---

V rámci přípravy na zkoušku z Principů počítačů (zimní semestr MFF UK 2020) jsem vypracoval následující článek, ve kterém jsou shrnuty informace z přednášek ([1](https://youtu.be/nL93qIxszrk), [2](https://youtu.be/N112dIlaIMs), [3](https://youtu.be/mumyiiNFL7M), [4](https://youtu.be/buyf8My8KkI)  [5](https://youtu.be/_meq5MJblFo), [6](https://youtu.be/2AoY5wilmjs), [7](https://youtu.be/awGKgyk0bC4), [8](https://youtu.be/3v51UGll2C8), [9](https://youtu.be/4hNO09hRdGM), [10](https://youtu.be/gy_vfpFQij0), [11](https://youtu.be/yQdT56p5QTA), [12](https://youtu.be/uIuJKBjjHTk), [13](https://youtu.be/ybE0Ylw1WTs)).

- .
{:toc}

---

### Zjednodušené schéma počítače

{% xopp 19-07-10_22-58-36 & Harwardská architektura%}

- vymyšlena na univerzitě v Harwardu
- **CPU** -- vykonává instrukce
- **kódová paměť** -- uchovává instrukce
	- nemůže být upravován počítačem -- není tam zápis
- **datová paměť** -- uchovává data, se kterými pracujeme

### Historie

#### Charles Babbage (1837)
- mechanický stroj _analytical engine_
	- z dnešního pohledu plnohodnotný počítač
	- byl Turingovsky úplný!
	- nebyl nikdy fyzicky postaven
	- měl usnadnit počítání tehdy komplexního systému daní

#### Ana Lovelace
- dcera G. G. Byrona
- finančně Babbage podporovala
- příběhy o ní jako programátorce (psaní programů, ladění bugů) jsou vesměs nesmysl, ale:
	1. napsala manuál stroje
	2. napadlo ji, že by se mohlo pracovat i s **jinými informacemi než s čísly** (texty, obrazy, hudba...)

### Kódování informace v počítačí
- pojďme si zakódovat čísla {% latex %}0, 1, 2, \ldots, 1 000 000{% endlatex %}
	- kódování {% latex %}1 = 1{% endlatex %}V, {% latex %}2 = 2{% endlatex %}V by nešlo, jelikož se musí čekat na bouřku

#### Analogový přenos
- {% latex %}0 = 0{% endlatex %}V, {% latex %}1 000 000 = 5{% endlatex %}V
- v praxi zní skvěle, ale v realitě řada problémů, jelikož napětí ovlivňuje:
	- délka vodiče
	- teplota vodiče
	- elektromagnetické pole, které je vodičem jak generováno, tak přijímáno

{% xopp 19-07-10_23-07-42 & ztrátovost analogového přenosu %}

#### Digitální přenos
- problém je v intervalech, které se překrývají... co je odtáhnout od sebe?
- pouze _2 hodnoty_ -- logická 1 a logická 0
- jednotka _bit_ (BInary inpuT, značíme {% latex %}b{% endlatex %})
- funguje s rozumným šumem (100procentní ale není)

{% xopp 19-07-10_23-10-06 & digitální přenos%}

##### Sériový přenos
- způsob přenosu více bitů informace: pošleme je za sebe

{% xopp 19-07-10_23-11-43 & přenos čísla 1011 %}

- odpor vodiče vůči změně napětí -- změna není instantní (proto je real jiný než timing)

- počítání hodnoty **na měřáku**
{% xopp 19-07-10_23-14-05 & referenční přenos (barvy ukazují způsoby, jakými lze signál do cíle vést) %}

- počítání **rozdílu** dvou vodičů
- výhoda -- elektromagnetické rušení signál neovlivňuje, jelikož rozdíl je relativní
{% xopp 19-07-10_23-22-08 & diferenciální přenos %}

- délka bitů musí být jasně dána, aby přijímající dobře interpretoval informace
	- dnes bývá dána hardwarově
	- přenosová rychlost (= transfer rate)... **baud** (symbols / second)

##### MSb/LSb odbočka
- je potřeba se dohodnout, které bity čísel přijdou první
{% xopp 19-07-10_23-23-44 %}

### Dohoda přenosu
- problém: hodiny se časem kvůli HW rozejdou -- data pak stranám nedávají smysl
- řešení je několik...

#### (1) Nový stav
- vymyšlení _dalšího stavu_ přenosu, ve kterém k přenosu nedochází
- používá např. RS-232

1. odpojení vodiče = _floating state_ (plovoucí stav) 
	- lze detekovat, že je linka odpojena
	- není to ideální, nepoužívá se vždy

2. idle stav
	- na začátku je linka **idle**
	- start dohodou, většinou **rising edgem** (dobře se detekuje), poté držen (většinou 1) _start bit_
		- start (a end) bit je potřeba -- když by to jen vystřelilo, tak by to druhá strana kvůli šumu vůbec nemusela detekovat
	- se startem (rising edge) se synchronizují hodiny
	- hodiny nejsou perfektní... omezení přenosu na max {% latex %}n{% endlatex %} bitů, kde {% latex %}n{% endlatex %} je konstanta (v reálu {% latex %}8b = 1B{% endlatex %})
	- velký overhead... z {% latex %}10b{% endlatex %} je jen {% latex %}8b{% endlatex %} datových... {% latex %}\underbrace{1000}_{\text{clock}} \cdot \underbrace{\frac{8}{10}}_{\text{start + end}} = 800\ bps{% endlatex %}

{% xopp 19-18-10_12-16-39 & přenos s idle stavem %}

#### (2) Vodič s hodinovým signálem
- používá {% latex %}I_2C{% endlatex %}
- nový (referenční) vodič s digitálním (hodinovým) signálem
- diktuje, kdy lze na datovém vodiči číst
- zdá se, že je {% latex %}%50{% endlatex %} overhead, jelikož se data mohou detekovat pouze na rising edge
	- většinou ale max. rychlost není potřeba
	- když je potřeba, tak lze obejít: detekce na rising i falling
		- značí se DDR (double data rate)
		- problém to hardwarově detekovat -- používané jen tam, kde je rychlost nezbytná

#### (3) Průběžná detekce
- bylo by fajn průběžné synchronizovat na rising edge... co když ale chodí samé nuly?
- _clock recovery_ (obnova hodinového signálu) -- převod dat z {% latex %}\underbrace{8b}_{256} \rightarrow \underbrace{10b}_{1024}{% endlatex %} a vyberou se ty hezké konfigurace
	- různě konfigurace -- nemusí to nutně být 10
- výhoda: nemusíme dělit na bity, prostě pošleme proud dat

### Typy přenosu
1. **half-duplex**: 1 datový vodič -- zařízení se v přenosu střídají 
	- komplikované
	- nikdy nelze posílat najednou oběma směry
2. **full duplex**: 2 nezávislé simplexí linky
	- např. RS-232 -- 2 datové + 1 zem

{% xopp 19-18-10_11-18-27 & RS-232 %}

- význačné stavy (out-of-band) = dochází baterka/změna módu/...
	- někdy je potřeba sdělit uprostřed přenosu
	- digitální signály (1/0)
	- lze přes to zařízení i napájet

#### Značení
- {% latex %}1{% endlatex %} pravda a {% latex %}0{% endlatex %} nepravda, někdy se ale hodí prohodit
- značí se následně:

{% xopp 19-18-10_11-23-35 & inverzní logika %}

- rozlišení soustav:
{% latex display %} 23 = 23_d = 23_{10} = 23_{dec} \\ \$23 = 0x23 = 23h = 23_{16} = 23_{hex} {% endlatex %}

### Komunikační protokol
- dohoda, jak přenos vypadá... {% latex %} \underbrace{\mathrm{den}}_{9b}/\underbrace{\mathrm{měsíc}}_{5b}/\underbrace{\mathrm{rok}}_{7b} = \underbrace{101101010/11010/0010001}_{\text{pa(c)ket}} {% endlatex %}

- problém: starší zařízení mají {% latex %}1B=7b{% endlatex %}
	- řešení: řadič (controller), který přijímá data ze zařízení a zpracovává je

{% xopp 19-18-10_12-42-10 & řadič (controller) %}

- config register -- nastavení přenosové rychlosti, parity,...
- stav register -- zda se načetl celý byte

#### Python implementace RS-232
- data chodí v následné podobě:
{% latex display %} \cdots \overbrace{B_1B_2B_3B_4}^{\mathrm{read}(1024)}B_1B_2B_3B_4 \cdots {% endlatex %}

Počáteční nastavení:
```python
serialPort = serial.Serial()
serialPort.baudrate = 1200
serialPort.bytesize = serial.SEVENBITS
serialPort.stopbits = serial.STOPBITS_ONE
serialPort.parity = serial.PARITY_NONE
```

Vypnutí/zapnutí, aby se myš resetovala:
```python
serialPort.port = "COM4"
serialPort.timeout = 0.5

serialPort.open()

print("Initializing serial mouse ...")

# power down
serialPort.setRTS(False);
serialPort.setDTR(False);

time.sleep(0.150)
serialPort.flushInput();
serialPort.flushOutput();
time.sleep(0.150)

# power up
serialPort.setDTR(True);
serialPort.setRTS(True);
```

Čtení (ignore) identifikačních dat:
```python
done = False
while not done:
    data = serialPort.read(1024)
    if len(data) == 0:
        done = True
    else:
        print("Mouse identification data: ", data)
    
print("Serial mouse initialization completed ...")
```

Čtení informací myši v šestnáctkové soustavě:
```python
print("V2: Hexadecimal display: waiting for mouse packets (press and hold Ctrl key to continue to next example):")
done = False
pkt = []
while not done:
    # dead 4 byte packet from mouse into pkt list variable ...
    nextByte = serialPort.read(1)
    if len(nextByte) == 1:
        pkt.append(nextByte[0])
        if len(pkt) == 4:  # We got the whole 4 byte packet, start processing it ...

            print("Packet[", format(pkt[0], "02X"), format(pkt[1], "02X"), format(pkt[2], "02X"), format(pkt[3], "02X"), "] ", end="", flush=True)
            pkt = []
    
    if keyboard.is_pressed('ctrl'):
        print("*** Ctrl key is now pressed, please release Ctrl key to continue ***")
        while keyboard.is_pressed('ctrl'):
            pass
        done = True
```

##### Poznámky
- `serialPort.read` blokuje, `serialPort.timeout` ne (čeká timeout)
- modul `keyboard` -- neblokující `input()`	


### Binární odbočka

#### Operace
- binární:
	- `OR` -- `|` -- alespoň jedno
	- `AND` -- `&` -- oboje
	- `XOR` -- `^` -- právě jedno
	- `SHL` a `SHR` -- `<<` a `>>` -- **posouvá k MSb, ne doleva/doprava**
		- `ROL`, `ROR` (_bit rotation_) -- jako posun, ale cyklí čísla; opět k MSb
- unární:
	- `NOT` -- `!` -- opak

#### Záporná čísla v počítači
1. jako celá čísla, ale první bit je znaménko
	- docela k ničemu -- žádné normální bitové operace na to nefungují (sčítání, odčítání, porovnání...)
2. **one's complement** (jedničkový doplněk) -- u záporných se prohodí 1 a 0
	- funguje porovnání (kladné x kladné a záporné x záporné) a také sčítání
	- problematické: máme _dvě nuly_
3. **two's complement** (dvojkový doplňek) -- negace čísla je {% latex %}\mathrm{NOT}\left(\mathrm{ABS}\left(a\right)\right) + 1{% endlatex %}
	- řeší to problém se dvěma nulami
	- rozsah je {% latex %}-2^{n - 1} \ldots 2^{n - 1} - 1{% endlatex %}

### Čísla v Pythonu

#### Implementace
- jako pole... ukládá si právě tolik cifer, kolik je potřeba (+ padding do bytu)
- také potřebuje vědět, kolik bytů to číslo má
	- tím pádem je max. velikost {% latex %}2^{32} - 1{% endlatex %} bitů
- znamená to, že se operace chovají divně... `~255` je `-256` (`(0)1111110 -> (1)00000001`)

#### Misc.
- literály: `0x123` (hex), `0o123` (oct), `0b101` (bin)
- převody: `int(str, base)`, `hex(num)`, `bin(num)`, `oct(num)`

### Převody mezi datovými typy
- **truncation** -- useknutí cifer, které se do menšího datového typu nevejdou
	- přesně u signed intů nemusí fungovat... může se např. změnit znaménko
- extension:
	- **zero** extension -- doplnění nul na prázdná místa po zvětšení datového typu
		- nedává smysl u signed intů
	- **signed** extension -- doplnění o MSb
		- dává smysl u signed intů, ale _ne u unsigned_

### Otročina
- pojmy **master** (řídící; řídí komunikaci, dává požadavky) a **slave** (řízený; vykonává požadavky)
	- v komunikaci vždy 1 master a 1 slave
	- role se mohou měnit
	- směr _master {% latex %}\mapsto{% endlatex %} slave_ je **write**, obrácený **read**

{% xopp 19-10-11_13-10-25 & slave/master přenos %}

#### Připojení
- **point-to-point** linka:
	- z bodu do bodu -- 1 master a 1 slave
	- nepraktické -- reálně je procesor pořád master a museli bychom do něj vézt trilión linek
- **multidrop/bus** (sběrnice)
	- více slavů na jedné lince
	- pozor -- sběrnice znamená něco jiného, ale dnes se to takhle říká

{% xopp 19-10-11_13-15-26 & sběrnice %}

- rozlišují se **adresou,** která je pro každé zařízení na sběrnici _unikátní_
	- rozsahu těchto adres se říká **adresový prostor** (adress space)
- linky jsou half-duplexy bez floatingového stavu
	- vždy se mezi sebou baví 2 zařízení

{% xopp 19-10-11_13-19-36 & implementace sběrnice %}

- když nevysílá nikdo, je tam díky pull-up rezistoru {% latex %}1{% endlatex %}; když někdo {% latex %}0{% endlatex %}, tak {% latex %}0{% endlatex %}
- to, že se to spolu vlastně mlátí budeme řešit až na vyšší úrovni

##### {% latex %}\text{I}^2 \text{C}{% endlatex %} (Inter Integrated Circuit)
- je to opravdová sběrnice
- podporuje **multimaster** -- více zařízení mohou být master
	- mohou se i střídat -- chvíli master, chvíli slave
	- rozdíl mezi USB -- to je single master

{% xopp 19-10-11_13-25-36 & I2C sběrnice %}

- SDA = serial data; SCL = serial clock 
- idle stav je vždy vyrušen masterem, který chce navázat komunikaci
	- rovněž _generuje hodinový signál_
	- začátek nastává, když nastane {% latex %}0{% endlatex %} na SDA a {% latex %}1{% endlatex %} na SCL (zakázaný stav!)

{% xopp 19-10-11_13-27-58 & komunikace v I2C %}

- {% latex %}9{% endlatex %} bit na byte
	- {% latex %}8{% endlatex %} data (MSb-first)
	- {% latex %}1{% endlatex %} acknowledgement bit (ack = ano; nak = ne)
		- pro {% latex %}0{% endlatex %} je ACK, {% latex %}1{% endlatex %} je NAK, jelikož {% latex %}0{% endlatex %} stahuje... pokud tam slave není, tak tam bude implicitně {% latex %}1{% endlatex %})
	- pořadí (při přenosu `B1 A1 B2 A2 B3 A3`) se liší následně:
		- write: `M/S/M/S/M/S...` (slave potvrzuje že přečetl)
		- read: `M/S/S/M/S/M...` (slave potvrzuje že posílá a pak začne posílat)
- pro clock jsou dány standardizované rozsahy, aby to slave ustál
	- má možnost dělat **clock stretching** -- pokud by nestíhal, tak může hodiny podržet na 0 (hold low)

{% xopp 19-10-11_13-34-38 & struktura přenosu I2C %}

- **management** je obecný pro {% latex %}I_2C{% endlatex %}; zbytek je device-specific
	- 1-7 je adresa, 8 je r/w
- **payload** -- to, „za co platíme“ (samotná data)

{% xopp 19-10-11_13-36-02 & I2C zařízení (ambient light sensor) %}
- ADC = analog-digital converter -- převod analogu do digitálu
	- přijímáme světlo (analogový signál)
- bus interface -- řídí zařízení, komunikuje,...
	- pro vyrábění k jiné sběrnici stačí nahradit pouze tohle
- adresa je _pevně daná_... na sběrnici může být pouze jedno
- zařízení má 2 registry (read only, write only)
	- znamená to, že _nemusíme rozlišovat_, ze kterého registru číst a do kterého psát

### Paměť
- _paměťový adresový prostor_ -- rozsah adres v paměti
	- pro {% latex %}200B{% endlatex %} bude {% latex %}8b{% endlatex %}
	- většinou i pro {% latex %}128B{% endlatex %} bude {% latex %}8b{% endlatex %} (se {% latex %}7b{% endlatex %} se nepracuje skvěle)
	- pro {% latex %}256B{% endlatex %} může být {% latex %}16b{% endlatex %} -- dobře se to scaluje (při upgradu hardwaru)

#### Jednotky
- {% latex %}1 kB{% endlatex %} není {% latex %}1000b{% endlatex %} (nepraktické), ale {% latex %}1024b{% endlatex %}
	- používají všichni... až na výrobce pevných disků
	- dnes se hodí používat jasnější značení {% latex %}1024B = 1 KiB{% endlatex %} (ki-bi-bajt)

| paměť                         | adresový prostor             | v reálu                                                                     |
| ---                           | ---                          | ---                                                                         |
| {% latex %}1 kB{% endlatex %} | {% latex %}10b{% endlatex %} | {% latex %}16b{% endlatex %} prostor ~ {% latex %}64 kB{% endlatex %} adres |
| {% latex %}1 MB{% endlatex %} | {% latex %}20b{% endlatex %} | {% latex %}24b{% endlatex %} prostor ~ {% latex %}16 MB{% endlatex %} adres |
| {% latex %}1 GB{% endlatex %} | {% latex %}30b{% endlatex %} | {% latex %}32b{% endlatex %} prostor ~ {% latex %}4 GB{% endlatex %} adres  |

#### Typy paměti

##### SRAM (static random access memory)
- 1 bit je 4 až 6 tranzistorů
- můžeme přistupovat k libovolné hodnotě
- všechny trvají stejně dlouho (staví na tom algoritmizace) -- v realitě 
	- **sekvenční** přístupy jsou rychlejší
	- **obrácené sekvenční** jsou něco mezi
	- **náhodné** přístupy jsou pomalejší
- je RW a **volatile** (po vypnutí ztratí všechna data)
- kapacita je malá (řádově MB)
- přístup {% latex %}10{% endlatex %}-{% latex %}100 GBps{% endlatex %}; ~{% latex %}1 ns{% endlatex %}

##### DRAM (dynamic random access memory)
- {% latex %}1b{% endlatex %} = 1 tranzistor a 1 kondenzátor
- levnější a větší (řádově GB), ale pomalejší (nabíjí/vybíjí se pomalu)
- v rámci přístupu pro ni platí (zhruba) to samé jako pro SRAM
- hodnoty si pamatuje _krátce_ (kondenzátory...)
	- každou {% latex %}1 ms{% endlatex %} je potřeba refresh (přečteme a zapíšeme)
	- částečně může za pomalý access time (pořád se čte a zapisuje)
- přístup {% latex %}1{% endlatex %}-{% latex %}10 GBps{% endlatex %}; ~{% latex %}10 ns{% endlatex %}

#### Co je to slovo?
1. **správná definice** -- jednotka přenosu
	- pro {% latex %}n{% endlatex %}-bitové zařízení je to {% latex %}n{% endlatex %}-bitové slovo
	- pro {% latex %}8b{% endlatex %} paměť to např. znamená, že lze vyžádat pouze {% latex %}8b{% endlatex %}
2. **špatná definice** -- {% latex %}16b{% endlatex %} (dáno historicky)
	- _double word_ (dword) = {% latex %}32b{% endlatex %}
	- _quad word_ (qword) = {% latex %}64b{% endlatex %}

#### Rozbor PCF8570 SRAM paměti
- {% latex %}3b{% endlatex %} programovatelná adresa, `1010` vestavěná
- rychlost přenosu přes {% latex %}I_2C{% endlatex %} je cca. {% latex %}100000Hz \sim 100000 bps{% endlatex %}
	- {% latex %}I_2C{% endlatex %} overhead je {% latex %}x / \left(3 \cdot 9\right) \rightarrow 3708 bps{% endlatex %}
		- na každou transakci ({% latex %}8b{% endlatex %} + ack) přeneseme 3B, z toho jen 1 jsou data
		- jde to zlepšit -- burst přenos (nezačínáme další přenosy, jen sekvenčně čteme/zapisujeme): {% latex %}\left(x - \left(2 \cdot 9\right)\right) /  9 \rightarrow 11109 bps{% endlatex %}
- zápis -- 1 transakce
- čtení -- 2 transakce (psaní do adresového registru nějakou hodnotu + zápis slova)

{% xopp 19-18-11_11-47-34 & PCF8570 pamět %}

### Instrukce, architektury
- **instrukce** -- posloupnost {% latex %}n{% endlatex %} bytů
- **instrukční sada** (instruction set) -- instrukce podporované daným CPU
- **strojový kód** -- posloupnost instrukcí  (machine code)
- **instruction pointer** (IP) -- pozice aktuálně ukazované instrukce
	- zpravidla ukazuje na první bit (vícebitové) instrukce
	- je {% latex %}x{% endlatex %}-bitový (logicky stejně jako code memory)

{% xopp 19-24-11_22-40-04 & architektura s instrukcemi %}

- **opcode** (operation code) -- typ instrukce
	- podle toho se interpretují argumenty
	- bývá {% latex %}1B{% endlatex %} až {% latex %}2B{% endlatex %}
- argumenty -- s čím pracovat -- hodnota/adresa/...

{% xopp 19-24-11_22-50-13 & struktura instrukcí %}

{% xopp 19-24-11_22-52-17 & jak to funguje doopravdy %}

#### Endianita
- pochází z Gulliverových cest podle skupin lidí, kteří jedli vejce z různých konců -- little end(iáni), big end(iáni)
	- je to ve výsledku vlastně úplně jedno, jen je potřeba si něco zvolit
- většina procesorů je *little endian* (ten divný způsob)

{% xopp 19-24-11_22-54-12 & endianita %}

#### Harward x von Neumann

{% xopp 19-24-11_22-56-28 %}

#### Historie CPU architektur
- G502 (Apple I -- Wozniak)
	- 8-bit CPU
	- von Neumann
	- 16-bit addr space (64 kB operační paměti)
	- little endian
- Intel 8088 
	- 16-bit CPU
	- 20-bit addr space (1 MB operační paměti)
	- little endian
	- převládlo -- 20-bit address space byl velká výhoda

#### Příklady instrukcí

| 6502            | x86                       | poznámka                       |
| ---             | ---                       | ---                            |
| `$EA`           | `$90`                     | posune IP                      |
| `$4C xx_0 xx_1` | `$E9 xx_0 xx_1 xx_2 xx_3` | skok na adresu `xx_1 xx_0 ...` |

- dost nepraktické (není tomu rozumět) -- řeší to **assembler**
	- skok je např. `JMP`, load je `LDA`, store je `STA`
- aritmetika je trochu problematická -- x86 ani 6502 neumějí ukládat na třetí adresu... je potřeba `LOAD a -> R1, ADD R2 + b, STORE R2 a`
- `T` instrukce -- transfer z jednoho registru do druhého (`TAX`, `TXA`,...)

#### Příznakový registr CPU
- 1 příznak (flag) = 1 bit informace
	- zero -- jestli poslední výsledek byla 0
	- sign -- záporný výsledek operace
	- carry (přenos) -- z nějakých operací
		- operace to definují různě (podle toho, co potřebují)
- `SET` a `CLR` instrukce umožňují explicitně upravovat hodnoty registrů

#### 6502 -- akumulátorová architektura
- `A` -- registr, na kterém se provádějí všechny aritmetické operace
- podpora `AND`, `OR`, `XOR`, `SHR`, `SHL`, `ROL`, `ROR`
	- bacha... `NOT` nemá (jde ale přes `XOR` s jedničkami)
- pro vícebitové proměnné je potřeba rozdělit na části a řešit zvlášť

##### Sčítání a odčítání
{% xopp 19-01-12_18-33-09 & sčítací (odčítací) blackbox %}
- je potřeba explicitně nastavit `carry` příznak na 0 (`CLC` instrukce)
	- řetězení: `LDA CLC ADC STA | LDA ADC STA | ...`
- přepis sčítání na odčítání
	1. přepsání na sčítání: `A := v - A  ->  v + (-A)  ->  v + (NOT(A) + 1)`
	2. subtract w/ borrow (SBB) -- carry je borrow 
		- carry znamená, že si něco potřebuji půjčit z vyššího řádu
		- principiálně stejné jako normální sčítání
		- x86 to takhle dělá
		- problematické: v HW to není lehké dělat
	3. subtract w/ carry (SBC) -- carry je _not borrow_
		- nezapomenout na začátku pomocí `SEC` nastavit carry na 1
		- snadněji se to HW implementuje
		- funguje na to hezký trik (B je borrow; C je carry):

```
A - X - B              // odečítání X a borrow od A
A - X - B + 256        // 256 je obecně n-bit
A - X - (1 - C) + 256  // použití carry flagu
A + (255 - X) + C
A + NOT(X) + C
```

#### x86
- více registrů = více svobody!
- {% latex %}32b{% endlatex %} slovo + {% latex %}32b{% endlatex %} address space
- `EFlags` -- flagy
- obecné registry (7) -- můžeme s nimi dělat, co chceme
	-  v rámci zpětné podpory dovolují pracovat s prvními {% latex %}8b{% endlatex %}, {% latex %}16b{% endlatex %}, {% latex %}9{% endlatex %}-{% latex %}16b{% endlatex %}...
	- lehčeji se řeší komplexní výrazy -- `a + b + e - (c + d)`
		- u 6502 bychom museli pořád ukládat do akumulátoru (a dokonce ještě někam do paměti)
		- u x86 můžeme použít více registrů

##### Příklady instrukcí
- obecný tvar (assembleru): `OP target, source`
- `MOV EAX, [EXP]` -- přesun z adresy na pozici hodnoty `EXP` do registru `EAX`
- `MOV [EAX], EXP` -- přesun z `EXP` do paměti na adrese v `EAX`
- `ADD`/`ADC` -- s/bez carry

##### Rychlost operací
- GHz -- jednotka rychlosti procesoru (takty)
	- 1 takt... {% latex %}1 / \mathrm{rychlost}{% endlatex %}
- dnes už lze za 1 takt zvládnout základní instrukce jako logické, aritmetiku...
	- bavíme se o operacích _na registrech_ -- přístup do paměti je významně pomalejší
- také záleží na tom, zda nesčítáme {% latex %}64b{% endlatex %} čísla na {% latex %}32b{% endlatex %} architektuře
	- když ale sčítáme {% latex %}16b{% endlatex %} na {% latex %}32b{% endlatex %}, tak je to také 1 takt

#### Čísla v Pythonu, vol. 2
- blocky jsou vlastně {% latex %}32b{% endlatex %}, jelikož se očekává, že budou běžet (alespoň) na {% latex %}32b{% endlatex %} architektuře (to před tím byl trochu kec)
- stále tam je {% latex %}32b{% endlatex %}, které určuje, kolik bitů je využito
- kolik zabírá `x = 5` v Pythonu:
	- {% latex %}+4B{% endlatex %} -- samotné číslo
	- {% latex %}+4B{% endlatex %} -- proměnná určující, kolik bitů je využito
	- {% latex %}+4B{% endlatex %}/{% latex %}8B{% endlatex %} (podle architektury) -- adresa, jelikož `int` je objekt
	- {% latex %}+4B{% endlatex %} -- typ proměnné
	- {% latex %}+4B{% endlatex %} -- **reference counting** -- kolik proměnných ukazuje na hodnotu
	- musí se s tím provádět hrozně šaškáren... je to vážně pomalé (klidně až 100x)
- trochu záchrana -- čísla od {% latex %}-5{% endlatex %} do {% latex %}256{% endlatex %} jsou optimalizovány (uloženy někde v tabulce)
- má výhodu -- nemusíme řešit **arithmetic overflow** (přetečení) nebo **underflow** (podtečení)
- ještě pozor: reálně je v každém bloku uloženo jen {% latex %}30b{% endlatex %} hodnot, jelikož poslední je chápán jako carry příznak (Python nevidí do procesoru)

#### Násobení a dělení
- trochu těžší instrukce -- bývají pomalejší (dobré s tím počítat):
	- násobení -- 10 taktů
	- dělení -- 10/100 taktů

| operace | x86/x64 | ARM (mobily) | {% latex %}\mu C{% endlatex %} | 6502    |
| ---     | ---     | ---          | ---                            | ---     |
| *       | ano     | ano          | možná                          | ne      |
| //      | ano     | možná        | ne                             | fakt ne |

- je potřeba to na architekturách, které to nemají, softwarově implementovat
	- `SHL` je násobení 2 je `SHL`; dělení 2 je `SHR`
		- násobení a dělení jinými čísly lze rozdělit na posuny a součty (pokročilé)
	- pozor na signed čísla -- `SHL` funguje jen pro menší čísla a `SHR` nefunguje vůbec
		- je potřeba `SAR` (kopíruje MSb), ale pořád to není ono (`-5 // 2 = -3`)


#### Reálná čísla

##### Fixed-point
- pevný počet bitů pro části před a za desetinou čárkou
- hezky na tom funguje aritmetika -- můžeme normálně sčítat, odčítat, porovnávat...
	- výrazně rychlejší než floating-point (viz. dále)
- problém na operacích s hodně velkými a hodně malými čísly -- přesnost...

##### Floating-point
- čísla v normalizovaném formátu: {% latex %}1.0110101 \cdot 10^n{% endlatex %}

{% xopp 20-19-01_13-29-05 & struktura floating-point čísla %}

- v mantise první 1 ignorujeme (je tam totiž v normalizovaném tvaru vždy)
- exponent je v _bias_ reprezentaci: mapování {% latex %}\left(-n, n\right) \mapsto \left(0, 2n - 1\right){% endlatex %}
	- převody jsou přičítání/odčítání biasu
	- hodí se (později uvidíme proč)
- SW implementace by byla pomalá -- bývá to podporováno v CPU
	- floating-point registry
	- stejně pomalejší než celá čísla

| x86/x64 | ARM (mobily) | {% latex %}\mu C{% endlatex %} | 6502 |
| ---     | ---          | ---                            | ---  |
| HW      | HW/SW        | SW                             | SW   |

###### IEEE 754
- standarta definující {% latex %}32b{% endlatex %} a {% latex %}64b{% endlatex %} floating point čísla
- pro {% latex %}32b{% endlatex %} (float) je {% latex %}1b-8b-23b{% endlatex %}
- pro {% latex %}64b{% endlatex %} (double) je {% latex %}1b-11b-52b{% endlatex %}
	- takhle je to ukládané Pythonu

###### Ošklivá čísla
- {% latex %}0.1{% endlatex %} nelze reprezentovat jako floating-point číslo (nekonečný zápis)
	- programy proto zaokrouhlují
	- {% latex %}0.1 + 0.2 = 0.300000000000004{% endlatex %}... 
- _nikdy floating point čísla neporovnávat_ -- používat {% latex %}abs(a - b) < \epsilon{% endlatex %}

###### Speciální hodnoty
- pro nulový exponent je číslo v denormalizovaném tvaru (pro reprezentaci fakt hodně malých čísel)
- {% latex %}0{% endlatex %} jsou samé nuly (až na znaménko)
	- proto jsme volili reprezentaci s biasem
	- znaménko znamená, že máme 2 nuly, standard definuje oboje jako to samé
- samé {% latex %}1{% endlatex %} v exponentu nabývá podle znaménka a mantisy speciálních hodnot ({% latex %}\infty{% endlatex %}, {% latex %}\mathrm{nan}{% endlatex %}...):
	- {% latex %}\infty / 2 = \infty{% endlatex %}; {% latex %}\infty + 2 = \infty{% endlatex %}
	- {% latex %}\infty / \infty = \mathrm{nan}{% endlatex %} (not a number)
		- cokoliv + {% latex %}\mathrm{nan}{% endlatex %} je {% latex %}\mathrm{nan}{% endlatex %}
		- existuje více typů {% latex %}\mathrm{nan}{% endlatex %} (podle vzniku)
	- {% latex %}1.0 / 0{% endlatex %} bývá v normálních jazycích {% latex %}\infty{% endlatex %}, Python ale kontroluje dělení nulou a hodí chybu

### Paměti ROM
- jsou _non-volatile_ -- hodnoty přežijí vypnutí počítače

| typ                         | write                             | read                            |
| ROM (Read Only Memory)      | {% latex %}1{% endlatex %}        | {% latex %}\infty{% endlatex %} |
| PROM (Programable ROM)      | {% latex %}1{% endlatex %}        | {% latex %}\infty{% endlatex %} |
| EPROM (Erasable PROM)       | „{% latex %}\infty{% endlatex %}“ | {% latex %}\infty{% endlatex %} |
| EEPROM (Electrically EPROM) | „{% latex %}\infty{% endlatex %}“ | {% latex %}\infty{% endlatex %} |

- EPROM -- problém s mazáním (dělá se to s UV zářením... nepraktické)
- EEPROM -- všechno tím nahradit nechceme, je pomalejší
	- také jim lze říkat **NVRAM** (non-volatile [[RAM]])
	- omezený počet writů kvůli tomu, že fyzikálně se elektrony připojí do obalu atomů a nejdou pak moc dobře vytlačit
	- adresovatelné po individuálních bytech
	- **flash** -- jiná výrobní technologie
		- dokáže zapsat/vracet velké bloky -- {% latex %}1{% endlatex %}/{% latex %}10 kB{% endlatex %}
		- rychlejší na přístup k většímu počtu dat, pomalejší na random přístup

{% xopp 20-19-01_18-52-03 & Harward počítač (s GPIO) %}
- {% latex %}GPIO{% endlatex %} = General Purpose Input and Output
	- slouží jak pro vstup, tak pro výstup
	- `DIR` registry určuje směr pinů, `IN` a `OUT` jsou hodnoty na vstupu/výstupu

#### Permanentní datové uložiště
- hodilo by se -- konfigurace (když umře napájení...)

##### HDD
- podle magnetického pólu na daném místě 1 nebo 0
- **sektor** -- dnes {% latex %}4 kB{% endlatex %} (dříve {% latex %}512B{% endlatex %})
- **hlavičky** -- pohybují se všechny najednou
- disk se otáčí, hlavičky se hýbají do strany -- podle toho přístup k bytům
- adresa hodnoty je trojice **CHS** (cylindr, hlava, sektor)
- přístup vně je lepší -- rychlost sektorů dále od středu je větší
	- zaplňují se od vnějších po vnitřní

{% xopp 20-19-01_19-04-31 & HDD %}

###### Výhody
- levnější než alternativy
- velké množství data

###### Nevýhody
- náchylné na poškození
- sekvenční přístup je fajn (disk se otáčí), obráceny je příšerný
- docela pomalé... 10 ms sekvenční / 0.5 MB/s obrácený sekvenční

##### CD / DVD / BLURAY
- optické -- pokud se odrazí, tak {% latex %}1{% endlatex %}; jinak {% latex %}0{% endlatex %}
- nejsou optimální pro archivační (řádově 10ky let) -- vypalovací se vrací do svého původního stavu 
- oproti pevnému disku jsou data spirála (jako gramofonová deska)

{% xopp 20-19-01_19-22-10 & CD %}

- používá **LBA** -- linear block adressing (není to už trojice -- lehčí na programování)
- přenosová rychlost je menší (**10 MBps**), přístupová také ({% latex %}100 ms{% endlatex %})

##### Řadiče pro uložiště
- registry:
	- adresový
	- příkazový
	- buffer (postupné čtení/zápis)
	- info registr (počet sektorů, velikost sektoru,...)
- bylo by nepraktické používat na každé zařízení jiný -- pro všechny se používá **LBA**, jen tam jsou vždy pro příslušná zařízení mapování:
	- pro HDD dochází k mapování LBA {% latex %}\iff{% endlatex %} CHS
	- takhle připojený flash disk je vlastně SSD (Solid State Drive)

### Adresování, soubory
- **offset** (v {% latex %}B{% endlatex %}) -- posun od začátku paměti
- **base address** -- odkud začínáme (čteme/píšeme/...)
- `bytes` objekt v Pythonu -- práce s byty
	- lze je indexovat (`bts[0]`)

{% xopp 20-19-01_19-37-02 & struktura paměti %}

- **metadata** -- _data o datech_; ukládá:
	- čísla sektorů, kde se soubor nachází
		- princip _fragmentace_ -- rozdělení souborů do více sektorů; nechtěné (přístup je pomalejší)
	- jméno souboru
	- velikost
	- obecně: volné sektory
- **OS** -- abstrakce nad disky
	- stejné API pro čtení, psaní, práce s metadaty...
	- používají všechny programy -- `open("file", "r")` volá systémovou funkci

#### V Pythonu
- `f = open(..., "r")` říká, že je to textový soubor
	- `rb` -- read binary -- interpretuje jako binární
	- `f.readline()` -- čtení řádku
	- `f.read()` -- čtení všeho; parametr určí počet bytů
		- může vrátit měně, když toho tam tolik není
	- `f` také ukládá aktuální offset
		- čtení ho mění
		- `seek(pos)` -- nastavení offsetu od začátku souboru (v bytech)

#### Šestnáctkový výpis
- hex view(er) -- vypsání souborů jako šestnáctkové byty
- {% latex %}1B{% endlatex %} = 1 znak
- 3 sloupečky (po 16 znacích):
	1. hex offset (pozice v souboru)
	2. hex zapis (`AF 1F 3C 14 ...`)
	3. (pokus o) interpretace dat jako text

#### Reprezentace obrazu
- bitmapy -- mapy bitů
- rozdělíme na **pixely** -- na každém bude informace o tom, „jaké je tam světlo“

{% xopp 20-19-01_20-01-26 & obrázek v počítači %}

- indexováno {% latex %}(x, y){% endlatex %}
	- pozor -- {% latex %}y{% endlatex %} jdoucí dolů _stoupá_, neklesá
- v paměti bývá uloženo po řádcích

##### Pixel
- co sem uložit? fotonů máme od {% latex %}0{% endlatex %} do {% latex %}\infty{% endlatex %}
	- je třeba (dobře) stanovit meze (analog {% latex %}\rightarrow{% endlatex %} digital) -- mapování intenzit
- **bit depth** (bpp = bitová hloubka) -- kolik dat máme na pixel: 
	- {% latex %}1b{% endlatex %} -- černobílá
	- {% latex %}8b{% endlatex %} -- odstíny šedi
	- floating pointy -- větší rozsah (HDR)
		- problémy: lidské oko to neumí dobře zpracovávat a foťáky to neumí dobře fotit
- není foton jako foton: frekvence určuje barvu
	- vnímáme malé spektrum (viditelně světlo)
	- tyčinky (rozsah) x čípky (frekvence -- 3 barvy)

{% xopp 20-19-01_20-15-41 & čipky v oku %}

- barevná bit depth (různě úrovně)
	- {% latex %}3b{% endlatex %} na pixel -- dost neúsporné (jen jestli je červelá/zelená/modrá) a blbě se rozděluje
	- {% latex %}4b{% endlatex %} na pixel -- poslední je intenzita (1 násobí vše 2x)
	- {% latex %}2B{% endlatex %} na pixel -- 5R/5G/5B/1 nic
		- někdy ten 1 bývá v zelené složce (oko je na ni citlivější)
	- {% latex %}3B{% endlatex %} na pixel (true color; 65535 barev)
		- je to ošklivě nesoudělné; ukládá se většinou do {% latex %}32b{% endlatex %}... co se zbylými {% latex %}8b{% endlatex %}?
			- plýtvat
			- vytvořit na alpha kanál určující (ne)průhlednost pixelu (255 je neprůhledné, 0 transparentní)

##### Ukládání do paměti
- nestačí je jen uložit za sebe -- potřebujeme metadata (obrázku, ne souboru), jako např.:
	1. bitová hloubka
	2. výška, šířka
	3. pořadí barev (endianita) -- `RGB(A)` / `(A)BGR` (populárnější) 
	4. offset, na kterém začínají data

- obecně metadata (hlavička) bývají na začátku souboru, abychom ji přečetli první

###### BMP
- původně Windows formát
- relativně jednoduchý
- data jsou little endian (jak čísla, tak barvy)
- první {% latex %}2B{% endlatex %} jsou **magic** (signature) znaky
	- měly by být unikátní pro typy souborů
	- dány autorem
	- zajímavost exe má `5a 4d`, což je v ASCII `MZ` -- iniciály Marka Zbikowskiho (autor)

#### Reprezentace textu
- **string** -- posloupnost znaků
	- písmena (abcdegh)
	- číslice (123456789)
	- symboly (@#$%^&*)
	- whitespace (mezera, tabulátor)
- **grafém** -- nejmenší jednotka psaného jazyka
- **kódování** (většinou pro celý text) zavádí:
	1. 1 znak {% latex %}\iff{% endlatex %} 1 kód (číslo) 
	2. kód {% latex %}\iff{% endlatex %} binární reprezentace
		- zda bude 1 kód = {% latex %}1B{% endlatex %}, {% latex %}2B{% endlatex %}, proměnlivý...
- ukládaní do paměti tak, jak by se text četl (latinka levo-pravo, arabština pravo-levo...)
- historicky _nemívá metadata_ -- problematické (určovaní kódovaní)

##### ASCII
- _American Standard Code for Information Interchange_
- standardizování v 80. letech
- {% latex %}7b{% endlatex %} kódování ({% latex %}0{% endlatex %}-{% latex %}127{% endlatex %})
- číslice i písmena jsou v kódování blízko sebe -- lze je dobře vyčíst, převádět...
- **extended** -- rozšíření
	- každá část Evropy (W/M/E) si to rozšířila jinak
		- ISO8859-2 (Latin 2) -- snaha o standardizaci, ale trochu pozdě
		- Win1250 -- Windowsové kódování 

##### Unicode
- standardizace -- všechny jazyky, všechny symboly, ~~žádné problémy~~
- {% latex %}0{% endlatex %}-{% latex %}127{% endlatex %} -- odpovídají kódům z ASCII
- {% latex %}128{% endlatex %}-{% latex %}\$FFFF{% endlatex %} -- běžně znaky
- problém -- neurčili binární reprezentaci, takže vznikly různé:
	- **UTF-32** -- každý znak je 4B
		- 2 verze UTF32 LE a UTF32 BE... guláš
		- paměťově ne moc příjemné
	- **UCS-2** -- jednoduché (a debilní)
		- podporuje pevné {% latex %}2B{% endlatex %}... dokážeme reprezentovat pouze znaky v téhle mezi
	- **UTF-16** - proměnlivá délka znaku ({% latex %}2B{% endlatex %}/{% latex %}4B{% endlatex %})
		- 4B... **surrogates** (náhradníci): pro určité hodnoty prvních {% latex %}2B{% endlatex %} musí být přečteny druhé {% latex %}2B{% endlatex %}
			- výsledek se dohromady skládá magií
		- nelze přesně říct, kolik znaků je v souboru s tímhle kódováním uloženo
		- také varianty LE a BE
	- **UTF-8** -- {% latex %}1B{% endlatex %}, {% latex %}2B{% endlatex %}, {% latex %}3B{% endlatex %}, {% latex %}4B{% endlatex %} znaky
		- {% latex %}1B{% endlatex %}... první bit je {% latex %}0{% endlatex %}
		- {% latex %}nB{% endlatex %}... prvních {% latex %}n{% endlatex %} bitů je {% latex %}1{% endlatex %}, ten za tím {% latex %}0{% endlatex %} (pro {% latex %}n = 2{% endlatex %} je to {% latex %}110{% endlatex %})
			- každý další byt začíná 10 -- lehce lze zjistit, že jsou součástí nějakého znaku
		- neřeší se endianita -- jsou to prostě velká čísla
		- populární na internetu

##### Rasterizace
- string {% latex %}\mapsto{% endlatex %} bitmapa
- zajímavost: qwerty byla navržena tak, aby se na psacím stroji psalo pomalu (a klávesy se nezasekávaly)
- potřebujeme rozeznávat, kdy skočit na další řádek... každý systém to řeší jinak:
	- původně `CR` (carriage return) + `LF` (line feed) z psacích strojů
		- zachovalo se pro Windows
	- Unix si zvolil `LF`
	- Mac OS si zvolil `CR` (moderní ale už používají `LF`)
	- Unicode -- 2 nové znaky... `LS` (line separator) a `PS` (paragraph separator)
		- naprosto vůbec se to nechytlo, je v tom ještě větší guláš

##### V Pythonu
- `f.read("path" "r", encoding="enc")` -- nastavení encodingu
	- když to nespecifikujeme, tak to čte kódování typické pro daný OS
		- Windows -- 1520
		- Linux (asi) UTF-8
- `f.readline()` -- čte string (uloženo jako nějaká verze Unicode) až do konce řádku
- `strng.encode("enc")` -- string {% latex %}\mapsto{% endlatex %} bytes
- `bts.decode("enc")` -- bytes {% latex %}\mapsto{% endlatex %} string
- bytes je immutable -- je potřeba použít bytearray

### Dokončení rozdělané magie
- **bridge** -- řadič, který hostu zpřístupňuje jinou sběrnici
- **memory controller** -- middle man mezi pamětí a CPU
	- řeší refresh u DRAM
	- maskuje to, že máme 1GB a 512MB paměť -- linearizuje to pro CPU

#### Proximity sensor
- měří vzdálenost věci před senzorem
- je komplikované, má hodně senzorů -- jak si vybrat ten správný?
	- ten v příkladu používá {% latex %}8b{% endlatex %} adresový prostor
	- čtení je 1W (implicitní zápis do adresového registru) a 1W (vybraný registr), psaní je 1W a 1R

#### Systémová sběrnice
- PCIe (express)
	- sériová
	- jsou na tom všechna zařízení; na packet reagují jen ty, pro které je určený
	- 2 dedikované druhy packetů (memory write, memory read)
		- jen memory controller reaguje na tenhle packet
		- není tam adresa zařízení, ale paměti
	- příklad: 
		1. CPU pošle MRd (AMemory Read packet) 
			- cílová adresa je adresa paměti
			- musí tam být uložena i adresa procesoru, aby mohl přijít packet zpět
		2. memory controller vykoná požadavek, pošle CpID (Completion with data)
			- cílová adresa je adresa procesoru (aby to došlo správnému procesoru)

##### Memory/mapped I/O [[wiki](https://en.wikipedia.org/wiki/Memory-mapped_I/O)]
- princip používání stejného adresového prostoru jak pro paměť, tak pro I/O
	- pro I/O jsou mapovány nějaké části paměti, které jsou volné
	- je potřeba, aby adresy byly unikátní

##### Co dělat po startu?
- **CPU startup vector** -- odtud procesor začíná vykonávat instrukce
	- hardkódované v CPU (např. 0xFFFFFFF0)
		- bývá tam v paměti skok někam, kde se instrukcí vejde více
- **firmware ROM** -- paměť (non-volatile), kde je uložený program, který po startu dělá několik věcí:
	1. test a konfigurace HW
		- mapování (nekonfliktních) adres pro zařízení
	2. hledání užitečného softwaru (**bootování**)
		- další rom -- **option ROM**
			- mívaly starší systémy
			- bootuje instantně (je to ROM...)
			- princip cartrigových her -- instantní spuštění
			- bývá např. u grafických karet -- počáteční nastavení
		- **pevný disk** -- mívá boot sector, který je uzpůsobený k načtení do paměti a spuštění
			- je tu tzv. **bootloader** -- menší prográmek, který hledá na disku zbylá data
				- dnes většinou načítá **kernel** -- převezme zakladní funkce FS, načte zbytek OS...
	3. implementuje funkce pro bootování -- načti sektor, znak z klávesnice, vykresli něco...
