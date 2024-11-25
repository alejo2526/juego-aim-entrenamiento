def main():
    # Función principal que maneja el flujo del juego
    game = Game()
    
    while True:
        if game.game_state == "enter_name":
            game.enter_name()
        elif game.game_state == "menu":
            game.show_menu()
        elif game.game_state == "playing":
            game.run()
        elif game.game_state == "game_over":
            game.show_game_over()

if __name__ == "__main__":
    main()