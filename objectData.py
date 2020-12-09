import math

class Player(object):
    def __init__(self, name, level):
        self.name = name
        self.health = 100
        self.gear = [Pistol(level)]
        self.activeWeapon = self.gear[0]
        self.path = 'link.png'  # From http://pixelartmaker.com/art/8608a4f38543034

    def attack(self, direction):
        self.activeWeapon.ammo -= 1
        if self.activeWeapon.ammo == 0:
            self.gear.remove(0)


class Heart(object):
    path = 'heart.png'  # From http://pixelartmaker.com/art/58d2cbf24f07452
    def __init__(self, difficulty):
        self.health = int(50 * math.log(difficulty)) # Heart is not infinitely powerful, the powerup provided gradually levels off


class Weapon(object):
    def __init__(self, difficulty):
        self.level = difficulty
        self.damage = 10 * difficulty
        self.ammo = 50
        self.travelSpeed = 2


class Pistol(Weapon):
    pass

class Rocket(Weapon):
    def __init__(self, difficulty):
        super().__init__(difficulty)
        self.damage = 20 * difficulty
        self.ammo = 10
        self.travelSpeed = 1

class Sword(Weapon):
    def __init__(self, difficulty):
        super().__init__(difficulty)
        self.damage = 10 * difficulty
        self.ammo = 100

class Enemy(object):
    enemyCount = 0  # Should not go higher than 25? Or it can increase dynamically as Player progresses through levels
    path = 'goomba.png'  # Goomba sprite courtesy of https://toppng.com/vector-goomba-super-mario-bros-goomba-sprite-PNG-free-PNG-Images_199959
    def __init__(self, name, level):
        self.name = name
        self.health = 20 * level
        Enemy.enemyCount += 1

class Projectile(object):
    def __init__(self, drow, dcol, damage, speed, player=True):
        self.drow = drow
        self.dcol = dcol
        self.damage = damage
        self.speed = speed
        if player is False:
            self.Enemy = True
        else:
            self.Enemy = False

#class map(object):
#    level = 1

# vex1 = Enemy('Goblin')
# vex2 = Enemy('Minotaur')
