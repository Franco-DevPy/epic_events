# Epic Events CRM

CRM (Customer Relationship Management) system for Epic Events, an event management company.

## Features

- **User Management**: Three roles with different permissions (Management, Commercial, Support)
- **Client Management**: Track clients and their information
- **Contract Management**: Create and manage contracts with clients
- **Event Management**: Organize and track events linked to contracts
- **Authentication**: Secure JWT-based authentication system

## Tech Stack

- **Backend**: Python 3.x
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **CLI**: Questionary + Colorama
- **Authentication**: JWT + Argon2 (password hashing)

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL 12+

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Franco-DevPy/epic_events.git
cd epic_events
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:

Create a `.env` file in the root directory:
```env
# Database Configuration
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

# JWT Configuration
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
```

5. Create the database in PostgreSQL:
```sql
CREATE DATABASE your_database_name;
```

6. Initialize the database tables:
```bash
python -m app.database.init_db
```

## Usage

Run the application:
```bash
python epicevents.py
```

## User Roles

### Management
- View all clients, contracts, and events
- Create, update, and delete users
- Assign support users to events

### Commercial
- Create and manage their own clients
- Create contracts for their clients
- Create events for signed contracts
- View and update their own events

### Support
- View and update events assigned to them
- Cannot access client or contract management


## License

This project is part of OpenClassrooms Python Developer path - Project 12.
