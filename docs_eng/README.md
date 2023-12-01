# Project: Mailing Management Service
 [Russian](../README.md)| **English**

## Project Description

The project "Mailing Management Service" is a web application developed in the Python programming language using the Django framework.
The project encompasses functionality for creating, managing, and tracking mailings, along with a blog for promoting the service.

## Components of the Project

The project consists of the following components:

1. **Home Application:**
    - Contains the base template and view template for the home page
    - Includes the `HomeView` controller for displaying the main page
    - Features the `get_cached_clients` function for caching clients on the homepage in the `services.py` file

2. **Blog Application:**
   - Includes the `Blog` model
   - Implements CRUD mechanisms for creating, editing, viewing, and deleting blog articles
   - Access rights are implemented to ensure that actions related to managing blog articles belong to the `"content_manager"` group

3. **Newsletter Application:**
    - Contains models for settings `MailingSettings`, messages `Message`, and logs `MailingLogs`
    - Implements CRUD mechanisms for creating, editing, viewing, and deleting mailings
    - Includes templates and controllers for displaying log lists
    - Features the `send_message` command for launching mailings from the terminal
    - Includes the `send_newsletter` function for automatic message distribution in the `services.py` file
    - Contains a validator in the `validators.py` file to validate the mailing creation/editing form

4. **Service Client Application:**
   - Includes the model for service clients `Client`
   - Implements CRUD mechanisms for creating, editing, viewing, and deleting clients

5. **Users Application:**
   - Contains the user model `User`
   - Includes templates and controllers for user login, registration, and verification
   - Features templates and controllers providing an interface for the manager's account
   - Contains controllers for generating a new password `GenerateNewPasswordView`, disabling a user `DisableUserView` and disabling mailings `DisableMessageView`

6. **Directory static:**
    - Contains `css-styles`, `images`, `JS code` 

## Technologies
   - The project is developed in the `Python` programming language using the `Django framework`
   - A third-party library, `psycopg2-binary`, is used for working with the database
   - `django-crontab` is employed for executing periodic tasks (automated mailings)
   - The project utilizes the in-memory database management system `Redis` for caching
   - `Poetry` is the chosen tool for managing the virtual environment
   - The frontend part of the project is written using `HTML`, `CSS-styles`, `JavaScript` and a framework `Bootstrap`

## How to install and run a project
   - Fork the repository
   - Install all dependencies from the `pyproject.toml` file
   - Create the database and perform migrations for the database with `python3 manage.py migrate`
   - Configure the necessary environment variables as specified in the `.env.sample` file
   - Start the server with `python3 manage.py runserver`

## How to use the project
   - Initially you need to register or log in with email and password 
   - As a regular user, you have access to functionalities such as viewing service clients, your mailings, and reports of your mailings
   - As a regular user, you can edit, delete your mailings, and view the mailing report. Mailings and reports of other users are not accessible to you
   - Mailing settings are available to choose from an existing list
   - You can browse articles from the blog
   - For a manager, the manager's toolkit is available, including:
      - Can view any mailings
      - Can view the list of service users and the client list
      - Can block service users
      - Can disable mailings
      - Cannot edit mailings
      - Cannot manage the mailing list
      - Cannot change mailings and messages
   - The content manager has full rights to work with the CRUD mechanism of the blog

## Notes
   - The project was developed as an educational assignment and can be further enhanced and expanded for broader use
   - Interfaces for modifying and creating entities are implemented using `Django-forms`
   - Environment variables necessary for project operation can be found in the `.env.sample` file
   - All required dependencies are listed in the `pyproject.toml` file