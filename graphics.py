import pygame
from globals import *


class Graphics:
    def __init__(self, notes):
        self.judgement_line = pygame.Rect(0, JUDGEMENT_LINE_POS, WIDTH, LINE_WIDTH)
        self.lane_separators = [pygame.Rect(WIDTH // LANES * i - (LINE_WIDTH / 2), 0, LINE_WIDTH, HEIGHT) for i in
                                range(1, LANES)]
        
        self.font = pygame.font.SysFont("Arial", WIDTH // 4)
        self.notes = notes

        self.combo_text = self.font.render("0", True, COMBO_COL)
        self.accuracy_text = self.font.render("100.00%", True, COMBO_COL)

    def render_combo(self, judge, _):
        self.combo_text = self.font.render(str(judge.combo), True, COMBO_COL)

    def render_accuracy(self, judge, _):
        self.accuracy_text = self.font.render(str(f"{judge.accuracy:.2f}%"), True, COMBO_COL)
    
    def draw(self, screen):
        self.draw_bg(screen)
        self.notes.draw(screen)
        self.draw_ui(screen)

        pygame.display.flip()

    def draw_bg(self, screen):
        screen.fill((0, 0, 0))
        [pygame.draw.rect(screen, LANE_SEP_COL, sep) for sep in self.lane_separators]
        pygame.draw.rect(screen, JUDGEMENT_LINE_COL, self.judgement_line)

    def draw_ui(self, screen: pygame.Surface):
        combo_w, combo_h = self.combo_text.get_size()
        screen.blit(self.combo_text, (WIDTH // 2 - combo_w // 2, HEIGHT // 2 - combo_h // 2))

        acc_w, acc_h = self.accuracy_text.get_size()
        screen.blit(self.accuracy_text, (WIDTH - acc_w, 0))
