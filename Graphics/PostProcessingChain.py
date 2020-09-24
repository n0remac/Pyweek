import arcade

from Graphics.RenderTarget import RenderTarget


class PostProcessingChain:
    def __init__(self, context, window_size):
        self.context = context
        self.window_size = window_size

        # draw from ping into pong, then flip
        self.ping_rt = RenderTarget(context, window_size, "f2")
        self.pong_rt = RenderTarget(context, window_size, "f2")

        self.effects = []

    def resize(self, window_size):
        self.window_size = window_size
        self.ping_rt.resize(window_size)
        self.pong_rt.resize(window_size)

        for effect in self.effects:
            effect.resize(window_size)

    def add_effect(self, post_effect):
        if post_effect in self.effects:
            return
        self.effects.append(post_effect)
        post_effect.on_add(self, self.context, self.window_size)

    def remove_effect(self, post_effect):
        self.effects.remove(post_effect)

    def reset_effect_chain(self):
        self.effects = []

    # Apply chain to source target, returning a render target with the final image on it
    def apply_chain(self, source_rendertarget):

        # count active effects
        active_effects = 0
        for effect in self.effects:
            if effect.enabled:
                active_effects += 1

        # none active special case
        if active_effects == 0:
            return source_rendertarget

        # handle special first case
        self.effects[0].apply(source_rendertarget, self.pong_rt)
        self.flip_targets()

        # handle all other cases
        for x in range(1, len(self.effects)):
            effect = self.effects[x]
            effect.apply(self.ping_rt, self.pong_rt)
            self.flip_targets()

        # we always write to pong, but flipping afterwards, so the final image is in ping
        return self.ping_rt

    def flip_targets(self):
        temp = self.ping_rt
        self.ping_rt = self.pong_rt
        self.pong_rt = temp

    def get_effect(self, type):
        for effect in self.effects:
            if isinstance(effect, type):
                return effect
        return None
