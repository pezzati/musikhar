**Upload File**
----

* **URL**

  `/media-management/upload/<type>`

* **Method:**
  
  `POST`
  </br> form-data
  
*  **URL Params**

   **Required:**
 
   `type=song/video/cover`


* **Data Params**
    
    `file`

* **Success Response:**
  
  * **Code:** 200 <br />
    **Content:** `{'upload_id': <id>}`
 
* **Error Response:**

  * **Code:** 403 UNAUTHORIZED <br />

  OR

  * **Code:** 400 BAD REQUEST <br />