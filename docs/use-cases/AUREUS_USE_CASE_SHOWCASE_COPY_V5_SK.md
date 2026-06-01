# Aureus Use Case Showcase Copy V5 SK

Profesionálna slovenská verzia 12-stranového use-case showcase pre lokálnych klientov, účtovníkov a firmy.

## Strana 1 - Aureus Use Case Portfolio

**Podtitul:** Šesť príkladov kontrolovanej AI automatizácie pre firmy, ktoré potrebujú užitočnú prácu, ľudské schvaľovanie a dôkazový záznam.

Toto nie sú ukážky chatbotov.

Je to portfólio kontrolovaných AI pracovných systémov:

- opakovaná práca sa najprv zmapuje,
- AI pripraví ďalší užitočný krok,
- človek schváli citlivé rozhodnutia,
- systém uchová dôkazový záznam,
- firma dostane jasnejšie rozhodnutie, čo urobiť ďalej.

```text
AI pripraví. Ľudia schvália. Dôkaz zostáva.
```

**Use cases v tomto materiáli**

| Use case | Najlepšie použitie |
| --- | --- |
| Automation Audit | nájsť prvú užitočnú automatizáciu skôr, než sa začne stavať |
| n8n Workflow Review + Build | upratať existujúce alebo nové workflowy tak, aby sa dali bezpečne prevádzkovať |
| FinEcon Pocket / Bridge | kontrolovaný tok dokladov s Pocket vstupom, review a POHODA odovzdaním |
| Approval-Safe Sales Machine | AI-asistovaný predaj bez slepého odosielania správ |
| Aureus OS / AOP | riadenie AI práce cez scope, validáciu, schvaľovanie, dôkaz a handoff |
| Public Proof Website + Automation | prepojenie verejnej ponuky, intake a follow-up procesu |

## Strana 2 - Ako vyberáme správny AI use case

Dobrý AI use case nezačína modelom. Začína procesom.

Aureus hľadá procesy s piatimi signálmi:

- **opakovaná práca** - úloha sa deje dosť často na to, aby dávalo zmysel vytvoriť systém,
- **úzke miesto v odbornosti** - ľudia míňajú odborný čas na triedenie, kontrolu alebo prepisovanie,
- **nejasné vlastníctvo / citlivé rozhodnutie** - ďalší krok je dôležitý a potrebuje review,
- **proces pripravený na dôkaz** - workflow vie uchovať záznam, čo sa stalo,
- **ohraničený pilot** - prvá verzia sa dá bezpečne otestovať pred škálovaním.

**Discovery flow**

```text
Objaviť -> Ohodnotiť -> Navrhnúť -> Postaviť -> Skontrolovať -> Škálovať
```

Cieľ nie je automatizovať všetko. Cieľ je nájsť prvý kontrolovaný workflow, ktorý vytvorí viditeľnú hodnotu a dá sa skontrolovať.

## Strana 3 - Automation Audit

**Prísľub v jednej vete:** Nájsť prvú užitočnú AI automatizáciu predtým, než sa minú peniaze na stavbu.

**Problém klienta**

Firma vie, že práca je manuálna a chaotická, ale nevie, čo automatizovať ako prvé. Existujú nápady, nástroje aj bolesti, ale chýba bezpečné poradie.

**Čo pripraví AI**

AI pomáha zhrnúť poznámky z procesu, zoskupiť opakovanú prácu, nájsť úzke miesta, pripraviť kandidátov na automatizáciu a navrhnúť mapu impact / effort.

**Čo schvaľujú ľudia**

Majiteľ alebo zodpovedná osoba potvrdí, ktorý proces je dôležitý, ktoré akcie sú citlivé, čo musí zostať manuálne a čo môže patriť do prvého bezpečného pilotu.

**Aký dôkaz zostáva**

Mapa procesu, zoznam kandidátov na automatizáciu, tabuľka schvaľovacích hraníc, zoznam rizík, pilot brief a odporúčanie ďalšieho kroku.

**Kontrolovaný workflow**

```text
intake -> mapa procesu -> kandidáti -> impact/effort skóre -> schvaľovacia hranica -> pilot brief
```

**Čo dostane klient**

- mapu procesu,
- zoradené možnosti automatizácie,
- hranice review a rizík,
- odporúčanie prvého pilotu,
- rozhodnutie, čo stavať ďalej.

**Proof status:** Verejne bezpečný koncept; odporúčaný prvý nákup; pripravené na pilot.

**Hranice**

Netvrdíme, že každý proces sa má automatizovať. Nesľubujeme ROI. Samotný audit nie je tvrdenie o produkčnom nasadení.

**Najlepší prvý krok**

