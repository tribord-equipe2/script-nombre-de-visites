import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from collections import Counter
import sys

routeur = str()
routeur = sys.argv[1]

#initialiser la base de donee
cred = credentials.Certificate("cle_db.json")
firebase_admin.initialize_app(cred,{ "databaseURL" : "https://routeur-3db4c.firebaseio.com/"})

#extraction des donnees de tout les bancs
dataBancs = db.reference("/Bancs").get()


dataPresence = db.reference("/presence/"+routeur).get()
if dataPresence:
	dataPresence = dataPresence["adresses"]
else:
	sys.stdout.write("0")
	sys.stdout.flush()
	sys.exit()


#contientlesentrees "arrive" dans la db
macList = list()

#dataBancs dict
for i in dataBancs.keys():
	#dict
	banc = dataBancs[i]
	for j in banc.keys():
		donee = banc[j]
		if donee["type"] == "ajout":
			macList += [donee["adresse"]]
#Les nombres de visites sont dans macList
macList = Counter(macList)

if routeur not in dataBancs:
	sys.stdout.write("reference invalide")
	sys.stdout.flush()
	sys.exit()

adresse = "0"
banc = dataBancs[routeur]
#iterer dans les cles dans l'ordre inverse (plus recent au plus vieux)
for i in list(banc.keys())[::-1]:
	if banc[i]["type"] == "ajout" and (banc[i]["adresse"] in dataPresence):
		adresse = banc[i]["adresse"]
		break
		
#mac = f"{adresse} {macList[adresse]}"
mac = f"{macList[adresse]}"
sys.stdout.write(mac)
sys.stdout.flush()
sys.exit()
