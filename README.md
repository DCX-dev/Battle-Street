# Battle Street

A kid-friendly battle game vs CPU made with Pygame!

## Features

- **vs CPU Mode**: Battle against a challenging AI opponent with advanced tactics, dodging, and 85% accuracy!
- **LAN Multiplayer**: Play with up to 10 players on separate computers over the same WiFi network!
- **Lobby Codes**: Each lobby gets a unique 6-character code for easy joining!
- **Auto Server Discovery**: Games are automatically found OR join by typing the lobby code!
- **Lobby System**: Host creates a lobby, players join, and host starts when ready (min 2 players)
- **Mouse-Aimed Shooting**: Shoot projectiles toward your mouse cursor for precise aiming
- **Visual Weapons**: See the weapons equipped on your character!
- **Win/Lose Screens**: Shows which player won/lost with coins earned or lost
- **Coin Rewards & Penalties**: Win 25 coins per victory, lose up to 15 coins per defeat
- **Scrolling Shop System**: Browse through all items with smooth scrolling - no items hidden!
- **Beautiful UI**: Gradient backgrounds, smooth buttons, and polished screens
- **Street Background**: Battle on an actual street with buildings, sidewalks, and road markings!
- **Shop System**: Buy new weapons and upgrades with coins you earn from winning battles
- **Coin System**: Each player has their own coins (CPU doesn't earn coins)
- **Auto-Save**: Your coins, weapons, and upgrades are automatically saved!
- **16 Explosive Weapons**: Start with your fists, then upgrade to cartoon grenades, missiles, and bombs!
- **Henry Stickmin Style**: Pure cartoon explosives and melee combat - perfect for E10+ rating!
- **Cartoon Explosions**: Colorful, fun explosion effects on every weapon hit!
- **Upgrades**: Speed Boost, Health Up, and Shield
- **Melee & Ranged**: Start with your fists, then blast enemies with comedic explosives!

## Installation

1. Make sure you have Python 3 installed
2. Install pygame:
   ```bash
   pip install pygame
   ```
   or
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

Run the game:
```bash
python battle_game.py
```

### Controls

**Both CPU and LAN Mode:**
- A/D: Move left/right
- W: Jump
- Left Click: Shoot toward mouse cursor
- ESC: Return to menu

**Note:** In LAN multiplayer, each player uses A/D/W + mouse on their own computer to control their own character!

### Menu Navigation
- Arrow Keys: Navigate menu options
- Enter: Select
- ESC: Return to main menu (during game)

### Shop
- Up/Down: Browse items
- B: Buy selected item (adds weapon to inventory or applies upgrade)
- E: Equip selected weapon (if you own it)
- ESC: Return to menu

## Gameplay

### Single Player (vs CPU)
1. Start a battle against the CPU
2. Battle by moving with WASD and clicking to shoot at your mouse cursor
3. Reduce the CPU's health to zero to win
4. **Win:** Earn 25 coins and see the victory screen!
5. **Lose:** Lose up to 15 coins (but never below 0)
6. After each battle, press ESC to return to the menu
7. Visit the shop to buy better weapons and upgrades with your earned coins
8. **Weapons:** Press B to buy (adds to inventory), press E to equip any owned weapon
9. **Upgrades:** Press B to buy and automatically apply the upgrade
10. **Note:** When you buy upgrades, the CPU also gets a small random upgrade to keep it balanced!

### LAN Multiplayer (2-10 Players)
1. **Host** selects "Host LAN Game" - creates a lobby with a unique 6-character code
2. **Join** players have TWO options:
   - **Type the lobby code** at the top of the screen and press ENTER
   - **Select from available games** list (auto-scans the network)
3. **Lobby System:**
   - Host sees a unique code (e.g., "A7B2K9") - share this with friends!
   - **Character Selection**: Use ←→ arrows to choose your color (10 colors available!)
   - Taken colors show with an X - can't pick the same color as another player
   - Shows all connected players with their chosen colors (up to 10)
   - Host can press ENTER to start when 2+ players have joined
   - Cannot start with only 1 player
   - Each player has their own shop, coins, and weapons on their own computer
4. Both computers must be on the same WiFi network
5. Each player uses A/D/W + mouse on their own computer
6. Battle in a free-for-all until one player wins!

## Weapons - Pure Cartoon Explosives! 💥

### Melee
- **Fist** (FREE) - Damage: 8 - Your starting weapon! Punch 'em! 👊

### Cartoon Bombs & Grenades (Henry Stickmin Style!)
- **Splat Bomb** ($40) - Damage: 12 - Colorful splat explosion! 💥
- **Confetti Bomb** ($60) - Damage: 14 - Party time explosion! 🎉
- **Pie Bomb** ($80) - Damage: 16 - Classic slapstick comedy! 🥧
- **Whoopee Cushion** ($100) - Damage: 18 - Silly sound blast! 💨
- **Cartoon Grenade** ($120) - Damage: 20 - Kid-friendly cartoon boom! 💚
- **Glitter Grenade** ($140) - Damage: 22 - Sparkly explosion! ✨
- **Smoke Bomb** ($160) - Damage: 24 - Disappear in a puff! 💨
- **Bubble Mine** ($180) - Damage: 26 - Pops into giant bubbles! 🫧
- **Sticky Bomb** ($260) - Damage: 34 - Sticks then BOOM! 💥

### Cartoon Rockets & Missiles
- **Rubber Rocket** ($200) - Damage: 28 - Bouncy missile fun! 🚀
- **TNT Stick** ($220) - Damage: 30 - Classic cartoon TNT! 🧨
- **Foam Missile** ($240) - Damage: 32 - Soft but powerful! 🚀
- **Super Grenade** ($280) - Damage: 36 - Super-powered boom! 💣
- **Mega Rocket** ($320) - Damage: 40 - The ultimate cartoon rocket! 🚀💥
- **Nuke Launcher** ($400) - Damage: 45 - The BIGGEST cartoon explosion! ☢️💥

## Upgrades

- **Speed Boost** (40 coins) - Move faster
- **Health Up** (60 coins) - Increase maximum health
- **Shield** (100 coins) - Reduce incoming damage

Have fun battling on Battle Street! 🎮

