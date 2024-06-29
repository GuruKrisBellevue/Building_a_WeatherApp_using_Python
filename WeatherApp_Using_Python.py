# Weather App using Python Flask
# Author: Guruprasad Velikadu Krishnamoorthy
# Description: Build a WeatherApp that looks up weather using a US City name
# and  State code or by using US Zip code using Python Flask
# Date: 11/19/2022

# Change#:1
# Change(s) Made: Initial version of code
# Date of Change: 11/19/2022
# Author: Guruprasad Velikadu Krishnamoorthy
# Change Approved by:
# Date Moved to Production:

# Importing Libraries
import requests
from flask import Flask, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFProtect
import ast
import wtforms
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

# Declaring variables and the API URLs
limit = 1
API_key = 'c32c8a6653a4b8573ffe00abcd4e6d67'
weatherapi_url = "https://api.openweathermap.org/data/2.5/weather"
city_geocode_url = "http://api.openweathermap.org/geo/1.0/direct"
zip_geocode_url = "http://api.openweathermap.org/geo/1.0/zip"

# Dictionary with US state codes and description used in the forms
US_states = {
    'ak': 'alaska',
    'al': 'alabama',
    'ar': 'arkansas',
    'as': 'american samoa',
    'az': 'arizona',
    'ca': 'california',
    'co': 'colorado',
    'ct': 'connecticut',
    'dc': 'district of columbia',
    'de': 'delaware',
    'fl': 'florida',
    'ga': 'georgia',
    'gu': 'guam',
    'hi': 'hawaii',
    'ia': 'iowa',
    'id': 'idaho',
    'il': 'illinois',
    'in': 'indiana',
    'ks': 'kansas',
    'ky': 'kentucky',
    'la': 'louisiana',
    'ma': 'massachusetts',
    'md': 'maryland',
    'me': 'maine',
    'mi': 'michigan',
    'mn': 'minnesota',
    'mo': 'missouri',
    'mp': 'northern mariana islands',
    'ms': 'mississippi',
    'mt': 'montana',
    'na': 'national',
    'nc': 'north carolina',
    'nd': 'north dakota',
    'ne': 'nebraska',
    'nh': 'new hampshire',
    'nj': 'new jersey',
    'nm': 'new mexico',
    'nv': 'nevada',
    'ny': 'new york',
    'oh': 'ohio',
    'ok': 'oklahoma',
    'or': 'oregon',
    'pa': 'pennsylvania',
    'pr': 'puerto rico',
    'ri': 'rhode island',
    'sc': 'south carolina',
    'sd': 'south dakota',
    'tn': 'tennessee',
    'tx': 'texas',
    'ut': 'utah',
    'va': 'virginia',
    'vi': 'virgin islands',
    'vt': 'vermont',
    'wa': 'washington',
    'wi': 'wisconsin',
    'wv': 'west virginia',
    'wy': 'wyoming'
}

# Initiating the Flask Application
weather_app = Flask(__name__)
# Cross-site Request Forgery protection against Web attacks
csrf = CSRFProtect(weather_app)
csrf.init_app(weather_app)
# Assigning a secret keys for security
weather_app.config['SECRET_KEY'] = "7367734654756753645736387887"

"""
This function will validate for the numbers in ZIP code and raise exception 
if invalid values are entered. It is used in the Class Validations.
"""


def validate_numbers_only(form, field):
    try:
        if not int(field.data.strip(" ")) or len(field.data.strip(" ")) \
                < 5:
            raise ValidationError('Please enter a valid 5 digit Zip Code')
        else:
            pass
    except:
        raise ValidationError('Please enter a valid 5 digit Zip Code')


"""
This Class definition includes the form objects for GeoCode lookup using 
City name and State entered by user.
It uses the fields and validators from wtforms
"""


