# Recruitment task for AI Clearing
Python implemented REST API handling a car database. Made as a part of recruitment process for the Software Developer Intern position at AI Clearing.
## Setting up locally
1. Clone the repozitory
2. (Optionally) initialize Python virtual enviroment

    Windows (Powershell):
    ```
    $ python -m venv .env
    $ .\.env\Scripts\Activate.ps1
    ```
    Linux:
    ```
    $ python -m venv .env
    $ source .env/bin/activate
    ```
3. Install requirements
    ```
    $ pip install -r requirements.txt
    ```
4. Initialize database
    ```
    $ flask shell
    >>> from app import db
    >>> db.create_all()
    >>> exit()
    ```
5. Run the application
    ```
    $ flask run
    ```
## Usage
The API responds to requests specified in `task.txt` file. `tests.py` requires initialized database and the application running locally (if needed, change the `URL` constant). The application is hosted online under [here](https://ai-clearing-recr-784938d7e519.herokuapp.com/).

### Requests
-  **POST /cars** request requires a make and a model of a car: `{"make" : "foo", "model" : "foo"}` The database can hold multiple cars of the same make and model. API returns the car's ID from database.
-  **GET /cars** request doesn't require a body. It returns all cars from database with their average rate.
- **GET /popular** request requires an amount of cars to be returned: `{"amount" : X}` where X is an integer bigger than 0.
- **POST /rate** request requires: `{"id" : X, "value" : Y}` where X is an existing car's ID and Y is an integer between 1 and 5. It returns the rate's ID from datbase.
## Additional tools used
- **SQLite Database viewer** - for assessing the database
- **Postman** - for testing requests during development
- **Heroku** - for hosting of the API
