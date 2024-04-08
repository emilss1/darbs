

# from flask import Flask, render_template, request
# import sqlite3
# import requests
# import random

# # Initialize Flask application
# app = Flask(__name__)

# # Define routes
# @app.route('/')
# def index(): 
#     return render_template('training_session.html')

# @app.route('/train', methods=['POST'])
# def train():
#     muscles_input = request.form.get('muscles')
#     muscles = [muscle.strip() for muscle in muscles_input.split(',')]
#     exercise_type = str(request.form.get('type'))
#     difficulty_input = request.form.get('difficulty')
#     difficulty_map = {'easy': 'beginner', 'medium': 'intermediate', 'hard': 'expert'}
#     difficulty = str(difficulty_map[difficulty_input.lower()])

#     num_exercises = int(request.form.get('num_exercises'))
    
#     # Print selected options
    
#     print("Selected muscles:", muscles)
#     print("Selected difficulty:", difficulty)
#     print("Number of exercises:", num_exercises)
#     print("Exercise type:", exercise_type)

#     exercises = get_exercises_from_api(muscles, difficulty, num_exercises,exercise_type)
#     print("Selected exercises:", exercises)

#     return render_template('training_session.html', exercises=exercises, len = num_exercises)
    

# # Helper function to get exercises from API
# def get_exercises_from_api(muscles, difficulty, num_exercises,exercise_type):
#     print('Fetching...')
#     all_exercises = []
#     for muscle in muscles:
#         api_url = 'https://api.api-ninjas.com/v1/exercises?muscle={}&difficulty={}&type={}'.format(muscle, difficulty,exercise_type)
#         print(api_url)
#         response = requests.get(api_url, headers={'X-Api-Key': 'F9mFjxwjJcqEgOUD5Fv/kw==TKCJh4qV7KJuil9I'})

#         if response.status_code == requests.codes.ok:
#             api_data = response.json()
#             # Select exercises from the API response
#             selected_exercises = api_data[:num_exercises]
#             all_exercises.extend(selected_exercises)
#             # data = api_data[0]
#             print('hello')
          
#     return all_exercises

# # Run the Flask application
# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request
import sqlite3
import requests
import random

# Initialize Flask application
app = Flask(__name__)

# Define routes
@app.route('/')
def index(): 
    return render_template('training_session.html')

@app.route('/train', methods=['POST'])
def train():
    muscles_input = request.form.get('muscles')
    muscles = [muscle.strip() for muscle in muscles_input.split(',')]
    exercise_type = str(request.form.get('type'))
    difficulty_input = request.form.get('difficulty')
    difficulty_map = {'easy': 'beginner', 'medium': 'intermediate', 'hard': 'expert'}
    difficulty = str(difficulty_map[difficulty_input.lower()])

    num_exercises = int(request.form.get('num_exercises'))
    
    # Print selected options
    print("Selected muscles:", muscles)
    print("Selected difficulty:", difficulty)
    print("Number of exercises:", num_exercises)
    print("Exercise type:", exercise_type)

    exercises = get_exercises_from_api(muscles, difficulty, num_exercises, exercise_type)
    print("Selected exercises:", exercises)

    # Check if exercises list is empty
    if not exercises:
        error_message = f"No exercises found for muscles: {', '.join(muscles)}, difficulty: {difficulty}, and exercise type: {exercise_type}. Please try again."
        return render_template('training_session.html', error_message=error_message)
    else:
        return render_template('training_session.html', exercises=exercises, len=num_exercises)

# Helper function to get exercises from API
def get_exercises_from_api(muscles, difficulty, num_exercises, exercise_type):
    print('Fetching...')
    all_exercises = []
    for muscle in muscles:
        api_url = 'https://api.api-ninjas.com/v1/exercises?muscle={}&difficulty={}&type={}'.format(muscle, difficulty, exercise_type)
        print(api_url)
        response = requests.get(api_url, headers={'X-Api-Key': 'F9mFjxwjJcqEgOUD5Fv/kw==TKCJh4qV7KJuil9I'})

        if response.status_code == requests.codes.ok:
            api_data = response.json()
            # Select exercises from the API response
            selected_exercises = api_data[:num_exercises]
            all_exercises.extend(selected_exercises)
            # data = api_data[0]
            print('hello')
          
    return all_exercises

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
