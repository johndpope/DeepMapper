output = "<body>"

with open("./img.txt", "r") as fp:
    file = fp.read().split("\n")
    fp.close()

for line in file:
    line = line.strip().split("\t")
    if len(line) < 3:
        continue
    print(line)
    output += f"<img src='https://app.snapchat.com/web/deeplink/snapcode?username={line[0]}&type=PNG&size=240'></img><img src='{line[2]}'> - {line[0]} - </img>"

output += "</body>"

with open("./imgs.html", "w") as fp:
    fp.write(output)
    fp.close()