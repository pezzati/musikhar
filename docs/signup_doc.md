**Sign Up**
----
   New user sign up

* **URL**

      /user/signup

* **Method:**
  
   `POST`
  
* **Data Params**

        {
            "username": "new_user",
            "password": "new_userPassword2"
        }

* **Success Response:**
  
  * **Code:** 200 <br />
    **Content:** `{token: <token_key>}`
 
* **Error Response:**

  * **Code:** 403 FORBIDDEN <br />

  OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** 
    
        [
            {
                "error": "رمز ورود وارد نشده است"
            },
            {
                "error": "نام کاربری وارد نشده است"
            }
        ]

* **Sample Call:**

      curl -X POST -H "Content-Type: application/json" -d '{"username":"test_user","password":"123456"}' http://127.0.0.1:8000/user/signup
* **Notes:**
    
    * **Gender?** 16 August by Peyman