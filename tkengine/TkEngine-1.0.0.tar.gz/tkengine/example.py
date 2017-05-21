import pyglet, sys, collections
from .window	import TkWindow
from .world	import TkWorld
from .menu		import TkMenu
from .scene	import TkScene
from .option	import TkOption

class MainMenu(TkMenu):

	def __init__(self, world):
		self.label = "Main Menu"
		self.menu_items = collections.OrderedDict((
			("About"	, lambda : self.world.transition("about")),
			("Options"	, lambda : self.world.transition("option")),
			("Quit"		, lambda : self._quit()),
		))
		super(MainMenu, self).__init__(world)

	def entry(self):
		pyglet.gl.glClearColor(0, 0, 0, 0)

class AboutScene(TkScene):

	def __init__(self, world):
		super(AboutScene, self).__init__(world)
		self.text = pyglet.text.Label("Lorem Ipsum.", font_name="Times New Roman",
			font_size=24, x=self.world.window.width // 2, y=self.world.window.height // 2)

	def on_draw(self):
		self.world.window.clear()
		self.text.draw()

	def on_key_press(self, button, modifiers):
		self.world.transition("main")

class Option(TkOption):

	def __init__(self, world):
		world.set_options([
			["char", 125, 0, 255],
			["int", 42, -2147483648, 2147483647],
			["bool", 0, 0, 1],
			["42 : 69", 42, 42, 69]
		])
		super(Option, self).__init__(world)


def main():
	window = TkWindow(600, 600, visible=False, caption="TkEngine")
	world = TkWorld(window)
	main = MainMenu(world)
	about = AboutScene(world)
	option = Option(world)
	world.add_scenes({"main": main, "about": about, "option": option})
	world.transition("main")
	pyglet.app.run()

if __name__ == "__main__":
	main()