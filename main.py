import pygame
import sys
import random
import math
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize mixer for audio

WIDTH, HEIGHT = 500, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shadow Ninja: Neon Escape")
clock = pygame.time.Clock()

# Enhanced Color Palette
BG_DARK = (10, 5, 25)        # Darker space blue
BG_STARS = (30, 25, 60)      # Star layer
NEON_CYAN = (0, 255, 255)
NEON_MAGENTA = (255, 0, 255)
NEON_GREEN = (0, 255, 150)
NEON_YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
SILVER = (200, 200, 220)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
PURPLE = (180, 70, 255)
ORANGE = (255, 165, 0)

# Fonts
title_font = pygame.font.SysFont("Arial Black", 40, bold=True)
font = pygame.font.SysFont("Verdana", 30, bold=True)
ui_font = pygame.font.SysFont("Courier New", 22, bold=True)
small_font = pygame.font.SysFont("Courier New", 18)

# Game States
MENU = 0
PLAYING = 1
GAME_OVER = 2
CHARACTER_SELECT = 3
SETTINGS = 4
current_state = MENU

# Initialize audio
try:
    # Create dummy sounds if files don't exist
    coin_sound = pygame.mixer.Sound('coin.wav') if os.path.exists('coin.wav') else pygame.mixer.Sound(buffer=bytes([0]))
    powerup_sound = pygame.mixer.Sound('powerup.wav') if os.path.exists('powerup.wav') else pygame.mixer.Sound(buffer=bytes([0]))
    hit_sound = pygame.mixer.Sound('hit.wav') if os.path.exists('hit.wav') else pygame.mixer.Sound(buffer=bytes([0]))
    select_sound = pygame.mixer.Sound('select.wav') if os.path.exists('select.wav') else pygame.mixer.Sound(buffer=bytes([0]))
except:
    # Create silent sounds as fallback
    coin_sound = pygame.mixer.Sound(buffer=bytes([0]))
    powerup_sound = pygame.mixer.Sound(buffer=bytes([0]))
    hit_sound = pygame.mixer.Sound(buffer=bytes([0]))
    select_sound = pygame.mixer.Sound(buffer=bytes([0]))

# Audio settings
music_volume = 0.5
sfx_volume = 0.7
music_enabled = True
sfx_enabled = True

# Star background effect
stars = []
for _ in range(100):
    stars.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(0, HEIGHT),
        'speed': random.uniform(0.5, 2),
        'size': random.randint(1, 3)
    })

# Character Selection
characters = [
    {"name": "Classic Ninja", "emoji": "🥷", "speed": 6, "color": NEON_CYAN, "unlocked": True},
    {"name": "Cyber Ninja", "emoji": "🤖", "speed": 7, "color": NEON_MAGENTA, "unlocked": True},
    {"name": "Ghost Ninja", "emoji": "👻", "speed": 8, "color": NEON_GREEN, "unlocked": True},
    {"name": "Dragon Ninja", "emoji": "🐉", "speed": 5, "color": RED, "unlocked": True},
    {"name": "Samurai", "emoji": "⚔️", "speed": 6, "color": PURPLE, "unlocked": False},
    {"name": "Ninja Cat", "emoji": "🐱", "speed": 9, "color": ORANGE, "unlocked": False}
]
selected_char = 0

# Player Properties
player_x = 100
player_y = HEIGHT // 2
p_width, p_height = 40, 40
velocity_y = 0
on_top = False
invincible = False
invincible_timer = 0
double_points = False
double_points_timer = 0
speed_boost = False
speed_boost_timer = 0
magnet = False
magnet_timer = 0

# Game Objects
obstacles = []
coins = []
powerups = []
spawn_timer = 0
score = 0
high_score = 0
lives = 3
game_speed = 7
combo = 0
max_combo = 0

# Menu selections
menu_selection = 0
character_select_selection = 0
game_over_selection = 0
settings_selection = 0

