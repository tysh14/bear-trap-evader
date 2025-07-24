import pygame
from sys import exit
from random import sample
from game_files.my_sprites import Grass_Tile,Bear_Face
from game_files.timescore import display_score,display_time

pygame.font.init()
pygame.display.init()
pygame.mixer.init()

def restart_game(tile_group, trap_positions, bear):
    """Calls reset methods for all sprites"""
    
    bear.reset_bear()
    Grass_Tile.no_of_revealed_tiles = 0
    for tile in tile_group:
        tile.reset_tile(trap_positions)
    

def animate_bg(bg_xpos, bg2_xpos):
    """Slowly moves background to the left"""

    bg_xpos -=0.5
    bg2_xpos -=0.5

    if bg_xpos <= -970:
        bg_xpos = 970
    elif bg2_xpos <= -970:
        bg2_xpos = 970

    return bg_xpos,bg2_xpos


def main():
    screen = pygame.display.set_mode((850,970))
    pygame.display.set_caption('Beartrap Evader')
    icon = pygame.image.load('game_files/graphics/happy_bear.png')
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()

    #FONTS
    numbers_font = pygame.font.Font('game_files/fonts/plumppixel.medium.ttf',35)
    title_font = pygame.font.Font('game_files/fonts/plumppixel.medium.ttf',80)

    #SOUNDS
    bg_music = pygame.mixer.Sound("game_files/sounds/mischief-in-the-garden-by-audio-library-beats.mp3")
    lose_sound = pygame.mixer.Sound("game_files/sounds/game-over-arcade.mp3")
    win_sound = pygame.mixer.Sound("game_files/sounds/winning.mp3")
    grass_sound = pygame.mixer.Sound("game_files/sounds/click_tile.wav")

    win_sound.set_volume(0.7)
    bg_music.set_volume(0.5)
    bg_music.play(loops = -1)


    ##START PAGE SURFS/RECTS######################
    bg_pos_x = 0
    bg2_pos_x = 970
    bg_image = pygame.image.load('game_files/graphics/big_forest.jpg').convert_alpha()
    bg_image = pygame.transform.scale(bg_image,(970,970))
    bg_rect = bg_image.get_rect(center = (470,485))

    bg_image2 = pygame.image.load('game_files/graphics/big_forest.jpg').convert_alpha()
    bg_image2 = pygame.transform.scale(bg_image,(970,970))

    title_bg_surf = pygame.Surface((600,100))
    title_bg_rect = title_bg_surf.get_rect(center = (425,250))

    title2_bg_surf = pygame.Surface((450,120))
    title2_bg_rect = title2_bg_surf.get_rect(center = (425,345))

    title1_surf = title_font.render("Beartrap", False, '#ffffff')
    title1_rect = title1_surf.get_rect(center = (425,250))

    title2_surf = title_font.render("Evader", False, '#ffffff')
    title2_rect = title2_surf.get_rect(center = (425,345))

    start_text_bg_surf = pygame.Surface((600,60))
    start_text_bg_rect = start_text_bg_surf.get_rect(center = (425,600))

    start_text_surf = numbers_font.render("Press any key to start.", False,"#ffffff")
    start_text_rect = start_text_surf.get_rect(center = (425,600))


    ##GAME PAGE SURFS/RECTS/SPRITES######################
    square_surf = pygame.Surface((800,800))
    square_rect = square_surf.get_rect(center = (425,545))

    border_surf = pygame.Surface((810,810))
    border_rect = border_surf.get_rect(center = (425,545))

    og_score = 35 #const

    trap_pos = sample(range(1,257),og_score) #trap tile indeces

    grass_tiles = pygame.sprite.Group()
    for i in range(256):
        grass_tiles.add(Grass_Tile(trap_pos))
    tile_list = grass_tiles.sprites()

    bear = Bear_Face()
    bear_group = pygame.sprite.GroupSingle()
    bear_group.add(bear)

    bear_frame_surf = pygame.Surface((135,120))
    bear_frame_rect = bear_frame_surf.get_rect(center = (425, 72.5))


    ##LOSE/WIN PAGE SURFS/RECTS######################
    g_over_bg_surf = pygame.Surface((650,120))
    g_over_bg_rect = g_over_bg_surf.get_rect(center = (425,400))

    g_over_text_surf = title_font.render("Game over.", False,"#ffffff")
    g_over_text_rect = g_over_text_surf.get_rect(center = (425,400))

    win_bg1_surf = pygame.Surface((650,100))
    win_bg1_rect = win_bg1_surf.get_rect(center = (425,300))

    win_bg2_surf = pygame.Surface((820,60))
    win_bg2_rect = win_bg2_surf.get_rect(center = (425,400))

    win_text_surf = title_font.render("Well done.", False,"#ffffff")
    win_text_rect = win_text_surf.get_rect(center = (425,300))

    win_text2_surf = numbers_font.render("You evaded all the bear traps.", False,"#ffffff")
    win_text2_rect = win_text2_surf.get_rect(center = (425,400))

    again_bg_surf = pygame.Surface((800,60))
    again_bg_rect = again_bg_surf.get_rect(center = (425,850))

    again_text_surf = numbers_font.render("Press any key to start again.", False,"#ffffff")
    again_text_rect = again_text_surf.get_rect(center = (425,850))

    score = 35 #changes as you place berries

    #game state booleans
    start_page = True
    game_active = False
    lose_page = False
    win_page = False
    end_game_l = False
    end_game_w = False
    pause_game = False

    while True:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game_active:

                #REVEAL TILE EVENT
                if event.type == pygame.MOUSEBUTTONDOWN and square_rect.collidepoint(pygame.mouse.get_pos()) and event.button == 1:
                    for tile in grass_tiles:
                        if tile.rect.collidepoint(pygame.mouse.get_pos()): 
                            outcome = tile.reveal_tile(tile_list)
                            grass_sound.play()
                            if outcome == False:
                                end_game_l = True
                            elif outcome == True:
                                end_game_w = True

                #PLACE BERRY EVENT
                if event.type == pygame.MOUSEBUTTONDOWN and square_rect.collidepoint(pygame.mouse.get_pos()) and event.button == 3:
                    for tile in grass_tiles:
                        if tile.rect.collidepoint(pygame.mouse.get_pos()):
                            new_score = tile.place_berry(score)
                            score = new_score
                            grass_sound.play()

            elif start_page:

                #START GAME EVENT
                if event.type == pygame.KEYDOWN:
                    start_time = int(pygame.time.get_ticks()/1000)
                    start_page = False
                    game_active = True


            elif lose_page or win_page:

                #RESTART GAME EVENT
                if event.type == pygame.KEYDOWN:
                    score = 35
                    trap_pos = sample(range(1,257),og_score)
                    restart_game(tile_list,trap_pos,bear)
                    lose_page = False
                    win_page = False
                    end_game_l = False
                    end_game_w = False
                    game_active = True
                    start_time = int(pygame.time.get_ticks()/1000)

                    
        if game_active:

            screen.blit(bg_image,bg_rect)

            grass_tiles.draw(screen)
            pygame.draw.rect(screen, "#41362f", border_rect,5,border_radius = 10)
            pygame.draw.rect(screen, '#587C4BFF', bear_frame_rect,border_radius = 10)
            pygame.draw.rect(screen, "#2B3D25FF", bear_frame_rect,5,border_radius = 10)
            bear_group.draw(screen)

            display_time(screen,numbers_font,start_time)
            display_score(screen,numbers_font,score)

            #Reveals trap tiles and changes bear face if the player loses
            if end_game_l:

                for index in trap_pos: 
                    tile_list[index-1].image = pygame.image.load('game_files/graphics/trap.jpg').convert_alpha()
                    tile_list[index-1].image = pygame.transform.scale(tile_list[index-1].image,(50,50))
                    screen.blit(tile_list[index-1].image, tile_list[index-1].rect)

                bear.unalive()
                bear_group.draw(screen)
                lose_sound.play()
                game_active = False
                lose_page = True
                pause_game = True


            #Changes bear face to happy face if player wins
            elif end_game_w:

                bear.make_happy()
                bear_group.draw(screen)
                win_sound.play()
                game_active = False
                win_page = True
                pause_game = True

        elif start_page:

            bg_pos_x, bg2_pos_x = animate_bg(bg_pos_x,bg2_pos_x)
            screen.blit(bg_image,(bg_pos_x,0))
            screen.blit(bg_image2,(bg2_pos_x,0))
            pygame.draw.rect(screen, "#3F322DFF",title_bg_rect,border_radius = 10)
            pygame.draw.rect(screen, "#3F322DFF",title2_bg_rect,border_radius = 10)
            pygame.draw.rect(screen, "#3F322DFF",start_text_bg_rect,border_radius = 10)
            screen.blit(title1_surf,title1_rect)
            screen.blit(title2_surf,title2_rect)
            screen.blit(start_text_surf,start_text_rect)


        elif lose_page:

            bg_pos_x, bg2_pos_x = animate_bg(bg_pos_x,bg2_pos_x)
            screen.blit(bg_image,(bg_pos_x,0))
            screen.blit(bg_image2,(bg2_pos_x,0))
            pygame.draw.rect(screen, "#3F322DFF",g_over_bg_rect,border_radius = 10)
            pygame.draw.rect(screen, "#3F322DFF",again_bg_rect,border_radius = 10)
            screen.blit(g_over_text_surf,g_over_text_rect)
            screen.blit(again_text_surf,again_text_rect)


        elif win_page:

            bg_pos_x, bg2_pos_x = animate_bg(bg_pos_x,bg2_pos_x)
            screen.blit(bg_image,(bg_pos_x,0))
            screen.blit(bg_image2,(bg2_pos_x,0))
            pygame.draw.rect(screen, "#3F322DFF",again_bg_rect,border_radius = 10)
            pygame.draw.rect(screen, "#3F322DFF",win_bg1_rect,border_radius = 10)
            pygame.draw.rect(screen, "#3F322DFF",win_bg2_rect,border_radius = 10)
            screen.blit(win_text_surf,win_text_rect)
            screen.blit(win_text2_surf,win_text2_rect)
            screen.blit(again_text_surf,again_text_rect)
        
        pygame.display.update()
        
        if pause_game: #pause before going to lose/win page
            pygame.time.delay(3000)
            pause_game = False

        clock.tick(60)

