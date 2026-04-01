"""
Flask server for Emotion Detection API.

This module exposes a single endpoint `/emotionDetector` that accepts
text input as a query parameter and returns the detected emotions along
with the dominant emotion in a formatted response.

It uses the emotion_detector function from the emotion_detection module
to analyze the emotional tone of the input text.
"""

from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

# Define a route for the root URL ("/")
@app.route("/")
def render_index_page():
    """ Returns the index page."""
    return render_template('/index.html')

#Define a route for the '/emotionDetector' URL
@app.route('/emotionDetector', methods=['GET'])
def emotiondetector():
    """
    Analyze the emotional tone of the provided text.

    This function retrieves the input text from the query parameter
    'textToAnalyze', processes it using the emotion_detector function,
    and returns a formatted string containing the emotion scores and
    the dominant emotion.

    Returns:
        str: A formatted string with emotion scores and dominant emotion,
             or an error message if the input is invalid.
    """
    try:
        # Get input text
        text_to_analyze = request.args.get('textToAnalyze')

        # Validate input
        if not text_to_analyze:
            return "Invalid Input! Try again!"

        # Call emotion detection function
        result = emotion_detector(text_to_analyze)

        # Check for invalid or empty result
        if result is None or result.get("dominant_emotion") is None:
            return "Invalid Input! Try again!"

        # Extract emotion values
        anger = result.get("anger")
        disgust = result.get("disgust")
        fear = result.get("fear")
        joy = result.get("joy")
        sadness = result.get("sadness")
        dominant_emotion = result.get("dominant_emotion")

        # Format response
        response_text = (
            f"For the given statement, the system response is "
            f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
            f"'joy': {joy} and 'sadness': {sadness}. "
            f"The dominant emotion is {dominant_emotion}."
        )

        return response_text

    except Exception as e: # pylint: disable=broad-exception-caught
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # pylint: disable=pointless-string-statement
    app.run(host="0.0.0.0", port=5000, debug=True)
