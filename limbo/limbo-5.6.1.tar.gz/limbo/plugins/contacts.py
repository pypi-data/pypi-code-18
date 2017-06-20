import os
import re

DIR = os.path.dirname(os.path.realpath(__file__))
VCF = """BEGIN:VCARD
VERSION:3.0
N:Abel;Alayna;;;
FN:Alayna Abel
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:2407157056
EMAIL;type=INTERNET;type=WORK:alayna@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Auclair;Mike;;;
FN:Mike Auclair
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:4014516037
EMAIL;type=INTERNET;type=WORK:mike.auclair@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Balboni;Jeff;;;
FN:Jeff Balboni
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:4065997488
EMAIL;type=INTERNET;type=WORK:jeff@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Baliff;Rachel;;;
FN:Rachel Baliff
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:240-463-8495
EMAIL;type=INTERNET;type=WORK:rachel@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Bonenberger;Brian;;;
FN:Brian Bonenberger
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:810-599-0918
EMAIL;type=INTERNET;type=WORK:brian@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Carelock;Nikki;;;
FN:Nikki Carelock
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:8323985056
EMAIL;type=INTERNET;type=WORK:nikki@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Chapman;Danny;;;
FN:Danny Chapman
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:401-451-3151
EMAIL;type=INTERNET;type=WORK:danny@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Cizmadia;Dee;;;
FN:Dee Cizmadia
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:310.270.3930
EMAIL;type=INTERNET;type=WORK:dee@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Cloud;Daniel;;;
FN:Daniel Cloud
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:2028027073
EMAIL;type=INTERNET;type=WORK:daniel.cloud@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Clyde;Nick;;;
FN:Nick Clyde
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:530-559-2575
EMAIL;type=INTERNET;type=WORK:nick@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Dawson;Alastair;;;
FN:Alastair Dawson
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:714-595-3281
EMAIL;type=INTERNET;type=WORK:alastair@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Dengo;Sophia;;;
FN:Sophia Dengo
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:8325663655
EMAIL;type=INTERNET;type=WORK:sophia@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:DiMartino;Robert;;;
FN:Robert DiMartino
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:513-827-0573
EMAIL;type=INTERNET;type=WORK:robert.dimartino@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Doan;Eugene;;;
FN:Eugene Doan
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:857-526-6580
EMAIL;type=INTERNET;type=WORK:eugene@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Ellena;Laura;;;
FN:Laura Ellena
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:858-699-0544
EMAIL;type=INTERNET;type=WORK:laura@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Fairhead;Bob;;;
FN:Bob Fairhead
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:6177840700
EMAIL;type=INTERNET;type=WORK:bob@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Fettet;Louis;;;
FN:Louis Fettet
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:5042020991
EMAIL;type=INTERNET;type=WORK:louis@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Follows;Karey;;;
FN:Karey Follows
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:7035091617
EMAIL;type=INTERNET;type=WORK:karey@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Fromberg;Oren;;;
FN:Oren Fromberg
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:2404868091
EMAIL;type=INTERNET;type=WORK:oren@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Gansen;Chris;;;
FN:Chris Gansen
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:7345784242
EMAIL;type=INTERNET;type=WORK:chris@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Gardner;Joe;;;
FN:Joe Gardner
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:512-791-8200
EMAIL;type=INTERNET;type=WORK:joe.gardner@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Gershman;Greg;;;
FN:Greg Gershman
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:4439282961
EMAIL;type=INTERNET;type=WORK:greg@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Greim;Cat;;;
FN:Cat Greim
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:4127217317
EMAIL;type=INTERNET;type=WORK:cat@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Gryth;Brian;;;
FN:Brian Gryth
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:3037485447
EMAIL;type=INTERNET;type=WORK:brian.gryth@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Guse;Nathan;;;
FN:Nathan Guse
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:9203901269
EMAIL;type=INTERNET;type=WORK:nathan@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Gwinn;Katie;;;
FN:Katie Gwinn
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:5639209683
EMAIL;type=INTERNET;type=WORK:katie@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Hawkins;Spencer;;;
FN:Spencer Hawkins
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:5713090621
EMAIL;type=INTERNET;type=WORK:spencer@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Hein;Shawna;;;
FN:Shawna Hein
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:5302774925
EMAIL;type=INTERNET;type=WORK:shawna@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Holland;Aubrey;;;
FN:Aubrey Holland
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:617-290-8159
EMAIL;type=INTERNET;type=WORK:aubrey@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Hsu;Claire;;;
FN:Claire Hsu
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:7188012354
EMAIL;type=INTERNET;type=WORK:claire@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:James;Alexis;;;
FN:Alexis James
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:2156204651
EMAIL;type=INTERNET;type=WORK:alexis@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Johnson;Carl;;;
FN:Carl Johnson
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:8085990232
EMAIL;type=INTERNET;type=WORK:carl@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Johnson;Chris;;;
FN:Chris Johnson
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:8054785327
EMAIL;type=INTERNET;type=WORK:chris.johnson@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Julian;Jonathan;;;
FN:Jonathan Julian
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:4438031427
EMAIL;type=INTERNET;type=WORK:jonathan@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Karshenas;Kam;;;
FN:Kam Karshenas
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:2176372227
EMAIL;type=INTERNET;type=WORK:kam@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Kassemi;James;;;
FN:James Kassemi
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:5054140621
EMAIL;type=INTERNET;type=WORK:james.kassemi@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:King;Brian;;;
FN:Brian King
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:12024257630
EMAIL;type=INTERNET;type=WORK:brian.king@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Koski;Ken;;;
FN:Ken Koski
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:651-497-1094
EMAIL;type=INTERNET;type=WORK:ken@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Kutil;Ben;;;
FN:Ben Kutil
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:4104409565
EMAIL;type=INTERNET;type=WORK:ben@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Lewis;Elizabeth;;;
FN:Elizabeth Lewis
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:7039661887
EMAIL;type=INTERNET;type=WORK:elizabeth.lewis@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Li;Lihan Li;;;
FN:Lihan Li Li
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:7036188660
EMAIL;type=INTERNET;type=WORK:lihan@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Lindo;Mo;;;
FN:Mo Lindo
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:3019191674
EMAIL;type=INTERNET;type=WORK:mo@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Linn;Stacy;;;
FN:Stacy Linn
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:5419685218
EMAIL;type=INTERNET;type=WORK:stacy@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Manning;Christopher;;;
FN:Christopher Manning
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:773-290-8012
EMAIL;type=INTERNET;type=WORK:christopher.manning@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Martinez;Austin;;;
FN:Austin Martinez
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:2177141336
EMAIL;type=INTERNET;type=WORK:austin@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:McMonagle;Joseph;;;
FN:Joseph McMonagle
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:484 686 4499
EMAIL;type=INTERNET;type=WORK:joe@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Meek;Wryen;;;
FN:Wryen Meek
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:6787015005
EMAIL;type=INTERNET;type=WORK:wryen@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Mejeur;Curtis;;;
FN:Curtis Mejeur
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:6162936808
EMAIL;type=INTERNET;type=WORK:curtis@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Mill;Bill;;;
FN:Bill Mill
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:860-882-3587
EMAIL;type=INTERNET;type=WORK:bill@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Miller;Michael;;;
FN:Michael Miller
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:3013333333
EMAIL;type=INTERNET;type=WORK:michael@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Miller Sharkey;Slayanna;;;
FN:Slayanna Miller Sharkey
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:8285515435
EMAIL;type=INTERNET;type=WORK:leanna@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Million;Savannah;;;
FN:Savannah Million
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:2067075447
EMAIL;type=INTERNET;type=WORK:@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Murray;Scott;;;
FN:Scott Murray
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:8643146872
EMAIL;type=INTERNET;type=WORK:scott@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Nagle;Ryan;;;
FN:Ryan Nagle
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:7739887258
EMAIL;type=INTERNET;type=WORK:ryan@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Neelbauer;Juliana;;;
FN:Juliana Neelbauer
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:2023303907
EMAIL;type=INTERNET;type=WORK:juliana@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Oberhaus;Kristin;;;
FN:Kristin Oberhaus
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:712-470-0087
EMAIL;type=INTERNET;type=WORK:kristin.oberhaus@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Olson;Mark;;;
FN:Mark Olson
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:4435621041
EMAIL;type=INTERNET;type=WORK:mark@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:O'Neil;Dan;;;
FN:Dan O'Neil
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:7739606045
EMAIL;type=INTERNET;type=WORK:danx@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Phan;Cindy;;;
FN:Cindy Phan
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:9169958395
EMAIL;type=INTERNET;type=WORK:cindy@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Rhein;James;;;
FN:James Rhein
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:7739515944
EMAIL;type=INTERNET;type=WORK:james@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Roueche;Rachael;;;
FN:Rachael Roueche
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:703 489 0705
EMAIL;type=INTERNET;type=WORK:rachael.roueche@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Ryan;Bill;;;
FN:Bill Ryan
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:9787299758
EMAIL;type=INTERNET;type=WORK:bill.ryan@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Sahni;Mickin;;;
FN:Mickin Sahni
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:7037171679
EMAIL;type=INTERNET;type=WORK:mickin@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Shyong;Ben;;;
FN:Ben Shyong
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:4085059891
EMAIL;type=INTERNET;type=WORK:ben.shyong@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Smith;Graham;;;
FN:Graham Smith
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:267-386-5979
EMAIL;type=INTERNET;type=WORK:graham@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Smith;Paul;;;
FN:Paul Smith
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:773-934-4607
EMAIL;type=INTERNET;type=WORK:paul@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Smith;Winnie;;;
FN:Winnie Smith
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:3028980775
EMAIL;type=INTERNET;type=WORK:winnie@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Steinmetz;Amrom;;;
FN:Amrom Steinmetz
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:9176275884
EMAIL;type=INTERNET;type=WORK:amrom@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Sutton;Michael;;;
FN:Michael Sutton
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:3013790889
EMAIL;type=INTERNET;type=WORK:michael.sutton@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Swain;Veronica;;;
FN:Veronica Swain
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:609-802-4586
EMAIL;type=INTERNET;type=WORK:veronica@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Szekeresh;Sarah-Jaine;;;
FN:Sarah-Jaine Szekeresh
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:(513) 652-6524
EMAIL;type=INTERNET;type=WORK:sarah-jaine@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Szeluga;Chris;;;
FN:Chris Szeluga
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:9089388795
EMAIL;type=INTERNET;type=WORK:chris.szeluga@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Taylor;Alex;;;
FN:Alex Taylor
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:4012266317
EMAIL;type=INTERNET;type=WORK:alex@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Topper;Ian;;;
FN:Ian Topper
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:9376812200
EMAIL;type=INTERNET;type=WORK:ian@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Valarida;Christopher;;;
FN:Christopher Valarida
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:503 302 0306
EMAIL;type=INTERNET;type=WORK:chris.valarida@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Veal;Rachel;;;
FN:Rachel Veal
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:571-244-9368
EMAIL;type=INTERNET;type=WORK:rachel.veal@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Vinograd;Patrick;;;
FN:Patrick Vinograd
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:650-804-2530
EMAIL;type=INTERNET;type=WORK:patrick@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Walker;Kristin;;;
FN:Kristin Walker
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:540-797-8853
EMAIL;type=INTERNET;type=WORK:kristin@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Weber;Caitlin;;;
FN:Caitlin Weber
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:503-367-9483
EMAIL;type=INTERNET;type=WORK:caitlin@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Wilkerson;Rob;;;
FN:Rob Wilkerson
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:443 745 1069
EMAIL;type=INTERNET;type=WORK:rob@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Williams;Carolyn;;;
FN:Carolyn Williams
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:2404238529
EMAIL;type=INTERNET;type=WORK:carolyn@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Wohl;Jeremy;;;
FN:Jeremy Wohl
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:415 994 5074
EMAIL;type=INTERNET;type=WORK:jeremy@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Wolfert;Patrick;;;
FN:Patrick Wolfert
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:5413602784
EMAIL;type=INTERNET;type=WORK:patrick.wolfert@adhocteam.us
END:VCARD
BEGIN:VCARD
VERSION:3.0
N:Woodard;Mel;;;
FN:Mel Woodard
ORG:Ad Hoc LLC
TEL;type=CELL;type=VOICE:4252811675
EMAIL;type=INTERNET;type=WORK:mel@adhocteam.us
END:VCARD"""

def phone(name):
    cards = ["BEGIN:{}".format(x) for x in re.split("^BEGIN:", VCF, flags=re.M) if x]
    matches = [c for c in cards if all(n in c for n in name.split())]

    if not matches:
        return "not able to find that person, sorry"

    result = []
    for card in matches:
        fn, phone = re.search("FN:(.*?)\n.*TEL.*?([\d\-]*)\n", card, flags=re.S).groups()
        result.append("*{}*: {}".format(fn, phone))

    return "\n".join(result)


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!phone (.*)", text)
    if not match:
        return

    searchterm = match[0]
    return phone(searchterm)

on_bot_message = on_message
