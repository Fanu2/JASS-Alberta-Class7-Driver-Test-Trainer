#!/usr/bin/env python3
"""
Alberta Class 7 Knowledge Test Trainer
JASS Alberta Driver Test Trainer v1.0

Purpose:
- Study Alberta Class 7 car/light-truck rules.
- Practice randomized 30-question mock tests.
- Review explanations and weak areas.
- Open the official Government of Alberta Driver's Guide.

The question bank is original practice material based on the Government of Alberta
Driver's Guide and should NOT be treated as the official examination.
No app can guarantee a passing result.
"""

from __future__ import annotations

import json
import random
import sys
import webbrowser
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QButtonGroup, QCheckBox, QComboBox, QDialog,
    QDialogButtonBox, QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QMainWindow, QMessageBox,
    QPushButton, QProgressBar, QRadioButton, QScrollArea, QSizePolicy,
    QSpinBox, QStackedWidget, QVBoxLayout, QWidget
)

OFFICIAL_GUIDE_PAGE = "https://www.alberta.ca/driver-guides-overview-and-pdf-versions"
OFFICIAL_KNOWLEDGE_PAGE = "https://www.alberta.ca/drivers-knowledge-test"

@dataclass
class Question:
    category: str
    question: str
    options: List[str]
    answer: int
    explanation: str

