# Working Statistics Dashboard

This is a full-stack Flask application for managing employee data, analyzing work statistics, and supporting multi-role access (Admin, Manager, etc.).
It includes a visual admin interface, secure authentication, and dynamic chart rendering with Seaborn and Matplotlib.
The app also supports importing employee data from external systems (CSV/JSON), automatically saving it into a relational database, and visualizing trends through interactive dashboards.

## Features

- Role-based Authentication (Admin, Manager, Local Manager)

- User & Employee Management (via Flask-Admin)

- Statistics Dashboard with Seaborn & Matplotlib

- Password Reset via Email Token (JWT)

- Multi-department Filtering

- Navigation via Flask Blueprints

- Dockerized for easy deployment


## Tech Stack

- Backend: Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-Bcrypt

- Frontend: Flask-Admin (Bootstrap4 UI)

- Database: SQLite

- Visualization: Seaborn, Matplotlib

- Security: JWT, Bcrypt

- Containerization: Docker


## Running Locally

### With Docker

```
docker build -t working-stats-dashboard .
docker run -p 5000:5000 working-stats-dashboard
```

### Manual Setup

1. Clone the repo and create a virtual environment

2. Install dependencies:

```
pip install -r requirements.txt

```

3. Set environment variables (e.g. JWT secret, mail settings)

4. Run the app:

```
python run.py

```

## Default Roles & Permissions

| Role       	| Permissions                                 	|
|----------------|-------------------------------------------------|
| Admin      	| Full access, including User/Employee CRUD   	|
| Manager    	| View team data, limited editing             	|
| Chief Dept.	| Filtered stats and department views         	|
| Local Manager  | Read-only access to local employee data     	|



## Sample Plots

The app includes statistical visualizations for employee hours, visits, and more — available under the Stat Plots tab.


