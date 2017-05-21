import pyglet, collections, math
from pyglet import gl

class TkWorld(object):

	def __init__(self, window, font=''):
		self.window = window
		self.font = font
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

	def run(self, entry):
		self.transition(entry)
		pyglet.app.run()


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

	def __init__(self, world,  menu_items=None, label="", label_pos=(10, 500), items_pos=(240, 300)):
		super(TkMenu, self).__init__(world)
		if not menu_items:
			menu_items = (("Quit", lambda: self._quit()))
		self.menu_items = collections.OrderedDict(menu_items)
		self.label = label
		self.label_pos = label_pos
		self.items_pos = items_pos
		self.text_batch = pyglet.graphics.Batch()
		self.cursor = pyglet.text.Label(">", font_name=self.world.font, font_size=36,
				x=self.items_pos[0] - 40, y=self.items_pos[1], batch=self.text_batch)
		self.cursor_pos = 0
		self._generate_text()
		self.key_handlers = {
			pyglet.window.key.ESCAPE	: self._quit,
			pyglet.window.key.UP		: lambda: self._move_cursor(1),
			pyglet.window.key.DOWN		: lambda: self._move_cursor(-1),
			pyglet.window.key.ENTER		: self._menu_action
		}

	def exit(self):
		self.cursor_pos = 0
		self.cursor.y = self.items_pos[1]

	def _quit(self):
		self.world.window.close()

	def on_draw(self):
		self.world.window.clear()
		self.text_batch.draw()

	def _generate_text(self):
		pyglet.text.Label(self.label, font_name=self.world.font, font_size=56,
			x=self.label_pos[0], y=self.label_pos[1], batch=self.text_batch)

		menu_texts = self.menu_items.keys()
		for i, text in enumerate(menu_texts):
			pyglet.text.Label(text, font_name=self.world.font, font_size=36,
				x=self.items_pos[0], y=self.items_pos[1] - 40 * i, batch=self.text_batch)

	def _menu_action(self):
		actions = list(self.menu_items.values())
		actions[self.cursor_pos]()

	def _move_cursor(self, direction):
		self.cursor_pos = (self.cursor_pos - direction) % len(self.menu_items)
		self.cursor.y = self.items_pos[1] - 40 * self.cursor_pos


class TkGridMap(TkScene):

	def __init__(self, world, size, scale, Cell, *cell_args, **cell_kwargs):
		super(TkGridMap, self).__init__(world)
		self.size = size
		self.scale = scale
		self.x = self.size // 2
		self.y = self.size // 2
		self.cells = []
		for x in range(1, self.size + 1):
			line = []
			for y in range(1, self.size + 1):
				line.append(Cell(x, y, self.scale, *cell_args, **cell_kwargs))
			self.cells.append(line)
		for x, line in enumerate(self.cells):
			for y in range(0, self.size):
				self.cells[x][y].neighbors = {
					"E": self.cells[(x - 1) % self.size][y],
					"W": self.cells[(x + 1) % self.size][y],
					"S": self.cells[x][(y - 1) % self.size],
					"N": self.cells[x][(y + 1) % self.size],
					"NE": self.cells[(x - 1) % self.size][(y + 1) % self.size],
					"NW": self.cells[(x + 1) % self.size][(y + 1) % self.size],
					"SE": self.cells[(x - 1) % self.size][(y - 1) % self.size],
					"SW": self.cells[(x + 1) % self.size][(y - 1) % self.size]
				}
		self.current = self.cells[self.x][self.y]
		self.current.selected = True
		self.key_handlers = {
			pyglet.window.key.RIGHT : lambda : self.move_cursor(1, 0),
 			pyglet.window.key.LEFT : lambda : self.move_cursor(-1, 0),
			pyglet.window.key.DOWN : lambda : self.move_cursor(0, -1),
			pyglet.window.key.UP : lambda : self.move_cursor(0, 1),
		}

	def move_cursor(self, x, y):
		self.current.selected = False
		self.x = (self.x + x) % self.size
		self.y = (self.y + y) % self.size
		self.current = self.cells[self.x][self.y]
		self.current.selected = True

	def draw(self, _):
		self.world.window.clear()
		for line in self.cells:
			for cell in line:
				cell.draw()


class TkPlainCell(object):

	def __init__(self, x, y, s):
		self.selected = False
		self.neighbors = {}
		self.color = (0.0, 0.0, 0.0)
		self.points = (
			((s * x) + s * 10 * x - s * 5, (s * y) + s * 10 * y - s * 5),
			((s * x) + s * 10 * x - s * 5, (s * y) + s * 10 * y + s * 5),
			((s * x) + s * 10 * x + s * 5, (s * y) + s * 10 * y + s * 5),
			((s * x) + s * 10 * x + s * 5, (s * y) + s * 10 * y - s * 5)
		)
		self.square = gl.glGenLists(1)
		gl.glNewList(self.square, gl.GL_COMPILE)
		self.draw_square()
		gl.glEndList()

	def draw_square(self):
		gl.glBegin(gl.GL_POLYGON)
		gl.glVertex2i(*self.points[0])
		gl.glVertex2i(*self.points[1])
		gl.glVertex2i(*self.points[2])
		gl.glVertex2i(*self.points[3])
		gl.glEnd()

	def draw(self):
		gl.glColor3f(*self.color)
		gl.glCallList(self.square)
		gl.glFlush()


class TkOption(TkScene):

	def __init__(self, world, items_pos=(240, 300)):
		super(TkOption, self).__init__(world)
		self.items_pos = items_pos
		self.updated_options = self.world.get_options()
		if not len(self.updated_options):
			raise Exception("No world options given.")
		self.text_batch = pyglet.graphics.Batch()
		self.cursor = pyglet.text.Label(">", font_name=self.world.font, font_size=36,
			x=self.items_pos[0] - 40, y=self.items_pos[1], batch=self.text_batch)
		self.cursor_pos = 0
		self.item_list = []
		self._generate_text()
		self.key_handlers = {
			pyglet.window.key.UP		: lambda: self._move_cursor(1),
			pyglet.window.key.DOWN		: lambda: self._move_cursor(-1),
			pyglet.window.key.LEFT		: lambda: self._update_value(-1),
			pyglet.window.key.RIGHT		: lambda: self._update_value(1)
		}

	def exit(self):
		self.updated_options = self.world.get_options()
		self.cursor_pos = 0
		self.cursor.y = self.items_pos[1]

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
		self.cursor.y = self.items_pos[1] - 40 * self.cursor_pos

	def _generate_text(self):
		for i, key in enumerate(self.updated_options):
			self.item_list.append(pyglet.text.Label("{}: {}".format(key[0], key[1]),
				font_name=self.world.font, font_size=36,
				x=self.items_pos[0], y=self.items_pos[1] - 40 * i, batch=self.text_batch))
