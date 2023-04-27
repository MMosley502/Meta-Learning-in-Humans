import csv

file = open("list_attr_celeba_analysis.csv", "r")
data = list(csv.reader(file, delimiter=","))
file.close()

print(data[0])

print(len(data))

pairs = {}
#make pairs of tags
for i in range(1, 41):
    for o in range (1, 41):
        temp = (data[0][i], data[0][o])
        pairs.update({temp: 0})
#print(pairs)
#print(pairs.items())

for n in range(len(data)):
    if n%1000 == 0:
        print(data[n])
    for i in range(1, 41):
        for o in range (1, 41):
            
            #print(data[n][i])
            #print(data[n][o])
            if data[n][i] == '1' and data[n][o] == '1':
                #print("true")
                pairs[(data[0][i], data[0][o])] = pairs[(data[0][i], data[0][o])] + 1

print(pairs[("Black_Hair", "Male")])
#print(data)




