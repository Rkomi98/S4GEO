
![logo](https://user-images.githubusercontent.com/72648197/170985612-5f4d9e43-4dd0-4541-89a7-63c116f66eda.png)

This is the repository of the project developed for the course "Software Engineering for Geoinformatics" by [@Se4GEO/contributors](https://github.com/Rkomi98/S4GEO/graphs/contributors). 
```diff
@@Read it before downloading the files@@
```
We are including here a short description on what our software provides to users and how they can use it.
Our webiste is an Open-Source Web Application, created to give to all users the possibility to get informed about air pollution and pollutants, on 5 cities: it is possible thanks to visualization of air quality data from sensors and through further analysis provided by the application.

## What do I need to run the application on my device? 
To run the application on your device it is mandatory to have installed all the libraries you can find at the beginning of the python script available in the main.py file. Then:
1. Configure the database in the PGADMIN application (the installation of PGADMIN and the extention of Postgis is mandatory to run the application). If you haven't installed PGADMIN and PostgresSQL we suggest you to use the username and password we used in the dbconfig.txt file. Otherwise you will have to change in the application the password ('Gram2021'), the name of user and of the database according to the one used in your device. 
2. Before running the application for the first time you the "createschema.py" file and then to use jupyter notebook "DatabaseCreation.ipynb"
3. Check if the databases exist in your local database.
4. Be careful to open your Python editor and have in the path the main, the dbconfig.txt file exactly as you can find it in the repository.
5. Run the app from main.py file.
## Sections of the web application
After running the main.py file the users can access the homepage. On the top menu bar the users can access only the "More Info" page without logging in. Inside this page they can view general information about our application and about the air quality data we use. 
To create a project the users need to be registered, so it is important that the database is correctly configured.
#### How to register and login
To register the user has to go in the login page and then in register. Once registered, the user can login.
* If the user is already registered and tries to register with the same user, the page is automatically reloaded
* If the user tries to login with the wrong user or password, the page is automatically reloaded
![immagine](https://user-images.githubusercontent.com/72648197/171901830-c62b520e-1a0d-4f18-80f1-4a843e73a182.png)
![immagine](https://user-images.githubusercontent.com/72648197/171902834-46eb3940-d959-49f8-88e2-eeaf71c81ac6.png)


### Create Project page
In the "Create project" page you can decide a city between:
* Skopje
* Belgrad
* Krakow
* Paris
* London

Furthermore you can choose if you want "Real data" (the frequence of update changes between city and city) or forecast data (so data of pollutants of the last 2 days, today and the next 5 days) or both. In the last case the analysis will be performed only on forecast data.  
![projpage](https://user-images.githubusercontent.com/94118751/172116201-b3346263-2c45-48de-bc41-a53e06fd3e90.jpg)
:warning: **If you have performed only some requests it is normal if you receive error**: Try the jupyter notebook if you want to see the problem. You need some observations to perform a pandas profiling analysis.

