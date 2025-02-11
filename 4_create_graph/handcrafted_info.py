# Unfortunately we cannot automatically parse eevry river properly.
# Therefore we add handextracted infos here to be used during graph construction


# We have: 
# Sink nodes: These are rivers/oceans/lakes that are dead ends. Technically they are not rivers but they are needed to find leaf nodes.
# For each state we got: Name corrections from data naming to wiki naming
# Additional nodes that do not exist in wiki data
# Additional edges that do not exist in wiki data
# Weird Edges that have no solution yet? Double check at some point

sink_rivers = [
    "Rhein",
    "Elbe",
    "Oder",
    "Alte Oder", # At least the last station that we have
    "Ucker" # ends in haff
]

# End point because weird, no connection station available. 
ignore_rivers = [
    "Salveybach", # Double check
    "Volzine", # Double check
    "Lindower Rhin", # Double check
    'Obere Havel-Wasserstraße / Havel-Oder-Wasserstraße', # I dont get the flow... Double check
    "Karower Bach", # Flows directly into the ocean.
]


# Couple of ocean/lake/Lagoon/Fjordish sink nodes.
additional_sinks = [
    ['Nordsee', "Nordsee",  [56.741234, 2.891172]],
    ['Ostsee' "Ostsee", [58.487952, 19.863281]],
    ['Schwarzes Meer', "Schwarzes_Meer", [43.872824, 33.993808]],
    ['Leinegraben', "Leinegraben", [51.287708, 12.417187]],
    ['Tegernsee', "Tegernsee", [47.713152, 11.758016]],
    ['Chiemsee', "Chiemsee", [47.89, 12.47]]
]


# THURINGIA
thuringia_node_name_corrections = [
    ["Parthe", "Jüchse"],
    ["Laucha", "Laucha (Hörsel)"],
    ["Flograben", ' '], 
    ["Finstere Erle", "Erle (Fluss)"],
    ["Pleie", "Pleiße"],
    ["Flobach", "Floßbach"],
    ["Hrsel", "Hörsel"],
    ["Weie Elster", "Weiße Elster"],
    ["Apfelstdt",  "Apfelstädt"],
    ["Grmpen", "Grümpen"],
    ["Bse Schleuse",  "Böse Schleuse"],
    ["Gltzsch",  "Göltzsch"],
    ["Knigseer Rinne", "Königseer Rinne"],
    ["Schmücker Graben", "Hörsel"],
    ["Ltsche", "Lütsche"],
    ["Alte Gramme", "Gramme"],
    ["Schwarze Sorbitz", "Sorbitz"], 
    ["Katze", 'Katze (Schwarza)'],
    ["Leine", "Leine (Aller)"],
    ["Wipper", "Wipper (Unstrut)"],
    ["Lossa", "Lossa (Unstrut)"],
    ["Bode", "Bode (Wipper)"]
]
thuringia_additional_nodes = [
    ['Katze (Schwarza)',[50.553092290979954, 11.052280426963355]],
    ['Haselbachstollen',[50.752018983795345, 10.651615398568284]],
    ["Kernwasser", [50.753992776357336, 10.690535843873116]],
    ["Engnitz", [50.39878518460781, 11.201034982772835]],
    ["Schmalwasser", [50.79390984992156, 10.616593198679936]],
    ["Mittelwasser", [50.782006527611415, 10.620727213169001]],
    ["Plothenbach", [50.608934215905315, 11.649261280898187]],
    ["Schlagebach", [50.58539427526699, 11.17934377373044]],
    ["Erlbach",[50.90995686129518, 12.047065408053902]],
    ["Orlbach", [51.13637998046943, 10.624923791154677]],
    ["Böse Schleuse", [50.543127623048235, 10.879483756386792]],
    ["Tannenbach", [50.54369054673415, 10.879648050384617]],
    ["Flutkanal", [51.26730431926082, 11.483257988979013]], 
    ["Lemnitz", [50.429808489479555, 11.678024010471512]],
    ["Suthbach", [51.139267286080376, 10.621815515804307]],
    ["Otterbach", [50.592015671523626, 11.632839795605014]],
    ["Silbergraben", [50.74391337501102, 10.724985897618444]],
    ["Schmalwasserstollen", [50.747141335936604, 10.676531897289578]],
    ["Floßbach", [50.736218797728434, 11.593264461252046]],
    ["Steinbach", [50.68323244314141, 10.777292320848092]]
    ]
