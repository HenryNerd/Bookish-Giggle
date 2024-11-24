# Importing and initializing pygame
import pygame as pg
import asyncio

pg.init()

# Pygame variables
display = pg.display
clock  = pg.time.Clock()

# Variables
FRAMERATE = 30
GRAVITY = 1
velocity_y = 0
clone_velocity_y = 0
position_x = 50
position_y = 500
clone_x = 300
clone_y = 500
giggle = pg.Rect(position_x, position_y, 155, 170)
giggle_clone = pg.Rect(clone_x, clone_y, 155, 170)
jump_power = -17
jumping = False
swapping = False
moving_right = False
platform_move_distance = 0
otherplatform_move_distance = 0
sprite_frame = 1
screen_width = 1920
screen_height = 1080
won_once = False
giggle_number = 0
sidescroll_trigger = pg.Rect(screen_width - 600, 0, 600, screen_height)
sidescroll = False
current_level = "menu"
platforms = []

# Setting up the display
screen = pg.display.set_mode((screen_width, screen_height))
display.toggle_fullscreen()
display.set_caption("Bookish Giggle")

# Getting assets
def get_image(filepath, width=1920, height=1080):
    image = pg.image.load(filepath).convert_alpha()

    image = pg.transform.scale(image, (width, height))

    return image

menu_background = get_image(f"Assets/GiggleBackground.png")
forest_background = get_image(f"Assets/Forest.png")
forest_platform = get_image(f"Assets/ForestPlatform.png", 500, 250)
lava_background = get_image(f"Assets/Lava.png")
lava_platform = get_image(f"Assets/LavaPlatform.png", 500, 200)
start_button = get_image(f"Assets/StartButton.png", 500, 200)
giggle_img = get_image(f"Assets/GiggleRight.png", 200, 200)
giggle_img_clone = get_image(f"Assets/GiggleRight.png", 200, 200)
death_screen_text = get_image(f"Assets/death_screen.png", 1024, 1024)
win_screen_text = get_image(f"Assets/win_screen.png", 1024, 1024)

# Colors
bg_color = pg.Color(255, 255, 255)
red = pg.Color(255, 0, 0)

# Functions

# Draws the background depending on the level
def draw_background():
    global screen_height, screen_width

    if current_level == "menu":
        screen.blit(menu_background, (0, 0))
        menu_background.blit(start_button, (150, screen_height - 300))
    elif current_level == "levelOne":
        screen.blit(forest_background, (0, 0))
    elif current_level == "levelTwo":
        screen.blit(lava_background, (0, 0))
    elif current_level == "Fail":
        screen.fill(red)
        screen.blit(death_screen_text, (56 , screen_height - 1024))
    elif current_level == "win":
        screen.fill(bg_color)
        screen.blit(win_screen_text, (56 , screen_height - 1024))

# Updates the player and it's collisions, along with it's movement
def update_player():
    if not swapping:
        global position_x, clone_x, position_y, velocity_y, giggle, giggle_img, jumping, sprite_frame, clone_y, giggle_clone, clone_velocity_y, sidescroll_trigger, sidescroll, screen_height, screen_width, current_level, platform_move_distance

        if position_y > screen_height or clone_y > screen_height:
            current_level = "Fail"
            reset_defaults()

        if position_x < 85:
            for platform in platforms:
                platform[0] += 8
            clone_x += 8
            position_x += 8

        if current_level == "levelOne":
            if 3560 <= ((position_x + platform_move_distance) - 90) <= 4350 and 3550 <= ((clone_x + otherplatform_move_distance) - 340) <= 4350:
                current_level = "levelTwo"
                reset_defaults()
                platform_move_distance = 0
        elif current_level == "levelTwo":            
            if 4750 <= ((position_x + platform_move_distance) - 90) <= 5250 and 4750 <= ((clone_x + otherplatform_move_distance) - 340) <= 5250:
                current_level = "win"

        print((position_x + platform_move_distance) - 90, (clone_x + otherplatform_move_distance) - 340)

        # Updates velocity depending on the gravity and collisions
        velocity_y += GRAVITY
        clone_velocity_y += GRAVITY
        position_y += velocity_y
        clone_y += clone_velocity_y

        key_pressed = pg.key.get_pressed()

        if giggle.colliderect(sidescroll_trigger):
            sidescroll = True
        else:
            sidescroll = False

        if key_pressed[pg.K_d] or key_pressed[pg.K_RIGHT]:
            position_x += 8
            if sidescroll:
                move_platforms()
        
        for platform in platforms:
            if giggle.colliderect(platform) and velocity_y > 0 and (position_y) <= (platform[1]):
                position_y = platform[1] - 169
                velocity_y = 0
                jumping = False
                sprite_frame = 1
                giggle_img = get_image(f"Assets/GiggleRight.png", 200, 200)

                if key_pressed[pg.K_w] or key_pressed[pg.K_UP]:
                    velocity_y = jump_power
                    jumping = True
            elif giggle.colliderect(giggle_clone) and velocity_y > 0 and position_y <= (clone_y):
                position_y = giggle_clone[1] - 169
                velocity_y = 0
                jumping = False
                sprite_frame = 1
                giggle_img = get_image(f"Assets/GiggleRight.png", 200, 200)

                if key_pressed[pg.K_w] or key_pressed[pg.K_UP]:
                    velocity_y = jump_power
                    jumping = True

            if giggle_clone.colliderect(platform) and clone_velocity_y > 0 and clone_y < (platform[1] + (platform[1]/2)):
                clone_y = platform[1] - 169
                clone_velocity_y = 0

        giggle = pg.Rect(position_x, position_y, 155, 170)
        giggle_clone = pg.Rect(clone_x, clone_y, 155, 170)

        # Animate the player
        if jumping:
            if 1 <= sprite_frame <= 5 or 26 <= sprite_frame <= 30:
                current_sprite = f"Assets/sprite_0.png"
                if 1 <= sprite_frame <= 5:
                    sprite_frame += 1
                else: sprite_frame = 1
            elif 6 <= sprite_frame <= 10 or 21 <= sprite_frame <= 25:
                current_sprite = f"Assets/sprite_1.png"
                sprite_frame += 1
            elif 11 <= sprite_frame <= 15 or 16 <= sprite_frame <= 20:
                current_sprite = f"Assets/sprite_2.png"
                sprite_frame += 1
            giggle_img = get_image(current_sprite, 200, 200)
        
        screen.blit(giggle_img, giggle)
        screen.blit(giggle_img_clone, giggle_clone)

