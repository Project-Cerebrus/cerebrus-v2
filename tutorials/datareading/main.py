import pickle
import os

os.system("clear")
# make list
names = ["Ace", "Kaneki", "Skull Crusher"]

print(names)

# Save list using pickle # web is write as binary
pickle.dump(names,open("names.dat", "wb"))

# change list  
names.remove("Skull Crusher")

# re print
print(names)

#load list #rb is read binary
newnames = pickle.load(open("names.dat","rb"))