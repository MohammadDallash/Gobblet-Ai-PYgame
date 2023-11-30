class State():
    def __init__(self, game):
        self.game = game
        self.helper = self.game.helper

    def update(self, delta_time, actions):
        pass
    def render(self, surface):
        pass

    def enter_state(self):
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()