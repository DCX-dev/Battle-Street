import pygame
import random
import sys
import math
import socket
import threading
import pickle
import time
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Network constants
GAME_PORT = 55664  # Single port for all networking
BROADCAST_PORT = 55665  # Broadcast discovery port

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 100, 255)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 50)
GRAY = (150, 150, 150)
DARK_GRAY = (80, 80, 80)
LIGHT_GRAY = (200, 200, 200)
ORANGE = (255, 165, 0)
PURPLE = (200, 50, 200)
CYAN = (0, 255, 255)
DARK_BLUE = (20, 20, 60)
DARK_GREEN = (20, 60, 20)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle Street")
clock = pygame.time.Clock()

# Load weapon textures (AFTER screen is created)
WEAPON_TEXTURES = {}
weapon_files = {
    "Fist": "fist.png",
    "Water Gun": "water_gun.png",
    "Splat Bomb": "splat_bomb.png",
    "Cork Gun": "cork_gun.png",
    "Confetti Bomb": "confetti_bomb.png",
    "Squirt Gun": "squirt_gun.png",
    "Pie Bomb": "pie_bomb.png",
    "Nerf Blaster": "nerf_blaster.png",
    "Whoopee Cushion": "whoopee_cushion.png",
    "Bubble Gun": "bubble_gun.png",
    "Cartoon Grenade": "cartoon_grenade.png",
    "Banana Gun": "banana_gun.png",
    "Glitter Grenade": "glitter_grenade.png",
    "Paint Gun": "paint_gun.png",
    "Smoke Bomb": "smoke_bomb.png",
    "Potato Gun": "potato_gun.png",
    "Bubble Mine": "bubble_mine.png",
    "Ray Gun": "ray_gun.png",
    "Rubber Rocket": "rubber_rocket.png",
    "Laser Pistol": "laser_pistol.png",
    "TNT Stick": "tnt_stick.png",
    "Zap Gun": "zap_gun.png",
    "Foam Missile": "foam_missile.png",
    "Plasma Rifle": "plasma_rifle.png",
    "Sticky Bomb": "sticky_bomb.png",
    "Blaster Cannon": "blaster_cannon.png",
    "Super Grenade": "super_grenade.png",
    "Ion Blaster": "ion_blaster.png",
    "Mega Rocket": "mega_rocket.png",
    "Photon Cannon": "photon_cannon.png",
    "Nuke Launcher": "nuke_launcher.png"
}

for weapon_name, filename in weapon_files.items():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, "weapons", filename)
    
    if os.path.exists(filepath):
        try:
            WEAPON_TEXTURES[weapon_name] = pygame.image.load(filepath).convert_alpha()
            print(f"✅ Loaded {weapon_name} texture from {filepath}")
        except Exception as e:
            print(f"❌ Error loading {weapon_name}: {e}")
            WEAPON_TEXTURES[weapon_name] = None
    else:
        print(f"⚠️  Missing texture: {filepath}")
        WEAPON_TEXTURES[weapon_name] = None

# Fonts
title_font = pygame.font.Font(None, 90)
menu_font = pygame.font.Font(None, 50)
text_font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)
tiny_font = pygame.font.Font(None, 22)

# Game state
class GameState:
    MENU = 0
    BATTLE = 1
    SHOP = 2
    MODE_SELECT = 3
    WIN = 4
    LOSE = 5
    HOST_WAIT = 6
    JOIN_GAME = 7
    COLOR_SELECT = 8
    LOBBY = 9  # Pre-game lobby where players move around
    USERNAME_INPUT = 10  # Enter username before playing
    ROLE_SELECT = 11  # Select role before battle
    CUSTOMIZE = 12  # Customize menu (username, hats, skins, visors)

# Weapon data
WEAPONS = {
    "Fist": {"damage": 8, "cost": 0, "speed": 12, "color": (255, 220, 180), "explosion": False, "melee": True, "range": 40},
    "Water Gun": {"damage": 10, "cost": 30, "speed": 15, "color": (100, 150, 255), "explosion": False, "melee": False},
    "Splat Bomb": {"damage": 12, "cost": 40, "speed": 7, "color": (255, 100, 0), "explosion": True, "melee": False},
    "Cork Gun": {"damage": 13, "cost": 50, "speed": 16, "color": (200, 150, 100), "explosion": False, "melee": False},
    "Confetti Bomb": {"damage": 14, "cost": 60, "speed": 7, "color": (255, 200, 255), "explosion": True, "melee": False},
    "Squirt Gun": {"damage": 15, "cost": 70, "speed": 17, "color": (0, 200, 255), "explosion": False, "melee": False},
    "Pie Bomb": {"damage": 16, "cost": 80, "speed": 8, "color": (255, 230, 180), "explosion": True, "melee": False},
    "Nerf Blaster": {"damage": 17, "cost": 90, "speed": 18, "color": (255, 140, 0), "explosion": False, "melee": False},
    "Whoopee Cushion": {"damage": 18, "cost": 100, "speed": 9, "color": (200, 100, 200), "explosion": True, "melee": False},
    "Bubble Gun": {"damage": 19, "cost": 110, "speed": 14, "color": (200, 255, 255), "explosion": False, "melee": False},
    "Cartoon Grenade": {"damage": 20, "cost": 120, "speed": 8, "color": (50, 255, 50), "explosion": True, "melee": False},
    "Banana Gun": {"damage": 21, "cost": 130, "speed": 15, "color": (255, 255, 100), "explosion": False, "melee": False},
    "Glitter Grenade": {"damage": 22, "cost": 140, "speed": 8, "color": (255, 180, 255), "explosion": True, "melee": False},
    "Paint Gun": {"damage": 23, "cost": 150, "speed": 16, "color": (255, 100, 200), "explosion": False, "melee": False},
    "Smoke Bomb": {"damage": 24, "cost": 160, "speed": 7, "color": (150, 150, 150), "explosion": True, "melee": False},
    "Potato Gun": {"damage": 25, "cost": 170, "speed": 13, "color": (180, 140, 100), "explosion": False, "melee": False},
    "Bubble Mine": {"damage": 26, "cost": 180, "speed": 6, "color": (100, 255, 255), "explosion": True, "melee": False},
    "Ray Gun": {"damage": 27, "cost": 190, "speed": 20, "color": (0, 255, 100), "explosion": False, "melee": False},
    "Rubber Rocket": {"damage": 28, "cost": 200, "speed": 10, "color": (255, 100, 150), "explosion": True, "melee": False},
    "Laser Pistol": {"damage": 29, "cost": 210, "speed": 22, "color": (255, 0, 0), "explosion": False, "melee": False},
    "TNT Stick": {"damage": 30, "cost": 220, "speed": 8, "color": (255, 0, 0), "explosion": True, "melee": False},
    "Zap Gun": {"damage": 31, "cost": 230, "speed": 21, "color": (255, 255, 0), "explosion": False, "melee": False},
    "Foam Missile": {"damage": 32, "cost": 240, "speed": 11, "color": (255, 128, 0), "explosion": True, "melee": False},
    "Plasma Rifle": {"damage": 33, "cost": 250, "speed": 19, "color": (100, 100, 255), "explosion": False, "melee": False},
    "Sticky Bomb": {"damage": 34, "cost": 260, "speed": 7, "color": (100, 255, 100), "explosion": True, "melee": False},
    "Blaster Cannon": {"damage": 35, "cost": 270, "speed": 17, "color": (255, 50, 150), "explosion": False, "melee": False},
    "Super Grenade": {"damage": 36, "cost": 280, "speed": 9, "color": (255, 50, 255), "explosion": True, "melee": False},
    "Ion Blaster": {"damage": 38, "cost": 300, "speed": 23, "color": (150, 200, 255), "explosion": False, "melee": False},
    "Mega Rocket": {"damage": 40, "cost": 320, "speed": 12, "color": (255, 50, 50), "explosion": True, "melee": False},
    "Photon Cannon": {"damage": 42, "cost": 350, "speed": 24, "color": (255, 255, 255), "explosion": False, "melee": False},
    "Nuke Launcher": {"damage": 45, "cost": 400, "speed": 10, "color": (255, 255, 0), "explosion": True, "melee": False},
}

UPGRADES = {
    "Speed Boost": {"effect": "speed", "value": 2, "cost": 40},
    "Health Up": {"effect": "health", "value": 20, "cost": 60},
    "Shield": {"effect": "defense", "value": 5, "cost": 100},
}

# Roles system
ROLES = {
    "Engineer": {
        "name": "Engineer",
        "description": "Build structures and hide in vents",
        "color": (255, 165, 0),  # Orange
        "abilities": ["build", "vent"],
        "resources": 100,  # Starting build resources
        "vent_duration": 600,  # 10 seconds at 60 FPS
        "vent_cooldown": 900,  # 15 seconds cooldown
    },
    "Defender": {
        "name": "Defender",
        "description": "Protect your team's loot (Team mode only)",
        "color": (0, 150, 255),  # Blue
        "abilities": ["defend"],
        "team_only": True,
    },
    "Captain": {
        "name": "Captain",
        "description": "Lead your team and manage members (Team mode only)",
        "color": (255, 215, 0),  # Gold
        "abilities": ["lead", "eject"],
        "team_only": True,
    },
    "Ejector": {
        "name": "Ejector",
        "description": "Eliminate ejected players (Team mode only)",
        "color": (255, 0, 0),  # Red
        "abilities": ["execute"],
        "team_only": True,
    },
    "Fighter": {
        "name": "Fighter",
        "description": "Standard combat role",
        "color": (150, 150, 150),  # Gray
        "abilities": [],
    },
    "Trapper": {
        "name": "Trapper",
        "description": "Trap enemies in cages for 7 seconds",
        "color": (128, 0, 128),  # Purple
        "abilities": ["trap", "cage"],
        "trap_duration": 420,  # 7 seconds at 60 FPS
        "trap_cooldown": 600,  # 10 seconds cooldown
    }
}

# Vehicles
VEHICLES = {
    "None": {
        "name": "No Vehicle (On Foot)",
        "cost": 0,
        "health_multiplier": 1.0,
        "speed_multiplier": 1.0,
        "can_fly": False,
        "size": (40, 60),
        "color": None,  # Uses player color
        "description": "Standard on-foot combat"
    },
    "Rocket": {
        "name": "Rocket Pack",
        "cost": 500,
        "health_multiplier": 1.5,
        "speed_multiplier": 1.3,
        "can_fly": True,
        "size": (50, 70),
        "color": (255, 100, 50),
        "description": "Fast flying vehicle with missile launcher"
    },
    "Tank": {
        "name": "Battle Tank",
        "cost": 1000,
        "health_multiplier": 3.0,
        "speed_multiplier": 0.7,
        "can_fly": False,
        "size": (80, 60),
        "color": (100, 120, 100),
        "description": "Heavy armor, powerful weapons, slow movement"
    },
    "Ship": {
        "name": "Battleship",
        "cost": 1000000,
        "health_multiplier": 40.0,
        "speed_multiplier": 0.5,
        "can_fly": True,
        "size": (150, 120),
        "color": (150, 150, 180),
        "description": "Massive flying fortress with incredible firepower"
    }
}

# Powers (placeholder for future expansion)
POWERS = {
    "Shield Bubble": {"effect": "shield", "duration": 300, "cost": 200, "description": "Temporary invincibility"},
    "Speed Burst": {"effect": "speed_burst", "duration": 180, "cost": 150, "description": "Triple speed temporarily"},
    "Health Regen": {"effect": "regen", "duration": 240, "cost": 180, "description": "Regenerate health over time"},
}

# Cosmetics (hats, skins, visors)
COSMETICS = {
    # Hats
    "Basic Cap": {"type": "hat", "cost": 50, "color": (255, 0, 0), "description": "A simple red cap"},
    "Cool Hat": {"type": "hat", "cost": 100, "color": (0, 100, 255), "description": "A stylish blue hat"},
    "Crown": {"type": "hat", "cost": 500, "color": (255, 215, 0), "description": "Royal gold crown"},
    
    # Skins
    "Blue Skin": {"type": "skin", "cost": 75, "color": (50, 150, 255), "description": "Cool blue appearance"},
    "Green Skin": {"type": "skin", "cost": 75, "color": (50, 255, 100), "description": "Fresh green look"},
    "Purple Skin": {"type": "skin", "cost": 100, "color": (200, 50, 255), "description": "Mysterious purple"},
    "Golden Skin": {"type": "skin", "cost": 1000, "color": (255, 215, 0), "description": "Legendary gold skin"},
    
    # Visors
    "Cool Shades": {"type": "visor", "cost": 150, "color": (50, 50, 50), "description": "Stylish sunglasses"},
    "Cyber Visor": {"type": "visor", "cost": 300, "color": (0, 255, 255), "description": "Futuristic visor"},
}

# Battle Maps
MAPS = {
    "Street": {
        "name": "City Street",
        "bg_color": (100, 100, 120),
        "ground_color": (60, 60, 60),
        "decoration": "buildings",
        "sky_color": (135, 206, 250)
    },
    "Desert": {
        "name": "Sandy Desert",
        "bg_color": (255, 220, 150),
        "ground_color": (194, 178, 128),
        "decoration": "cacti",
        "sky_color": (255, 200, 100)
    },
    "Grassland": {
        "name": "Green Fields",
        "bg_color": (100, 200, 100),
        "ground_color": (80, 180, 80),
        "decoration": "trees",
        "sky_color": (135, 206, 250)
    },
    "Arena": {
        "name": "Battle Arena",
        "bg_color": (120, 80, 80),
        "ground_color": (90, 60, 60),
        "decoration": "pillars",
        "sky_color": (60, 40, 40)
    }
}

# Platform class
class Platform:
    def __init__(self, x, y, width, height, color=(100, 100, 100)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        
    def draw(self, screen):
        # Draw platform with 3D effect
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Top highlight
        pygame.draw.rect(screen, tuple(min(c + 30, 255) for c in self.color), 
                        (self.x, self.y, self.width, 3))
        # Bottom shadow
        pygame.draw.rect(screen, tuple(max(c - 30, 0) for c in self.color), 
                        (self.x, self.y + self.height - 3, self.width, 3))
        # Side shadow
        pygame.draw.rect(screen, tuple(max(c - 20, 0) for c in self.color), 
                        (self.x + self.width - 3, self.y, 3, self.height))
    
    def check_collision(self, player, player_vy):
        """Check if player is landing on this platform"""
        # Player must be falling (velocity_y > 0)
        if player_vy <= 0:
            return False
            
        # Check if player is above and overlapping horizontally
        player_bottom = player.y + player.height
        player_left = player.x
        player_right = player.x + player.width
        
        # Check horizontal overlap
        if player_right < self.x or player_left > self.x + self.width:
            return False
            
        # Check if player is landing on platform (from above)
        if player_bottom >= self.y and player_bottom <= self.y + self.height + abs(player_vy):
            return True
            
        return False

# Collectible class
class Collectible:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type  # "coin", "health", "speed", "damage"
        self.size = 20
        self.lifetime = 600  # 10 seconds at 60 FPS
        self.bounce_offset = 0
        self.bounce_speed = 0.1
        
    def update(self):
        self.lifetime -= 1
        self.bounce_offset = math.sin(pygame.time.get_ticks() * self.bounce_speed * 0.01) * 5
        return self.lifetime > 0
        
    def draw(self, screen):
        y = self.y + self.bounce_offset
        if self.type == "coin":
            # Draw coin
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(y)), self.size)
            pygame.draw.circle(screen, ORANGE, (int(self.x), int(y)), self.size - 5)
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(y)), self.size - 8)
        elif self.type == "health":
            # Draw health pack
            pygame.draw.circle(screen, WHITE, (int(self.x), int(y)), self.size)
            pygame.draw.circle(screen, RED, (int(self.x), int(y)), self.size - 3)
            # Cross
            pygame.draw.line(screen, WHITE, (self.x - 8, y), (self.x + 8, y), 3)
            pygame.draw.line(screen, WHITE, (self.x, y - 8), (self.x, y + 8), 3)
        elif self.type == "speed":
            # Draw speed boost
            pygame.draw.circle(screen, CYAN, (int(self.x), int(y)), self.size)
            pygame.draw.polygon(screen, WHITE, [
                (self.x - 5, y + 5),
                (self.x + 10, y),
                (self.x - 5, y - 5)
            ])
        elif self.type == "damage":
            # Draw damage boost
            pygame.draw.circle(screen, (255, 100, 100), (int(self.x), int(y)), self.size)
            pygame.draw.polygon(screen, WHITE, [
                (self.x, y - 8),
                (self.x + 8, y + 8),
                (self.x - 8, y + 8)
            ])
            
    def check_collision(self, player):
        dx = player.x + player.width / 2 - self.x
        dy = player.y + player.height / 2 - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < (self.size + player.width / 2)