# Original practice questions. Rules are intentionally phrased differently from
# the official guide; users should consult the official guide for the authoritative text.
Q = [
Question("Test & Licensing","How many questions are on the Alberta Class 7 knowledge test?",
["20","25","30","40"],2,"The current Alberta knowledge test has 30 multiple-choice questions."),
Question("Test & Licensing","What score is required to pass the Class 7 knowledge test?",
["20/30","23/30","25/30","28/30"],2,"You need at least 25 correct answers out of 30."),
Question("Test & Licensing","How often can you take the knowledge test?",
["Once per hour","Once per day","Once per week","Unlimited times per day"],1,"The Alberta page says the test can be taken once per day."),
Question("Test & Licensing","Where are Alberta knowledge tests taken?",
["Only at police stations","At registry agent offices","Only online from home","At driving schools only"],1,"Knowledge tests are taken at Alberta registry agent offices."),
Question("Licensing","A Class 7 learner driving a Class 5 vehicle must be accompanied by whom?",
["Anyone over 16","A full Class 5 driver who is at least 18 and sits in the front passenger seat","Any passenger with 2 years of experience","No one"],1,"A Class 7 learner must have the required qualified supervising driver in the front passenger seat."),
Question("Licensing","What is the minimum age to obtain a Class 7 learner's licence in Alberta?",
["14","15","16","18"],0,"The minimum age is 14."),
Question("Licensing","What is the minimum age for a full non-GDL Class 5 licence?",
["16","17","18","21"],2,"A full non-GDL Class 5 requires the driver to be at least 18."),
Question("Licensing","A Class 7 driver may drive between which hours?",
["10 pm–6 am","12 am–5 am is prohibited","1 am–4 am","There is no restriction"],1,"Class 7 drivers cannot drive between midnight and 5 am."),
Question("Licensing","What alcohol level applies to a Class 7 driver?",
["Up to 0.05%","Up to 0.08%","0%","Only under 0.02%"],2,"Learner drivers must have zero alcohol while driving."),
Question("Licensing","A Class 7 driver may carry more people than there are seat belts if the trip is short.",
["True","False","Only in daytime","Only with an adult"],1,"The number of occupants cannot exceed the available seat belts."),
Question("Traffic Signs","A red octagonal sign means:",
["Yield","Stop","Do not enter","Railway crossing"],1,"The eight-sided red sign is STOP."),
Question("Traffic Signs","An inverted red-and-white triangle means:",
["Stop","Yield","School zone","No passing"],1,"The inverted triangle is the YIELD sign."),
Question("Traffic Signs","A yellow diamond-shaped sign generally gives:",
["Regulatory instructions","Warning information","Parking permission","Route numbers"],1,"Yellow diamond signs generally warn of upcoming conditions or hazards."),
Question("Traffic Signs","A white rectangular sign generally provides:",
["Regulatory information","Weather forecasts","Emergency medical information","Fuel prices"],0,"White rectangular signs commonly communicate rules/regulations."),
Question("Traffic Signs","A fluorescent yellow-green sign is commonly associated with:",
["Pedestrian/school-related warnings","Parking meters","Highway route numbers","Railway freight"],0,"Fluorescent yellow-green is used for high-visibility pedestrian and school-related warnings."),
Question("Traffic Signals","A steady red traffic light means:",
["Proceed if clear","Stop","Slow down only","Turn immediately"],1,"A steady red signal requires a stop."),
Question("Traffic Signals","A steady yellow light means:",
["Speed up","Stop if you can do so safely; otherwise proceed cautiously through the intersection","Always reverse","Turn only"],1,"Yellow warns that the signal is changing to red; stop when safe."),
Question("Traffic Signals","A flashing red light should be treated as:",
["A yield sign","A stop sign","A green light","A school-zone sign"],1,"A flashing red signal requires a complete stop, then proceed when safe."),
Question("Traffic Signals","A flashing yellow light means:",
["Stop completely","Proceed with caution","Road closed","You must turn right"],1,"Flashing yellow means proceed with caution."),
Question("Traffic Signals","If a traffic light is not working, a driver should:",
["Treat it as a green light","Proceed without slowing","Treat the intersection as an all-way stop","Follow the car ahead"],2,"A malfunctioning signal should be treated as an all-way stop."),
Question("Right of Way","At an uncontrolled intersection, if two vehicles arrive at approximately the same time, who generally has the right of way?",
["The vehicle on the left","The vehicle on the right","The larger vehicle","The faster vehicle"],1,"The vehicle on the right generally has the right of way when vehicles arrive at the same time."),
Question("Right of Way","When turning left, you generally must yield to:",
["Oncoming traffic and pedestrians that have the right of way","Only trucks","Nobody","Only bicycles"],0,"Left-turning traffic must yield to relevant oncoming traffic and pedestrians."),
Question("Right of Way","A pedestrian in a marked crosswalk generally has:",
["No priority","The right of way","Priority only at night","Priority only if waving"],1,"Drivers must yield as required to pedestrians in crosswalks."),
Question("Right of Way","When an emergency vehicle approaches with siren/lights, you should generally:",
["Race ahead of it","Safely pull over and stop as required","Stop in the middle of the intersection","Ignore it if you have a green light"],1,"Safely yield and pull over/stop as required."),
Question("Right of Way","At a four-way stop, the first vehicle to stop generally proceeds first, when safe.",
["True","False","Only trucks proceed first","Only vehicles turning right"],0,"Order of arrival is a key rule at an all-way stop, subject to right-of-way rules."),
Question("Turning","Before making a turn, you should:",
["Signal only after turning","Check mirrors/blind spots, signal, and turn when safe","Honk continuously","Move without checking"],1,"Proper observation, signalling and a safe manoeuvre are required."),
Question("Turning","A right turn on a red light is generally permitted when:",
["Always, without stopping","After a complete stop and when permitted and safe, yielding as required","Only for trucks","Never in Alberta"],1,"Unless prohibited by a sign/signal, a right turn on red can be made after a complete stop when safe and after yielding."),
Question("Turning","A left turn on red may be permitted when turning:",
["From a one-way street onto another one-way street, after stopping and yielding, unless prohibited","From any street onto any street","Only at night","Never"],0,"The one-way-to-one-way left-on-red exception applies when permitted and safe."),
Question("Lane Use","A solid yellow line generally indicates:",
["Passing is permitted in both directions","Passing restrictions; do not cross where prohibited","A parking lane","A bike-only lane"],1,"Solid yellow markings indicate restrictions on crossing/passing depending on the marking arrangement."),
Question("Lane Use","Broken white lane lines generally separate:",
["Traffic moving in the same direction","Opposing traffic","Railway tracks","Parking stalls only"],0,"White lines generally separate lanes of traffic moving in the same direction."),
Question("Lane Use","Yellow centre lines generally separate:",
["Same-direction lanes","Opposing traffic","Parking spaces","Sidewalks"],1,"Yellow centre markings separate opposing directions of traffic."),
Question("Lane Use","Before changing lanes, you should check:",
["Only the rear-view mirror","Mirrors and the blind spot, signal, and move when safe","Only the speedometer","Only the vehicle behind"],1,"Mirror checks plus a shoulder/blind-spot check are important before changing lanes."),
Question("Lane Use","A shoulder check is especially important because:",
["Mirrors show every area beside the vehicle","Mirrors have blind spots","It increases fuel economy","It activates the signal"],1,"Blind spots are areas not fully visible in mirrors."),
Question("Speed","Unless otherwise posted, what is the typical maximum speed on an urban roadway in Alberta?",
["30 km/h","40 km/h","50 km/h","80 km/h"],2,"The commonly established urban default is 50 km/h unless posted otherwise."),
Question("Speed","You should drive at a speed that:",
["Always equals the posted maximum","Is reasonable for conditions and allows you to control the vehicle safely","Is faster than surrounding traffic","Is the same in every weather condition"],1,"The posted limit is a maximum, not a requirement to drive at that speed in all conditions."),
Question("Speed","In poor weather, the safest response is generally to:",
["Increase speed","Reduce speed and increase following distance as needed","Turn off headlights","Follow more closely"],1,"Reduced visibility/traction requires appropriate speed and spacing."),
Question("Speed","A school zone speed limit applies only if children are visible.",
["True","False","Only on weekends","Only after sunset"],1,"Do not assume a school-zone restriction depends on whether children are visible."),
Question("Speed","A playground zone is primarily intended to protect:",
["Only school buses","Children and pedestrians around playground areas","Parked vehicles","Road workers only"],1,"Playground zones are safety areas for children and pedestrians."),
Question("Following Distance","A useful minimum following-distance rule in normal conditions is:",
["1 second","2 seconds","4 seconds","10 seconds"],1,"A minimum two-second gap is a common baseline in normal conditions; increase it for poor conditions."),
Question("Following Distance","When roads are slippery, you should:",
["Decrease following distance","Increase following distance","Follow the vehicle ahead more closely","Brake later"],1,"Extra space is needed because stopping distances increase."),
Question("Parking","When parking downhill beside a curb, the front wheels should generally be turned:",
["Away from the curb","Toward the curb","Straight only","Left regardless of direction"],1,"Downhill parking beside a curb generally requires wheels turned toward the curb."),
Question("Parking","When parking uphill beside a curb, the front wheels should generally be turned:",
["Toward the curb","Away from the curb","Straight only","Randomly"],1,"Uphill beside a curb generally requires the wheels turned away from the curb."),
Question("Parking","You should never leave a vehicle unattended unless it is:",
["In gear/park with parking brake appropriately applied","Running","Unlocked","On a hill"],0,"Secure the vehicle appropriately, including the parking brake and transmission position."),
Question("Parking","Parking in front of a fire hydrant is:",
["Always permitted","Restricted/prohibited under parking rules","Required for emergencies","Allowed if hazard lights are on"],1,"Parking near fire hydrants is restricted to maintain emergency access."),
Question("Seat Belts","Who is responsible for ensuring children are properly restrained?",
["Nobody","The driver has responsibilities for passengers under applicable law","Only the child","Only the police"],1,"Drivers have legal responsibilities regarding seat-belt/child-restraint use."),
Question("Seat Belts","A seat belt should be worn:",
["Only on highways","On every trip","Only by the driver","Only at night"],1,"Seat belts should be used on every trip."),
Question("Child Safety","A child restraint should be used according to:",
["The manufacturer's instructions and applicable Alberta requirements","The child's favourite colour","Only the vehicle brand","No rules"],0,"Use an appropriate restraint and follow the applicable requirements and manufacturer's instructions."),
Question("School Bus","When a school bus has alternating flashing red lights, drivers must:",
["Pass quickly","Stop as required and remain stopped until it is safe/legal to proceed","Only slow down","Honk"],1,"Flashing red school-bus lights require drivers to stop as required by Alberta law."),
Question("School Bus","You should pass a stopped school bus with flashing red lights if you are late.",
["True","False","Only on rural roads","Only if no children are visible"],1,"Being late does not remove the legal stopping requirement."),
Question("Emergency","When approaching a stopped emergency vehicle with flashing lights, you should:",
["Ignore it","Slow down and move over when safe as required by law","Speed up","Stop beside it"],1,"Alberta's rules require drivers to slow down and move over where applicable and safe."),
Question("Emergency","If an emergency vehicle is approaching from behind, your priority is to:",
["Block the lane","Safely yield and allow it to pass","Race it to the intersection","Stop wherever you are without regard to safety"],1,"Yield safely and avoid obstructing the emergency response."),
Question("Railway","At a railway crossing with flashing signals or lowered gates, you should:",
["Cross if you don't see a train","Stop and wait until the warning ends and it is safe to cross","Drive around the gate","Follow another vehicle closely"],1,"Never go around lowered gates or ignore active warning signals."),
Question("Railway","It is safe to stop your vehicle on railway tracks if traffic is heavy.",
["True","False","Only at night","Only if hazard lights are on"],1,"Never stop on railway tracks."),
Question("Bicycles","When passing a cyclist, drivers should:",
["Give adequate space and pass only when safe/legal","Honk continuously","Pass extremely close","Force the cyclist onto the shoulder"],0,"Leave appropriate clearance and pass only when safe and lawful."),
Question("Motorcycles","Motorcycles can be hidden in a vehicle's blind spot.",
["True","False","Only in winter","Only on highways"],0,"Motorcycles are smaller and can be harder to see, especially in blind spots."),
Question("Night Driving","When approaching an oncoming vehicle at night, you should:",
["Use high beams directly into its windshield","Use appropriate low beams and avoid glare","Turn off all lights","Flash continuously"],1,"Use lighting that avoids blinding other road users."),
Question("Night Driving","If high beams from another vehicle create glare, you should:",
["Look directly at the lights","Reduce speed as needed and focus toward the right edge of your lane","Speed up","Close your eyes"],1,"Avoid staring at glare and reduce speed if visibility is affected."),
Question("Weather","Black ice is particularly dangerous because:",
["It is always visible","It can be difficult to see and can greatly reduce traction","It only occurs in summer","It increases tire grip"],1,"Black ice can be nearly invisible and significantly reduce traction."),
Question("Weather","In fog, you should generally:",
["Use appropriate low-beam headlights and reduce speed","Use high beams only","Drive faster to escape it","Turn off lights"],0,"Low beams generally provide better visibility than high beams in fog."),
Question("Weather","If your vehicle begins to skid, you should generally:",
["Stay calm, look where you want to go and steer appropriately; avoid abrupt actions","Accelerate hard","Close your eyes","Turn sharply without looking"],0,"Smooth control and looking where you want to go help recover from a skid."),
Question("Vehicle Safety","Before driving, you should:",
["Ensure windows/mirrors are clear and controls are adjusted","Adjust mirrors while moving","Ignore warning lights","Drive first and check later"],0,"Prepare the vehicle before moving."),
Question("Vehicle Safety","If your windshield is obstructed by snow or ice, you should:",
["Drive slowly anyway","Clear it before driving","Use only the wipers","Open the window instead"],1,"Clear windows, mirrors and lights before driving."),
Question("Vehicle Safety","Tire condition matters because:",
["It affects traction, steering and braking","It only affects fuel economy","It is cosmetic","It affects radio reception"],0,"Tires are critical to traction and control."),
Question("Distracted Driving","Using a hand-held phone while driving is:",
["A safe way to save time","Restricted under Alberta distracted-driving law","Required at intersections","Allowed when traffic is slow"],1,"Alberta restricts distracted driving, including prohibited hand-held device use."),
Question("Distracted Driving","Distracted driving can include:",
["Only texting","Activities that take attention away from driving","Only eating","Only using GPS"],1,"Distraction can be visual, manual or cognitive."),
Question("Impairment","Driving after consuming alcohol or drugs can:",
["Never affect driving","Impair judgement, reaction time and control","Improve concentration","Make stopping shorter"],1,"Alcohol and drugs can impair skills required for safe driving."),
Question("Impairment","If you are too tired to drive safely, the best choice is:",
["Keep driving faster","Stop driving and rest/use another safe option","Open a window and continue","Turn up music and ignore it"],1,"Fatigue is a serious safety risk."),
Question("Collisions","After a collision, you should:",
["Leave immediately","Stop and take the actions required by law and safety circumstances","Hide the vehicle","Delete evidence"],1,"Drivers have legal and safety responsibilities after collisions."),
Question("Insurance","A driver should carry the required proof of insurance when driving.",
["True","False","Only on highways","Only in another province"],0,"Carry the required documentation when driving."),
Question("Road Markings","A stop line tells a driver:",
["Where to stop for the applicable control","Where to park","Where to accelerate","Where to change tires"],0,"Stop at the marked stop line when one is present."),
Question("Road Markings","A crosswalk is primarily intended to:",
["Provide a pedestrian crossing area","Mark a parking space","Mark a passing lane","Show a speed limit"],0,"Crosswalk markings identify pedestrian crossing areas."),
Question("Intersections","Blocking an intersection because traffic ahead is stopped is:",
["Good defensive driving","Something to avoid","Required when the light is green","Allowed whenever you signal"],1,"Do not enter an intersection unless you can proceed without blocking it."),
Question("Intersections","When making a turn, you should yield to pedestrians who have the right of way.",
["True","False","Only on weekends","Only at night"],0,"Turning drivers must yield as required to pedestrians."),
Question("Expressways","When entering a freeway using an acceleration lane, you should:",
["Build speed to match traffic when safe and merge without forcing others to brake","Stop at the end of the ramp","Enter at walking speed","Drive on the shoulder"],0,"Use the acceleration lane to reach an appropriate speed and merge safely."),
Question("Expressways","When exiting a freeway, you should:",
["Slow sharply in the through lane","Move into the exit lane and decelerate as appropriate","Stop before the exit","Reverse if you miss it"],1,"Move to the exit lane and slow appropriately."),
Question("Passing","Before passing another vehicle, you should:",
["Ensure the manoeuvre is legal and safe and that you have adequate sight distance","Pass at any intersection","Assume the other driver will slow down","Use the shoulder automatically"],0,"Passing requires legality, visibility, space and safety."),
Question("Passing","Passing on a solid line is:",
["Always permitted","Restricted/prohibited where the marking indicates it is unsafe or prohibited","Required","Only allowed for motorcycles"],1,"Solid markings can prohibit crossing/passing depending on their configuration."),
Question("Construction","In a construction zone, you should:",
["Obey temporary signs, workers and traffic-control devices","Ignore temporary signs","Speed up","Pass flaggers"],0,"Temporary controls and workers must be obeyed."),
Question("Construction","A flagger's stop instruction should be:",
["Ignored if you have a green light","Followed","Followed only by trucks","Optional"],1,"Flaggers controlling traffic must be obeyed."),
Question("Pedestrians","Drivers should be especially alert for pedestrians at:",
["Crosswalks, intersections, school areas and other pedestrian activity areas","Only highways","Only parking lots","Only rural roads"],0,"Pedestrian conflicts can occur anywhere, especially at crossing/activity areas."),
Question("Safe Driving","A posted speed limit is:",
["A guaranteed safe speed for every condition","The maximum legal speed under normal conditions, subject to applicable rules","A minimum speed","Optional"],1,"Drivers must adjust speed for conditions and obey applicable limits."),
Question("Safe Driving","If visibility or road conditions deteriorate, you should:",
["Adjust speed and following distance","Maintain the same speed no matter what","Follow more closely","Turn off lights"],0,"Safe driving requires adapting to conditions."),
Question("Safe Driving","The safest driver continually:",
["Scans the roadway and anticipates hazards","Looks only at the vehicle ahead","Uses mirrors once per hour","Ignores side roads"],0,"Active scanning and hazard anticipation are core defensive-driving skills."),
Question("Signs","A 'Do Not Enter' sign means:",
["Enter only if no traffic is visible","Do not enter the roadway/area from that direction","Parking permitted","Yield"],1,"Do Not Enter prohibits entry from that direction."),
Question("Signs","A 'No U-turn' sign means:",
["U-turns are required","U-turns are prohibited where the sign applies","Only trucks may turn","U-turns are allowed at night"],1,"The sign prohibits U-turns where it applies."),
Question("Signs","A speed-limit sign indicates:",
["The maximum posted speed under the applicable conditions","A suggested minimum","The speed of the car ahead","A target you must always reach"],0,"It establishes the posted maximum, subject to applicable rules."),
Question("Signs","A 'Yield' sign requires you to:",
["Give the right of way as required and stop if necessary","Always stop for 10 seconds","Speed up","Ignore pedestrians"],0,"Yield means give the right of way; stop when necessary."),
Question("Road Sharing","Large trucks have larger blind spots than passenger cars.",
["True","False","Only when parked","Only in winter"],0,"Large vehicles can have substantial blind areas."),
Question("Road Sharing","When following a large truck, you should:",
["Leave adequate space and avoid lingering in blind spots","Follow very closely","Drive beside it indefinitely","Turn off headlights"],0,"Adequate space improves visibility and reaction time."),
Question("Road Sharing","When a vehicle is stopped for a pedestrian crossing, you should:",
["Pass it without checking","Be alert for the pedestrian and obey crossing rules","Honk and pass","Use the shoulder"],1,"A stopped vehicle may be yielding to a pedestrian you cannot yet see."),
Question("Parking","Before opening your door into traffic, you should:",
["Check for cyclists and vehicles","Open immediately","Only look at the dashboard","Honk"],0,"Check the area beside and behind the vehicle before opening a door."),
Question("Winter","Winter tires and appropriate traction equipment can:",
["Improve traction in winter conditions","Guarantee no skids","Make ice harmless","Replace safe driving"],0,"Appropriate tires improve traction but cannot eliminate winter hazards."),
Question("Winter","When approaching a slippery downhill section, you should:",
["Reduce speed before the hazard and avoid abrupt braking/steering","Accelerate hard","Brake sharply halfway down","Follow closely"],0,"Slow before the hazard and use smooth controls."),
Question("Emergency","If you see an emergency scene ahead, you should:",
["Slow appropriately, follow directions and avoid interfering","Stop to take photos in the roadway","Drive through cones","Ignore responders"],0,"Protect responders and follow traffic-control directions."),
Question("Railway","If your vehicle becomes stuck on railway tracks, you should:",
["Get everyone out and move away from the tracks, then seek emergency help","Stay inside and wait","Try to push it while seated","Wait for a train to stop"],0,"Railway emergencies require immediate evacuation away from the tracks and emergency notification."),
Question("Safe Driving","Seat belts should be fastened before the vehicle starts moving.",
["True","False","Only on highways","Only for children"],0,"Seat belts should be used before moving."),
Question("Safe Driving","A driver's responsibility includes:",
["Maintaining control and obeying traffic laws","Only avoiding police","Only protecting the vehicle","Only following other cars"],0,"Safe driving includes control, attention and compliance with traffic laws."),
]


