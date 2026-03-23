# -*- coding: utf-8 -*-
"""
CHEM SNAKE GAME - FINAL VERSION
"""

import turtle as t
import random
import time

# -------------------------
# GLOBAL VARIABLES
# -------------------------

delay = 0.12
move_step = 15

score = 0
diamonds = 0
lives = 3

game_state = "welcome"
range_selected = (1, 10)

round_number = 1
elements_eaten = 0

eaten_elements = []

range_unlock = {
    "1-10": True,
    "11-20": False,
    "21-30": False
}

level2_timer = 90
level2_start = 0
last_quiz_time = 0

# -------------------------
# ELEMENT DATA (1–30)
# -------------------------

elements = [
{"name":"Hydrogen","symbol":"H","number":1,"example":"Hydrogen is found in water and used as fuel."},
{"name":"Helium","symbol":"He","number":2,"example":"Helium is used in balloons and MRI cooling."},
{"name":"Lithium","symbol":"Li","number":3,"example":"Lithium is used in phone batteries."},
{"name":"Beryllium","symbol":"Be","number":4,"example":"Beryllium is used in aerospace materials."},
{"name":"Boron","symbol":"B","number":5,"example":"Boron is used in glass and detergents."},
{"name":"Carbon","symbol":"C","number":6,"example":"Carbon is essential for life."},
{"name":"Nitrogen","symbol":"N","number":7,"example":"Nitrogen is used in fertilizers."},
{"name":"Oxygen","symbol":"O","number":8,"example":"Oxygen is used for breathing."},
{"name":"Fluorine","symbol":"F","number":9,"example":"Fluorine is used in toothpaste."},
{"name":"Neon","symbol":"Ne","number":10,"example":"Neon is used in lights."},
{"name":"Sodium","symbol":"Na","number":11,"example":"Sodium is found in salt."},
{"name":"Magnesium","symbol":"Mg","number":12,"example":"Magnesium is used in fireworks."},
{"name":"Aluminium","symbol":"Al","number":13,"example":"Aluminium is used in cans."},
{"name":"Silicon","symbol":"Si","number":14,"example":"Silicon is used in chips."},
{"name":"Phosphorus","symbol":"P","number":15,"example":"Phosphorus is used in fertilizers."},
{"name":"Sulfur","symbol":"S","number":16,"example":"Sulfur is used in medicine."},
{"name":"Chlorine","symbol":"Cl","number":17,"example":"Chlorine purifies water."},
{"name":"Argon","symbol":"Ar","number":18,"example":"Argon is used in bulbs."},
{"name":"Potassium","symbol":"K","number":19,"example":"Potassium is found in bananas."},
{"name":"Calcium","symbol":"Ca","number":20,"example":"Calcium strengthens bones."},
{"name":"Scandium","symbol":"Sc","number":21,"example":"Scandium is used in sports gear."},
{"name":"Titanium","symbol":"Ti","number":22,"example":"Titanium is used in aircraft."},
{"name":"Vanadium","symbol":"V","number":23,"example":"Vanadium strengthens steel."},
{"name":"Chromium","symbol":"Cr","number":24,"example":"Chromium prevents rust."},
{"name":"Manganese","symbol":"Mn","number":25,"example":"Manganese is used in batteries."},
{"name":"Iron","symbol":"Fe","number":26,"example":"Iron is used in construction."},
{"name":"Cobalt","symbol":"Co","number":27,"example":"Cobalt is used in magnets."},
{"name":"Nickel","symbol":"Ni","number":28,"example":"Nickel is used in coins."},
{"name":"Copper","symbol":"Cu","number":29,"example":"Copper is used in wires."},
{"name":"Zinc","symbol":"Zn","number":30,"example":"Zinc protects metals."}
]

# -------------------------
# SCREEN
# -------------------------

sc = t.Screen()
sc.title("Chem Snake Game")
sc.bgcolor("#e6f2ff")
sc.setup(700, 700)
sc.tracer(0)

# -------------------------
# TURTLES
# -------------------------

head = t.Turtle()
head.shape("square")
head.color("black")
head.penup()
head.direction = "Stop"

segments = []
foods = []

pen = t.Turtle()
pen.hideturtle()
pen.penup()

# -------------------------
# FUNCTIONS
# -------------------------

def get_elements():
    return [e for e in elements if range_selected[0] <= e["number"] <= range_selected[1]]

def create_foods():
    global foods
    for f in foods:
        f.hideturtle()
    foods = []

    for _ in range(3):
        food = t.Turtle()
        food.shape("circle")
        food.penup()

        element = random.choice(get_elements())
        food.element = element

        size = max(0.5, element["number"]/20)
        food.shapesize(size, size)

        if element["symbol"] in ["He","Ne","Ar"]:
            food.color("blue")
            food.is_noble = True
        else:
            food.color("red")
            food.is_noble = False

        food.goto(random.randint(-300,300), random.randint(-300,300))
        foods.append(food)

def add_segment(n=1):
    for _ in range(n):
        seg = t.Turtle()
        seg.shape("square")
        seg.color("grey")
        seg.penup()
        segments.append(seg)

def move():
    if head.direction == "up":
        head.sety(head.ycor() + move_step)
    if head.direction == "down":
        head.sety(head.ycor() - move_step)
    if head.direction == "left":
        head.setx(head.xcor() - move_step)
    if head.direction == "right":
        head.setx(head.xcor() + move_step)

# -------------------------
# QUIZ
# -------------------------

def run_quiz():
    global diamonds
    if len(eaten_elements) == 0:
        return

    correct = 0
    for _ in range(3):
        q = random.choice(eaten_elements)
        answer = sc.textinput("Quiz", f"What is symbol of {q['name']}?")

        if answer and answer.lower() == q["symbol"].lower():
            correct += 1

    diamonds += correct

# -------------------------
# CONTROLS
# -------------------------

def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

sc.listen()
sc.onkeypress(go_up,"Up")
sc.onkeypress(go_down,"Down")
sc.onkeypress(go_left,"Left")
sc.onkeypress(go_right,"Right")

# -------------------------
# MAIN LOOP
# -------------------------

while True:
    sc.update()

    if game_state == "level1":

        if len(foods) == 0:
            create_foods()

        move()

        for food in foods:
            if head.distance(food) < 20:

                eaten_elements.append(food.element)

                add_segment(1)
                score += 10
                elements_eaten += 1

                food.goto(1000,1000)

        if elements_eaten >= 15:
            run_quiz()
            game_state = "level2"
            level2_start = time.time()

    elif game_state == "level2":

        move()

        elapsed = int(time.time() - level2_start)
        remaining = level2_timer - elapsed

        if remaining <= 0:
            game_state = "level1"
            elements_eaten = 0

        for food in foods:
            if head.distance(food) < 20:

                if food.is_noble:
                    if segments:
                        segments.pop()
                else:
                    add_segment(max(1, food.element["number"]//10))

                food.goto(1000,1000)

    time.sleep(delay)

sc.mainloop()