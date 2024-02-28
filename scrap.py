# https://www.fifaratings.com/players

# necessary libraries
from bs4 import BeautifulSoup
import requests
import csv




skill_name = ["ATT", "SKI", "MOV", "POW", "MEN", "DEF", "GK"] # the skills that we want to scrap
skills_stat = [] # to store the values that we scrap
name_list = [] # to store the names of the players
not_found = [] # to store the names of the players that are not found in the website
height = [] # to store the height of the players
weight = [] # to store the weight of the players




# reading the names from the csv file and store it in name_list
with open('names.csv', 'r') as file:    # the csv file that contains names is names.csv
    for line in file:
        name_list.append(line.strip())
    name_list.pop(0)
    k = 0
    for index in range(len(name_list)):
        name_list[index] = name_list[index].replace(f"{k},", "")
        name_list[index] = name_list[index].replace(" ", "-")
        k += 1





# scrapping the values from the website
for name in name_list:
    url = f"https://www.fifaratings.com/{name}"
    html_text = requests.get(url, headers={'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"}).text
    soup = BeautifulSoup(html_text, "lxml")

    players = soup.find_all("span", class_ = "mr-n1")
    temp = []
    for item in players:
        temp.append(item.text)

    if temp == []:
        not_found.append(name)
    else:
        skills_stat.append(temp)








# removing the uneccessary values from skills_stat
index_to_remove = [2 * i + 1 for i in range(8)]
for item in skills_stat:
    for index in sorted(index_to_remove, reverse=True):
        del item[index]
    del item[-1]   






# combining skill_name and skills_stat

data = []
columns = ["ATT", "SKI", "MOV", "POW", "MEN", "DEF", "GK"]
i, j = 0, 0
n, m = len(name_list), len(skills_stat)
while i < n and j < m:
    player = {}
    if name_list[i] in not_found:
        player["name"] = name_list[i]
        for column in columns:
            player[column] = '0'
        data.append(player)
        i += 1
    
    else:
        player["name"] = name_list[i]
        for index, column in enumerate(columns):
            player[column] = skills_stat[j][index]
        data.append(player)
        i += 1
        j += 1









# storing data in a csv file
csv_file = r'C:\Users\Badr Lakhal\Desktop\Baina python project\stats.csv'

fields = data[0].keys()

with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    
    writer.writeheader()

    for row in data:
        writer.writerow(row)
