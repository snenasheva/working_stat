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


## Configuration

Create a .env file or set environment variables manually:

### Example `.env` file

```
SECRET_KEY=put_your_secret_key_here
JWT_SECRET_KEY=your_jwt_key
DATABASE_URL=sqlite:///work_hours.db

# Email settings
MAIL_SERVER=smtp.yourmailserver.com
MAIL_PORT=587
MAIL_USE_TLS=True
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_email_password
```

## Running Locally

### With Docker
1. Clone the repository
```
bash
git clone https://github.com/your-username/working_stat.git
cd working_stat
```

2. Create a .env file (see Configuration section above)

3. Build the Docker image

```
docker build -t working-stats-dashboard .
```

4. Run the container with environment variables

```
docker run --env-file .env -p 5000:5000 working-stats-dashboard
```

5. Access the app

Open your browser and go to http://localhost:5000

   
### Manual Setup

1. Clone the repo and create a virtual environment

```bash
git clone https://github.com/your-username/working_stat.git
cd working_stat
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

2. Install dependencies:

```
pip install -r requirements.txt

```

3. Set environment variables (or create .env as described above)

4. Run the app:

```
python run.py

```

## Database Migrations

flask db init   	# Run once to initialize
flask db migrate -m "Add something"
flask db upgrade


## Default Roles & Permissions

| Role       	| Permissions                                 	|
|----------------|-------------------------------------------------|
| Admin      	| Full access, including User/Employee CRUD   	|
| Manager    	| View team data, limited editing             	|
| Chief Dept.	| Filtered stats and department views         	|
| Local Manager  | Read-only access to local employee data     	|



## Sample Plots

The app includes statistical visualizations for employee hours, visits, and more — available under the Stat Plots tab.


