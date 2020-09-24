import arcade
import math

from Constants.Game import SPRITE_SCALING_TILES, SPRITE_SCALING_PLAYER, SPRITE_SIZE, AIR_ANGLE, FIRE_ANGLE, WATER_ANGLE, BEAM_ANGLE, CONE_ANGLE, BALL_ANGLE, CONE, BEAM, BALL, AIR, FIRE, WATER
from Constants.UI import INNER_RING_OPACITY, OUTER_RING_OPACITY, RING_ANIM_SPEED

class SelectionRings:
    def __init__(self,game_resources):

        self.game_resources = game_resources

        # Create spell selection ring sprites
        self.inner_ring = arcade.Sprite(
            "Graphics/spell_rings/inner_ring.png", SPRITE_SCALING_PLAYER
        )
        self.outer_ring = arcade.Sprite(
            "Graphics/spell_rings/outer_ring.png", SPRITE_SCALING_PLAYER
        )

        self.inner_ring.alpha = INNER_RING_OPACITY
        self.outer_ring.alpha = OUTER_RING_OPACITY

        self.inner_ring.center_x = self.game_resources.player_sprite.center_x
        self.inner_ring.center_y = self.game_resources.player_sprite.center_y
        self.outer_ring.center_x = self.game_resources.player_sprite.center_x
        self.outer_ring.center_y = self.game_resources.player_sprite.center_y

        # Variables for determining selected spell
        self.selected_element = AIR
        self.selected_attack = CONE

        # Variables for storing the mouse location
        self.mousex = 0
        self.mousey = 0

        # Stores selected spell angle
        self.inner_angle_offset = AIR_ANGLE
        self.outer_angle_offset = CONE_ANGLE

        self.inner_target_angle = self.inner_angle_offset
        self.outer_target_angle = self.outer_angle_offset
        self.absolute_inner_target_angle = self.inner_angle_offset
        self.absolute_outer_target_angle = self.outer_angle_offset

    def on_update(self,delta_time):
        # Make rings follow the player
        self.inner_ring.center_x = self.game_resources.player_sprite.center_x
        self.inner_ring.center_y = self.game_resources.player_sprite.center_y
        self.outer_ring.center_x = self.game_resources.player_sprite.center_x
        self.outer_ring.center_y = self.game_resources.player_sprite.center_y

        #get angle from player to mouse
        start_x = self.game_resources.player_sprite.center_x
        start_y = self.game_resources.player_sprite.center_y
        dest_x = self.mousex
        dest_y = self.mousey

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.degrees(math.atan2(y_diff, x_diff))

        self.inner_angle_offset = lerp(self.inner_angle_offset, self.inner_target_angle, RING_ANIM_SPEED)
        self.outer_angle_offset = lerp(self.outer_angle_offset, self.outer_target_angle, RING_ANIM_SPEED)

        self.inner_ring.angle = angle + self.inner_angle_offset
        self.outer_ring.angle = angle + self.outer_angle_offset

    def rotate_inner_ring(self,dtheta):
        self.inner_angle_offset = self.absolute_angle(self.inner_angle_offset)
        # Accepts a value of 1 or -1, and rotates it 120 degrees in the positive or negative direction
        if (dtheta > 0):
            self.selected_element += 1
        elif (dtheta < 0):
            self.selected_element -= 1

        # Keep selected element in range
        if self.selected_element >= 3:
            self.selected_element = 0
        elif self.selected_element < 0:
            self.selected_element = 2

        if self.selected_element == CONE:
            self.absolute_inner_target_angle = CONE_ANGLE
        elif self.selected_element == BEAM:
            self.absolute_inner_target_angle = BEAM_ANGLE
        elif self.selected_element == BALL:
            self.absolute_inner_target_angle = BALL_ANGLE

        # If distance to the target angle is more than 180 degrees, turn the other way to an equivalent angle
        angle_dist = self.absolute_inner_target_angle-self.inner_angle_offset
        if angle_dist < -180:
            self.inner_target_angle = self.absolute_inner_target_angle + 360
        elif angle_dist > 180:
            self.inner_target_angle = self.absolute_inner_target_angle - 360
        else:
            self.inner_target_angle = self.absolute_inner_target_angle


    def rotate_outer_ring(self,dtheta):
        self.outer_angle_offset = self.absolute_angle(self.outer_angle_offset)
        # Accepts a value of 1 or -1, and rotates it 120 degrees in the positive or negative direction
        if (dtheta > 0):
            self.selected_attack += 1
        elif (dtheta < 0):
            self.selected_attack -= 1

        # Keep selected element in range
        if self.selected_attack >= 3:
            self.selected_attack = 0
        elif self.selected_attack < 0:
            self.selected_attack = 2

        if self.selected_attack == AIR:
            self.absolute_outer_target_angle = AIR_ANGLE
        elif self.selected_attack == FIRE:
            self.absolute_outer_target_angle = FIRE_ANGLE
        elif self.selected_attack == WATER:
            self.absolute_outer_target_angle = WATER_ANGLE

        # If distance to the target angle is more than 180 degrees, turn the other way to an equivalent angle
        angle_dist = self.absolute_outer_target_angle-self.outer_angle_offset
        if angle_dist < -180:
            self.outer_target_angle = self.absolute_outer_target_angle + 360
        elif angle_dist > 180:
            self.outer_target_angle = self.absolute_outer_target_angle - 360
        else:
            self.outer_target_angle = self.absolute_outer_target_angle


    def on_mouse_motion(self, x, y, dx, dy):
        self.mousex = x
        self.mousey = y

    def absolute_angle(self,angle):
        final = angle%360
        if final < 0:
            final += 360
        return final

def lerp(start,end,ratio):
    compare = (start-end)
    if compare == 0:
        return start
    else:
        if ratio >= 0 and ratio <= 1:
            final = (ratio*start) + ((1-ratio)*end)
        else:
            return None
        return final
