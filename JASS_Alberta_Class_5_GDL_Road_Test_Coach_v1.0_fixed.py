
"""
JASS Alberta Class 5 GDL Road Test Coach
Offline PySide6 study/practice application.

Purpose:
- Prepare for the Alberta Class 5-GDL basic road test.
- Covers road-test knowledge, manoeuvres, observation habits, common failure points,
  vehicle readiness, mock questions, and a self-scoring practice drive.

Important:
This is a study aid, not an official Alberta road-test scoring sheet.
Always use the current Alberta Driver's Guide and Alberta.ca information.
"""

import sys
import random
from dataclasses import dataclass
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QColor, QFont, QIcon, QPainter, QPen, QBrush
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QListWidget, QListWidgetItem, QStackedWidget,
    QScrollArea, QProgressBar, QMessageBox, QCheckBox, QRadioButton,
    QButtonGroup, QGroupBox, QTextEdit, QSpinBox, QComboBox, QSplitter,
    QToolButton, QLineEdit
)

APP_NAME = "JASS • Alberta Class 5 GDL Road Test Coach"
VERSION = "1.0"

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

@dataclass
class Question:
    text: str
    options: list
    answer: int
    explanation: str
    tag: str


QUESTIONS = [
    Question(
        "At a stop sign, when should you proceed?",
        ["After slowing down if the road looks clear",
         "Only after a complete stop and when it is safe/legal to proceed",
         "When the vehicle behind you starts moving",
         "After checking only the left side"],
        1,
        "A complete stop is required. Then check the intersection and proceed only when safe and when right-of-way rules allow.",
        "Stops"
    ),
    Question(
        "Before changing lanes, which sequence is the best habit?",
        ["Signal → mirror → blind spot → move when safe",
         "Mirror → signal → blind spot → move when safe",
         "Blind spot → signal → accelerate immediately",
         "Signal only if another vehicle is nearby"],
        1,
        "A strong routine is mirror check, signal, blind-spot check, then a smooth lane change when safe. Keep checking the path while moving.",
        "Lane Changes"
    ),
    Question(
        "What should you do at an uncontrolled intersection when visibility is limited?",
        ["Maintain speed because you have priority",
         "Slow enough to observe, be prepared to yield, and proceed only when safe",
         "Stop in the middle of the intersection",
         "Sound the horn and continue"],
        1,
        "The official guide emphasizes slowing and observing at uncontrolled intersections and being prepared to yield.",
        "Intersections"
    ),
    Question(
        "For a right turn, which is a good road-test habit?",
        ["Approach in the proper lane, signal, check, turn smoothly and finish in the appropriate lane",
         "Turn from whichever lane is empty",
         "Signal after beginning the turn",
         "Move wide into the opposite lane first"],
        0,
        "Plan the turn early: correct lane, signal, mirror/shoulder checks, appropriate speed, then a controlled turn into the correct lane.",
        "Turns"
    ),
    Question(
        "What is the safest approach to a yellow traffic light?",
        ["Always accelerate to beat it",
         "Stop if you can do so safely; otherwise proceed cautiously according to the signal and conditions",
         "Always stop suddenly",
         "Ignore it if no one is behind you"],
        1,
        "A yellow light warns that the signal is changing. Do not create a hazard by stopping abruptly; make the safe/legal choice for the conditions.",
        "Signals"
    ),
    Question(
        "When reversing, where should your attention be?",
        ["Only the rear-view mirror",
         "Only the backup camera",
         "Continuously observe the path, including direct vision and mirrors, and check for pedestrians/vehicles",
         "Only the left mirror"],
        2,
        "Cameras and mirrors assist but do not replace active observation. Reverse slowly and keep checking the area around the vehicle.",
        "Backing"
    ),
    Question(
        "What is a common road-test mistake during parking?",
        ["Taking time to observe",
         "Climbing a curb or failing to complete a legal park within the allowed attempts",
         "Correcting the vehicle carefully",
         "Checking surroundings before opening a door"],
        1,
        "Parking errors can become serious test failures. Practise controlled corrections rather than rushing.",
        "Parking"
    ),
    Question(
        "If a pedestrian is crossing where you must yield, what should you do?",
        ["Continue if you think there is enough space",
         "Yield and do not create a conflict",
         "Honk so the pedestrian moves faster",
         "Pass the pedestrian closely"],
        1,
        "Pedestrian safety has priority where the law requires you to yield. Never pressure or endanger a pedestrian.",
        "Pedestrians"
    ),
    Question(
        "What is the road-test philosophy behind 'look far ahead'?",
        ["It lets you ignore nearby hazards",
         "It gives you more time to identify hazards, choose a lane and adjust smoothly",
         "It means you should stare straight ahead",
         "It eliminates mirror checks"],
        1,
        "Good observation is active: scan ahead, sides, mirrors and blind spots. Early information produces smoother decisions.",
        "Observation"
    ),
    Question(
        "What should you do if you miss an examiner's direction?",
        ["Make a sudden turn to obey it",
         "Ask for clarification or continue safely; never make an unsafe manoeuvre just to follow an instruction",
         "Stop in a live lane",
         "Reverse to the missed street"],
        1,
        "Safety comes first. A missed turn is preferable to a dangerous or illegal manoeuvre.",
        "Exam Technique"
    ),
    Question(
        "What is the best attitude toward speed on the road test?",
        ["Drive exactly at the limit regardless of conditions",
         "Choose a safe, legal speed appropriate for the road, traffic and conditions",
         "Drive well below the limit everywhere",
         "Match the fastest nearby vehicle"],
        1,
        "The examiner is looking for safe speed control, not simply a number on the speedometer.",
        "Speed"
    ),
    Question(
        "When preparing for a left turn, what should you avoid?",
        ["Planning lane position early",
         "Cutting across lanes or turning from an improper lane",
         "Checking traffic",
         "Signalling appropriately"],
        1,
        "Lane selection and turn positioning are assessed skills. Set up early and make the turn smoothly.",
        "Turns"
    ),
    Question(
        "Why should you make your observation checks visible?",
        ["Because exaggerated head movement is always required",
         "Because the examiner needs to see that you are actually checking mirrors/blind spots",
         "Because mirrors are optional",
         "Because it makes the car turn faster"],
        1,
        "Use natural, deliberate checks. A quick eye movement that cannot be observed may not demonstrate the skill clearly to an examiner.",
        "Observation"
    ),
    Question(
        "If traffic suddenly slows ahead, what is the best response?",
        ["Brake late and hard",
         "Look ahead, ease off early, create space and brake smoothly as needed",
         "Change lanes without checking",
         "Follow very closely"],
        1,
        "Anticipation is a major defensive-driving skill. Early speed reduction gives you options and reduces harsh braking.",
        "Defensive Driving"
    ),
    Question(
        "What should you do before starting the road test?",
        ["Only start the engine",
         "Know the controls, adjust seat/mirrors, fasten seat belt and ensure the vehicle is road-test ready",
         "Let the examiner discover vehicle problems",
         "Turn off all mirrors"],
        1,
        "Do a calm cockpit setup before moving. Vehicle readiness matters before the driving portion begins.",
        "Vehicle"
    ),
    Question(
        "Which is the best way to handle a hill parking manoeuvre?",
        ["Rush because the wheels must be turned quickly",
         "Know the required wheel direction for the situation, secure the vehicle, and verify it is safely parked",
         "Leave the vehicle in neutral",
         "Ignore the curb"],
        1,
        "Hill parking is a controlled procedure. Practise the exact wheel-position rules from the current Alberta Driver's Guide.",
        "Parking"
    ),
    Question(
        "What is a good rule for following distance?",
        ["Stay close so nobody cuts in",
         "Maintain enough space to react and stop safely for the conditions",
         "One car length at every speed",
         "Only leave space on highways"],
        1,
        "Following distance should increase with speed, poor weather, reduced visibility and other hazards.",
        "Following Distance"
    ),
    Question(
        "During a lane change, what should you do if the blind spot is occupied?",
        ["Move anyway because you signalled",
         "Wait and change only when the path is clear",
         "Accelerate into the blind spot",
         "Turn the wheel first"],
        1,
        "A signal communicates intent; it does not give you the right to move into an occupied space.",
        "Lane Changes"
    ),
    Question(
        "What is a useful memory sequence for a stop sign?",
        ["STOP → SCAN → DECIDE → GO",
         "GO → SIGNAL → STOP",
         "BRAKE → CLOSE EYES → GO",
         "HORN → GO → MIRROR"],
        0,
        "Use STOP → SCAN → DECIDE → GO as a mental cue. The exact legal right-of-way still depends on the intersection.",
        "Memory Trick"
    ),
    Question(
        "What is a useful memory sequence for a lane change?",
        ["MOVE → SIGNAL → LOOK",
         "MIRROR → SIGNAL → SHOULDER CHECK → MOVE",
         "HORN → MOVE → MIRROR",
         "SIGNAL → MOVE → SHOULDER CHECK"],
        1,
        "Think M-S-S-M: Mirror, Signal, Shoulder check, Move. Keep the movement smooth and confirm the space remains clear.",
        "Memory Trick"
    ),
]

