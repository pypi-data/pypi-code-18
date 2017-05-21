from . import scene
import pyglet

class TkMenu(scene.TkScene):

	def __init__(self, world, label_x=10, label_y=500):
		super(TkMenu, self).__init__(world)
		assert self.menu_items
		if not hasattr(self, "label"):
			self.label = False
		self.text_batch = pyglet.graphics.Batch()
		self.cursor = pyglet.text.Label(">", font_name="Times New Roman", font_size=36,
			x=200, y=300, batch=self.text_batch)
		self.cursor_pos = 0
		self._generate_text(label_x, label_y)
		self.key_handlers = {
			pyglet.window.key.ESCAPE	: self._quit,
			pyglet.window.key.UP		: lambda: self._move_cursor(1),
			pyglet.window.key.DOWN		: lambda: self._move_cursor(-1),
			pyglet.window.key.ENTER		: self._menu_action
		}

	def exit(self):
		self.cursor_pos = 0
		self.cursor.y = 300

	def _quit(self):
		self.world.window.close()

	def on_draw(self):
		self.world.window.clear()
		self.text_batch.draw()

	def _generate_text(self, label_x, label_y):
		if self.label:
			pyglet.text.Label(self.label, font_name="Times New Roman", font_size=56,
						x=label_x, y=label_y, batch=self.text_batch)

		menu_texts = self.menu_items.keys()
		for i, text in enumerate(menu_texts):
			pyglet.text.Label(text, font_name="Times New Roman", font_size=36,
				x=240, y=300 - 40 * i, batch=self.text_batch)

	def _menu_action(self):
		actions = list(self.menu_items.values())
		actions[self.cursor_pos]()

	def _move_cursor(self, direction):
		self.cursor_pos = (self.cursor_pos - direction) % len(self.menu_items)
		self.cursor.y = 300 - 40 * self.cursor_pos

