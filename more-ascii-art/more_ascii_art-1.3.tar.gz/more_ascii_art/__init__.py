# Importing assets
import cat
import chicken
import mouse
import elephant

# Error handling variable
err = print("Something went wrong. Report a bug at https://github.com/PenetratingShot/Python-ASCII-Art/issues")

# Help section
def help():
    print("     Welcome to more-ascii-art help!      ")
    print("Usage: (local) ")
    print("       1. Build the library with >>> pip install -e .")
    print("       2. Use the python shell to >>> import more-ascii-art")
    print("       3. Type in print and then the build name and then the function you wish to execute")
    print("            Like this: >>> print more-ascii-art.help()")
    print("Usage: (pip package) ")
    print("       1. Install more-ascii-art with >>> pip install more-ascii-art ")
    print("       2. Type in 'print' and then the function you wish to execute... ")
    print("            Like this: >>> print more-ascii-art.help()
    print("Commands: ")
    print("       1. help() - Displays this help message")
    print("       2. selection() - Displays all ASCII selections and prompts you for which one you want")
    print("            a. cat     ")
    print("            b. chicken ")
    print("            c. mouse ")
    print("            d. elephant ")
    print("       3. changelog() - Displays what has been changed in each version of more-ascii-art ")

# Changelog for different versions
def changelog():
    print("v1.3: ")
    print("  - elephant picture")
    print("  - updated help section ")
    print("  - changelog() command ")
    print("  - updated selection() ")
    print("  - updated user input ")

# User selection and processing    
def selection():
    print("Please note that selections are case sensitive...")
    print("Here are the selections you can choose from (for now): ")
    print("1. cat ")
    print("2. chicken ")
    print("3. mouse ")
    print("4. elephant ")
    
    # Taking real time input from user
    user_input = input("Please type in your selection: ")
    
    # Processing statements
    if (user_input == "cat"):
        return cat()
    else:
        print (err)
        
    if (user_input == "chicken"):
        return chicken()
    else:
        print (err)
        
    if (user_input == "mouse"):
        return mouse()
    else:
        print (err)
    if (user_input == "elephant"):
        return elephant()
    else:
        print (err)
