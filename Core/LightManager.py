from Core.RendererFactory import RendererFactory

class LightManager:
    def __init__(self, game_resources, window):

        # create light list
        self.light_list = []

        self.game_resources = game_resources

        # create default scene renderer via factory.
        # This configures the post processing stack and default lighting
        self.scene_renderer = RendererFactory.create_renderer(window)

        # bind rendering callbacks
        self.scene_renderer.draw_primary_callback = self.on_draw_scene
        self.scene_renderer.draw_emissive_callback = self.on_draw_emissive
        self.scene_renderer.draw_after_post_callback = self.on_draw_after_post

        # Set background color
        # Based on old arcade.AMAZON color
        # (59, 122, 87)
        self.scene_renderer.background_color = (
            59.0 / 255.0,
            122.0 / 255.0,
            87.0 / 255.0,
            1.0,
        )

        # dim the ambient lighting to make the player's light more vibrant
        self.scene_renderer.light_renderer.ambient_light = (0.25, 0.25, 0.25)

        self.player_light = self.scene_renderer.light_renderer.create_point_light(
            (400, 400),  # Position
            (
                1.75,
                1.75,
                1.75,
            ),  # Color, 0 = black, 1 = white, 0.5 = grey, order is RGB This can go over 1.0 because of HDR
            160.0,
        )  # Radius

        self.add_lights()
        
    def add_lights(self):
        # dict used to determine radius of light based on light_type
        radius_by_type = {"torch": 70.0, "candle": 40.0}

        for light in self.game_resources.light_list:
            radius = radius_by_type.get(light.properties["type"])
            self.light_list.append(
                self.scene_renderer.light_renderer.create_point_light(
                    (light.center_x, light.center_y),  # Position
                    (
                        1.75,
                        2.75,
                        1.75,
                    ),  # Color, 0 = black, 1 = white, 0.5 = grey, order is RGB This can go over 1.0 because of HDR
                    radius,
                )  # Radius
            )

    # This method should idealy do nothing but invoke the scene renderer. use the following drawing methods instead
    def on_draw(self):
        self.scene_renderer.draw_scene()

    # This method should be used to draw everything efected by lighting and post-processing
    def on_draw_scene(self):
        self.game_resources.on_draw()

    # Everything drawn in here will be drawn with blend mode:Additive. Use for glowing stuff that ignores lighting
    def on_draw_emissive(self):
        pass

    # Drawn after all post processing, for things like UI
    def on_draw_after_post(self):
        pass

    def on_update(self, delta_time):
        # move the player light to the player
        self.player_light.position = (
            self.game_resources.player_sprite.center_x,
            self.game_resources.player_sprite.center_y,
        )