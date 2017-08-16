**Start up project**

* **Requirements**
    
    * VirtualEnvironment for python 3.6
    * pip for python 3.6
        * You can check with this command <br /> `pip --version`
    * git
    
* **Clone and install packages**

    * Clone the project
    * Create virtualenv
        * not in the git directory
    * Active the virtualenv with below command <br /> `sorce /path_to_venv/bin/activate`
        * in terminal you must always active it in every session
    * Go to project directory and install the libraries with below command <br /> `pip install -r requirements.txt`

* **Initial Data Base**

    * Run this command for creating data base and tables <br /> `./manage.py migrate`
    * Run this command for creating a superuser <br /> `./manage.py createsuperuser`

       