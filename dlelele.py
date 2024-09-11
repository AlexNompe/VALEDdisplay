players = 2
starting_bank = 75
step = 5
deposit = 5

player_banks = [starting_bank for i in range(players)]
player_points = [0 for i in range(players)]
player_actions = ["w" * i for i in range(players)]
bets = 0
stats = []

winner = -1
skip = False


def Статистика():
    global players
    global player_actions
    global player_banks
    global player_points
    global bets
    global step
    global deposit
    global stats
    stats = [f"{str(i + 1)}) {player_banks[i]} {player_points[i]}" for i in range(players)]

    for i in range(players):
        if player_banks[i] == 0 and player_points[i] == 0:
            print("Серия партий окончена! Спасибо за игру, выбирайте победителя")
            quit()

    print("Статистика:")
    print("\n".join(stats))
    print("")

    for i in range(players):
        print(f"Игрок {str(i + 1)}, возьмите или положите очки с банка ({player_banks[i]})")
        amount = input()
        if not "+" in amount:
            while not amount.isdigit():
                print("Ставка не имеет смысла")
                amount = input()
            amount = int(amount)
            while not (0 <= amount <= player_banks[i]):
                print("Нет возможности положить столько")
                amount = int(input())
            while not (amount % deposit == 0):
                print(f"Класть можно только колличество очков кратное {deposit}")
                amount = int(input())
            print(f"Взято {amount} очков из банка")
        else:
            while not amount.replace("+","").isdigit():
                print("Ставка не имеет смысла")
                amount = input()
            amount = -int(amount.replace("+",""))
            while not (amount == -deposit):
                print(f"Класть можно только по {deposit} очков за раз")
                amount = -int(input().replace("+",""))
            print(f"Положено {-amount} очков в банк")
        player_banks[i] -= amount
        player_points[i] += amount
        stats[i] += f" -> {player_banks[i]} {player_points[i]}"
        print("")
    print("Статистика:")
    print("\n".join(stats))
    print("")


def Раунд(string):
    global players
    global player_actions
    global player_banks
    global player_points
    global bets
    global step
    global stats
    global winner
    global skip
    print(f"{string}\n")
    for i in range(players):
        if not player_actions[i] == "пасс":
            player_actions[i] = f"{"w" * i}"
    actions = players
    i = 0
    while not player_actions.count("чек") + player_actions.count("пасс") == players:
        exit = False
        #print(player_actions)
        while (player_actions[(i % players)] == "пасс" or player_points[(i % players)] == 0) and player_points.count(
                0) != players:
            if i > players * 100 and player_actions[(i % players)] == "олын":
                break
            i += 1
        if players - player_actions.count("пасс") > 1 and players - player_actions.count("олын") > 0:
            print(f"Игрок {str((i % players) + 1)}, ваше действие?")
            player_actions[(i % players)] = input().replace(str(player_points[(i % players)]),"олын")
            while not (player_actions[(i % players)].isdigit() or player_actions[(i % players)] in ["олын", "чек",
                                                                                                    "пасс"]) or (
                    "олын" in player_actions and player_actions[(i % players)] not in ["олын", "пасс"]):
                print("Действие не имеет смысла")
                player_actions[(i % players)] = input()
            while player_actions[(i % players)].isdigit() and player_actions[
                ((i - 1 + players) % players)].isdigit() and int(player_actions[(i % players)]) < int(
                    player_actions[((i - 1 + players) % players)]):
                print(f"Вы не можете поставить меньше {player_actions[((i - 1 + players) % players)]}")
                player_actions[(i % players)] = input()

            if player_actions[(i % players)] != "пасс" and player_actions.count(player_actions[(i % players)]) != (
                    players - player_actions.count("пасс") - player_actions.count("")):
                actions += 3
            if player_actions[(i % players)].isdigit():
                action = int(player_actions[(i % players)])
                while not (0 < action <= player_points[(i % players)]):
                    print("Нет возможности поставить столько")
                    action = input()
                    exit = True
                    break
                if exit: continue
                while not (action % step == 0):
                    print(f"Ставить можно только колличество очков кратное {step}")
                    action = input()
                    exit = True
                    break
                if exit: continue
                action = int(action)
                print(f"Поставлено {action} очков")
                bets += action
                player_points[(i % players)] -= action
                stats[(i % players)] += f" -> {player_points[(i % players)]}"
            elif player_actions[(i % players)] == "олын":
                print("Поставлены все очки")
                bets += player_points[(i % players)]
                player_points[(i % players)] = 0
                stats[(i % players)] += f" -> олын"
            elif player_actions[(i % players)] == "чек":
                stats[(i % players)] += f" -> чек"
            elif player_actions[(i % players)] == "пасс":
                stats[(i % players)] += f" -> пасс"
            i += 1
            print("")
        elif players - player_actions.count("пасс") <= 1 and not player_actions[(i % players)] == "пасс" or player_points[(i % players)] == 0 and not player_actions.count("олын") > 1:
            print(f"Игрок {str((i % players) + 1)}, забирает ставки в размере {bets}\n")
            player_points[(i % players)] += bets
            bets = 0
            stats[(i % players)] += f" -> {player_points[(i % players)]}"
            skip = True
            break
        else:
            break
    print(f"Статистика:\n{bets}")
    print("\n".join(stats))
    print("")


while True:
    player_actions = ["w" * i for i in range(players)]
    bets = 0
    stats = []
    winner = -1
    skip = False

    Статистика()

    if not skip:
        Раунд("Префлоп")
        if ("олын" in player_actions or player_points.count(0) == players or players - player_actions.count("пасс") <= 1) and bets > 0:
            print("Вскрывайте свои карты")
            winner = int(input())
            print(f"Игрок {str(winner)}, забирает ставки в размере {bets}\n")
            player_points[winner-1] += bets
            bets = 0
            stats[winner-1] += f" -> {player_points[winner-1]}"
            continue
        else:
            if not skip: Раунд("Флоп")

    if not skip:
        if ("олын" in player_actions or player_points.count(0) == players or players - player_actions.count(
                "пасс") <= 1) and bets > 0:
            print("Вскрывайте свои карты")
            winner = int(input())
            print(f"Игрок {str(winner)}, забирает ставки в размере {bets}\n")
            player_points[winner - 1] += bets
            bets = 0
            stats[winner - 1] += f" -> {player_points[winner - 1]}"
            continue
        else:
            Раунд("4 карты")

    if not skip:
        if ("олын" in player_actions or player_points.count(0) == players or players - player_actions.count(
                "пасс") <= 1) and bets > 0:
            print("Вскрывайте свои карты")
            winner = int(input())
            print(f"Игрок {str(winner)}, забирает ставки в размере {bets}\n")
            player_points[winner - 1] += bets
            bets = 0
            stats[winner - 1] += f" -> {player_points[winner - 1]}"
            continue
        else:
            Раунд("5 карт")

    if not skip:
        print("Вскрывайте свои карты\n")
        winner = int(input())
        print(f"Игрок {str(winner)}, забирает ставки в размере {bets}\n")
        player_points[winner - 1] += bets
        bets = 0
        stats[winner - 1] += f" -> {player_points[winner - 1]}"
        continue
