# Indus: An AI-Web Innovation for Smart E-commerce

### Technology Stack
- Python 3.8
- Flask
- Scikit-Learn
- Tensorflow

### TODOS
1. Complete the Edit Product functionality
2. Integrate the Chatbot

### Setting up the project
1. Create a .env file inside the project folder.
2. Set the following variables in the .env file
    - FLASK_CONFIG, options are development and production
    - SECRET_KEY, Generate a secret key and set it to this variable
    - SESSION_TYPE, Specify a session type, I used sqlalchemy session
    - DATABASE_URL OR DEV_DATABASE_URL, Set it according to the type of FLASK_CONFIG
3. Set the FLASK_APP=run.py using your terminal.
4. Create database tables using `flask db migrate`
5. Seed the data into the database tables.
