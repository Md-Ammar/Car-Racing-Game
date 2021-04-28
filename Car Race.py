import pygame
import os
import random
import math
import accessories as acc
from datetime import datetime


pygame.init()

w, h = 840, 650
win = pygame.display.set_mode((w, h))
pygame.display.set_caption("Car Race")

clock = pygame.time.Clock()

data = os.path.join(os.getcwd(), "data")
os.chdir(data)
bg = pygame.image.load("background.png")
car_img = pygame.transform.scale(pygame.image.load("car.png"), (80, 160))
blue_car_img = pygame.transform.scale(pygame.image.load("car_blue.png"), (80, 160))
yellow_car_img = pygame.transform.scale(pygame.image.load("car_yellow.png"), (80, 160))
car_imgs = [car_img, blue_car_img, yellow_car_img]

run = True

first_img = -h
second_img = 0
Other_cars = []
start = datetime.now().time()

class Car:
    def __init__(self, x, y, vel, img):
        self.x = x
        self.y = y
        self.vel = vel
        self.steer_vel = 10
        self.max_vel = 360
        self.right = False
        self.left = False
        self.distance = 0
        self.img = img
        self.hitbox = pygame.Rect(0, 0, 0, 0)

    def draw(self):
        self.hitbox = pygame.Rect(self.x, self.y, car_img.get_width(), car_img.get_height())
        img = self.img
        if self.left:
            img = pygame.transform.rotate(car_img, self.steer_vel)
        elif self.right:
            img = pygame.transform.rotate(car_img, -self.steer_vel)
        win.blit(img, (self.x, self.y))
        pygame.draw.rect(win, (200, 0, 0), self.hitbox, 3)

    def move(self, m):
        self.y -= m

    def calc_dist(self, t):
        timetaken = str(
            datetime.combine(datetime.today(), datetime.now().time()) - datetime.combine(datetime.today(), start))[0:7]

        min = int(timetaken[2:4])
        sec = int(timetaken[5:])

        if sec > 0:
            self.distance += (self.vel * 3.6) / (sec * 1000)

        acc.text("TIME = " + str(min) + str(sec), 0, 50, (200, 0, 0))
        # acc.text(str(self.distance), 0, 100, (200, 0, 0))


def spawn_car():
    for cars in Other_cars:
        x = random.randrange(150, w - 150 - car.hitbox.width)
        y = random.randrange(-500, 0)
        speed_cap = [car.vel - 20, car.vel + 20]
        if speed_cap[0] <= 0:
            speed_cap[0] = 0
        if y not in range(cars.y, cars.y + car.hitbox.width):
            Other_cars.append(Car(x, y, random.randrange(speed_cap[0], speed_cap[1]), car_imgs[random.randrange(len(car_imgs))]))
            break


def collision():
    for cars in Other_cars:
        if car.hitbox.colliderect(cars.hitbox) or car.x < 150 or car.x + car.hitbox.width > w - 150:
            return True
    return False


def dashboard():
    pygame.draw.rect(win, (0, 0, 0), (0, 0, 250, 100))
    acc.text("SPEED = " + str(car.vel), 0, 0, (200, 0, 0))
    acc.text("DISTANCE = " + str(car.distance), 0, 100, (200, 0, 0))


def redraw():
    global first_img, second_img
    win.fill((200, 200, 200))

    first_img += car.vel
    second_img += car.vel
    if second_img >= 650:
        second_img = first_img
    if first_img >= 0:
        first_img = -(650 - second_img)
    win.blit(bg, (0, first_img))
    win.blit(bg, (0, second_img))

    pygame.draw.line(win, (0, 200, 0), (150, 0), (150, h), 2)
    pygame.draw.line(win, (0, 200, 0), (w - 150, 0), (w - 150, h), 2)

    if len(Other_cars) < 5:
        spawn_car()

    for cars in Other_cars:
        cars.draw()
        cars.move(cars.vel - car.vel)
        acc.text(str(cars.vel), cars.x, cars.y, (0, 200, 200))
        if cars.y <= -1000 or cars.y >= 1000:
            Other_cars.pop(Other_cars.index(cars))

    car.draw()
    car.calc_dist(start)

    dashboard()
    if collision():
        pygame.draw.rect(win, (200, 0, 0), car.hitbox)

    pygame.display.update()


def nav():
    global run
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False

    if keys[pygame.K_UP] and car.vel + 1 <= car.max_vel:
        car.vel += 1
        if car.y >= 400:
            car.y -= 1
    else:
        if car.y <= 450 and car.vel > 0:
            car.y += 1
    if keys[pygame.K_DOWN] and car.vel - 2 >= 0:
        car.vel -= 2
        if car.y <= 500:
            car.y += 1
    else:
        if car.y >= 450 and car.vel > 0:
            car.y -= 1

    if keys[pygame.K_RIGHT] and car.vel > 0:
        car.right = True
        car.x += car.steer_vel
    else:
        car.right = False
    if keys[pygame.K_LEFT] and car.vel > 0:
        car.x -= car.steer_vel
        car.left = True
    else:
        car.left = False

car = Car(250, 450, 0, car_img)
Other_cars.append(Car(random.randrange(0, w - 50), random.randrange(-100, 0), random.randrange(0, 120), car_imgs[random.randrange(len(car_imgs))]))

while run:
    clock.tick(10 + 2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.VIDEORESIZE:
            win = pygame.display.set_mode(event.dict['size'])
            w = win.get_width()
            h = win.get_height()
            print(w, h)

    redraw()
    nav()

pygame.quit()