class ExplosionParticle:
    """Cartoon explosion particle for visual effects"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.base_color = color
        self.particles = []
        # Create particles in a burst pattern
        for i in range(15):
            angle = (i / 15) * 2 * math.pi
            speed = random.uniform(2, 5)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': random.randint(3, 8),
                'life': random.randint(20, 40),
                'max_life': 40
            })
    
    def update(self):
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
        return len(self.particles) > 0  # Return True if still alive
    
    def draw(self, screen):
        for particle in self.particles:
            # Fade out as life decreases
            life_ratio = particle['life'] / particle['max_life']
            size = int(particle['size'] * life_ratio)
            if size > 0:
                # Create colorful cartoon explosion with multiple colors
                colors = [self.base_color, YELLOW, ORANGE, RED, WHITE]
                color_idx = int((1 - life_ratio) * (len(colors) - 1))
                color = colors[min(color_idx, len(colors) - 1)]
                pygame.draw.circle(screen, color, (int(particle['x']), int(particle['y'])), size)

class Player:
    def __init__(self, x, y, color, controls, username="Player", role="Fighter"):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.color = color
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.controls = controls
        self.weapon = "Fist"
        self.projectiles = []
        self.explosions = []
        self.coins = 0
        self.defense = 0
        self.facing_right = True
        self.shoot_cooldown = 0
        
        # Username and role system
        self.username = username
        self.role = role
        self.is_ghost = False  # Ghost mode when defeated
        self.team = None  # Team assignment (for team mode)
        
        # Role-specific attributes
        self.build_resources = ROLES[role].get("resources", 0)  # Engineer resources
        self.in_vent = False  # Engineer vent status
        self.vent_timer = 0  # Time remaining in vent
        self.vent_cooldown_timer = 0  # Cooldown before can use vent again
        self.structures = []  # Built structures (Engineer)
        
        # Trapper attributes
        self.is_trapped = False  # If player is trapped in cage
        self.trap_timer = 0  # Time remaining in trap
        self.trap_cooldown_timer = 0  # Cooldown before can trap again
        self.cage_x = 0  # Position of cage
        self.cage_y = 0
        
        # Vehicle system
        self.vehicle = "None"
        self.owned_vehicles = ["None"]
        
        # Cosmetics system
        self.hat = None
        self.skin = None
        self.visor = None
        self.owned_cosmetics = []
        
        # Temporary buffs from collectibles
        self.temp_speed_boost = 0
        self.temp_damage_boost = 0
        self.temp_speed_duration = 0
        self.temp_damage_duration = 0
        
        # Mouse targeting for weapon aiming
        self.target_x = SCREEN_WIDTH // 2
        self.target_y = SCREEN_HEIGHT // 2
        
        # Physics for ground-based movement
        self.velocity_y = 0
        self.gravity = 0.8
        self.jump_power = -15
        self.on_ground = False
        self.ground_y = SCREEN_HEIGHT - 180  # Stand on the sidewalk
        
    def move(self, keys, platforms=None):
        # Update temporary buffs
        if self.temp_speed_duration > 0:
            self.temp_speed_duration -= 1
            if self.temp_speed_duration == 0:
                self.temp_speed_boost = 0
        if self.temp_damage_duration > 0:
            self.temp_damage_duration -= 1
            if self.temp_damage_duration == 0:
                self.temp_damage_boost = 0
        
        # Get vehicle data
        vehicle_data = VEHICLES[self.vehicle]
        can_fly = vehicle_data["can_fly"]
        speed_mult = vehicle_data["speed_multiplier"]
        
        # Calculate move speed (with vehicle and temp boosts)
        move_speed = (self.speed + self.temp_speed_boost) * speed_mult
        
        # Flying vehicles have different movement
        if can_fly:
            # Free 2D movement for flying vehicles
            if keys[self.controls["left"]]:
                self.x -= move_speed
                self.facing_right = False
            if keys[self.controls["right"]]:
                self.x += move_speed
                self.facing_right = True
            if keys[pygame.K_w]:  # Up
                self.y -= move_speed
            if keys[pygame.K_s]:  # Down
                self.y += move_speed
            
            # No gravity for flying vehicles
            self.velocity_y = 0
            self.on_ground = False
        else:
            # Ground-based movement for non-flying vehicles
            if keys[self.controls["left"]]:
                self.x -= move_speed
                self.facing_right = False
            if keys[self.controls["right"]]:
                self.x += move_speed
                self.facing_right = True
            
            # Jump (Space key - check directly since it's universal)
            if keys[pygame.K_SPACE] and self.on_ground:
                self.velocity_y = self.jump_power
                self.on_ground = False
            
            # Apply gravity
            self.velocity_y += self.gravity
            self.y += self.velocity_y
            
            # Check platform collisions
            self.on_ground = False
            if platforms:
                for platform in platforms:
                    if platform.check_collision(self, self.velocity_y):
                        self.y = platform.y - self.height
                        self.velocity_y = 0
                        self.on_ground = True
                        break
            
            # Ground collision
            if not self.on_ground and self.y >= self.ground_y:
                self.y = self.ground_y
                self.velocity_y = 0
                self.on_ground = True
        
        # Keep player on screen
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(50, min(SCREEN_HEIGHT - self.height - 50, self.y))
    
    def shoot(self, target_x, target_y):
        weapon_data = WEAPONS[self.weapon]
        
        # Check if weapon is melee
        if weapon_data.get("melee", False):
            # Melee attack - no projectile, just update facing direction
            start_x = self.x + self.width // 2
            if target_x > start_x:
                self.facing_right = True
            else:
                self.facing_right = False
            return  # Melee damage is handled in check_melee_hit
        
        # Ranged weapon - create projectile
        # Calculate angle from player center to target
        start_x = self.x + self.width // 2
        start_y = self.y + self.height // 2
        
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Normalize direction
            dx = dx / distance
            dy = dy / distance
            
            # Update facing direction
            if dx > 0:
                self.facing_right = True
            else:
                self.facing_right = False
            
            # Apply damage boost
            damage = weapon_data["damage"] + self.temp_damage_boost
            
            projectile = Projectile(
                start_x,
                start_y,
                dx,
                dy,
                damage,
                weapon_data["speed"],
                weapon_data["color"],
                weapon_data.get("explosion", False)
            )
            self.projectiles.append(projectile)
    
    def check_melee_hit(self, other_player):
        """Check if melee attack hits another player"""
        weapon_data = WEAPONS[self.weapon]
        
        # Only check for melee weapons
        if not weapon_data.get("melee", False):
            return False
        
        # Check if other player is in range
        melee_range = weapon_data.get("range", 40)
        
        # Calculate distance to other player's center
        my_center_x = self.x + self.width / 2
        my_center_y = self.y + self.height / 2
        other_center_x = other_player.x + other_player.width / 2
        other_center_y = other_player.y + other_player.height / 2
        
        dx = other_center_x - my_center_x
        dy = other_center_y - my_center_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Check if in range and facing the right direction
        if distance <= melee_range:
            # Check if facing towards opponent
            if (self.facing_right and dx > 0) or (not self.facing_right and dx < 0):
                # Apply damage with boost
                damage = weapon_data["damage"] + self.temp_damage_boost
                damage = max(1, damage - other_player.defense)
                other_player.health -= damage
                return True
        
        return False
    
    def draw(self, screen):
        vehicle_data = VEHICLES[self.vehicle]
        vehicle_color = vehicle_data["color"] if vehicle_data["color"] else self.color
        
        # Draw vehicle based on type
        if self.vehicle == "None":
            # Determine player color (use skin if equipped, otherwise default color)
            player_color = self.color
            if self.skin:
                player_color = COSMETICS[self.skin]["color"]
            
            # Draw player body with outline
            pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
            pygame.draw.rect(screen, player_color, (self.x, self.y, self.width, self.height))
            
            # Draw simple face
            eye_y = self.y + 15
            if self.facing_right:
                pygame.draw.circle(screen, WHITE, (int(self.x + 25), eye_y), 5)
                pygame.draw.circle(screen, BLACK, (int(self.x + 25), eye_y), 2)
            else:
                pygame.draw.circle(screen, WHITE, (int(self.x + 15), eye_y), 5)
                pygame.draw.circle(screen, BLACK, (int(self.x + 15), eye_y), 2)
            
            # Draw visor if equipped
            if self.visor:
                visor_color = COSMETICS[self.visor]["color"]
                visor_y = self.y + 12
                pygame.draw.rect(screen, visor_color, (self.x + 8, visor_y, 24, 8))
                pygame.draw.rect(screen, BLACK, (self.x + 8, visor_y, 24, 8), 1)
            
            # Draw hat if equipped
            if self.hat:
                hat_color = COSMETICS[self.hat]["color"]
                hat_x = self.x + self.width // 2
                hat_y = self.y - 5
                # Hat brim
                pygame.draw.ellipse(screen, hat_color, (self.x + 5, hat_y, 30, 10))
                # Hat top
                pygame.draw.rect(screen, hat_color, (self.x + 10, hat_y - 15, 20, 15))
                pygame.draw.rect(screen, BLACK, (self.x + 10, hat_y - 15, 20, 15), 1)
        elif self.vehicle == "Tank":
            # Draw tank
            # Tank body
            pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
            pygame.draw.rect(screen, vehicle_color, (self.x, self.y + 20, self.width, self.height - 20))
            # Tank turret
            pygame.draw.circle(screen, vehicle_color, (int(self.x + self.width // 2), int(self.y + 25)), 20)
            pygame.draw.circle(screen, BLACK, (int(self.x + self.width // 2), int(self.y + 25)), 20, 2)
            # Tank barrel (points in facing direction)
            barrel_x = self.x + self.width // 2
            barrel_end = barrel_x + (30 if self.facing_right else -30)
            pygame.draw.line(screen, BLACK, (barrel_x, self.y + 25), (barrel_end, self.y + 25), 6)
            # Tank tracks
            pygame.draw.rect(screen, BLACK, (self.x, self.y + self.height - 10, self.width, 10), 3)
        elif self.vehicle == "Rocket":
            # Draw rocket pack
            # Rocket body
            pygame.draw.ellipse(screen, vehicle_color, (self.x, self.y, self.width, self.height))
            pygame.draw.ellipse(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
            # Rocket flames
            flame_y = self.y + self.height
            for i in range(3):
                flame_size = random.randint(5, 15)
                flame_x = self.x + self.width // 2 + random.randint(-10, 10)
                flame_colors = [(255, 200, 0), (255, 100, 0), (255, 50, 0)]
                pygame.draw.circle(screen, flame_colors[i % 3], (flame_x, flame_y + i * 5), flame_size)
            # Cockpit window
            pygame.draw.circle(screen, (150, 200, 255), (int(self.x + self.width // 2), int(self.y + 20)), 12)
        elif self.vehicle == "Ship":
            # Draw massive battleship
            # Ship hull
            pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
            pygame.draw.rect(screen, vehicle_color, (self.x, self.y + 30, self.width, self.height - 30))
            # Ship bridge/tower
            bridge_w = self.width // 3
            bridge_x = self.x + self.width // 2 - bridge_w // 2
            pygame.draw.rect(screen, vehicle_color, (bridge_x, self.y, bridge_w, 40))
            pygame.draw.rect(screen, BLACK, (bridge_x, self.y, bridge_w, 40), 2)
            # Windows
            for i in range(3):
                win_x = bridge_x + 10 + i * 15
                pygame.draw.rect(screen, CYAN, (win_x, self.y + 10, 10, 8))
            # Missile launchers
            for i in range(4):
                launcher_x = self.x + 10 + i * 35
                pygame.draw.rect(screen, DARK_GRAY, (launcher_x, self.y + 50, 10, 20))
                pygame.draw.rect(screen, RED, (launcher_x + 2, self.y + 50, 6, 15))
        
        # Draw weapon on player/vehicle
        self.draw_weapon(screen)
        
        # Draw health bar with border
        bar_width = self.width
        bar_height = 8
        health_ratio = max(0, self.health / self.max_health)
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 15, bar_width + 4, bar_height + 4))
        pygame.draw.rect(screen, DARK_GRAY, (self.x, self.y - 13, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN if health_ratio > 0.3 else RED, (self.x, self.y - 13, bar_width * health_ratio, bar_height))
        
    def draw_weapon(self, screen):
        """Draw the equipped weapon on the player, rotating towards mouse cursor"""
        # Check if weapon texture exists
        if self.weapon not in WEAPON_TEXTURES:
            return
        
        weapon_texture = WEAPON_TEXTURES[self.weapon]
        
        # Calculate weapon position (from player's hand)
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        # Calculate angle to target (mouse cursor)
        dx = self.target_x - center_x
        dy = self.target_y - center_y
        
        # Convert to angle in degrees
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        
        # Update facing direction based on mouse position
        if dx > 0:
            self.facing_right = True
        else:
            self.facing_right = False
        
        # Rotate the weapon texture to point at mouse
        rotated_weapon = pygame.transform.rotate(weapon_texture, -angle_deg)
        
        # Get the rect for positioning
        weapon_rect = rotated_weapon.get_rect()
        
        # Position the weapon slightly offset from player center (like holding it)
        offset_distance = 25
        weapon_rect.center = (
            center_x + math.cos(angle_rad) * offset_distance,
            center_y + math.sin(angle_rad) * offset_distance
        )
        
        # Draw the weapon
        screen.blit(rotated_weapon, weapon_rect)
        
    def update_projectiles(self, other_player):
        for proj in self.projectiles[:]:
            proj.update()
            if proj.x < 0 or proj.x > SCREEN_WIDTH or proj.y < 0 or proj.y > SCREEN_HEIGHT:
                self.projectiles.remove(proj)
            elif proj.check_collision(other_player):
                damage = max(1, proj.damage - other_player.defense)
                other_player.health -= damage
                # Create explosion effect if weapon has explosion
                if proj.has_explosion:
                    explosion = ExplosionParticle(proj.x, proj.y, proj.color)
                    self.explosions.append(explosion)
                self.projectiles.remove(proj)
    
    def update_explosions(self):
        """Update all explosion effects"""
        for explosion in self.explosions[:]:
            if not explosion.update():
                self.explosions.remove(explosion)

class Projectile:
    def __init__(self, x, y, dx, dy, damage, speed, color, has_explosion=False):
        self.x = x
        self.y = y
        self.dx = dx  # Direction x (normalized)
        self.dy = dy  # Direction y (normalized)
        self.damage = damage
        self.speed = speed
        self.color = color
        self.radius = 8
        self.has_explosion = has_explosion
        
    def update(self):
        self.x += self.speed * self.dx
        self.y += self.speed * self.dy
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
    def check_collision(self, player):
        return (self.x >= player.x and self.x <= player.x + player.width and
                self.y >= player.y and self.y <= player.y + player.height)

class Game:
    def __init__(self):
        # Start with username input, but will skip if we have saved username
        self.state = GameState.USERNAME_INPUT
        self.has_saved_username = False  # Will be set in load_progress
        self.menu_selection = 0
        self.shop_selection = 0
        self.shop_scroll_offset = 0
        self.shop_player = 1
        self.shop_tab = 0  # 0=Weapons, 1=Vehicles, 2=Powers
        self.is_cpu_mode = True
        self.is_network_game = False
        self.is_host = False
        self.network_socket = None
        self.client_connections = []  # List of client connections (for host)
        self.network_thread = None
        self.broadcast_socket = None
        self.opponent_data = None
        self.cpu_shoot_timer = 0
        self.cpu_strategy_timer = 0
        self.cpu_dodge_direction = 0
        self.coins_earned = 0
        self.coins_lost = 0
        self.winner = None
        self.loser = None
        self.server_ip = ""
        self.connection_status = "Waiting..."
        self.discovered_servers = []
        self.server_selection = 0
        self.lobby_players = []  # List of player names in lobby
        self.player_name = f"Player_{random.randint(1000, 9999)}"
        self.max_players = 10
        self.can_start = False
        self.lobby_code = ""
        self.input_code = ""  # For typing in a code to join
        self.last_broadcast_time = 0  # Track when we last received a broadcast
        self.network_running = False
        self.last_network_update = 0
        self.my_player_index = 0  # Which player am I in the all_players list?
        self.network_players_data = {}  # Store all players' data from network
        
        # Color selection in lobby
        self.available_colors = [
            ("Red", RED),
            ("Blue", BLUE),
            ("Green", GREEN),
            ("Yellow", YELLOW),
            ("Purple", PURPLE),
            ("Orange", ORANGE),
            ("Cyan", CYAN),
            ("Pink", (255, 100, 150)),
            ("Lime", (150, 255, 100)),
            ("Gold", (255, 200, 100))
        ]
        self.selected_color_index = 0  # Default to Red
        self.player_colors_taken = {}  # Maps player index to color index
        self.taken_colors = []  # For CPU mode color selection
        
        # Username and role system
        self.player_username = ""
        self.username_input_active = True
        self.selected_role = "Fighter"  # Default role
        self.role_selection_index = 0
        self.available_roles = ["Fighter", "Engineer"]  # Start with basic roles
        self.team_mode_enabled = False  # Toggle for team mode
        self.num_teams = 2  # Number of teams in team mode (2-7)
        self.team_size = 4  # Players per team
        
        # Customize menu system
        self.customize_tab = 0  # 0=Username, 1=Hats, 2=Skins, 3=Visors
        self.customize_selection = 0
        
        # Engineer inventory
        self.wood_inventory = 10  # Starting wood for engineers
        
        # Local player (A/D to move, Space to jump)
        self.player1 = Player(100, SCREEN_HEIGHT // 2 - 30, RED, {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "jump": pygame.K_SPACE,
            "up": pygame.K_SPACE,  # For compatibility
            "down": pygame.K_s,
            "shoot": pygame.K_SPACE
        })
        
        # Initialize owned weapons list
        self.player1.owned_weapons = ["Fist"]
        
        # CPU or network opponent
        self.player2 = Player(SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2 - 30, BLUE, {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "jump": pygame.K_SPACE,
            "up": pygame.K_SPACE,
            "down": pygame.K_s,
            "shoot": pygame.K_SPACE
        })
        
        # Additional players for multiplayer
        self.all_players = [self.player1, self.player2]
        self.player_colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, CYAN, (255, 100, 150), (150, 255, 100), (255, 200, 100)]
        
        # Load saved progress (after both players are created)
        self.load_progress()
        
        # If we have a saved username, skip straight to menu
        if self.has_saved_username:
            self.state = GameState.MENU
        
        # Collectibles and map system
        self.collectibles = []
        self.current_map = "Street"  # Default map
        self.collectible_spawn_timer = 0
        self.collectible_spawn_interval = 180  # Spawn every 3 seconds
        
        # Platforms system
        self.platforms = []
        self.generate_map_platforms()
        
    def assign_random_roles(self):
        """Randomly assign roles to all players before battle"""
        # All available roles (not just team-only ones for now)
        available_roles = ["Fighter", "Engineer", "Defender", "Captain", "Ejector"]
        
        # Assign random role to player1
        self.player1.role = random.choice(available_roles)
        self.player1.build_resources = ROLES[self.player1.role].get("resources", 0)
        print(f"🎲 {self.player1.username} assigned role: {self.player1.role}")
        
        # Assign random role to CPU
        if self.is_cpu_mode and not self.is_network_game:
            self.player2.role = random.choice(available_roles)
            self.player2.username = "CPU"
            self.player2.build_resources = ROLES[self.player2.role].get("resources", 0)
            print(f"🤖 CPU assigned role: {self.player2.role}")
    
    def reset_battle(self):
        # Apply vehicle stats to ensure size/health are correct
        self.apply_vehicle_stats(self.player1)
        self.apply_vehicle_stats(self.player2)
        
        # Reset main players
        self.player1.health = self.player1.max_health
        self.player2.health = self.player2.max_health
        self.player1.x = 100
        self.player1.y = self.player1.ground_y  # Start on ground
        self.player1.velocity_y = 0
        self.player1.on_ground = True
        self.player2.x = SCREEN_WIDTH - 150
        self.player2.y = self.player2.ground_y  # Start on ground
        self.player2.velocity_y = 0
        self.player2.on_ground = True
        self.player1.projectiles = []
        self.player2.projectiles = []
        self.player1.explosions = []
        self.player2.explosions = []
        self.cpu_shoot_timer = 0
        self.cpu_strategy_timer = 0
        self.cpu_dodge_direction = 0
        
        # CPU always uses same weapon as player
        if self.is_cpu_mode and not self.is_network_game:
            self.player2.weapon = self.player1.weapon
        
        # Reset collectibles
        self.collectibles = []
        self.collectible_spawn_timer = 0
        
        # Choose random map
        map_names = list(MAPS.keys())
        self.current_map = random.choice(map_names)
        print(f"Battle Map: {MAPS[self.current_map]['name']}")
        
        # Regenerate platforms for the new map
        self.generate_map_platforms()
        
        # Team mode: spawn CPU teammates
        if self.team_mode_enabled and self.is_cpu_mode:
            self.spawn_teams()
        # If multiplayer, create additional players
        elif self.is_network_game and len(self.lobby_players) > 2:
            # Clear existing additional players
            self.all_players = [self.player1, self.player2]
            
            # Create additional players positioned around the arena
            num_additional = len(self.lobby_players) - 2
            for i in range(num_additional):
                # Distribute players around the edges
                if i % 4 == 0:
                    x, y = SCREEN_WIDTH // 2, 50
                elif i % 4 == 1:
                    x, y = 50, SCREEN_HEIGHT - 200
                elif i % 4 == 2:
                    x, y = SCREEN_WIDTH - 90, SCREEN_HEIGHT - 200
                else:
                    x, y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200
                
                # Get color from selection or default
                color_idx = self.player_colors_taken.get(i + 2, (i + 2) % len(self.available_colors))
                color = self.available_colors[color_idx][1]
                
                new_player = Player(x, y, color, {
                    "left": pygame.K_a,
                    "right": pygame.K_d,
                    "jump": pygame.K_SPACE,
                    "up": pygame.K_SPACE,
                    "down": pygame.K_s,
                    "shoot": pygame.K_SPACE
                })
                self.all_players.append(new_player)
        else:
            self.all_players = [self.player1, self.player2]
        
    def spawn_teams(self):
        """Spawn CPU teammates and enemy teams for team mode"""
        self.all_players = []
        
        # Team colors for visual distinction
        team_colors = [
            (255, 50, 50),   # Red team
            (50, 50, 255),   # Blue team
            (50, 255, 50),   # Green team
            (255, 255, 50),  # Yellow team
            (255, 128, 0),   # Orange team
            (128, 0, 255),   # Purple team
            (0, 255, 255),   # Cyan team
        ]
        
        # Determine team composition
        total_players = self.num_teams * self.team_size
        
        # Roles that must be on each team
        required_roles = ["Engineer", "Captain"]
        optional_roles = ["Fighter", "Fighter", "Ejector"]  # For a team of 5+
        
        for team_num in range(self.num_teams):
            team_color = team_colors[team_num % len(team_colors)]
            
            # Assign roles for this team
            team_roles = required_roles.copy()
            remaining_slots = self.team_size - len(required_roles)
            
            # Fill remaining slots with varied roles
            for i in range(remaining_slots):
                if i == 0 and self.team_size >= 4:
                    team_roles.append("Trapper")
                elif i == 1 and self.team_size >= 5:
                    team_roles.append("Ejector")
                else:
                    team_roles.append("Fighter")
            
            # Create players for this team
            for player_idx in range(self.team_size):
                # Position players spread out on their side
                if team_num == 0:  # Player's team (left side)
                    base_x = 100 + player_idx * 80
                    base_y = 300 + (player_idx % 3) * 100
                else:  # Enemy teams (right side and varied positions)
                    base_x = SCREEN_WIDTH - 200 - player_idx * 80
                    base_y = 200 + (player_idx % 3) * 120
                
                role = team_roles[player_idx % len(team_roles)]
                
                # First player in team 0 is the human player
                if team_num == 0 and player_idx == 0:
                    # Update player1 with team info
                    self.player1.team = team_num
                    self.player1.role = role
                    self.player1.color = team_color
                    self.player1.build_resources = ROLES[role].get("resources", 0)
                    self.all_players.append(self.player1)
                else:
                    # Create CPU player
                    cpu_player = Player(
                        base_x, base_y, team_color,
                        {"left": pygame.K_a, "right": pygame.K_d, "jump": pygame.K_SPACE, "up": pygame.K_SPACE, "down": pygame.K_s, "shoot": pygame.K_SPACE},
                        username=f"CPU-{team_num}-{player_idx}",
                        role=role
                    )
                    cpu_player.team = team_num
                    cpu_player.weapon = self.player1.weapon  # Same weapon as player
                    self.all_players.append(cpu_player)
        
        print(f"🎮 Team Mode: {self.num_teams} teams with {self.team_size} players each")
        print(f"👤 Your team: Team {self.player1.team} ({self.player1.role})")
    
    def draw_username_input(self):
        # Gradient background
        for y in range(SCREEN_HEIGHT):
            color_val = int(30 + (y / SCREEN_HEIGHT) * 50)
            pygame.draw.line(screen, (color_val + 20, color_val, color_val + 30), (0, y), (SCREEN_WIDTH, y))
        
        # Title
        title = title_font.render("WELCOME TO BATTLE STREET", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title, title_rect)
        
        # Instructions
        inst_text = menu_font.render("Enter Your Username:", True, WHITE)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
        screen.blit(inst_text, inst_rect)
        
        # Username input box
        input_box_width = 400
        input_box_height = 60
        input_box_x = SCREEN_WIDTH // 2 - input_box_width // 2
        input_box_y = 350
        
        # Draw input box
        pygame.draw.rect(screen, WHITE, (input_box_x, input_box_y, input_box_width, input_box_height))
        pygame.draw.rect(screen, YELLOW, (input_box_x, input_box_y, input_box_width, input_box_height), 4)
        
        # Draw username text
        username_text = text_font.render(self.player_username, True, BLACK)
        username_rect = username_text.get_rect(midleft=(input_box_x + 15, input_box_y + input_box_height // 2))
        screen.blit(username_text, username_rect)
        
        # Draw cursor if active
        if self.username_input_active and int(pygame.time.get_ticks() / 500) % 2 == 0:
            cursor_x = username_rect.right + 5
            pygame.draw.line(screen, BLACK, (cursor_x, input_box_y + 15), (cursor_x, input_box_y + input_box_height - 15), 3)
        
        # Hint text
        hint = small_font.render("(Required - Type your name and press ENTER)", True, LIGHT_GRAY)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, 450))
        screen.blit(hint, hint_rect)
        
        # Show error if trying to continue without username
        if not self.player_username and hasattr(self, 'show_username_error'):
            error = text_font.render("Username is required!", True, RED)
            error_rect = error.get_rect(center=(SCREEN_WIDTH // 2, 520))
            screen.blit(error, error_rect)
    
    def draw_role_select(self):
        # Dramatic dark background with gradient
        for y in range(SCREEN_HEIGHT):
            color_val = int(10 + (y / SCREEN_HEIGHT) * 30)
            pygame.draw.line(screen, (color_val, color_val + 10, color_val + 20), (0, y), (SCREEN_WIDTH, y))
        
        # Pulsing effect for dramatic reveal
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.003)) * 30
        
        # Title with glow
        title = title_font.render("ROLE REVEAL", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        # Glow effect
        glow = title_font.render("ROLE REVEAL", True, (255, 255, int(100 + pulse)))
        glow_rect = glow.get_rect(center=(SCREEN_WIDTH // 2 + 2, 82))
        screen.blit(glow, glow_rect)
        screen.blit(title, title_rect)
        
        # Player role reveal (center of screen)
        role_data = ROLES[self.player1.role]
        
        # Large role card
        card_width = 400
        card_height = 400
        card_x = SCREEN_WIDTH // 2 - card_width // 2
        card_y = 180
        
        # Animated glow border
        glow_size = int(10 + pulse / 3)
        pygame.draw.rect(screen, role_data["color"], 
                        (card_x - glow_size, card_y - glow_size, card_width + glow_size * 2, card_height + glow_size * 2), 
                        glow_size)
        
        # Card background
        pygame.draw.rect(screen, (30, 30, 40), (card_x, card_y, card_width, card_height))
        pygame.draw.rect(screen, role_data["color"], (card_x, card_y, card_width, card_height), 5)
        
        # Username
        username_text = text_font.render(self.player1.username, True, CYAN)
        username_rect = username_text.get_rect(center=(SCREEN_WIDTH // 2, card_y + 40))
        screen.blit(username_text, username_rect)
        
        # "You are..."
        you_are_text = small_font.render("You are a...", True, LIGHT_GRAY)
        you_are_rect = you_are_text.get_rect(center=(SCREEN_WIDTH // 2, card_y + 80))
        screen.blit(you_are_text, you_are_rect)
        
        # BIG ROLE NAME
        role_name_large = pygame.font.Font(None, 80)
        role_text = role_name_large.render(self.player1.role.upper(), True, role_data["color"])
        role_rect = role_text.get_rect(center=(SCREEN_WIDTH // 2, card_y + 160))
        # Shadow
        role_shadow = role_name_large.render(self.player1.role.upper(), True, BLACK)
        shadow_rect = role_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 3, card_y + 163))
        screen.blit(role_shadow, shadow_rect)
        screen.blit(role_text, role_rect)
        
        # Role description
        desc_y = card_y + 240
        desc_words = role_data["description"].split()
        line = ""
        for word in desc_words:
            test_line = line + word + " "
            if small_font.size(test_line)[0] < card_width - 40:
                line = test_line
            else:
                if line:
                    desc_line = small_font.render(line, True, WHITE)
                    desc_rect = desc_line.get_rect(center=(SCREEN_WIDTH // 2, desc_y))
                    screen.blit(desc_line, desc_rect)
                    desc_y += 30
                line = word + " "
        if line:
            desc_line = small_font.render(line, True, WHITE)
            desc_rect = desc_line.get_rect(center=(SCREEN_WIDTH // 2, desc_y))
            screen.blit(desc_line, desc_rect)
        
        # CPU role (small display in corner)
        if self.is_cpu_mode:
            cpu_role_data = ROLES[self.player2.role]
            cpu_text = tiny_font.render(f"CPU is: {self.player2.role}", True, cpu_role_data["color"])
            screen.blit(cpu_text, (20, SCREEN_HEIGHT - 100))
        
        # Continue prompt (pulsing)
        alpha = int(128 + 127 * abs(math.sin(pygame.time.get_ticks() * 0.005)))
        continue_text = menu_font.render("Press ENTER to Begin Battle", True, (255, 255, 255, alpha))
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        screen.blit(continue_text, continue_rect)
    
    def draw_menu(self):
        # Gradient background
        for y in range(SCREEN_HEIGHT):
            color_val = int(20 + (y / SCREEN_HEIGHT) * 40)
            pygame.draw.line(screen, (color_val, color_val, color_val + 20), (0, y), (SCREEN_WIDTH, y))
        
        # Title with shadow
        title_shadow = title_font.render("BATTLE STREET", True, BLACK)
        title_shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 4, 124))
        screen.blit(title_shadow, title_shadow_rect)
        
        title = title_font.render("BATTLE STREET", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(title, title_rect)
        
        # Menu options with boxes
        options = ["vs CPU", "Host LAN Game", "Join LAN Game", "Shop", "Customize", "Quit"]
        for i, option in enumerate(options):
            y_pos = 220 + i * 70
            
            # Draw button background
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 180, y_pos - 25, 360, 50)
            if i == self.menu_selection:
                pygame.draw.rect(screen, GREEN, button_rect)
                pygame.draw.rect(screen, WHITE, button_rect, 3)
                color = BLACK
            else:
                pygame.draw.rect(screen, DARK_GRAY, button_rect)
                pygame.draw.rect(screen, LIGHT_GRAY, button_rect, 2)
                color = WHITE
            
            text = menu_font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            screen.blit(text, text_rect)
            
        # Instructions
        instructions = small_font.render("Use Arrow Keys to navigate, Enter to select", True, LIGHT_GRAY)
        inst_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 630))
        screen.blit(instructions, inst_rect)
        
    def draw_mode_select(self):
        # Gradient background
        for y in range(SCREEN_HEIGHT):
            color_val = int(20 + (y / SCREEN_HEIGHT) * 40)
            pygame.draw.line(screen, (color_val, color_val, color_val + 20), (0, y), (SCREEN_WIDTH, y))
        
        # Title with shadow
        title_shadow = title_font.render("Select Mode", True, BLACK)
        screen.blit(title_shadow, title_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 4, 154)))
        title = title_font.render("Select Mode", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title, title_rect)
        
        options = ["2 Player Mode", "vs CPU"]
        for i, option in enumerate(options):
            y_pos = 300 + i * 90
            
            # Draw button background
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 180, y_pos - 30, 360, 60)
            if i == self.mode_selection:
                pygame.draw.rect(screen, GREEN, button_rect)
                pygame.draw.rect(screen, WHITE, button_rect, 3)
                color = BLACK
            else:
                pygame.draw.rect(screen, DARK_GRAY, button_rect)
                pygame.draw.rect(screen, LIGHT_GRAY, button_rect, 2)
                color = WHITE
            
            text = menu_font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            screen.blit(text, text_rect)
            
        instructions = small_font.render("Arrow Keys: Navigate | Enter: Select | ESC: Back", True, LIGHT_GRAY)
        inst_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 600))
        screen.blit(instructions, inst_rect)
        
    def draw_battle(self):
        # Get current map data
        map_data = MAPS[self.current_map]
        
        # Sky gradient background
        sky_color = map_data["sky_color"]
        for y in range(SCREEN_HEIGHT - 200):
            ratio = y / (SCREEN_HEIGHT - 200)
            r = int(sky_color[0] + (map_data["bg_color"][0] - sky_color[0]) * ratio)
            g = int(sky_color[1] + (map_data["bg_color"][1] - sky_color[1]) * ratio)
            b = int(sky_color[2] + (map_data["bg_color"][2] - sky_color[2]) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Draw map decorations
        if map_data["decoration"] == "buildings":
            # Draw buildings for Street map
            building_colors = [(100, 100, 120), (80, 80, 100), (120, 120, 140), (90, 90, 110)]
            building_heights = [180, 220, 160, 240, 200, 190]
            for i in range(6):
                bldg_x = i * 180 - 20
                bldg_height = building_heights[i]
                bldg_width = 160
                bldg_y = SCREEN_HEIGHT - 200 - bldg_height
                color = building_colors[i % len(building_colors)]
                pygame.draw.rect(screen, color, (bldg_x, bldg_y, bldg_width, bldg_height))
                pygame.draw.rect(screen, BLACK, (bldg_x, bldg_y, bldg_width, bldg_height), 2)
                # Windows
                for row in range(3, bldg_height // 25):
                    for col in range(2, bldg_width // 30):
                        window_x = bldg_x + col * 30
                        window_y = bldg_y + row * 25
                        is_lit = (i + row + col) % 3 == 0
                        window_color = YELLOW if is_lit else (50, 50, 70)
                        pygame.draw.rect(screen, window_color, (window_x, window_y, 15, 18))
        elif map_data["decoration"] == "cacti":
            # Draw cacti for Desert map
            for i in range(8):
                x = i * 130 + 50
                y = SCREEN_HEIGHT - 250
                # Cactus body
                pygame.draw.rect(screen, GREEN, (x, y, 30, 80))
                pygame.draw.rect(screen, GREEN, (x - 20, y + 20, 20, 30))
                pygame.draw.rect(screen, GREEN, (x + 30, y + 30, 20, 25))
        elif map_data["decoration"] == "trees":
            # Draw trees for Grassland map
            for i in range(10):
                x = i * 105 + 30
                y = SCREEN_HEIGHT - 260
                # Tree trunk
                pygame.draw.rect(screen, (101, 67, 33), (x, y + 30, 20, 40))
                # Tree foliage
                pygame.draw.circle(screen, (34, 139, 34), (x + 10, y + 20), 35)
        elif map_data["decoration"] == "pillars":
            # Draw pillars for Arena map
            for i in range(6):
                x = i * 180 + 60
                y = SCREEN_HEIGHT - 350
                # Pillar
                pygame.draw.rect(screen, (150, 150, 150), (x, y, 50, 150))
                pygame.draw.rect(screen, (120, 120, 120), (x + 10, y + 10, 30, 130))
                pygame.draw.rect(screen, (180, 180, 180), (x, y, 50, 20))
        
        # Draw ground
        ground_color = map_data["ground_color"]
        pygame.draw.rect(screen, ground_color, (0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 40))
        pygame.draw.rect(screen, tuple(max(0, c - 30) for c in ground_color), (0, SCREEN_HEIGHT - 160, SCREEN_WIDTH, 40))
        pygame.draw.rect(screen, tuple(max(0, c - 50) for c in ground_color), (0, SCREEN_HEIGHT - 120, SCREEN_WIDTH, 120))
        
        # Draw road lines for Street map only
        if self.current_map == "Street":
            for i in range(0, SCREEN_WIDTH, 60):
                pygame.draw.rect(screen, YELLOW, (i, SCREEN_HEIGHT - 65, 40, 5))
            pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - 125, SCREEN_WIDTH, 3))
            pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 3))
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(screen)
        
        # Draw collectibles
        for collectible in self.collectibles:
            collectible.draw(screen)
        
        # Draw Engineer barriers
        for player in self.all_players:
            if player.role == "Engineer":
                for structure in player.structures:
                    if structure["type"] == "barrier":
                        # Draw wooden barrier
                        pygame.draw.rect(screen, (139, 69, 19), (structure["x"], structure["y"], structure["width"], structure["height"]))
                        pygame.draw.rect(screen, (101, 67, 33), (structure["x"], structure["y"], structure["width"], structure["height"]), 3)
                        # Health bar on barrier
                        health_ratio = structure["health"] / 50
                        pygame.draw.rect(screen, RED, (structure["x"], structure["y"] - 10, structure["width"], 5))
                        pygame.draw.rect(screen, GREEN, (structure["x"], structure["y"] - 10, structure["width"] * health_ratio, 5))
        
        # Draw trapped player cages
        for player in self.all_players:
            if player.is_trapped:
                # Draw cage bars
                cage_width = player.width + 20
                cage_height = player.height + 30
                cage_x = player.cage_x - 10
                cage_y = player.cage_y - 15
                
                # Cage background
                pygame.draw.rect(screen, (50, 50, 50, 100), (cage_x, cage_y, cage_width, cage_height))
                
                # Vertical bars
                for i in range(5):
                    bar_x = cage_x + i * (cage_width // 4)
                    pygame.draw.rect(screen, (80, 80, 80), (bar_x, cage_y, 5, cage_height))
                
                # Horizontal bars
                for i in range(4):
                    bar_y = cage_y + i * (cage_height // 3)
                    pygame.draw.rect(screen, (80, 80, 80), (cage_x, bar_y, cage_width, 5))
                
                # Timer display
                time_left = player.trap_timer / 60  # Convert to seconds
                timer_text = tiny_font.render(f"{time_left:.1f}s", True, RED)
                screen.blit(timer_text, (player.cage_x, player.cage_y - 35))
         
        for player in self.all_players:
            # Ghost mode: only draw if alive OR if viewer is also dead/ghost
            should_draw = False
            if player.health > 0:
                should_draw = True  # Alive players always visible
            elif self.team_mode_enabled and player.is_ghost:
                # Ghosts only visible to other dead players (or themselves)
                if self.player1.is_ghost or player == self.player1:
                    should_draw = True
            
            if should_draw:
                # Draw with transparency if ghost
                if player.is_ghost:
                    # Create semi-transparent surface
                    ghost_surface = pygame.Surface((player.width, player.height), pygame.SRCALPHA)
                    ghost_surface.fill((*player.color, 100))  # 100 = semi-transparent
                    screen.blit(ghost_surface, (player.x, player.y))
                    
                    # Draw ghost label
                    ghost_text = tiny_font.render("👻 GHOST", True, (150, 150, 255))
                    screen.blit(ghost_text, (player.x, player.y - 50))
                else:
                    player.draw(screen)
                
                # Draw username above player
                username_text = small_font.render(player.username, True, WHITE)
                username_rect = username_text.get_rect(center=(player.x + player.width // 2, player.y - 30))
                # Background for username
                bg_rect = pygame.Rect(username_rect.x - 5, username_rect.y - 2, username_rect.width + 10, username_rect.height + 4)
                pygame.draw.rect(screen, BLACK, bg_rect)
                pygame.draw.rect(screen, ROLES[player.role]["color"], bg_rect, 2)
                screen.blit(username_text, username_rect)
                
                # Draw role badge
                role_text = tiny_font.render(player.role, True, ROLES[player.role]["color"])
                role_rect = role_text.get_rect(center=(player.x + player.width // 2, player.y - 12))
                screen.blit(role_text, role_rect)
                
        # Draw projectiles and explosions for all players
        for player in self.all_players:
            for proj in player.projectiles:
                proj.draw(screen)
            for explosion in player.explosions:
                explosion.draw(screen)
            
        # Draw player info panels with backgrounds
        # Player 1 panel (local player)
        pygame.draw.rect(screen, (0, 0, 0, 128), (0, 0, 280, 80))
        pygame.draw.rect(screen, BLACK, (5, 5, 270, 70), 2)
        
        if self.is_network_game:
            p1_label = text_font.render(f"You (P1)", True, RED)
        else:
            p1_label = text_font.render(f"P1 Coins: {self.player1.coins}", True, YELLOW)
        screen.blit(p1_label, (15, 12))
        
        p1_weapon = small_font.render(f"Weapon: {self.player1.weapon}", True, WHITE)
        screen.blit(p1_weapon, (15, 45))
        
        # Opponent panel
        pygame.draw.rect(screen, (0, 0, 0, 128), (SCREEN_WIDTH - 250, 0, 250, 80))
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 245, 5, 240, 70), 2)
        
        if self.is_network_game:
            opponent_label = text_font.render(f"Opponent", True, CYAN)
        else:
            opponent_label = text_font.render(f"CPU", True, CYAN)
        screen.blit(opponent_label, (SCREEN_WIDTH - 200, 12))
        
        p2_weapon = small_font.render(f"Weapon: {self.player2.weapon}", True, WHITE)
        screen.blit(p2_weapon, (SCREEN_WIDTH - 240, 45))
        
        # Engineer wood inventory and buy button
        if self.player1.role == "Engineer":
            button_x = SCREEN_WIDTH - 180
            button_y = 100
            button_width = 160
            button_height = 60
            
            # Draw button background
            pygame.draw.rect(screen, (80, 50, 20), (button_x, button_y, button_width, button_height))
            pygame.draw.rect(screen, YELLOW, (button_x, button_y, button_width, button_height), 3)
            
            # Wood inventory display
            wood_text = small_font.render(f"Wood: {int(self.player1.build_resources)}", True, WHITE)
            screen.blit(wood_text, (button_x + 10, button_y + 8))
            
            # Buy button text
            buy_text = tiny_font.render("Press B: Buy Wood", True, YELLOW)
            screen.blit(buy_text, (button_x + 10, button_y + 32))
            cost_text = tiny_font.render("(25 coins)", True, LIGHT_GRAY)
            screen.blit(cost_text, (button_x + 35, button_y + 48))
        
        # Draw controls at bottom with background
        pygame.draw.rect(screen, (0, 0, 0, 128), (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40))
        
        # Update controls text based on vehicle
        if self.player1.vehicle == "Ship" or self.player1.vehicle == "Rocket":
            controls1 = tiny_font.render("A/D=Move | W/S=Up/Down | Click=Shoot | ESC=Menu", True, WHITE)
        else:
            controls1 = tiny_font.render("A/D=Move | Space=Jump | Click=Shoot | ESC=Menu", True, WHITE)
        controls_rect = controls1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 28))
        screen.blit(controls1, controls_rect)
        
        # Draw minimap for Ship vehicle
        if self.player1.vehicle == "Ship":
            self.draw_minimap()
        
    def draw_minimap(self):
        """Draw minimap for the Ship vehicle showing exterior view"""
        # Minimap dimensions and position (bottom-right corner)
        minimap_width = 200
        minimap_height = 150
        minimap_x = SCREEN_WIDTH - minimap_width - 20
        minimap_y = SCREEN_HEIGHT - minimap_height - 60
        
        # Draw minimap background
        pygame.draw.rect(screen, (20, 20, 40), (minimap_x, minimap_y, minimap_width, minimap_height))
        pygame.draw.rect(screen, YELLOW, (minimap_x, minimap_y, minimap_width, minimap_height), 3)
        
        # Draw minimap title
        minimap_title = tiny_font.render("RADAR", True, YELLOW)
        screen.blit(minimap_title, (minimap_x + 5, minimap_y + 5))
        
        # Calculate scaling factor for minimap
        scale_x = minimap_width / SCREEN_WIDTH
        scale_y = minimap_height / SCREEN_HEIGHT
        
        # Draw players on minimap
        for i, player in enumerate(self.all_players):
            if player.health > 0:
                mini_x = minimap_x + int(player.x * scale_x)
                mini_y = minimap_y + int(player.y * scale_y)
                
                # Draw player marker
                if player == self.player1:
                    pygame.draw.circle(screen, GREEN, (mini_x, mini_y), 6)
                    pygame.draw.circle(screen, WHITE, (mini_x, mini_y), 6, 1)
                else:
                    pygame.draw.circle(screen, RED, (mini_x, mini_y), 5)
        
        # Draw collectibles on minimap
        for collectible in self.collectibles:
            mini_x = minimap_x + int(collectible.x * scale_x)
            mini_y = minimap_y + int(collectible.y * scale_y)
            if collectible.type == "coin":
                pygame.draw.circle(screen, YELLOW, (mini_x, mini_y), 2)
            else:
                pygame.draw.circle(screen, CYAN, (mini_x, mini_y), 2)
        
        # Draw grid lines
        for i in range(1, 4):
            # Vertical lines
            grid_x = minimap_x + i * (minimap_width // 4)
            pygame.draw.line(screen, (40, 40, 60), (grid_x, minimap_y), (grid_x, minimap_y + minimap_height))
            # Horizontal lines
            grid_y = minimap_y + i * (minimap_height // 4)
            pygame.draw.line(screen, (40, 40, 60), (minimap_x, grid_y), (minimap_x + minimap_width, grid_y))
        
    def draw_shop(self):
        # Gradient background
        for y in range(SCREEN_HEIGHT):
            color_val = int(40 + (y / SCREEN_HEIGHT) * 30)
            pygame.draw.line(screen, (color_val, color_val + 10, color_val + 20), (0, y), (SCREEN_WIDTH, y))
        
        # Title with shadow
        title_shadow = title_font.render("SHOP", True, BLACK)
        screen.blit(title_shadow, title_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 4, 44)))
        title = title_font.render("SHOP", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 40))
        screen.blit(title, title_rect)
        
        # Tab buttons
        tab_names = ["WEAPONS", "VEHICLES", "POWERS", "COSMETICS"]
        tab_width = 180
        tab_height = 40
        tab_y = 90
        tab_spacing = 15
        total_tab_width = len(tab_names) * tab_width + (len(tab_names) - 1) * tab_spacing
        start_x = (SCREEN_WIDTH - total_tab_width) // 2
        
        for i, tab_name in enumerate(tab_names):
            tab_x = start_x + i * (tab_width + tab_spacing)
            tab_rect = pygame.Rect(tab_x, tab_y, tab_width, tab_height)
            
            # Draw tab
            if i == self.shop_tab:
                pygame.draw.rect(screen, YELLOW, tab_rect)
                tab_color = BLACK
                pygame.draw.rect(screen, WHITE, tab_rect, 3)
            else:
                pygame.draw.rect(screen, (60, 60, 80), tab_rect)
                tab_color = WHITE
                pygame.draw.rect(screen, LIGHT_GRAY, tab_rect, 2)
            
            tab_text = text_font.render(tab_name, True, tab_color)
            text_rect = tab_text.get_rect(center=tab_rect.center)
            screen.blit(tab_text, text_rect)
        
        # Player info panel
        player = self.player1
        info_rect = pygame.Rect(50, 145, SCREEN_WIDTH - 100, 60)
        pygame.draw.rect(screen, (50, 50, 70), info_rect)
        pygame.draw.rect(screen, YELLOW, info_rect, 2)
        
        coin_text = text_font.render(f"Coins: {player.coins}", True, YELLOW)
        screen.blit(coin_text, (70, 155))
        
        if self.shop_tab == 0:  # Weapons
            current = small_font.render(f"Weapon: {player.weapon}", True, GREEN)
        elif self.shop_tab == 1:  # Vehicles
            current = small_font.render(f"Vehicle: {VEHICLES[player.vehicle]['name']}", True, GREEN)
        elif self.shop_tab == 2:  # Powers
            current = small_font.render(f"Powers: Coming Soon!", True, GREEN)
        elif self.shop_tab == 3:  # Cosmetics
            hat_name = player.hat if player.hat else "None"
            current = small_font.render(f"Hat: {hat_name}", True, GREEN)
        screen.blit(current, (70, 180))
        
        # Build items list based on current tab
        items = []
        if self.shop_tab == 0:  # Weapons tab
            for weapon_name, weapon_data in WEAPONS.items():
                items.append(("weapon", weapon_name, weapon_data))
            for upgrade_name, upgrade_data in UPGRADES.items():
                items.append(("upgrade", upgrade_name, upgrade_data))
        elif self.shop_tab == 1:  # Vehicles tab
            for vehicle_name, vehicle_data in VEHICLES.items():
                items.append(("vehicle", vehicle_name, vehicle_data))
        elif self.shop_tab == 2:  # Powers tab
            for power_name, power_data in POWERS.items():
                items.append(("power", power_name, power_data))
        elif self.shop_tab == 3:  # Cosmetics tab
            for cosmetic_name, cosmetic_data in COSMETICS.items():
                items.append(("cosmetic", cosmetic_name, cosmetic_data))
        
        # Define scrollable area
        list_start_y = 220
        list_height = SCREEN_HEIGHT - 290
        item_height = 60
        visible_items = list_height // item_height
        
        # Auto-scroll to keep selection visible
        if self.shop_selection < self.shop_scroll_offset:
            self.shop_scroll_offset = self.shop_selection
        elif self.shop_selection >= self.shop_scroll_offset + visible_items:
            self.shop_scroll_offset = self.shop_selection - visible_items + 1
        
        # Draw scrollable list background
        list_rect = pygame.Rect(50, list_start_y, SCREEN_WIDTH - 100, list_height)
        pygame.draw.rect(screen, (30, 30, 40), list_rect)
        pygame.draw.rect(screen, LIGHT_GRAY, list_rect, 2)
        
        # Draw items with clipping
        for i in range(self.shop_scroll_offset, min(len(items), self.shop_scroll_offset + visible_items + 1)):
            item_type, item_name, item_data = items[i]
            y_pos = list_start_y + (i - self.shop_scroll_offset) * item_height + 5
            
            # Don't draw items outside the list area
            if y_pos >= list_start_y and y_pos < list_start_y + list_height - item_height:
                item_rect = pygame.Rect(60, y_pos, SCREEN_WIDTH - 120, item_height - 5)
                
                # Highlight selected item
                if i == self.shop_selection:
                    pygame.draw.rect(screen, GREEN, item_rect)
                    pygame.draw.rect(screen, WHITE, item_rect, 2)
                    text_color = BLACK
                else:
                    pygame.draw.rect(screen, (50, 50, 60), item_rect)
                    text_color = WHITE
                
                # Draw item info based on type
                if item_type == "weapon":
                    owned_weapons = getattr(player, 'owned_weapons', [player.weapon])
                    is_owned = item_name in owned_weapons
                    is_equipped = player.weapon == item_name
                    
                    status = " [EQUIPPED]" if is_equipped else (" [OWNED]" if is_owned else "")
                    name_text = small_font.render(f"{item_name}{status}", True, text_color)
                    screen.blit(name_text, (70, y_pos + 5))
                    
                    stats_text = tiny_font.render(
                        f"Damage: {item_data['damage']} | Speed: {item_data['speed']} | Cost: {item_data['cost']} coins",
                        True, text_color
                    )
                    screen.blit(stats_text, (70, y_pos + 32))
                elif item_type == "vehicle":
                    owned_vehicles = getattr(player, 'owned_vehicles', ["None"])
                    is_owned = item_name in owned_vehicles
                    is_equipped = player.vehicle == item_name
                    
                    status = " [ACTIVE]" if is_equipped else (" [OWNED]" if is_owned else "")
                    name_text = small_font.render(f"{item_data['name']}{status}", True, text_color)
                    screen.blit(name_text, (70, y_pos + 5))
                    
                    stats_text = tiny_font.render(
                        f"HP: x{item_data['health_multiplier']} | Speed: x{item_data['speed_multiplier']} | "
                        f"{'CAN FLY' if item_data['can_fly'] else 'GROUND'} | Cost: {item_data['cost']} coins",
                        True, text_color
                    )
                    screen.blit(stats_text, (70, y_pos + 32))
                elif item_type == "power":
                    name_text = small_font.render(f"{item_name}", True, text_color)
                    screen.blit(name_text, (70, y_pos + 5))
                    
                    stats_text = tiny_font.render(
                        f"{item_data['description']} | Cost: {item_data['cost']} coins",
                        True, text_color
                    )
                    screen.blit(stats_text, (70, y_pos + 32))
                elif item_type == "cosmetic":
                    # Check if cosmetic is owned/equipped
                    is_owned = item_name in player.owned_cosmetics
                    cosmetic_type = item_data['type']
                    is_equipped = False
                    if cosmetic_type == "hat":
                        is_equipped = player.hat == item_name
                    elif cosmetic_type == "skin":
                        is_equipped = player.skin == item_name
                    elif cosmetic_type == "visor":
                        is_equipped = player.visor == item_name
                    
                    status = " [EQUIPPED]" if is_equipped else (" [OWNED]" if is_owned else "")
                    name_text = small_font.render(f"{item_name}{status}", True, text_color)
                    screen.blit(name_text, (70, y_pos + 5))
                    
                    stats_text = tiny_font.render(
                        f"{item_data['type'].title()} - {item_data['description']} | Cost: {item_data['cost']} coins",
                        True, text_color
                    )
                    screen.blit(stats_text, (70, y_pos + 32))
                else:  # upgrade
                    name_text = small_font.render(f"{item_name}", True, text_color)
                    screen.blit(name_text, (70, y_pos + 5))
                    
                    stats_text = tiny_font.render(
                        f"{item_data['effect'].title()}: +{item_data['value']} | Cost: {item_data['cost']} coins",
                        True, text_color
                    )
                    screen.blit(stats_text, (70, y_pos + 32))
        
        # Draw scroll indicator
        if len(items) > visible_items:
            scroll_bar_height = max(30, int((visible_items / len(items)) * list_height))
            scroll_bar_y = list_start_y + int((self.shop_scroll_offset / len(items)) * list_height)
            pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH - 70, scroll_bar_y, 10, scroll_bar_height))
        
        # Instructions at bottom
        inst_bg = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
        pygame.draw.rect(screen, (20, 20, 30), inst_bg)
        if self.shop_tab == 0:
            inst = tiny_font.render("←→: Switch Tab | ↑↓: Navigate | B: Buy | E: Equip | ESC: Menu", True, WHITE)
        else:
            inst = tiny_font.render("←→: Switch Tab | ↑↓: Navigate | B: Buy | E: Equip/Activate | ESC: Menu", True, WHITE)
        inst_rect = inst.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 25))
        screen.blit(inst, inst_rect)
        
    def draw_win_screen(self):
        # Victory gradient background
        for y in range(SCREEN_HEIGHT):
            green_val = int(50 + (y / SCREEN_HEIGHT) * 100)
            pygame.draw.line(screen, (20, green_val, 20), (0, y), (SCREEN_WIDTH, y))
        
        # Victory banner
        banner_rect = pygame.Rect(100, 100, SCREEN_WIDTH - 200, 100)
        pygame.draw.rect(screen, GREEN, banner_rect)
        pygame.draw.rect(screen, YELLOW, banner_rect, 5)
        
        # Winner text
        winner_text = title_font.render(f"{self.winner} WON!", True, YELLOW)
        screen.blit(winner_text, winner_text.get_rect(center=(SCREEN_WIDTH // 2, 150)))
        
        # Loser text at top
        if self.loser:
            loser_small = text_font.render(f"{self.loser} Lost", True, RED)
            screen.blit(loser_small, loser_small.get_rect(center=(SCREEN_WIDTH // 2, 220)))
        
        # Stats panel
        stats_rect = pygame.Rect(200, 280, SCREEN_WIDTH - 400, 220)
        pygame.draw.rect(screen, (50, 80, 50), stats_rect)
        pygame.draw.rect(screen, WHITE, stats_rect, 3)
        
        # Coins earned
        coins_text = title_font.render(f"+{self.coins_earned} Coins!", True, YELLOW)
        screen.blit(coins_text, coins_text.get_rect(center=(SCREEN_WIDTH // 2, 350)))
        
        # Total coins
        total_text = text_font.render(f"Total Coins: {self.player1.coins}", True, WHITE)
        screen.blit(total_text, total_text.get_rect(center=(SCREEN_WIDTH // 2, 420)))
        
        # Continue message
        continue_text = small_font.render("Press ESC to return to menu", True, LIGHT_GRAY)
        screen.blit(continue_text, continue_text.get_rect(center=(SCREEN_WIDTH // 2, 460)))
        
    def draw_lose_screen(self):
        # Defeat gradient background
        for y in range(SCREEN_HEIGHT):
            red_val = int(80 + (y / SCREEN_HEIGHT) * 60)
            pygame.draw.line(screen, (red_val, 20, 20), (0, y), (SCREEN_WIDTH, y))
        
        # Defeat banner
        banner_rect = pygame.Rect(100, 100, SCREEN_WIDTH - 200, 100)
        pygame.draw.rect(screen, RED, banner_rect)
        pygame.draw.rect(screen, DARK_GRAY, banner_rect, 5)
        
        # Loser text (Player 1 lost)
        loser_text = title_font.render(f"{self.loser} LOST", True, WHITE)
        screen.blit(loser_text, loser_text.get_rect(center=(SCREEN_WIDTH // 2, 150)))
        
        # Winner text at bottom of banner
        if self.winner:
            winner_small = text_font.render(f"{self.winner} Won!", True, GREEN)
            screen.blit(winner_small, winner_small.get_rect(center=(SCREEN_WIDTH // 2, 220)))
        
        # Stats panel
        stats_rect = pygame.Rect(200, 280, SCREEN_WIDTH - 400, 220)
        pygame.draw.rect(screen, (80, 40, 40), stats_rect)
        pygame.draw.rect(screen, WHITE, stats_rect, 3)
        
        # Coins lost
        if self.coins_lost > 0:
            lost_text = title_font.render(f"-{self.coins_lost} Coins", True, ORANGE)
            screen.blit(lost_text, lost_text.get_rect(center=(SCREEN_WIDTH // 2, 350)))
        else:
            lost_text = text_font.render("No coins lost!", True, GREEN)
            screen.blit(lost_text, lost_text.get_rect(center=(SCREEN_WIDTH // 2, 350)))
        
        # Total coins
        total_text = text_font.render(f"Total Coins: {self.player1.coins}", True, WHITE)
        screen.blit(total_text, total_text.get_rect(center=(SCREEN_WIDTH // 2, 420)))
        
        # Continue message
        continue_text = small_font.render("Press ESC to return to menu", True, LIGHT_GRAY)
        screen.blit(continue_text, continue_text.get_rect(center=(SCREEN_WIDTH // 2, 460)))
        
    def handle_username_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Proceed to main menu if username is entered
                if self.player_username.strip():
                    self.player1.username = self.player_username
                    print(f"✨ Welcome, {self.player_username}!")
                    self.save_progress()  # Save the new username
                    self.state = GameState.MENU
                    self.username_input_active = False
                else:
                    self.show_username_error = True
            elif event.key == pygame.K_BACKSPACE:
                self.player_username = self.player_username[:-1]
                if hasattr(self, 'show_username_error'):
                    delattr(self, 'show_username_error')
            elif event.key == pygame.K_ESCAPE:
                # Allow going back to menu if we already have a username
                if self.has_saved_username:
                    self.state = GameState.MENU
                    self.username_input_active = False
                else:
                    # Can't escape - username is required for first time
                    self.show_username_error = True
            elif len(self.player_username) < 15:  # Max 15 characters
                # Only allow alphanumeric and some special characters
                if event.unicode.isprintable() and event.unicode not in ['<', '>', '/', '\\', '|']:
                    self.player_username += event.unicode
                    if hasattr(self, 'show_username_error'):
                        delattr(self, 'show_username_error')
    
    def draw_customize(self):
        # Gradient background
        for y in range(SCREEN_HEIGHT):
            color_val = int(30 + (y / SCREEN_HEIGHT) * 50)
            pygame.draw.line(screen, (color_val + 10, color_val + 30, color_val + 10), (0, y), (SCREEN_WIDTH, y))
        
        # Title
        title = title_font.render("CUSTOMIZE", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        # Tab buttons
        tab_names = ["USERNAME", "HATS", "SKINS", "VISORS"]
        tab_width = 180
        tab_height = 40
        tab_y = 110
        tab_spacing = 20
        total_width = len(tab_names) * tab_width + (len(tab_names) - 1) * tab_spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        for i, tab_name in enumerate(tab_names):
            tab_x = start_x + i * (tab_width + tab_spacing)
            tab_rect = pygame.Rect(tab_x, tab_y, tab_width, tab_height)
            
            if i == self.customize_tab:
                pygame.draw.rect(screen, YELLOW, tab_rect)
                tab_color = BLACK
                pygame.draw.rect(screen, WHITE, tab_rect, 3)
            else:
                pygame.draw.rect(screen, DARK_GRAY, tab_rect)
                tab_color = WHITE
                pygame.draw.rect(screen, LIGHT_GRAY, tab_rect, 2)
            
            tab_text = small_font.render(tab_name, True, tab_color)
            tab_text_rect = tab_text.get_rect(center=(tab_x + tab_width // 2, tab_y + tab_height // 2))
            screen.blit(tab_text, tab_text_rect)
        
        # Content area
        content_y = 180
        
        if self.customize_tab == 0:  # Username
            # Username editing
            inst = menu_font.render("Change Your Username:", True, WHITE)
            inst_rect = inst.get_rect(center=(SCREEN_WIDTH // 2, content_y))
            screen.blit(inst, inst_rect)
            
            # Input box
            input_box_width = 400
            input_box_height = 60
            input_box_x = SCREEN_WIDTH // 2 - input_box_width // 2
            input_box_y = content_y + 70
            
            pygame.draw.rect(screen, WHITE, (input_box_x, input_box_y, input_box_width, input_box_height))
            pygame.draw.rect(screen, YELLOW, (input_box_x, input_box_y, input_box_width, input_box_height), 4)
            
            username_text = text_font.render(self.player_username, True, BLACK)
            username_rect = username_text.get_rect(midleft=(input_box_x + 15, input_box_y + input_box_height // 2))
            screen.blit(username_text, username_rect)
            
            # Cursor
            if int(pygame.time.get_ticks() / 500) % 2 == 0:
                cursor_x = username_rect.right + 5
                pygame.draw.line(screen, BLACK, (cursor_x, input_box_y + 15), (cursor_x, input_box_y + input_box_height - 15), 3)
            
            hint = small_font.render("Type to edit, ENTER to save", True, LIGHT_GRAY)
            screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, input_box_y + 80))
            
        else:  # Hats, Skins, or Visors
            # Filter cosmetics by type
            cosmetic_type_map = {1: "hat", 2: "skin", 3: "visor"}
            filter_type = cosmetic_type_map[self.customize_tab]
            
            filtered_cosmetics = [(name, data) for name, data in COSMETICS.items() if data['type'] == filter_type]
            
            if not filtered_cosmetics:
                no_items = text_font.render("No items in this category", True, WHITE)
                screen.blit(no_items, (SCREEN_WIDTH // 2 - no_items.get_width() // 2, content_y + 100))
            else:
                # Display cosmetics as cards
                card_width = 200
                card_height = 220
                cards_per_row = 4
                card_spacing = 20
                start_x = (SCREEN_WIDTH - (cards_per_row * card_width + (cards_per_row - 1) * card_spacing)) // 2
                
                for idx, (cosmetic_name, cosmetic_data) in enumerate(filtered_cosmetics):
                    row = idx // cards_per_row
                    col = idx % cards_per_row
                    
                    card_x = start_x + col * (card_width + card_spacing)
                    card_y = content_y + row * (card_height + card_spacing)
                    
                    # Check if owned/equipped
                    is_owned = cosmetic_name in self.player1.owned_cosmetics
                    is_equipped = False
                    if filter_type == "hat":
                        is_equipped = self.player1.hat == cosmetic_name
                    elif filter_type == "skin":
                        is_equipped = self.player1.skin == cosmetic_name
                    elif filter_type == "visor":
                        is_equipped = self.player1.visor == cosmetic_name
                    
                    # Highlight selected
                    if idx == self.customize_selection:
                        pygame.draw.rect(screen, YELLOW, (card_x - 5, card_y - 5, card_width + 10, card_height + 10), 4)
                    
                    # Card background
                    if is_equipped:
                        pygame.draw.rect(screen, (50, 100, 50), (card_x, card_y, card_width, card_height))
                    elif is_owned:
                        pygame.draw.rect(screen, (50, 50, 80), (card_x, card_y, card_width, card_height))
                    else:
                        pygame.draw.rect(screen, (40, 40, 50), (card_x, card_y, card_width, card_height))
                    
                    pygame.draw.rect(screen, cosmetic_data['color'], (card_x, card_y, card_width, card_height), 3)
                    
                    # Item name
                    name_text = small_font.render(cosmetic_name, True, cosmetic_data['color'])
                    name_rect = name_text.get_rect(center=(card_x + card_width // 2, card_y + 30))
                    screen.blit(name_text, name_rect)
                    
                    # Status
                    if is_equipped:
                        status_text = tiny_font.render("[EQUIPPED]", True, GREEN)
                    elif is_owned:
                        status_text = tiny_font.render("[OWNED]", True, CYAN)
                    else:
                        status_text = tiny_font.render(f"{cosmetic_data['cost']} coins", True, YELLOW)
                    status_rect = status_text.get_rect(center=(card_x + card_width // 2, card_y + 60))
                    screen.blit(status_text, status_rect)
                    
                    # Preview (color square)
                    preview_size = 60
                    preview_x = card_x + card_width // 2 - preview_size // 2
                    preview_y = card_y + 90
                    pygame.draw.rect(screen, cosmetic_data['color'], (preview_x, preview_y, preview_size, preview_size))
                    pygame.draw.rect(screen, WHITE, (preview_x, preview_y, preview_size, preview_size), 2)
                    
                    # Description
                    desc = tiny_font.render(cosmetic_data['description'][:25], True, WHITE)
                    desc_rect = desc.get_rect(center=(card_x + card_width // 2, card_y + 175))
                    screen.blit(desc, desc_rect)
        
        # Instructions
        inst_bg = pygame.Rect(0, SCREEN_HEIGHT - 60, SCREEN_WIDTH, 60)
        pygame.draw.rect(screen, (20, 20, 30), inst_bg)
        
        if self.customize_tab == 0:
            inst = small_font.render("←→: Switch Tab | Type to edit | ENTER: Save | ESC: Back to Menu", True, WHITE)
        else:
            inst = small_font.render("←→: Switch Tab | ↑↓←→: Navigate | B: Buy | E: Equip | ESC: Back to Menu", True, WHITE)
        screen.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, SCREEN_HEIGHT - 30))
    
    def handle_customize_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Return to menu
                self.state = GameState.MENU
            elif event.key == pygame.K_LEFT:
                self.customize_tab = (self.customize_tab - 1) % 4
                self.customize_selection = 0
            elif event.key == pygame.K_RIGHT:
                self.customize_tab = (self.customize_tab + 1) % 4
                self.customize_selection = 0
            
            # Handle based on tab
            if self.customize_tab == 0:  # Username editing
                if event.key == pygame.K_RETURN:
                    if self.player_username.strip():
                        self.player1.username = self.player_username
                        self.save_progress()
                        print(f"✅ Username updated to: {self.player_username}")
                elif event.key == pygame.K_BACKSPACE:
                    self.player_username = self.player_username[:-1]
                elif len(self.player_username) < 15:
                    if event.unicode.isprintable() and event.unicode not in ['<', '>', '/', '\\', '|']:
                        self.player_username += event.unicode
            else:  # Cosmetics tabs
                cosmetic_type_map = {1: "hat", 2: "skin", 3: "visor"}
                filter_type = cosmetic_type_map[self.customize_tab]
                filtered_cosmetics = [(name, data) for name, data in COSMETICS.items() if data['type'] == filter_type]
                
                if filtered_cosmetics:
                    num_items = len(filtered_cosmetics)
                    
                    if event.key == pygame.K_UP:
                        self.customize_selection = (self.customize_selection - 4) % num_items
                    elif event.key == pygame.K_DOWN:
                        self.customize_selection = (self.customize_selection + 4) % num_items
                    elif event.key == pygame.K_LEFT and self.customize_tab != 0:
                        self.customize_selection = max(0, self.customize_selection - 1)
                    elif event.key == pygame.K_RIGHT and self.customize_tab != 0:
                        self.customize_selection = min(num_items - 1, self.customize_selection + 1)
                    elif event.key == pygame.K_b:
                        # Buy cosmetic
                        if self.customize_selection < num_items:
                            cosmetic_name, cosmetic_data = filtered_cosmetics[self.customize_selection]
                            if cosmetic_name not in self.player1.owned_cosmetics:
                                if self.player1.coins >= cosmetic_data['cost']:
                                    self.player1.coins -= cosmetic_data['cost']
                                    self.player1.owned_cosmetics.append(cosmetic_name)
                                    self.save_progress()
                                    print(f"✅ Purchased {cosmetic_name}!")
                                else:
                                    print(f"❌ Not enough coins! Need {cosmetic_data['cost']}, have {self.player1.coins}")
                            else:
                                print(f"Already own {cosmetic_name}")
                    elif event.key == pygame.K_e:
                        # Equip cosmetic
                        if self.customize_selection < num_items:
                            cosmetic_name, cosmetic_data = filtered_cosmetics[self.customize_selection]
                            if cosmetic_name in self.player1.owned_cosmetics:
                                if filter_type == "hat":
                                    self.player1.hat = cosmetic_name
                                elif filter_type == "skin":
                                    self.player1.skin = cosmetic_name
                                elif filter_type == "visor":
                                    self.player1.visor = cosmetic_name
                                self.save_progress()
                                print(f"✅ Equipped {cosmetic_name}!")
                            else:
                                print(f"❌ Don't own {cosmetic_name} yet!")
    
    def handle_role_select_input(self, event):
        # Role reveal screen - press any key to continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Continue to battle
                self.state = GameState.BATTLE
    
    def handle_menu_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu_selection = (self.menu_selection - 1) % 6
            elif event.key == pygame.K_DOWN:
                self.menu_selection = (self.menu_selection + 1) % 6
            elif event.key == pygame.K_RETURN:
                if self.menu_selection == 0:  # vs CPU
                    self.is_cpu_mode = True
                    self.is_network_game = False
                    self.taken_colors = []
                    self.state = GameState.COLOR_SELECT  # Go to color selection first
                elif self.menu_selection == 1:  # Host LAN Game
                    self.start_host()
                elif self.menu_selection == 2:  # Join LAN Game
                    self.start_server_browser()
                elif self.menu_selection == 3:  # Shop
                    self.state = GameState.SHOP
                    self.shop_selection = 0
                    self.shop_scroll_offset = 0
                elif self.menu_selection == 4:  # Customize
                    # Open customize menu
                    self.customize_tab = 0
                    self.customize_selection = 0
                    self.state = GameState.CUSTOMIZE
                elif self.menu_selection == 5:  # Quit
                    return False
        return True
        
    def handle_mode_select_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.mode_selection = (self.mode_selection - 1) % 2
            elif event.key == pygame.K_DOWN:
                self.mode_selection = (self.mode_selection + 1) % 2
            elif event.key == pygame.K_RETURN:
                if self.mode_selection == 0:
                    self.is_cpu_mode = False
                else:
                    self.is_cpu_mode = True
                self.reset_battle()
                self.state = GameState.BATTLE
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU
                
    def handle_battle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.network_running = False  # Stop network sync
                self.state = GameState.MENU
            elif event.key == pygame.K_b and self.player1.role == "Engineer":
                # Buy wood for Engineer
                wood_cost = 25
                if self.player1.coins >= wood_cost:
                    self.player1.coins -= wood_cost
                    self.player1.build_resources += 10
                    print(f"✅ Purchased 10 wood! Total: {int(self.player1.build_resources)}")
                    self.save_progress()
                else:
                    print(f"❌ Not enough coins! Need {wood_cost}, have {self.player1.coins}")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse click - shoot
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Shoot with YOUR player (based on player index)
                if self.is_network_game and self.my_player_index < len(self.all_players):
                    my_player = self.all_players[self.my_player_index]
                    my_player.shoot(mouse_x, mouse_y)
                else:
                    # CPU mode - player1 shoots
                    self.player1.shoot(mouse_x, mouse_y)
                    
            elif event.button == 3:  # Right mouse click - Engineer build
                if self.player1.role == "Engineer" and self.player1.build_resources >= 10:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Build a defensive structure (barrier)
                    structure = {
                        "type": "barrier",
                        "x": mouse_x - 25,
                        "y": mouse_y - 50,
                        "width": 50,
                        "height": 100,
                        "health": 50
                    }
                    self.player1.structures.append(structure)
                    self.player1.build_resources -= 10
                    print(f"🔨 Built barrier! Resources left: {int(self.player1.build_resources)}")
                elif self.player1.role == "Trapper" and self.player1.trap_cooldown_timer <= 0:
                    # Trap nearest enemy
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Find enemy near click position
                    for enemy in self.all_players:
                        if enemy != self.player1 and enemy.health > 0 and enemy.team != self.player1.team:
                            dist = ((enemy.x - mouse_x)**2 + (enemy.y - mouse_y)**2)**0.5
                            if dist < 100 and not enemy.is_trapped:
                                # Trap the enemy!
                                enemy.is_trapped = True
                                enemy.trap_timer = ROLES["Trapper"]["trap_duration"]
                                enemy.cage_x = enemy.x
                                enemy.cage_y = enemy.y
                                self.player1.trap_cooldown_timer = ROLES["Trapper"]["trap_cooldown"]
                                print(f"🪤 Trapped {enemy.username} for 7 seconds!")
                                break
                
    def handle_shop_input(self, event):
        if event.type == pygame.KEYDOWN:
            # Calculate number of items based on current tab
            if self.shop_tab == 0:  # Weapons
                num_items = len(WEAPONS) + len(UPGRADES)
            elif self.shop_tab == 1:  # Vehicles
                num_items = len(VEHICLES)
            elif self.shop_tab == 2:  # Powers
                num_items = len(POWERS)
            else:  # Cosmetics
                num_items = len(COSMETICS)
            
            if event.key == pygame.K_LEFT:
                # Switch to previous tab
                self.shop_tab = (self.shop_tab - 1) % 4
                self.shop_selection = 0
                self.shop_scroll_offset = 0
            elif event.key == pygame.K_RIGHT:
                # Switch to next tab
                self.shop_tab = (self.shop_tab + 1) % 4
                self.shop_selection = 0
                self.shop_scroll_offset = 0
            elif event.key == pygame.K_UP:
                self.shop_selection = (self.shop_selection - 1) % num_items
            elif event.key == pygame.K_DOWN:
                self.shop_selection = (self.shop_selection + 1) % num_items
            elif event.key == pygame.K_b:
                # Buy item
                self.purchase_item()
            elif event.key == pygame.K_e:
                # Equip weapon/vehicle
                self.equip_item()
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU
                
    def handle_win_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.save_progress()  # Save when returning to menu
                self.reset_battle()
                self.state = GameState.MENU
                
    def handle_lose_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.save_progress()  # Save when returning to menu
                self.reset_battle()
                self.state = GameState.MENU
    
    def handle_color_select_input(self, event):
        """Handle color selection input for CPU mode"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU
            elif event.key == pygame.K_LEFT:
                self.selected_color_index = (self.selected_color_index - 1) % len(self.available_colors)
            elif event.key == pygame.K_RIGHT:
                self.selected_color_index = (self.selected_color_index + 1) % len(self.available_colors)
            elif event.key == pygame.K_t:
                # Toggle team mode
                self.team_mode_enabled = not self.team_mode_enabled
                print(f"Team Mode: {'ENABLED' if self.team_mode_enabled else 'DISABLED'}")
            elif event.key == pygame.K_RETURN:
                # Apply selected color
                selected_color_name, selected_color = self.available_colors[self.selected_color_index]
                
                if selected_color not in self.taken_colors:
                    self.my_color = selected_color
                    self.player1.color = selected_color
                    print(f"Selected color: {selected_color_name}")
                    
                    # Assign random roles before battle
                    self.assign_random_roles()
                    
                    # Show role reveal screen
                    self.state = GameState.ROLE_SELECT
                    
                    # Prepare battle (but don't start yet)
                    self.reset_battle()
                
    def purchase_item(self):
        player = self.player1
        
        # Build items list based on current tab
        if self.shop_tab == 0:  # Weapons
            items = list(WEAPONS.items()) + list(UPGRADES.items())
        elif self.shop_tab == 1:  # Vehicles
            items = list(VEHICLES.items())
        elif self.shop_tab == 2:  # Powers
            items = list(POWERS.items())
        else:  # Cosmetics
            items = list(COSMETICS.items())
        
        if self.shop_selection < len(items):
            item_name, item_data = items[self.shop_selection]
            cost = item_data["cost"]
            
            print(f"Attempting to buy: {item_name} for {cost} coins. You have: {player.coins}")
            
            if player.coins >= cost:
                if self.shop_tab == 0:  # Weapons tab
                    if self.shop_selection < len(WEAPONS):
                        # It's a weapon - add to owned weapons
                        if not hasattr(player, 'owned_weapons'):
                            player.owned_weapons = [player.weapon]
                        
                        if item_name not in player.owned_weapons:
                            player.coins -= cost
                            player.owned_weapons.append(item_name)
                            print(f"Purchased {item_name}! Coins remaining: {player.coins}")
                            print(f"Owned weapons: {player.owned_weapons}")
                            self.save_progress()
                        else:
                            print(f"Already own {item_name}")
                    else:
                        # It's an upgrade - apply immediately
                        player.coins -= cost
                        if item_data["effect"] == "speed":
                            player.speed += item_data["value"]
                        elif item_data["effect"] == "health":
                            player.max_health += item_data["value"]
                            player.health += item_data["value"]
                        elif item_data["effect"] == "defense":
                            player.defense += item_data["value"]
                        
                        print(f"Purchased upgrade {item_name}! Coins remaining: {player.coins}")
                        self.save_progress()
                elif self.shop_tab == 1:  # Vehicles tab
                    # It's a vehicle - add to owned vehicles
                    if not hasattr(player, 'owned_vehicles'):
                        player.owned_vehicles = ["None"]
                    
                    if item_name not in player.owned_vehicles:
                        player.coins -= cost
                        player.owned_vehicles.append(item_name)
                        print(f"Purchased {item_name}! Coins remaining: {player.coins}")
                        print(f"Owned vehicles: {player.owned_vehicles}")
                        self.save_progress()
                    else:
                        print(f"Already own {item_name}")
                elif self.shop_tab == 2:  # Powers tab
                    print("Powers are not yet implemented!")
                elif self.shop_tab == 3:  # Cosmetics tab
                    # It's a cosmetic - add to owned cosmetics
                    if item_name not in player.owned_cosmetics:
                        player.coins -= cost
                        player.owned_cosmetics.append(item_name)
                        print(f"Purchased {item_name}! Coins remaining: {player.coins}")
                        print(f"Owned cosmetics: {player.owned_cosmetics}")
                        self.save_progress()
                    else:
                        print(f"Already own {item_name}")
            else:
                print(f"Not enough coins! Need {cost}, have {player.coins}")
    
    def equip_item(self):
        """Equip a weapon or vehicle that has been purchased"""
        player = self.player1
        
        # Build items list based on current tab
        if self.shop_tab == 0:  # Weapons
            items = list(WEAPONS.items()) + list(UPGRADES.items())
        elif self.shop_tab == 1:  # Vehicles
            items = list(VEHICLES.items())
        elif self.shop_tab == 2:  # Powers
            items = list(POWERS.items())
        else:  # Cosmetics
            items = list(COSMETICS.items())
        
        if self.shop_tab == 0:  # Weapons tab
            if self.shop_selection < len(WEAPONS):
                item_name, item_data = items[self.shop_selection]
                
                print(f"Attempting to equip: {item_name}")
                
                # Initialize owned_weapons if it doesn't exist
                if not hasattr(player, 'owned_weapons'):
                    player.owned_weapons = [player.weapon]
                
                # Check if weapon is owned
                if item_name in player.owned_weapons:
                    player.weapon = item_name
                    print(f"Equipped {item_name}!")
                    
                    # CPU always uses same weapon as player
                    if not self.is_network_game and self.is_cpu_mode:
                        self.player2.weapon = item_name
                        print(f"🤖 CPU weapon set to: {item_name}")
                    
                    self.save_progress()
                else:
                    print(f"Don't own {item_name} yet - buy it first!")
            else:
                print("Can't equip upgrades - they apply automatically when purchased")
        elif self.shop_tab == 1:  # Vehicles tab
            item_name, item_data = items[self.shop_selection]
            
            print(f"Attempting to activate vehicle: {item_name}")
            
            # Initialize owned_vehicles if it doesn't exist
            if not hasattr(player, 'owned_vehicles'):
                player.owned_vehicles = ["None"]
            
            # Check if vehicle is owned
            if item_name in player.owned_vehicles:
                old_vehicle = player.vehicle
                player.vehicle = item_name
                
                # Apply vehicle stats
                self.apply_vehicle_stats(player)
                
                print(f"Activated {item_name}!")
                
                # CPU uses None vehicle always (for balance)
                if not self.is_network_game and self.is_cpu_mode:
                    self.player2.vehicle = "None"
                    self.apply_vehicle_stats(self.player2)
                
                self.save_progress()
            else:
                print(f"Don't own {item_name} yet - buy it first!")
        elif self.shop_tab == 2:  # Powers tab
            print("Powers are not yet implemented!")
        elif self.shop_tab == 3:  # Cosmetics tab
            item_name, item_data = items[self.shop_selection]
            
            print(f"Attempting to equip: {item_name}")
            
            # Check if cosmetic is owned
            if item_name in player.owned_cosmetics:
                cosmetic_type = item_data["type"]
                if cosmetic_type == "hat":
                    player.hat = item_name
                    print(f"Equipped hat: {item_name}!")
                elif cosmetic_type == "skin":
                    player.skin = item_name
                    print(f"Equipped skin: {item_name}!")
                elif cosmetic_type == "visor":
                    player.visor = item_name
                    print(f"Equipped visor: {item_name}!")
                
                self.save_progress()
            else:
                print(f"Don't own {item_name} yet - buy it first!")
    
    def give_cpu_random_upgrade(self, prefer_weapon=False):
        """Give CPU a small random balanced upgrade"""
        cpu = self.player2
        
        # If prefer_weapon is True, 85% chance weapon upgrade, otherwise 50%
        weapon_chance = 0.85 if prefer_weapon else 0.5
        
        if random.random() < weapon_chance:
            # Weapon upgrade - give CPU a weapon that's similar to player's level
            player_weapon_cost = WEAPONS.get(self.player1.weapon, {"cost": 0})["cost"]
            cpu_weapon_cost = WEAPONS.get(cpu.weapon, {"cost": 0})["cost"]
            
            # Find weapons that are better than CPU's current but not better than player's
            affordable_weapons = []
            for weapon_name, weapon_data in WEAPONS.items():
                weapon_cost = weapon_data["cost"]
                # CPU can get weapons between their current weapon and player's weapon cost
                # Or at least any weapon up to player's cost
                if weapon_cost <= player_weapon_cost and weapon_cost > 0:
                    affordable_weapons.append(weapon_name)
            
            if affordable_weapons:
                # Prefer weapons closer to player's weapon cost (more competitive)
                # Sort by cost descending and pick from top 3
                affordable_weapons.sort(key=lambda w: WEAPONS[w]["cost"], reverse=True)
                top_weapons = affordable_weapons[:min(3, len(affordable_weapons))]
                new_weapon = random.choice(top_weapons)
                
                # Only upgrade if it's better than current weapon
                if WEAPONS[new_weapon]["cost"] >= cpu_weapon_cost:
                    cpu.weapon = new_weapon
                    print(f"🤖 CPU upgraded to {new_weapon}!")
                else:
                    # If no better weapon available, give stat upgrade instead
                    self._give_cpu_stat_upgrade(cpu)
            else:
                self._give_cpu_stat_upgrade(cpu)
        else:
            self._give_cpu_stat_upgrade(cpu)
    
    def _give_cpu_stat_upgrade(self, cpu):
        """Helper function to give CPU a stat upgrade"""
        upgrade_type = random.choice(["speed", "health", "defense"])
        
        if upgrade_type == "speed":
            cpu.speed += 0.5
            print(f"⚡ CPU speed increased!")
        elif upgrade_type == "health":
            cpu.max_health += 10
            cpu.health += 10
            print(f"❤️ CPU health increased!")
        elif upgrade_type == "defense":
            cpu.defense += 2
            print(f"🛡️ CPU defense increased!")
    
    def generate_map_platforms(self):
        """Generate platforms based on current map"""
        self.platforms = []
        
        # Get map-specific color for platforms
        map_data = MAPS[self.current_map]
        ground_color = map_data["ground_color"]
        platform_color = tuple(min(c + 20, 255) for c in ground_color)
        
        if self.current_map == "Street":
            # City Street - Fire escapes and ledges
            self.platforms.append(Platform(150, 350, 120, 15, platform_color))
            self.platforms.append(Platform(400, 280, 150, 15, platform_color))
            self.platforms.append(Platform(700, 350, 120, 15, platform_color))
            self.platforms.append(Platform(250, 450, 100, 15, platform_color))
            self.platforms.append(Platform(600, 200, 130, 15, platform_color))
            
        elif self.current_map == "Desert":
            # Sandy Desert - Rock formations
            self.platforms.append(Platform(200, 380, 140, 18, (160, 120, 80)))
            self.platforms.append(Platform(450, 300, 120, 18, (160, 120, 80)))
            self.platforms.append(Platform(700, 380, 140, 18, (160, 120, 80)))
            self.platforms.append(Platform(100, 450, 100, 18, (160, 120, 80)))
            self.platforms.append(Platform(800, 250, 110, 18, (160, 120, 80)))
            
        elif self.current_map == "Fields":
            # Green Fields - Tree platforms and hills
            self.platforms.append(Platform(180, 370, 130, 15, (100, 160, 80)))
            self.platforms.append(Platform(420, 290, 140, 15, (100, 160, 80)))
            self.platforms.append(Platform(680, 370, 130, 15, (100, 160, 80)))
            self.platforms.append(Platform(300, 470, 110, 15, (100, 160, 80)))
            self.platforms.append(Platform(550, 220, 120, 15, (100, 160, 80)))
            
        elif self.current_map == "Arena":
            # Battle Arena - Stone pillars and ledges
            self.platforms.append(Platform(170, 360, 130, 20, (110, 80, 80)))
            self.platforms.append(Platform(410, 270, 160, 20, (110, 80, 80)))
            self.platforms.append(Platform(710, 360, 130, 20, (110, 80, 80)))
            self.platforms.append(Platform(50, 440, 120, 20, (110, 80, 80)))
            self.platforms.append(Platform(820, 440, 120, 20, (110, 80, 80)))
            self.platforms.append(Platform(300, 190, 140, 20, (110, 80, 80)))
            self.platforms.append(Platform(550, 190, 140, 20, (110, 80, 80)))
    
    def apply_vehicle_stats(self, player):
        """Apply vehicle stats to a player (health, size, etc.)"""
        vehicle_data = VEHICLES[player.vehicle]
        
        # Update size based on vehicle
        player.width, player.height = vehicle_data["size"]
        
        # Apply health multiplier to max_health
        base_max_health = 100  # Base health
        player.max_health = int(base_max_health * vehicle_data["health_multiplier"])
        
        # Clamp current health to new max
        if player.health > player.max_health:
            player.health = player.max_health
    
    # ===== SAVE/LOAD SYSTEM =====
    
    def save_progress(self):
        """Save player progress to file"""
        try:
            save_data = {
                'username': self.player1.username,
                'coins': self.player1.coins,
                'owned_weapons': getattr(self.player1, 'owned_weapons', ["Fist"]),
                'current_weapon': self.player1.weapon,
                'owned_vehicles': getattr(self.player1, 'owned_vehicles', ["None"]),
                'current_vehicle': self.player1.vehicle,
                'owned_cosmetics': getattr(self.player1, 'owned_cosmetics', []),
                'hat': self.player1.hat,
                'skin': self.player1.skin,
                'visor': self.player1.visor,
                'speed': self.player1.speed,
                'max_health': self.player1.max_health,
                'defense': self.player1.defense
            }
            
            with open('battle_street_save.dat', 'wb') as f:
                pickle.dump(save_data, f)
            
            print(f"Progress saved! Username: {save_data['username']}, Coins: {save_data['coins']}")
        except Exception as e:
            print(f"Save error: {e}")
    
    def load_progress(self):
        """Load player progress from file"""
        try:
            with open('battle_street_save.dat', 'rb') as f:
                save_data = pickle.load(f)
            
            # Load username if it exists
            saved_username = save_data.get('username', '')
            if saved_username:
                self.player_username = saved_username
                self.player1.username = saved_username
                # Skip username input if we have a saved username
                self.has_saved_username = True
                print(f"✨ Welcome back, {saved_username}!")
            else:
                self.has_saved_username = False
            
            self.player1.coins = save_data.get('coins', 0)
            self.player1.owned_weapons = save_data.get('owned_weapons', ["Fist"])
            self.player1.weapon = save_data.get('current_weapon', "Fist")
            self.player1.owned_vehicles = save_data.get('owned_vehicles', ["None"])
            self.player1.vehicle = save_data.get('current_vehicle', "None")
            self.player1.owned_cosmetics = save_data.get('owned_cosmetics', [])
            self.player1.hat = save_data.get('hat', None)
            self.player1.skin = save_data.get('skin', None)
            self.player1.visor = save_data.get('visor', None)
            self.player1.speed = save_data.get('speed', 5)
            self.player1.max_health = save_data.get('max_health', 100)
            self.player1.defense = save_data.get('defense', 0)
            self.player1.health = self.player1.max_health
            
            # Apply vehicle stats
            self.apply_vehicle_stats(self.player1)
            
            # CPU always uses same weapon as player, no vehicle
            self.player2.weapon = self.player1.weapon
            self.player2.vehicle = "None"
            self.apply_vehicle_stats(self.player2)
            
            print(f"Progress loaded! Coins: {self.player1.coins}, Weapons: {self.player1.owned_weapons}, Vehicles: {self.player1.owned_vehicles}")
            print(f"CPU weapon set to: {self.player2.weapon}")
        except FileNotFoundError:
            self.has_saved_username = False
            print("No save file found - starting fresh")
        except Exception as e:
            self.has_saved_username = False
            print(f"Load error: {e}")
    
    # ===== NETWORKING METHODS =====
    
    def generate_lobby_code(self):
        """Generate a unique 6-character lobby code"""
        import string
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(6))
    
    def start_host(self):
        """Start hosting a LAN game with lobby"""
        try:
            self.is_host = True
            self.is_network_game = True
            self.is_cpu_mode = False
            
            # Generate unique lobby code
            self.lobby_code = self.generate_lobby_code()
            
            # Create server socket
            self.network_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.network_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Get local IP
            hostname = socket.gethostname()
            self.server_ip = socket.gethostbyname(hostname)
            
            # Bind to all interfaces to accept connections from anywhere
            self.network_socket.bind(('0.0.0.0', GAME_PORT))
            self.network_socket.listen(10)  # Allow up to 10 connections
            
            print(f"Server listening on port {GAME_PORT}")
            
            # Initialize lobby
            self.lobby_players = [self.player_name + " (Host)"]
            self.can_start = False
            
            # Initialize color selections
            self.player_colors_taken = {0: self.selected_color_index}  # Host gets their selected color
            
            # Start UDP broadcast
            self.start_broadcast()
            
            self.connection_status = f"Lobby created | Code: {self.lobby_code}"
            self.state = GameState.HOST_WAIT
            print(f"Lobby code: {self.lobby_code} | Listening on port {GAME_PORT}")
            
            # Start listening thread for new connections
            self.network_thread = threading.Thread(target=self.accept_connections, daemon=True)
            self.network_thread.start()
            
        except Exception as e:
            self.connection_status = f"Error: {str(e)}"
            print(f"Host error: {e}")
    
    def start_broadcast(self):
        """Start broadcasting server availability"""
        try:
            self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # For macOS
            try:
                self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            except AttributeError:
                pass
            print(f"Starting broadcast on {self.server_ip}...")
            broadcast_thread = threading.Thread(target=self.broadcast_server, daemon=True)
            broadcast_thread.start()
        except Exception as e:
            print(f"Broadcast setup error: {e}")
    
    def broadcast_server(self):
        """Continuously broadcast server info"""
        print(f"Broadcasting on port {BROADCAST_PORT} with code {self.lobby_code}...")
        broadcast_count = 0
        
        while self.is_host and self.state == GameState.HOST_WAIT:
            try:
                message = f"BATTLE_STREET_SERVER:{self.server_ip}:{len(self.lobby_players)}:{self.lobby_code}"
                
                # Send to multiple addresses to ensure delivery
                addresses = [
                    ('255.255.255.255', BROADCAST_PORT),  # Broadcast
                    ('127.0.0.1', BROADCAST_PORT),  # Localhost
                ]
                
                # Try to get local subnet broadcast too
                try:
                    ip_parts = self.server_ip.split('.')
                    if len(ip_parts) == 4:
                        subnet_broadcast = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.255"
                        addresses.append((subnet_broadcast, BROADCAST_PORT))
                except:
                    pass
                
                for addr in addresses:
                    try:
                        bytes_sent = self.broadcast_socket.sendto(message.encode(), addr)
                        if broadcast_count % 4 == 0:  # Print every 2 seconds
                            print(f"Broadcast sent to {addr}: {message} ({bytes_sent} bytes)")
                    except Exception as e:
                        if broadcast_count % 4 == 0:
                            print(f"Failed to send to {addr}: {e}")
                
                broadcast_count += 1
                time.sleep(0.5)
            except Exception as e:
                print(f"Broadcast error: {e}")
                break
        
        print("Stopped broadcasting")
    
    def accept_connections(self):
        """Accept multiple incoming connections"""
        self.network_socket.settimeout(1.0)
        print("Waiting for connections...")
        
        while self.is_host and len(self.lobby_players) < self.max_players and self.state == GameState.HOST_WAIT:
            try:
                client_socket, addr = self.network_socket.accept()
                print(f"Connection from {addr}")
                
                # Receive player name
                client_socket.settimeout(5.0)
                player_name = client_socket.recv(1024).decode()
                
                # Send player index to client
                player_index = len(self.client_connections) + 1  # Host is 0, clients are 1, 2, 3...
                try:
                    client_socket.send(str(player_index).encode())
                    print(f"Sent player index {player_index} to {player_name}")
                except:
                    pass
                
                self.client_connections.append(client_socket)
                self.lobby_players.append(player_name)
                
                # Update can_start flag
                self.can_start = len(self.lobby_players) >= 2
                
                print(f"Player {player_name} connected from {addr[0]}. Total players: {len(self.lobby_players)}")
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Connection accept error: {e}")
                continue
    
    def start_server_browser(self):
        """Start scanning for servers"""
        self.discovered_servers = []
        self.server_selection = 0
        self.connection_status = "Waiting..."
        self.last_broadcast_time = 0
        self.state = GameState.JOIN_GAME
        
        print("\n=== Starting Server Browser ===")
        
        # Start UDP listener for broadcasts
        scan_thread = threading.Thread(target=self.scan_for_servers, daemon=True)
        scan_thread.start()
    
    def scan_for_servers(self):
        """Scan for available servers"""
        try:
            scan_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            scan_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # For macOS, also set SO_REUSEPORT
            try:
                scan_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            except AttributeError:
                pass
            
            # Bind to all interfaces
            scan_socket.bind(('', BROADCAST_PORT))
            scan_socket.settimeout(0.5)
            
            print(f"Started scanning for servers on port {BROADCAST_PORT}...")
            print(f"Listening on all interfaces for UDP broadcasts...")
            
            receive_count = 0
            
            while self.state == GameState.JOIN_GAME:
                try:
                    data, addr = scan_socket.recvfrom(1024)
                    message = data.decode()
                    receive_count += 1
                    
                    print(f"[{receive_count}] Received: '{message}' from {addr}")
                    
                    if message.startswith("BATTLE_STREET_SERVER:"):
                        parts = message.split(':')
                        if len(parts) >= 4:
                            server_ip = parts[1]
                            player_count = parts[2]
                            lobby_code = parts[3]
                            
                            # Update last broadcast time
                            self.last_broadcast_time = time.time()
                            
                            print(f"  -> Parsed: IP={server_ip}, Players={player_count}, Code={lobby_code}")
                            
                            # Update or add server
                            server_info = {"ip": server_ip, "players": player_count, "code": lobby_code}
                            
                            # Check if server already in list
                            found = False
                            for i, server in enumerate(self.discovered_servers):
                                if server["ip"] == server_ip or server.get("code") == lobby_code:
                                    self.discovered_servers[i] = server_info
                                    found = True
                                    print(f"  -> Updated existing server")
                                    break
                            
                            if not found and len(self.discovered_servers) < 20:
                                self.discovered_servers.append(server_info)
                                print(f"  -> Added new server! Total servers: {len(self.discovered_servers)}")
                        else:
                            print(f"  -> Invalid message format (expected 4 parts, got {len(parts)})")
                    else:
                        print(f"  -> Not a Battle Street server message")
                            
                except socket.timeout:
                    # This is normal - just means no data received in 0.5 seconds
                    continue
                except Exception as e:
                    print(f"Receive error: {e}")
                    continue
                    
            scan_socket.close()
            print(f"Stopped scanning. Found {len(self.discovered_servers)} servers total.")
        except Exception as e:
            print(f"Scan setup error: {e}")
    
    def join_by_code(self, code):
        """Join a game by lobby code"""
        print(f"Searching for lobby code: {code}")
        print(f"Current discovered servers: {self.discovered_servers}")
        
        # Find server with matching code
        for server in self.discovered_servers:
            if server.get("code") == code:
                print(f"Found server with code {code} at IP {server['ip']}")
                threading.Thread(target=self.start_client, args=(server["ip"],), daemon=True).start()
                return
        
        # Code not found in discovered servers
        # Try localhost as fallback (for testing on same computer)
        print(f"Code {code} not in discovered servers, trying localhost...")
        self.connection_status = f"Trying to connect to code '{code}'..."
        
        # Try localhost first (for same-computer testing)
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(1.0)
            test_socket.connect(('127.0.0.1', GAME_PORT))
            test_socket.close()
            # If connection succeeded, try to join
            print(f"Found server on localhost, connecting...")
            threading.Thread(target=self.start_client, args=('127.0.0.1',), daemon=True).start()
            return
        except:
            print("No server on localhost")
        
        # Code not found anywhere
        self.connection_status = f"Lobby code '{code}' not found. Make sure host is in lobby."
        print(f"No server found with code {code}. Discovered servers: {len(self.discovered_servers)}")
    
    def start_client(self, ip_address):
        """Connect to host"""
        try:
            print(f"Attempting to connect to {ip_address}:{GAME_PORT}...")
            self.is_host = False
            self.is_network_game = True
            self.is_cpu_mode = False
            
            self.network_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.network_socket.settimeout(10.0)
            self.network_socket.connect((ip_address, GAME_PORT))
            
            # Send player name
            self.network_socket.send(self.player_name.encode())
            print(f"Connected as {self.player_name}")
            
            # Receive player index from host
            self.network_socket.settimeout(5.0)
            player_index_str = self.network_socket.recv(1024).decode()
            self.my_player_index = int(player_index_str)
            print(f"Assigned player index: {self.my_player_index}")
            
            self.connection_status = "Connected! Waiting for host to start..."
            self.input_code = ""  # Clear the input code
            self.state = GameState.HOST_WAIT  # Reuse host wait screen
            
            # Start listening for START signal from host
            listen_thread = threading.Thread(target=self.listen_for_start, daemon=True)
            listen_thread.start()
            
        except Exception as e:
            self.connection_status = f"Connection failed: {str(e)}"
            print(f"Client connection error: {e}")
            self.state = GameState.JOIN_GAME  # Return to server browser
    
    def listen_for_start(self):
        """Client listens for START signal from host"""
        try:
            self.network_socket.settimeout(None)  # Block until data received
            print("Listening for START signal from host...")
            
            while self.state == GameState.HOST_WAIT and not self.is_host:
                try:
                    data = self.network_socket.recv(1024)
                    if not data:
                        print("Connection closed by host")
                        break
                    
                    message = data.decode()
                    print(f"Received from host: {message}")
                    
                    if message == "START_GAME":
                        print("Received START_GAME signal! Entering battle...")
                        self.reset_battle()
                        self.state = GameState.BATTLE
                        self.network_running = True
                        
                        # Start network sync for client
                        sync_thread = threading.Thread(target=self.network_sync_loop, daemon=True)
                        sync_thread.start()
                        
                        break
                        
                except Exception as e:
                    print(f"Error receiving start signal: {e}")
                    break
                    
        except Exception as e:
            print(f"Listen for start error: {e}")
    
    def draw_host_wait(self):
        """Draw lobby screen with color selection"""
        screen.fill(DARK_BLUE)
        
        if self.is_host:
            title = title_font.render("LOBBY", True, YELLOW)
        else:
            title = title_font.render("WAITING FOR HOST", True, YELLOW)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 50)))
        
        if self.is_host:
            # Show lobby code prominently
            code_box = pygame.Rect(SCREEN_WIDTH // 2 - 200, 90, 400, 60)
            pygame.draw.rect(screen, GREEN, code_box)
            pygame.draw.rect(screen, YELLOW, code_box, 4)
            
            code_label = tiny_font.render("LOBBY CODE:", True, BLACK)
            screen.blit(code_label, code_label.get_rect(center=(SCREEN_WIDTH // 2, 105)))
            
            code_text = menu_font.render(self.lobby_code, True, BLACK)
            screen.blit(code_text, code_text.get_rect(center=(SCREEN_WIDTH // 2, 130)))
            
            # Show lobby info
            status = text_font.render(f"Players: {len(self.lobby_players)}/{self.max_players}", True, WHITE)
            screen.blit(status, status.get_rect(center=(SCREEN_WIDTH // 2, 180)))
            
            # Color selection for host
            color_label = small_font.render("Your Color:", True, WHITE)
            screen.blit(color_label, (100, 220))
            
            # Color palette
            color_y = 260
            for i, (color_name, color_rgb) in enumerate(self.available_colors[:5]):
                color_x = 100 + i * 80
                color_box = pygame.Rect(color_x, color_y, 60, 60)
                
                # Check if color is taken by another player
                is_taken = i in [v for k, v in self.player_colors_taken.items() if k != 0]
                is_selected = i == self.selected_color_index
                
                if is_taken:
                    # Grayed out with X
                    pygame.draw.rect(screen, DARK_GRAY, color_box)
                    pygame.draw.line(screen, RED, (color_x, color_y), (color_x + 60, color_y + 60), 4)
                    pygame.draw.line(screen, RED, (color_x + 60, color_y), (color_x, color_y + 60), 4)
                else:
                    pygame.draw.rect(screen, color_rgb, color_box)
                
                if is_selected and not is_taken:
                    pygame.draw.rect(screen, WHITE, color_box, 4)
                else:
                    pygame.draw.rect(screen, BLACK, color_box, 2)
                
                name_text = tiny_font.render(color_name, True, WHITE)
                screen.blit(name_text, (color_x, color_y + 65))
            
            # Second row of colors
            color_y2 = 360
            for i, (color_name, color_rgb) in enumerate(self.available_colors[5:10]):
                color_x = 100 + i * 80
                actual_index = i + 5
                color_box = pygame.Rect(color_x, color_y2, 60, 60)
                
                is_taken = actual_index in [v for k, v in self.player_colors_taken.items() if k != 0]
                is_selected = actual_index == self.selected_color_index
                
                if is_taken:
                    pygame.draw.rect(screen, DARK_GRAY, color_box)
                    pygame.draw.line(screen, RED, (color_x, color_y2), (color_x + 60, color_y2 + 60), 4)
                    pygame.draw.line(screen, RED, (color_x + 60, color_y2), (color_x, color_y2 + 60), 4)
                else:
                    pygame.draw.rect(screen, color_rgb, color_box)
                
                if is_selected and not is_taken:
                    pygame.draw.rect(screen, WHITE, color_box, 4)
                else:
                    pygame.draw.rect(screen, BLACK, color_box, 2)
                
                name_text = tiny_font.render(color_name, True, WHITE)
                screen.blit(name_text, (color_x, color_y2 + 65))
            
            inst_colors = tiny_font.render("←→: Choose Color", True, LIGHT_GRAY)
            screen.blit(inst_colors, (100, 450))
            
            # Player list
            list_y = 490
            players_label = small_font.render("Connected Players:", True, WHITE)
            screen.blit(players_label, (SCREEN_WIDTH // 2 + 100, list_y))
            for i, player in enumerate(self.lobby_players):
                player_text = tiny_font.render(f"{i+1}. {player}", True, GREEN)
                screen.blit(player_text, (SCREEN_WIDTH // 2 + 100, list_y + 30 + i * 25))
            
            # Start button or waiting message
            if self.can_start:
                start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 550, 200, 60)
                pygame.draw.rect(screen, GREEN, start_rect)
                pygame.draw.rect(screen, WHITE, start_rect, 3)
                start_text = menu_font.render("START", True, BLACK)
                screen.blit(start_text, start_text.get_rect(center=start_rect.center))
                
                inst = small_font.render("Press ENTER to start | ESC to cancel", True, LIGHT_GRAY)
            else:
                wait_text = text_font.render("Waiting for players...", True, ORANGE)
                screen.blit(wait_text, wait_text.get_rect(center=(SCREEN_WIDTH // 2, 570)))
                
                inst = small_font.render("Need at least 2 players | ESC to cancel", True, LIGHT_GRAY)
        else:
            # Client waiting
            wait_text = text_font.render(self.connection_status, True, WHITE)
            screen.blit(wait_text, wait_text.get_rect(center=(SCREEN_WIDTH // 2, 300)))
            
            inst = small_font.render("ESC to cancel", True, LIGHT_GRAY)
        
        screen.blit(inst, inst.get_rect(center=(SCREEN_WIDTH // 2, 640)))
    
    def draw_color_select(self):
        """Draw character color selection screen"""
        screen.fill(DARK_BLUE)
        
        title = title_font.render("Choose Your Color", True, YELLOW)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 80)))
        
        # Color palette - first row
        color_y = 200
        for i, (color_name, color_rgb) in enumerate(self.available_colors[:5]):
            color_x = 150 + i * 140
            color_box = pygame.Rect(color_x, color_y, 100, 100)
            
            # Check if color is taken
            is_taken = color_rgb in self.taken_colors
            is_selected = i == self.selected_color_index
            
            if is_taken:
                # Grayed out with X
                pygame.draw.rect(screen, DARK_GRAY, color_box)
                pygame.draw.line(screen, RED, (color_x + 10, color_y + 10), (color_x + 90, color_y + 90), 6)
                pygame.draw.line(screen, RED, (color_x + 90, color_y + 10), (color_x + 10, color_y + 90), 6)
            else:
                pygame.draw.rect(screen, color_rgb, color_box)
            
            if is_selected and not is_taken:
                pygame.draw.rect(screen, WHITE, color_box, 5)
            else:
                pygame.draw.rect(screen, BLACK, color_box, 3)
            
            name_text = small_font.render(color_name, True, WHITE)
            screen.blit(name_text, name_text.get_rect(center=(color_x + 50, color_y + 120)))
        
        # Second row of colors
        color_y2 = 380
        for i, (color_name, color_rgb) in enumerate(self.available_colors[5:10]):
            color_x = 150 + i * 140
            actual_index = i + 5
            color_box = pygame.Rect(color_x, color_y2, 100, 100)
            
            is_taken = color_rgb in self.taken_colors
            is_selected = actual_index == self.selected_color_index
            
            if is_taken:
                pygame.draw.rect(screen, DARK_GRAY, color_box)
                pygame.draw.line(screen, RED, (color_x + 10, color_y2 + 10), (color_x + 90, color_y2 + 90), 6)
                pygame.draw.line(screen, RED, (color_x + 90, color_y2 + 10), (color_x + 10, color_y2 + 90), 6)
            else:
                pygame.draw.rect(screen, color_rgb, color_box)
            
            if is_selected and not is_taken:
                pygame.draw.rect(screen, WHITE, color_box, 5)
            else:
                pygame.draw.rect(screen, BLACK, color_box, 3)
            
            name_text = small_font.render(color_name, True, WHITE)
            screen.blit(name_text, name_text.get_rect(center=(color_x + 50, color_y2 + 120)))
        
        # Team Mode Checkbox
        checkbox_y = 540
        checkbox_size = 30
        checkbox_x = SCREEN_WIDTH // 2 - 150
        checkbox_rect = pygame.Rect(checkbox_x, checkbox_y, checkbox_size, checkbox_size)
        
        # Draw checkbox
        pygame.draw.rect(screen, WHITE, checkbox_rect, 3)
        if self.team_mode_enabled:
            # Draw checkmark
            pygame.draw.line(screen, GREEN, (checkbox_x + 5, checkbox_y + 15), (checkbox_x + 12, checkbox_y + 22), 4)
            pygame.draw.line(screen, GREEN, (checkbox_x + 12, checkbox_y + 22), (checkbox_x + 25, checkbox_y + 8), 4)
        
        # Label
        team_label = menu_font.render("Team Mode (Get CPU Teammates)", True, WHITE)
        screen.blit(team_label, (checkbox_x + 40, checkbox_y))
        
        # Instructions
        inst = small_font.render("←→: Choose Color | T: Toggle Team Mode | ENTER: Confirm | ESC: Back", True, LIGHT_GRAY)
        screen.blit(inst, inst.get_rect(center=(SCREEN_WIDTH // 2, 600)))
    
    def draw_join_game(self):
        """Draw server browser with code input"""
        screen.fill(DARK_BLUE)
        
        title = title_font.render("Join Game", True, YELLOW)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 50)))
        
        # Code input section
        code_label = text_font.render("Enter Lobby Code:", True, WHITE)
        screen.blit(code_label, (SCREEN_WIDTH // 2 - 140, 100))
        
        code_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, 140, 300, 50)
        pygame.draw.rect(screen, WHITE, code_box, 3)
        pygame.draw.rect(screen, (30, 30, 50), code_box)
        
        code_display = menu_font.render(self.input_code, True, YELLOW)
        screen.blit(code_display, (code_box.x + 10, code_box.y + 8))
        
        code_inst = tiny_font.render("Type code and press ENTER to join", True, LIGHT_GRAY)
        screen.blit(code_inst, (SCREEN_WIDTH // 2 - 130, 195))
        
        # Divider
        pygame.draw.line(screen, GRAY, (100, 230), (SCREEN_WIDTH - 100, 230), 2)
        or_text = small_font.render("OR", True, GRAY)
        screen.blit(or_text, (SCREEN_WIDTH // 2 - 15, 220))
        
        # Available games section
        available_label = text_font.render("Available Games:", True, WHITE)
        screen.blit(available_label, (100, 260))
        
        # Show scanning status with activity indicator
        current_time = time.time()
        if self.last_broadcast_time > 0 and (current_time - self.last_broadcast_time) < 2:
            scan_status = "✓ Receiving broadcasts"
            scan_color = GREEN
        else:
            scan_status = "Scanning..."
            scan_color = LIGHT_GRAY
        
        scan_text = tiny_font.render(f"{scan_status} | Found: {len(self.discovered_servers)}", True, scan_color)
        screen.blit(scan_text, (SCREEN_WIDTH - 300, 265))
        
        # Connection status message if any
        if self.connection_status and self.connection_status != "Waiting...":
            status_msg = small_font.render(self.connection_status, True, ORANGE)
            screen.blit(status_msg, status_msg.get_rect(center=(SCREEN_WIDTH // 2, 600)))
        
        # Server list
        if not self.discovered_servers:
            no_servers = small_font.render("No games found yet...", True, GRAY)
            screen.blit(no_servers, no_servers.get_rect(center=(SCREEN_WIDTH // 2, 380)))
            
            # Testing help
            test_hint = tiny_font.render("Testing on same computer? Make sure host is in lobby screen!", True, DARK_GRAY)
            screen.blit(test_hint, test_hint.get_rect(center=(SCREEN_WIDTH // 2, 410)))
        else:
            list_y = 300
            for i, server in enumerate(self.discovered_servers[:5]):  # Show max 5
                # Server box
                server_rect = pygame.Rect(100, list_y + i * 65, SCREEN_WIDTH - 200, 55)
                
                if i == self.server_selection:
                    pygame.draw.rect(screen, GREEN, server_rect)
                    pygame.draw.rect(screen, WHITE, server_rect, 3)
                    text_color = BLACK
                else:
                    pygame.draw.rect(screen, DARK_GRAY, server_rect)
                    pygame.draw.rect(screen, LIGHT_GRAY, server_rect, 2)
                    text_color = WHITE
                
                # Server info with code
                code_text = small_font.render(f"Code: {server.get('code', 'N/A')}", True, text_color)
                screen.blit(code_text, (server_rect.x + 20, server_rect.y + 8))
                
                info_text = tiny_font.render(f"IP: {server['ip']} | Players: {server['players']}/{self.max_players}", True, text_color)
                screen.blit(info_text, (server_rect.x + 20, server_rect.y + 32))
        
        # Debug info
        debug_y = 630
        if self.discovered_servers:
            debug_msg = tiny_font.render(f"Servers found: {[s.get('code', 'N/A') for s in self.discovered_servers]}", True, DARK_GRAY)
            screen.blit(debug_msg, (20, debug_y))
        
        # Instructions
        inst = small_font.render("↑↓: Select | ENTER: Join | Type code above | ESC: Cancel", True, LIGHT_GRAY)
        screen.blit(inst, inst.get_rect(center=(SCREEN_WIDTH // 2, 665)))
    
    def handle_join_input(self, event):
        """Handle server browser input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.discovered_servers = []
                self.input_code = ""
                self.state = GameState.MENU
            elif event.key == pygame.K_UP and self.discovered_servers:
                self.server_selection = (self.server_selection - 1) % len(self.discovered_servers)
            elif event.key == pygame.K_DOWN and self.discovered_servers:
                self.server_selection = (self.server_selection + 1) % len(self.discovered_servers)
            elif event.key == pygame.K_RETURN:
                # Try to join by code first, then by selection
                if self.input_code and len(self.input_code) == 6:
                    # Join by code
                    print(f"User pressed ENTER to join with code: {self.input_code}")
                    self.join_by_code(self.input_code)
                elif self.discovered_servers:
                    # Connect to selected server
                    selected_server = self.discovered_servers[self.server_selection]
                    print(f"User selected server: {selected_server}")
                    threading.Thread(target=self.start_client, args=(selected_server["ip"],), daemon=True).start()
                else:
                    print("No code entered and no servers available")
            elif event.key == pygame.K_BACKSPACE:
                self.input_code = self.input_code[:-1]
            elif event.unicode.isalnum() and len(self.input_code) < 6:
                self.input_code += event.unicode.upper()
    
    def handle_host_wait_input(self, event):
        """Handle lobby input"""
        if event.type == pygame.KEYDOWN:
            # Color selection (arrow keys)
            if event.key == pygame.K_LEFT:
                if self.is_host:
                    # Cycle through available colors
                    for _ in range(len(self.available_colors)):
                        self.selected_color_index = (self.selected_color_index - 1) % len(self.available_colors)
                        # Check if this color is not taken
                        if self.selected_color_index not in [v for k, v in self.player_colors_taken.items() if k != 0]:
                            break
                    self.player_colors_taken[0] = self.selected_color_index
                    self.player1.color = self.available_colors[self.selected_color_index][1]
                    print(f"Selected color: {self.available_colors[self.selected_color_index][0]}")
            elif event.key == pygame.K_RIGHT:
                if self.is_host:
                    # Cycle through available colors
                    for _ in range(len(self.available_colors)):
                        self.selected_color_index = (self.selected_color_index + 1) % len(self.available_colors)
                        # Check if this color is not taken
                        if self.selected_color_index not in [v for k, v in self.player_colors_taken.items() if k != 0]:
                            break
                    self.player_colors_taken[0] = self.selected_color_index
                    self.player1.color = self.available_colors[self.selected_color_index][1]
                    print(f"Selected color: {self.available_colors[self.selected_color_index][0]}")
            elif event.key == pygame.K_ESCAPE:
                # Clean up connections
                if self.network_socket:
                    try:
                        self.network_socket.close()
                    except:
                        pass
                if self.broadcast_socket:
                    try:
                        self.broadcast_socket.close()
                    except:
                        pass
                for client in self.client_connections:
                    try:
                        client.close()
                    except:
                        pass
                self.client_connections = []
                self.lobby_players = []
                self.is_host = False
                self.state = GameState.MENU
            elif event.key == pygame.K_LEFT and self.is_host:
                # Cycle through colors
                self.selected_color_index = (self.selected_color_index - 1) % len(self.available_colors)
            elif event.key == pygame.K_RIGHT and self.is_host:
                # Cycle through colors
                self.selected_color_index = (self.selected_color_index + 1) % len(self.available_colors)
            elif event.key == pygame.K_RETURN and self.is_host and self.can_start:
                # Apply selected color
                selected_color_name, selected_color = self.available_colors[self.selected_color_index]
                
                # Check if color is not taken
                if selected_color not in self.taken_colors:
                    self.my_color = selected_color
                    self.player1.color = selected_color
                    self.taken_colors.append(selected_color)
                    print(f"Host selected color: {selected_color_name}")
                
                # Start the game!
                print(f"Host starting game with {len(self.lobby_players)} players")
                
                # Send START signal to all clients
                for client in self.client_connections:
                    try:
                        client.send(b"START_GAME")
                        print(f"Sent START signal to client")
                    except Exception as e:
                        print(f"Failed to send start signal: {e}")
                
                self.reset_battle()
                self.state = GameState.BATTLE
                self.network_running = True
                self.my_player_index = 0  # Host is always player 0
                
                # Start network sync thread for host
                if self.is_network_game:
                    sync_thread = threading.Thread(target=self.network_sync_loop, daemon=True)
                    sync_thread.start()
                
                print(f"Host entered battle state as player index {self.my_player_index}")
    
    def network_sync_loop(self):
        """Continuously sync ALL players' game state - super fast updates"""
        print("Starting network sync loop with 1ms updates...")
        
        while self.network_running and self.state == GameState.BATTLE:
            try:
                # Prepare ALL players data for synchronized screens
                all_players_data = []
                for i, player in enumerate(self.all_players):
                    player_data = {
                        'index': i,
                        'x': player.x,
                        'y': player.y,
                        'health': player.health,
                        'max_health': player.max_health,
                        'weapon': player.weapon,
                        'facing_right': player.facing_right,
                        'color': player.color,
                        'velocity_y': player.velocity_y,
                        'on_ground': player.on_ground,
                        'projectiles': [(p.x, p.y, p.dx, p.dy, p.damage, p.color, p.has_explosion) for p in player.projectiles]
                    }
                    all_players_data.append(player_data)
                
                # Add metadata about who sent this
                sync_data = {
                    'sender_index': self.my_player_index,
                    'all_players': all_players_data,
                    'timestamp': time.time()
                }
                
                data_bytes = pickle.dumps(sync_data)
                
                if self.is_host:
                    # Host broadcasts complete game state to all clients
                    for client in self.client_connections:
                        try:
                            client.sendall(data_bytes)
                        except:
                            pass
                    
                    # Host receives updates from clients
                    for idx, client in enumerate(self.client_connections):
                        try:
                            client.settimeout(0.0001)  # 0.1ms timeout for ultra-fast updates
                            received = client.recv(8192)
                            if received:
                                client_data = pickle.loads(received)
                                self.merge_network_data(client_data)
                        except socket.timeout:
                            pass
                        except:
                            pass
                else:
                    # Client sends their updates to host
                    try:
                        self.network_socket.sendall(data_bytes)
                    except:
                        pass
                    
                    # Client receives complete game state from host
                    try:
                        self.network_socket.settimeout(0.0001)  # 0.1ms timeout
                        received = self.network_socket.recv(8192)
                        if received:
                            host_data = pickle.loads(received)
                            self.sync_all_players(host_data)
                    except socket.timeout:
                        pass
                    except:
                        pass
                
                time.sleep(0.001)  # 1ms sync rate = 1000 updates/second!
                
            except Exception as e:
                print(f"Network sync error: {e}")
                time.sleep(0.01)
        
        print("Network sync loop ended")
    
    def merge_network_data(self, data):
        """Merge received network data into game state (for host)"""
        try:
            sender_idx = data.get('sender_index', -1)
            all_players_data = data.get('all_players', [])
            
            # Update the sender's player data
            if 0 <= sender_idx < len(self.all_players) and sender_idx < len(all_players_data):
                sender_data = all_players_data[sender_idx]
                self.update_single_player(self.all_players[sender_idx], sender_data)
                
        except Exception as e:
            print(f"Merge network data error: {e}")
    
    def sync_all_players(self, data):
        """Sync complete game state (for clients)"""
        try:
            all_players_data = data.get('all_players', [])
            
            # Update ALL players except yourself
            for player_data in all_players_data:
                player_idx = player_data.get('index', -1)
                
                if 0 <= player_idx < len(self.all_players):
                    # Don't overwrite your own player data (you control it locally)
                    if player_idx != self.my_player_index:
                        self.update_single_player(self.all_players[player_idx], player_data)
                        
        except Exception as e:
            print(f"Sync all players error: {e}")
    
    def update_single_player(self, player, data):
        """Update a single player with network data"""
        try:
            player.x = data.get('x', player.x)
            player.y = data.get('y', player.y)
            player.weapon = data.get('weapon', player.weapon)
            player.facing_right = data.get('facing_right', player.facing_right)
            
            # Update physics
            player.velocity_y = data.get('velocity_y', player.velocity_y)
            player.on_ground = data.get('on_ground', player.on_ground)
            
            # Update health (but only decrease, never increase to prevent healing)
            new_health = data.get('health', player.health)
            if new_health < player.health:
                player.health = new_health
            
            # Sync projectiles
            if 'projectiles' in data:
                player.projectiles = []
                for proj_data in data['projectiles']:
                    if len(proj_data) >= 7:
                        px, py, pdx, pdy, pdamage, pcolor, pexplosion = proj_data
                        weapon_data = WEAPONS.get(player.weapon, WEAPONS["Fist"])
                        new_proj = Projectile(px, py, pdx, pdy, pdamage, weapon_data["speed"], pcolor, pexplosion)
                        player.projectiles.append(new_proj)
            
        except Exception as e:
            print(f"Update single player error: {e}")
                        
    def update_battle(self):
        keys = pygame.key.get_pressed()
        
        # In network mode, only move YOUR player (based on my_player_index)
        if self.is_network_game and self.my_player_index < len(self.all_players):
            my_player = self.all_players[self.my_player_index]
            my_player.move(keys, self.platforms)
            # Handle jump separately (W key for jump, not Space which is for shooting)
            if keys[pygame.K_w] and my_player.on_ground:
                my_player.velocity_y = my_player.jump_power
                my_player.on_ground = False
        else:
            # CPU mode - move player1
            self.player1.move(keys, self.platforms)
            # Handle jump with W
            if keys[pygame.K_w] and self.player1.on_ground:
                self.player1.velocity_y = self.player1.jump_power
                self.player1.on_ground = False
        
        # CPU AI (only in CPU mode)
        if self.is_cpu_mode:
            if self.team_mode_enabled:
                # Update all CPU players
                for cpu_player in self.all_players:
                    if cpu_player != self.player1 and cpu_player.health > 0:
                        self.update_cpu_team(cpu_player)
            else:
                # Normal 1v1 CPU
                self.update_cpu()
        
        # Update all players' projectiles and explosions
        for i, player in enumerate(self.all_players):
            if player.health > 0:
                # Update explosions
                player.update_explosions()
                
                # Check projectiles against barriers
                for proj in player.projectiles[:]:
                    for barrier_owner in self.all_players:
                        if barrier_owner.role == "Engineer" and barrier_owner.team != player.team:
                            for structure in barrier_owner.structures[:]:
                                if structure["type"] == "barrier":
                                    # Check if projectile hits barrier
                                    if (structure["x"] < proj.x < structure["x"] + structure["width"] and 
                                        structure["y"] < proj.y < structure["y"] + structure["height"]):
                                        # Hit barrier!
                                        structure["health"] -= proj.damage
                                        if structure["health"] <= 0:
                                            barrier_owner.structures.remove(structure)
                                            print("🔨 Barrier destroyed!")
                                        if proj in player.projectiles:
                                            player.projectiles.remove(proj)
                                        break
                
                # Check projectiles against all OTHER players
                for other in self.all_players:
                    if other != player and other.health > 0 and not other.is_trapped:
                        # Friendly fire prevention: skip teammates
                        if self.team_mode_enabled and player.team == other.team:
                            continue
                        player.update_projectiles(other)
                
                # Check melee attacks against all OTHER players
                for other in self.all_players:
                    if other != player and other.health > 0:
                        # Friendly fire prevention: skip teammates
                        if self.team_mode_enabled and player.team == other.team:
                            continue
                        if player.check_melee_hit(other):
                            # Melee hit! Show a small visual effect
                            pass
            elif self.team_mode_enabled and not player.is_ghost:
                # Player just died in team mode - turn into ghost
                player.is_ghost = True
                print(f"👻 {player.username} became a ghost!")
                
            # Ghost mode movement (still can move around as spectator)
            if player.is_ghost and player == self.player1:
                # Allow player to move as ghost
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    player.x -= player.speed * 0.5
                if keys[pygame.K_d]:
                    player.x += player.speed * 0.5
                if keys[pygame.K_w]:
                    player.y -= player.speed * 0.5
                if keys[pygame.K_s]:
                    player.y += player.speed * 0.5
            
            # Update trap timers
            if player.is_trapped:
                player.trap_timer -= 1
                if player.trap_timer <= 0:
                    player.is_trapped = False
                    print(f"🔓 {player.username} escaped the trap!")
                else:
                    # Trapped players can't move
                    player.x = player.cage_x
                    player.y = player.cage_y
                    
                    # Teammates can rescue by standing nearby
                    for teammate in self.all_players:
                        if teammate.team == player.team and teammate != player and teammate.health > 0:
                            dist = ((teammate.x - player.x)**2 + (teammate.y - player.y)**2)**0.5
                            if dist < 80:
                                # Rescue progress - free after 2 seconds of contact
                                player.trap_timer -= 5  # Faster escape with help
                                if player.trap_timer <= 0:
                                    player.is_trapped = False
                                    print(f"🆘 {teammate.username} rescued {player.username}!")
            
            # Update trap cooldown
            if player.trap_cooldown_timer > 0:
                player.trap_cooldown_timer -= 1
        
        # Spawn and update collectibles
        self.collectible_spawn_timer += 1
        if self.collectible_spawn_timer >= self.collectible_spawn_interval:
            self.collectible_spawn_timer = 0
            # Spawn a random collectible
            collectible_type = random.choice(["coin", "coin", "health", "speed", "damage"])  # More coins
            
            # 50% chance to spawn on a platform, 50% chance to spawn in air
            if self.platforms and random.random() < 0.5:
                # Spawn on a random platform
                platform = random.choice(self.platforms)
                x = random.randint(int(platform.x + 20), int(platform.x + platform.width - 20))
                y = platform.y - 30  # Slightly above the platform
            else:
                # Spawn randomly in the air
                x = random.randint(100, SCREEN_WIDTH - 100)
                y = random.randint(100, SCREEN_HEIGHT - 250)
            
            self.collectibles.append(Collectible(x, y, collectible_type))
        
        # Update collectibles
        for collectible in self.collectibles[:]:
            if not collectible.update():
                self.collectibles.remove(collectible)
                continue
            
            # Check collection by players
            for player in self.all_players:
                if player.health > 0 and collectible.check_collision(player):
                    if collectible.type == "coin":
                        # Only add coins to player1 (local player)
                        if player == self.player1 or (self.is_network_game and self.all_players[self.my_player_index] == player):
                            player.coins += 5
                            print(f"+5 coins! Total: {player.coins}")
                    elif collectible.type == "health":
                        player.health = min(player.max_health, player.health + 20)
                        print("Health restored!")
                    elif collectible.type == "speed":
                        player.temp_speed_boost = 3
                        player.temp_speed_duration = 300  # 5 seconds
                        print("Speed boost!")
                    elif collectible.type == "damage":
                        player.temp_damage_boost = 5
                        player.temp_damage_duration = 300  # 5 seconds
                        print("Damage boost!")
                    self.collectibles.remove(collectible)
                    break
        
        # Check for winner (in multiplayer or CPU mode)
        if self.is_network_game:
            # Get MY player based on index
            my_player = self.all_players[self.my_player_index] if self.my_player_index < len(self.all_players) else self.player1
            
            # Count alive players
            alive_players = [p for p in self.all_players if p.health > 0]
            
            # ONLY end game when there's exactly 1 player left alive
            if len(alive_players) == 1:
                # One winner! Check if it's ME
                if alive_players[0] == my_player:
                    # I WON!
                    self.coins_earned = 25
                    self.player1.coins += self.coins_earned
                    self.winner = "You"
                    self.loser = "All Others"
                    self.state = GameState.WIN
                    self.network_running = False
                    print(f"I WON! (Player {self.my_player_index}) Showing victory screen")
                else:
                    # Someone else won, I lost
                    self.coins_lost = min(15, self.player1.coins)
                    self.player1.coins -= self.coins_lost
                    winner_index = self.all_players.index(alive_players[0])
                    self.winner = f"Player {winner_index + 1}"
                    self.loser = "You"
                    self.state = GameState.LOSE
                    self.network_running = False
                    print(f"Player {winner_index} WON! I LOST (Player {self.my_player_index})! Showing defeat screen")
            elif len(alive_players) == 0:
                # Everyone died somehow - tie?
                self.state = GameState.LOSE
                self.network_running = False
                print("Everyone died! Game over")
        else:
            # CPU mode
            if self.team_mode_enabled:
                # Team mode: check if all enemy teams are defeated
                player_team = self.player1.team
                alive_players = [p for p in self.all_players if p.health > 0]
                
                # Check if player is alive
                if self.player1.health <= 0:
                    self.coins_lost = min(15, self.player1.coins)
                    self.player1.coins -= self.coins_lost
                    self.winner = "Enemy Team"
                    self.loser = "Your Team"
                    self.state = GameState.LOSE
                else:
                    # Check if any enemy team members are still alive
                    enemy_alive = any(p.team != player_team for p in alive_players)
                    
                    if not enemy_alive:
                        # All enemies defeated! Victory!
                        self.coins_earned = 50  # Bonus coins for team victory
                        self.player1.coins += self.coins_earned
                        self.coins_lost = 0
                        self.winner = "Your Team"
                        self.loser = "Enemy Teams"
                        self.state = GameState.WIN
                        print("🎉 Team Victory!")
            else:
                # Normal 1v1 mode
                if self.player1.health <= 0:
                    self.coins_lost = min(15, self.player1.coins)
                    self.player1.coins -= self.coins_lost
                    self.winner = "CPU"
                    self.loser = "Player 1"
                    self.state = GameState.LOSE
                elif self.player2.health <= 0:
                    self.coins_earned = 25
                    self.player1.coins += self.coins_earned
                    self.coins_lost = 0
                    self.winner = "Player 1"
                    self.loser = "CPU"
                    self.state = GameState.WIN
            
    def update_cpu_team(self, cpu):
        """Update CPU AI for team mode - targets nearest enemy"""
        # Find nearest enemy (different team)
        enemies = [p for p in self.all_players if p.health > 0 and p.team != cpu.team]
        if not enemies:
            return  # No enemies left
        
        # Find closest enemy
        cpu_center_x = cpu.x + cpu.width // 2
        cpu_center_y = cpu.y + cpu.height // 2
        
        target = min(enemies, key=lambda e: ((e.x + e.width//2 - cpu_center_x)**2 + (e.y + e.height//2 - cpu_center_y)**2)**0.5)
        
        # Apply gravity and physics
        cpu.velocity_y += cpu.gravity
        cpu.y += cpu.velocity_y
        
        # Check platform collisions
        cpu.on_ground = False
        for platform in self.platforms:
            if platform.check_collision(cpu, cpu.velocity_y):
                cpu.y = platform.y - cpu.height
                cpu.velocity_y = 0
                cpu.on_ground = True
                break
        
        # Ground collision
        if not cpu.on_ground and cpu.y >= cpu.ground_y:
            cpu.y = cpu.ground_y
            cpu.velocity_y = 0
            cpu.on_ground = True
        
        # Simple AI: move toward target and shoot
        target_center_x = target.x + target.width // 2
        target_center_y = target.y + target.height // 2
        horizontal_distance = abs(cpu_center_x - target_center_x)
        
        # Move toward target
        ideal_distance = 250
        if horizontal_distance > ideal_distance + 50:
            if cpu.x < target.x:
                cpu.x += cpu.speed * 0.8
                cpu.facing_right = True
            else:
                cpu.x -= cpu.speed * 0.8
                cpu.facing_right = False
        elif horizontal_distance < ideal_distance - 50:
            if cpu.x < target.x:
                cpu.x -= cpu.speed * 0.6
                cpu.facing_right = True
            else:
                cpu.x += cpu.speed * 0.6
                cpu.facing_right = False
        
        # Jump occasionally when enemy is on platform above
        if cpu.on_ground and target_center_y < cpu_center_y - 80 and random.random() < 0.02:
            cpu.velocity_y = cpu.jump_power
            cpu.on_ground = False
        
        # Shoot periodically with moderate accuracy
        cpu.shoot_cooldown -= 1
        if cpu.shoot_cooldown <= 0 and horizontal_distance < 400:
            # Shoot with inaccuracy
            offset_x = random.randint(-70, 70)
            offset_y = random.randint(-50, 50)
            cpu.shoot(target_center_x + offset_x, target_center_y + offset_y)
            cpu.shoot_cooldown = random.randint(60, 100)
        
        # Keep CPU on screen
        cpu.x = max(0, min(cpu.x, SCREEN_WIDTH - cpu.width))
    
    def update_cpu(self):
        # HARD AI for CPU with ground-based movement!
        cpu = self.player2
        target = self.player1
        
        # Apply gravity and physics to CPU
        cpu.velocity_y += cpu.gravity
        cpu.y += cpu.velocity_y
        
        # Check platform collisions for CPU
        cpu.on_ground = False
        for platform in self.platforms:
            if platform.check_collision(cpu, cpu.velocity_y):
                cpu.y = platform.y - cpu.height
                cpu.velocity_y = 0
                cpu.on_ground = True
                break
        
        # Ground collision for CPU
        if not cpu.on_ground and cpu.y >= cpu.ground_y:
            cpu.y = cpu.ground_y
            cpu.velocity_y = 0
            cpu.on_ground = True
        
        # Get CPU center position
        cpu_center_x = cpu.x + cpu.width // 2
        cpu_center_y = cpu.y + cpu.height // 2
        target_center_x = target.x + target.width // 2
        target_center_y = target.y + target.height // 2
        
        # Calculate horizontal distance to player
        horizontal_distance = abs(cpu_center_x - target_center_x)
        
        # Strategy timer for movement patterns
        self.cpu_strategy_timer += 1
        
        # Check if CPU should jump onto a platform to reach the player or get better position
        should_jump_for_platform = False
        if cpu.on_ground:
            # Check if player is on a platform above CPU
            if target_center_y < cpu_center_y - 50:  # Player is significantly higher
                # Find if there's a platform nearby that CPU could jump to
                for platform in self.platforms:
                    platform_center_x = platform.x + platform.width / 2
                    horizontal_dist_to_platform = abs(cpu_center_x - platform_center_x)
                    
                    # Platform is near CPU horizontally and above CPU
                    if horizontal_dist_to_platform < 100 and platform.y < cpu.y and platform.y > cpu.y - 150:
                        # Check if platform is between CPU and target or helps get to target
                        if abs(platform_center_x - target_center_x) < abs(cpu_center_x - target_center_x):
                            should_jump_for_platform = True
                            # Move towards platform
                            if cpu_center_x < platform_center_x:
                                cpu.x += cpu.speed * 0.8
                                cpu.facing_right = True
                            else:
                                cpu.x -= cpu.speed * 0.8
                                cpu.facing_right = False
                            
                            # Jump when close enough to platform edge
                            if horizontal_dist_to_platform < 50:
                                cpu.velocity_y = cpu.jump_power
                                cpu.on_ground = False
                                print("CPU jumping to platform!")
                            break
        
        # Moderate dodging - sometimes jump over projectiles
        dodging = False
        if not should_jump_for_platform:
            for proj in target.projectiles:
                # Check if projectile is heading toward CPU at ground level
                dist_to_proj = abs(proj.x - cpu_center_x)
                
                # Jump to dodge if projectile is close and CPU is on ground (35% chance)
                if dist_to_proj < 150 and abs(proj.y - cpu_center_y) < 80 and cpu.on_ground and random.random() < 0.35:
                    cpu.velocity_y = cpu.jump_power
                    cpu.on_ground = False
                    dodging = True
                    print("CPU jumping to dodge!")
                    break
        
        if not dodging and not should_jump_for_platform:
            # Moderate horizontal movement
            ideal_distance = 250  # Optimal shooting distance
            
            if horizontal_distance > ideal_distance + 80:
                # Too far, move closer
                if cpu.x < target.x:
                    cpu.x += cpu.speed * 0.9  # Slower approach
                    cpu.facing_right = True
                else:
                    cpu.x -= cpu.speed * 0.9
                    cpu.facing_right = False
                    
            elif horizontal_distance < ideal_distance - 80:
                # Too close, back away
                if cpu.x < target.x:
                    cpu.x -= cpu.speed * 0.7
                    cpu.facing_right = True
                else:
                    cpu.x += cpu.speed * 0.7
                    cpu.facing_right = False
            else:
                # At good distance - occasionally jump for unpredictability  
                if self.cpu_strategy_timer % 90 == 0 and cpu.on_ground:
                    cpu.velocity_y = cpu.jump_power * 0.9
                    cpu.on_ground = False
                
                # Update facing direction
                cpu.facing_right = cpu.x < target.x
        
        # Keep on screen horizontally
        cpu.x = max(20, min(SCREEN_WIDTH - cpu.width - 20, cpu.x))
        
        # Moderate shooting
        self.cpu_shoot_timer += 1
        shoot_delay = random.randint(50, 90)  # Slower shooting
        
        if self.cpu_shoot_timer > shoot_delay:
            # Less accurate aiming
            predicted_x = target_center_x + random.randint(-60, 60)
            predicted_y = target_center_y + random.randint(-50, 50)
            
            # Moderate accuracy - 60% of shots
            accuracy = 0.60
            if random.random() < accuracy:
                cpu.shoot(predicted_x, predicted_y)
                self.cpu_shoot_timer = 0
            
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if self.state == GameState.USERNAME_INPUT:
                    self.handle_username_input(event)
                elif self.state == GameState.ROLE_SELECT:
                    self.handle_role_select_input(event)
                elif self.state == GameState.CUSTOMIZE:
                    self.handle_customize_input(event)
                elif self.state == GameState.MENU:
                    running = self.handle_menu_input(event)
                elif self.state == GameState.COLOR_SELECT:
                    self.handle_color_select_input(event)
                elif self.state == GameState.BATTLE:
                    self.handle_battle_input(event)
                elif self.state == GameState.SHOP:
                    self.handle_shop_input(event)
                elif self.state == GameState.WIN:
                    self.handle_win_input(event)
                elif self.state == GameState.LOSE:
                    self.handle_lose_input(event)
                elif self.state == GameState.HOST_WAIT:
                    self.handle_host_wait_input(event)
                elif self.state == GameState.JOIN_GAME:
                    self.handle_join_input(event)
                    
            # Update mouse position for weapon aiming during battle
            if self.state == GameState.BATTLE:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Update the local player's mouse target
                if self.is_network_game and self.my_player_index < len(self.all_players):
                    self.all_players[self.my_player_index].target_x = mouse_x
                    self.all_players[self.my_player_index].target_y = mouse_y
                else:
                    self.player1.target_x = mouse_x
                    self.player1.target_y = mouse_y
            
            if self.state == GameState.USERNAME_INPUT:
                self.draw_username_input()
            elif self.state == GameState.ROLE_SELECT:
                self.draw_role_select()
            elif self.state == GameState.CUSTOMIZE:
                self.draw_customize()
            elif self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.COLOR_SELECT:
                self.draw_color_select()
            elif self.state == GameState.BATTLE:
                self.update_battle()
                self.draw_battle()
            elif self.state == GameState.SHOP:
                self.draw_shop()
            elif self.state == GameState.WIN:
                self.draw_win_screen()
            elif self.state == GameState.LOSE:
                self.draw_lose_screen()
            elif self.state == GameState.HOST_WAIT:
                self.draw_host_wait()
            elif self.state == GameState.JOIN_GAME:
                self.draw_join_game()
                
            pygame.display.flip()
            clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()

