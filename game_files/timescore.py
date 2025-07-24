import pygame

def display_time(screen,chosen_font,start_time):
    """Blits current time passed onto the screen in mm:ss format"""

    current_time = int(pygame.time.get_ticks()/1000)- start_time

    minutes = current_time // 60
    seconds = current_time - (current_time // 60)*60

    time_bg_surf = pygame.Surface((150,60))
    time_bg_rect = time_bg_surf.get_rect(center = (715,72.5) )

    time_surf = chosen_font.render(f'{"{:02d}".format(minutes)}:{"{:02d}".format(seconds)}', False,'#ffffff')
    time_rect = time_surf.get_rect(center = (715,72.5))

    pygame.draw.rect(screen, '#587C4BFF', time_bg_rect,border_radius = 10)
    pygame.draw.rect(screen, "#2B3D25FF", time_bg_rect,5,border_radius = 10)
    screen.blit(time_surf,time_rect)


def display_score(screen,chosen_font,score):
    """Blits current score onto the screen

    i.e. the number of berries that are yet to be placed by the player
    """
    score_bg_surf = pygame.Surface((80,60))
    score_bg_rect = score_bg_surf.get_rect(center = (110,72.5) )

    score_surf = chosen_font.render(f'{"{:02d}".format(score)}', False, '#ffffff')
    score_rect = score_surf.get_rect(center = (110,72.5))

    pygame.draw.rect(screen, '#587C4BFF', score_bg_rect,border_radius = 10)
    pygame.draw.rect(screen, "#2B3D25FF", score_bg_rect,5,border_radius = 10)

    screen.blit(score_surf,score_rect)