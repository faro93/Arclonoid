import arcade
import sys
import getopt
import random

class BrickBreaker(arcade.Window):
    def __init__(self, argv):
        self.version = "v0.1"
        self.author = "faro"
        self.rdate = "2020/06"

        width = 1280
        height = 720
        title = f'Ball Breaker {self.version} by {self.author} ({self.rdate})'

        try:
            opts, args = getopt.getopt(argv, "h", ["help="])
        except getopt.GetoptError as err:
            self.usage(err)

        for opt, arg in opts:
            if opt in ['-h', '--help']:
                self.usage(0)

        super().__init__(width, height, title, fullscreen = True)

        self.players_list = arcade.SpriteList()
        self.balls_list = arcade.SpriteList()
        self.bricks_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

        self.set_mouse_visible(False)
        self.set_vsync(True)

        self.setup()

    def usage(self, error):
        lines = [f'bb.py [-h]',
                 f'Ball Breaker {self.version} by {self.author}, release date {self.rdate}',
                 f'\nAnother brick breaker using arcade python library',
                 f'arguments are :',
                 f'   -h|--help   to get this help']
        for l in lines:
            print(f'1.{l}')
        sys.exit(error)

    def setup(self):
        self.background = arcade.load_texture("images/ubuntu.matrix.1920x1080.jpg")

        self.player = Player(self.width, self.height)

        self.ball1 = Ball("images/ball.orange.png",
                          self.player.width, self.player.height,
                          self.width, self.height)
        self.balls_list.append(self.ball1)

        self.all_sprites.append(self.player)
        self.all_sprites.append(self.ball1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
            self.width, self.height, self.background)
        self.all_sprites.draw()


    def on_update(self, delta_time):
        self.all_sprites.on_update(delta_time)
        balls = self.player.collides_with_list(self.balls_list)
        if balls:
            for ball in balls:
                ball.collides_paddle(self.player.center_x)


    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            self.close()

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        self.player.motion(x)

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.ball1.MOVE = True

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


class Player(arcade.Sprite):
    def __init__(self, width, height):
        super().__init__("images/aqua.paddle.png")

        self.screen_width = width
        self.screen_height = height
        self.x_new_pos = 0
        self._set_center_x(self.width/2)
        self._set_center_y(self.height)
        print(f'paddle {self.width}x{self.height} ')

    def on_update(self, delta_time):
        x_dist = self.x_new_pos - self.center_x
        if x_dist > 1 or x_dist < 1:
            self.center_x += x_dist * .3

    def motion(self, x):
        self.x_new_pos = x


class Ball(arcade.Sprite):
    def __init__(self, filename, player_width, player_height, screen_width, screen_height):
        super().__init__(filename)

        self.player_width = player_width
        self.player_height = player_height
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.setup()

    def setup(self):
        self._set_center_x(self.screen_width/2)
        self._set_center_y(self.player_height*3)
        self.x_speed = 0 #random.randrange(self.screen_width)
        self.y_speed = 300

        self.MOVE = False

    def on_update(self, delta_time):
        if self.MOVE == True:
            self.center_x += self.x_speed * delta_time
            self.center_y += self.y_speed * delta_time

            if self.left < 0 or self.right > self.screen_width:
                self.x_speed *= -1
            if self.top > self.screen_height:
                self.y_speed *= -1
            if self.bottom < 0:
                self.setup()

    def collides_paddle(self, paddle_center_x):
        self.y_speed *= -1
        if self.center_x < paddle_center_x - 5 or self.center_x > paddle_center_x + 5:
            print(f'{int(self.center_x-paddle_center_x)} ')
            self.x_speed = int(self.center_x-paddle_center_x)*28



if __name__ == "__main__":
    BrickBreaker(sys.argv[1:])
    arcade.run()