import pygame

import colors
import config

from asteroid.asteroid_controller import AsteroidController
from events.eventSpawner import EventSpawner

from assets import backgroundSoundDir, bulletSoundDir, shipHitSoundDir
from ship.ship import Ship
from utils.vec2d import Vec2d
from utils.collisions import doCollide
from bullet.bullet_controller import BulletController
from visuals.screen_visuals import VisualsController
from powerups.powerup_controller import PowerupController
from gameover.ship_explosion import ShipExplosion
from utils.timer import Timer


class Game(object):

    def __init__(self):

        # Initialize imported pygame modules.
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.mixer.init()

        # Initialize screen object.
        # All visual game objects will have a refrence to this
        # screen object so they can draw to it.
        self.screen = pygame.display.set_mode(
            (config.screenWidth, config.screenHeight),
            0, 32)

        # Clock is used to track and control the framerate of the game.
        self.clock = pygame.time.Clock()

        # Game states
        self.paused = 0
        self.running = 1
        self.gameover = 0

        # Sound objects
        self.initSounds()

        # Game stats
        self.stats = {'score': 0, 'level': 1}

        # Game objects
        initialShipPos = Vec2d((config.screenWidth / 2,
                                config.screenHeight / 2))
        self.ship = Ship(self.screen, initialShipPos)
        self.shipBulletController = BulletController(self.screen, self.ship,
                                                     self.bulletSound)

        self.asteroidController = AsteroidController(self.screen, self.ship)

        # Powerup controller
        self.powerupController = PowerupController(self.screen, self.ship,
                                                   self.shipBulletController)

        # Event spawner
        self.eventSpawner = EventSpawner(self.asteroidController,
                                         self.powerupController,
                                         self.stats)

        # Screen visuals
        self.visualsController = VisualsController(self.screen,
                                                   self.asteroidController,
                                                   self.shipBulletController,
                                                   self.ship, self.stats)

        # Ship explosion
        self.explosion = None  # Will initialize during game over sequence.

    def run(self):

        while self.running:

            # Get time between last and current frame.
            timePassed = self.clock.tick(config.framerate)

            self.handleKeyboardEvents()

            if not self.paused:
                self.update(timePassed)

            self.draw()

    def handleKeyboardEvents(self):
        """
        Get all keyboard events and handles them accordingly.

        Keyboard events related to game states(paused, running,...)
        should only be handled when the key is pressed down(not held).

        Keyboard events related to game actions are handled whenever.
        """

        # Handle keyboard events for game states.
        for event in pygame.event.get():

            # Handle if user closed pygame window.
            if event.type == pygame.QUIT:
                self.running = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = 0
                elif event.key == pygame.K_p:
                    self.paused = not self.paused

        keysPressed = pygame.key.get_pressed()
        # Send keyboard input to ship
        self.ship.getKeyboardInput(keysPressed)
        self.shipBulletController.getKeyboardInput(keysPressed)

    def update(self, timePassed):
        """
        Updates all relevant game objects with timePassed.

        Args:
            timePassed: Time between last and current frame.
        """

        # Update ship and it's bullet controller.
        if not self.gameover:
            self.ship.update(timePassed)
        self.shipBulletController.update(timePassed)

        # Update asteroids, through their controller.
        self.asteroidController.updateAsteroids(timePassed)

        # Update powerups.
        self.powerupController.updatePowerups(timePassed)

        # Handle collisions.
        self.handleCollisions()

        # Update level.
        self.updateLevel()

        # Spawn new events
        if not self.gameover:
            self.eventSpawner.spawnRandomEvent()

        # Game over sequence
        if self.gameover:
            self.explosion.update(timePassed)
            self.endGameTimer.update(timePassed)

        # Maintain game objects.
        self.maintainGameObjects()

    def draw(self):
        """
        Draws all relevant game objects to the screen.
        """
        self.screen.fill(colors.black)

        # Draw ship and bullets from it's bullet controller.
        if not self.gameover:
            self.ship.blitMe()
        self.shipBulletController.blitBullets()

        # Draw asteroids.
        self.asteroidController.blitAsteroids()

        # Draw powerups.
        self.powerupController.drawPowerups()

        # Draw screen visuals.
        self.visualsController.blitMe()

        # Game over sequence.
        if self.gameover:
            self.explosion.blitMe()

        # Actually draw all objects to the screen.
        pygame.display.flip()

    def maintainGameObjects(self):
        # Maintain bullets.
        self.shipBulletController.maintainBullets()

        # Maintain asteroids.
        self.asteroidController.maintainAsteroids()

        # Maintain powerups.
        self.powerupController.maintainPowerups()

    def clearGameObjects(self):
        # Clear bullets.
        self.shipBulletController.clearBullets()

        # Clear asteroids.
        self.asteroidController.clearAsteroids()

        # Clear powerups.
        self.powerupController.clearPowerups()

    def handleCollisions(self):

        # Between ship and asteroids.
        if not self.ship.isInvincible:
            for asteroid in self.asteroidController.asteroids:
                if doCollide(self.ship, asteroid):
                    # Remove asteroid.
                    self.asteroidController.asteroids.remove(asteroid)

                    # Tell ship it has collided with an asteroid.
                    isShipAlive = self.ship.shipCollided()
                    if not isShipAlive:
                        self.initializeGameOverSequence()
                        return
                    else:
                        self.shipHitSound.play()

        # Between bullet and asteroids.
        for bullet in self.shipBulletController.bullets:
            for asteroid in self.asteroidController.asteroids:
                if doCollide(bullet, asteroid):
                    # Remove bullet and asteroid, and move on to next bullet.
                    self.stats['score'] += 1

                    self.shipBulletController.bullets.remove(bullet)
                    self.asteroidController.asteroids.remove(asteroid)

                    break

        # Between ship and powerups.
        self.powerupController.handleCollisionsWithShip()

    def initializeGameOverSequence(self):
        self.gameover = 1
        self.explosion = ShipExplosion(self.screen, self.ship.pos)
        self.clearGameObjects()
        self.stopSounds()
        self.createEndGameTimer()

    def initSounds(self):
        self.backgroundSound = pygame.mixer.Sound(backgroundSoundDir)
        self.backgroundSound.set_volume(0.2)
        self.backgroundSound.play(-1)

        self.bulletSound = pygame.mixer.Sound(bulletSoundDir)
        self.bulletSound.set_volume(0.1)

        self.shipHitSound = pygame.mixer.Sound(shipHitSoundDir)
        self.shipHitSound.set_volume(0.2)

    def stopSounds(self):
        self.backgroundSound.stop()

    def createEndGameTimer(self):
        self.endGameTimer = Timer(5000.0, self.endGame, callLimit=1)

    def endGame(self):
        self.running = 0

    def updateLevel(self):
        currentLevel = self.stats['level']
        currentScore = self.stats['score']

        currentLevelTarget = 10 * currentLevel * currentLevel

        if currentScore >= currentLevelTarget:
            self.stats['level'] += 1
