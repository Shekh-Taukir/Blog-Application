# Blog Application

## Overview

The Blog Application is a web-based platform where users can register, log in, and create, read, update, and delete blog posts. This application is designed to be user-friendly, secure, and responsive, providing an efficient way to manage and share content.

## Features

### User Authentication

- **User Registration:** Users can create an account to access the application.
- **Login/Logout:** Secure login and logout functionality.
- **Password Security:** Passwords are hashed to ensure data security.

### Blog Management

- **Create Blogs:** Authenticated users can create new blog posts.
- **Read Blogs:** All users can view published blog posts.
- **Edit Blogs:** Authenticated users can edit their own blog posts.
- **Delete Blogs:** Authenticated users can delete their own blog posts.

### Additional Features

- **Responsive Design:** Optimized for desktops, tablets, and mobile devices.
- **Dark and Gold Theme:** Aesthetic design featuring a dark background with gold accents.
- **Search and Filter:** Quickly find blogs using keywords or filters.
- **User-Specific Dashboard:** Personalized dashboard to manage user-specific content.

## Technologies Used

### Backend

- **Framework:** FastAPI
- **Database:** SQLite/PostgreSQL
- **Authentication:** OAuth2 with Password Hashing (using `bcrypt`)

### Frontend

- **HTML/CSS/JavaScript:** Core technologies for a responsive UI
- **Optional Frameworks:** React.js or plain JavaScript, depending on the implementation

### Deployment

- **Web Server:** Uvicorn
- **Cloud Deployment:** Can be hosted on platforms like AWS, Heroku, or Render.

## Acknowledgments

- Thanks to the open-source community for providing tools and frameworks.
- Inspired by various blogging platforms to create an intuitive application.
