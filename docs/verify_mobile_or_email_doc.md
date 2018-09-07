**Verify**
----
 After sign up user must verify his phone number Or email address.
    
* **URL**

  * To submit a code `/user/profile/verify/`
  * Resend request `/user/profile/verify?context=<email/mobile>`

* **Method:**
  
  * To submit a code `POST`
  * Resend a code `GET`
  
* **Data Params**

   * To submit a code: </br>
        
         {
            "code": "somecode",
            "udid": <string>,
            "bundle: <string>
         }
         
* **Success Response:**
  
  * **Code:** 200
    **Content:**
      
            {
                "token": <string>, 
                "new_user": False/True
            }
 
* **Error Response:**


  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "Log in" }`

  OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ error : "Email Invalid" }`
