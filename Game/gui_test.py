import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

bg_image = pygame.image.load('bg.jpg')
bg_image = bg_image.convert()
bg_image = pygame.transform.scale_by(bg_image, 0.6)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        screen.blit(bg_image, (0, 0))
        pygame.draw.circle(screen, 'red', player_pos, 40)
        
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            player_pos.y += 300 * dt
        if keys[pygame.K_a]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            player_pos.x += 300 * dt
        
        pygame.display.flip()
        
        dt = clock.tick(60) / 1000 # limits to 60 FPS

pygame.quit()