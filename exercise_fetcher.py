# import os
# import sqlite3
# import requests
# import random

# # Function to get the database path
# def get_database_path():
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     database_path = os.path.join(script_dir, 'exercises_database.db')
#     return database_path

# # Function to connect to the SQLite database
# def connect_to_database():
#     return sqlite3.connect(get_database_path())

# # Function to get exercises from the database
# def get_exercises_from_database(muscle, difficulty, num_exercises, exercise_type):
#     conn = connect_to_database()
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM exercises WHERE muscle=? AND difficulty=? LIMIT ? AND exercise_type=?', (muscle, difficulty, num_exercises, exercise_type))
#     result = cursor.fetchall()
#     conn.close()
#     return result

# # Function to get exercises from the API or database
# def get_exercises(muscles, difficulty, num_exercises, type):
#     # Try getting exercises from the API
#     try:
#         all_exercises = []
#         for muscle in muscles:
#             print(muscle, difficulty,type)
#             api_url = 'https://api.api-ninjas.com/v1/exercises?muscle={}&difficulty={}&type={}'.format(muscle, difficulty, type)
#             response = requests.get(api_url, headers={'X-Api-Key': 'F9mFjxwjJcqEgOUD5Fv/kw==TKCJh4qV7KJuil9I'})
#             print(response.json())
#             print(api_url)

#             if response.status_code == requests.codes.ok:
#                 api_data = response.json()
#                 if len(api_data) >= num_exercises:
#                     # selected_exercises = random.sample(api_data, num_exercises)
#                     all_exercises.extend(api_data)
#         return all_exercises
#     except Exception as e:
#         print(f"Error fetching data from API: {e}")
#         print("Fetching exercises from the database instead.")
#         # If API request fails, get exercises from the database
#         return get_exercises_from_database(muscles[0], difficulty, num_exercises, type)

# def get_user_input():
#     # Get muscles input
#     muscles_input = input("Enter the muscles you want to train, Possible values are: abdominals, abductors, adductors, biceps, calves, chest, forearms, glutes, hamstrings, lats, lower_back, middle_back, neck, quadriceps, traps, triceps (separated by commas): ")
#     muscles = [muscle.strip() for muscle in muscles_input.split(',')]
#     type = input('get exercise type')
#     # Get training level input
#     difficulty_input = input("Enter the training level (easy, medium, hard): ")
#     difficulty_map = {'easy': 'medium', 'hard': 'intermediate', 'hard': 'expert'}
#     difficulty = difficulty_map.get(difficulty_input.lower())

#     # Get number of exercises input
#     num_exercises = int(input("Enter the number of exercises you want to do: "))

#     return muscles, difficulty, num_exercises, type


# # Example usage
# def main():
    


#     muscles, difficulty, num_exercises, type = get_user_input()

#     # Call the get_exercises function
#     exercises = get_exercises(muscles, difficulty, num_exercises, type)
#     print(exercises[0])
#     print(exercises)
#     # Display the retrieved exercises
#     if exercises:
#         print("Retrieved Exercises:")
#         for exercise in exercises:
#             print(f"Exercise: {exercise['name']}")
#             print(f"Description: {exercise['instructions']}")
#             # print(f"Difficulty: {exercise.get('difficulty')}")
#             # print(f"Type: {exercise.get('type')}")
#             # print(f"Equipment: {exercise.get('equipment')}")
#             # print(f"Muscle: {exercise.get('muscle')}")
#             print("---")
#     else:
#         print("No exercises found, or unable to fetch exercises.")

# if __name__ == "__main__":
#     main()





import os
import sqlite3
import requests
import random

# Function to get the database path
def get_database_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(script_dir, 'exercises_database.db')
    return database_path

# Function to connect to the SQLite database
def connect_to_database():
    return sqlite3.connect(get_database_path())

# Function to get exercises from the database
def get_exercises_from_database(muscle, difficulty, num_exercises, exercise_type):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM exercises WHERE muscle=? AND difficulty=? AND exercise_type=? LIMIT ?', (muscle, difficulty, exercise_type, num_exercises))
    result = cursor.fetchall()
    conn.close()
    return result

# Function to get exercises from the API or database
def get_exercises(muscles, difficulty, num_exercises, exercise_type):
    # Try getting exercises from the API
    try:
        all_exercises = []
        for muscle in muscles:
            api_url = 'https://api.api-ninjas.com/v1/exercises?muscle={}&difficulty={}&type={}'.format(muscle, difficulty, exercise_type)
            response = requests.get(api_url, headers={'X-Api-Key': 'F9mFjxwjJcqEgOUD5Fv/kw==TKCJh4qV7KJuil9I'})

            if response.status_code == requests.codes.ok:
                api_data = response.json()
                if len(api_data) >= num_exercises:
                    all_exercises.extend(api_data)
        return all_exercises
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        print("Fetching exercises from the database instead.")
        # If API request fails, get exercises from the database
        return get_exercises_from_database(muscles[0], difficulty, num_exercises, exercise_type)

def get_user_input():
    # Get muscles input
    muscles_input = input("Enter the muscles you want to train, Possible values are: abdominals, abductors, adductors, biceps, calves, chest, forearms, glutes, hamstrings, lats, lower_back, middle_back, neck, quadriceps, traps, triceps (separated by commas): ")
    muscles = [muscle.strip() for muscle in muscles_input.split(',')]

    # Get training level input
    difficulty_input = input("Enter the training level (easy, medium, hard): ")
    difficulty_map = {'easy': 'beginner', 'medium': 'intermediate', 'hard': 'expert'}
    difficulty = difficulty_map.get(difficulty_input.lower())

    # Get number of exercises input
    num_exercises = int(input("Enter the number of exercises you want to do: "))

    # Get exercise type input
    exercise_type = input("Enter the exercise type (e.g., strength, endurance): ")

    return muscles, difficulty, num_exercises, exercise_type

# Example usage
def main():
    muscles, difficulty, num_exercises, exercise_type = get_user_input()

    # Call the get_exercises function
    exercises = get_exercises(muscles, difficulty, num_exercises, exercise_type)

    # Display the retrieved exercises
    if exercises:
        print("Retrieved Exercises:")
        for exercise in exercises:
            print(f"Exercise: {exercise.get('name')}")
            print(f"Description: {exercise.get('instructions')}")
            print(f"Difficulty: {exercise.get('difficulty')}")
            print(f"Type: {exercise.get('type')}")
            print(f"Equipment: {exercise.get('equipment')}")
            print(f"Muscle: {exercise.get('muscle')}")
            print("---")
    else:
        print("No exercises found, or unable to fetch exercises.")

if __name__ == "__main__":
    main()