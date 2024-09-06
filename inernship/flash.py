

from flask import Flask, request, jsonify
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)

# Load the adventure data from the CSV file
adventure_data = pd.read_csv('adventure_data.csv')

# Create a scaler to scale the data
scaler = StandardScaler()

# Scale the data
scaled_data = scaler.fit_transform(adventure_data[['price', 'difficulty_type']])

# Create a nearest neighbors model
nn = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')

# Fit the model to the scaled data
nn.fit(scaled_data)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    # Get the user's preferences from the JSON request
    user_preferences = request.get_json()
    location = user_preferences['location']
    price_range = user_preferences['price']
    activity_type = user_preferences['activity_type']
    difficulty_level = user_preferences['difficulty_level']

    # Get the user's location and convert it to a numerical value
    user_location = adventure_data[adventure_data['location'] == location].index[0]

    # Get the user's price range and difficulty level
    user_price_range = price_range
    user_difficulty_level = difficulty_level

    # Scale the user's input
    user_input = scaler.transform([[user_price_range, user_difficulty_level]])

    # Get the nearest neighbors
    distances, indices = nn.kneighbors(user_input)

    # Get the recommended adventure spots
    recommended_spots = adventure_data.iloc[indices[0]]

    # Filter the recommended spots by activity type
    recommended_spots = recommended_spots[recommended_spots['activity_type'] == activity_type]

    # Return the recommended spots as a JSON response
    response = jsonify([{
        'location': spot['location'],
        'price': spot['price'],
        'activity_type': spot['activity_type'],
        'difficulty_level': spot['difficulty_level']
    } for index, spot in recommended_spots.iterrows()])

    return response

if __name__ == '__main__':
    app.run(debug=True)