Pošlite jeden opakovaný proces, ktorý míňa čas alebo vytvára chyby.

## Strana 4 - n8n Workflow Review + Build

**Prísľub v jednej vete:** Zmeniť krehké automatizácie na reviewovateľné systémy, ktoré tím vie prevádzkovať.

**Problém klienta**

Workflow možno beží, ale tím nevie vysvetliť failure paths, vlastníctvo, credentialy, retry logiku, live akcie alebo handoff. Taká automatizácia sa ťažko dôveruje.

**Čo pripraví AI**

AI pomáha prečítať zámer workflowu, zhrnúť logiku, pripraviť dokumentáciu, nájsť slabé hranice, pripraviť validačný checklist a navrhnúť bezpečnejšiu štruktúru.

**Čo schvaľujú ľudia**

Majiteľ schvaľuje credential handling, live aktiváciu, externé odosielanie, produkčné zmeny, retry správanie a postup pri zlyhaní.

**Aký dôkaz zostáva**

Risk scan, mapa workflowu, poznámky k failure paths, validačný checklist, schvaľovacia hranica a handoff note.

**Kontrolovaný workflow**

```text
trigger -> input contract -> AI-asistovaný krok -> validácia -> schválenie -> dôkazová poznámka -> handoff
```

**Čo dostane klient**

- review poznámky,
- mapu zlyhaní a vlastníctva,
- validačný plán,
- smer opravy alebo bezpečnej stavby,
- handoff dokumentáciu.

**Proof status:** Verejne bezpečný koncept; setup-gated; pripravené na pilot.

**Hranice**

Bez explicitného schválenia sa nerobí live aktivácia, zmena credentialov, externé odoslanie ani produkčná akcia.

**Najlepší prvý krok**

Pošlite sanitizovaný opis workflowu a zlyhanie, ktorého sa najviac obávate.

## Strana 5 - FinEcon Pocket / Bridge

**Prísľub v jednej vete:** Presunúť doklady od vstupu po kontrolované odovzdanie s dôkazom, pričom účtovnícke potvrdenie zostáva zachované.

**Problém klienta**

Faktúry, bločky a doklady prichádzajú rôznymi kanálmi. Kontext sa stráca, review je nejasné a odovzdanie do účtovného systému sa ťažko kontroluje.

**Čo pripraví AI**

AI môže vytiahnuť kandidátske polia, klasifikovať typ dokladu, zhrnúť kontext, označiť chýbajúce údaje, pripraviť review poznámky a pripraviť dáta pre downstream handoff.

**Čo schvaľujú ľudia**

Ľudia kontrolujú neisté polia, účtovne citlivý výklad, výnimky, pripravenosť Bridge vrstvy, POHODA odovzdanie a všetko, čo ovplyvňuje oficiálne záznamy.

**Aký dôkaz zostáva**

Stav dokladu, review rozhodnutie, bridge readiness poznámka, proof pack, zoznam výnimiek, writeback smer a checklist pre účtovnícke potvrdenie.

**Kontrolovaný workflow**

```text
Pocket vstup / pripravený priečinok
-> sledovanie stavu
-> review action
-> bridge start
-> POHODA preflight
-> kontrolované odovzdanie
-> post-import writeback
-> proof pack
-> hranica účtovníckeho potvrdenia
```

**Čo dostane klient**

- cestu vstupu dokladov,
- smer review queue,
- POHODA handoff model,
- proof pack smer,
- zoznam výnimiek,
- checklist pre účtovníka.

**Proof status:** Interné E2E prešlo; účtovnícke potvrdenie čaká; setup-gated; pripravené na pilot.

**Source-backed fakty**

Source-backed FinEcon stack obsahuje 19 workflow exportov. Pocket vrstva obsahuje:

- FinEcon 13 - Pocket Document Intake,
- FinEcon 14 - Pocket Status API,
- FinEcon 15 - Pocket Review Action,
- FinEcon 16 - Pocket Bridge Start,
- FinEcon 17 - Pocket Company Registration.

Bridge vrstva obsahuje:

- FinEcon 09 - Bridge Review to POHODA,
- FinEcon 10 - Bridge Preflight & Runtime Readiness,
- FinEcon 11 - Bridge Live Import,
- FinEcon 12 - Bridge Post-Import Writeback & Proof Pack.

Dôkazová vrstva obsahuje:

- FinEcon 19 - Proof Pack Drive Publisher.

Interný status hovorí, že Core E2E prešiel, FinEcon Pocket to POHODA prešiel a POHODA live import prešiel cez tri nakonfigurované mServer prostredia. Účtovnícka správnosť a cleanup zostávajú pending accountant validation.

**Hranice**

