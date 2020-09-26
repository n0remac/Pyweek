
import arcade


class SoundPool():


    def __init__(self, path, count, vol):
        self.index = 0
        self.sounds = []
        self.volume = vol
        for x in range(count):
            self.sounds.append(arcade.load_sound(path))


    def play(self, vol):
        arcade.play_sound(self.sounds[self.index], volume=self.volume)
        self.index += 1

        if self.index >= len(self.sounds):
            self.index = 0