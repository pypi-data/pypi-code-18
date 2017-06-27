import random
def main():
	x="yes"
	while x!="no":
		print("(')")
		y=input("What color do you think this apple is: Red, Yellow, or Green?")
		z=random.choice(["Red", "Yellow", "Green"])
		if(y==z):
			x=input("Good Guess, want to play again? (yes/no)")
		else:
			print("Sorry, it was "+z+ " better luck next time!")
			x=input("Would you like to play again? (yes/no)")



main()
