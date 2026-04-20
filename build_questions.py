from __future__ import annotations

import json
import re
from pathlib import Path


def q(category, prompt, options, correct, explanation):
    return {
        "category": category,
        "prompt": prompt,
        "options": options,
        "correct": correct,
        "explanation": explanation,
    }


BASE_QUESTIONS = [
    q(
        "Road Signs",
        "What does a stop sign mean?",
        [
            "Come to a full stop and proceed only when it is safe",
            "Slow down only if another vehicle is close",
            "Yield without stopping",
            "Stop only for pedestrians",
        ],
        0,
        "A stop sign requires a full stop before you continue when the way is clear.",
    ),
    q(
        "Road Signs",
        "What does a yield sign tell a driver to do?",
        [
            "Come to a full stop every time",
            "Slow down and be prepared to stop if needed",
            "Speed up before entering the intersection",
            "Ignore cross traffic if no cars are visible",
        ],
        1,
        "A yield sign means reduce speed and give the right-of-way. Stop if traffic conditions require it.",
    ),
    q(
        "Road Signs",
        "What does a school crossing sign mean?",
        [
            "Pedestrians are prohibited",
            "A school crossing is ahead",
            "A playground is closed",
            "Only school buses may enter",
        ],
        1,
        "This warning sign tells drivers to watch for a school crossing ahead.",
    ),
    q(
        "Road Signs",
        "What does a railroad crossing sign warn you about?",
        [
            "A pedestrian tunnel ahead",
            "A blasting zone ahead",
            "A railroad crossing ahead",
            "A truck route ahead",
        ],
        2,
        "The sign warns that train tracks cross the roadway ahead.",
    ),
    q(
        "Road Signs",
        "What does a traffic signal ahead sign mean?",
        [
            "There is a traffic signal ahead",
            "You must stop immediately",
            "A speed camera is ahead",
            "Only turning traffic is allowed ahead",
        ],
        0,
        "This warning sign alerts you that a traffic signal is ahead.",
    ),
    q(
        "Road Signs",
        "What does a no left turn sign mean?",
        [
            "Left turns are permitted only after stopping",
            "Left turns are not allowed",
            "U-turns only are prohibited",
            "Traffic must keep left",
        ],
        1,
        "A no left turn sign means you may not make a left turn at that location.",
    ),
    q(
        "Road Signs",
        "What does a no U-turn sign mean?",
        [
            "Left turns are prohibited",
            "No stopping is allowed",
            "U-turns are prohibited",
            "A detour begins ahead",
        ],
        2,
        "This sign specifically prohibits U-turns.",
    ),
    q(
        "Road Signs",
        "What does a keep right sign mean?",
        [
            "The road becomes one-way",
            "Two-way traffic begins",
            "Drivers must keep to the right",
            "The divided highway ends",
        ],
        2,
        "Keep right signs direct traffic to pass an obstruction or median on the right side.",
    ),
    q(
        "Road Signs",
        "What does a right lane ends, keep left sign mean?",
        [
            "Merging traffic enters from the left",
            "The right lane ends, so stay left",
            "A divided highway begins",
            "Right turns are required",
        ],
        1,
        "This sign warns that the right lane ends and drivers should move left when safe.",
    ),
    q(
        "Road Signs",
        "What does a divided highway ends sign mean?",
        [
            "The roadway ahead is one way only",
            "Four lanes begin ahead",
            "A divided highway is ending",
            "Two lanes merge into one",
        ],
        2,
        "It warns that the median or divider separating traffic is ending.",
    ),
    q(
        "Road Signs",
        "What does a two-way traffic sign mean?",
        [
            "A divided highway begins",
            "Two-way traffic is ahead",
            "An intersection is ahead",
            "Four lanes of one-way traffic begin",
        ],
        1,
        "This sign warns that traffic in both directions will share the road ahead.",
    ),
    q(
        "Road Signs",
        "What does a do not enter sign prevent?",
        [
            "Entrance into a work zone only",
            "Entrance to a dead-end street only",
            "Wrong-way entrance onto one-way roads or ramps",
            "Entrance to a private driveway",
        ],
        2,
        "Do not enter signs keep drivers from entering against the proper direction of traffic.",
    ),
    q(
        "Road Signs",
        "What does a hospital sign with an arrow to the right mean?",
        [
            "A hotel is ahead on the right",
            "A hospital is ahead on the right",
            "A highway curves right",
            "A trail begins on the right",
        ],
        1,
        "It identifies hospital services in the direction shown by the arrow.",
    ),
    q(
        "Road Signs",
        "What does a hill ahead sign warn about?",
        [
            "A truck stop ahead",
            "A steep hill ahead",
            "No trucks are allowed",
            "An emergency ramp ahead",
        ],
        1,
        "The sign warns drivers about an upcoming hill grade.",
    ),
    q(
        "Road Signs",
        "What does a slippery when wet sign mean?",
        [
            "The road may be slippery when wet",
            "You are approaching a bridge",
            "Do not drive after drinking",
            "Chains are required ahead",
        ],
        0,
        "It warns that pavement traction is reduced when the road is wet.",
    ),
    q(
        "Road Signs",
        "What does a merging traffic from the right sign mean?",
        [
            "Traffic must turn right ahead",
            "Traffic will merge in from the right",
            "The right lane is closed permanently",
            "Only right turns are allowed",
        ],
        1,
        "This sign warns that vehicles will be entering your lane from the right.",
    ),
    q(
        "Road Signs",
        "A rectangular sign is usually what kind of sign?",
        [
            "A speed limit or other regulation sign",
            "A railroad crossing warning sign",
            "A stop sign",
            "A hazard marker only for construction",
        ],
        0,
        "Regulation signs are normally rectangular, including speed limit signs.",
    ),
    q(
        "Road Signs",
        "A diamond-shaped sign is usually what type of sign?",
        [
            "A destination sign",
            "A road hazard or warning sign",
            "A service sign",
            "A school bus sign only",
        ],
        1,
        "Warning signs are normally diamond-shaped.",
    ),
    q(
        "Road Signs",
        "What colors are used on signs that tell you the distance to the next highway exit?",
        [
            "Red with white letters",
            "Yellow with black letters",
            "Green with white letters",
            "Black with white letters",
        ],
        2,
        "Destination signs, including exit information signs, are green with white lettering.",
    ),
    q(
        "Road Signs",
        "What colors are used on most warning signs that show hazards ahead?",
        [
            "Black letters or symbols on yellow",
            "White letters on blue",
            "White letters on green",
            "Black letters on white",
        ],
        0,
        "Warning signs are usually yellow with black letters or symbols.",
    ),
    q(
        "Road Signs",
        "What colors are used on a typical work zone sign?",
        [
            "White with red letters",
            "Blue with white letters",
            "Orange with black letters",
            "Green with white letters",
        ],
        2,
        "Work zone warning signs are orange with black lettering or symbols.",
    ),
    q(
        "Road Signs",
        "What colors are used on most service signs?",
        [
            "Blue with white letters",
            "Yellow with black letters",
            "Green with white letters",
            "Red with white letters",
        ],
        0,
        "Service signs, such as hospital or gas information signs, are blue with white letters.",
    ),
    q(
        "Traffic Control",
        "You come to an intersection with a flashing red light. What should you do?",
        [
            "Slow down and proceed if the road looks clear",
            "Come to a full stop, then go when safe",
            "Stop only if another vehicle is already in the intersection",
            "Treat it like a green light",
        ],
        1,
        "A flashing red light is treated like a stop sign.",
    ),
    q(
        "Traffic Control",
        "What does a flashing yellow light mean?",
        [
            "Come to a full stop",
            "Proceed with caution",
            "Yield only to pedestrians",
            "Emergency vehicles only",
        ],
        1,
        "A flashing yellow light warns you to slow down and proceed carefully.",
    ),
    q(
        "Traffic Control",
        "What does a traffic light showing a green arrow and a red light mean?",
        [
            "You may only drive in the direction of the green arrow",
            "You must wait for a full green light",
            "You may go straight only",
            "All traffic must stop",
        ],
        0,
        "The green arrow permits movement only in the arrow's direction despite the red light for other movements.",
    ),
    q(
        "Traffic Control",
        "Which must you obey over a stop sign, flashing red light, or steady red light?",
        [
            "A police officer",
            "A stop sign",
            "A flashing red light",
            "A steady red light",
        ],
        0,
        "Directions from a police officer take priority over signs and signals.",
    ),
    q(
        "Traffic Control",
        "If an intersection has a stop sign and a crosswalk but no stop line, where must you stop?",
        [
            "With your front wheels in the crosswalk",
            "At the center of the intersection",
            "Before the crosswalk",
            "Fifty feet before the intersection",
        ],
        2,
        "Without a stop line, you must stop before entering the crosswalk.",
    ),
    q(
        "Traffic Control",
        "When may you cross a single broken white or yellow line?",
        [
            "Only when doing so will not interfere with traffic",
            "Only at an intersection",
            "Never",
            "Only to pass on a curve",
        ],
        0,
        "A broken line may be crossed when it is safe and legal to do so.",
    ),
    q(
        "Traffic Control",
        "When may you cross a single solid white line on the highway?",
        [
            "Whenever you want to change lanes",
            "Only to make a U-turn",
            "If traffic conditions require it",
            "Never under any circumstances",
        ],
        2,
        "Single solid white lines discourage lane changes, but the line may be crossed when traffic conditions require it.",
    ),
    q(
        "Traffic Control",
        "If the road has a solid yellow line and a broken yellow line on your side, when may you pass?",
        [
            "Only at an intersection",
            "Only in an emergency",
            "If traffic is clear",
            "Never",
        ],
        2,
        "A broken yellow line on your side means passing is allowed if the way is clear.",
    ),
    q(
        "Traffic Control",
        "When may you cross a double solid yellow line?",
        [
            "To pass a slow vehicle",
            "To turn into a driveway",
            "Whenever there is no oncoming traffic",
            "Only during daylight hours",
        ],
        1,
        "Double solid yellow lines cannot be crossed to pass, but you may cross them to enter a driveway.",
    ),
    q(
        "Traffic Control",
        "A solid white line on the right edge of the roadway slants toward the left. What does that show?",
        [
            "An intersection is just ahead",
            "You must turn left soon",
            "The road will get narrower",
            "A construction detour begins",
        ],
        2,
        "That pavement marking shows the roadway is narrowing.",
    ),
    q(
        "Traffic Control",
        "What is used on some roads to direct drivers into the correct turning lanes?",
        [
            "Flashing yellow lights",
            "White arrows painted in the lanes",
            "Red edge lines",
            "Reflective posts only",
        ],
        1,
        "Lane-use arrows painted on the roadway show which turns or movements are allowed from each lane.",
    ),
    q(
        "Traffic Control",
        "As you near an intersection, the light changes from green to yellow. What is your best action?",
        [
            "Speed up to beat the red light",
            "Prepare to stop before the intersection",
            "Stop in the middle of the intersection",
            "Drive through without checking traffic",
        ],
        1,
        "A steady yellow means the signal is about to turn red, so you should prepare to stop safely.",
    ),
    q(
        "Intersections and Turns",
        "When you want to make a right turn, where should your vehicle be before the turn?",
        [
            "Near the center of the street",
            "Close to the right side of the street",
            "Close to the left side of the street",
            "Past the center of the intersection",
        ],
        1,
        "For a right turn, position the vehicle near the right curb or right edge of the roadway.",
    ),
    q(
        "Intersections and Turns",
        "You are waiting in an intersection to complete a left turn. How should you keep your wheels?",
        [
            "Turned left",
            "Turned right",
            "Straight",
            "Pointed toward the curb",
        ],
        2,
        "Keeping your wheels straight helps prevent being pushed into oncoming traffic if you are hit from behind.",
    ),
    q(
        "Intersections and Turns",
        "You come to an intersection that is blocked by traffic. What should you do?",
        [
            "Enter slowly and wait inside the intersection",
            "Stay out of the intersection until you can pass through it",
            "Use your horn so traffic moves",
            "Follow the car ahead as closely as possible",
        ],
        1,
        "Do not enter a blocked intersection. Wait until there is room to clear it completely.",
    ),
    q(
        "Intersections and Turns",
        "You must yield the right-of-way to an approaching vehicle when you are doing what?",
        [
            "Turning left",
            "Already in a traffic circle",
            "Already in the intersection",
            "Going straight through a green light",
        ],
        0,
        "Drivers turning left must yield to oncoming traffic going straight or turning right.",
    ),
    q(
        "Intersections and Turns",
        "You hear a siren but cannot yet see the emergency vehicle. What should you do?",
        [
            "Keep driving until you can see it",
            "Pull to the curb and look to see if it is on your street",
            "Speed up and turn away from it",
            "Stop in the center lane",
        ],
        1,
        "Pull to the right and stop so you can locate the emergency vehicle and yield safely.",
    ),
    q(
        "Intersections and Turns",
        "You are making a left turn from a two-way street into a one-way street. Which lane should you enter?",
        [
            "The right lane",
            "The center lane",
            "The left lane",
            "Any lane with the least traffic",
        ],
        2,
        "A left turn into a one-way street should end in the left lane of that street.",
    ),
    q(
        "Intersections and Turns",
        "When do you have the right-of-way in a traffic circle?",
        [
            "When you are entering it",
            "When you are already in it",
            "Only if you are turning right",
            "Only if you honk first",
        ],
        1,
        "Vehicles already in the traffic circle have the right-of-way.",
    ),
    q(
        "Intersections and Turns",
        "What must you do when entering a roadway from a private road or driveway?",
        [
            "Merge quickly so traffic does not slow down",
            "Yield the right-of-way to pedestrians and roadway traffic",
            "Stop partly in the roadway so others can see you",
            "Sound your horn and pull out",
        ],
        1,
        "Drivers entering from private roads must yield to all pedestrians and traffic on the roadway.",
    ),
    q(
        "Intersections and Turns",
        "You want to turn left at a green light, but oncoming traffic is heavy. What should you do?",
        [
            "Take the right-of-way because your light is green",
            "Wait at the crosswalk",
            "Wait in the center of the intersection until traffic clears",
            "Use the shoulder to go around oncoming cars",
        ],
        2,
        "You may enter the intersection and wait to turn left when the light is green, as long as you yield to oncoming traffic.",
    ),
    q(
        "Intersections and Turns",
        "How far before a turn or lane change does New York law require you to signal?",
        [
            "At least 50 feet",
            "At least 75 feet",
            "At least 100 feet",
            "At least 200 feet",
        ],
        2,
        "New York requires a signal at least 100 feet before a turn or lane change.",
    ),
    q(
        "Intersections and Turns",
        "When two vehicles enter an intersection from different roads at the same time, which one must yield?",
        [
            "The vehicle on the right",
            "Neither vehicle",
            "The vehicle on the left",
            "The larger vehicle",
        ],
        2,
        "At the same time, the driver on the left yields to the driver on the right.",
    ),
    q(
        "Intersections and Turns",
        "What should you do when you see an emergency vehicle parked with emergency or hazard lights activated on a highway or parkway?",
        [
            "Maintain your speed and lane",
            "Move out of the lane closest to the vehicle if you can do so safely",
            "Make a U-turn to avoid it",
            "Stop behind it with hazard flashers on",
        ],
        1,
        "New York's Move Over Law requires drivers to move over when possible or slow down when approaching stopped emergency or hazard vehicles.",
    ),
    q(
        "Intersections and Turns",
        "Which vehicles require you to pull over and stop when they are responding to an emergency?",
        [
            "Vehicles displaying blue, green, or amber lights only",
            "Authorized emergency vehicles",
            "All stopped school buses",
            "Any tow truck",
        ],
        1,
        "You must yield by pulling over and stopping for authorized emergency vehicles using sirens or lights.",
    ),
    q(
        "Intersections and Turns",
        "What is the name of the law that requires drivers to use care around stopped emergency or hazard vehicles with activated lights?",
        [
            "Right-of-Way Law",
            "Move Over Law",
            "Green Light Law",
            "Brianna's Law",
        ],
        1,
        "The Move Over Law requires drivers to move over when possible or slow down around stopped emergency and hazard vehicles.",
    ),
    q(
        "Intersections and Turns",
        "A driver approaching an intersection must yield the right-of-way to what traffic?",
        [
            "Traffic that is already in the intersection",
            "Only vehicles on the left",
            "Only vehicles making right turns",
            "Traffic that arrives later",
        ],
        0,
        "Drivers must yield to vehicles already in the intersection.",
    ),
    q(
        "Passing",
        "After passing another vehicle, when should you return to the right lane?",
        [
            "As soon as your turn signal is on",
            "When you can see the front bumper of the other vehicle in your mirror",
            "When the other driver flashes headlights",
            "Immediately after moving ahead of its hood",
        ],
        1,
        "Wait until you can see the front bumper of the passed vehicle in your mirror before moving back right.",
    ),
    q(
        "Passing",
        "In which situation is passing always forbidden?",
        [
            "When the vehicle ahead is turning left",
            "When the vehicle ahead is stopped for a pedestrian in a crosswalk",
            "On a one-way street with two lanes",
            "When the vehicle ahead is parking at the curb",
        ],
        1,
        "You may never pass a vehicle that is stopped for a pedestrian in a crosswalk.",
    ),
    q(
        "Passing",
        "When may you pass another vehicle on the right?",
        [
            "When it is waiting to turn left",
            "Whenever you are in a hurry",
            "Only on curves",
            "Only if you honk first",
        ],
        0,
        "Passing on the right is permitted in limited cases, such as when the other vehicle is waiting to turn left.",
    ),
    q(
        "Passing",
        "On a three-lane expressway, another driver begins passing you on the right. When is that action allowed?",
        [
            "Never",
            "Only if that driver uses a horn",
            "As long as no signs forbid passing on the right",
            "Only if you slow to a stop",
        ],
        2,
        "Passing on the right can be legal on multi-lane roads if signs do not prohibit it and it is done safely.",
    ),
    q(
        "Passing",
        "What does it mean when a school bus is stopped and its red lights are flashing?",
        [
            "You may pass if no children are in the roadway",
            "You may not pass while the red lights are flashing",
            "You may pass if you are approaching from the front",
            "You may pass if traffic behind you is heavy",
        ],
        1,
        "Red flashing school bus lights mean traffic must stop and may not pass until the lights stop flashing.",
    ),
    q(
        "Passing",
        "When you want to overtake and pass another vehicle, what should you do first?",
        [
            "Stay close behind it to shorten the pass",
            "Signal and pass only when it is safe",
            "Wait for the other driver to wave you around",
            "Change lanes suddenly so the driver notices you",
        ],
        1,
        "Check mirrors, signal, and pass only when the road is clear and legal.",
    ),
    q(
        "Passing",
        "In general, on which side should you pass vehicles moving in the same direction?",
        [
            "On the shoulder",
            "On the right",
            "On the left",
            "On either side",
        ],
        2,
        "The normal rule is to pass on the left.",
    ),
    q(
        "Passing",
        "The vehicle behind you begins to pass. What should you do?",
        [
            "Maintain speed and honk",
            "Slow slightly and stay in your lane",
            "Move left to block the pass",
            "Speed up so traffic keeps moving",
        ],
        1,
        "Help the passing driver by staying in your lane and slowing slightly if needed.",
    ),
    q(
        "Parking",
        "In a parking space reserved for people with disabilities, a non-disabled driver may do what?",
        [
            "Park only in an emergency",
            "Stop briefly to unload packages",
            "Neither park, stop, nor stand there",
            "Stand there if staying in the vehicle",
        ],
        2,
        "Reserved disabled spaces may not be used by drivers without the proper permit or plates transporting the eligible person.",
    ),
    q(
        "Parking",
        "Before leaving a parking space parallel to the curb, how should you check for traffic?",
        [
            "Use only the inside mirror",
            "Sound your horn",
            "Turn your head and look for traffic",
            "Use your flashers first",
        ],
        2,
        "Turning your head helps you check blind spots before pulling out.",
    ),
    q(
        "Parking",
        "What does a no stopping sign mean?",
        [
            "You may stop briefly to discharge passengers",
            "You may stop only to obey traffic, a signal, an officer, or avoid conflict",
            "You may stop for less than five minutes",
            "You may stop to unload packages",
        ],
        1,
        "A no stopping zone allows stopping only for legal necessity or to avoid danger.",
    ),
    q(
        "Parking",
        "When may a vehicle use disabled parking plates or a disabled parking permit to park in a reserved space?",
        [
            "Any time the driver has the permit in the glove box",
            "Only when the disabled person connected to the permit or registration is being transported",
            "Whenever a family member is disabled",
            "Only on weekdays",
        ],
        1,
        "Reserved parking is allowed only when the person who qualifies for the permit or plates is being transported.",
    ),
    q(
        "Parking",
        "After parallel parking on a level street between two cars, what should you do with the front wheels?",
        [
            "Leave them turned toward the curb",
            "Straighten them and leave room between cars",
            "Turn them away from the curb",
            "Turn them sharply left",
        ],
        1,
        "After parking on a level street, straighten the wheels and leave space from the cars ahead and behind.",
    ),
    q(
        "Parking",
        "Where may you never park?",
        [
            "On a one-way street",
            "At the entrance to a building",
            "In a crosswalk",
            "On the right side of the road",
        ],
        2,
        "Parking in a crosswalk is always illegal.",
    ),
    q(
        "Parking",
        "What does a no parking sign mean?",
        [
            "You may never stop there for any reason",
            "You may stop temporarily to load or unload passengers or merchandise",
            "You may leave the vehicle for less than five minutes",
            "You may park if the driver stays inside",
        ],
        1,
        "No parking still allows a temporary stop to load or unload passengers or merchandise.",
    ),
    q(
        "Parking",
        "When may you get out of a car on the traffic side if you are parked parallel to the curb?",
        [
            "Only during daylight hours",
            "Only after using four-way flashers",
            "When doing so will not interfere with traffic",
            "Only when the nearest light turns red",
        ],
        2,
        "You may exit on the traffic side only when it will not interfere with other road users.",
    ),
    q(
        "Parking",
        "What does a no standing sign mean?",
        [
            "You may stop to load or unload merchandise",
            "You may stop only temporarily to pick up or discharge passengers",
            "You may never stop under any circumstances",
            "You may park if you stay in the car",
        ],
        1,
        "No standing allows a temporary stop only to pick up or drop off passengers.",
    ),
    q(
        "Parking",
        "How close may you park to a fire hydrant in New York?",
        [
            "No closer than 15 feet",
            "No closer than 10 feet",
            "No closer than 20 feet",
            "No closer than 25 feet",
        ],
        0,
        "State rules prohibit parking within 15 feet of a fire hydrant.",
    ),
    q(
        "Defensive Driving",
        "A safe speed for your vehicle depends mainly on what?",
        [
            "The posted speed limit only",
            "The driver's confidence",
            "The weather and road conditions",
            "How quickly your car accelerates",
        ],
        2,
        "A safe speed depends on conditions, even when the posted speed limit is higher.",
    ),
    q(
        "Defensive Driving",
        "Which statement is always true about road rage?",
        [
            "There is nothing you can do to prevent it",
            "Only violent people experience it",
            "You should remain polite to aggressive drivers",
            "You should hold your lane at all costs",
        ],
        2,
        "Staying calm and not escalating a situation is the safest response.",
    ),
    q(
        "Defensive Driving",
        "Seat belts work best when they are worn by whom?",
        [
            "The driver only",
            "Passengers only on expressways",
            "All occupants every time they are in the car",
            "Only people sitting in front",
        ],
        2,
        "Seat belts protect drivers and passengers best when everyone wears them every trip.",
    ),
    q(
        "Defensive Driving",
        "A lane closed ahead sign warns of a work zone. What should you do?",
        [
            "Merge into the correct lane when it is safe",
            "Drive to the end of the closed lane before looking",
            "Speed up and force your way in",
            "Ignore the sign until you see workers",
        ],
        0,
        "Merge safely when warned that a lane is closing rather than waiting until the last second.",
    ),
    q(
        "Defensive Driving",
        "What are minimum speed signs designed to do?",
        [
            "Show road conditions",
            "Keep traffic flowing smoothly",
            "Protect only pedestrians",
            "Test future traffic signal needs",
        ],
        1,
        "Minimum speed signs help maintain safe traffic flow by discouraging very slow travel.",
    ),
    q(
        "Defensive Driving",
        "Driving in a state of rage can do what?",
        [
            "Affect your judgment, raise crash risk, and lead to license consequences",
            "Improve alertness",
            "Help you respond more quickly",
            "Reduce the chance of a collision",
        ],
        0,
        "Road rage harms judgment, increases crash risk, and can result in legal penalties.",
    ),
    q(
        "Defensive Driving",
        "One rule of defensive driving is to do what with your eyes?",
        [
            "Focus only on the vehicle ahead",
            "Stay alert and keep your eyes moving",
            "Look straight ahead only",
            "Check mirrors only when turning",
        ],
        1,
        "Scanning ahead, to the sides, and in mirrors helps you spot problems early.",
    ),
    q(
        "Defensive Driving",
        "On long trips, what helps prevent drowsiness?",
        [
            "Driving faster",
            "Turning the radio up",
            "Stopping at regular intervals for rest",
            "Opening a window instead of resting",
        ],
        2,
        "Regular breaks are an effective way to reduce fatigue on long drives.",
    ),
    q(
        "Defensive Driving",
        "On a New York highway with no posted speed limit, what is the fastest legal speed?",
        [
            "50 mph",
            "55 mph",
            "60 mph",
            "65 mph",
        ],
        1,
        "When no lower speed is posted, the general maximum speed is 55 mph.",
    ),
    q(
        "Defensive Driving",
        "What is true of work zones?",
        [
            "They are dangerous only at night",
            "Rear-end collisions are the most common crash there",
            "They are always stationary and easy to avoid",
            "Speeding fines never change there",
        ],
        1,
        "Rear-end crashes are common in work zones because traffic often slows or stops unexpectedly.",
    ),
    q(
        "Alcohol and Drugs",
        "Drivers under the influence of alcohol are whose problem?",
        [
            "Only the drinker's problem",
            "Only a police enforcement problem",
            "Every driver's problem",
            "Not a major issue in New York",
        ],
        2,
        "Impaired driving puts everyone on the road at risk.",
    ),
    q(
        "Alcohol and Drugs",
        "What can happen when alcohol and another drug are combined in your blood?",
        [
            "The effects of both may increase",
            "The alcohol is canceled out",
            "Driving ability is unchanged",
            "The drug becomes harmless",
        ],
        0,
        "Alcohol and other drugs can intensify each other's effects and make driving more dangerous.",
    ),
    q(
        "Alcohol and Drugs",
        "What effect can drinking alcohol while taking prescription or over-the-counter medicine have?",
        [
            "It can multiply the effects of the alcohol",
            "It always makes you more alert",
            "It reduces the effect of the medicine only",
            "It has no effect because they are different substances",
        ],
        0,
        "Alcohol can interact with medicines and worsen impairment.",
    ),
    q(
        "Alcohol and Drugs",
        "Which factors influence the effects of alcohol on a person?",
        [
            "The amount of food in the stomach, body weight, and time between drinks",
            "Only the type of alcohol consumed",
            "Only how physically fit the person is",
            "Only the weather",
        ],
        0,
        "Food, body weight, and the time between drinks all affect BAC and impairment.",
    ),
    q(
        "Alcohol and Drugs",
        "Blood alcohol content does not depend on which of the following?",
        [
            "Your body weight",
            "How much you drink",
            "How much time passes between drinks",
            "How physically fit you are",
        ],
        3,
        "Physical fitness does not lower BAC.",
    ),
    q(
        "Alcohol and Drugs",
        "What is the only effective way to reduce your BAC?",
        [
            "Exercise",
            "Drink coffee",
            "Take a cold shower",
            "Allow time for your body to remove the alcohol",
        ],
        3,
        "Only time lowers BAC. Coffee, showers, and exercise do not make you sober.",
    ),
    q(
        "Alcohol and Drugs",
        "Which of these does not happen after drinking alcohol?",
        [
            "Reaction time slows",
            "Judgment of distance is distorted",
            "You become calmer so you can concentrate better",
            "You are less alert",
        ],
        2,
        "Alcohol does not improve concentration. It impairs judgment and alertness.",
    ),
    q(
        "Alcohol and Drugs",
        "If you drink socially, what is the best way to help ensure safe driving?",
        [
            "Take a cold shower before driving",
            "Ride home with a sober friend",
            "Stop drinking 30 minutes before leaving",
            "Drink coffee before driving",
        ],
        1,
        "The safest choice is not to drive after drinking and instead ride with someone sober.",
    ),
    q(
        "Alcohol and Drugs",
        "What should a driver do before driving after taking a non-prescription drug?",
        [
            "Read the label",
            "Drive only in daylight",
            "Drink coffee first",
            "Assume it is safe because it was bought without a prescription",
        ],
        0,
        "Many over-the-counter medicines can impair driving, so always check the label.",
    ),
    q(
        "Alcohol and Drugs",
        "What happens to your driver license if you refuse a chemical test after arrest?",
        [
            "Nothing happens unless you are convicted later",
            "You cannot be arrested",
            "Your license can be taken away",
            "You automatically win the case",
        ],
        2,
        "Under implied consent rules, refusing a chemical test can cause suspension or revocation.",
    ),
    q(
        "Alcohol and Drugs",
        "Drinking alcohol and driving is what kind of traffic safety problem?",
        [
            "A minor problem",
            "A serious problem",
            "Safe if only a few drinks were consumed",
            "Dangerous only to the drinking driver",
        ],
        1,
        "Alcohol-impaired driving is a major and serious traffic safety problem.",
    ),
    q(
        "Alcohol and Drugs",
        "What effect does coffee have on BAC after drinking alcohol?",
        [
            "It lowers BAC",
            "It cancels the alcohol",
            "It has no effect on BAC",
            "It increases BAC",
        ],
        2,
        "Coffee may make you feel more awake, but it does not reduce BAC.",
    ),
    q(
        "Alcohol and Drugs",
        "Which driving-related abilities does alcohol affect?",
        [
            "Only reaction time",
            "Only judgment of distances",
            "Only recovery from headlight glare",
            "All of these abilities",
        ],
        3,
        "Alcohol affects glare recovery, reaction time, and distance judgment.",
    ),
    q(
        "Alcohol and Drugs",
        "In New York, what BAC is evidence of intoxication?",
        [
            "0.03%",
            "0.05%",
            "0.08%",
            "0.10%",
        ],
        2,
        "A BAC of 0.08% or higher is evidence of intoxication for DWI.",
    ),
    q(
        "Alcohol and Drugs",
        "Which kinds of drugs other than alcohol can affect driving ability?",
        [
            "Only illegal drugs",
            "Allergy medicine, marijuana, and cold remedies",
            "Only prescription sleeping pills",
            "Only pain medicine",
        ],
        1,
        "Many legal and illegal drugs can impair driving, including cold remedies, allergy medicine, and marijuana.",
    ),
    q(
        "Alcohol and Drugs",
        "Which statement about BAC is true?",
        [
            "Physical fitness lowers BAC quickly",
            "A breath test is one way to measure BAC",
            "Coffee or a cold shower lowers BAC",
            "A chemical test is always required for a conviction",
        ],
        1,
        "Breath, blood, urine, or saliva tests can measure BAC.",
    ),
    q(
        "Alcohol and Drugs",
        "On average, how long does it take the human body to dispose of the alcohol in about 12 ounces of beer?",
        [
            "About one hour",
            "About five minutes",
            "About five hours",
            "About one day",
        ],
        0,
        "On average, the body removes about the alcohol in one 12-ounce beer in about an hour.",
    ),
    q(
        "Alcohol and Drugs",
        "A chemical test is used to measure what?",
        [
            "Reaction time",
            "Driving skill",
            "Blood alcohol content",
            "Eyesight",
        ],
        2,
        "Chemical tests measure the amount of alcohol in your body, usually reported as BAC.",
    ),
    q(
        "Alcohol and Drugs",
        "What can result from driving under the influence of alcohol or other drugs?",
        [
            "Possible jail time, fines, and driver license revocation",
            "Only a warning on the first offense",
            "Only higher insurance rates",
            "No consequences if no crash occurs",
        ],
        0,
        "Alcohol- and drug-related driving offenses can lead to fines, jail, and loss of license.",
    ),
    q(
        "Alcohol and Drugs",
        "What does alcohol do to driving skills and judgment?",
        [
            "It helps both",
            "It harms both",
            "It harms judgment only",
            "It harms driving skill only",
        ],
        1,
        "Alcohol impairs both the physical and mental abilities needed for safe driving.",
    ),
    q(
        "Special Driving Conditions",
        "You are entering a highway with a very short entrance lane. What is the safest way to enter traffic?",
        [
            "Use as much of the ramp as possible to reach cruising speed",
            "Stop at the end of the ramp and wait for a gap",
            "Drive onto the shoulder until you can merge",
            "Use the left lane of the highway to gain speed",
        ],
        0,
        "Use the acceleration lane or ramp to get close to highway speed before merging.",
    ),
    q(
        "Special Driving Conditions",
        "When attempting to stop on a slippery road, what is the best action?",
        [
            "Apply the brakes quickly and firmly",
            "Shift into neutral and coast",
            "Apply the brakes in slow, steady strokes",
            "Turn the wheel sharply to the shoulder",
        ],
        2,
        "Gentle, steady braking helps maintain traction on slippery surfaces.",
    ),
    q(
        "Special Driving Conditions",
        "You have just left an expressway and are beginning to drive on an ordinary highway. What should you do?",
        [
            "Check your speedometer to keep at the lower speed limit",
            "Stay at expressway speed until traffic forces you to slow",
            "Check tire pressure immediately",
            "Double your following distance regardless of traffic",
        ],
        0,
        "Drivers often continue too fast after leaving an expressway, so check your speed.",
    ),
    q(
        "Special Driving Conditions",
        "What should you do at a railroad crossing that has no signals or gates?",
        [
            "Always stop completely",
            "Slow down and be prepared to stop",
            "Increase speed to cross quickly",
            "Assume no train is coming",
        ],
        1,
        "You should slow down, look, listen, and be ready to stop for a train.",
    ),
    q(
        "Special Driving Conditions",
        "If traffic prevents you from crossing all the way over railroad tracks, when may you proceed?",
        [
            "When at least half of your vehicle can clear the tracks",
            "When no train is visible",
            "Only when there is room for your vehicle on the other side",
            "When the driver behind you honks",
        ],
        2,
        "Never enter a railroad crossing unless you can clear the tracks completely.",
    ),
    q(
        "Special Driving Conditions",
        "When driving in heavy fog during daylight, which headlights should you use?",
        [
            "No headlights",
            "Parking lights only",
            "High beams",
            "Low beams",
        ],
        3,
        "Low beams reduce glare reflected by fog better than high beams.",
    ),
    q(
        "Special Driving Conditions",
        "Your car begins to skid on a slippery road. Which way should you steer?",
        [
            "Toward the side of the road",
            "In the direction you want the front wheels to go",
            "The opposite way from the skid",
            "Back and forth quickly",
        ],
        1,
        "Steering in the direction you want the front wheels to travel helps regain control.",
    ),
    q(
        "Special Driving Conditions",
        "Why is expressway driving different from driving on an ordinary street?",
        [
            "Trucks always travel slower there",
            "You must think faster and handle your vehicle more effectively",
            "There are no blind spots on expressways",
            "There is less need to plan ahead",
        ],
        1,
        "Higher speeds leave less time to react, so expressway driving requires quicker judgment and control.",
    ),
    q(
        "Special Driving Conditions",
        "Why do expressways have acceleration lanes?",
        [
            "To test your brakes",
            "To stop and wait for an opening",
            "To reach proper speed before blending with traffic",
            "To pass vehicles on the right",
        ],
        2,
        "Acceleration lanes let drivers speed up and merge more safely.",
    ),
    q(
        "Special Driving Conditions",
        "If a tire blows out while you are driving, what should you do first?",
        [
            "Brake hard immediately",
            "Hold the steering wheel firmly and ease off the gas",
            "Shift into neutral and stop in your lane",
            "Turn sharply toward the shoulder",
        ],
        1,
        "A blowout should be handled by maintaining control and letting the vehicle slow gradually.",
    ),
    q(
        "Special Driving Conditions",
        "May you ever drive around or under a railroad crossing gate that is being lowered or raised?",
        [
            "Yes, if no train is close",
            "Yes, if the gate is high enough",
            "Only if traffic is heavy",
            "No, under no circumstances",
        ],
        3,
        "Driving around or under crossing gates is never allowed.",
    ),
    q(
        "Special Driving Conditions",
        "If your brake pedal suddenly sinks to the floor, what should you try first?",
        [
            "Pump the pedal to build pressure",
            "Turn off the engine",
            "Hook your toe under the pedal",
            "Use the parking brake hard right away",
        ],
        0,
        "Pumping the brake pedal may restore enough pressure to slow or stop the vehicle.",
    ),
    q(
        "Special Driving Conditions",
        "Your right wheels run onto a soft shoulder. What is the best way to get back on the highway?",
        [
            "Brake hard and steer sharply left",
            "Ease off the gas and brake gently",
            "Turn left hard, then right hard",
            "Stop completely on the shoulder first",
        ],
        1,
        "Slow down gently and return to the pavement carefully to avoid a skid.",
    ),
    q(
        "Special Driving Conditions",
        "When should you begin using your turn signal before leaving an expressway?",
        [
            "As soon as you enter the exit lane",
            "At least 100 feet before the exit ramp",
            "Only when you see cars behind you",
            "Just before the ramp begins",
        ],
        1,
        "Signal early so other drivers know you are preparing to leave the expressway.",
    ),
    q(
        "Special Driving Conditions",
        "At night, how can you reduce glare from the headlights of an approaching vehicle?",
        [
            "Look directly at the headlights",
            "Turn on your interior light",
            "Look toward the lower right side of your lane",
            "Wear dark sunglasses",
        ],
        2,
        "Looking toward the right edge of your lane helps avoid being blinded by glare.",
    ),
    q(
        "Special Driving Conditions",
        "Why is night driving more dangerous than daytime driving?",
        [
            "There are always more cars on the road",
            "The distance you can see ahead is reduced",
            "Streetlights blur your vision",
            "Traffic signs are invisible at night",
        ],
        1,
        "Limited visibility is the biggest difference and danger during night driving.",
    ),
    q(
        "Special Driving Conditions",
        "If you drive past your exit on an expressway, what should you do?",
        [
            "Back up on the shoulder",
            "Make a U-turn at the next opening",
            "Drive to the next exit",
            "Stop and wait for police help",
        ],
        2,
        "Never back up or make a U-turn on an expressway. Continue to the next exit.",
    ),
    q(
        "Special Driving Conditions",
        "When driving at night, what is most important?",
        [
            "Use high beams at all times",
            "Drive within the range of your headlights",
            "Watch only intersections",
            "Brake as late as possible",
        ],
        1,
        "You must be able to stop within the distance lit by your headlights.",
    ),
    q(
        "Special Driving Conditions",
        "If an approaching train is close enough or fast enough to be a danger, what must you do?",
        [
            "Cross quickly before it reaches you",
            "Slow down and proceed carefully",
            "Wait until the train has completely passed",
            "Move onto the shoulder and look again",
        ],
        2,
        "Do not cross until the train has fully passed and it is safe.",
    ),
    q(
        "Special Driving Conditions",
        "Which statement applies to all driving emergencies?",
        [
            "Always brake immediately",
            "Your first reaction is always best",
            "Think before you act",
            "Always steer to the shoulder",
        ],
        2,
        "Staying calm and thinking before acting helps you choose the safest response.",
    ),
    q(
        "Special Driving Conditions",
        "What vehicles must stop at every railroad crossing?",
        [
            "Pickup trucks",
            "School buses and passenger buses carrying passengers",
            "Motorcycles",
            "Cars towing small trailers",
        ],
        1,
        "School buses and passenger buses carrying passengers must stop at all railroad crossings.",
    ),
    q(
        "Sharing the Road",
        "You want to back out of your driveway and see children playing nearby. What should you do before moving?",
        [
            "Sound your horn",
            "Tell the children to stay back",
            "Walk behind your vehicle to make sure the way is clear",
            "Rev the engine",
        ],
        2,
        "Children can be hard to see, so physically checking behind the vehicle is safest.",
    ),
    q(
        "Sharing the Road",
        "What equipment must a bicycle used after dark have?",
        [
            "Reflective handlebar grips",
            "A front headlight and a red taillight",
            "Brake lights",
            "Amber turn signals",
        ],
        1,
        "Bicycles used after dark need lighting so others can see them.",
    ),
    q(
        "Sharing the Road",
        "On a roadway, where must a bicyclist generally ride?",
        [
            "On the right side of the road",
            "Facing traffic on the left side",
            "On either side of the road",
            "Where there is the least traffic",
        ],
        0,
        "Bicyclists generally ride on the right side and follow the same traffic direction as motor vehicles.",
    ),
    q(
        "Sharing the Road",
        "If there are no sidewalks, on which side of the road should a pedestrian walk?",
        [
            "The same side as traffic",
            "The side facing oncoming traffic",
            "The side with lighter traffic",
            "Either side",
        ],
        1,
        "Pedestrians should walk facing traffic when no sidewalk is available.",
    ),
    q(
        "Sharing the Road",
        "What should a motorist do when approaching a bicyclist?",
        [
            "Proceed as usual",
            "Pass as quickly as possible",
            "Exercise extreme caution",
            "Swerve into the opposite lane immediately",
        ],
        2,
        "Drivers should give bicyclists extra space and use great care.",
    ),
    q(
        "Sharing the Road",
        "What does a slow-moving vehicle emblem look like?",
        [
            "A square red sign",
            "A round green sign",
            "A triangular orange sign",
            "A yellow diamond sign",
        ],
        2,
        "The slow-moving vehicle emblem is a fluorescent orange triangle.",
    ),
    q(
        "Sharing the Road",
        "How does a bicyclist differ from a motorist under New York rules?",
        [
            "A bicyclist does not need to obey traffic laws",
            "A bicyclist does not have to signal turns",
            "A bicyclist is not required to insure the bicycle",
            "A bicyclist never has to report crashes",
        ],
        2,
        "Bicyclists must follow traffic laws, but bicycle insurance is not required like motor vehicle insurance.",
    ),
    q(
        "Sharing the Road",
        "When does a blind pedestrian have the legal right-of-way while crossing the street?",
        [
            "Only when wearing dark glasses",
            "Only when helped by another person",
            "When using a guide dog or a white or metallic cane",
            "Only at a traffic signal",
        ],
        2,
        "Blind pedestrians using a guide dog or white/metallic cane must always be given the right-of-way.",
    ),
    q(
        "Sharing the Road",
        "Where must drivers yield to pedestrians?",
        [
            "Only at marked crosswalks",
            "At all crosswalks and intersections",
            "Only when a crossing guard is present",
            "Only on school days",
        ],
        1,
        "Drivers must yield to pedestrians at both marked and unmarked crosswalks and intersections.",
    ),
    q(
        "Sharing the Road",
        "What should you do if another vehicle is stopped for pedestrians at a crosswalk?",
        [
            "Pass it carefully on the right",
            "Pass it only if the horn is used",
            "Never pass it",
            "Pass it if you cannot see pedestrians",
        ],
        2,
        "Do not pass a vehicle stopped at a crosswalk because pedestrians may be crossing where you cannot see them.",
    ),
    q(
        "Sharing the Road",
        "Near which places should drivers be especially alert for children?",
        [
            "Only near shopping centers",
            "Near schools, bus stops, parks, playgrounds, and ice cream trucks",
            "Only near highways",
            "Only in rural areas",
        ],
        1,
        "Children can enter the roadway unexpectedly near places where they gather.",
    ),
    q(
        "Sharing the Road",
        "When backing up near children, what should you rely on most?",
        [
            "Your mirrors only",
            "Your horn",
            "Looking through the back window and checking behind the vehicle",
            "The backup camera only",
        ],
        2,
        "Mirrors and cameras help, but drivers still need to look directly behind the vehicle.",
    ),
]

