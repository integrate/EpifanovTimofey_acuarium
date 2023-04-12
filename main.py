import math

import wrap, random

wrap.world.create_world(800, 600)
wrap.world.set_back_color(255, 255, 255)
wrap.add_sprite_dir("sprite")
water = wrap.sprite.add("aqua", 400, 550, "water")
corm1 = wrap.sprite.add("aqua", 500, 200, "fishfood")
corm2 = wrap.sprite.add('aqua', 580, 200, "fishfood2")
fish = []
food = []
pf = None


def poyavlenie():
    a = wrap.sprite.add("fish", 100, 500, random.choice(
        ["fish purple1", "fish pink1", "fish blue1", "fish colored1", "fish colored2", "fish colored3"]))
    fish.append({"id": a, "skorostx": random.randint(2, 5), "skorosty": random.randint(2, 5),
                 "razmer": wrap.sprite.get_height(a)})


poyavlenie()


@wrap.on_mouse_down(wrap.BUTTON_RIGHT, wrap.BUTTON_MIDDLE)
def fishfood(pos_x, pos_y, button):
    global pf
    if button == wrap.BUTTON_RIGHT and pf == None:
        if wrap.sprite.is_collide_point(corm1, pos_x, pos_y):
            pf = corm1
        if wrap.sprite.is_collide_point(corm2, pos_x, pos_y):
            pf = corm2
        return
    if pf == None:
        return

    if button == wrap.BUTTON_RIGHT:
        g = 3
    else:
        g = 15
    for p in range(g):
        if pf == corm1:
            food1("c1", corm1, random.randint(-8, 8), random.randint(5, 15))
        if pf == corm2:
            food1("c2", corm2, random.randint(-8, 8), random.randint(5, 15))
    wrap.sprite.set_angle(pf, 345)


@wrap.on_mouse_up(wrap.BUTTON_RIGHT, wrap.BUTTON_MIDDLE)
def ugol():
    if pf == None:
        return
    wrap.sprite.set_angle(pf, 90)
    if wrap.sprite.get_bottom(pf) > wrap.sprite.get_top(water):
        wrap.sprite.move_bottom_to(pf, wrap.sprite.get_top(water))


@wrap.always(50)
def move_food():
    for f in food:
        if wrap.sprite.is_collide_sprite(f["id"], water):
            wrap.sprite.move(f["id"], 0, f["speed"])
        else:
            wrap.sprite.move(f["id"], 0, 9)
        if wrap.sprite.get_bottom(f["id"]) >= 800:
            wrap.sprite.move_bottom_to(f["id"], 800)
            food.remove(f)


@wrap.on_key_down(wrap.K_ESCAPE)
def otpuskanie():
    global pf
    if pf == None:
        return
    if pf == corm1:
        wrap.sprite.move_to(pf, 500, 200)
    if pf == corm2:
        wrap.sprite.move_to(pf, 580, 200)
    wrap.sprite.set_angle(pf, 90)
    pf = None


@wrap.on_mouse_move()
def peretaskivanie(pos_x, pos_y):
    if pf == None:
        return
    wrap.sprite.move_to(pf, pos_x, pos_y)
    if wrap.sprite.get_bottom(pf) > wrap.sprite.get_top(water):
        wrap.sprite.move_bottom_to(pf, wrap.sprite.get_top(water))


def food1(tag, banka, x, y):
    ffood = wrap.sprite.add("aqua", wrap.sprite.get_x(banka) + x, wrap.sprite.get_bottom(banka) + y,
                            "fish food granula")
    wrap.sprite.set_size(ffood, 11, 10)
    speed = random.randint(2, 3)
    sitnost = random.randint(2, 4)
    fff = {"id": ffood, "speed": speed, "sitnost": sitnost, "tag": tag}
    food.append(fff)


