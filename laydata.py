from seleniumbase import SB
from bs4 import BeautifulSoup
stats = [
    "player",
    "nationality",
    "position",
    "team",
    "age",
    "birth_year",
    "games",
    "games_starts",
    "minutes",
    "goals",
    "assists"
]

with SB(uc=True) as sb:
    sb.open("https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats")
    
    sb.sleep(10)  # đảm bảo load xong

    html = sb.get_page_source()
   
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table", {"id": "stats_standard"})
    cauthus=table.select("tbody tr")
    for cauthu in cauthus:
        player={}
        for stat in stats:
            hang=cauthu.find("td",{"data-type":stat})
            if hang:
                player[stat]=hang.text.strip()
            else:
                player[stat]="N/A"
        print(player)
        
    input()