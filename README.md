# Social Network APIs

# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/nayan441/social_network.git
    $ cd social_network
## Without Docker    
Activate the virtualenv for your project.
    
    $ virtualenv venv
    $ source venv/bin/activate (for Ubuntu)
    $./venv/Script/activate (for Windows)

Install project dependencies:

    $ pip install -r requirements.txt
    
Then simply apply the migrations:

    $ python manage.py makemigrations
    $ python manage.py migrate

Create some  users:

    $ python manage.py create_users
    

You can now run the development server:

    $ python manage.py runserver

## With Docker    


Build a docker image

    $ docker build -t my_social_network .

Run a docker image

    $ docker run -p 8000:8000 my_social_network

## Postman API collection

Create an environment for Postman collection as it is required to create and update variables for smooth testing.
There are some tests in Postman for automated token updation.
Entire documentation can be access by clicking on "View complete collection documentation-->" tab  in postman
Create some users first with email, password and name.