FinEcon nie je účtovná autorita. Nenahrádza účtovníka, neposkytuje daňové ani právne poradenstvo a netvrdí účtovnícku správnosť pred odborným potvrdením.

**Najlepší prvý krok**

Vyberte jeden tok dokladov a určite, čo musí človek alebo účtovník schváliť pred downstream použitím.

## Strana 6 - Approval-Safe Sales Machine

**Prísľub v jednej vete:** Použiť AI na prípravu predajnej práce bez slepého odosielania outreach správ.

**Problém klienta**

Lead sa raz preskúma a potom follow-up závisí od pamäte. Správy sú nekonzistentné, claimy môžu byť rizikové a nie je jasné, ktorý lead potrebuje review.

**Čo pripraví AI**

AI môže urobiť research verejného kontextu, klasifikovať lead fit, pripraviť outreach, follow-up, reply classification a booking / next-step note.

**Čo schvaľujú ľudia**

Ľudia schvaľujú claimy, externé správy, citlivú personalizáciu, do-not-contact rozhodnutia a samotné odoslanie.

**Aký dôkaz zostáva**

Lead state, qualification note, draft správa, approval status, reply classification, follow-up plán a daily report.

**Kontrolovaný workflow**

```text
lead source -> discovery -> qualification -> draft outreach -> manuálne schválenie -> follow-up draft -> reply classification -> booking draft -> daily report -> audit log
```

**Čo dostane klient**

- bezpečný lead state model,
- workflow schvaľovaných správ,
- smer reply handlingu,
- do-not-contact hranicu,
- reporting štruktúru.

**Proof status:** Verejne bezpečný koncept; setup-gated; pripravené na pilot.

**Hranice**

Žiadny blind outreach. Žiadne odoslanie bez schválenia. Žiadne generovanie nepodložených tvrdení.

**Najlepší prvý krok**

Začnite jedným lead source a jednou schválenou offer message.

## Strana 7 - Aureus OS / AOP

**Prísľub v jednej vete:** Riadiť AI-asistovanú prácu cez scope, validáciu, schválenia, dôkaz a handoff.

**Problém klienta**

Tímy používajú AI v chatoch, dokumentoch, úlohách, automatizáciách a Gite, ale práca sa rozpadá. Chýba jasná misia, vlastník, schvaľovacia hranica a dôkazový záznam.

**Čo pripraví AI**

AI môže pomáhať plánovať, robiť research, draftovať, kontrolovať, sumarizovať, validovať a pripraviť handoff artefakty.

**Čo schvaľujú ľudia**

Ľudia schvaľujú scope, citlivé akcie, verejné tvrdenia, produkčné zmeny, externé správy, finančné handoffy a klientsky viditeľné výstupy.

**Aký dôkaz zostáva**

Mission brief, zdrojové referencie, validačné poznámky, approval decisions, change summary, risk list a handoff.

**Kontrolovaný workflow**

```text
misia -> scope a obmedzenia -> AI-asistovaná práca -> validácia -> action gate -> dôkaz -> handoff
```

**Čo dostane klient**

- operating model pre AI prácu,
- review a approval gates,
- formát dôkazu,
- handoff disciplínu,
- odporúčanie prvého operating area.

**Proof status:** Verejne bezpečný koncept; setup-gated; pripravené na pilot pre tímy, ktoré potrebujú cross-team control.

**Hranice**

Aureus OS je interná operating vrstva a AOP je interný control engine. Väčšinou sa nepredáva ako prvý abstraktný produkt. Klient typicky začína auditom, workflow buildom alebo pilotom a AI Operating System Setup dáva zmysel až pri potrebe riadiť viac tímov alebo procesov.

**Najlepší prvý krok**

Pomenujte jednu oblasť, kde má AI pomôcť, ale nemá byť finálnou autoritou.

## Strana 8 - Public Proof Website + Automation

**Prísľub v jednej vete:** Prepojiť verejnú ponuku s proof-safe webom a operatívnym intake flow.

**Problém klienta**

Ponuka existuje v hlave foundera, ale web ju nevysvetľuje jasne a nespúšťa ďalší operatívny krok.

**Čo pripraví AI**

AI môže pripraviť offer copy, štruktúru stránok, intake otázky, zhrnúť buyer context a pripraviť follow-up alebo proposal materiály.

**Čo schvaľujú ľudia**

Majiteľ schvaľuje claimy, pricing, vizuály, verejné stránky, publikovanie, routing leadov a externé správy.

**Aký dôkaz zostáva**

Public claim register, page map, offer menu, intake record, handoff note a follow-up path.

**Kontrolovaný workflow**

```text
offer clarity -> verejná stránka -> intake form -> review -> follow-up draft -> handoff -> proof-safe updates
```

**Čo dostane klient**

