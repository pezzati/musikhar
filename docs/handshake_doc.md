**Handshake**
----
Handshake is for check the token and the build version of the application.
</br>
It must called when application opens and at the first.

* **URL**

  `/handshake`

* **Method:**
  
  `POST`
  
*  **URL Params**

   **Optional:**
    If token exists send it in header like other calls :D
   

* **Data Params**

        {
            "build_version": <integer>,
            "device_type": <ios/android>,
            "udid": <string>,
            "one_signal_id": <string>,
            "bundle": <string>
        }
        
    * `one_signal_id` could be null
      
* **Success Response:**
  
  * **Code:** 200 <br />
    **Content:**
    
        {
            "force_update": false,
            "is_token_valid": true,
            "suggest_update": true,
            "url": "http://path.com",
            "update_log": <string>,
            "token": <string>
        }
    
    * `token` can be none. It's not none only if it's a guest user.
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** 
    
        [
            {
                "error": "نوع سیستم عامل دستگاه ناشناخته است"
            }
        ]
