from colour import Color


class Health:
    def __init__(
        self,
        light_source,
        amount=10,
        max_health=200,
        healthy_color="white",
        dead_color="red",
    ):
        self.light_source = light_source
        self.light_source.radius = max_health
        self.amount = amount
        self.max_health = 200
        self.healthy_color = Color(healthy_color)
        self.dead_color = Color(dead_color)
        self.color_range = list(
            self.healthy_color.range_to(self.dead_color, max_health // amount + 1)
        )
        self.color_selector = 0
        print(light_source.color)

    def heal(self):
        print(self.light_source.color)
        if self.light_source.radius < self.max_health:
            self.light_source.radius += self.amount
            self.light_source.color = self.color_range[
                (self.max_health - self.light_source.radius) // 10
            ].rgb

    def hurt(self):
        if self.light_source.radius > 0:
            self.light_source.radius -= self.amount
            self.light_source.color = self.color_range[
                (self.max_health - self.light_source.radius) // 10
            ].rgb
