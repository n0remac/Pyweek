import arcade

from Graphics.SceneRenderer import SceneRenderer

from Graphics.PostProcessing.Tonemap import Tonemap


class RendererFactory:
    def create_renderer(window):

        scene_renderer = SceneRenderer(window)

        # Background color of the scene (replaces the arcade.background thing), is affected by lighting
        scene_renderer.background_color = (0.5, 0.5, 0.5, 1.0)

        # Ambient light value applied to every pixel
        scene_renderer.light_renderer.ambient_light = (1.0, 1.0, 1.0)

        # Setup all post processing
        RendererFactory.setup_post_processing(scene_renderer)

        return scene_renderer

    def setup_post_processing(scene_renderer):

        tonemap = Tonemap()
        scene_renderer.post_processing.add_effect(tonemap)

        # Set what HDR value gets mapped to 100% white on your monitor
        tonemap.white_point = 2.0
