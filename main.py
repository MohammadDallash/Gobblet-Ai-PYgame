from game import Game
#from states.playing import Playing
g=Game()

while g.running:

    g.game_loop()



#testing check wins


# obj = Playing(g)
# obj.board = [
#                 [1,1, 1,16],
#                 [17,18, 17,1],
#                 [1,16, 1,1],
#                 [1,1, 1,1]]
# obj.check_wins()
