import pygame, sys, random # pytgame is important here 


pygame.init()
screen = pygame.display.set_mode((600, 400))  #we set the size of the window



pygame.display.set_caption("Collect 5 Stars") #window title
clock = pygame.time.Clock()

player = pygame.Rect(280, 180, 20, 20) # character is square    

stars = [pygame.Rect(random.randint(0, 570), random.randint(0, 370), 30, 30) for _ in range(5)] # 5 stars randomly placed
font = pygame.font.SysFont(None, 48)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()     #check if the user wants to quit

    keys = pygame.key.get_pressed()
    player.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5 # this is movement 
    player.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 5

    stars = [s for s in stars if not s.colliderect(player)] # collecting stars, if the player touches a star it disappears from the list

    screen.fill((20, 30, 50)) # background color 

    for s in stars: pygame.draw.polygon(screen, (255, 210, 50),
        [(s.centerx, s.y), (s.right, s.centery), (s.left, s.centery)]) # this paints stars as triangles, you can change the shape by changing the points in the list
    pygame.draw.rect(screen, (80, 150, 255), player, border_radius=4) # this is the player, a blue square with rounded corners but also sprite of player can be used instead of a square, you can also change the color of the player by changing the RGB values in the list
    
    if not stars:
        t = font.render("ALL STARS COLLECTED!", True, (255, 210, 40)) # win con 
        screen.blit(t, (300 - t.get_width()//2, 175)) 
    else:
        t = font.render(f"Stars left: {len(stars)}", True, (230, 230, 230))
        screen.blit(t, (10, 10))
        
    player.clamp_ip(screen.get_rect()) # traps the player inside the window, so it can't go outside of the window 
    pygame.display.flip()
    clock.tick(60)
