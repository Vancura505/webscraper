"""
Scraper_Vancura.py: WebScraper

author: Krystof Vancura
email: krystof2017@gmail.com
discord: ---------
"""

import requests
import bs4 as bs
import csv
import sys

def scrape(url, output_file):
    obce_data = {
        "cisla": [],
        "nazvy": [],
        "volici": [],
        "obalky": [],
        "valid_obalky": [],
        "hlasy_stran": []
    }
    nazvy_stran = set()

    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'html.parser')

    cisla_obci = [td.text for td in soup.find_all("td", class_="cislo")]
    nazvy_obci = [td.text for td in soup.find_all("td", class_="overflow_name")]

    obce_data["cisla"].extend(cisla_obci)
    obce_data["nazvy"].extend(nazvy_obci)

    for idx, cislo_obce in enumerate(cisla_obci):
        detail_url = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec={cislo_obce}&xvyber=7103"
        res = requests.get(detail_url)

        if res.status_code != 200:
            print(f"Chyba při načítání obce {cislo_obce}")
            obce_data["volici"].append("N/A")
            obce_data["obalky"].append("N/A")
            obce_data["valid_obalky"].append("N/A")
            obce_data["hlasy_stran"].append({})
            continue

        print(f"Zpracovávám obec {cislo_obce} ({idx+1}/{len(cisla_obci)})")
        soup_detail = bs.BeautifulSoup(res.text, 'html.parser')

        def extract_value(headers_id):
            td = soup_detail.find("td", class_="cislo", headers=headers_id)
            return td.text.replace('\xa0', ' ') if td else "N/A"

        obce_data["volici"].append(extract_value("sa2"))
        obce_data["obalky"].append(extract_value("sa5"))
        obce_data["valid_obalky"].append(extract_value("sa6"))

        nazvy_stran_obec = [td.text for td in soup_detail.find_all("td", class_="overflow_name", headers=["t1sa1 t1sb2", "t2sa1 t2sb2"])]
        hlasy_stran_obec = [td.text.replace('\xa0', ' ') for td in soup_detail.find_all("td", class_="cislo", headers=["t1sa2 t1sb3", "t2sa2 t2sb3"])]

        hlasovani = {}
        for i, strana in enumerate(nazvy_stran_obec):
            hlasy = hlasy_stran_obec[i] if i < len(hlasy_stran_obec) else "N/A"
            hlasovani[strana] = hlasy
            nazvy_stran.add(strana)

        obce_data["hlasy_stran"].append(hlasovani)

    hlavicky = ["Cislo Obce", "Nazev Obce", "Pocet Volicu", "Pocet Obalek", "Pocet Validnich Obalek"] + sorted(nazvy_stran)

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=hlavicky, restval="0")
            writer.writeheader()

            for i in range(len(obce_data["cisla"])):
                radek = {
                    "Cislo Obce": obce_data["cisla"][i],
                    "Nazev Obce": obce_data["nazvy"][i] if i < len(obce_data["nazvy"]) else "N/A",
                    "Pocet Volicu": obce_data["volici"][i],
                    "Pocet Obalek": obce_data["obalky"][i],
                    "Pocet Validnich Obalek": obce_data["valid_obalky"][i]
                }
                radek.update(obce_data["hlasy_stran"][i])
                writer.writerow(radek)

        print(f"\nData byla úspěšně uložena do souboru '{output_file}'")

    except Exception as e:
        print(f"\nChyba při zápisu do CSV: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Použití: python skript.py <URL> <vystup.csv>")
        sys.exit(1)

    vstupni_url = sys.argv[1]
    vystupni_soubor = sys.argv[2]

    if not vystupni_soubor.endswith(".csv"):
        vystupni_soubor += ".csv"

    scrape(vstupni_url, vystupni_soubor)
