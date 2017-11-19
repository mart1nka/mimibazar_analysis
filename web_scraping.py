import requests
import re
from bs4 import BeautifulSoup
import pandas
import json

def extract_recipe_info(recipe_table):
    header = recipe_table.find('h2')
    title = header.text
    link = header.find("a")["href"]
    
    header.decompose()
    
    category = recipe_table.previous_sibling.text.strip()
    
    # odstranime vsetok bordel od odkazu "ULOZIT" dalej
    save_link = recipe_table.find("a", string=re.compile("ULOŽIT"))
    after_save_link = list(save_link.next_siblings)
    for n in after_save_link:
        n.replace_with("")
    save_link.decompose()
    
    # zbavime sa "a" tagov
    for l in list(recipe_table.find_all("a")):
        l.decompose()
        
    # zbavime sa readmore triedy u dlhych receptov    
    for m in list(recipe_table.find_all(class_="readmore-postup")):
        m.decompose()
    
    # zamenime b za @@@, aby nam to pomohlo oddelit ingrediencie od postupu
    top_level_bold_section = list(recipe_table.find_all("b"))
    for b in top_level_bold_section:
        b.replace_with("@@@ " + b.text)
    
    # vytvorime si funkciu, ktora nam vyjme pozadovanu cast receptu pomocou regexu 
    # dotall ignoruje breaky, group 1 nadpis, strip nas zbavi prebytocnych znakov z HTML
    # ak je sekcia prazdna, vraciame None
    def extract_section(section_title, recipe_text):
        regexPattern = section_title + "(.*?)(@@@|$)"
        search = re.search(regexPattern, recipe_text, flags=re.DOTALL)
        if search:
            return search.group(1).strip()
        else:
            return None
     
    # zavolame pozadovany text pre regex
    ingredients = extract_section("POTŘEBNÉ PŘÍSADY", recipe_table.text)
    instructions = extract_section("POSTUP PŘÍPRAVY", recipe_table.text)

    # vrati nam slovnik
    return {
        "category": category,
        "title": title,
        "ingredients": ingredients,
        "instructions": instructions,
        "link": link
    }

#nacitame stranku, vrati nam obsah tabulky z mimibazaru ako zoznam slovnikov s polozkami receptu
def get_recipe_page(page_number):
    page = requests.get('https://www.mimibazar.cz/recepty.php?strana=' + str(page_number))
    soup = BeautifulSoup(page.text, 'html.parser')
    recipe_tables = soup.find_all(class_='recepty content t2')

    info_list = [extract_recipe_info(rt) for rt in recipe_tables]
    return info_list

#zadame pozadovane cisla stranok
all_recipes = []
for page_num in range(0, 13000):
    print(page_num)
    all_recipes += get_recipe_page(page_num)

#hladame len recepty, v ktorych su ingredience
recipes_w_ingredients = [r for r in all_recipes if r["ingredients"]]

with open('d:\\data\\data2.json', 'w') as fp:
    json.dump(recipes_w_ingredients, fp)

