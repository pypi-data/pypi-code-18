from src.Main_ import Main
from src.ImageCropper_ import ImageCropper
import argparse

def create_model():
	parser = argparse.ArgumentParser()
	parser.add_argument("Model_Name", help="What would you" 
			+ "like your model to be called")
	args = parser.parse_args()

	Main.create_model(args.Model_Name)
	return

def crop():
	parser = argparse.ArgumentParser()
	parser.add_argument("Source_Folder", help="The path to the folder"
			+ " you want cropped")
	parser.add_argument("Destination", help="The path to destination location")
	args = parser.parse_args()
	ImageCropper.crop_all_images(args.Source_Folder, args.Destination)
	return

def predict():
	parser = argparse.ArgumentParser()
	parser.add_argument("Set_Name", help="The name of the set of wells to predict")
	parser.add_argument("Model_Name", help="The name of the neural network to use")
	args = parser.parse_args()
	Main.predict(args.Set_Name, args.Model_Name)
	return

def test_individual():
	parser = argparse.ArgumentParser()
	parser.add_argument("Set_Name", help="The name of the test set")
	parser.add_argument("Model_Name", help="The name of the neural network to use")
	args = parser.parse_args()
	Main.test_individual(args.Set_Name, args.Model_Name)
	return

def test_wells():
	parser = argparse.ArgumentParser()
	parser.add_argument("Set_Name", help="The name of the test set")
	parser.add_argument("Model_Name", help="The name of the neural network to use")
	args = parser.parse_args()
	Main.test_wells(args.Set_Name, args.Model_Name)
	return

def train():
	parser = argparse.ArgumentParser()
	parser.add_argument("Training_Set", help="The name of the training set"
			+ " that you want to train on")
	parser.add_argument("Model_Name", help="The model you want to train")
	parser.add_argument("Epochs", help="The number of epochs you want to train on",
			type=int)
	args = parser.parse_args()
	Main.train(args.Training_Set, args.Model_Name, args.Epochs)
	return