class WeatherByCityName(FlaskForm):
    # Field to capture the City name. Required field
    city_name = StringField("CityName",
                            validators=[DataRequired(), Length(min=2)])
    # Field to capture the state name. Required field
    state = SelectField("StateName",
                        validators=[DataRequired()],
                        choices=[
                            (' ', ' '),
                            ('AL', 'Alabama'),
                            ('AK', 'Alaska'),
                            ('AZ', 'Arizona'),
                            ('AR', 'Arkansas'),
                            ('CA', 'California'),
                            ('CO', 'Colorado'),
                            ('CT', 'Connecticut'),
                            ('DE', 'Delaware'),
                            ('DC', 'District Of Columbia'),
                            ('FL', 'Florida'),
                            ('GA', 'Georgia'),
                            ('HI', 'Hawaii'),
                            ('ID', 'Idaho'),
                            ('IL', 'Illinois'),
                            ('IN', 'Indiana'),
                            ('IA', 'Iowa'),
                            ('KS', 'Kansas'),
                            ('KY', 'Kentucky'),
                            ('LA', 'Louisiana'),
                            ('ME', 'Maine'),
                            ('MD', 'Maryland'),
                            ('MA', 'Massachusetts'),
                            ('MI', 'Michigan'),
                            ('MN', 'Minnesota'),
                            ('MS', 'Mississippi'),
                            ('MO', 'Missouri'),
                            ('MT', 'Montana'),
                            ('NE', 'Nebraska'),
                            ('NV', 'Nevada'),
                            ('NH', 'New Hampshire'),
                            ('NJ', 'New Jersey'),
                            ('NM', 'New Mexico'),
                            ('NY', 'New York'),
                            ('NC', 'North Carolina'),
                            ('ND', 'North Dakota'),
                            ('OH', 'Ohio'),
                            ('OK', 'Oklahoma'),
                            ('OR', 'Oregon'),
                            ('PA', 'Pennsylvania'),
                            ('RI', 'Rhode Island'),
                            ('SC', 'South Carolina'),
                            ('SD', 'South Dakota'),
                            ('TN', 'Tennessee'),
                            ('TX', 'Texas'),
                            ('UT', 'Utah'),
                            ('VT', 'Vermont'),
                            ('VA', 'Virginia'),
                            ('WA', 'Washington'),
                            ('WV', 'West Virginia'),
                            ('WI', 'Wisconsin'),
                            ('WY', 'Wyoming')])
    # Radio field to capture Temperature units. If not selected, Fahrenheit
    # will be default value.
    unit = RadioField('Unit of Temperature', choices=['Fahrenheit',
                                                      'Celsius', 'Kelvin'],
                      default='Fahrenheit')
    # Submit button to validate and post the response to API
    submit = SubmitField("Search")


"""
This Class definition includes the form objects for GeoCode lookup using 
Zipcode entered by user.
It uses the fields and validators from wtforms
"""


class WeatherByZip(FlaskForm):
    # Field to capture the City name. Required field. Must be 5 Digits.
    zip_code = StringField("ZipCode", [
        wtforms.validators.DataRequired(), wtforms.validators.length(
            min=5, max=5, message="Please enter 5 Digit Zip code"),
        validate_numbers_only])
    # Radio field to capture Temperature units. If not selected, Fahrenheit
    # will be default value.
    unit = RadioField('Unit of Temperature', choices=['Fahrenheit',
                                                      'Celsius', 'Kelvin'],
                      default='Fahrenheit')
    # Submit button to validate and post the response to API
    submit = SubmitField("Search")


"""
This Function will request a response from the API and catch the HTTPError 
and ConnectionError exceptions.
Inputs : API URL and the Parameters for the API response.
Outputs : URL Response and custom Error messages(if any).
"""


