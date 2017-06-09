#!/usr/bin/env python3
"""
Displays robot fetch at a disco party.
"""
from pymj import load_model_from_path, MjSim, MjViewer
from pymj.modder import TextureModder

model = load_model_from_path("xmls/fetch/main.xml")
sim = MjSim(model)

viewer = MjViewer(sim)
modder = TextureModder(sim)

while True:
    for name in sim.model.geom_names:
        modder.rand_noise(name)

    viewer.render()
