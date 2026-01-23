import pickle
from collections import deque

# NODE CLASS (Linked List)
class PropertyNode:
    def __init__(self, propertyID, property_type, property_location, price, rent):
        self.id = propertyID
        self.type = property_type
        self.location = property_location
        self.price = price
        self.rent = rent
        self.sold = False
        self.rented = False
        self.next = None  # Pointer to next node

# GLOBAL DATA STRUCTURES
head = None                   # Head of linked list
undo_stack = []               # Stack for undo (last action)
rented_queue = deque()        # Queue for recently rented
sold_queue = deque()          # Queue for recently sold

# FIND PROPERTY FOR INNER WORKING
def find_property(propertyID):
    current = head
    while current:
        if current.id == propertyID:
            return current
        current = current.next
    return None

# ADD PROPERTY (insert)
def add_property():
    global head

    propertyID = input("Enter Property ID: ")

    # If property already exists
    if find_property(propertyID):                   
        print("Property ID already exists.\n")
        return
    
    # If property does not already exists
    property_type = input("Enter Property Type: ")
    property_location = input("Enter Location: ")

    try:
        price = float(input("Enter Price: "))
        rent = float(input("Enter Rent (if want to rent): "))
    except ValueError:
        print("Invalid input! Price and Rent must be numbers.\n")
        return
    
    # Creating a node
    new_node = PropertyNode(propertyID, property_type, property_location, price, rent)

    if head is None:
        head = new_node
    else:
        current = head
        while current.next:
            current = current.next
        current.next = new_node

    # Appending action into undo stack
    undo_stack.append(("add", propertyID))
    print("Property added successfully.\n")

# VIEW ALL PROPERTIES
def view_properties():

    # If no properties exist
    if head is None:
        print("No properties available.\n")
        return
    
    # If one or more properties exist
    current = head
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
    property_ID = input("Enter Property ID to mark as SOLD: ")
    property = find_property(property_ID)

    # If property is not found
    if property is None:
        print("Property not found.\n")
        return

    # If property is already sold
    if property.sold:
        print("Already sold.\n")
        return
    
    # If property is already rented
    if property.rented:
        print("Property is rented. Cannot mark as sold.\n")
        return

    # If property is found and not sold or rented
    property.sold = True
    sold_queue.append(property)
    undo_stack.append(("sold", property_ID))
    print("Marked as SOLD.\n")

# MARK PROPERTY AS RENTED
def mark_as_rented():
    propertyID = input("Enter Property ID to mark as RENTED: ")
    property = find_property(propertyID)

    # If property is not found
    if property is None:
        print("Property not found.\n")
        return

    # If property is already rented
    if property.rented:
        print("Already rented.\n")
        return
    
    # If property is already sold
    if property.sold:
        print("Property is sold. Cannot rent.\n")
        return

    # If property is found and not sold or rented
    property.rented = True
    rented_queue.append(property)
    undo_stack.append(("rented", propertyID))
    print("Marked as RENTED.\n")

# REMOVE PROPERTY (delete)
def remove_property():
    global head

    propertyID = input("Enter Property ID to remove: ")

    # If there are no properties to be removed
    if head is None:
        print("No properties available.\n")
        return

    # If first node is the one to remove
    if head.id == propertyID:
        undo_stack.append(("remove", head))
        head = head.next
        print("Property removed.\n")
        return

    # Remove from middle or end
    prev = head
    current = head.next

    while current:
        if current.id == propertyID:
            undo_stack.append(("remove", current))
            prev.next = current.next
            print("Property removed.\n")
            return
        prev = current
        current = current.next

    print("Property not found.\n")

# SEARCH PROPERTY FOR USER
def search_property():
    propertyID = input("Enter Property ID to search: ")
    property = find_property(propertyID)

    # If property is not found
    if property is None:
        print("Property not found.\n")
        return

    # If property is found
    print("\n--- Property Found ---")
    print(f"ID: {property.id}")
    print(f"Type: {property.type}")
    print(f"Location: {property.location}")
    print(f"Price: {property.price}")
    print(f"Rent: {property.rent}")
    print("Status:",
          "SOLD" if property.sold else "NOT SOLD",
          "|",
          "RENTED" if property.rented else "NOT RENTED")
    print()

# UNDO FUNCTION
def undo():
    global head

    # If no action was performed
    if not undo_stack:
        print("Nothing to undo.\n")
        return

    action, data = undo_stack.pop()

    # If last action was adding property
    if action == "add":
        propertyID = data
        previous = None
        current = head

        while current:
            if current.id == propertyID:
                if previous is None:
                    head = current.next
                else:
                    previous.next = current.next
                print("Undo successful: Added property removed.\n")
                return
            previous = current
            current = current.next

    # If last action was deleting property
    elif action == "remove":
        node = data
        node.next = head
        head = node
        print("Undo successful: Removed property restored.\n")

    # If last action was marking property as sold
    elif action == "sold":
        property = find_property(data)
        if property:
            property.sold = False
            print("Undo successful: Property marked as NOT sold.\n")

    # If last action was marking as rented
    elif action == "rented":
        property = find_property(data)
        if property:
            property.rented = False
            print("Undo successful: Property marked as NOT rented.\n")

# SAVE DATA TO FILE USING PICKLE
def save_to_file():
    with open("properties.pkl", "wb") as f:
        pickle.dump(head, f)
    print("Data saved successfully.\n")

# LOAD DATA FROM FILE USING PICKLE
def load_from_file():
    global head
    try:
        with open("properties.pkl", "rb") as f:
            head = pickle.load(f)

    # If file not found, start empty 
    except:
        head = None   

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

        choice = input("Enter choice: ")

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