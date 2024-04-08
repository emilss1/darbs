import os
import sqlite3

def get_database_path():
    # Get the absolute path to the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(script_dir, 'exercises_database.db')
    return database_path

def create_database():
    # Connect to the SQLite database
    conn = sqlite3.connect(get_database_path())
    cursor = conn.cursor()

    # Create a table to store exercise data with additional fields
    cursor.execute('''CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            difficulty TEXT,
            exercise_type TEXT,
            exercise_equipment TEXT,
            muscle TEXT
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def insert_exercise(exercise_data):
    # Connect to the SQLite database
    conn = sqlite3.connect(get_database_path())
    cursor = conn.cursor()

    # Insert exercise data into the database
    cursor.execute('''INSERT INTO exercises (name, description, difficulty, exercise_type, exercise_equipment, muscle)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', exercise_data)

def get_exercises(muscle, difficulty, count):
    conn = sqlite3.connect('exercises_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM exercises WHERE muscle=? AND difficulty=? LIMIT ?', (muscle, difficulty, count))
    result = cursor.fetchall()
    conn.close()
    return result

def main():
    # Get user input for muscle, difficulty, and count
    muscle_input = input("Enter the muscle group you want to train (e.g., triceps): ").lower()
    difficulty_input = input("Enter the difficulty level you want (easy, medium, hard - these are only olympic weightlifting exercises ): ").lower()
    count_input = int(input("Enter the number of exercises you want to retrieve: "))
    if difficulty_input == "easy":
        difficulty_input = "beginer"
    elif difficulty_input == "medium":
        difficulty_input = "intermediate"
    else:
        difficulty_input = "expert"
    # Call the get_exercises function with user-provided values
    exercises = get_exercises(muscle_input, difficulty_input, count_input)

    # Display the retrieved exercises
    if exercises:
        print("Retrieved Exercises:")
        for exercise in exercises:
            print(f"Exercise: {exercise[0]}")
            print(f"Description: {exercise[1]}")
            print(f"Difficulty: {exercise[2]}")
            print(f"Type: {exercise[3]}")
            print(f"Equipment: {exercise[4]}")
            print(f"Muscle: {exercise[5]}")
            print("---")    
    else:
        print("No exercises found, or not enough exercises in data base.")

if __name__ == "__main__":

    # Commit the changes and close the connection
    main()