ACTIVE_BASE_QUESTIONS = BASE_QUESTIONS[:110] + BASE_QUESTIONS[-10:]

def lower_first(text: str) -> str:
    return text[:1].lower() + text[1:] if text else text


def trim_question(prompt: str) -> str:
    return prompt.strip().rstrip(" ?")


def spaced_clause(text: str) -> str:
    cleaned = text.strip()
    return f" {cleaned}" if cleaned else ""


def finalize_prompt(text: str) -> str:
    cleaned = " ".join(text.strip().split())
    cleaned = cleaned.replace(".?", "?").replace("..", ".")
    if cleaned.endswith("."):
        cleaned = cleaned[:-1].rstrip()
    return cleaned if cleaned.endswith("?") else f"{cleaned}?"


def strip_leading_you(text: str) -> str:
    cleaned = lower_first(text.strip())
    return cleaned[4:] if cleaned.startswith("you ") else cleaned


def build_prompt_variant(prompt: str, exam: int) -> str:
    base = prompt.strip()
    stem = trim_question(base)

    if exam == 1:
        return finalize_prompt(base)

    patterns = [
        (
            r"^What does (.+) mean$",
            lambda m, e: [
                f"A driver sees {m.group(1)}. What does it mean?",
                f"Which meaning matches {m.group(1)}?",
            ][e - 2],
        ),
        (
            r"^What does (.+) tell a driver to do$",
            lambda m, e: [
                f"A driver sees {m.group(1)}. What action does it require?",
                f"Which action matches {m.group(1)}?",
            ][e - 2],
        ),
        (
            r"^What does (.+) prevent$",
            lambda m, e: [
                f"A driver sees {m.group(1)}. What does it prohibit or prevent?",
                f"Which restriction matches {m.group(1)}?",
            ][e - 2],
        ),
        (
            r"^What does (.+) warn you about$",
            lambda m, e: [
                f"A warning sign shows {m.group(1)}. What is it warning you about?",
                f"Choose the correct warning meaning for {m.group(1)}.",
            ][e - 2],
        ),
        (
            r"^What colors are used on (.+)$",
            lambda m, e: [
                f"Which color combination is used on {lower_first(m.group(1))}?",
                f"Identify the sign colors used on {lower_first(m.group(1))}.",
            ][e - 2],
        ),
        (
            r"^What is the name of (.+)$",
            lambda m, e: [
                f"Choose the correct name for {lower_first(m.group(1))}.",
                f"What is the proper term for {lower_first(m.group(1))}?",
            ][e - 2],
        ),
        (
            r"^What is used (.+)$",
            lambda m, e: [
                f"Which marking or device is used {lower_first(m.group(1))}?",
                f"Choose what is used {lower_first(m.group(1))}.",
            ][e - 2],
        ),
        (
            r"^What happens to (.+)$",
            lambda m, e: [
                f"Choose what happens to {lower_first(m.group(1))}.",
                f"What is the result for {lower_first(m.group(1))}?",
            ][e - 2],
        ),
        (
            r"^What is true of (.+)$",
            lambda m, e: [
                f"Which statement about {lower_first(m.group(1))} is true?",
                f"Choose the true statement about {lower_first(m.group(1))}.",
            ][e - 2],
        ),
        (
            r"^What are (.+) designed to do$",
            lambda m, e: [
                f"Choose the purpose of {lower_first(m.group(1))}.",
                f"What are {lower_first(m.group(1))} intended to do?",
            ][e - 2],
        ),
        (
            r"^What does (.+) look like$",
            lambda m, e: [
                f"Which description matches how {lower_first(m.group(1))} looks?",
                f"Choose the correct appearance of {lower_first(m.group(1))}.",
            ][e - 2],
        ),
        (
            r"^What is (.+)$",
            lambda m, e: [
                f"Choose the correct answer about {lower_first(m.group(1))}.",
                f"Which statement correctly completes this: {m.group(1)}?",
            ][e - 2],
        ),
        (
            r"^What are (.+)$",
            lambda m, e: [
                f"Choose the correct answer about {lower_first(m.group(1))}.",
                f"Which statement correctly explains {lower_first(m.group(1))}?",
            ][e - 2],
        ),
        (
            r"^What happens (.+)$",
            lambda m, e: [
                f"Choose the likely result when{spaced_clause(m.group(1))}.",
                f"Identify what happens when{spaced_clause(m.group(1))}.",
            ][e - 2],
        ),
        (
            r"^What effect does (.+)$",
            lambda m, e: [
                f"Choose the correct effect of {lower_first(m.group(1))}.",
                f"Which effect is linked to {lower_first(m.group(1))}?",
            ][e - 2],
        ),
        (
            r"^How does (.+) differ from (.+)$",
            lambda m, e: [
                f"In what way does {lower_first(m.group(1))} differ from {lower_first(m.group(2))}?",
                f"Choose the correct difference between {lower_first(m.group(1))} and {lower_first(m.group(2))}.",
            ][e - 2],
        ),
        (
            r"^What can happen (.+)$",
            lambda m, e: [
                f"Choose the correct result if{spaced_clause(m.group(1))}.",
                f"Which outcome can happen if{spaced_clause(m.group(1))}?",
            ][e - 2],
        ),
        (
            r"^What can happen when (.+)$",
            lambda m, e: [
                f"Choose the correct result when {lower_first(m.group(1))}.",
                f"Which outcome can happen when {lower_first(m.group(1))}?",
            ][e - 2],
        ),
        (
            r"^What can result from (.+)$",
            lambda m, e: [
                f"Choose the correct result of {lower_first(m.group(1))}.",
                f"Which consequence can follow from {lower_first(m.group(1))}?",
            ][e - 2],
        ),
        (
            r"^What should you do (.+)$",
            lambda m, e: [
                f"In this situation, what should you do{spaced_clause(m.group(1))}?",
                f"Choose the safest action{spaced_clause(m.group(1))}.",
            ][e - 2],
        ),
        (
            r"^What should a driver do (.+)$",
            lambda m, e: [
                f"Which action should a driver take{spaced_clause(m.group(1))}?",
                f"Choose the safest action a driver should take{spaced_clause(m.group(1))}.",
            ][e - 2],
        ),
        (
            r"^Where may you never park$",
            lambda m, e: [
                "Choose the location where parking is never allowed.",
                "Where is parking always prohibited?",
            ][e - 2],
        ),
        (
            r"^When may (.+)$",
            lambda m, e: [
                f"Under which condition may you {strip_leading_you(m.group(1))}?",
                f"Choose when it is legal or appropriate to {strip_leading_you(m.group(1))}.",
            ][e - 2],
        ),
        (
            r"^When should (.+)$",
            lambda m, e: [
                f"Choose the correct time when {lower_first(m.group(1))}.",
                f"Under which condition should {lower_first(m.group(1))}?",
            ][e - 2],
        ),
        (
            r"^Where may (.+)$",
            lambda m, e: [
                f"Choose the correct place where {lower_first(m.group(1))}.",
                f"Where is it legal or correct to {lower_first(m.group(1))}?",
            ][e - 2],
        ),
        (
            r"^Where must (.+)$",
            lambda m, e: [
                f"Choose the correct location where {lower_first(m.group(1))}.",
                f"Where is a driver required to {lower_first(m.group(1))}?",
            ][e - 2],
        ),
        (
            r"^How far (.+)$",
            lambda m, e: [
                f"What is the correct distance when {lower_first(m.group(1))}?",
                f"Choose the required distance for this rule: {lower_first(m.group(1))}.",
            ][e - 2],
        ),
        (
            r"^How close (.+)$",
            lambda m, e: [
                f"Choose the correct distance limit: how close {lower_first(m.group(1))}?",
                f"What is the nearest legal distance when {lower_first(m.group(1))}?",
            ][e - 2],
        ),
        (
            r"^How does (.+)$",
            lambda m, e: [
                f"Choose the correct explanation for how {lower_first(m.group(1))}.",
                f"Which statement correctly explains how {lower_first(m.group(1))}?",
            ][e - 2],
        ),
        (
            r"^Which (.+)$",
            lambda m, e: [
                f"Select the true statement: which {lower_first(m.group(1))}?",
                f"Identify the correct answer: which {lower_first(m.group(1))}?",
            ][e - 2],
        ),
        (
            r"^(.+) does not depend on which of the following$",
            lambda m, e: [
                f"Choose the factor that {lower_first(m.group(1))} does not depend on.",
                f"Which item does {lower_first(m.group(1))} not depend on?",
            ][e - 2],
        ),
        (
            r"^Why (.+)$",
            lambda m, e: [
                f"Choose the best reason: {lower_first(m.group(1))}.",
                f"What is the main reason {lower_first(m.group(1))}?",
            ][e - 2],
        ),
        (
            r"^If (.+)$",
            lambda m, e: [
                f"Scenario: {m.group(1)}. What is the best action?",
                f"In this situation, if {lower_first(m.group(1))}, what should you do?",
            ][e - 2],
        ),
        (
            r"^You (.+)$",
            lambda m, e: [
                f"Scenario: you {lower_first(m.group(1))}. What is the best action?",
                f"If you {lower_first(m.group(1))}, what should you do next?",
            ][e - 2],
        ),
    ]

    for pattern, builder in patterns:
        match = re.match(pattern, stem)
        if match:
            return finalize_prompt(builder(match, exam))

    fallback = [
        f"Choose the best answer for this rule: {stem}",
        f"New York permit review — {stem}; choose the correct answer below",
    ][exam - 2]
    return finalize_prompt(fallback)


