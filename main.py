import math

import wrap, random

wrap.world.create_world(800, 800)
wrap.world.set_back_color(255, 255, 255)
wrap.add_sprite_dir("sprite")
water = wrap.sprite.add("aqua", 400, 550, "water")
corm1 = wrap.sprite.add("aqua", 500, 200, "fishfood")
corm2 = wrap.sprite.add('aqua', 580, 200, "fishfood2")
fish = []
food = []
pf = None


@wrap.on_key_down(wrap.K_SPACE)
def poyavlenie():
    a = wrap.sprite.add("fish", 100, 700, random.choice(
        ["fish purple1", "fish pink1", "fish blue1", "fish colored1", "fish colored2", "fish colored3"]))
    fish.append({"id": a, "skorostx": random.randint(2, 5), "skorosty": random.randint(2, 5)})
    print(fish)


@wrap.on_mouse_down(wrap.BUTTON_RIGHT, wrap.BUTTON_MIDDLE)
def fishfood(pos_x, pos_y, button):
    global pf
    if button == wrap.BUTTON_RIGHT:
        if pf == None:
            if wrap.sprite.is_collide_point(corm1, pos_x, pos_y):
                pf = corm1
            if wrap.sprite.is_collide_point(corm2, pos_x, pos_y):
                pf = corm2
            return
        wrap.sprite.set_angle(pf, 345)
        if pf == corm1:
            food1("c1", corm1, 0, 8)
            food1("c1", corm1, 5, 11)
            food1("c1", corm1, -4, 9)
        if pf == corm2:
            food1("c2", corm2, 1, 6)
            food1("c2", corm2, 8, 10)
            food1("c2", corm2, -6, 14)
    # else:


@wrap.on_mouse_up(wrap.BUTTON_RIGHT)
def ugol():
    if pf != None:
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
    if pf != None:
        if pf == corm1:
            wrap.sprite.move_to(pf, 500, 200)
        if pf == corm2:
            wrap.sprite.move_to(pf, 580, 200)
        wrap.sprite.set_angle(pf, 90)
        pf = None


@wrap.on_mouse_move()
def peretaskivanie(pos_x, pos_y):
    if pf != None:
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
        f["skorostx"] = -f["skorostx"]
        x = wrap.sprite.get_x(f["id"])
        y = wrap.sprite.get_y(f["id"])
        wrap.sprite.set_reverse_x(f["id"], not wrap.sprite.get_reverse_x(f["id"]))
        wrap.sprite.set_angle_to_point(f["id"], x + f["skorostx"], y + f["skorosty"])
        wrap.sprite.move_left_to(f["id"], 0)
    if wrap.sprite.get_right(f["id"]) >= 800:
        f["skorostx"] = -f["skorostx"]
        x = wrap.sprite.get_x(f["id"])
        y = wrap.sprite.get_y(f["id"])
        wrap.sprite.set_reverse_x(f["id"], not wrap.sprite.get_reverse_x(f["id"]))
        wrap.sprite.set_angle_to_point(f["id"], x + f["skorostx"], y + f["skorosty"])
        wrap.sprite.move_right_to(f["id"], 800)
    if wrap.sprite.get_bottom(f["id"]) >= 800:
        f["skorosty"] = -f["skorosty"]
        x = wrap.sprite.get_x(f["id"])
        y = wrap.sprite.get_y(f["id"])
        wrap.sprite.set_angle_to_point(f["id"], x + f["skorostx"], y + f["skorosty"])
        wrap.sprite.move_bottom_to(f["id"], 800)
    if wrap.sprite.get_top(f["id"]) <= wrap.sprite.get_top(water) - 10:
        f["skorosty"] = -f["skorosty"]
        x = wrap.sprite.get_x(f["id"])
        y = wrap.sprite.get_y(f["id"])
        wrap.sprite.set_angle_to_point(f["id"], x + f["skorostx"], y + f["skorosty"])
        wrap.sprite.move_top_to(f["id"], wrap.sprite.get_top(water) - 10)


@wrap.always(45)
def move():
    global kroshka
    for f in fish:
        if len(food) == 0:
            wrap.sprite.move(f["id"], f["skorostx"], f["skorosty"])
            x = wrap.sprite.get_x(f["id"])
            y = wrap.sprite.get_y(f["id"])
            wrap.sprite.set_angle_to_point(f["id"], x + f["skorostx"], y + f["skorosty"])
        else:
            r = food[0]["id"]
            x = wrap.sprite.get_x(r)
            y = wrap.sprite.get_y(r)
            sk = math.sqrt(f["skorostx"] ** 2 + f["skorosty"] ** 2)
            wrap.sprite.set_angle_to_point(f["id"], x, y)
            wrap.sprite.move_at_angle_point(f["id"], x, y, sk * 1.5)
            if wrap.sprite.is_collide_sprite(f["id"], r):
                wrap.sprite.remove(r)
                wrap.sprite.set_height_proportionally(f["id"],wrap.sprite.get_height(f["id"])+food[0]["sitnost"])
                del food[0]
        otbivka(f)


import wrap_py

wrap_py.app.start()
