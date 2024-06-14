import os
import sys
import hashlib
import time
import shutil
module_dir = os.path.abspath('Wikipedia-API')  # Assuming Wikipedia-API is in the same directory
sys.path.insert(0, module_dir)
import wikipediaapi

note_directory = "notes/"
go = True


def hash_string(input_string: str) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode("utf-8"))
    hashed_string = sha256_hash.hexdigest()

    return hashed_string

def get_wikipedia_explanation(topic):
    # Specify a user agent
    user_agent = "MyWikiScraper/1.0 (YourEmailAddress@example.com)"
    wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent)
    
    page = wiki_wiki.page(topic)
    if page.exists():
        return page.summary
    else:
        return "Sorry, the program couldn't find any information on that topic."

while True:
    global auth, b
    auth = False
    b = False
    time.sleep(2)
    log = input("\n\n\nWelcome!\nYou have the following options:\n\n1.register\n2.log in\n3.reset password\n4.QUIT\nPlease enter a number: ")

    if log == "1":
        if not os.path.exists("secure/"):
            dob = input("What is your date of birth? : ")
            ran = input("name one thing that you like (Make sure no one can guess this! REMEMBER THIS WORD! USE ONLY CAPITAL LETTERS) : ")

            os.makedirs("secure/")

            with open("secure/dob.txt", 'w') as file:
                file.write(hash_string(dob))
            with open("secure/ran.txt", 'w') as file:
                file.write(hash_string(ran))
        if not os.path.exists("secure/password"):
            if not os.path.exists("secure/"):
                os.makedirs("secure")
            with open("secure/password", 'w') as file:
                file.write(hash_string(input("Choose your password: ")))
        else: 
            print("ERROR: There is already a password registered")
    elif log == "2":
        if os.path.exists("secure/password"):
            with open("secure/password", 'r') as file:
                password = input("enter your password: ")
                pw = hash_string(password)
                file = file.read()
                if file == pw:
                    auth = True
                else:
                    print("Wrong password!! Not Authenticated")
        else:
            print("There is not yet a password registered.")
    elif log == "3":
        if not os.path.exists("secure/password"):
            print(f"ERROR There is not yet a password registered")
        else:
            dob = input("What is your date of birth? : ")
            ran = input("What was the item that you liked and used for password register? USE CAPITAL LETTERS: ")

            with open("secure/dob.txt", 'r') as file:
                file = file.read()
                if hash_string(dob) == file:
                    with open("secure/ran.txt", 'r') as file:
                        file = file.read()
                        if hash_string(ran) == file:
                            sure = input("Are you sure? (y/N)")
                            if sure == "y":
                                shutil.rmtree("secure/")
                                print("You can now restart the registering process from the login menu")
                            else:
                                print(f"Reset process failed! Try again later")
                        else:
                            print("Error wrong answer process aborted")
                else:
                    print("Error wrong answer process aborted")


    elif log == "4":
        b = True
        break

    if auth == True:
        b = False
        break

while go:
    time.sleep(2)
    print("\n\n\nWelcome to the main menu!! \n")
    menu = input("You have the following options: \n1. create new note\n2. read notes\n3. Search on the wiki\n4. Delete note\n5.QUIT\nPlease enter a number")


    def list_directory_contents(directory):
        if os.path.exists(directory) and os.path.isdir(directory):
            contents = os.listdir(directory)
            print(f"All your notes in '{directory}':")
            for index, content in enumerate(contents):
                content_path = os.path.join(directory, content)
                if os.path.isdir(content_path):
                    print(f"{index}: {content}/ (Folder)")
                else:
                    print(f"{index}: {content} (File)")
            return contents
        else:
            print(f"Folder '{directory}' does not exist. This could be, because you have not yet created any notes")
            return []

    def get_user_choice(contents):
        while True:
            try:
                choice = int(input("The number of the note you want to select: "))
                if 0 <= choice < len(contents):
                    return choice
                else:
                    print("Invalid Entry. Please try again!")
            except ValueError:
                print("Invalid entry please enter a number")
    if b == True:
        print("Error Not authenticated!")
        break
    elif menu == "1":
        name = input("title: ")
        if " " in name:
            name = name.replace(" ", "_")
        with open(note_directory + name, "w") as file:
            file.write(input("Content of your note: "))
            print(f"Note with successfully created!")
    elif menu == "2":
        while True:
            contents = list_directory_contents(note_directory)
            if not contents:
                break
            choice = get_user_choice(contents)
            selected_item = contents[choice]
            selected_path = os.path.join(note_directory, selected_item)

            if os.path.isdir(selected_path):
                print("ganing access to '{selected_path}'")
            else:
                with open(selected_path, 'r') as file:
                    content = file.read()
                    print(f"content of your note '{selected_item}':\n{content}")
                break
    elif menu == "3":
        topic = input("On what topic do you want to do reasearch? : ")
        explanation = get_wikipedia_explanation(topic)
        print("This is the explanation: \n\n\n" + explanation)
        time.sleep(1)
        save = input("Do you want to save this explanation to your notes? (y/N)")
        if " " in topic:
            topic = topic.replace(" ", "_")
        if save == "y":
            with open("notes/" + topic, 'w') as file:
                file.write(explanation)
            print("note was saved!")
        else:
            print("no note was saved!")
        time.sleep(2)
    
    elif menu == "4":
        while True:
            contents = list_directory_contents(note_directory)
            if not contents:
                break
            choice = get_user_choice(contents)
            selected_item = contents[choice]
            selected_path = os.path.join(note_directory, selected_item)

            if os.path.isdir(selected_path):
                print("ganing access to '{selected_path}'")
            else:
                sure = input("Are you sure ? (y/N)")
                if sure == "y":
                    os.remove(selected_path)
                    print("Note deleted successfully")
                else:
                    print("nothing was deleted!")

                break

    elif menu == "5":
        go = False


    


    

