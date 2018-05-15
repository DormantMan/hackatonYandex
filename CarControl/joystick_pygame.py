import pygame
from joystick_cmd import Joystick

pygame.init()


class Label:
    def __init__(self, rect, text, text_color='grey', background_color='blue'):
        self.rect = pygame.Rect(rect)
        self.text = text
        if background_color != '-1':
            self.bgcolor = pygame.Color(background_color)
        else:
            self.bgcolor = None
        self.font_color = pygame.Color(text_color)
        # Рассчитываем размер шрифта в зависимости от высоты
        self.font = pygame.font.Font(None, self.rect.height - 16)
        self.rendered_text = None
        self.rendered_rect = None

    def render(self, surface):
        if self.bgcolor:
            surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 10, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)


class Button(Label):
    def __init__(self, rect, text, text_color='grey', background_color='blue'):
        super().__init__(rect, text, text_color='grey', background_color='blue')
        self.bgcolor = pygame.Color('blue')
        # при создании кнопка не нажата
        self.pressed = False
        self.click = False
        self.mouse_on = False

    def render(self, surface):
        self.click = False
        if self.mouse_on:
            surface.fill(pygame.Color('lightblue'), self.rect)
        else:
            surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        text_width = self.rendered_text.get_rect().width
        if text_width > self.rect.width:
            width_delta = text_width / self.rect.width
            text = self.text[:int(len(self.text) / width_delta) - 2]
            text += '...'
            self.rendered_text = self.font.render(text, 1, self.font_color)
        if not self.pressed:
            color1 = pygame.Color('white')
            color2 = pygame.Color('black')
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 5, centery=self.rect.centery)
        else:
            color1 = pygame.Color('black')
            color2 = pygame.Color('white')
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 7, centery=self.rect.centery + 2)

        # рисуем границу
        pygame.draw.rect(surface, color1, self.rect, 2)
        pygame.draw.line(surface, color2, (self.rect.right - 1, self.rect.top), (self.rect.right - 1, self.rect.bottom),
                         2)
        pygame.draw.line(surface, color2, (self.rect.left, self.rect.bottom - 1),
                         (self.rect.right, self.rect.bottom - 1), 2)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.rect.collidepoint(*event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False
            self.click = self.rect.collidepoint(*event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(*event.pos):
                self.mouse_on = True
            else:
                self.mouse_on = False

        if self.pressed:
            return True


class TextBox(Label):
    def __init__(self, rect, text, max_len=None):
        super().__init__(rect, text, background_color='white')
        self.active = False
        self.blink = True
        self.blink_timer = 0
        self.cursor_position = 0
        self.cursor_pixels_pos = 0
        self.max_len = max_len

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.get_symb_by_click(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.execute()
            elif event.key == pygame.K_BACKSPACE:
                if len(self.text) > 0 and self.cursor_position != 0:
                    # print(self.text, end=' ')
                    text = self.text[:self.cursor_position - 1]
                    # print(text, end=' ')
                    text += self.text[self.cursor_position:]
                    # print(text)
                    self.text = text
                    self.cursor_position -= 1
            elif event.key == pygame.K_TAB:
                pass
            elif event.key == pygame.K_LEFT:
                if self.cursor_position != 0:
                    self.cursor_position -= 1
                    # print(self.cursor_position)
            elif event.key == pygame.K_RIGHT:
                if self.cursor_position <= len(self.text) - 1:
                    self.cursor_position += 1
            else:
                if event.unicode not in 'abcdefghijklmnopqrstuvwxyz' \
                                        'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
                                        'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' \
                                        'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' \
                                        ',.1234567890 ':
                    print('Invalid symbol:', event.unicode)
                    return

                if pygame.K_LSHIFT in pygame.key.get_pressed():
                    symb = event.unicode.upper()
                else:
                    symb = event.unicode

                if symb == '':
                    return

                if len(self.text) == self.max_len:
                    return
                if not self.max_len:
                    lasts = self.rect.width - self.rendered_rect.width
                    newsymb = self.font.render(symb, 1, self.font_color).get_rect().width
                    if newsymb + 5 > lasts:
                        return

                if self.cursor_position != len(self.text):
                    text = self.text[:self.cursor_position]
                    # print(text, end=' ')
                    text += symb
                    # print(text, end=' ')
                    text += self.text[self.cursor_position:]
                    # print(text)
                    self.text = text
                else:
                    self.text += symb

                if symb != '':
                    self.cursor_position += 1

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(*event.pos)

        if self.active:
            return True

    def get_symb_by_click(self, pos):
        x, y = pos
        if self.rect.collidepoint(x, y):
            x -= self.rect.x
            for ind, symb in enumerate(self.text):
                newsymb = self.font.render(symb, 1, self.font_color).get_rect().width
                x -= newsymb
                if x <= 0:
                    self.cursor_position = ind
                    break
            if x >= 0:
                self.cursor_position = len(self.text)

    def update(self):
        if pygame.time.get_ticks() - self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()

    def render(self, surface):
        super(TextBox, self).render(surface)
        if self.blink and self.active:
            ind = 0
            self.cursor_pixels_pos = 0
            while self.cursor_position != len(self.text) + ind:
                ind -= 1
                try:
                    symb = self.text[ind]
                except IndexError:
                    self.cursor_position = 0
                    break
                rendered_symb = self.font.render(symb, 1, self.font_color)
                symb_rect = rendered_symb.get_rect()
                self.cursor_pixels_pos += symb_rect.width + 2
            x_pos = self.rendered_rect.right - 2 - self.cursor_pixels_pos
            pygame.draw.line(surface, pygame.Color('black'),
                             (x_pos, self.rendered_rect.top + 2),
                             (x_pos, self.rendered_rect.bottom - 2))

    def execute(self):
        self.active = False
        search(self.text)


class GUI:
    def __init__(self):
        self.elements = []

    def add_elements(self, *elements):
        for el in elements:
            self.elements.append(el)

    def render(self, surface):
        for element in self.elements:
            render = getattr(element, 'render', None)
            if callable(render):
                element.render(surface)

    def update(self):
        for element in self.elements:
            update = getattr(element, 'update', None)
            if callable(update):
                element.update()

    def get_event(self, event):
        ui_hovered = False
        for element in self.elements:
            get_event = getattr(element, 'get_event', None)
            if callable(get_event):
                collided = element.get_event(event)
                if collided:
                    ui_hovered = True
        return ui_hovered

DEBUG = False

if not DEBUG:
    joystick = Joystick()
WIDTH, HEIGHT = 720, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('RC CAR')

bckg = pygame.image.load('joystick.jpg')

btn_upup = Button((190, 330, 40, 30), '')
btn_down = Button((190, 390, 40, 30), '')
btn_left = Button((160, 360, 40, 30), '')
btn_righ = Button((220, 360, 40, 30), '')
btn_reset = Button((430, 350, 50, 50), '')

key_upup = False
key_down = False
key_left = False
key_righ = False

gui = GUI()
gui.add_elements(btn_upup, btn_down, btn_left, btn_righ, btn_reset)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        gui.get_event(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                key_upup = True
            elif event.key == pygame.K_s:
                key_down = True
            elif event.key == pygame.K_a:
                key_left = True
            elif event.key == pygame.K_d:
                key_righ = True
            elif event.key == pygame.K_r:
                btn_reset.click = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                key_upup = False
            elif event.key == pygame.K_s:
                key_down = False
            elif event.key == pygame.K_a:
                key_left = False
            elif event.key == pygame.K_d:
                key_righ = False

    screen.blit(bckg, (0, 0))

    if not DEBUG:
        joystick.send()
    gui.update()

    if btn_upup.pressed or key_upup:
        print('UP CLICK')
        if not DEBUG:
            joystick.inc_speed()
    elif btn_down.pressed or key_down:
        print('DOWN CLICK')
        if not DEBUG:
            joystick.dec_speed()
    if btn_left.pressed or key_left:
        print('LEFT CLICK')
        if not DEBUG:
            joystick.left()
    elif btn_righ.pressed or key_righ:
        print('RIGHT CLICK')
        if not DEBUG:
            joystick.right()

    if btn_reset.click:
        print('RESET')
        if not DEBUG:
            joystick.reset()

    gui.render(screen)
    pygame.display.flip()
    clock.tick(30)

if not DEBUG:
    joystick.stop()
pygame.quit()