def build_questions():
    questions = []
    for idx, item in enumerate(ACTIVE_BASE_QUESTIONS):
        for exam in range(1, 4):
            prompt = build_prompt_variant(item["prompt"], exam)
            questions.append(
                {
                    "id": len(questions) + 1,
                    "exam": exam,
                    "category": item["category"],
                    "question": prompt,
                    "options": item["options"],
                    "correct": item["correct"],
                    "explanation": item["explanation"],
                    "sourceGroup": idx + 1,
                }
            )
    return questions


def validate(questions):
    assert len(ACTIVE_BASE_QUESTIONS) == 120, f"Expected 120 base questions, found {len(ACTIVE_BASE_QUESTIONS)}"
    assert len(questions) == 360, f"Expected 360 total questions, found {len(questions)}"
    ids = [q["id"] for q in questions]
    assert len(ids) == len(set(ids)), "Duplicate IDs found"
    question_texts = [q["question"] for q in questions]
    assert len(question_texts) == len(set(question_texts)), "Duplicate question texts found"
    for exam in (1, 2, 3):
        exam_questions = [q for q in questions if q["exam"] == exam]
        assert len(exam_questions) == 120, f"Exam {exam} does not have 120 questions"
        exam_question_texts = [q["question"] for q in exam_questions]
        assert len(exam_question_texts) == len(set(exam_question_texts)), f"Exam {exam} has duplicate prompts"
    for item in questions:
        assert len(item["options"]) == 4, f"Question {item['id']} does not have 4 options"
        assert 0 <= item["correct"] < 4, f"Question {item['id']} has invalid correct index"


def write_questions_js(questions, destination: Path):
    payload = json.dumps(questions, indent=2)
    content = (
        "// Generated by build_questions.py using the PRD dataset plan.\n"
        f"const questions = {payload};\n\n"
        "window.questions = questions;\n"
    )
    destination.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    all_questions = build_questions()
    validate(all_questions)
    write_questions_js(all_questions, Path(__file__).with_name("questions.js"))
    print(f"Generated {len(all_questions)} questions from {len(ACTIVE_BASE_QUESTIONS)} base items.")
