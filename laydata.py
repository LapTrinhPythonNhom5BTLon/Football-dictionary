from seleniumbase import SB
from bs4 import BeautifulSoup
import re
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
    "assists",

    "goals_assists_pens_per90",
    "goals_pens_per90",
    "goals_assists_per90",
    "assists_per90",
    "goals_per90",
    "cards_red",
    "cards_yellow",
    "pens_att",
    "pens_made",
    "goals_pens",
    "goals_assists",
    "minutes_90s"
]
def fixmin(s):
    if "," in s:
        return s.replace(",","")
    return s
def get_players():
    ans=[]
    with SB(uc=True) as sb:
        sb.open("https://fbref.com/en/comps/9/2024-2025/stats/2024-2025-Premier-League-Stats")
        
        sb.sleep(20)  # đảm bảo load xong

        html = sb.get_page_source()
        #html = re.sub(r"<!--|-->", "", html)

        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", {"id": "stats_standard"})
        cauthus=table.select("tbody tr")

        for cauthu in cauthus:
            player={}
            for stat in stats:
                hang=cauthu.find("td",{"data-stat":stat})
                if hang:
                    for icon in hang.find_all("span",class_=lambda x:x and "f-" in x):
                        icon.decompose()  
                    player[stat]=hang.text.strip()
                else:
                    player[stat]="N/A"
            if player["minutes"] != "N/A" and int(fixmin(player["minutes"]))>90:
                ans.append(player)
    return ans