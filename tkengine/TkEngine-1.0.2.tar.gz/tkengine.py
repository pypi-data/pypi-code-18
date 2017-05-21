import pyglet, collections, math

class TkWorld(object):

	def __init__(self, window):
		self.window = window
		self.current = None
		self.scenes = {}
		self.options = []
		self.minmax = []

	def get_options(self):
		options = []
		for key in self.options:
			current = self.options.index(key)			
			options.append([key, getattr(self, key), *self.minmax[current]])
		return options

	def set_options(self, new):
		for key, value, min, max in new:
			if key not in self.options:
				self.options.append(key)
				self.minmax.append([min, max])
			current = self.options.index(key)
			if self.minmax[current][0] <= value <= self.minmax[current][1]:
				setattr(self, key, value)

	def transition(self, scene):
		if self.current:
			self.current.unload(self.window)
		self.current = self.scenes[scene]
		self.current.load(self.window)

	def add_scenes(self, new_scenes):
		self.scenes.update(new_scenes)


class TkWindow(pyglet.window.Window):

	def __init__(self, *args, **kwargs):
		super(TkWindow, self).__init__(*args, **kwargs)
		self.center()
		self.clear()
		self.flip()
		self.clear()
		self.set_visible(True)

	def center(self):
		self.set_location(self.screen.width // 2 - self.width // 2,
						self.screen.height // 2 - self.height // 2)


class TkScene(object):

	WINDOW_EVENTS = ["on_draw", "on_mouse_press", "on_mouse_release", "on_mouse_drag", "on_key_press"]

	def __init__(self, world):
		self.world = world

	def on_key_press(self, button, modifiers):
		handler = self.key_handlers.get(button, lambda : None)
		handler()

	def load(self, window):
		for event in TkScene.WINDOW_EVENTS:
			if hasattr(self, event):
				window.__setattr__(event, self.__getattribute__(event))
		if hasattr(self, "entry"):
			self.entry()

	def unload(self, window):
		for event in TkScene.WINDOW_EVENTS:
			if hasattr(self, event):
				window.__setattr__(event, lambda *args: False)
		if hasattr(self, "exit"):
			self.exit()


class TkMenu(TkScene):

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


class TkOption(TkScene):

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

