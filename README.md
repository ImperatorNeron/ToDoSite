# **ToDoSite**
The first **Pet Project**.\
Link to author's GitHub: https://github.com/ImperatorNeron

**ToDoSite** is a site that allows you to work on everyday tasks. Functionality allows you to create, edit, delete, mark as completed (or not completed) tasks. There is also the logic of maintaining an account with registration, changing user information and the ability to receive a point for each completed task, which allows anyone to get into the rating. A bonus to this is that the user can view the information of another user who got into the rating table. <br><br>

# Installation

First of all, we create a directory for the project and configure the virtual space. The terminal should look something like this:
```
(python) D:\Проекти\ToDoProject>
```  
For a more detailed explanation of how to create a virtual environment:
[Virtualenv та venv](https://uk.peterfeatherstone.com/505-virtualenv-and-venv-python-virtual-environments-explained)

The next step is to install all necessary packages for proper functioning. In PyCharm, this is done as follows:
```
pip install SOME-PACKAGE-NAME
```
where **SOME-PACKAGE-NAME** is the package name, which is required for the project. More details about project requirements in ***requirements.txt***.
<br>

***Please note, these libraries must be installed first of all!***
<br>

Next, you need to upload the project folder to the directory we created. After that make it **Sources Root**.
The next step is to do migrations that will create a database and the necessary tables to store data. First, we need to go to the desired folder. Then, we should to do the migrations.
This is done like this:

<br>

```
(python) D:\Проекти\test cd todo

(python) D:\Проекти\test\todo>py manage.py migrate

...
```

<br>

Along with this, you need to execute the following command. With this we collect all static files:

<br>

```
(python) D:\Проекти\test\todo>py manage.py collectstatic

138 static files copied to 'D:\Проекти\test\todo\static'.
```

Second last thing we need is .env file. There are some settings configurations. You can create it in main folder where lay files: db.sqlite3, manage.py and etc. You should write 3 constants: SECRET_KEY, DEBUG, ALLOWED_HOSTS.

The last thing that remains is to start the server on the local machine:

```
(python) D:\Проекти\test\todo>py manage.py runserver [port]
```

**Well done!**
<br><br>

## **Contributing**
All bug fixes, improvements and code optimizations are welcome.

<br>

## **License**
The project is allowed to be used for its own purposes in the absence of a patent.
