import json
import re
import datetime

# File to store users and projects data for future retrieval 
db_file = "crowdfunding_db.json"

################## Load existing data from the JSON file ##################
try:
    with open(db_file, "r") as file:
        data = json.load(file)
except FileNotFoundError:
    data = {"users": [], "projects": []}


################## Save New Data in the JSON file ##################
def save_data():
    with open(db_file, "w") as file:
        json.dump(data, file, indent=4)


################## Phone number validation ##################
def validate_egyptian_phone(phone):
    return re.fullmatch(r"^(\+20|0)?1[0-9]{9}$", phone)


################## User Registeration ##################
def register():
    print("\n\nRegister")
    print("-----------")
    first_name = input("First Name : ")
    last_name = input("Last Name : ")
    email = input("Email : ")
    password = input("Password : ")
    confirm_password = input("Confirm Password : ")
    phone = input("Mobile Phone : ")
    
    if password != confirm_password:
        print("\nPasswords do not match!")
        return
    if not validate_egyptian_phone(phone):
        print("\nInvalid Egyptian phone number!")
        return
    
    data["users"].append({"first_name": first_name, "last_name": last_name, "email": email, "password": password, "phone": phone})
    save_data()
    print("\nRegistration successful!")


################## User Login ##################
def login():
    print("\n\nLogin")
    print("------")
    email = input("Email : ")
    password = input("Password : ")
    
    for user in data["users"]:
        if user["email"] == email and user["password"] == password:
            print("\nLogin successful!")
            return email
    print("\nInvalid credentials!")
    return None


################## Create New Project ##################
def create_project(user_email):
    print("\n\nCreate Project")
    print("------------------")
    title = input("Title : ")
    details = input("Details : ")
    target = input("Total Target Amount : ")
    start_date = input("Start Date (YYYY-MM-DD) : ")
    end_date = input("End Date (YYYY-MM-DD) : ")
    
    try:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        if start_date >= end_date:
            print("\nInvalid date range!")
            return
    except ValueError:
        print("\nInvalid date format!")
        return
    
    data["projects"].append({"title": title, "details": details, "target": target, "start_date": start_date.strftime("%Y-%m-%d"), "end_date": end_date.strftime("%Y-%m-%d"), "owner": user_email})
    save_data()
    print("\nProject created successfully!")


################## View All Current Projects ##################
def view_projects():
    print("\n\nAll Projects")
    print("-------------")
    if len(data["projects"]) == 0 :
        print("\nYou don't have any added projects yet.")
    for project in data["projects"]:
        print(f"- Title : {project['title']}, Target : {project['target']} EGP, Start : {project['start_date']}, End : {project['end_date']}")


################## Edit a specific Project ##################
def edit_project(user_email):
    print("\nEdit Project")
    print("-------------")
    title = input("Enter the project title to edit : ")
    
    for project in data["projects"]:
        if project["title"] == title and project["owner"] == user_email:
            project["details"] = input("New Details : ")
            save_data()
            print("\nProject updated!")
            return
    print("\nProject not found or not owned by you!")


################## Delete a specific  Project ##################
def delete_project(user_email):
    print("\nDelete Project")
    print("-------------")
    title = input("Enter the project title to delete : ")
    
    for project in data["projects"]:
        if project["title"] == title and project["owner"] == user_email:
            data["projects"].remove(project)
            save_data()
            print("\nProject deleted!")
            return
    print("\nProject not found or not owned by you!")


################## Find a specific Project ##################
def search_project():
    print("\nSearch Projects by Date")
    print("-------------------------")
    date = input("Enter date (YYYY-MM-DD) : ")
    
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        results = [p for p in data["projects"] if p["start_date"] <= date <= p["end_date"]]
        if len(results) == 0 :
            print("\nThere is no project found for this date.")
        for p in results:
            print(f"Title : {p['title']}, Target : {p['target']} EGP")
    except ValueError:
        print("\nInvalid date format!")



# Main Function
def main():
    while True:
        print("\nCrowdfunding Console App Start Menu")
        print("------------------------------------")
        print("\n1. Register.")
        print("2. Login.")
        print("3. Exit.")
        choice = input("\nEnter choice : ")
        
        if choice == "1":
            register()
        elif choice == "2":
            user_email = login()
            if user_email:
                print(f"\nWelcome, {user_email} !")
                while True:
                    print("\n\n#################################################")
                    print("\n\nChoose what do you want to do from this menu")
                    print("----------------------------------------------")
                    print("\n1. Create Project.")
                    print("2. View Projects.")
                    print("3. Edit My Project.")
                    print("4. Delete My Project.")
                    print("5. Search Project by Date.")
                    print("6. Logout.")
                    sub_choice = input("\nEnter choice : ")
                    
                    if sub_choice == "1":
                        create_project(user_email)
                    elif sub_choice == "2":
                        view_projects()
                    elif sub_choice == "3":
                        edit_project(user_email)
                    elif sub_choice == "4":
                        delete_project(user_email)
                    elif sub_choice == "5":
                        search_project()
                    elif sub_choice == "6":
                        print("\nLogging out...")
                        break
                    else:
                        print("\nInvalid choice!")
        elif choice == "3":
            print("\nExiting the program...")
            break
        else:
            print("\nInvalid choice!")


# Start/Run the app
if __name__ == "__main__":
    main()
