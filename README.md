# Web Spider by Python

In this repository, I try to use some wonderful python libraries and framework to achieve tricky web crawlers...



## Quick Start

### Set Environment 

1. Activate a virtualenv using python3 

```sh		
$ virtualenv env3 /usr/local/bin/python3
```

2. Install the requirements

```sh
$ pip install -r requirements.txt
```

3. Notes: Make sure you have installed mongodb in your system


### Create DB

```sh
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py create_admin
$ python manage.py create_data
```

### Run the Application

```sh
$ python manage.py runserver
```

So access the application at the address [http://localhost:5000/](http://localhost:5000/)

> Want to specify a different port?

> ```sh
> $ python manage.py runserver -h 0.0.0.0 -p 8080
> ```

### Testing

Without coverage:

```sh
$ python manage.py test
```

With coverage:

```sh
$ python manage.py cov
```