thuringia_additional_edges = [
    ['Katze (Schwarza)',"Schwarza"],
    ['Haselbachstollen',"Schmalwasser"],
    ["Schmalwasserstollen", "Kernwasser"],
    ["Kernwasser", "Ohra"],
    ["Engnitz", "Steinach"],
    ["Schmalwasser", "Apfelstädt"],
    ["Mittelwasser", "Apfelstädt"],
    ["Plothenbach", "Saale"],
    ["Schlagebach", "Lichte"],
    ["Böse Schleuse", "Schleuse"],
    ["Tannenbach", "Schleuse"],
    ["Flutkanal", "Unstrut"],
    ["Lemnitz", "Saale"],
    ["Suthbach", "Unstrut"],
    ["Otterbach", "Saale"],
    ["Silbergraben", "Ohra"],
    ["Orlbach", "Unstrut"],
    ["Floßbach", "Orla"],
    ["Steinbach", "Wilde Gera"],
    ["Erlbach", "Weiße Elster"],
]
thuringia_weird_edges = []



# bavaria
bavaria_node_name_corrections = []
bavaria_additional_nodes = []
bavaria_additional_edges = []
bavaria_marked_as_sink  = []
bavaria_edges_by_hand = []
bavaria_confounding = []
bavaria_quality_control_remove = []
bavaria_quality_control_add =  []




# BERLIN
berlin_node_name_corrections = [
["Müggelspree", "Spree"]
]
berlin_additional_nodes = [
    ["Landwehrkanal", [52.520344400925964, 13.317294749125127]],
    ["Nordgraben", [52.562505692489836, 13.228678571762389]],
    ["Teltowkanal", [52.40060244702933, 13.074670482346608]],
]
berlin_additional_edges = [
    ["Landwehrkanal", "Spree"],
    ["Nordgraben", "Havel"],
    ["Teltowkanal", "Havel"],
]
berlin_weird_edges = []


# SAXONY
saxony_node_name_corrections = [
    ["Langes Wasser", "Langes Wasser (Hoyerswerdaer Schwarzwasser)"],
    ["Vereinigte Weißeritz", "Weißeritz"],
    ["Breitenbach (Blatensky potok)", "Breitenbach (Schwarzwasser)"],
    ["Jöhstädter Schwarzwasser", "Schwarzwasser (Preßnitz)"],
    ["Zwota (Svatava)"	, "Zwota (Fluss)"],
    ["Große Striegis", "Striegis"],
    ["Natzschung (Nacetinsky potok)", 'Natzschung (Fluss)'],
    ["Jahna-Umflut", "Jahna Umflut"],
    ["Landwasser", "Landwasser (Mandau)"],
    ["Vereinigte Mulde", "Mulde"],
    ["Mühlbach", "Mühlbach (Mulde)"]
]
saxony_additional_nodes = [
    ["Lomschanke",[51.30764092913986, 14.456081660330382]],
    ["Niederauer Dorfbach",[51.17322801722008, 13.472770507079023]],
    ["Keppritzbach",[51.28412349506308, 13.28906967988004]],
    ["Rothschönberger Stolln (Techn. Anlage)", [51.07297236082332, 13.404375621254497]],
    ["Elligastbach", [51.35699454513539, 13.488112498301952]],
    ["Mühlbach (Mulde)", [51.35619711328818, 12.728803173822005]],
    ["Rotes Wasser", [50.7860575195639, 13.814651911429145]],
    ["Schwarze Elster-Umflut (Tradoer Teichgruppe)", [51.3468780131057, 14.221343204839204]]
]
saxony_additional_edges = [
    ["Lomschanke", "Kleine Spree"],
    ["Niederauer Dorfbach", "Elbe"],
    ["Keppritzbach", "Jahna"],
    ["Rothschönberger Stolln (Techn. Anlage)", "Triebisch"],
    ["Elligastbach", "Große Röder"],
    ["Mühlbach (Mulde)","Mulde"],
    ["Rotes Wasser", "Müglitz"],
    ["Schwarze Elster-Umflut (Tradoer Teichgruppe)", "Schwarze Elster"],
    ["Fuhne", "Saale"],
    ["Ihle", "Elbe-Havel-Kanal"],
]
saxony_weird_edges = [
    "Schwarze Elster-Umflut (Tradoer Teichgruppe)"
]



