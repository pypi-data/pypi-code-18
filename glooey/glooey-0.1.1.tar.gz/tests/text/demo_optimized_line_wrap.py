#!/usr/bin/env python3

import pyglet
import glooey
import run_demos

window = pyglet.window.Window()
gui = glooey.Gui(window)
labels = [
        glooey.Label(glooey.drawing.lorem_ipsum(10), 200),
        glooey.Label(glooey.drawing.lorem_ipsum(10), 200),
]

@run_demos.on_space(gui) #
def test_label():
    gui.clear()
    gui.add(labels[0])
    yield "Fill the screen with 1 paragraph."

    gui.clear()
    vbox = glooey.VBox()
    vbox.default_cell_size = 0
    vbox.add(labels[0])
    vbox.add(labels[1])
    gui.add(vbox)
    yield "Fill the screen with 2 paragraphs."

    vbox.width_hint = 500
    vbox.alignment = 'center'
    yield "Squish the paragraphs a little bit."

pyglet.app.run()


