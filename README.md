# Cigarette Detection System 

Instructions for Setting Up and Running the Cigarette Brand Detection 
Application

Installation
Clone the Repository:
```Bash
git clone https://github.com/Madhu-2101/Cigarette_Detection_System.git
```
1. Install Required Dependencies
Install the required Python packages by creating a virtual environment and installing the 
dependencies.
Create a virtual environment (venv):
 ```terminal
 python -m venv venv
 ```
Activate the virtual environment:
 ```terminal
 venv/Scripts/activate
 ```
Install required Python packages:
 In the root directory of the project, install the required packages by running:
 ```terminal
 pip install -r requirements.txt
 ```
2. Set Up MySQL Database
The project interacts with a MySQL database to store cigarette brand counts and removal 
logs.
Install MySQL: 
Download and install MySQL from https://dev.mysql.com/downloads/mysql.
Create the database:
 Log into the MySQL console:
 ```bash
 mysql -u root -p
 ```
 Run the following SQL commands to create the database and tables:
 ```sql
 CREATE DATABASE cigarette_tracking_database;

USE cigarette_tracking_database;

CREATE TABLE Brands (
 id INT PRIMARY KEY AUTO_INCREMENT,
 brand_name VARCHAR(255) UNIQUE,
 current_count INT,
 last_updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

 CREATE TABLE RemovalLogs (
 id INT PRIMARY KEY AUTO_INCREMENT,
 brand_id INT,
 count_before_removal INT,
 removed_count INT,
 count_after_removal INT,
 removal_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (brand_id) REFERENCES Brands(id)
 );
 ```
Update database connection settings:
 Change the database configuration in `database.py`. Adjust the following details as needed:
 ```python
 DB_CONFIG = {
 'host': 'localhost',
 'user': 'root',
 'password': ‘YourPassword',
 'database': 'cigarette_tracking_database'
 }
 ```
4. Run the Application
Now that everything is set up, we can run the application.
Start the Flask app with SocketIO:
 ```terminal
 python app.py
 ```
Access the application:
 Once the server is running, open web browser and navigate to `http://localhost:5000/`. main 
page of the application with options to start and stop video detection.

5. Start Real-Time Video Detection
- Use the "Start Video" button on the page to start the real-time detection process. This will 
initiate the webcam and begin detecting cigarette brands in the video feed using the YOLO 
model.(it takes around 30 - 40 seconds to start the camera)
View Results:
 - The page will display real-time detection counts for each cigarette brand.
 - The "Current Counts" section will show the current counts of the detected brands, and the 
"Removal Logs" section will display logs of any brand removals.
6. Stopping the Video Detection
To stop the detection process, use the "Stop Video" button on the main page. The video 
detection process will terminate, and the detection will cease.
7. Exit the Application
We can stop the Flask server by pressing `CTRL + C` in the terminal where the app is 
running.