def catch_url_exceptions(url, params):
    # Using Try and Except block to catch HTTPError and Connection Errors
    try:
        url_response = {}
        error_message = " "
        # Using "GET" method to receive response from API
        url_response = requests.request("GET", url=url, params=params)
        url_response.raise_for_status()
        return url_response, error_message
    # Catch HTTPErrors
    except requests.exceptions.HTTPError:
        error_message = "Error! No Matching Values found! Please recheck the" \
                        "values entered and Try Again!"
        return None, error_message
    # Catch Connection errors
    except requests.exceptions.ConnectionError:
        error_message = "Hmm! Internet appears to be disconnected! Please " \
                        "try again later"
        return None, error_message
    # Catch other Exceptions
    except requests.exceptions.RequestException:
        error_message = "Error!!! Requests Exception found! Please try later"
        return None, error_message


"""
This function is used to extract values from the json and the list of 
child elements passed as an input.
Inputs :       Json from the URL Response,
               First Child element
               List of additional child elements in a list (Optional)
               Option that indicates if there are more than 1 Child element
                                                    Type: Boolean; (optional)
Outputs :      The extracted value from the Json
"""


def extract_values(json_variable, child_element1, *args, option=False):
    # Using Try and Except block to catch exceptions
    try:
        return_val = []
        # This will execute if there are more than 1 Child element
        if not option:
            # Extracting the first child element
            return_val = json_variable[child_element1]
            # Looping through all the child elements
            for item in args:
                return_val = return_val[item]
                # Returning the final value
            return return_val
        # This will be executed if there is only 1 child element
        else:
            return_val = json_variable[child_element1]
            return return_val
        # Catching Key error exceptions and returning None
    except KeyError:
        return_val = None
        return return_val
        # Catching Index error exceptions and returning None
    except IndexError:
        return_val = None
        return return_val


"""
This  Function is to capture the user choice of unit of Temperature and 
translate that into the value that API can understand.
If User chooses Fahrenheit, the function returns Imperial
            for Celsius, the function returns Metric
            for Kelvin, the function returns Standard
Inputs  : The Unit value chosen by the user
Outputs : Temperature Unit that API can understand and the Symbol for display
"""


def request_units(units):
    if units.lower() == 'fahrenheit':
        final_units = 'imperial'
        symbol = '\u00b0F'

    elif units.lower() == 'celsius':
        final_units = 'metric'
        symbol = '\u00b0C'

    elif units.lower() == 'kelvin':
        final_units = 'standard'
        symbol = ' k'

    else:
        final_units = 'imperial'
        symbol = '\u00b0F'

    return final_units, symbol


"""
This function parses the Json response from the API and the final Weather 
results to be displayed to the user.
Inputs   : The JSON response from the API and the Unit of Temperature chosen 
           by user. 
Outputs  : Final output in a dictionary to be displayed to the user.
"""


