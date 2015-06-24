"""
Small script to retrieve all humblebundle games purchased and add metadata from metacritic
Generates an .html file as output
"""

__author__ = "Dean Oemcke"

import humblebundle

from metacriticScraper import *
from htmltable import *


humble_email = "your@humble.email"
humble_pass = "yourhumblepass"


class Humble_game(object):
    def __init__(self, human_name, machine_name, bundle_name, purchase_type, icon, url):
        self.human_name = human_name
        self.machine_name = machine_name
        self.bundle_name = bundle_name
        self.purchase_type = purchase_type
        self.icon = icon
        self.url = url


def get_game_header_for_print():
    fields = [
        "Icon",
        "Game",
        "Bundle",
        "Type",
        "Link",
        "MC Title",
        "Platform",
        "# Players",
        "Genre",
        "Metascore",
        "Metascore desc",
        "Metascore reviews",
        "Userscore",
        "Userscore desc",
        "Userscore reviews",
        "Summary",
        "Release Date",
        "Rating",
        "Developer",
        "Publisher",
        "Publisher Link",
        "Official Site",
        "Game Link",
    ]
    return fields

def get_game_detail_for_print(hb, mc):
    hb_fields = [
        hb.icon, hb.human_name, hb.bundle_name, hb.purchase_type, hb.url,
    ]
    if metacritic_model:
        metacritic_fields = [
            mc.title,
            mc.system,
            mc.num_players,
            mc.genres,
            mc.metascore,
            mc.metascore_desc,
            mc.metascore_count,
            mc.user_score,
            mc.user_score_desc,
            mc.user_count,
            mc.summary,
            mc.release_date,
            mc.esrb,
            mc.developer,
            mc.publisher,
            mc.publisher_link,
            mc.official_site,
            mc.link,
            mc.id,
        ]
    else:
        metacritic_fields = ["-"] * 19

    return hb_fields + metacritic_fields

def calculate_purchase_type(machine_name):
    if "_soundtrack" in machine_name:
        return 'soundtrack'
    elif "_android" in machine_name:
        return 'mobile'
    else:
        return 'pc'

def fetch_humble_gameslist():
    client = humblebundle.HumbleApi()
    client.login(humble_email, humble_pass)
    order_list = client.order_list()
    games_list = []

    for order in order_list:
        if not order.subproducts:
            humble_model = Humble_game(
                order.product.human_name,
                order.product.machine_name,
                order.product.human_name,
                calculate_purchase_type(order.product.machine_name),
                "",
                ""
            )
            games_list.append(humble_model)
        else:
            for game in order.subproducts:
                humble_model = Humble_game(
                    game.human_name,
                    game.machine_name,
                    order.product.human_name,
                    calculate_purchase_type(game.machine_name),
                    game.icon,
                    game.url
                )
                games_list.append(humble_model)

    return games_list

def fetch_metacritic_info(game):
    try:
        results = mc.search(game.human_name, "game")
        match = False
        game_id = False
        metacritic_model = False

        #find first match that has a metascore (regardless of platform)
        #if no metascore then just use first result
        if len(results) > 0:
            for result in results:
                if result.metascore and not match:
                    match = result
            if not match:
                match = results[0]
            game_id = match.id

        #once we have a game id look it up in metacritc
        if game_id:
            metacritic_model = mc.get_info(game_id)

    except:
        print 'error scraping info for: ', game.human_name

    return metacritic_model



#fetch gamelist from humble bundle
gamelist = fetch_humble_gameslist()

#open an html file for writing and populate with header
output = open('gamelist.html', 'w')
output.truncate()
headerItems = get_game_header_for_print()
print headerItems
output.write(generate_table_header(headerItems))

#fetch metadata for each game from metacritic and write out to file as we go
mc = Metacritic()
for game in gamelist:

    print game.human_name, "..."
    if game.purchase_type == 'soundtrack':
        metacritic_model = False
    else:
        metacritic_model = fetch_metacritic_info(game)

    #print out game to file
    game.url = "<a href='" + game.url + "'>" + game.url + "</a>"
    game.icon = "<img src='" + game.icon + "' />"
    detailItems = get_game_detail_for_print(game, metacritic_model)
    #print detailItems
    output.write(generate_table_row(detailItems))

#print out html footer
output.write(generate_table_footer())
output.close()

