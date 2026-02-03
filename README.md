# NUN North Country Wild Uploader (Dorsie)

## Project Overview
The NoCo Wild Uploader is a web-based application developed as part of the NUN NoCo Wild project. NoCo Wild supports wildlife research and conservation efforts in the A2A region.

The application is designed to:

 - Provide a simple, user-friendly interface for uploading game camera images along with the associated metadata.

 - Handle uploaded data in a structured and consistent way on the backend.

 The uploader acts as a bridge between field data collection, helping ensure that the data gathered can be efficiently stored, managed, and later used to inform research.

## Data Flow Overview
The uploader guides collected data from the user through the frontend and backend before it is saved for later use. Users upload their game camera images and complete the form with all required details.

The diagram below illustrates how data moves from the user's game camera to the application interface, and then through the backend into storage. 

(insert diagram)

## Running the Application (Tutorial)

1. ...

2. ...

## Application Structure
The application is split into a small Flask backend (app.py) and a single frontend file (index.html). Together, these handle user access, data collection, and file uploads for the NoCo Wild uploader.

### app.py (backend)
The backend is run using Flask and is responsible for managing access to the application and handling submitted data. Its main components include:

- Login System (prototype): Currently provides a simple hard-coded login. The goal is to use SAML so users can connect to their NUN account on login.

- Page Routes: There is a login page and the main uploader interface.

- Background Routes: Handles behind-the-scences actions such as saving selected data, map coordinates, and uploaded files as the user moves through the form.

- Final Submission Handling: Collects the uploaded images and puts them into the uploads folder. Also, collects all form data and puts that into a JSON file in the uploads folder.

### index.html (frontend)
The frontend consists of a single HTML page that guides users through the submission process using tabs. Its main components include:

 - Tabbed Form Layout: Organizes the uploader into clear steps (Upload, Affiliation, Habitat, Dates, Location, Submit) while keeping everything within one form.

 - File Upload Interface: Allows users to upload entire folders of media using drag and drop or file section.

 - Map-Based Location Selection: Integrates an interactive map that lets users select the deployment location by clicking on the map.

 - User Interaction and Validation: Uses JavaScript to control tab switching, check that required fields are completed, and provide visual feedback as selections are saved.

 - Backend Communication: Sends data to the Flask backend as needed without reloading the page, and submits all collected data at the end of the process.


