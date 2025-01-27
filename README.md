# Videoflix Backend

This is the backend part of the Videoflix project, built with Django to power the video streaming platform.

## Requirements

- You need to have **Python** installed to run this project.

## Getting Started

1. **Clone the Frontend and Backend Projects**
   - Clone this backend project.
   - Clone the frontend project as well (find the frontend [here](https://github.com/Kakar21/Videoflix-Frontend)).

2. **Create a Virtual Environment**
   - In the project root, create a virtual environment:
     ```bash
     python -m venv env
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       env\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source env/bin/activate
       ```

3. **Install Dependencies**
   - Install all required packages from `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

4. **Configure Environment Variables**
   - Copy the `.env.example` file and rename it to `.env`:
     ```bash
     cp videoflix_backend/.env.example videoflix_backend/.env
     ```
   - Open `.env` and enter your own configuration details.

5. **Run Migrations**
   - Apply database migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

6. **Create an Admin User**
   - Create a superuser for the admin panel:
     ```bash
     python manage.py createsuperuser
     ```
   - Follow the prompts to enter username, email, and password.

7. **Start Windows RQ Worker** (if using Windows)
   - Run the following command:
     ```bash
     rqworker -w rq_win.WindowsWorker
     ```

8. **Start the Server**
   - Start the Django server:
     ```bash
     python manage.py runserver
     ```

9. **Access the Admin Panel**
   - Open your browser and go to:
     ```
     http://127.0.0.1:8000/admin
     ```
   - Log in with the admin credentials created earlier.

10. **Add Video Content**
   - Use the admin panel to create and manage videos as needed.

11. **Follow Frontend README**
   - Once the backend is set up, follow the instructions in the frontend README to start the UI.

### You're Done!

Your backend server is now up and running, ready to support Videoflix. Enjoy developing your Netflix clone!
