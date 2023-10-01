TestJob
An expense sharing application is where you can add your expenses and split it among
different people. The app keeps balances between people as in who owes how much to
whom.

## Getting Started

1. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/Akshay-bisht/splitwise.git
2. Create a virtual environment and activate it:
    ```shell
    python -m venv venv
    source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
3. Install the required dependencies:
    ```shell
    pip install -r requirements.txt
4. Run the Django development server:
    ```shell
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
5. Open your web browser and access the application at http://localhost:8000/
6. To run test cases:
    ```shell
    python manage.py test

Register User

http://127.0.0.1:8000/api/users/register/ #POST
![Register API](image.png)

Login User

http://127.0.0.1:8000/api/user/login/ #POST
![Login API](image-1.png)

Generate Expenses

http://127.0.0.1:8000/api/expenses/ # POST
Body: {
    "user_paid": 4,  // User1's ID
    "description": "Testings Bill",
    "amount": 1200.00,
    "expense_type": "PERCENT",
    "selected_user":[{
        "user_id":2,
        "share":20
    },{
        "user_id":3,
        "share":20
    },{"user_id":4,
        "share":20
    },{
        "user_id":1,
        "share":40
    }]
}
![Expenses share](image-2.png)

Individual User Balance

http://127.0.0.1:8000/api/user_balances/ # GET
![User Balance](image-3.png)

Passbook

http://127.0.0.1:8000/api/passbook/ # GET
![User passbook](image-4.png)