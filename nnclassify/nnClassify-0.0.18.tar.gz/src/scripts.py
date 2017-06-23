from src.Main_ import Main
import argparse

def create_model():
    parser = argparse.ArgumentParser()
    parser.add_argument("Model_Name", help="What would you" 
            + "like your model to be called")
    args = parser.parse_args()

    Main.create_model(args.Model_Name)
    return