def weather_response(parse_json, units):
    # This block will execute if No matching values were returned by the API
    if parse_json is None:
        # Return empty response for each field due to no Matching value
        weather_results = {
            'City_Name': "",
            'State': "",
            'Country': "",
            'Main Condition': "",
            'Description': "",
            'Temperature': "",
            'Minimum Temperature': "",
            'Maximum Temperature': "",
            'Feels Like Temperature': "",
            'Humidity': "",
            'Pressure': "",
            'Cloud Cover': ""
        }
        # This indicator is used in the final output to show a generic error
        index_error = True
    # This block will execute if data is returned by the API
    else:
        # Extracting values from the Geocode API response
        latitude = extract_values(parse_json, 'lat')
        longitude = extract_values(parse_json, 'lon')
        city_name = extract_values(parse_json, 'name')
        state = extract_values(parse_json, 'state')
        country = extract_values(parse_json, 'country')
        # Calling the function to translate the Units that API understands
        final_units, symbol = request_units(units)
        # Assigning parameters for Weather API
        weatherapi_parameters = {'lat': latitude, 'lon': longitude,
                                 'appid': API_key,
                                 'units': final_units}
        # This will get response from Weather API and catch errors
        weatherapi_response, error_message = catch_url_exceptions(
            weatherapi_url, weatherapi_parameters)
        # Converting API response to JSON format
        weatherapi_json = weatherapi_response.json()
        # This will extract values from the Weather API response
        main_condition = extract_values(weatherapi_json, 'weather', 0, 'main',
                                        option=False)
        description = extract_values(weatherapi_json, 'weather', 0,
                                     'description', option=False)
        temperature = extract_values(weatherapi_json, 'main', 'temp',
                                     option=False)
        min_temp = extract_values(weatherapi_json, 'main', 'temp_min',
                                  option=False)
        max_temp = extract_values(weatherapi_json, 'main', 'temp_max',
                                  option=False)
        feels_like = extract_values(weatherapi_json, 'main', 'feels_like',
                                    option=False)
        humidity = extract_values(weatherapi_json, 'main', 'humidity',
                                  option=False)
        pressure = extract_values(weatherapi_json, 'main', 'pressure',
                                  option=False)
        cloud_cover = extract_values(weatherapi_json, 'clouds', 'all',
                                     option=False)
        # The Geocode API for Zipcode search does not return State information.
        # The below statements is to handle if State is returned as None
        if state is None:
            # This is the output for search using ZipCode
            weather_results = {
                'City Name': city_name,
                'Country': country,
                'Main Condition': main_condition,
                'Description': description,
                'Temperature': str(temperature) + symbol,
                'Minimum Temperature': str(min_temp) + symbol,
                'Maximum Temperature': str(max_temp) + symbol,
                'Feels Like Temperature': str(feels_like) + symbol,
                'Humidity': str(humidity) + ' %',
                'Pressure': str(pressure) + ' hPa',
                'Cloud Cover': str(cloud_cover) + ' %'
            }
            index_error = False
            # This is the output for search using City names
        else:
            weather_results = {
                'City Name': city_name,
                'State': state,
                'Country': country,
                'Main Condition': main_condition,
                'Description': description,
                'Temperature': str(temperature) + symbol,
                'Minimum Temperature': str(min_temp) + symbol,
                'Maximum Temperature': str(max_temp) + symbol,
                'Feels Like Temperature': str(feels_like) + symbol,
                'Humidity': str(humidity) + ' %',
                'Pressure': str(pressure) + ' hPa',
                'Cloud Cover': str(cloud_cover) + ' %'
            }
            index_error = False
    return weather_results, index_error


"""
Flask decorator and function for home page and it renders home_page.html
"""


@weather_app.route("/")
@weather_app.route("/home")
def home():
    return render_template("home_page.html")


"""
Flask Decorator and function for search based on City name and State name.
It renders city_search.html
"""


@weather_app.route("/city_search", methods=["GET", "POST"])
def city_search():
    # Instantiating object for WeatherByCityName class
    city_form = WeatherByCityName()
    # This block will execute if the request is Post and form is submitted
    # without any validation errors
    if request.method == "POST" and city_form.validate_on_submit():
        # Getting data from the form and assigning to variables
        city_name = request.form.get("city_name").strip(" ")
        state_code = request.form.get("state").strip(" ")
        # Search is only restricted to US cities.
        country_name = 'USA'
        units = request.form.get("unit").strip(" ")
        # creating Parameter to be used for Geocode API response
        city_parameters = {'q': f"{city_name},{state_code},{country_name}",
                           'limit': limit, 'appid': API_key}
        # This will call the GeoCode API response using City name & state
        city_response, error_message = catch_url_exceptions(city_geocode_url,
                                                            city_parameters)
        # Starting Try and except block to validate the API response
        try:
            # This block will execute if the API response is not empty
            if city_response.json():
                city_json = city_response.json()[0]
                # Extracting the Weather response by calling the function
                weather_results, index_error = weather_response(city_json,
                                                                units)
                return redirect(url_for('results',
                                        weather_results=weather_results,
                                        index_error=index_error,
                                        error_message=error_message))
            # This block will execute if city response is empty
            else:
                weather_results, index_error = weather_response(None, units)
                return redirect(url_for('results',
                                        weather_results=weather_results,
                                        index_error=index_error,
                                        error_message=error_message))
        # Except block will execute if the response is empty and JSON
        # conversion throws exceptions
        except:
            weather_results, index_error = weather_response(None, units)
            return redirect(url_for('results',
                                    weather_results=weather_results,
                                    index_error=index_error,
                                    error_message=error_message))
    # This will execute if the request is GET when the page first loads
    else:
        return render_template("city_search.html", title="SearchByCityName",
                               form=city_form)