# SAXONY ANHALT
saxony_anhalt_node_name_corrections = [
    ["Querne-Weida",  "Querne/Weida"],
    ["Laucha", "Laucha (Saale)"],
    ["Beber", "Beber (Ohre)"],
    ["Goldbach", "Goldbach (Bode)"],
    ["Fuhne (westlich)", "Fuhne"],
    ["Jeetze", 'Jeetzbach'],
    ["Zörbiger Strengbach", "Strengbach"],
    ["Leine", "Leine (Helme)"],
    ["Wipper", "Wipper (Saale)"],
    ["Nuthe", "Nuthe (Elbe)"]
]
saxony_anhalt_additional_nodes = [
["Zahna", [51.85538923523028, 12.703689103530408]],
["Goldbach (Bode)", [51.88951405223316, 11.183211556417927]],
["Biberbach", [51.243808360101035, 11.638224759418015483254]],
["Tucheim-Parchener Bach", [52.411176608174, 12.139707615727879]],
["Untermilde", [52.71726528993822, 11.52184650380211]], 
["Zehrengraben", [52.99846095201102, 11.543801623638142]],
["Götsche", [51.526069691500474, 11.922449128271142]],
["Geisel", [51.371505116799874, 11.997993536449185]],
["Strengbach",[51.64876947145937, 12.094792274654372]],
["Jäglitz", [52.869980612369595, 12.388766634604671]],
["Alte Jäglitz", [52.79418003986678, 12.279309915613435]]
]
saxony_anhalt_additional_edges = [
["Zahna", "Elbe"],
["Goldbach (Bode)", "Bode"],
["Biberbach", "Unstrut"],
["Tucheim-Parchener Bach", "Elbe-Havel-Kanal"],
["Untermilde", "Biese"],
["Alte Jäglitz", "Dosse"],
["Jäglitz", "Neue Jäglitz"],
["Zehrengraben", "Seege"],
["Götsche", "Saale"],
["Geisel", "Saale"],
["Wettera", "Saale"],
["Strengbach", "Fuhne"]
]
saxony_anhalt_weird_edges = []


# BRANDENBURG
brandenburg_node_name_corrections = [
    ["Klinge",  "Klingefließ"],
    ["Obere Malxe", "Malxe"],
    ["Löcknitz", "Löcknitz (Elbe)"],
    ["Stille Oder", "Alte Oder"],
    ["Stepenitz", "Stepenitz (Elbe)"],
    ["Ucker", "Uecker"]
]

