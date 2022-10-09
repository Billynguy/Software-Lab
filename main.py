import projects
import hardwareSet
import connector

# PLAYGROUND FOR JUST MESSING AROUND WITH DATABASE!

id = 101
name = "Second Tester"
description = "the very second test project!"
user = "NotBilly"

# HWSet1 = hardwareSet.HWSet("SecondTest", 1000)
# Project1 = projects.Projects(101, name, description, user)
# Project1.add_user("Daniel")
# Project1.add_user("Daniel")
# Project1.add_hwsets("HWSet1")
# Project1.add_hwsets("HWSet2")
# Project1.remove_hwsets("HWSet2")

# print(projects.Projects.get_description(100))
# projects.Projects.add_user(100, "John")
# projects.Projects.remove_user(100, "John")
# projects.Projects.add_hwsets(100, "Hardware Set")
# projects.Projects.remove_hwsets(100, "Hardware Set")
# projects.Projects.remove_hwsets(100, "HWSet1")
pid = "100"
print(hardwareSet.HWSet.get_names())
print(hardwareSet.HWSet.get_capacity("TestSet"))
print(hardwareSet.HWSet.get_availability("TestSet"))
projects = hardwareSet.HWSet.get_checkedout_list("SecondTest")
amount = 100;
for x in projects:
    if(x == pid):
        print("found")
        x = projects.get(pid)
        print(x)
        x = x + amount
        print(x)
        projects.setdefault(pid, x)

    else:
        print("not found")
