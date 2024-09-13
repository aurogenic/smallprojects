import math
from random import random

config = { "assistance": True, "hardcore": True }
attemptsDict ={ 1: 2, 2:6,  3:14, 4:30,  5:62 }
limitsDict ={ 1: 4, 2:17,  3:72, 4:334,  5:1613 }

def main():
    print("welcome to Numberando:) ")
    while(True):
        print("Enter '/help' for more info")
        print("Enter '/settings' to change settings")
        print("Enter '/start' to start the game")
        print("Enter '/quit' to change quit")
        a1 = input("command -> : ")
        match(a1.lower()):
            case '/start': start()
            case '/help': help()
            case '/settings': settings()
            case '/quit': break
            case default: print("enter valid command")
    print("Thankyou for playing, see you soon")

def start():
    print("")
    attempts = 0
    level = getNumber(text="Enter level (max-number of digits for the number)",  max=5)
    maxAttempts = attemptsDict[level]
    history = []
    top = 10 ** level
    limit = limitsDict[level] if config['hardcore'] else top
    x = int(random() * top)
    # print("hidden number is", x)
    score = 0
    progress = 0
    while(attempts < maxAttempts):
        print("Attempts Remaining: ", maxAttempts-attempts, "\n")
        query = getNumber("enter query number", max=limit)
        attempts += 1
        reminder = x%query
        history.append([query, reminder])
        if(reminder == 0):
            print("The Number is Divisible by", query)
        elif(config["assistance"]):
            print("Dividing the number by", query, "gives the reminder", reminder)
        else:
            print("The Number is not Divisible By",  query)
        answer = getNumber(max=top)
        for q, r in history:
            if answer%q == r:
                progress += 1
        if answer == x:
            print("\nBravooo :D", answer ,"is the right answer: ")
            score += (maxAttempts * 10 / attempts)
            score = int(score *500 / 620)
            
            break
        else:
            print("Wrong answer")

    if(attempts >= maxAttempts):
        print("\nGame-Over :(")
        print("the number is", x, "\n")
    score += int( score*progress / (attempts * (attempts+1) /2))
    if(config["assistance"]):
        score = int(score/ (7-level))
    if(config["hardcore"]):
        score = score * (level+1)
    print("your Score:  ", score)
    print("")

def getNumber(text="Enter Your Answer", min=1, max=100000):
    while(True):
        try:
            response = int(input(text + " (" + str(min) + "~" + str(max) + ") :").strip())
            if min <= response <= max:
                break
            else:
                print('value should be between', min ,'and', max)

        except EOFError:
            response = 0
            break

        except ValueError:
            print("enter valid Integer")

    return response

def settings():
    print("settings:")
    while(True):
        print("assistance:",  config["assistance"], "use '/assistance' to change")
        print("hardcore:", config["hardcore"],  "use '/hardcore to change")
        print("enter '/confirm' to save changes")
        a3 = input("command -> ").strip().lower()
        match(a3):
            case "/assistance": assist()
            case "/hardcore": hardcore()
            case "/confirm": break

def assist():
    global config
    while(True):
        a2 = input("assitance:\ndo you want reminders in each query(yes/no) : ").strip().lower()
        match(a2):
            case "no": config["assistance"] = False
            case "yes": config["assistance"] = True
            case default: continue
        break

def hardcore():
    global config
    while(True):
        a2 = input("hardcore:\ndo you want to enable hardcore mode (yes/no) : ")
        match(a2):
                case "no": config["hardcore"] = False
                case "yes": config["hardcore"] = True
                case default: continue
        break

def help():
    print(helpString)

helpString = """
Welcome to Numberando!

Numberando is a fun number-guessing game where you try to guess a randomly generated number.

Commands:
- '/help': Displays this help message.
- '/settings': Allows you to change game settings.
- '/start': Starts the game.
- '/quit': Quits the game.

Gameplay:
- You are supposed to guess a hidden number
- You will be prompted to enter a query number to check if the hidden number is divisible by the query number(you can also get reminders in assisatance mode)
- Try to guess the correct number within the given number of attempts to earn the highest score.

Settings:
- Assistance: Enable or disable assistance to get reminders during the game.
- Hardcore Mode: when enabled limits the query number to make the game harder


Have fun playing Numberando!
"""

if __name__== "__main__":
    main()