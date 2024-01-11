from flask import render_template, request, Blueprint, jsonify
from myblog.models import Post
import requests
main = Blueprint('main',__name__)



@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("index.html", posts=posts)

 

@main.route("/about")
def about():
    return render_template("about.html", title = "About")

@main.route('/calendar')  
def calendar():
    return render_template('calendar.html', title='Calendar')


@main.route("/weather")
def weather():
    lat = 44.9975455
    lon = 19.9384273
    api_key = 'f564165bcd870b35e7bb54944da16f94'  # Replace with your actual API key
    api_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Check if the response is JSON
        if 'application/json' in response.headers.get('content-type', ''):
            weather_data = response.json()
            return render_template('weather.html', weather_data=weather_data)
        else:
            # If not JSON, handle the error gracefully
            return render_template('weather.html', error='Unexpected response from the API')

    except requests.exceptions.RequestException as e:
        return render_template('weather.html', error=str(e))