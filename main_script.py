
import sqlite3
import requests
import random

def get_user_input():
    # Get muscles input
    muscles_input = input("Enter the muscles you want to train (separated by commas): ")
    muscles = [muscle.strip() for muscle in muscles_input.split(',')]
    
    # Get training level input
    difficulty_input = input("Enter the training level (easy, medium, hard): ")
    difficulty_map = {'easy': 'beginner', 'medium': 'intermediate', 'hard': 'expert'}
    difficulty = difficulty_map.get(difficulty_input.lower())

    # Get number of exercises input
    num_exercises = int(input("Enter the number of exercises you want to do: "))

    return muscles, difficulty, num_exercises

def perform_training_session(exercises):
    print("\nTraining Session:")
    for exercise in exercises:
        print(f"\nExercise: {exercise['name']}")
        print(f"Description: {exercise['instructions']}")
        input("Press Enter to continue to the next exercise...")

def main():
    muscles, difficulty, num_exercises = get_user_input()

    for muscle in muscles:
        api_url = 'https://api.api-ninjas.com/v1/exercises?muscle={}&difficulty={}'.format(muscle, difficulty)
        response = requests.get(api_url, headers={'X-Api-Key': 'F9mFjxwjJcqEgOUD5Fv/kw==TKCJh4qV7KJuil9I'})

        if response.status_code == requests.codes.ok:
            api_data = response.json()  # Parse the JSON response
            # print(api_data)

            # Check if there are enough exercises in the selected difficulty level
            if len(api_data) < num_exercises:
                print(f"Not enough exercises available for {muscle} in the {difficulty} difficulty level.")
                continue

            # Shuffle the exercises to randomize the training session
            random.shuffle(api_data)

            # Select the first 'num_exercises' for the training session
            selected_exercises = api_data[:num_exercises]

            # Connect to the SQLite database
            conn = sqlite3.connect('exercises_database.db')
            cursor = conn.cursor()

            # Create a table to store exercise data with additional fields
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS exercises (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    description TEXT,
                    difficulty TEXT,
                    exercise_type TEXT,
                    exercise_equipment TEXT,
                    muscle TEXT
                )
            ''')

            # Assuming the API response is a list of exercises
            for exercise in selected_exercises:
                exercise_name = exercise.get('name')

                # Check if the exercise already exists in the database
                cursor.execute('SELECT * FROM exercises WHERE name=? AND muscle=?', (exercise_name, muscle))
                existing_exercise = cursor.fetchone()

                if existing_exercise is None:
                    # If the exercise doesn't exist, insert it into the database
                    exercise_description = exercise.get('description', 'No description available.')
                    exercise_difficulty = exercise.get('difficulty', '')
                    exercise_type = exercise.get('type', '')
                    exercise_equipment = exercise.get('equipment', '')

                    # Insert exercise data into the database
                    cursor.execute('''
                        INSERT INTO exercises (name, description, difficulty, exercise_type, exercise_equipment, muscle)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (exercise_name, exercise_description, exercise_difficulty, exercise_type, exercise_equipment, muscle))

                    # Print information about the exercise
                    print(f"Muscle: {muscle}")
                    print(f"Exercise: {exercise_name}")
                    print(f"Description: {exercise_description}")
                    print(f"Difficulty: {exercise_difficulty}")
                    print(f"Type: {exercise_type}")
                    print(f"Equipment: {exercise_equipment}")
                    print("---")

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            # Perform the training session
            perform_training_session(selected_exercises)

        else:
            print("Error:", response.status_code, response.text)

if __name__ == "__main__":
    main()