brandenburg_additional_nodes = [
    ["Schwarzes Fließ", [51.9776724694111, 14.704913251864012]],
    ["Südumfluter",[51.837069402700905, 14.186775254599356]],
    ["Hegensteinfließ", [53.18578615721768, 13.154423203704054]],
    ["Belziger Bach", [52.231085892505604, 12.657397586707788]],
    ["Königsgraben Luckenwalde", [52.11223142626772, 13.196684274576358]],
    ["Dossespeicher-Zuleiter", [52.99538427195692, 12.504057666807991]],
    ["Brieskower Kanal", [52.28829574332449, 14.575474830882946]],
    ["Freienwalder Landgraben", [52.83127842078231, 13.986941322494769]],
    ["Föhrenfließ", [51.58544415660388, 14.731570042448732]],
    ["Hammergraben Lauchhammer", [51.460455937217134, 13.623357136941564]],
    ["Grano-Buderoser Mühlenfließ", [52.011948715263934, 14.725890650850575]],
    ["Schacke", [51.5360102178286, 13.37430157973241]],
    ["Dahme-Umflut-Kanal", [52.10900372780405, 13.758274006024905]],
    ["Klempnitz", [52.89190393438797, 12.456683367781652]],
    ["Temnitz (Rhin)", [52.79091859771979, 12.61424360203155]],
    ["Elbe-Havel-Kanal", [52.39375498516879, 12.39176504896246]],
    ["Großer Havelländischer Hauptkanal",[52.664357370423375, 12.312884112363431] ],
    ["Dauergraben", [53.386607060368846, 13.865283606184994]], 
    ["Hausseebruchgraben", [53.2661702842787, 13.624255540451939]],
    ["Schulzenfließ", [53.07892421855705, 13.366599129941921]]
]

brandenburg_additional_edges = [
    ["Südumfluter", "Spree"],
    ["Schwarzes Fließ", "Lausitzer Neiße"],
    ["Belziger Bach", "Plane"],
    ["Königsgraben Luckenwalde", "Nuthe"],
    ["Dossespeicher-Zuleiter", "Dosse"],
    ["Brieskower Kanal", "Oder"],
    ["Freienwalder Landgraben", "Alte Oder"],
    ["Föhrenfließ", "Lausitzer Neiße"],
    ["Hammergraben Lauchhammer", "Schwarze Elster"],
    ["Grano-Buderoser Mühlenfließ", 'Lausitzer Neiße'],
    ["Schacke", "Schwarze Elster"],
    ["Rhin", "Havel"],
    ["Temnitz (Rhin)", "Rhin"],
    ["Hegensteinfließ", "Havel"],
    ["Dahme-Umflut-Kanal", "Dahme"],
    ["Klempnitz", "Dosse"],
    ["Elbe-Havel-Kanal" , "Havel"],
    ["Großer Havelländischer Hauptkanal", "Havel"],
    ["Dauergraben", "Uecker"],
    ["Hausseebruchgraben" , "Strom"],
    ["Schulzenfließ", "Havel"]
]
brandenburg_weird_edges = [
 "Hammergraben Lauchhammer", "Föhrenfließ","Lindower Rhin","Klempnitz"
]
state_placeholder_edges = [
["Zwota (Fluss)", "Bavaria"],
["Milz", "Bavaria"], 
["Itz", "Bavaria"],
["Aller", "Lower Saxony"],
["Werra", "Hessen"],
["Kreck (Fluss)", "Bavaria"],
["Leine (Aller)", "Lower Saxony"]
]