TOPICS = {
    "🎯 Test Day": [
        ("What the test is really checking",
         "The goal is safe, controlled driving: observation, speed control, lane selection, right-of-way, turns, parking, vehicle handling and interaction with other road users."),
        ("Golden rule",
         "Never trade safety for a test instruction. If you miss a turn, continue safely and wait for the next instruction. Do not make a sudden turn, illegal stop or unsafe lane change."),
        ("Before you move",
         "Seat → mirrors → belt → controls → parking brake/vehicle status → surroundings. Take a breath. Start the test calmly."),
        ("Visible observation",
         "Use natural, deliberate head/eye movements for mirrors and shoulder checks. The examiner must be able to see that you are checking."),
        ("Smooth beats rushed",
         "Smooth acceleration, braking, steering and lane changes demonstrate control. Do not crawl unnecessarily, but do not rush to 'look confident'."),
    ],
    "👀 Observation": [
        ("SCAN", "Look well ahead for traffic lights, signs, pedestrians, parked vehicles, lane changes and developing hazards."),
        ("MIRRORS", "Check mirrors regularly and before braking, turning, changing lanes or changing position."),
        ("SHOULDER", "Blind-spot checks are essential before a lane change or lateral movement."),
        ("INTERSECTIONS", "Approach with enough control to see, decide and respond. Uncontrolled intersections require particular caution."),
        ("PEDESTRIANS", "Scan sidewalks, crossings, driveways, bus stops and parked-car gaps. Never assume a pedestrian has seen you."),
    ],
    "↔️ Lane Changes": [
        ("M-S-S-M", "Mirror → Signal → Shoulder check → Move. Confirm the space is still clear as you move."),
        ("Signal ≠ permission", "A signal communicates your intention; it does not give right-of-way."),
        ("Do not drift", "Use a deliberate, controlled steering movement. Keep speed appropriate while changing lanes."),
        ("Cancel signal", "After completing the movement, ensure the signal is cancelled if it does not cancel automatically."),
        ("Plan early", "Read overhead signs and lane markings early. Last-second lane changes are a common source of risk."),
    ],
    "↪️ Turns": [
        ("RIGHT TURN", "Correct lane → signal → mirror/shoulder observation as applicable → slow appropriately → yield → turn into the proper lane."),
        ("LEFT TURN", "Correct lane and position → signal → scan for traffic/pedestrians → yield as required → complete the turn without cutting across lanes."),
        ("Turn speed", "Slow enough to control the vehicle and observe, but avoid unnecessarily stopping or crawling where you have the right-of-way."),
        ("Finish the turn", "Do not let the vehicle wander into another lane. Straighten smoothly and establish the new lane position."),
    ],
    "🅿️ Parking": [
        ("PARALLEL PARK", "Practise the whole sequence slowly: observation, signal, positioning, controlled reverse, steering corrections and final legal position."),
        ("HILL PARK", "Know the exact wheel-direction rules from the current Alberta Driver's Guide for uphill/downhill and curb/no-curb situations."),
        ("CORRECTIONS", "A controlled correction is better than forcing a bad angle. Keep observing throughout the manoeuvre."),
        ("CURBS", "Avoid climbing the curb. Use slow vehicle control and practise reference points in the actual vehicle you will test in."),
        ("THREE-TRY MINDSET", "Practise until you can park legally and safely without relying on luck or one perfect attempt."),
    ],
    "🚦 Intersections": [
        ("STOP", "Come to a complete stop where required. Then scan and determine right-of-way before moving."),
        ("UNCONTROLLED", "Slow and observe. Be prepared to yield, including to traffic to your right where applicable."),
        ("RIGHT ON RED", "Follow the current Alberta rules and signage; complete the required stop and yield before turning when permitted."),
        ("YELLOW", "Treat the changing signal as a decision point. Do not create a hazard by stopping abruptly when you cannot safely stop."),
        ("T INTERSECTIONS", "Do not assume the end of the road automatically gives you priority. Identify signs, signals and right-of-way."),
    ],
    "⚠️ Common Fail Triggers": [
        ("AUTOMATIC-FAIL TYPE ERRORS", "The Alberta government says a road test can result in an automatic fail for actions such as unsafe driving, breaking traffic laws or endangering another road user."),
        ("SPEED", "Exceeding the speed limit or driving too fast for conditions can be a failure."),
        ("RIGHT-OF-WAY", "Failing to yield at an intersection or during a lane change can be a failure."),
        ("STOP", "Failing to stop completely where required is a serious error."),
        ("PARKING", "Climbing a curb while parking or being unable to park legally within the permitted attempts has been identified in Alberta guidance as a failure condition."),
    ],
    "🧠 Memory Tricks": [
        ("M-S-S-M", "Lane change: MIRROR → SIGNAL → SHOULDER → MOVE."),
        ("S-S-D-G", "Stop routine: STOP completely → SCAN → DECIDE → GO."),
        ("LOOK-LONG", "At every block: look far ahead before looking close. Early information buys time."),
        ("SPEED = SPACE", "More speed or worse conditions require more space and earlier decisions."),
        ("TURN = SETUP", "Good turns are mostly won before the steering wheel moves: lane + signal + observation + speed."),
        ("MISS ≠ PANIC", "Missed instruction? Stay safe, continue legally, then follow the next instruction."),
    ],
}

