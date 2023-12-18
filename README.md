# TakeTech

## Award
We recieved second place at 2021 Hackathon Taiwan Junior with this web app project.

## Overview
This repository contains the Flask application for a platform designed to facilitate donations and volunteer activities. It allows organizations to manage and display a complete list of resources, volunteer opportunities, and organization information. Individual donors can view their donated items, and both types of users can register as volunteers and donate items.

## Environment and Execution
To run the Flask app, use the following command:
```
python app.py
```

## Dependencies
This project uses the following Python modules:
- datetime
- re
- flask
- flask-login
- sqlalchemy.orm
- email.mime.multipart
- email.mime.text
- smtplib
- time
- sqlalchemy
- werkzeug.security
- os
- flask_sqlalchemy
- flask_migrate
- flask_wtf
- wtforms

## Features
### Organizational Account vs. Individual Donor Account
**Exclusive to Organizational Account:**
1. Access to a complete list of materials (`/products`).
2. View the list of volunteers (`/volunteer_list`).
3. Organization details are displayed on the organization info page (`/requests`).

**Exclusive to Individual Donor Account:**
1. View a list of materials they have uploaded (`/products`).

**Common Features for Both Accounts:**
1. Register as a volunteer (`/volunteer`).
2. Donate materials (`/post_product`).

### Web Functionality
1. Materials posted on `/post_product` can be viewed in the materials list (`/products`).
2. Volunteer applications from `/volunteer` are visible to organizations in the volunteer list (`/volunteer_list`).
3. Organizations can send emails from product detail pages, automatically sent from the official account (tacktech@gmail.com) to the uploader.
4. Donors can send emails to requesters through `/send`, facilitated by the official account (tacktech@gmail.com).
5. Item owners can delete their items from the item detail page.
6. Users can edit their public profiles by clicking on their username when logged in. Clicking on a donor's username in the materials list displays their profile.
7. Organization introductions are displayed on the organization info page (`/requests`).

## Project Proposal
For a detailed project proposal, visit the following link:
[Project Proposal](https://drive.google.com/file/d/1ZjV1g9mjQAdK7DxgEG81KdVpwRen12LQ/view?usp=sharing)
