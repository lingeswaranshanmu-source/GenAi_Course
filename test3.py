ling = int(input("Enter the free time per day: "))

if ling >= 10:
    freetime = input("Type 'study' or 'play': ").lower()  # user choice
    if freetime == "study":
        print("Focus on coding & building business")
    elif freetime == "play":
        print("Play cricket")
    else:
        print("Invalid choice, try again")
else:
    print("Not enough free time today, focus on essentials")