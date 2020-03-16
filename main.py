import  random
from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
print("\n\n")
#print("Name                             HP                              MP")
print("\n\n")



# Create Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 18, 1500, "white")
curaga = Spell("Curaga", 50, 5500, "white")

# Create some Item
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("HI-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer","Fully restores HP/MP of one party member",9999)
hielixer = Item("MeghElixer", "elixer","Fully restores party's HP/MP",9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

#Items
player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spell = [fire, meteor , cure ]
player_items = [{"item": potion,"quantity": 15},{"item": hipotion,"quantity": 5},
                {"item": superpotion,"quantity": 5},{"item": elixer,"quantity": 5},
                {"item": hielixer,"quantity": 2}, {"item": grenade,"quantity": 5}]


# Instantiate People
player1 = Person("Hulk   : ", 3472, 145, 300, 34, player_spells, player_items)
player2 = Person("Thor   : ", 4672, 134, 321, 34, player_spells, player_items)
player3 = Person("Ironman: ", 3123, 210, 153, 34, player_spells, player_items)

enemy1 = Person("Loki  :",2031, 130 , 534, 325, enemy_spell, [])
enemy2 = Person("Thanos:",12602, 684 , 632, 25, enemy_spell, [])
enemy3 = Person("Ultron:",2031, 130 , 534, 325, enemy_spell, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + "RPG Bettle Game !" + bcolors.ENDC)

while running:
    print ("====================")
    print("\n\n")
    print("  Name                        HP                                MP")
    for player in players:

        player.get_stats()
    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("    Choose Actions: ")
        index = int(choice) - 1
        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print ("You attacked  "+ enemies[enemy].name.replace(" ", "") + " for ", dmg, " point of damage")
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("  Choose Magic:")) - 1
            if magic_choice == -1 :
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\n Not enough MP \n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for ", str(magic_dmg), " HP." + bcolors.ENDC + "\n")
            elif spell.type == "black":

                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals for ", str(magic_dmg), " points of damage " + enemies[enemy].name.replace(" ", "")  + bcolors.ENDC + "\n")
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + "has died.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("   Choose Item"))- 1
            if item_choice == -1:
                continue
            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + "heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp

                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP " + bcolors.ENDC)
            elif item.type == "attack":

                enemy =   player.choose_target(enemies)

                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals ", str(item.prop), " points of damage "+ enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + "has died.")
                    del enemies[enemy]

  # check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1


    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
        running = False

    elif defeated_players == 2:
            print(bcolors.FAIL + "You Lose!" + bcolors.ENDC)
            running = False
    print("\n")

    for enemy in enemies:
        enemy_choice = random.randrange(0, 3)


        if enemy_choice == 0:
            target = random.randrange(0, 3)
            enemy_dmg = enemies[0].generate_damage()

            players[target].take_damage(enemy_dmg)
            print (enemy.name.replace(" ", "") +  " attackts" + players[target].name.replace(" ", "") + " for", enemy_dmg, " Player HP", player.get_hp())



        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE +  spell.name + " heals " + enemy.name + "for" + str(magic_dmg), "HP" + bcolors.ENDC)

            elif spell.type == "black":
                target = random.randrange(0, 3)


                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + " heals for" + str(magic_dmg), "point of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)
                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + "has died.")
                    del players[player]
