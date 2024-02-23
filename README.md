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
## Additional tools used
- **SQLite Database viewer** - for assessing the database
- **Postman** - for testing requests during development
- **Heroku** - for hosting of the API