# Creates all the platform hitboxes
def create_platforms():
    global win_rectangle

    pg.mixer.music.stop()

    platforms.clear()

    def make_plathitbox(x_pos, y_pos):
            platforms.append(pg.Rect(x_pos, y_pos, 400, 250))

    if current_level == "menu":
        track3 = pg.mixer.music.load(f"Assets/Music/My Song 20(1).wav")
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)
    if current_level == "levelOne":
        make_plathitbox(50, screen_height - 300)
        make_plathitbox(600, screen_height - 600)
        make_plathitbox(1250, screen_height - 200)
        make_plathitbox(1840, screen_height - 500)
        make_plathitbox(2440, screen_height - 800)
        make_plathitbox(3200, screen_height - 800)
        make_plathitbox(4100, screen_height - 400)

        track = pg.mixer.music.load(f"Assets/Music/Forest (2).wav")
        pg.mixer.music.set_volume(1)
        pg.mixer.music.play(-1)
    if current_level == "levelTwo":
        make_plathitbox(50,screen_height - 300)
        make_plathitbox(700, screen_height - 550)
        make_plathitbox(1250, screen_height - 700)
        make_plathitbox(1800, screen_height - 400)
        make_plathitbox(2500, screen_height - 500)
        make_plathitbox(3000,screen_height - 300)
        make_plathitbox(3500, screen_height - 550)
        make_plathitbox(4000, screen_height - 700)
        make_plathitbox(4500, screen_height - 400)
        make_plathitbox(5000, screen_height - 500)
        track2 = pg.mixer.music.load(f"Assets/Music/More music I guess.wav")
        pg.mixer.music.set_volume(1)
        pg.mixer.music.play(-1)
create_platforms()

# Draws all of the platforms
def draw_platforms():
    for platform in platforms:
        if current_level == "levelOne":
            screen.blit(forest_platform, platform)
        elif current_level == "levelTwo":
            screen.blit(lava_platform, platform)

#Swaps you with your clone
def clone_swap():
    global position_x, position_y, clone_x, clone_y, swapping, giggle, giggle_clone, giggle_number

    if not jumping and not swapping:
        swapping = True
        if giggle_number == 0:
            giggle_number = 1
        elif giggle_number == 1:
            giggle_number = 0
        placeholder_x = position_x
        placeholder_y = position_y
        position_x = clone_x
        position_y = clone_y
        giggle = pg.Rect(position_x, position_y, 155, 170)
        clone_x = placeholder_x
        clone_y = placeholder_y
        giggle_clone = pg.Rect(clone_x, clone_y, 155, 170)

        swapping = False

def move_platforms():
    global clone_x, position_x, platform_move_distance, otherplatform_move_distance, giggle_number

    for platform in platforms:
        platform[0] -= 8
    clone_x -= 8
    position_x -= 8
    if giggle_number == 0:
        platform_move_distance += 8
    elif giggle_number == 1:
        otherplatform_move_distance += 8

def reset_defaults():
    global giggle, giggle_clone, position_x, position_y, clone_x, clone_y
    create_platforms()
    position_x = 50
    position_y = 500
    clone_x = 300
    clone_y = 500
    giggle = pg.Rect(position_x, position_y, 155, 170)
    giggle_clone = pg.Rect(clone_x, clone_y, 155, 170)

# Game loop
async def game_loop():
    running = True
    while running:
        global current_level, position_x, position_y, clone_x, clone_y, giggle, giggle_clone

        # Functions that need to repeat
        draw_background()
        draw_platforms()

        if current_level != "menu" and current_level != "Fail" and current_level != "win":
            update_player()
    
        # Check for keydown events
        for key_event in pg.event.get():
            if key_event.type == pg.QUIT:
                running = False
            elif key_event.type == pg.KEYDOWN:
                if key_event.key == pg.K_ESCAPE:
                    running = False
                if key_event.key == pg.K_SPACE:
                    clone_swap()
                if key_event.key == pg.K_RETURN:
                    if current_level == "Fail":
                        current_level = "levelOne"
                        reset_defaults()
            elif key_event.type == pg.MOUSEBUTTONDOWN:
                if current_level == "menu":
                    if 150 <= key_event.pos[0] <= 650 and (screen_height - 300) <= key_event.pos[1] <= (screen_height - 300 + 200):
                        current_level = "levelOne"
                        create_platforms()
    
        # Sets the framerate
        clock.tick(FRAMERATE)
    
        # Updates the display
        display.update()
asyncio.run( game_loop() )

# Quit the game when the main loop is done
pg.quit()