DICEY = [
("School vs school area","You see a school sign, but there is NO maximum-speed sign attached. What is it?","School area","A school area warns that children may be walking/crossing; it is not automatically a 30 km/h school zone.","MEMORY: No speed sign = area, not zone."),
("School zone hours","On a normal school day, which standard school-zone periods apply unless local signs say otherwise?","8:00–9:30, 11:30–1:30, 3:00–4:30","These are the standard Alberta periods; municipalities may set different times and post them.","MEMORY: 8–9:30 / 11:30–1:30 / 3–4:30."),
("Playground hours","When are standard playground-zone restrictions in effect?","Every day, 8:30 a.m. to 1 hour after sunset","Unlike school zones, playground restrictions apply every day; municipal times can differ if posted.","MEMORY: PLAY = EVERY day; 8:30 → sunset + 1 hour."),
("School-zone passing","Can you pass a vehicle travelling in the same direction inside an active school zone?","No","Passing or attempting to pass another vehicle travelling in the same direction is prohibited while the school zone is in effect.","MEMORY: SCHOOL = NO PASS."),
("Playground-zone passing","Can you pass a vehicle travelling in the same direction inside an active playground zone?","No","The same no-passing rule applies while the playground speed restriction is in effect.","MEMORY: SCHOOL + PLAYGROUND = NO PASS."),
("School bus—undivided","A school bus has flashing red lights on an undivided road. You are approaching from the opposite direction. Must you stop?","Yes","On an undivided road, traffic approaching from either direction must stop as required.","MEMORY: NO MEDIAN = BOTH directions."),
("School bus—divided","A school bus is stopped on the opposite side of a divided highway with a median. Must traffic on your side stop?","Generally no","The stopping requirement applies to traffic approaching from behind the bus; a divided highway separates opposing traffic.","MEMORY: MEDIAN = separates the directions."),
("Flashing red","What does a flashing red signal require?","Complete stop, then proceed when safe","Flashing red is treated like a stop sign.","MEMORY: RED FLASH = STOP."),
("Flashing yellow","What does a flashing yellow signal require?","Proceed with caution","It warns you to approach/proceed cautiously; it is not a stop requirement.","MEMORY: YELLOW FLASH = CAUTION."),
("Right on red","Can you turn right on a red light?","Yes, after a complete stop, if permitted and safe, while yielding","A red light requires a stop. After stopping, a right turn may be made unless prohibited, and you must yield as required.","MEMORY: STOP → LOOK → YIELD → TURN."),
("Left on red","When can a left turn on red be permitted?","From one one-way street onto another one-way street, after stopping, if permitted and safe","This is a specific exception; don't generalize it to two-way streets.","MEMORY: ONE-WAY → ONE-WAY."),
("Green left turn","You have a green light and want to turn left. Do you automatically have priority?","No","You must yield to oncoming traffic and pedestrians that have the right of way.","MEMORY: GREEN ≠ GUARANTEE."),
("Uncontrolled intersection","Two vehicles arrive at approximately the same time at an uncontrolled intersection. Who generally goes first?","Vehicle on the right","The right-hand vehicle generally has priority when arrival is simultaneous.","MEMORY: SAME TIME → RIGHT."),
("Driveway exit","You are leaving a driveway and crossing a sidewalk. Who has priority?","Pedestrians and road traffic as applicable; you must stop/yield","Entering a roadway from a driveway/alley/parking area requires yielding and caution.","MEMORY: LEAVING PRIVATE SPACE = YIELD."),
("Blocked intersection","Your light is green, but traffic is stopped beyond the intersection. Should you enter and wait in the intersection?","No","Do not enter if you cannot clear the intersection without blocking it.","MEMORY: GREEN LIGHT, CLEAR EXIT."),
("Pedestrian crossing","A vehicle ahead stops at a crosswalk and you cannot see why. Can you pass it?","No—wait and make sure it is safe/legal","The stopped vehicle may be yielding to a pedestrian you cannot see.","MEMORY: STOPPED AT CROSSWALK = EXPECT A PERSON."),
("Emergency vehicle","An emergency vehicle approaches while you are already in an intersection. Should you stop in the middle?","No—clear the intersection if safe, then pull over","You should not obstruct the intersection; yield safely and pull over as required.","MEMORY: CLEAR → PULL OVER → STOP."),
("Emergency following","How close may you follow an emergency vehicle responding with lights/siren?","Do not follow within 150 metres","Alberta specifies a 150-metre restriction.","MEMORY: EMERGENCY = 150 m."),
("Hill—uphill curb","Parked uphill beside a curb. Which way should the wheels turn?","Left, away from the curb","If the vehicle rolls backward, the wheel position helps direct it toward the curb rather than traffic.","MEMORY: UP + CURB = LEFT."),
("Hill—uphill no curb","Parked uphill with no curb. Which way should the wheels turn?","Right, toward the edge of the road","Without a curb, the wheels should direct a rolling vehicle toward the road edge.","MEMORY: UP + NO CURB = RIGHT."),
("Hill—downhill","Parked downhill beside a curb. Which way should the wheels turn?","Right, toward the curb","If the vehicle rolls forward, it should roll toward the curb.","MEMORY: DOWN = RIGHT."),
("Yellow lines","What do yellow centre lines generally separate?","Opposing directions of traffic","Yellow centre markings distinguish opposing traffic flows.","MEMORY: YELLOW = OPPOSITE."),
("White lines","What do white lane lines generally separate?","Traffic moving in the same direction","White lane markings commonly separate same-direction lanes.","MEMORY: WHITE = WITH YOU."),
("Posted speed","The posted speed is 100 km/h and the road is icy. Must you drive 100?","No","The posted limit is a maximum; conditions may require a lower safe speed.","MEMORY: LIMIT = CEILING, NOT TARGET."),
("Following distance","What is the basic minimum following-distance guideline in ideal conditions?","At least 2 seconds","Increase the gap in poor conditions and for larger vehicles.","MEMORY: NORMAL = 2; BIG/POOR = MORE."),
("Large vehicle following","What following gap is recommended for a large vehicle such as a motorhome in ideal conditions?","At least 4 seconds","Large vehicles need more space and can block your view of hazards.","MEMORY: BIG = 4."),
("School sign wording","Does a school sign by itself automatically mean 30 km/h?","No","The school-zone definition requires a maximum-speed sign attached; without it, it is a school area.","MEMORY: LOOK FOR THE SPEED SIGN."),
("Playground sign wording","Does a playground sign without a maximum-speed sign automatically create a 30 km/h playground zone?","No","Without the maximum-speed sign it is a playground area; use caution.","MEMORY: NO SPEED SIGN = AREA."),
("Yellow light","You approach a yellow light and can safely stop. Should you accelerate to beat the red?","No","Yellow means the signal is changing; stop if you can do so safely.","MEMORY: YELLOW = DECIDE, NOT ACCELERATE."),
("Traffic signal failure","If traffic signals are not functioning, what should you do?","Treat the intersection as an all-way stop and proceed cautiously","This avoids assuming priority when the normal signal control is absent.","MEMORY: DEAD LIGHT = FOUR-WAY STOP."),
("Skid","Your vehicle starts to skid. Should you slam on the brakes?","No","Avoid abrupt control inputs; look where you want to go and steer appropriately for the skid.","MEMORY: SKID = SMOOTH, LOOK, STEER."),
("Fog","Why are high beams generally unsuitable in fog?","They can reflect glare back and reduce useful visibility","Use appropriate low beams and adjust speed for visibility.","MEMORY: FOG = LOW."),
("Winter windows","Can you drive if snow/ice still obstructs your windshield?","No—clear the windshield and other required areas first","Clear visibility is essential before moving.","MEMORY: CLEAR BEFORE GEAR."),
("Seat belts","Can you carry more passengers than there are seat belts because the trip is short?","No","Alberta's learner/GDL guidance includes the requirement not to exceed available seat belts.","MEMORY: ONE PERSON = ONE BELT."),
("Class 7 night restriction","Can a Class 7 learner drive between midnight and 5 a.m.?","No","Class 7 learners have a midnight-to-5 a.m. driving restriction.","MEMORY: CLASS 7 = NO 12–5."),
("Class 7 alcohol","Can a Class 7 learner have alcohol in their system while driving?","No","Learner drivers are subject to zero alcohol/drug tolerance.","MEMORY: LEARNER = ZERO."),
("Demerits GDL","At how many demerit points can a Class 5-GDL driver be suspended?","8 or more","GDL drivers have a lower demerit threshold than full Class 5 drivers.","MEMORY: GDL = 8."),
("GDL passenger rule","Can a Class 5-GDL driver have more passengers than seat belts?","No","Occupants cannot exceed available seat belts.","MEMORY: BELTS SET THE LIMIT."),
("Blind spot","If you can see a vehicle in your side mirror, is it guaranteed that the vehicle can see you?","No","Mirrors do not eliminate blind spots; shoulder checks are still needed.","MEMORY: MIRROR ≠ ALL CLEAR."),
("Truck blind spot","A truck driver can see you because you can see the truck's mirror. True or false?","False","Large vehicles have substantial blind spots.","MEMORY: SEEING THEM ≠ BEING SEEN."),
("Construction flagger","A flagger signals you to stop while your traffic light is green. What should you do?","Follow the flagger's traffic-control instruction","Temporary traffic control at a work zone must be obeyed.","MEMORY: FLAGGER = ROAD BOSS."),
("Rail crossing gate","A railway crossing gate is down but no train is visible. Can you drive around it?","No","Never drive around a lowered crossing gate.","MEMORY: GATE DOWN = STAY DOWN."),
("Rail tracks blocked","Traffic ahead is stopped and your vehicle would have to stop on railway tracks. Should you enter?","No","Never block railway tracks; wait until you can clear them.","MEMORY: TRACKS MUST STAY CLEAR."),
("Phone distraction","If traffic is stopped at a red light, can you freely use a hand-held phone?","No","Distracted-driving restrictions are not suspended simply because the vehicle is stopped in traffic.","MEMORY: RED LIGHT ≠ PHONE TIME."),
("Passing","Can you pass whenever the road looks clear, even if a sign/marking prohibits it?","No","Passing must be both safe and legal; signs and pavement markings can prohibit it.","MEMORY: SAFE + LEGAL."),
("School zone speed","If the school zone is in effect and the posted maximum is 30 km/h, can you drive 35 because no children are visible?","No","The restriction applies based on the zone/time/signage, not on whether children happen to be visible.","MEMORY: ZONE ≠ CHILD COUNT."),
("Playground speed","If the playground zone is active, can you drive 35 km/h because the road is empty?","No","The posted maximum applies while the restriction is in effect.","MEMORY: EMPTY ROAD ≠ EXTRA SPEED."),
("Right of way","Having the right of way means you never need to watch for other vehicles. True or false?","False","Right of way does not remove the duty to drive defensively and avoid collisions.","MEMORY: RIGHT OF WAY ≠ RIGHT TO CRASH."),
("Intersection turn","A green arrow allows a protected movement. Should you still watch for pedestrians?","Yes","Even with a protected movement, drivers must remain alert to applicable pedestrian controls and hazards.","MEMORY: ARROW = PROTECTED MOVEMENT, NOT BLINDNESS."),
("Roadside emergency","A stopped emergency vehicle has flashing lights. Should you maintain speed if you are in the adjacent lane?","No","Slow down and move over as required and when safe.","MEMORY: LIGHTS = SLOW + MOVE."),
("Vehicle preparation","Should you adjust mirrors and seat after starting to drive if you can do it quickly?","No","Set up the vehicle before moving; avoid distractions while driving.","MEMORY: SET BEFORE GO."),
]

