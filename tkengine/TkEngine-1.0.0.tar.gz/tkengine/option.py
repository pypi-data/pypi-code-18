from . import scene
import pyglet

class TkOption(scene.TkScene):

	def __init__(self, world):
		super(TkOption, self).__init__(world)
		self.updated_options = self.world.get_options()
		if not len(self.updated_options):
			raise Exception("No world options given.")
		self.text_batch = pyglet.graphics.Batch()
		self.cursor = pyglet.text.Label(">", font_name="Times New Roman", font_size=36,
			x=100, y=300, batch=self.text_batch)
		self.cursor_pos = 0
		self.item_list = []
		self._generate_text()
		self.key_handlers = {
			pyglet.window.key.ESCAPE	: self._quit,
			pyglet.window.key.RETURN	: self._save,
			pyglet.window.key.UP		: lambda: self._move_cursor(1),
			pyglet.window.key.DOWN		: lambda: self._move_cursor(-1),
			pyglet.window.key.LEFT		: lambda: self._update_value(-1),
			pyglet.window.key.RIGHT		: lambda: self._update_value(1)
		}

	def exit(self):
		self.updated_options = self.world.get_options()
		self.cursor_pos = 0
		self.cursor.y = 300

	def on_draw(self):
		self.world.window.clear()
		self.text_batch.draw()

	def _update_value(self, value):
		current = self.updated_options[self.cursor_pos][1]
		min = self.updated_options[self.cursor_pos][2]
		max = self.updated_options[self.cursor_pos][3]
		if min <= current + value <= max:
			self.updated_options[self.cursor_pos][1] = current + value
		for item in self.item_list:
			item.delete()
		self._generate_text()

	def _move_cursor(self, direction):
		self.cursor_pos = (self.cursor_pos - direction) % len(self.updated_options)
		self.cursor.y = 300 - 40 * self.cursor_pos

	def _generate_text(self):
		for i, key in enumerate(self.updated_options):
			self.item_list.append(pyglet.text.Label("{}: {}".format(key[0], key[1]),
				font_name="Times New Roman", font_size=36,
				x=140, y=300 - 40 * i, batch=self.text_batch))
		self.item_list.append(pyglet.text.Label("Press return to save.",
			font_name="Times New Roman", font_size=30,
			x=140, y=300 - 40 * (i + 3), batch=self.text_batch))

	def _quit(self):
		self.world.transition("main")

	def _save(self):
		self.world.set_options(self.updated_options)
		self.world.transition("main")

