from os import system
import msvcrt

system("color f0")
system("title PyCraft Updater")

print "Hello!"
print "I'm scanning for a new version right now..."

import version

exec open("C:/Documents and Settings/Owner/Desktop/Thomas' Stuff/PyCraft 3/Release/version.py").read()

if MAJOR > version.MAJOR:
    print "Wow, PyCraft", MAJOR, "just came out! Let's get it!"
elif MINOR > version.MINOR:
    print "Oooh, a new release!"
elif BUILD > version.BUILD:
    print "There's a new build out!"
else:
    print "No, you've got the latest version!"

print "Update (y/n)?"

while True:
    a = msvcrt.getch()
    if a == "y":
        script = open("C:/Documents and Settings/Owner/Desktop/Thomas' Stuff/PyCraft 3/Release/update.bat").read()
        open("update.bat","w").write(script)
        system("update")
        raw_input()
        quit()
    if a == "n":
        print "Bye!"
        raw_input()
        quit()
    

