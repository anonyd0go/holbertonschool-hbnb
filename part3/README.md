# Part 3: Enhancing Backend with Authentication and Database Integration
In this part of the HBnB Project, will consist of the extending the backend of the application with the introduction of **user authentication**, **authorization**, and **database integration**. This phase will focus on securing the back end of our application, integrating persistent storage, and preparing the application for the scalability of real world deployment.

In this part, I will implement a true persistance layer for the application, initially with **SQLite** for development and migrate it to **MySQL** for production.  Authentication will also be introduced in order to secure the API by using **JWT-based Authentication**. The goal is to have hands-n experience in a real-world database system with efficient scalability and implement role based acces to enforce restrictions based on user's privileges.

## Objectives:
1. Authentication and Authorization:
    * Implement JWT-based authentication with **Flask-JWT-Extended** and role-based access control. (with the `is_admin` attribute for specified endpoints)

2. Database Integration:
    * Implement percistance to replace in-memory storage.
    * Use **SQLite** for development through the use of **SQLAlchemy** for ORM.
    * Prepare for production grade **RDBMS** like **MySQL**.

3. CURD Operations with Database Persistence:
    * Refactor all CURD operations to interact with the implemented persistance DB.

4. Database Design and Visualization:
    * Design a correctly mapped database schema with **mermaid.js**

5. Data Consistency and Validation:
    * Ensure data validation and constraints are properly enforced
