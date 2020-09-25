import arcade

from Graphics.SceneRenderer import SceneRenderer

from Graphics.PostProcessing.Tonemap import Tonemap
from Graphics.PostProcessing.Bloom import Bloom
from Graphics.PostProcessing.Vignette import Vignette


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

        RendererFactory.setup_bloom(scene_renderer)
        RendererFactory.setup_tonemap(scene_renderer)
        RendererFactory.setup_vignette(scene_renderer)

    def setup_bloom(scene_renderer):
        bloom = Bloom()
        scene_renderer.post_processing.add_effect(bloom)

        # TEMP
        bloom.power = 1.5
        bloom.threshold = 0.75

    def setup_tonemap(scene_renderer):
        tonemap = Tonemap()
        scene_renderer.post_processing.add_effect(tonemap)

        # Set what HDR value gets mapped to 100% white on your monitor
        tonemap.white_point = 3.0

    def setup_vignette(scene_renderer):
        vignette = Vignette()
        scene_renderer.post_processing.add_effect(vignette)
