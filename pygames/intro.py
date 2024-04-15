import pygame
pygame.init()
screen = pygame.display.set_mode((500,500))
done = False
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pygame.draw.rect(screen,red,[100,30,60,60])
    pygame.draw.polygon(screen,blue,((25,75),(76,125),(275,200),(350,25),(60,280)))
    pygame.draw.circle(screen,white,(180,180),60)
    pygame.draw.line(screen,green,(10,200),(300,10),4)
    pygame.draw.ellipse(screen,red,(250,200,130,80))
    pygame.display.update()