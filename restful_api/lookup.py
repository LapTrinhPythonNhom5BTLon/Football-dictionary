import argparse
import requests
from tabulate import tabulate
import csv

parser = argparse.ArgumentParser()
parser.add_argument("--name", type=str)
parser.add_argument("--club", type=str)
args = parser.parse_args()

local = "http://127.0.0.1:5000"

def get_data(tieu_chi, ten):
    url = ""
    target = ""
    if tieu_chi == "name":
        url += local + "/get-players/player?name=" + ten
        target = "cau thu"
    if tieu_chi == "club":
        url += local + "/get-teams/team?name=" + ten
        target = "doi bong"
    
    api_call = requests.get(url)
    
    if api_call.status_code == 200:
        data = api_call.json()
        if not data:
            print("Khong tim thay du lieu")
            return
        
        player_list = data.get(target, [])
        if not player_list:
            return
        
        print(tabulate(player_list, headers="keys", tablefmt="grid"))
        
        filename = f"{ten}.csv"
        with open(filename, "w", newline="", encoding="utf-8") as f:
            fieldnames = player_list[0].keys()
            write = csv.DictWriter(f, fieldnames=fieldnames)
            write.writeheader()
            write.writerows(player_list)
        
        
if args.name:
    get_data("name", args.name)
if args.club:
    get_data("club", args.club)