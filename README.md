# Recruitment task for AI Clearing
Python implemented REST API handling a car database. Made as a part of recruitment process for the Python Developer Intern position at AI Clearing.
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
The API responds to requests specified in `task.txt` file.