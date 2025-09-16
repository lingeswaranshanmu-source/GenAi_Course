ebookdiscounttoday = int(input("What is discount percentage? "))

if ebookdiscounttoday >= 30:
    print("Buy more books today")

    decision = input("Type 'order' or 'prebook': ").lower()  # user chooses

    if decision == "order":
        print("Happily order today")
    elif decision == "prebook":
        print("Prebook for any upcoming releases")
    else:
        print("choose either order or preorder")
else:
    print("Discount too low, not worth buying now")


