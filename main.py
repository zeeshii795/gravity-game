 elif current_state == GAME_OVER:
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    game_over_selection = (game_over_selection + 1) % 4
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    game_over_selection = (game_over_selection - 1) % 4
                elif event.key == pygame.K_RETURN:
                    if game_over_selection == 0:  # Play Again
                        reset_game()
                        current_state = PLAYING
                    elif game_over_selection == 1:  # Main Menu
                        current_state = MENU
                    elif game_over_selection == 2:  # Change Character
                        current_state = CHARACTER_SELECT
                        character_select_selection = selected_char
                    elif game_over_selection == 3:  # Quit
                        pygame.quit()
                        sys.exit()
            
            elif current_state == SETTINGS:
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    settings_selection = (settings_selection + 1) % 5
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    settings_selection = (settings_selection - 1) % 5
                elif event.key == pygame.K_RIGHT:
                    if settings_selection == 2:  # Music volume
                        music_volume = min(1.0, music_volume + 0.1)
                        pygame.mixer.music.set_volume(music_volume)
                    elif settings_selection == 3:  # SFX volume
                        sfx_volume = min(1.0, sfx_volume + 0.1)
                elif event.key == pygame.K_LEFT:
                    if settings_selection == 2:  # Music volume
                        music_volume = max(0.0, music_volume - 0.1)
                        pygame.mixer.music.set_volume(music_volume)
                    elif settings_selection == 3:  # SFX volume
                        sfx_volume = max(0.0, sfx_volume - 0.1)
                elif event.key == pygame.K_RETURN:
                    if settings_selection == 0:  # Music toggle
                        music_enabled = not music_enabled
                        if music_enabled:
                            pygame.mixer.music.play(-1)
                        else:
                            pygame.mixer.music.stop()
                    elif settings_selection == 1:  # SFX toggle
                        sfx_enabled = not sfx_enabled
                    elif settings_selection == 4:  # Back to menu
                        current_state = MENU
                elif event.key == pygame.K_ESCAPE:
                    current_state = MENU
        
        # Mouse click handling
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_clicked = True
        
        # Mouse wheel handling
        if event.type == pygame.MOUSEWHEEL:
            mouse_wheel_event = event
    
    # Update and draw based on current state
    if current_state == MENU:
        buttons = draw_menu()
        
        # Check mouse hover for menu
        for i, button in enumerate(buttons):
            if button.collidepoint(mouse_pos):
                menu_selection = i
                if mouse_clicked:
                    play_sound(select_sound)
                    if i == 0:  # Start Game
                        reset_game()
                        current_state = PLAYING
                    elif i == 1:  # Character Select
                        current_state = CHARACTER_SELECT
                        character_select_selection = selected_char
                    elif i == 2:  # Settings
                        current_state = SETTINGS
                        settings_selection = 0
                    elif i == 3:  # Quit
                        pygame.quit()
                        sys.exit()
    
    elif current_state == CHARACTER_SELECT:
        char_buttons, back_button = draw_character_select()
        
        # Check mouse hover for character selection
        for i, button in enumerate(char_buttons):
            if button.collidepoint(mouse_pos):
                character_select_selection = i
                if mouse_clicked and characters[i]["unlocked"]:
                    play_sound(select_sound)
                    selected_char = i
        
        if back_button.collidepoint(mouse_pos):
            if mouse_clicked:
                play_sound(select_sound)
                current_state = MENU
    
    elif current_state == PLAYING:
        result = update_game()
        if result == GAME_OVER:
            current_state = GAME_OVER
        draw_game()
    
    elif current_state == GAME_OVER:
        buttons = draw_game_over()
        
        # Check mouse hover for game over screen
        for i, button in enumerate(buttons):
            if button.collidepoint(mouse_pos):
                game_over_selection = i
                if mouse_clicked:
                    play_sound(select_sound)
                    if i == 0:  # Play Again
                        reset_game()
                        current_state = PLAYING
                    elif i == 1:  # Main Menu
                        current_state = MENU
                    elif i == 2:  # Change Character
                        current_state = CHARACTER_SELECT
                        character_select_selection = selected_char
                    elif i == 3:  # Quit
                        pygame.quit()
                        sys.exit()
    
    elif current_state == SETTINGS:
        buttons = draw_settings()
        
        # Check mouse hover for settings
        for i, button in enumerate(buttons):
            if button.collidepoint(mouse_pos):
                settings_selection = i
                if mouse_clicked:
                    play_sound(select_sound)
                    if i == 0:  # Music toggle
                        music_enabled = not music_enabled
                        if music_enabled:
                            pygame.mixer.music.play(-1)
                        else:
                            pygame.mixer.music.stop()
                    elif i == 1:  # SFX toggle
                        sfx_enabled = not sfx_enabled
                    elif i == 4:  # Back to menu
                        current_state = MENU
        
        # Mouse wheel for volume adjustment
        if mouse_wheel_event:
            if settings_selection == 2:  # Music volume
                music_volume = max(0.0, min(1.0, music_volume + mouse_wheel_event.y * 0.05))
                pygame.mixer.music.set_volume(music_volume)
            elif settings_selection == 3:  # SFX volume
                sfx_volume = max(0.0, min(1.0, sfx_volume + mouse_wheel_event.y * 0.05))
    
    pygame.display.flip()
    clock.tick(60)