# Convert to Question objects for the existing test engine.
for cat, qtext, answer_text, explanation, memory in DICEY:
    opts = [answer_text, "None of the above", "Only if another driver agrees", "Only when police are present"]
    # Make the correct answer first but randomize when shown.
    Q.append(Question("DICEY • " + cat, qtext, opts, 0, explanation + "  " + memory))

DICEY_MEMORY = [
("Traffic lights","RED = STOP","Flashing red → full stop. Yellow flash → caution."),
("School / playground","NO SPEED SIGN = AREA","Speed sign attached = zone. School and playground areas are warnings."),
("Zones","SCHOOL = SCHOOL DAYS","PLAY = EVERY DAY","Remember the different timing rules."),
("School bus","NO MEDIAN = BOTH","DIVIDED = OPPOSITE SIDE SEPARATED","Look for the median, not merely the number of lanes."),
("Turns","STOP → YIELD → TURN","Right on red is not automatic permission."),
("Intersections","SAME TIME → RIGHT","At an uncontrolled intersection, the right-hand vehicle generally goes first."),
("Hill parking","UP + CURB = LEFT","UP + NO CURB = RIGHT; DOWN = RIGHT."),
("Road lines","YELLOW = OPPOSITE","WHITE = SAME DIRECTION."),
("Following distance","2 NORMAL / 4 BIG","Increase it for poor weather and road conditions."),
("Emergency","CLEAR → PULL OVER → STOP","150 m: don't follow a responding emergency vehicle closely."),
("Winter","CLEAR → SLOW → SMOOTH","Clear windows, slow for conditions, avoid abrupt inputs."),
("Defensive driving","RIGHT OF WAY ≠ RIGHT TO CRASH","Having priority never means ignoring hazards."),
]

