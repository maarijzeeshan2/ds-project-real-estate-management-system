"""Real Estate Management System"""

import pickle
from collections import deque

# NODE CLASS (Linked List)
class PropertyNode:
    def __init__(self, property_id, property_type, property_location, price, rent):
        self.id = property_id
        self.type = property_type
        self.location = property_location
        self.price = price
        self.rent = rent
        self.sold = False
        self.rented = False
        self.next = None  # Pointer to next node

# GLOBAL DATA STRUCTURES
HEAD = None                   # Head of linked list
undo_stack = []               # Stack for undo (last action)
rented_queue = deque()        # Queue for recently rented
sold_queue = deque()          # Queue for recently sold

# FIND PROPERTY FOR INNER WORKING
def find_property(property_id):
    current = HEAD
    while current:
        if current.id == property_id:
            return current
        current = current.next
    return None

# ADD PROPERTY (insert)
def add_property():
    global HEAD

    property_id = input("Enter Property ID: ").strip()

    # If no input is entered
    if property_id == "":
        print("Invalid input! ID cannot be empty.")
        return 
    
    # If property_data already exists
    if find_property(property_id):                 
        print("Property ID already exists.\n")
        return
       
    # If property_data does not already exists
    property_type = input("Enter Property Type: ").strip()

    # If no input is entered
    if property_type == "":
        print("Invalid input! Property type cannot be empty.")
        return
    
    property_location = input("Enter Location: ").strip()

    # If no input is entered
    if property_location == "":
        print("Invalid input! Property location cannot be empty.")
        return 
    
    try:
        price = float(input("Enter Price: "))
        rent = float(input("Enter Rent (if want to rent): "))
    except ValueError:
        print("Invalid input! Price and Rent must be numbers.\n")
        return
        
    # Creating a node
    new_node = PropertyNode(property_id, property_type, property_location, price, rent)

    if HEAD is None:
        HEAD = new_node
    else:
        current = HEAD
        while current.next:
            current = current.next
        current.next = new_node

    # Appending action into undo stack
    undo_stack.append(("add", property_id))
    print("Property added successfully.\n")

# VIEW ALL PROPERTIES
def view_properties():

    # If no properties exist
    if HEAD is None:
        print("No properties available.\n")
        return
    
    # If one or more properties exist
    current = HEAD
    print("\n--- All Properties ---")
    while current:
        print(f"ID: {current.id}")
        print(f"Type: {current.type}")
        print(f"Location: {current.location}")
        print(f"Price: {current.price}")
        print(f"Rent: {current.rent}")
        print("Status:",
              "SOLD" if current.sold else "NOT SOLD",
              "|",
              "RENTED" if current.rented else "NOT RENTED")
        print("-----------------------------")
        current = current.next
    print()

# MARK PROPERTY AS SOLD
def mark_as_sold():
    property_id = input("Enter Property ID to mark as SOLD: ")
    property_data = find_property(property_id)

    # If property_data is not found
    if property_data is None:
        print("Property not found.\n")
        return

    # If property_data is already sold
    if property_data.sold:
        print("Already sold.\n")
        return
    
    # If property_data is already rented
    if property_data.rented:
        print("Property is rented. Cannot mark as sold.\n")
        return

    # If property_data is found and not sold or rented
    property_data.sold = True
    sold_queue.append(property_data)
    undo_stack.append(("sold", property_id))
    print("Marked as SOLD.\n")

# MARK PROPERTY AS RENTED
def mark_as_rented():
    property_id = input("Enter Property ID to mark as RENTED: ")
    property_data = find_property(property_id)

    # If property_data is not found
    if property_data is None:
        print("Property not found.\n")
        return

    # If property_data is already rented
    if property_data.rented:
        print("Already rented.\n")
        return
    
    # If property_data is already sold
    if property_data.sold:
        print("Property is sold. Cannot rent.\n")
        return

    # If property_data is found and not sold or rented
    property_data.rented = True
    rented_queue.append(property_data)
    undo_stack.append(("rented", property_id))
    print("Marked as RENTED.\n")

