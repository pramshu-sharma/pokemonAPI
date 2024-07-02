Instructions for the application:

Clone Git Repo
  1. Use the command in a terminal: git clone https://github.com/pramshu-sharma/pokemonAPI

Setting up Virtual Environment
  1. Navigate to the project folder using the terminal and create a virtual environment. (e.g. virtualenv pokemonenv)
  2. Activate Virtual Env. (e.g. .\pokemonenv\Scripts\activate)

Installing Requirements and Setting Up Environment Variables
  1. With the virtualenv activated install requirements. (pip install -r requirements.txt)
  2. Enter database credentials in the .env file. (user, password, database (DB), host)

Loading data from the API to the Postgresql DB
 1. Run the script load_data.py.
 2. When completed the data should be present in the DB.

Using the Application
  1. When in the project folder in the terminal type 'uvicorn app:app --reload' to run the application.
  2. After the server has been booted up, navigate to '/api/v1/pokemons' to use the application.
  3. Use the form at the top to filter the results.

Application Screenshot
![image](https://github.com/pramshu-sharma/pokemonAPI/assets/125169937/6eaa12a3-81ce-4a53-adae-f9a735b927e2)

  
