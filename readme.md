# TEST Web telescope control software

## How to

First, install the requirements from the requirements.txt file
```bash
pip install -r requirements.txt
```
Then run the migrations, which creating the database tables
```bash
python manage.py migrate
```
After that, a superuser (admin) must be created
```bash
python manage.py createsuperuser
```
fill the requested information (the eMail address is not needed for this project and can be empty).

Finally, we can start the development web-server
```bash
python manage.py runserver
```