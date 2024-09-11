text = ""
with open("plushie_code_insertion.py", "r+") as file:
    text = file.read().replace("BLACKHOLE","ALEXNOMPE").replace("blackhole","alexnompe").replace("Blackhole","AlexNompe")

if text != "":
   with open("plushie_code_insertion.py", "w+") as file:
       file.write(text)