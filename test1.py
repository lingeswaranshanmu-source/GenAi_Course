#dictionary operations

first = {"name": "ling", "place": "cbe"}

print(first["name"])   # prints: ling

first["thing"] = "batting"
print(first)

del first["place"]
print (first)

ebookdiscount = int(input("What is discount percentage? "))

if ebookdiscount == 90:
    print("You are so lucky")
elif ebookdiscount >= 50:
    print("Get more books at low prices today")
else:
    print("Limited discount, try again for more discount")

    #nestedif statements

