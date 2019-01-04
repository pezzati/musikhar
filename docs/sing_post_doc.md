**Sing Karaoke**
----

* **URL**

  `/song/posts/<post_id>/sing/`

* **Method:**
  
  `POST`

  
* **Success Response:**
  
  * **Code:** 200 <br />
    **Content:** 
    
            {
                "posts": [
                    {
                        "id": 258,
                        "count": 1
                    },
                    {
                        "id": 12,
                        "count": 3
                    }
                ],
                "coins": 671,
                "days": 12
            }
 
* **Error Response:**

  * **Code:** 400 BAD_REQUEST <br />
    **Content:** 
    
    * happens when post does not exist. Content like Error Doc

  OR

  * **Code:** 402 PAYMENT_REQUIRED <br />
    **Content:**
    
    * Happens does not own the post. Content like Error Doc