CHECKLIST = [
    "I have a valid vehicle and required documents for my appointment.",
    "The vehicle has acceptable tires and working brakes.",
    "Headlights, brake lights, signal lights and horn work.",
    "Windshield, mirrors and wipers provide adequate visibility.",
    "Seat belts and doors work properly.",
    "Fuel/charge is sufficient for the test.",
    "Seat and mirrors are adjusted before moving.",
    "I can identify the main controls without searching.",
    "I can perform a complete stop every time it is required.",
    "I can do a visible mirror and shoulder-check routine.",
    "I can change lanes smoothly without drifting.",
    "I can perform right and left turns from the correct lane.",
    "I can handle uncontrolled intersections calmly.",
    "I can parallel park without rushing.",
    "I can hill-park correctly according to the current guide.",
    "I can maintain appropriate speed for conditions.",
    "I can keep a safe following distance.",
    "I know what to do if I miss an examiner's instruction.",
]

MANOEUVRES = {
    "Parallel Parking": [
        "Signal and observe before positioning.",
        "Set up parallel to the parked vehicle with a safe, practical gap.",
        "Reverse slowly while continuously observing the path.",
        "Use steering reference points that you have practised in your vehicle.",
        "Correct calmly if needed; do not rush the steering.",
        "Finish legally, safely and close enough to the curb without climbing it.",
        "Before moving away, observe again and signal appropriately."
    ],
    "Hill Parking": [
        "Select the correct location and stop safely.",
        "Set the parking brake and secure the vehicle.",
        "Apply the exact wheel-direction rule for the situation from the current Alberta guide.",
        "Verify the vehicle is secure before leaving it.",
        "When leaving, observe mirrors/blind spot and enter traffic only when safe."
    ],
    "Right Turn": [
        "Read the intersection early.",
        "Signal in good time according to the situation.",
        "Check mirrors and surroundings.",
        "Reduce speed enough to control the turn and see hazards.",
        "Yield where required.",
        "Turn into the appropriate lane without swinging wide.",
        "Accelerate smoothly after the turn."
    ],
    "Left Turn": [
        "Choose the correct lane and position early.",
        "Signal and scan for vehicles, pedestrians and cyclists.",
        "Yield to traffic and pedestrians as required.",
        "Keep the turn controlled and predictable.",
        "Complete the turn into the appropriate lane.",
        "Check your new lane position and speed after the turn."
    ],
    "Lane Change": [
        "MIRROR",
        "SIGNAL",
        "SHOULDER CHECK",
        "MOVE only when the gap is safe.",
        "Keep a smooth steering path.",
        "Cancel the signal and re-establish normal observation."
    ],
    "Stop Sign": [
        "Approach under control.",
        "STOP completely.",
        "SCAN all relevant directions.",
        "DECIDE who has right-of-way.",
        "GO only when legal and safe.",
    ],
}

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------

