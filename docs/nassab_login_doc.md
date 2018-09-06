**Nassab Login**
----
  <_Additional information about your API call. Try to use verbs that match both request type (fetching vs modifying) and plurality (one vs multiple)._>

* **URL**

  `/user/nassablogin/`

* **Method:**
  
  `POST`
  
* **Data Params**

        {
            "bundle": <string>,
            "udid": <string>,
            "email": email@email.com
        }
        
* **Success Response:**
  
    * **Code:** 200
    **Content:**
      
            {
                "token": <string>, 
                "new_user": False/True
            }
 
* **Error Response:**

  * **Code:** 403 FORBIDDEN <br />