edges_by_hand = [
    [574930,573110, "Neue Gramme flows into the Gramme but after the last station. Map to next river."],
    [252520,None, "Flows into Itz but beyond the last station. Next river is main which is not included."],
    [577343,577320, "Flows into Leuda which flows into weida (2 jumps for next station). Issue here with height."],
    [2414920, None, "As usual, double jump"],
    [252510,None, "Flows into Itz but beyond the last station. Next river is main which is not included."],
    [422201, 422000, "Matching goes wrong as there is another river with the same name in the same state"],
    [429940, None, "Double jump as usual, but the weser is not in the data set"],
    [574130, 573010, "Double jump but river in the middle does not exist."],
    [429720, 429600,"Leinakanal, Wilder Graben (Oder Wilde Leina), Nesse."],
    [574110,574130 , "Node doesnt exit in wiki graph so it cant be matched"],
    [574320,574300, "Flows over some weird Bach. into Wilde Gera "],
    [552121, 5011100,"Flows into Keppritzfbach then Jahna then Elbe without infos"],
    [579504,579006, "Hassel into Rappode into Bode"],
    [444210,None, "Goes into Oker where we dont have data. "],
    [597208,None, "Goes into Jeetzel where we dont have data. "],
    [6952903, None, "Goes into Uecker where we dont have data"],
    [5546801,5530500, "Jumps one river as usual."],
    [5826701,5827700,"Again some river jump."],
    ["043411", None, "Flows into the ocean"],
    ["044051", None, "Ocean"],
    ["043902", None,  "Ocean"],
    ["596180",5930010, "Elde into Kanal into Elbe"],
    ["049012", None,  "Ocean"],
    ["045542", None,   "Ocean"],
    [596550, 596180, "Artificial Canal that goes into Elde Kanal"],
    ["046111", None, "Ends into the Ocean"],
    ["046161", None, "Ends into the Ocean"],
    ["047700", "047073", "Trebel into Penne"], 
    ["046175", None, "Ends into the Ocean"],
    ["045530", None, "Barthe only measured before and next is ocean"],
    ["045813", None, "Ocean"],
    ["045402", None, "Ocean"],
    ["046401", None, "Ocean"],
    ["045500", None, "Ocean"],
    ["598100", None, "ELbe but last measurement before"],
    [596455, 596180, "Goes into elde. Wasserstraße the only masurement available after crossing"],
    ["048412", "048035", "Tollensee matching didnt work"],
    ["043700", None, "Ocean"],
    ["043600", None,  "Ocean"],
    ["599105", None, "Elbe but too late."],
    ["043550", "043420", "Name didnt exist."],
    ["0494101", "049012", "Beeke doesnt exist, Uecker is next."],
    ["044253", "044022", "non estimated height broken"],
    ["043810","596180", "Will be impossible to detect. through lakes and Stör into elde."],
    ["047015", None, "Peene not available before ocean"],
    ["047302", None, "Moves into Ostpeene which goes into kanal which goes into ocean. No measurements"],
    ["048601", None, "into Zarow, ocean which doesnt exist."],
    ["048602", "048601", "Complicated pattern but flows into weißen graben. river unknown."],
    ["048639", "048601", "river named differently flows into graben as well."],
    ["047073", "047023", "Peene reversed. Probably need to remove cycle."],
    ["047101", "047073", "Peene connected."],
    ["045061", None, "Endpoint in the Ocean."],
    ["5898807", "5807900", "Into havel but  elevation is broken"],
    [5845800, 5823800, "Hammergraben over a lot of distance into spree."],
    [5890801,5891701, "Wustrauer Rhin that flows into the Rhin somehow"],
    [5891001, 5891701, "Flows back together into the rhin"],
    ["043460", None, "Into trave but behind last station"],
    [594137,594005, "FLows into Milde but the next station is in Biese" ],
    [594107,594005, "Milde Into biese but wiki weird"],
    [594010, 594021, "Biese into Aland but wiki weird"],
    [594180,594010, "Uchte into Biese." ],
    [594050,5930010, "Aland into elbe. wiki weird" ],
    [594021,594020, "Aland connection"]

]
    

