import math

class player(object):
    def __init__(self, name, level):
        self.name = name
        self.health = 100
        self.gear = [pistol(level)]
        self.activeWeapon = self.gear[0]
        self.path = 'link.png'

    def attack(self, direction):
        self.activeWeapon.ammo -= 1
        if self.activeWeapon.ammo == 0:
            self.gear.remove(0)
        # Maybe trigger the shooting animation here?

    def jump(self):
        pass

class heart(object):
    path = 'heart.png'
    def __init__(self, difficulty):
        self.health = int(50 * math.log(difficulty)) # Heart is not infinitely powerful, the powerup provided gradually levels off


class weapon(object):
    def __init__(self, difficulty):
        self.level = difficulty
        self.damage = 10 * difficulty
        self.ammo = 50
        self.image = 'path to image of weapon' # Haven't found images to use yet
        self.travelSpeed = 2


class pistol(weapon):
    pass

class rocket(weapon):
    def __init__(self, difficulty):
        super().__init__(difficulty)
        self.damage = 20 * difficulty
        self.ammo = 10
        self.travelSpeed = 1

class sword(weapon):
    def __init__(self, difficulty):
        super().__init__(difficulty)
        self.damage = 10 * difficulty
        self.ammo = 100

class enemy(object):
    enemyCount = 0  # Should not go higher than 25? Or it can increase dynamically as player progresses through levels
    path = 'goomba.png'  # Goomba sprite courtesy of https://toppng.com/vector-goomba-super-mario-bros-goomba-sprite-PNG-free-PNG-Images_199959
    def __init__(self, name, level):
        self.name = name
        self.health = 20 * level
        enemy.enemyCount += 1

class projectile(object):
    def __init__(self, drow, dcol, damage, speed, player=True):
        self.drow = drow
        self.dcol = dcol
        self.damage = damage
        self.speed = speed
        if player is False:
            self.enemy = True
        else:
            self.enemy = False

#class map(object):
#    level = 1

# vex1 = enemy('Goblin')
# vex2 = enemy('Minotaur')
