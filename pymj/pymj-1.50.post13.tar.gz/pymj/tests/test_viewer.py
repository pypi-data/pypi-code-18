from pymj import load_model_from_path, MjSim
from pymj.mjviewer import MjViewer

def test_viewer():
    model = load_model_from_path("pymj/tests/test.xml")
    sim = MjSim(model)
    viewer = MjViewer(sim)
    for _ in range(100):
        sim.step()
        viewer.render()