def reset_game():
    global player_x, player_y, obstacles, coins, powerups, spawn_timer
    global score, lives, game_speed, on_top, invincible, double_points, speed_boost, magnet
    global invincible_timer, double_points_timer, speed_boost_timer, magnet_timer, combo, max_combo
    
    player_x = 100
    player_y = HEIGHT // 2
    obstacles = []
    coins = []
    powerups = []
    spawn_timer = 0
    score = 0
    lives = 3
    game_speed = 7
    on_top = False
    invincible = False
    double_points = False
    speed_boost = False
    magnet = False
    invincible_timer = 0
    double_points_timer = 0
    speed_boost_timer = 0
    magnet_timer = 0
    combo = 0
    max_combo = 0

def play_sound(sound):
    """Play sound effect if enabled"""
    if sfx_enabled and sound:
        sound.set_volume(sfx_volume)
        sound.play()

def spawn_obstacle():
    """Spawn obstacles with different patterns"""
    pattern = random.randint(1, 5)
    
    if pattern == 1:  # Single obstacle
        side = random.choice([0, HEIGHT - 80])
        obstacles.append({
            "rect": pygame.Rect(WIDTH + 50, side, 50, 80),
            "type": "fire"
        })
    elif pattern == 2:  # Top and bottom obstacles
        obstacles.append({
            "rect": pygame.Rect(WIDTH + 50, 0, 50, 80),
            "type": "fire"
        })
        obstacles.append({
            "rect": pygame.Rect(WIDTH + 150, HEIGHT - 80, 50, 80),
            "type": "fire"
        })
    elif pattern == 3:  # Moving obstacle
        obstacles.append({
            "rect": pygame.Rect(WIDTH + 50, random.randint(100, HEIGHT-180), 50, 80),
            "type": "spike",
            "move_y": random.choice([-1, 1]),
            "move_speed": random.uniform(0.5, 1.5)
        })
    elif pattern == 4:  # Wide obstacle
        obstacles.append({
            "rect": pygame.Rect(WIDTH + 50, random.randint(100, HEIGHT-180), 100, 60),
            "type": "wide"
        })
    else:  # Double moving obstacles
        y_pos = random.randint(100, HEIGHT-280)
        obstacles.append({
            "rect": pygame.Rect(WIDTH + 50, y_pos, 50, 80),
            "type": "spike",
            "move_y": 1,
            "move_speed": 1.0
        })
        obstacles.append({
            "rect": pygame.Rect(WIDTH + 150, y_pos + 150, 50, 80),
            "type": "spike",
            "move_y": -1,
            "move_speed": 1.0
        })

def spawn_coin():
    """Spawn coins in accessible positions"""
    for _ in range(random.randint(1, 3)):
        coins.append(pygame.Rect(
            WIDTH + random.randint(50, 200),
            random.randint(100, HEIGHT - 150),
            25, 25
        ))

def spawn_powerup():
    """Spawn random power-up"""
    powerup_type = random.choice(["shield", "double", "speed", "magnet", "life"])
    powerups.append({
        "rect": pygame.Rect(WIDTH + 100, random.randint(100, HEIGHT - 150), 35, 35),
        "type": powerup_type
    })

def draw_background():
    """Draw animated starry background"""
    screen.fill(BG_DARK)
    
    # Draw stars
    for star in stars:
        star['x'] -= star['speed'] * 0.5
        if star['x'] < 0:
            star['x'] = WIDTH
            star['y'] = random.randint(0, HEIGHT)
        
        brightness = random.randint(150, 255)
        color = (brightness, brightness, brightness)
        pygame.draw.circle(screen, color, (int(star['x']), int(star['y'])), star['size'])

