from collections import defaultdict
"""
    Was used to keep track of what was the last upgrade path
    Until it was finished when I realized that I couldn't use it..
"""
def upgradeDiff(instructions):
    uppdelade_upgrades_per_apa = defaultdict(dict)
    # delar upp alla upgraderingar för sig per apa
    for idx, instruction in enumerate(instructions):
        if instruction["UPGRADE"] != "-":
            if len(uppdelade_upgrades_per_apa[instruction["MONKEY"]]) > 0:
                uppdelade_upgrades_per_apa[instruction["MONKEY"]].append(instruction["UPGRADE"])
                
            else: 
                uppdelade_upgrades_per_apa[instruction["MONKEY"]] = [ instruction["UPGRADE"] ]

    # För varje upgrade per apa
    for monkey_upgrade in uppdelade_upgrades_per_apa.values():
        if len(monkey_upgrade) > 1: # Hoppa ifall det bara är en upgrade på den apan
            for index in range(len(monkey_upgrade)): # ifall index av listan är 0 hoppa
                if index != 0:
                    # Senaste och nuvarande uppgradeing splitar ut alla -
                    last_upgrade = monkey_upgrade[index -1].split("-")
                    upgrade = monkey_upgrade[index].split("-")

                    # mappar om str till int i upgrade listorna
                    top_last, middle_last, bottom_last = tuple(map(int, last_upgrade))
                    top, middle, bottom = tuple(map(int, upgrade))

                    # Hittar diffen mellan förra uppgradering och nuvarande uppgraderingen
                    diff = "{}-{}-{}".format(abs(top-top_last), abs(middle-middle_last), abs(bottom-bottom_last))
                    
                    print(last_upgrade, upgrade, diff)
                    
                    # Ändrar monkey_upgrade
                    monkey_upgrade[index] = diff