"""
Flask decorator to display the final results. This takes Weather results, 
Errors from URL exceptions(if any) and Index error messages(if any) as inputs.
It renders the page final_results.html
"""


@weather_app.route("/<weather_results>/<error_message>/<index_error>",
                   methods=["GET", "POST"])
def results(weather_results, error_message, index_error):
    # This block will execute if the request is Post
    if request.method == "POST":
        return f"<h1>'Please return to home page'</h1>"
    # This block will execute if the request is Get
    else:
        # This will convert the weather results response to dictionary format
        weather_results_dict = ast.literal_eval(weather_results)
        # This block will execute if Index errors are found and displays
        # error message to the User
        if index_error == 'True':
            index_error_msg = "It appears the values entered are not in our " \
                              "database!Please recheck the values and try " \
                              "the program again!"
        else:
            index_error_msg = " "
        return render_template("final_results.html", title="Weather_Results",
                               weather_results=weather_results_dict,
                               error_message=error_message,
                               index_error_msg=index_error_msg)


"""
Flask decorator and function for Zip code search.
This will render zip_search.html
"""


@weather_app.route("/zip_search", methods=["GET", "POST"])
def zip_search():
    # Instantiating object for WeatherByZip class
    zip_form = WeatherByZip()
    # This block will execute if the request is Post and form is submitted
    # without any validation errors
    if request.method == "POST" and zip_form.validate():
        # Getting data from the form and assigning to variables
        zip_code = request.form.get("zip_code").strip(" ")
        # Search is only restricted to US cities.
        country_code = 'US'
        units = request.form.get("unit").strip(" ")
        # creating Parameter to be used for Geocode API response
        zip_parameters = {'zip': f"{zip_code},{country_code}",
                          'appid': API_key}
        # This will call the GeoCode API response using Zip code
        zip_response, error_message = catch_url_exceptions(zip_geocode_url,
                                                           zip_parameters)
        # Starting Try and except block to validate the API response
        try:
            if zip_response.json():
                zip_json = zip_response.json()
                # Extracting the Weather response by calling the function
                weather_results, index_error = weather_response(zip_json,
                                                                units)
                return redirect(url_for('results',
                                        weather_results=weather_results,
                                        index_error=index_error,
                                        error_message=error_message))
            # This block will execute if API response is empty
            else:
                weather_results, index_error = weather_response(None, units)
                return redirect(url_for('results',
                                        weather_results=weather_results,
                                        index_error=index_error,
                                        error_message=error_message))
        # Except block will execute if the response is empty and JSON
        # conversion throws exceptions
        except:
            weather_results, index_error = weather_response(None, units)
            return redirect(url_for('results',
                                    weather_results=weather_results,
                                    index_error=index_error,
                                    error_message=error_message))
    # This will execute if the request is GET when the page first loads
    else:
        return render_template("zip_search.html", title="SearchByZip",
                               form=zip_form)


"""
This is to catch exceptions if user enters any other invalid route and 
route to the home page
"""


@weather_app.route("/<name>")
def exception_page1(name):
    return render_template("home_page.html")


@weather_app.errorhandler(404)
def pageNotFound(error):
    return render_template("home_page.html")


"""
This is the main block. It will run the weather_app Flask Application.
"""


def main():
    weather_app.run()


"""
Calling the Main function.
"""
if __name__ == "__main__":
    main()