STATE_FILE = Path.home() / ".jass_alberta_driver_trainer.json"

class Trainer:
    def __init__(self):
        self.stats = {"attempts": 0, "passed": 0, "questions": 0, "correct": 0, "wrong": 0, "weak": {}}
        try:
            if STATE_FILE.exists():
                self.stats.update(json.loads(STATE_FILE.read_text(encoding="utf-8")))
        except Exception:
            pass
    def save(self):
        try:
            STATE_FILE.write_text(json.dumps(self.stats, indent=2), encoding="utf-8")
        except Exception:
            pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JASS Alberta Class 7 • Smart Driver Test Trainer")
        self.resize(1220, 820)
        self.trainer = Trainer()
        self.questions = Q
        self.session = []
        self.index = 0
        self.answers = []
        self.build_ui()
        self.cheat_button = QPushButton("🧠  VISUAL CHEAT SHEET")
        self.cheat_button.setToolTip("Open the visual memory cheat sheet")
        self.cheat_button.clicked.connect(self.show_visual_cheat_sheet)
        self.cheat_button.setObjectName("cheatButton")
        self.cheat_button.setMinimumHeight(42)
        self.cheat_button.setCursor(Qt.PointingHandCursor)
        # Put the button in the window's top-level layout if possible.
        central = self.centralWidget()
        if central is not None and central.layout() is not None:
            central.layout().insertWidget(0, self.cheat_button)



    def show_visual_cheat_sheet(self):
        page = self.build_visual_cheat_sheet()
        dlg = QDialog(self)
        dlg.setWindowTitle("🧠 Visual Memory Cheat Sheet")
        dlg.resize(1050, 760)
        layout = QVBoxLayout(dlg)
        layout.addWidget(page)
        dlg.exec()

    def build_visual_cheat_sheet(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        title = QLabel("🧠 VISUAL MEMORY CHEAT SHEET")
        title.setObjectName("heroTitle")
        layout.addWidget(title)

        subtitle = QLabel(
            "Quick visual cues for the Alberta Class 7 knowledge test. "
            "Remember the BIG CUE first, then the explanation."
        )
        subtitle.setObjectName("heroSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        cards = [
            ("🔴", "FLASHING RED", "STOP", "Stop completely, then proceed when safe."),
            ("🟡", "FLASHING YELLOW", "SLOW + CAUTION", "Slow down and proceed only when safe."),
            ("➡️", "SAME TIME", "RIGHT GOES FIRST", "At an uncontrolled intersection, yield to the vehicle on your right."),
            ("⬆️🅿️", "UPHILL + CURB", "WHEELS LEFT", "Turn wheels so the curb can help stop a rollback."),
            ("⬆️", "UPHILL + NO CURB", "WHEELS RIGHT", "Turn wheels away from the roadway."),
            ("⬇️", "DOWNHILL", "WHEELS RIGHT", "Turn toward the curb/edge."),
            ("🟡", "YELLOW LINE", "OPPOSITE", "Yellow centre lines separate opposing traffic."),
            ("⚪", "WHITE LINE", "SAME DIRECTION", "White lines generally separate lanes travelling the same direction."),
            ("🚸", "SCHOOL ZONE", "NO PASSING", "When active, obey the posted speed and do not pass."),
            ("🛝", "PLAYGROUND", "EVERY DAY", "Remember: playground restrictions use a daily active period."),
            ("🚌", "SCHOOL BUS", "RED = STOP", "Flashing red bus lights mean stop as required by the road configuration."),
            ("🚑", "EMERGENCY", "CLEAR → PULL OVER → STOP", "Give way and safely pull over/stop as required."),
            ("📏", "EMERGENCY", "150 m", "Do not follow within 150 m of an emergency vehicle displaying flashing lights."),
            ("⏱️", "FOLLOWING GAP", "2 sec → MORE", "Use at least 2 seconds in normal conditions; increase the gap when conditions require."),
            ("🟢", "GREEN LIGHT", "GO ≠ BLIND", "Green permits movement only when the path/intersection is clear."),
            ("↪️", "RIGHT ON RED", "STOP → CHECK → TURN", "Complete a stop first; turn only when permitted and safe."),
            ("🚶", "PEDESTRIAN", "YIELD", "Yield where required and watch carefully at crossings."),
            ("⚠️", "POSTED SPEED", "MAX ≠ TARGET", "The posted limit is not a command to drive that speed in unsafe conditions."),
            ("🚗💨", "SKID", "LOOK + STEER", "Look where you want to go and steer appropriately; avoid panic reactions."),
            ("⚠️", "RIGHT OF WAY", "NOT A CRASH RIGHT", "Priority never means you should proceed into a collision."),
        ]

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        grid = QGridLayout(content)
        grid.setContentsMargins(4, 4, 10, 10)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(12)

        for i, (icon, heading, cue, explanation) in enumerate(cards):
            card = QFrame()
            card.setObjectName("memoryCard")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(16, 14, 16, 14)
            cl.setSpacing(7)

            top = QHBoxLayout()
            ico = QLabel(icon)
            ico.setObjectName("memoryIcon")
            top.addWidget(ico)
            h = QLabel(heading)
            h.setObjectName("memoryHeading")
            top.addWidget(h, 1)
            cl.addLayout(top)

            cue_label = QLabel(cue)
            cue_label.setObjectName("memoryCue")
            cue_label.setAlignment(Qt.AlignCenter)
            cue_label.setWordWrap(True)
            cl.addWidget(cue_label)

            exp = QLabel(explanation)
            exp.setObjectName("memoryExplanation")
            exp.setWordWrap(True)
            cl.addWidget(exp)

            grid.addWidget(card, i // 2, i % 2)

        scroll.setWidget(content)
        layout.addWidget(scroll, 1)
        return page


    def build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        hero = QFrame()
        hero.setObjectName("hero")
        hl = QVBoxLayout(hero)
        title = QLabel("JASS Alberta Class 7")
        title.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        subtitle = QLabel("Smart preparation • dicey rules • memory tricks • exam-style practice")
        subtitle.setObjectName("subtitle")
        hl.addWidget(title)
        hl.addWidget(subtitle)
        layout.addWidget(hero)

        tabs = QHBoxLayout()
        b1 = QPushButton("📘 Study")
        b2 = QPushButton("🧠 Dicey Questions")
        b3 = QPushButton("📝 Mock Test")
        b4 = QPushButton("🗂 Memory Tricks")
        b5 = QPushButton("📊 Progress")
        b6 = QPushButton("🌐 Official Guide")
        b1.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        b2.clicked.connect(self.show_dicey)
        b3.clicked.connect(self.start_test)
        b4.clicked.connect(self.show_memory)
        b5.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        b6.clicked.connect(lambda: webbrowser.open(OFFICIAL_GUIDE_PAGE))
        for b in (b1,b2,b3,b4,b5,b6):
            b.setMinimumHeight(44)
            tabs.addWidget(b)
        layout.addLayout(tabs)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # Study page
        study = QWidget()
        sl = QVBoxLayout(study)
        note = QLabel(
            "<b>Important:</b> This app is a study trainer, not the official test. "
            "The Government of Alberta guide is the authoritative study source. "
            "The real Class 7 test currently has 30 questions and requires 25 correct."
        )
        note.setWordWrap(True)
        note.setStyleSheet("background:#fff4cc;padding:12px;border:1px solid #e1c45a;")
        sl.addWidget(note)
        catbox = QComboBox()
        cats = sorted(set(x.category for x in self.questions))
        catbox.addItem("All topics")
        catbox.addItems(cats)
        self.catbox = catbox
        sl.addWidget(catbox)
        self.study_list = QListWidget()
        sl.addWidget(self.study_list)
        catbox.currentTextChanged.connect(self.populate_study)
        self.populate_study("All topics")
        self.stack.addWidget(study)

        # Test page
        test = QWidget()
        tl = QVBoxLayout(test)
        top = QHBoxLayout()
        self.test_label = QLabel("No test running")
        self.progress = QProgressBar()
        self.progress.setRange(0,30)
        top.addWidget(self.test_label)
        top.addWidget(self.progress)
        tl.addLayout(top)
        self.q_label = QLabel("")
        self.q_label.setWordWrap(True)
        self.q_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        tl.addWidget(self.q_label)
        self.opts = []
        self.group = QButtonGroup(self)
        for i in range(4):
            rb = QRadioButton()
            rb.setFont(QFont("Arial", 12))
            rb.setMinimumHeight(42)
            self.group.addButton(rb, i)
            self.opts.append(rb)
            tl.addWidget(rb)
        self.feedback = QLabel("")
        self.feedback.setWordWrap(True)
        tl.addWidget(self.feedback)
        controls = QHBoxLayout()
        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.next_question)
        self.next_btn.setEnabled(False)
        self.submit_btn = QPushButton("Submit Answer")
        self.submit_btn.clicked.connect(self.submit_answer)
        self.start_btn = QPushButton("Start 30-Question Test")
        self.start_btn.clicked.connect(self.start_test)
        controls.addWidget(self.start_btn)
        controls.addWidget(self.submit_btn)
        controls.addWidget(self.next_btn)
        tl.addLayout(controls)
        self.stack.addWidget(test)

        # Dicey page
        dice = QWidget()
        dl = QVBoxLayout(dice)
        dtop = QHBoxLayout()
        dl.addWidget(QLabel("<h2>🧠 Dicey Questions</h2>"))
        self.dicey_count = QLabel()
        dtop.addWidget(self.dicey_count)
        dtop.addStretch()
        shuffle_btn = QPushButton("Shuffle")
        shuffle_btn.clicked.connect(self.show_dicey)
        dtop.addWidget(shuffle_btn)
        dl.addLayout(dtop)
        self.dice_list = QListWidget()
        self.dice_list.setAlternatingRowColors(True)
        dl.addWidget(self.dice_list)
        self.stack.addWidget(dice)
        self.dice_page_index = self.stack.count()-1

        # Memory page
        mem = QWidget()
        ml = QVBoxLayout(mem)
        ml.addWidget(QLabel("<h2>🧩 Memory Tricks</h2>"))
        self.memory_list = QListWidget()
        for item in DICEY_MEMORY:
            name, trick, explanation = item[:3]
            item = QListWidgetItem(f"{name}\n{trick}\n{explanation}")
            self.memory_list.addItem(item)
        ml.addWidget(self.memory_list)
        ml.addWidget(QLabel("Tip: learn the trigger words first, then learn the exception. The official guide remains the authority."))
        self.stack.addWidget(mem)
        self.memory_page_index = self.stack.count()-1

        # Progress page
        prog = QWidget()
        pl = QVBoxLayout(prog)
        self.progress_text = QLabel()
        self.progress_text.setWordWrap(True)
        pl.addWidget(self.progress_text)
        reset = QPushButton("Reset Progress")
        reset.clicked.connect(self.reset_progress)
        pl.addWidget(reset)
        pl.addStretch()
        self.stack.addWidget(prog)
        self.update_progress()

    def show_dicey(self):
        self.stack.setCurrentIndex(self.dice_page_index)
        self.dice_list.clear()
        items = DICEY[:]
        random.shuffle(items)
        for cat, qtext, ans, expl, mem in items:
            item = QListWidgetItem(f"⚠ {cat}\nQUESTION: {qtext}\nANSWER: {ans}\nWHY: {expl}\nMEMORY TRICK: {mem}")
            item.setSizeHint(item.sizeHint())
            self.dice_list.addItem(item)
        self.dicey_count.setText(f"{len(items)} dicey questions")

    def show_memory(self):
        self.stack.setCurrentIndex(self.memory_page_index)

    def populate_study(self, cat):
        self.study_list.clear()
        items = self.questions if cat == "All topics" else [x for x in self.questions if x.category == cat]
        for q in items:
            item = QListWidgetItem(f"[{q.category}] {q.question}\nAnswer: {q.options[q.answer]}\nWhy: {q.explanation}")
            item.setSizeHint(item.sizeHint())
            self.study_list.addItem(item)

    def start_test(self):
        self.stack.setCurrentIndex(1)
        self.session = random.sample(self.questions, 30)
        self.index = 0
        self.answers = []
        self.test_label.setText("Question 1 of 30")
        self.progress.setValue(0)
        self.feedback.setText("")
        self.submit_btn.setEnabled(True)
        self.next_btn.setEnabled(False)
        self.show_question()

    def show_question(self):
        q = self.session[self.index]
        self.q_label.setText(f"{self.index+1}. {q.question}")
        for i, rb in enumerate(self.opts):
            rb.setText(q.options[i])
            rb.setChecked(False)
            rb.setEnabled(True)
        self.feedback.setText("")
        self.submit_btn.setEnabled(True)
        self.next_btn.setEnabled(False)
        self.progress.setValue(self.index)

    def submit_answer(self):
        selected = self.group.checkedId()
        if selected < 0:
            QMessageBox.information(self, "Choose an answer", "Please select an answer first.")
            return
        q = self.session[self.index]
        correct = selected == q.answer
        self.answers.append(correct)
        self.trainer.stats["questions"] += 1
        self.trainer.stats["correct"] += int(correct)
        self.trainer.stats["wrong"] += int(not correct)
        if not correct:
            key = q.question
            self.trainer.stats["weak"][key] = self.trainer.stats["weak"].get(key, 0) + 1
        self.trainer.save()
        if correct:
            self.feedback.setText(f"<b>✓ Correct.</b> {q.explanation}")
        else:
            self.feedback.setText(f"<b>✗ Incorrect.</b> Correct answer: <b>{q.options[q.answer]}</b><br>{q.explanation}")
        for rb in self.opts:
            rb.setEnabled(False)
        self.submit_btn.setEnabled(False)
        self.next_btn.setEnabled(True)

    def next_question(self):
        if self.index >= 29:
            score = sum(self.answers)
            self.trainer.stats["attempts"] += 1
            if score >= 25:
                self.trainer.stats["passed"] += 1
            self.trainer.save()
            QMessageBox.information(
                self, "Test Complete",
                f"You scored {score}/30 ({score/30:.0%}).\n\n"
                + ("PASS level reached (25/30)." if score >= 25 else "Below the current Alberta pass threshold of 25/30. Review the explanations and try again.")
            )
            self.update_progress()
            self.stack.setCurrentIndex(2)
            return
        self.index += 1
        self.test_label.setText(f"Question {self.index+1} of 30")
        self.show_question()

    def update_progress(self):
        s = self.trainer.stats
        rate = (s["correct"]/s["questions"]*100) if s["questions"] else 0
        self.progress_text.setText(
            f"<h2>Your progress</h2>"
            f"Mock tests completed: <b>{s['attempts']}</b><br>"
            f"Mock tests at 25/30 or better: <b>{s['passed']}</b><br>"
            f"Practice questions answered: <b>{s['questions']}</b><br>"
            f"Overall practice accuracy: <b>{rate:.1f}%</b><br><br>"
            "Recommended readiness target: consistently score <b>27–30/30</b> on fresh mock tests. "
            "That is a preparation target, not a guarantee of the official result."
        )

    def reset_progress(self):
        if QMessageBox.question(self, "Reset", "Reset all saved progress?") == QMessageBox.StandardButton.Yes:
            self.trainer.stats = {"attempts":0,"passed":0,"questions":0,"correct":0,"wrong":0,"weak":{}}
            self.trainer.save()
            self.update_progress()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("JASS Alberta Class 7 Smart Driver Test Trainer")
    app.setStyleSheet("""
        QMainWindow { background: #f5f7fb; }
        QFrame#hero { background: #17324d; border-radius: 14px; padding: 10px; }
        QFrame#hero QLabel { color: white; }
        QLabel#subtitle { color: #d8e5f2; font-size: 13px; }
        QPushButton { padding: 9px 14px; border: 1px solid #c7d0da; border-radius: 8px; background: white; }
        QPushButton:hover { background: #edf4fa; }
        QListWidget { background: white; border: 1px solid #d7dee7; border-radius: 10px; padding: 8px; }
        QListWidget::item { padding: 12px; margin: 3px; }
        QRadioButton { background: white; border: 1px solid #d7dee7; border-radius: 8px; padding: 10px; }
        QRadioButton:hover { background: #eef5fb; }
        QProgressBar { border: 1px solid #c7d0da; border-radius: 7px; text-align: center; background: white; }
        QProgressBar::chunk { background: #2f6f9f; border-radius: 6px; }
    """)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
