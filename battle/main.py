import random
from classes.game import Person,bcolor
from classes.magic import Spell
from classes.inventory import Item


# Create black magics
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")


# Create white Magics
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")
curage = Spell("Curage", 50, 6000, "white")

# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenda = Item("Grenda", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, curage]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 5}, {"item": grenda, "quantity": 5}]
# Instantiate people
player1 = Person("vales", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Nick ", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Robot", 3089, 174, 288, 34, player_spells, player_items)

enemy1  = Person("Imp  ", 1250, 130, 560, 325, enemy_spells, [])
enemy2  = Person("Magus", 18200, 701, 525, 25, enemy_spells, [])
enemy3  = Person("Imp  ", 1250, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

num_of_players = len(players)
num_of_enemies = len(enemies)

running = True
i = 0

print( bcolor.FAIL + bcolor.BOLD + "AN ENEMY ATTACK!" + bcolor.ENDC)
while running:
    # Displaying state
    print("===============")

    print("\n\n")
    print("NAME                HP                                     MP        ")
    for player in players:
        player.get_stats()
    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    # Players Attack
    for player in players:
        print("\n\n")
        player.get_stats()
        print("\n")


        player.choose_action()
        choice = input("   choose Action:")
        index = int(choice) - 1

        # Normal Attack
        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)

            print("You attacked for " + str(dmg) + " points of damage to " + enemies[enemy].name)

        # Magic
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("   Choose Magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()
            if current_mp < spell.cost:
                print(bcolor.FAIL + "\nNOT enough MP\n" + bcolor.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolor.OKBLUE + "\n" + spell.name + " heals for " + str(magic_dmg) + " HP." + bcolor.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)

                print(bcolor.OKBLUE + "\n" + spell.name +" deals " + str(magic_dmg) + " Points of damage to "
                      + enemies[enemy].name + bcolor.ENDC)

        # Items
        elif index == 2:
            player.choose_item()
            item_choice = int(input("   Choose Item:")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player_items[item_choice]["quantity"] == 0:
                print(bcolor.FAIL + "\n" + item.name + " Non Left... " + bcolor.ENDC)
                continue

            player_items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolor.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) + " HP." + bcolor.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolor.OKGREEN + "\n" + item.name + "Fully restores HP/MP" + bcolor.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bcolor.FAIL + "\n" + item.name + " deals " + str(item.prop) + " points of damage to "+
                      enemies[enemy].name + bcolor.ENDC)

    # Check if Game is over and you Win
    defeated_enemy = 0
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemy += 1
            del enemies[enemies.index(enemy)]
            print("\n Remaining enemies", len(enemies))

    if defeated_enemy == num_of_enemies:
        print(bcolor.OKGREEN + "YOU WIN" + bcolor.ENDC)
        running = False
        break

    # Enemies Attack
    for enemy in enemies:
        target = random.randrange(0, len(players))
        while True:
            enemy_choice = random.randrange(0, 2)

            # Normal attack
            if enemy_choice == 0:
                enemy_dmg = enemy.generate_damage()
                players[target].take_damage(enemy_dmg)
                print("Enemy attacks for " + str(enemy_dmg) + " points of damage to " +
                      players[target].name)
                break
            # Magic Choice
            elif enemy_choice == 1:
                magic_choice = random.randrange(0, len(enemy.magic))

                spell = enemy.magic[magic_choice]
                current_mp = enemy.get_mp()
                if current_mp < spell.cost:
                    continue
                else:
                    magic_dmg = spell.generate_damage()
                    enemy.reduce_mp(spell.cost)

                    if spell.type == "white":
                        enemy.heal(magic_dmg)
                        print(bcolor.OKBLUE + "\n" + spell.name + " heals for " + enemy.name + str(magic_dmg) + " HP." + bcolor.ENDC)
                    elif spell.type == "black":
                        players[target].take_damage(magic_dmg)

                        print(bcolor.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg) + " Points of damage to "
                              + players[target].name + bcolor.ENDC)
                    break



    # Check if Game is over and you loose
    defeated_player = 0
    for player in players:
        if player.get_hp() == 0:
            defeated_player += 1
            del players[players.index(player)]
            print("\n Remaining players", len(players))

    if defeated_player == num_of_players:
        print(bcolor.FAIL + "Your enemies has DEFEATED YOU " + bcolor.ENDC)
        running = False