- proof-safe štruktúru ponuky,
- smer web copy,
- intake path,
- follow-up workflow,
- checklist verejných hraníc.

**Proof status:** Verejne bezpečný koncept; setup-gated; pripravené na pilot.

**Hranice**

Žiadny fake proof. Žiadne nepodložené tvrdenia. Žiadne verejné publikovanie bez schválenia vlastníkom.

**Najlepší prvý krok**

Pošlite ponuku, cieľového kupujúceho a jednu otázku, ktorú musí web zodpovedať.

## Strana 9 - Client Use-Case Scorecard

Tento scorecard slúži na výber prvého pilotu.

| Use case | Viditeľná hodnota | Ohraničené úsilie | Citlivosť review | Proof readiness | First-pilot fit | Najlepší vstup |
| --- | --- | --- | --- | --- | --- | --- |
| Automation Audit | Vysoká | Nízke | Nízka | Vysoká | Vysoká | prvý nákup |
| n8n Workflow Review + Build | Vysoká | Stredné | Stredná | Vysoká | Vysoká | existujúci workflow |
| FinEcon Pocket / Bridge | Vysoká | Stredné | Vysoká | Stredná | Vysoká | tok dokladov |
| Approval-Safe Sales Machine | Stredná | Stredné | Vysoká | Vysoká | Stredná | lead follow-up |
| Aureus OS / AOP | Vysoká | Vysoké | Vysoká | Vysoká | Stredná | team control model |
| Public Proof Website + Automation | Stredná | Stredné | Stredná | Vysoká | Vysoká | offer clarity |

**Odporúčanie**

- Prvý nákup: Automation Audit.
- Najrýchlejší technický dôkaz: n8n Workflow Review.
- Najsilnejší finance fit: FinEcon Pilot.
- Najsilnejší operating model: Aureus OS Setup.
- Najlepší verejný asset: Public Proof Website + Automation.

## Strana 10 - 30-dňový klientsky pilot

Cieľ nie je automatizovať všetko za 30 dní. Cieľ je dokázať jeden kontrolovaný workflow, ktorý klient chápe, schvaľuje a vie skontrolovať.

| Týždeň | Fokus | Výstup |
| --- | --- | --- |
| Týždeň 1 | Discovery a mapa procesu | Reálny proces, vlastníci, vstupy, výnimky a rizikové body sú viditeľné. |
| Týždeň 2 | Návrh pilotu a schvaľovacia hranica | Bezpečný scope pilotu, rola AI, approval points a acceptance criteria sú definované. |
| Týždeň 3 | Build / test kontrolovaného dôkazu | Kontrolovaný workflow alebo proof surface sa otestuje na syntetických alebo schválených príkladoch. |
| Týždeň 4 | Review, handoff, ďalšie rozhodnutie | Klient dostane dôkaz, rizikové poznámky, handoff a jasné rozhodnutie o ďalšej fáze. |

**Do 30. dňa klient dostane**

- mapu procesu,
- pilot spec,
- schvaľovaciu hranicu,
- príklad dôkazu,
- risk list,
- ďalšie rozhodnutie.

## Strana 11 - Ako používať tento showcase

Tento showcase sa dá použiť ako:

- podklad na prvý sales call,
- follow-up PDF,
- LinkedIn carousel,
- GitHub portfolio proof layer,
- príloha k návrhu spolupráce,
- sales follow-up materiál.

**Bezpečnostné pravidlá**

- žiadne private exporty,
- žiadny fake proof,
- žiadne tvrdenie o účtovnej autorite,
- žiadna slepá automatizácia,
- žiadne verejné claimy bez schválenia,
- žiadne customer-results tvrdenia bez samostatného dôkazu.

## Strana 12 - Najlepší prvý krok

Začnite s **Automation Audit**.

Je to najbezpečnejší prvý nákup, pretože nájde prvý užitočný workflow predtým, než sa začne stavať.

Potom vyberieme ďalšiu cestu:

| Ak proces súvisí s... | Ďalšia cesta |
| --- | --- |
| faktúrami, dokladmi, financiami alebo POHODA realitou | FinEcon Pilot |
| existujúcou automatizáciou alebo workflow riskom | n8n Workflow Review + Build |
| lead follow-up alebo sales operations | Approval-Safe Sales Machine |
| AI prácou roztrúsenou naprieč tímom | Aureus OS Setup |
| nejasnou verejnou ponukou alebo slabým webom | Public Proof Website + Automation |

Vždy držíme dve kontroly:

```text
schvaľovacia hranica + dôkazový záznam
```

**Akcia pre kupujúceho**

Pošlite jeden workflow, tok dokladov alebo opakovaný proces, ktorý chcete skontrolovať.
