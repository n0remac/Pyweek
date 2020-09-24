from colour import Color

from Graphics.PostProcessing.Vignette import Vignette


class Health:
    def __init__(
        self,
        light_source,
        post_processing_manager,
        amount=10,
        max_health=200,
        healthy_color="white",
        dead_color="red",
    ):
        self.light_source = light_source
        self.light_source.radius = max_health
        self.amount = amount
        self.max_health = max_health
        self.max_light_radius = max_health
        self.healthy_color = Color(healthy_color)
        self.dead_color = Color(dead_color)

        # TODO: Pass in values ?
        # used to get some HDR and light bloom going at full HP
        self.light_power_dead = 0.9
        self.light_Power_full = 2.0

        self.vignette_effect = post_processing_manager.get_effect(Vignette)

        # TODO: Expose to constructor ?
        self.vignette_inner_dead = 0.2
        self.vignette_inner_full = 1.0

        self.vignette_outer_dead = 1.25
        self.vignette_outer_full = 2.0

        # assign property at the end as it requires vignette_effect and other values to be set first
        self.health = self.max_health

    def clamp(value, min_val, max_val):
        return min(max(value, min_val), max_val)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = Health.clamp(value, 0.0, self.max_health)

        if self._health <= 0.0:
            # U R HEALL DEAD
            # TODO
            pass

        # Set light radius and color
        self.light_source.radius = self.max_light_radius * self.health_percentage
        self.light_source.color = self.health_color

        # Set vignette effect
        self.vignette_effect.inner_distance = Health.lerp(
            self.vignette_inner_dead, self.vignette_inner_full, self.health_percentage
        )
        self.vignette_effect.outer_distance = Health.lerp(
            self.vignette_outer_dead, self.vignette_outer_full, self.health_percentage
        )

    # Compute a color based on current health
    @property
    def health_color(self):
        a = self.dead_color.hsl
        b = self.healthy_color.hsl

        factor = self.health_percentage

        # This is not great Need real game vector math library
        # Also a color library with no mix or lerp ? (Or i just can't read and find it)
        # lerp between colors in hsl and then convert to rgb.
        result = (Health.lerp(a[x], b[x], factor) for x in range(3))

        ret_val = Color()
        ret_val.set_hsl(result)
        ret_val = ret_val.rgb

        # Apply HRD type stuff
        light_power = Health.lerp(
            self.light_power_dead, self.light_Power_full, self.health_percentage
        )
        # Oh well.
        ret_val = (
            ret_val[0] * light_power,
            ret_val[1] * light_power,
            ret_val[2] * light_power,
        )

        return ret_val

    def lerp(a, b, factor):
        return (a * (1.0 - factor)) + (b * factor)

    @property
    def health_percentage(self):
        return float(self._health) / float(self.max_health)