def otbivka(f):
    if wrap.sprite.get_left(f["id"]) <= 0:
        f["skorostx"] = abs(f["skorostx"])
        wrap.sprite.set_reverse_x(f["id"], False)
        x = wrap.sprite.get_x(f["id"])
        y = wrap.sprite.get_y(f["id"])
        wrap.sprite.set_angle_to_point(f["id"], x + f["skorostx"], y + f["skorosty"])
        wrap.sprite.move_left_to(f["id"], 0)

    if wrap.sprite.get_right(f["id"]) >= 800:
        f["skorostx"] = -abs(f["skorostx"])
        wrap.sprite.set_reverse_x(f["id"], True)
        x = wrap.sprite.get_x(f["id"])
        y = wrap.sprite.get_y(f["id"])
        wrap.sprite.set_angle_to_point(f["id"], x + f["skorostx"], y + f["skorosty"])
        wrap.sprite.move_right_to(f["id"], 800)

    if wrap.sprite.get_bottom(f["id"]) >= 600:
        f["skorosty"] = -abs(f["skorosty"])
        x = wrap.sprite.get_x(f["id"])
        y = wrap.sprite.get_y(f["id"])
        wrap.sprite.set_angle_to_point(f["id"], x + f["skorostx"], y + f["skorosty"])
        wrap.sprite.move_bottom_to(f["id"], 600)

    if wrap.sprite.get_top(f["id"]) <= wrap.sprite.get_top(water) - 10:
        f["skorosty"] = abs(f["skorosty"])
        x = wrap.sprite.get_x(f["id"])
        y = wrap.sprite.get_y(f["id"])
        wrap.sprite.set_angle_to_point(f["id"], x + f["skorostx"], y + f["skorosty"])
        wrap.sprite.move_top_to(f["id"], wrap.sprite.get_top(water) - 10)


def random_move(f):
    wrap.sprite.move(f["id"], f["skorostx"], f["skorosty"])
    x = wrap.sprite.get_x(f["id"])
    y = wrap.sprite.get_y(f["id"])
    wrap.sprite.set_angle_to_point(f["id"], x + f["skorostx"], y + f["skorosty"])


def razmnoszenie(f):
    if wrap.sprite.get_height(f["id"]) > f["razmer"] * 1.4:
        poyavlenie()
        wrap.sprite.set_height_proportionally(f["id"], f["razmer"])


def move_and_eat(f, r):
    x = wrap.sprite.get_x(r["id"])
    y = wrap.sprite.get_y(r["id"])
    x1 = wrap.sprite.get_x(f["id"])
    sk = math.sqrt(f["skorostx"] ** 2 + f["skorosty"] ** 2)
    if x < x1:
        wrap.sprite.set_reverse_x(f["id"], True)
    if x > x1:
        wrap.sprite.set_reverse_x(f["id"], False)
    wrap.sprite.set_angle_to_point(f["id"], x, y)
    wrap.sprite.move_at_angle_point(f["id"], x, y, sk * 1.5)
    if wrap.sprite.is_collide_sprite(f["id"], r["id"]):
        wrap.sprite.remove(r["id"])
        food.remove(r)
        wrap.sprite.set_height_proportionally(f["id"], wrap.sprite.get_height(f["id"]) + r["sitnost"])
        razmnoszenie(f)


def move_eat(f):
    c2f = False
    for y in food:
        if y["tag"] == "c2":
            c2f = y
            break
    c1f = False
    for y in food:
        if y["tag"] == "c1":
            c1f = y
            break

    if c2f != False and (wrap.sprite.get_costume(f["id"]) == "fish colored1" or wrap.sprite.get_costume(
            f["id"]) == "fish purple1"):
        move_and_eat(f, c2f)

    elif c1f != False and wrap.sprite.get_costume(f["id"]) != "fish colored1" and wrap.sprite.get_costume(
            f["id"]) != "fish purple1":
        move_and_eat(f, c1f)
    else:
        random_move(f)


@wrap.always(45)
def move():
    global kroshka
    for f in fish:
        move_eat(f)
        otbivka(f)


import wrap_py

wrap_py.app.start()