STYLE = """
QMainWindow, QWidget {
    background: #0b1020;
    color: #e8edf7;
    font-family: "Segoe UI", "Inter", sans-serif;
}
QFrame#sidebar {
    background: #11182b;
    border-right: 1px solid #26324a;
}
QLabel#brand {
    color: #7dd3fc;
    font-size: 22px;
    font-weight: 800;
}
QLabel#subtitle {
    color: #94a3b8;
    font-size: 12px;
}
QLabel#pageTitle {
    font-size: 30px;
    font-weight: 800;
    color: #f8fafc;
}
QLabel#pageSub {
    color: #94a3b8;
    font-size: 14px;
}
QPushButton#nav {
    text-align: left;
    padding: 13px 15px;
    border-radius: 9px;
    color: #cbd5e1;
    background: transparent;
    border: 0;
    font-size: 13px;
}
QPushButton#nav:hover {
    background: #1a2540;
    color: #fff;
}
QPushButton#nav:checked {
    background: #17365d;
    color: #7dd3fc;
    font-weight: 700;
}
QFrame#card, QGroupBox {
    background: #121a2e;
    border: 1px solid #26324a;
    border-radius: 14px;
}
QGroupBox {
    margin-top: 10px;
    padding: 16px;
    font-weight: 700;
}
QLabel#cardTitle {
    font-size: 18px;
    font-weight: 750;
    color: #f8fafc;
}
QLabel#metric {
    font-size: 27px;
    font-weight: 850;
    color: #7dd3fc;
}
QLabel#muted {
    color: #94a3b8;
}
QPushButton#primary {
    background: #0284c7;
    color: white;
    border: 0;
    border-radius: 9px;
    padding: 11px 18px;
    font-weight: 700;
}
QPushButton#primary:hover { background: #0ea5e9; }
QPushButton#secondary {
    background: #1e293b;
    color: #dbeafe;
    border: 1px solid #334155;
    border-radius: 9px;
    padding: 10px 16px;
}
QPushButton#danger {
    background: #4c1d24;
    color: #fecaca;
    border: 1px solid #7f1d1d;
    border-radius: 9px;
    padding: 10px 16px;
}
QListWidget {
    background: #0e1527;
    border: 1px solid #26324a;
    border-radius: 10px;
    padding: 5px;
}
QListWidget::item {
    padding: 11px;
    border-radius: 7px;
}
QListWidget::item:selected {
    background: #17365d;
    color: #7dd3fc;
}
QProgressBar {
    background: #1e293b;
    border: 0;
    border-radius: 6px;
    height: 10px;
    text-align: center;
}
QProgressBar::chunk {
    background: #0ea5e9;
    border-radius: 6px;
}
QRadioButton {
    padding: 9px;
    spacing: 9px;
}
QCheckBox {
    spacing: 10px;
    padding: 8px;
}
QTextEdit, QLineEdit, QComboBox, QSpinBox {
    background: #0d1527;
    color: #e2e8f0;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px;
}
QScrollArea { border: 0; }
QToolButton {
    background: #1e293b;
    border-radius: 8px;
    padding: 8px;
}
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def title_block(title, subtitle):
    w = QWidget()
    l = QVBoxLayout(w)
    l.setContentsMargins(0, 0, 0, 18)
    a = QLabel(title)
    a.setObjectName("pageTitle")
    b = QLabel(subtitle)
    b.setObjectName("pageSub")
    l.addWidget(a)
    l.addWidget(b)
    return w


def card(title, text):
    f = QFrame()
    f.setObjectName("card")
    l = QVBoxLayout(f)
    l.setContentsMargins(18, 16, 18, 16)
    t = QLabel(title)
    t.setObjectName("cardTitle")
    t.setWordWrap(True)
    x = QLabel(text)
    x.setObjectName("muted")
    x.setWordWrap(True)
    x.setTextInteractionFlags(Qt.TextSelectableByMouse)
    l.addWidget(t)
    l.addSpacing(6)
    l.addWidget(x)
    return f


def scroll_page(content):
    s = QScrollArea()
    s.setWidgetResizable(True)
    s.setWidget(content)
    return s


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------

class RoadTestCoach(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1320, 820)
        self.setMinimumSize(1050, 680)

        self.pages = QStackedWidget()
        self.nav_buttons = []

        self.quiz_index = 0
        self.quiz_score = 0
        self.quiz_answered = 0
        self.quiz_questions = []

        self.build_ui()
        self.show_page(0)

    def build_ui(self):
        root = QWidget()
        root_l = QHBoxLayout(root)
        root_l.setContentsMargins(0, 0, 0, 0)
        root_l.setSpacing(0)

        side = QFrame()
        side.setObjectName("sidebar")
        side.setFixedWidth(245)
        sl = QVBoxLayout(side)
        sl.setContentsMargins(18, 22, 18, 18)

        brand = QLabel("JASS ROAD TEST")
        brand.setObjectName("brand")
        sub = QLabel("Alberta Class 5 • GDL Coach")
        sub.setObjectName("subtitle")
        sl.addWidget(brand)
        sl.addWidget(sub)
        sl.addSpacing(22)

        navs = [
            ("🏁  Dashboard", 0),
            ("🎯  Test Day", 1),
            ("👀  Observation", 2),
            ("↔️  Lane Changes", 3),
            ("↪️  Turns", 4),
            ("🅿️  Parking", 5),
            ("🚦  Intersections", 6),
            ("⚠️  Failure Triggers", 7),
            ("🧠  Memory Tricks", 8),
            ("🛠️  Manoeuvre Lab", 9),
            ("☑️  Test-Day Checklist", 10),
            ("📝  Mock Knowledge Test", 11),
            ("🚗  Practice Drive Score", 12),
        ]
        for text, idx in navs:
            b = QPushButton(text)
            b.setObjectName("nav")
            b.setCheckable(True)
            b.clicked.connect(lambda checked=False, i=idx: self.show_page(i))
            sl.addWidget(b)
            self.nav_buttons.append(b)

        sl.addStretch()
        v = QLabel(f"v{VERSION}\nOffline • Study aid")
        v.setObjectName("subtitle")
        sl.addWidget(v)

        root_l.addWidget(side)
        root_l.addWidget(self.pages, 1)
        self.setCentralWidget(root)

        self.pages.addWidget(self.dashboard_page())
        self.pages.addWidget(self.topic_page("🎯 Test Day", "The habits that make the road test calmer and safer."))
        self.pages.addWidget(self.topic_page("👀 Observation", "Make your scanning routine deliberate and visible."))
        self.pages.addWidget(self.topic_page("↔️ Lane Changes", "The M-S-S-M routine and common traps."))
        self.pages.addWidget(self.topic_page("↪️ Turns", "Correct setup, observation, speed and lane discipline."))
        self.pages.addWidget(self.topic_page("🅿️ Parking", "Parallel and hill parking practice principles."))
        self.pages.addWidget(self.topic_page("🚦 Intersections", "Stops, right-of-way, uncontrolled intersections and signals."))
        self.pages.addWidget(self.topic_page("⚠️ Failure Triggers", "High-risk errors to eliminate before test day."))
        self.pages.addWidget(self.topic_page("🧠 Memory Tricks", "Short mental cues for stressful moments."))
        self.pages.addWidget(self.manoeuvre_page())
        self.pages.addWidget(self.checklist_page())
        self.pages.addWidget(self.quiz_page())
        self.pages.addWidget(self.practice_drive_page())

    def show_page(self, idx):
        self.pages.setCurrentIndex(idx)
        for i, b in enumerate(self.nav_buttons):
            b.setChecked(i == idx)

    # ------------------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------------------

    def dashboard_page(self):
        c = QWidget()
        l = QVBoxLayout(c)
        l.setContentsMargins(30, 28, 30, 28)

        l.addWidget(title_block(
            "Alberta Class 5-GDL Road Test Coach",
            "A focused offline trainer for the basic Class 5-GDL road test."
        ))

        hero = QFrame()
        hero.setObjectName("card")
        hl = QHBoxLayout(hero)
        hl.setContentsMargins(22, 22, 22, 22)
        left = QVBoxLayout()
        h = QLabel("PASS BY HABIT — NOT BY LUCK")
        h.setStyleSheet("font-size:25px;font-weight:850;color:#7dd3fc;")
        p = QLabel(
            "Build a repeatable routine for observation, lane changes, turns, "
            "intersections, parking and speed control. The app deliberately "
            "focuses on safe driving rather than 'gaming' the examiner."
        )
        p.setWordWrap(True)
        p.setObjectName("muted")
        left.addWidget(h)
        left.addSpacing(8)
        left.addWidget(p)
        left.addSpacing(15)
        btn = QPushButton("Start 20-Question Mock Test")
        btn.setObjectName("primary")
        btn.clicked.connect(lambda: self.start_quiz())
        left.addWidget(btn, 0, Qt.AlignLeft)
        hl.addLayout(left, 1)

        metric = QVBoxLayout()
        m = QLabel("75")
        m.setObjectName("metric")
        ml = QLabel("Class 5 / 6 error-point threshold: more than 75 = fail")
        ml.setObjectName("muted")
        ml.setWordWrap(True)
        metric.addWidget(m, 0, Qt.AlignCenter)
        metric.addWidget(ml, 0, Qt.AlignCenter)
        hl.addLayout(metric)
        l.addWidget(hero)
        l.addSpacing(18)

        grid = QGridLayout()
        cards = [
            ("M-S-S-M", "Mirror → Signal → Shoulder → Move", 0, 0),
            ("S-S-D-G", "Stop → Scan → Decide → Go", 0, 1),
            ("LOOK-LONG", "See developing hazards early", 1, 0),
            ("MISS ≠ PANIC", "A missed turn is safer than a dangerous manoeuvre", 1, 1),
        ]
        for t, x, r, col in cards:
            grid.addWidget(card(t, x), r, col)
        l.addLayout(grid)
        l.addSpacing(18)

        info = card(
            "Current Alberta essentials",
            "A Class 5-GDL is the probationary licence obtained after meeting eligibility "
            "requirements and passing the Class 5 road test. Alberta states that drivers "
            "are no longer required to take the advanced road test to exit GDL; the "
            "advanced test was removed from that process in 2023."
        )
        l.addWidget(info)

        note = QLabel(
            "SOURCE NOTE • This app uses Alberta government information available at build time. "
            "Rules and procedures can change—verify the current Alberta Driver's Guide before test day."
        )
        note.setObjectName("muted")
        note.setWordWrap(True)
        l.addSpacing(10)
        l.addWidget(note)
        l.addStretch()
        return scroll_page(c)

    # ------------------------------------------------------------------
    # Topics
    # ------------------------------------------------------------------

    def topic_page(self, key, subtitle):
        c = QWidget()
        l = QVBoxLayout(c)
        l.setContentsMargins(30, 28, 30, 28)
        l.addWidget(title_block(key, subtitle))

        # Keep UI labels independent from the internal topic dictionary keys.
        # This prevents a harmless navigation-label change from causing a
        # KeyError during application startup.
        topic_key = {
            "⚠️ Failure Triggers": "⚠️ Common Fail Triggers",
        }.get(key, key)

        for t, x in TOPICS.get(topic_key, []):
            l.addWidget(card(t, x))
            l.addSpacing(10)
        l.addStretch()
        return scroll_page(c)

    # ------------------------------------------------------------------
    # Manoeuvres
    # ------------------------------------------------------------------

    def manoeuvre_page(self):
        c = QWidget()
        l = QVBoxLayout(c)
        l.setContentsMargins(30, 28, 30, 28)
        l.addWidget(title_block(
            "🛠️ Manoeuvre Lab",
            "Pick one manoeuvre and rehearse the sequence before practising in the car."
        ))

        row = QHBoxLayout()
        listw = QListWidget()
        listw.setFixedWidth(260)
        for name in MANOEUVRES:
            listw.addItem(name)
        row.addWidget(listw)

        right = QVBoxLayout()
        title = QLabel("Select a manoeuvre")
        title.setObjectName("cardTitle")
        right.addWidget(title)

        steps = QTextEdit()
        steps.setReadOnly(True)
        steps.setMinimumHeight(390)
        right.addWidget(steps)

        cue = QLabel("")
        cue.setObjectName("muted")
        cue.setWordWrap(True)
        right.addWidget(cue)
        row.addLayout(right, 1)
        l.addLayout(row)

        def select():
            name = listw.currentItem().text() if listw.currentItem() else None
            if not name:
                return
            title.setText(name)
            steps.setPlainText("\n".join(
                f"{i+1}. {x}" for i, x in enumerate(MANOEUVRES[name])
            ))
            cue.setText(
                "PRACTICE CUE: Say the sequence quietly before moving. "
                "During the actual test, keep the manoeuvre natural and safety-focused."
            )
        listw.currentRowChanged.connect(lambda _: select())
        listw.setCurrentRow(0)
        return c

    # ------------------------------------------------------------------
    # Checklist
    # ------------------------------------------------------------------

    def checklist_page(self):
        c = QWidget()
        l = QVBoxLayout(c)
        l.setContentsMargins(30, 28, 30, 28)
        l.addWidget(title_block(
            "☑️ Test-Day Checklist",
            "Tick each item only when you can honestly do it without guessing."
        ))

        progress = QProgressBar()
        progress.setRange(0, len(CHECKLIST))
        l.addWidget(progress)
        l.addSpacing(12)

        checks = []
        for text in CHECKLIST:
            cb = QCheckBox(text)
            checks.append(cb)
            l.addWidget(cb)

        def update():
            progress.setValue(sum(x.isChecked() for x in checks))

        for cb in checks:
            cb.stateChanged.connect(update)

        reset = QPushButton("Reset checklist")
        reset.setObjectName("secondary")
        reset.clicked.connect(lambda: [x.setChecked(False) for x in checks])
        l.addWidget(reset, 0, Qt.AlignLeft)
        l.addStretch()
        return scroll_page(c)

    # ------------------------------------------------------------------
    # Quiz
    # ------------------------------------------------------------------

    def quiz_page(self):
        self.quiz_root = QWidget()
        l = QVBoxLayout(self.quiz_root)
        l.setContentsMargins(30, 28, 30, 28)

        l.addWidget(title_block(
            "📝 Mock Knowledge Test",
            "20 questions • instant explanations • repeat until the habits become automatic."
        ))

        self.quiz_progress = QProgressBar()
        l.addWidget(self.quiz_progress)
        l.addSpacing(15)

        self.quiz_card = QFrame()
        self.quiz_card.setObjectName("card")
        ql = QVBoxLayout(self.quiz_card)
        self.quiz_question = QLabel("")
        self.quiz_question.setWordWrap(True)
        self.quiz_question.setStyleSheet("font-size:21px;font-weight:800;")
        ql.addWidget(self.quiz_question)
        self.quiz_group = QButtonGroup(self)
        self.quiz_options_box = QVBoxLayout()
        ql.addLayout(self.quiz_options_box)

        self.quiz_feedback = QLabel("")
        self.quiz_feedback.setWordWrap(True)
        self.quiz_feedback.setTextFormat(Qt.RichText)
        ql.addWidget(self.quiz_feedback)

        buttons = QHBoxLayout()
        self.quiz_check = QPushButton("Check Answer")
        self.quiz_check.setObjectName("primary")
        self.quiz_check.clicked.connect(self.check_answer)
        self.quiz_next = QPushButton("Next Question")
        self.quiz_next.setObjectName("secondary")
        self.quiz_next.clicked.connect(self.next_question)
        self.quiz_next.setEnabled(False)
        buttons.addWidget(self.quiz_check)
        buttons.addWidget(self.quiz_next)
        buttons.addStretch()
        ql.addLayout(buttons)

        l.addWidget(self.quiz_card)
        l.addStretch()
        return self.quiz_root

    def start_quiz(self):
        self.quiz_questions = random.sample(QUESTIONS, len(QUESTIONS))
        self.quiz_index = 0
        self.quiz_score = 0
        self.quiz_answered = 0
        self.show_page(11)
        self.load_question()

    def load_question(self):
        q = self.quiz_questions[self.quiz_index]
        self.quiz_progress.setMaximum(len(self.quiz_questions))
        self.quiz_progress.setValue(self.quiz_index)
        self.quiz_question.setText(
            f"{self.quiz_index + 1}. {q.text}"
        )
        while self.quiz_options_box.count():
            item = self.quiz_options_box.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.quiz_group = QButtonGroup(self)
        for i, option in enumerate(q.options):
            rb = QRadioButton(option)
            self.quiz_group.addButton(rb, i)
            self.quiz_options_box.addWidget(rb)
        self.quiz_feedback.setText("")
        self.quiz_check.setEnabled(True)
        self.quiz_next.setEnabled(False)

    def check_answer(self):
        q = self.quiz_questions[self.quiz_index]
        chosen = self.quiz_group.checkedId()
        if chosen < 0:
            QMessageBox.information(self, "Choose an answer", "Select one answer first.")
            return
        self.quiz_answered += 1
        if chosen == q.answer:
            self.quiz_score += 1
            self.quiz_feedback.setText(
                f"<b style='color:#86efac'>✓ Correct</b><br>{q.explanation}"
            )
        else:
            self.quiz_feedback.setText(
                f"<b style='color:#fca5a5'>✗ Not quite</b><br>"
                f"<b>Correct answer:</b> {q.options[q.answer]}<br>{q.explanation}"
            )
        self.quiz_check.setEnabled(False)
        self.quiz_next.setEnabled(True)

    def next_question(self):
        if self.quiz_index + 1 >= len(self.quiz_questions):
            pct = round(self.quiz_score / len(self.quiz_questions) * 100)
            QMessageBox.information(
                self, "Mock Test Complete",
                f"Score: {self.quiz_score}/{len(self.quiz_questions)} ({pct}%)\n\n"
                "Review the topic pages for anything you missed. "
                "This practice score is not an official Alberta road-test score."
            )
            self.show_page(0)
            return
        self.quiz_index += 1
        self.load_question()

    # ------------------------------------------------------------------
    # Practice drive self-score
    # ------------------------------------------------------------------

    def practice_drive_page(self):
        c = QWidget()
        l = QVBoxLayout(c)
        l.setContentsMargins(30, 28, 30, 28)
        l.addWidget(title_block(
            "🚗 Practice Drive Score",
            "Use this after a real practice drive with an instructor or experienced supervising driver."
        ))

        l.addWidget(card(
            "How to use this",
            "This is NOT an official Alberta scoring form. It is a self-coaching tool. "
            "Score each area from 0–3: 0 = unsafe/not demonstrated, 1 = inconsistent, "
            "2 = usually good, 3 = consistent and calm."
        ))
        l.addSpacing(12)

        areas = [
            "Observation / mirror checks",
            "Blind-spot checks",
            "Speed control",
            "Following distance",
            "Stops and right-of-way",
            "Right turns",
            "Left turns",
            "Lane changes",
            "Uncontrolled intersections",
            "Parallel parking",
            "Hill parking",
            "Smooth steering / braking",
            "Pedestrian awareness",
            "Lane positioning",
            "Following instructions safely",
        ]
        self.score_spins = []
        form = QGridLayout()
        for r, area in enumerate(areas):
            form.addWidget(QLabel(area), r, 0)
            sp = QSpinBox()
            sp.setRange(0, 3)
            sp.setValue(0)
            sp.setToolTip("0 unsafe/not demonstrated • 1 inconsistent • 2 usually good • 3 consistent")
            self.score_spins.append(sp)
            form.addWidget(sp, r, 1)
        l.addLayout(form)

        total_label = QLabel("Total: 0 / 45")
        total_label.setObjectName("metric")
        l.addWidget(total_label)

        advice = QLabel("Start by improving the lowest-scoring areas.")
        advice.setWordWrap(True)
        advice.setObjectName("muted")
        l.addWidget(advice)

        def update_score():
            total = sum(x.value() for x in self.score_spins)
            total_label.setText(f"Total: {total} / 45")
            lows = [areas[i] for i, x in enumerate(self.score_spins) if x.value() <= 1]
            if lows:
                advice.setText("Priority practice: " + " • ".join(lows[:5]))
            else:
                advice.setText("No area is currently at 0–1. Keep practising until the routine is reliable under pressure.")

        for sp in self.score_spins:
            sp.valueChanged.connect(update_score)

        reset = QPushButton("Reset drive score")
        reset.setObjectName("secondary")
        reset.clicked.connect(lambda: [x.setValue(0) for x in self.score_spins])
        l.addWidget(reset, 0, Qt.AlignLeft)
        l.addStretch()
        return scroll_page(c)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setStyleSheet(STYLE)
    w = RoadTestCoach()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
