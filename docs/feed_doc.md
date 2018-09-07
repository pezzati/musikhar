**Feed**

* **URL**

  `/song/feeds`

* **Method:**
  
  `GET`
  
* **Success Response:**
  
  * **Code:** 200  With pagination <br />
    **Content:** 
    
        {
            "name": "test-feed",
            "link": "http://127.0.0.1:8000/song/feeds/ea8f809b74dd/karaokes"
        }
  
   *Note* Response of `link` is list of posts with pagination
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />