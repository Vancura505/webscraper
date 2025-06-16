Tento skript slouží ke stažení a uložení výsledků voleb z webu volby.cz
Načítá seznam obcí z hlavní výsledkové stránky zvoleného kraje.
Pro každou obec stahuje podrobné volební údaje:
Počet voličů
Počet vydaných obálek
Počet platných hlasů
Hlasy pro jednotlivé politické strany
Výsledná data ukládá do CSV souboru, kde každý řádek reprezentuje jednu obec a každý sloupec jednu proměnnou (včetně politických stran).
Výstupem je CSV soubor s kompletními daty.
Knihovny:
requests – pro stahování HTML obsahu z webových stránek.
bs4 – pro parsování a extrakci dat z HTML.
csv a sys – slouží k práci se soubory a argumenty v příkazové řádce.