confounding = [
    # River splits (Confounding.).
    [552101,552121, "Jahna splits into umflut. confounding."],    
    [553001,553012, "Schwarze Elster splits into Lakes that flow back. This might be very loosely coupled."],
    [554550,5546801, "Geißlitz is a split of the Große Röder. confounding."],
    [574210, 574930, "Gera splits and flows into this weird area which probably flows back into umstrut. Neue gramme und Gera confounded (likely.)"],
    [573110, 573150, "Unstrut split into Kanal anf flows back into each other."],
    [5879407, 5879408, "Splits and flows back togther into Nuther later. COnfounding."],
    [5821000, 5845800, "Splits from Spree. Later flows back in a weird manner."],
    [5898302, 5898601, "Jäglitz splits in old and new. Later flows back together into Havel. Confounding."],
    [5823800,5856400, "Connection from Spree to Dahme. Cnfounding." ],
    [5827000,5866301, "Split and come back into spree. Needs further mapping probably, berlin..."],
    [5815901, 5870801, "Havel area is crazy. This is probably correct and confounding havel."],
    [5891001, 5891701, "Flows back together into the rhin"],
    [5891200,5891001, "SPlits into umfut und Rhin"],
    ["595990",596180 , "Elde into Kanal into Elbe"],
    ["574610","429720", "Artificial river split"],
    [554550,5546400, "Triple split"],
    [5862811,5870100, "Kanal coming from dahme"],
    [5827000, 5826701, "Spree splits into this"],

]



quality_control_remove = [
(12,14),
(1062,1060),
(1061,1062),
(199,198),
(198,197),
(652,653),
(614,613),
(1015,1014),
(682,681),
(798,797),
(795,794),
(468,736),
(823,736),
(463,1023),
(233,173),
(142,167),
(303,910),
(215,22),
(297,812),
(754,811),
(427,582),
(935,307),
(433,865),
(573,305),
(678,305),
(283,730),
(226,729),
(252,86),
(203,974),
(392,791),
(393,376),
(181,270),
(1048,829),
(412,816),
(152,175),
(954,666),
(82,951),
(951,614),
(947,614),
(528,1015),
(92,912),
(752,911),
(721,911),
(539,1016),
(657,890),
(179,166),
(646,814),
(992,106),
(162,169),
(727,171),
(84,729),
(698,173),
(824,173),
(456,316),
(653,745),
(1093,730),
(764,730),
(1073,732),
(300,298),
(230,344),
(955,1037),
(381,642),
(117,211),
(431,177),
(398,177),
(990,176),
(621,577),
(936,625),
(576,305),
(277,305),
(864,305),
(1109,865),
(933,308),
(99,310),
(99,307),
(656,1037),
(728,727),
(729,728),
(1015,1013),
(1013,1014),
(258,439),
(1060,1059),
(197,559),
(301,775),
(621,571),
(71,869),
(245,145),
(148,145),
(151,309),
(590,589)

]


quality_control_add = [
(199,197),
(197,198),
(198,559),
(1061,1060),
(1060,1062),
(653,652),
(613,614),
(682,1110),
(795,798),
(798,794),
(795,798),
(468,791),
(823,791),
(463,1018),
(233,555),
(142,304),
(303,909),
(215,20),
(297,811),
(754,810),
(935,306),
(433,864),
(573,307),
(678,304),
(283,729),
(226,727),
(252,85),
(203,975),
(392,793),
(393,175),
(181,269),
(1048,828),
(412,815),
(152,174),
(82,613),
(951,613),
(947,613),
(528,1014),
(539,752),
(657,889),
(179,555),
(646,811),
(992,105),
(162,168),
(728,171),
(84,727),
(698,172),
(824,174),
(456,315),
(652,745),
(1093,729),
(764,729),
(1073,731),
(300,792),
(230,770),
(955,1036),
(381,641),
(117,212),
(431,176),
(398,176),
(990,175),
(621,570),
(936,305),
(576,306),
(276,305),
(864,307),
(1109,864),
(933,307),
(656,1036),
(727,728),
(729,727),
(12,166),
(148,409),
(146,148),
(1015,1014),
(1014,1013),
(1003,21),
(258,592),
(1062,1059),
(301,774),
(773,201),
(400,613),
(427,578),
(295,577),
(71,868),
(125,122),
(245,145),
(472,682),
(584,309),
(151,584),
(312,584),
(495,584),
(786,584),
(99,307),
(99,277),
(20,589),
(591,22),
(865,101),
(100,22)
]