# REMOVE PROPERTY (delete)
def remove_property():
    global HEAD

    property_id = input("Enter Property ID to remove: ")

    # If there are no properties to be removed
    if HEAD is None:
        print("No properties available.\n")
        return

    # If first node is the one to remove
    if HEAD.id == property_id:
        undo_stack.append(("remove", HEAD))
        HEAD = HEAD.next
        print("Property removed.\n")
        return

    # Remove from middle or end
    prev = HEAD
    current = HEAD.next

    while current:
        if current.id == property_id:
            undo_stack.append(("remove", current))
            prev.next = current.next
            print("Property removed.\n")
            return
        prev = current
        current = current.next

    print("Property not found.\n")

# SEARCH PROPERTY FOR USER
def search_property():
    property_id = input("Enter Property ID to search: ")
    property_data = find_property(property_id)

    # If property_data is not found
    if property_data is None:
        print("Property not found.\n")
        return

    # If property_data is found
    print("\n--- Property Found ---")
    print(f"ID: {property_data.id}")
    print(f"Type: {property_data.type}")
    print(f"Location: {property_data.location}")
    print(f"Price: {property_data.price}")
    print(f"Rent: {property_data.rent}")
    print("Status:",
          "SOLD" if property_data.sold else "NOT SOLD",
          "|",
          "RENTED" if property_data.rented else "NOT RENTED")
    print()

# UNDO FUNCTION
def undo():
    global HEAD

    # If no action was performed
    if not undo_stack:
        print("Nothing to undo.\n")
        return

    action, data = undo_stack.pop()

    # If last action was adding property_data
    if action == "add":
        property_id = data
        previous = None
        current = HEAD

        while current:
            if current.id == property_id:
                if previous is None:
                    HEAD = current.next
                else:
                    previous.next = current.next
                print("Undo successful: Added property_data removed.\n")
                return
            previous = current
            current = current.next

    # If last action was deleting property_data
    elif action == "remove":
        node = data
        node.next = HEAD
        HEAD = node
        print("Undo successful: Removed property_data restored.\n")

    # If last action was marking property_data as sold
    elif action == "sold":
        property_data = find_property(data)
        if property_data:
            property_data.sold = False
            print("Undo successful: Property marked as NOT sold.\n")

    # If last action was marking as rented
    elif action == "rented":
        property_data = find_property(data)
        if property_data:
            property_data.rented = False
            print("Undo successful: Property marked as NOT rented.\n")

# SAVE DATA TO FILE USING PICKLE
def save_to_file():
    with open("properties.pkl", "wb") as f:
        pickle.dump(HEAD, f)
    print("Data saved successfully.\n")

# LOAD DATA FROM FILE USING PICKLE
def load_from_file():
    global HEAD
    try:
        with open("properties.pkl", "rb") as f:
            HEAD = pickle.load(f)

    # If file not found, start empty
    except FileNotFoundError:
        HEAD = None
        
    # If file cannot be opened or read or saved data is corrupted or invalid
    except (OSError, pickle.UnpicklingError) as e:
        print("Error loading property data: " ,e)
        HEAD = None

# MENU
def menu():
    while True:
        print("\n +++++ Real Estate Management System +++++ \n")
        print("Welcome! \n")
        print("1. Add Property")
        print("2. View All Properties")
        print("3. Search Property")
        print("4. Mark Property as Sold")
        print("5. Mark Property as Rented")
        print("6. Remove Property")
        print("7. Undo Last Action")
        print("8. Exit and Save \n")

        choice = input("Enter choice (1 to 8): ")

        if choice == "1":
            add_property()
        elif choice == "2":
            view_properties()
        elif choice == "3":
            search_property()
        elif choice == "4":
            mark_as_sold()
        elif choice == "5":
            mark_as_rented()
        elif choice == "6":
            remove_property()
        elif choice == "7":
            undo()
        elif choice == "8":
            save_to_file()
            print("Goodbye!")
            break
        else:
            print("Invalid choice.\n")

# MAIN PROGRAM
if __name__ == "__main__":
    load_from_file()
    menu()
