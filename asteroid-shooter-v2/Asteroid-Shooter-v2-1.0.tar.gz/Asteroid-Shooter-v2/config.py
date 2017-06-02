"""
Config file that holds constants used throught the program.
Can probably be done much better than this.
"""
import pygame
from utils.vec2d import Vec2d


# Game config
screenWidth = 1000
screenHeight = 700
framerate = 60

# Ship config
shipHealth = 3
shipTranslationSpeed = 0.2
keyToTranslationVector = {
    pygame.K_j: Vec2d((-shipTranslationSpeed, 0)),  # Left
    pygame.K_l: Vec2d((shipTranslationSpeed, 0)),  # Right
    pygame.K_i: Vec2d((0, -shipTranslationSpeed)),  # Up
    pygame.K_k: Vec2d((0, shipTranslationSpeed))  # Down
}

shipRotationSpeed = 0.3
keyToRotationAngle = {
    pygame.K_a: -shipRotationSpeed,  # Counterclockwise
    pygame.K_d: shipRotationSpeed  # Clockwise
}

invincibilityDuration = 3000.0

# BulletController config
timeBetweenBullets = 150
bulletLimit = 15
timeCooldownStart = 700
timeBetweenBulletCooldowns = 100

# Bullet config
bulletTranslationSpeed = 0.4


# Asteroid config
asteroidTranslationSpeed = 0.2

# Homing asteroid config
homingAsteroidTranslationSpeed = 0.15
homingAsteroidRotationSpeed = 4.0

# Health bar config
healthBarMargin = 5

# Bullet spam powerup config
bulletSpamTimeAlive = 5000.0
bulletSpamTimeActive = 5000.0
timeBetweenBulletSpamBullets = 50.0

# Wide bullet powerup config
wideBulletTimeAlive = 5000.0
wideBulletTimeActive = 5000.0

# ScoreBoard config
scoreboardMarginFromScreen = 10
scoreboardHeight = 25

# Level text config
levelTextHeight = 16
levelTextMarginFromScreen = 10

# Ship explosion
shipExplosionScrollPeriod = 200
