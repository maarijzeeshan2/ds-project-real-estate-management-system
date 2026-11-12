# Real Estate Management System

## Overview
This project is a Python-based real estate management system. It allows storing, searching, updating, deleting, and displaying property records.

## Features
-	Managing property records containing property ID, type, location, price, rent, and status.
-	Inserting new property records.
-	Searching for property records using property ID.
-	Displaying all properties in sequential order.
-	Updating property status as sold or rented.
-	Deleting property records when required.
-	Undoing the most recent user action.
-	Automatically saving data to a file when user exits and loading it when the program starts.

## Concepts Used
- Object Oriented Programming
- Data Structures including Linked Lists, Stack and Queues
  - A singly linked list was used as the main data structure to store property records.
  - A stack was used to implement the undo feature.
  - Two queues were used to maintain the order of sold and rented properties.
- File handling was implemented through python's pickle module.
- Menu driven interface

## Code Quality
- Used Pylint to check code quality.
- Improved code structure and readability.
- Improved exception handling.

## Technologies Used
- Python
- VS Code
- GitHub
- Pickle
- Pylint

## How to Run
1. Download or copy the repository.
2. Open the project folder in VS Code.
3. Run the main python file.
