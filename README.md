# Billionnaires Budget Buddy

A professional desktop financial management application built with Python, MySQL, and CustomTkinter.

## Features

- **Dual User Roles**: Support for clients (regular users) and bankers (administrators)
- **Secure Authentication**: User registration and login with encrypted passwords
- **Account Management**: Create, view, and manage multiple financial accounts
- **Transaction Management**: Add funds, withdraw, transfer between accounts, and send to external accounts
- **Transaction Categorization**: Organize all transactions with income and expense categories
- **Financial Analytics**: View account balance history, spending by category, and more
- **Reports**: Download transaction reports for selected periods
- **Real-time Updates**: All changes reflected immediately in the UI

## Screenshots

*Screenshots will be added here once the application is deployed*

## Requirements

- Python 3.8+
- MySQL 8.0+
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/billionnaires-budget-buddy.git
   cd billionnaires-budget-buddy
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up MySQL:
   - Create a MySQL database
   - Configure database connection in a `.env` file (see Configuration section)

5. Initialize the database:
   ```
   python app/database_setup.py
   ```

## Configuration

Create a `.env` file in the root directory with the following variables:

```
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_PORT=3306
DB_NAME=billionnaires_budget_buddy
```

## Usage

Run the application:

```
python app/app.py
```

### Default Admin Account

After initializing the database, a default admin account is created:

- Email: admin@billionnaires.com
- Password: admin123

**Important**: Change this password after first login in a production environment.

## Project Structure

```
billionnaires-budget-buddy/
├── app/
│   ├── models/
│   │   ├── user.py
│   │   ├── account.py
│   │   ├── transaction.py
│   │   └── category.py
│   ├── views/
│   │   ├── login_view.py
│   │   ├── register_view.py
│   │   ├── main_view.py
│   │   ├── dashboard_view.py
│   │   ├── accounts_view.py
│   │   ├── transactions_view.py
│   │   ├── analytics_view.py
│   │   └── dialogs/
│   │       ├── add_funds_dialog.py
│   │       ├── withdraw_funds_dialog.py
│   │       ├── transfer_funds_dialog.py
│   │       └── send_funds_dialog.py
│   ├── controllers/
│   ├── utils/
│   ├── resources/
│   │   └── icons/
│   ├── database_setup.py
│   └── app.py
├── requirements.txt
├── .env
└── README.md
```

## Development

### Adding a New Feature

1. Create necessary models in `app/models/`
2. Create required views in `app/views/`
3. Update the database schema in `app/database_setup.py` if needed
4. Implement the feature in the appropriate controller

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- CustomTkinter for the modern UI components
- Matplotlib for data visualization
- MySQL for robust data storage 