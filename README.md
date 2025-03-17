# Link cutter / URL shortener

![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/tests-passing-brightgreen?style=flat-square&logo=pytest)!
![Flask](https://img.shields.io/badge/Flask-2.0.2-blue)
![Status](https://img.shields.io/badge/status-finished-green?style=flat-square)

## System requirements
* Python 3.9
* Flask 2.0.2
* Works on Linux, Windows, macOS

## Key features:
* Generates short links and associates them with the original long URLs
* Redirects to the original URL when accessing the short link

# User interface
The service has a single-page form consisting of two fields:
* A required field for the original long URL
* An optional field for a custom short link (maximum 16 characters)

If the user suggests a custom short link that is already taken, an appropriate notification appears. The existing link in the database remains unchanged.

If the user leaves the custom short link field empty, the service automatically generates one. The default format for a short link is six random characters, which can include:
* Uppercase latin letters
* Lowercase Latin letters
* Digits from 0 to 9

The automatically generated short link is added to the database only if the identifier is unique. Otherwise, a new identifier is generated.


## Project API

The project's API is publicly accessible. The service supports two endpoints:
* /api/id/ — POST request to create a new short link;
* /api/id/<short_id>/ — GET request to retrieve the original URL by the specified short URL.

Examples of API requests, possible responses, and errors are provided in the **openapi.yml** specification.


## API requests examples

**GET** `.../api/id/{short_id}/`
*200*
```
{
  "url": "string"
}
```
*404*
```
{
  "message": "Указанный id не найден"
}
```


**POST** `.../api/id/`
```
{
  "url": "string",
  "custom_id": "string"
}
```
*201*
```
{
  "url": "string",
  "short_link": "string"
}
```
*400*
```
{
  "message": "Отсутствует тело запроса"
}
```


## .env file template
```
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=SECRET
```


## Deployement

* Clone the project to your computer `git clone git@github.com:SemenovaLiza/yacut.git`
* Create a virtual environment `python3 -m venv venv`
* Activate the virtual environment:
* For Linux/macOS:

    ```
    source venv/bin/activate
    ```

* For Windows:

    ```
    source venv/scripts/activate
    ```
* Install dependencies from requirements.txt `pip install -r requirements.txt`
* Run tests `pytest`
* Run the application `flask run`

# Author
Elizaveta Semenova