def draw_player():
    """Draw player with selected character and effects"""
    # Draw glow effect if invincible
    if invincible:
        for i in range(5):
            alpha = 100 - i * 20
            glow_rect = pygame.Rect(
                player_x - i*2,
                player_y - i*2,
                p_width + i*4,
                p_height + i*4
            )
            s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(s, (*NEON_CYAN, alpha), (0, 0, glow_rect.width, glow_rect.height), border_radius=10)
            screen.blit(s, glow_rect)
    
    # Draw magnet effect
    if magnet:
        # Draw magnetic field
        for i in range(3):
            radius = 150 + i * 10
            s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*NEON_YELLOW, 30), (radius, radius), radius, 3)
            screen.blit(s, (player_x + p_width//2 - radius, player_y + p_height//2 - radius))
    
    # Draw player character
    char = characters[selected_char]
    player_txt = font.render(char["emoji"], True, char["color"])
    screen.blit(player_txt, (player_x, player_y))
    
    # Draw speed lines if boosting
    if speed_boost:
        for i in range(3):
            offset = (i + 1) * 5
            pygame.draw.line(screen, NEON_YELLOW,
                            (player_x - offset, player_y + p_height//2),
                            (player_x - offset - 10, player_y + p_height//2), 3)

def draw_button(text, x, y, width, height, color, hover_color, is_hovered, font_obj, text_color=WHITE):
    """Draw a button with hover effect"""
    button_color = hover_color if is_hovered else color
    pygame.draw.rect(screen, button_color, (x, y, width, height), border_radius=10)
    pygame.draw.rect(screen, NEON_CYAN if is_hovered else SILVER, (x, y, width, height), 3, border_radius=10)
    
    text_surf = font_obj.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + width//2, y + height//2))
    screen.blit(text_surf, text_rect)
    return pygame.Rect(x, y, width, height)

def draw_menu():
    """Draw main menu screen"""
    draw_background()
    
    # Title with glow effect
    for offset in range(3, 0, -1):
        title_shadow = title_font.render("SHADOW NINJA", True, (50, 50, 100))
        screen.blit(title_shadow, (WIDTH//2 - title_shadow.get_width()//2 + offset, 100 + offset))
    
    title = title_font.render("SHADOW NINJA", True, NEON_CYAN)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    subtitle = font.render("NEON ESCAPE", True, NEON_MAGENTA)
    screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 160))
    
    # Menu buttons
    buttons = []
    button_width, button_height = 300, 50
    start_x = WIDTH//2 - button_width//2
    
    # Start Game button
    buttons.append(draw_button(
        "▶ START GAME", start_x, 280, button_width, button_height,
        (40, 40, 80), NEON_GREEN, menu_selection == 0, ui_font
    ))
    
    # Character Select button
    buttons.append(draw_button(
        "👤 SELECT CHARACTER", start_x, 350, button_width, button_height,
        (40, 40, 80), NEON_CYAN, menu_selection == 1, ui_font
    ))
    
    # Settings button
    buttons.append(draw_button(
        "⚙️ SETTINGS", start_x, 420, button_width, button_height,
        (40, 40, 80), NEON_MAGENTA, menu_selection == 2, ui_font
    ))
    
    # Quit button
    buttons.append(draw_button(
        "❌ QUIT", start_x, 490, button_width, button_height,
        (40, 40, 80), RED, menu_selection == 3, ui_font
    ))
    
    # High score
    if high_score > 0:
        hs_text = ui_font.render(f"🏆 HIGH SCORE: {high_score}", True, GOLD)
        screen.blit(hs_text, (WIDTH//2 - hs_text.get_width()//2, 560))
    
    # Instructions
    inst1 = small_font.render("Use ARROW KEYS or WASD to navigate", True, (150, 150, 150))
    inst2 = small_font.render("Press ENTER or CLICK to select", True, (150, 150, 150))
    screen.blit(inst1, (WIDTH//2 - inst1.get_width()//2, 620))
    screen.blit(inst2, (WIDTH//2 - inst2.get_width()//2, 645))
    
    return buttons

def draw_character_select():
    """Draw character selection screen"""
    draw_background()
    
    title = title_font.render("SELECT YOUR NINJA", True, NEON_CYAN)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    
    # Draw characters in a grid
    char_buttons = []
    for i, char in enumerate(characters):
        col = i % 2
        row = i // 2
        x_pos = WIDTH//2 - 200 + col * 220
        y_pos = 150 + row * 150
        
        # Background for character card
        bg_color = (30, 30, 60)
        if not char["unlocked"]:
            bg_color = (50, 30, 30)  # Red tint for locked
        
        if i == selected_char:
            pygame.draw.rect(screen, (50, 50, 90), (x_pos-20, y_pos-20, 200, 130), border_radius=15)
            pygame.draw.rect(screen, NEON_CYAN, (x_pos-20, y_pos-20, 200, 130), 3, border_radius=15)
        else:
            pygame.draw.rect(screen, bg_color, (x_pos-20, y_pos-20, 200, 130), border_radius=15)
        
        # Character emoji
        char_text = font.render(char["emoji"], True, char["color"] if char["unlocked"] else (100, 100, 100))
        screen.blit(char_text, (x_pos, y_pos))
        
        # Character info
        name_text = ui_font.render(char["name"], True, WHITE if char["unlocked"] else (100, 100, 100))
        screen.blit(name_text, (x_pos + 60, y_pos))
        
        speed_text = small_font.render(f"Speed: {char['speed']}", True, SILVER if char["unlocked"] else (80, 80, 80))
        screen.blit(speed_text, (x_pos + 60, y_pos + 35))
        
        # Lock icon for locked characters
        if not char["unlocked"]:
            lock_text = small_font.render("🔒 Score 1000+ to unlock", True, (150, 100, 100))
            screen.blit(lock_text, (x_pos, y_pos + 70))
        
        char_buttons.append(pygame.Rect(x_pos-20, y_pos-20, 200, 130))
    
    # Back button
    back_button = draw_button(
        "← BACK TO MENU", WIDTH//2 - 150, 600, 300, 50,
        (40, 40, 80), NEON_CYAN, False, ui_font
    )
    
    return char_buttons, back_button

def draw_game_over():
    """Draw game over screen"""
    draw_background()
    
    # Game Over text
    game_over = title_font.render("GAME OVER", True, RED)
    screen.blit(game_over, (WIDTH//2 - game_over.get_width()//2, 100))
    
    # Score display
    score_text = font.render(f"SCORE: {score}", True, NEON_CYAN)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 180))
    
    # Max combo
    combo_text = small_font.render(f"MAX COMBO: {max_combo}", True, NEON_YELLOW)
    screen.blit(combo_text, (WIDTH//2 - combo_text.get_width()//2, 220))
    
    if score > high_score:
        new_record = font.render("🎉 NEW HIGH SCORE! 🎉", True, GOLD)
        screen.blit(new_record, (WIDTH//2 - new_record.get_width()//2, 260))
    
    # Buttons
    buttons = []
    button_width, button_height = 300, 50
    start_x = WIDTH//2 - button_width//2
    
    # Play Again button
    buttons.append(draw_button(
        "🔄 PLAY AGAIN", start_x, 320, button_width, button_height,
        (40, 40, 80), NEON_GREEN, game_over_selection == 0, ui_font
    ))
    
    # Main Menu button
    buttons.append(draw_button(
        "🏠 MAIN MENU", start_x, 390, button_width, button_height,
        (40, 40, 80), NEON_CYAN, game_over_selection == 1, ui_font
    ))
    
    # Character Select button
    buttons.append(draw_button(
        "👤 CHANGE CHARACTER", start_x, 460, button_width, button_height,
        (40, 40, 80), NEON_MAGENTA, game_over_selection == 2, ui_font
    ))
    
    # Quit button
    buttons.append(draw_button(
        "❌ QUIT", start_x, 530, button_width, button_height,
        (40, 40, 80), RED, game_over_selection == 3, ui_font
    ))
    
    return buttons

def draw_settings():
    """Draw settings screen"""
    draw_background()
    
    title = title_font.render("SETTINGS", True, NEON_CYAN)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    
    buttons = []
    button_width, button_height = 300, 40
    start_x = WIDTH//2 - button_width//2
    
    # Music toggle
    music_text = f"🎵 MUSIC: {'ON' if music_enabled else 'OFF'}"
    buttons.append(draw_button(
        music_text, start_x, 150, button_width, button_height,
        (40, 40, 80), NEON_GREEN, settings_selection == 0, ui_font
    ))
    
    # SFX toggle
    sfx_text = f"🔊 SOUND EFFECTS: {'ON' if sfx_enabled else 'OFF'}"
    buttons.append(draw_button(
        sfx_text, start_x, 210, button_width, button_height,
        (40, 40, 80), NEON_CYAN, settings_selection == 1, ui_font
    ))
    
    # Music volume
    vol_text = f"🎶 MUSIC VOLUME: {int(music_volume * 100)}%"
    buttons.append(draw_button(
        vol_text, start_x, 270, button_width, button_height,
        (40, 40, 80), NEON_MAGENTA, settings_selection == 2, ui_font
    ))
    
    # SFX volume
    sfx_vol_text = f"🔉 SFX VOLUME: {int(sfx_volume * 100)}%"
    buttons.append(draw_button(
        sfx_vol_text, start_x, 330, button_width, button_height,
        (40, 40, 80), NEON_YELLOW, settings_selection == 3, ui_font
    ))
    
    # Back button
    buttons.append(draw_button(
        "← BACK TO MENU", start_x, 420, button_width, button_height,
        (40, 40, 80), NEON_CYAN, settings_selection == 4, ui_font
    ))
    
    # Instructions
    inst = small_font.render("Use LEFT/RIGHT to adjust volume, ENTER to toggle", True, (150, 150, 150))
    screen.blit(inst, (WIDTH//2 - inst.get_width()//2, 500))
    
    return buttons

def update_game():
    """Update all game elements"""
    global player_x, player_y, score, lives, game_speed, spawn_timer, high_score, combo, max_combo
    global invincible, invincible_timer, double_points, double_points_timer
    global speed_boost, speed_boost_timer, magnet, magnet_timer
    
    # Handle input
    keys = pygame.key.get_pressed()
    current_speed = characters[selected_char]["speed"]
    if speed_boost:
        current_speed = int(current_speed * 1.5)
    
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= current_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += current_speed
    
    # Screen boundaries
    player_x = max(0, min(WIDTH - p_width, player_x))
    
    # Smooth vertical movement
    target_y = 20 if on_top else HEIGHT - p_height - 20
    player_y += (target_y - player_y) * 0.15
    
    # Spawn objects
    spawn_timer += 1
    if spawn_timer > 40 - min(game_speed, 30):  # Faster spawning as game speeds up
        spawn_obstacle()
        if random.random() > 0.3:
            spawn_coin()
        if random.random() > 0.85 and len(powerups) < 2:
            spawn_powerup()
        spawn_timer = 0
    
    # Update obstacles
    for obs in obstacles[:]:
        obs["rect"].x -= game_speed
        
        # Move vertical obstacles
        if "move_y" in obs:
            obs["rect"].y += obs["move_speed"] * obs["move_y"]
            if obs["rect"].y <= 0 or obs["rect"].y >= HEIGHT - 80:
                obs["move_y"] *= -1
        
        # Remove off-screen obstacles
        if obs["rect"].x < -100:
            obstacles.remove(obs)
            if not invincible:
                score += 1
                combo += 1
                max_combo = max(max_combo, combo)
        
        # Check collision
        player_rect = pygame.Rect(player_x, player_y, p_width, p_height)
        if player_rect.colliderect(obs["rect"]) and not invincible:
            play_sound(hit_sound)
            lives -= 1
            invincible = True
            invincible_timer = 180  # 3 seconds at 60 FPS
            combo = 0
            if lives <= 0:
                if score > high_score:
                    high_score = score
                # Unlock characters based on score
                if score >= 1000:
                    for char in characters:
                        char["unlocked"] = True
                return GAME_OVER
    
    # Update coins with magnet effect
    player_center_x = player_x + p_width // 2
    player_center_y = player_y + p_height // 2
    
    for coin in coins[:]:
        coin.x -= game_speed
        
        # Magnet effect
        if magnet:
            coin_center_x = coin.x + 12.5
            coin_center_y = coin.y + 12.5
            distance = math.sqrt((player_center_x - coin_center_x)**2 + (player_center_y - coin_center_y)**2)
            if distance < 150:
                # Move coin toward player
                angle = math.atan2(player_center_y - coin_center_y, player_center_x - coin_center_x)
                coin.x += math.cos(angle) * 10
                coin.y += math.sin(angle) * 10
        
        if coin.x < -50:
            coins.remove(coin)
        
        # Collect coin
        if pygame.Rect(player_x, player_y, p_width, p_height).colliderect(coin):
            play_sound(coin_sound)
            points = 20 if double_points else 10
            score += points
            combo += 1
            max_combo = max(max_combo, combo)
            coins.remove(coin)
    
    # Update power-ups
    for powerup in powerups[:]:
        powerup["rect"].x -= game_speed
        if powerup["rect"].x < -50:
            powerups.remove(powerup)
        
        # Collect power-up
        if pygame.Rect(player_x, player_y, p_width, p_height).colliderect(powerup["rect"]):
            play_sound(powerup_sound)
            if powerup["type"] == "shield":
                invincible = True
                invincible_timer = 300  # 5 seconds
            elif powerup["type"] == "double":
                double_points = True
                double_points_timer = 240  # 4 seconds
            elif powerup["type"] == "speed":
                speed_boost = True
                speed_boost_timer = 180  # 3 seconds
            elif powerup["type"] == "magnet":
                magnet = True
                magnet_timer = 200  # ~3.3 seconds
            elif powerup["type"] == "life":
                lives = min(lives + 1, 5)  # Max 5 lives
            powerups.remove(powerup)
    
    # Update timers
    if invincible:
        invincible_timer -= 1
        if invincible_timer <= 0:
            invincible = False
    
    if double_points:
        double_points_timer -= 1
        if double_points_timer <= 0:
            double_points = False
    
    if speed_boost:
        speed_boost_timer -= 1
        if speed_boost_timer <= 0:
            speed_boost = False
    
    if magnet:
        magnet_timer -= 1
        if magnet_timer <= 0:
            magnet = False
    
    # Gradually increase game speed
    if score > 0 and score % 100 == 0 and game_speed < 15:
        game_speed += 0.2
    
    return PLAYING

def draw_game():
    """Draw all game elements"""
    draw_background()
    
    # Draw obstacles
    for obs in obstacles:
        if obs["type"] == "fire":
            fire_txt = font.render("🔥", True, WHITE)
            screen.blit(fire_txt, (obs["rect"].x, obs["rect"].y))
            pygame.draw.line(screen, NEON_MAGENTA,
                           (obs["rect"].x, obs["rect"].y + 70),
                           (obs["rect"].x + 40, obs["rect"].y + 70), 3)
        elif obs["type"] == "spike":
            spike_txt = font.render("💀", True, WHITE)
            screen.blit(spike_txt, (obs["rect"].x, obs["rect"].y))
        else:  # wide obstacle
            pygame.draw.rect(screen, RED, obs["rect"])
            pygame.draw.rect(screen, NEON_MAGENTA, obs["rect"], 3)
    
    # Draw coins
    for coin in coins:
        coin_txt = font.render("🪙", True, GOLD)
        screen.blit(coin_txt, (coin.x, coin.y))
    
    # Draw power-ups
    for powerup in powerups:
        if powerup["type"] == "shield":
            powerup_txt = font.render("🛡️", True, NEON_CYAN)
        elif powerup["type"] == "double":
            powerup_txt = font.render("2×", True, NEON_GREEN)
        elif powerup["type"] == "speed":
            powerup_txt = font.render("⚡", True, NEON_YELLOW)
        elif powerup["type"] == "magnet":
            powerup_txt = font.render("🧲", True, PURPLE)
        else:  # life
            powerup_txt = font.render("❤️", True, RED)
        screen.blit(powerup_txt, (powerup["rect"].x, powerup["rect"].y))
    
    # Draw player
    draw_player()
    
    # UI Overlay
    score_surf = ui_font.render(f"SCORE: {score}", True, NEON_CYAN)
    screen.blit(score_surf, (20, 20))
    
    lives_surf = ui_font.render(f"LIVES: {'❤️' * lives}", True, RED)
    screen.blit(lives_surf, (20, 60))
    
    combo_surf = small_font.render(f"COMBO: {combo}", True, NEON_YELLOW)
    screen.blit(combo_surf, (20, 100))
    
    # Power-up indicators
    y_pos = 130
    if invincible:
        shield_text = small_font.render(f"INVINCIBLE: {invincible_timer//60}s", True, NEON_CYAN)
        screen.blit(shield_text, (20, y_pos))
        y_pos += 25
    if double_points:
        double_text = small_font.render(f"DOUBLE POINTS: {double_points_timer//60}s", True, NEON_GREEN)
        screen.blit(double_text, (20, y_pos))
        y_pos += 25
    if speed_boost:
        speed_text = small_font.render(f"SPEED BOOST: {speed_boost_timer//60}s", True, NEON_YELLOW)
        screen.blit(speed_text, (20, y_pos))
        y_pos += 25
    if magnet:
        magnet_text = small_font.render(f"MAGNET: {magnet_timer//60}s", True, PURPLE)
        screen.blit(magnet_text, (20, y_pos))
    
    # Character info
    char_name = small_font.render(f"NINJA: {characters[selected_char]['name']}", True, SILVER)
    screen.blit(char_name, (WIDTH - char_name.get_width() - 20, 20))
    
    # Speed info
    speed_info = small_font.render(f"SPEED: {game_speed:.1f}", True, (150, 200, 255))
    screen.blit(speed_info, (WIDTH - speed_info.get_width() - 20, 50))
    
    # Instructions
    hint_txt = small_font.render("SPACE: Flip | ARROWS: Move | ESC: Menu", True, (150, 150, 200))
    screen.blit(hint_txt, (WIDTH//2 - hint_txt.get_width()//2, HEIGHT - 40))

# Start background music if available
try:
    # Try to load background music
    if os.path.exists('background_music.mp3'):
        pygame.mixer.music.load('background_music.mp3')
        pygame.mixer.music.set_volume(music_volume)
        if music_enabled:
            pygame.mixer.music.play(-1)  # Loop forever
    else:
        print("Note: background_music.mp3 not found. Game will run without background music.")
except Exception as e:
    print(f"Could not load music: {e}")

# Main game loop
mouse_wheel_event = None
while True:
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False
    mouse_wheel_event = None
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            play_sound(select_sound)
            
            if current_state == MENU:
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    menu_selection = (menu_selection + 1) % 4
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    menu_selection = (menu_selection - 1) % 4
                elif event.key == pygame.K_RETURN:
                    if menu_selection == 0:  # Start Game
                        reset_game()
                        current_state = PLAYING
                    elif menu_selection == 1:  # Character Select
                        current_state = CHARACTER_SELECT
                        character_select_selection = selected_char
                    elif menu_selection == 2:  # Settings
                        current_state = SETTINGS
                        settings_selection = 0
                    elif menu_selection == 3:  # Quit
                        pygame.quit()
                        sys.exit()
            
            elif current_state == CHARACTER_SELECT:
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    if character_select_selection + 2 < len(characters):
                        character_select_selection += 2
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    if character_select_selection - 2 >= 0:
                        character_select_selection -= 2
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    if character_select_selection + 1 < len(characters):
                        character_select_selection += 1
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    if character_select_selection - 1 >= 0:
                        character_select_selection -= 1
                elif event.key == pygame.K_RETURN:
                    if characters[character_select_selection]["unlocked"]:
                        selected_char = character_select_selection
                elif event.key == pygame.K_ESCAPE:
                    current_state = MENU
            
            elif current_state == PLAYING:
                if event.key == pygame.K_SPACE:
                    on_top = not on_top
                elif event.key == pygame.K_ESCAPE:
                    current_state = MENU
            
            elif current_state == GAME
