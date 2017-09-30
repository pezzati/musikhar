**Search only One Model**
----
When you want to search among only One model (Artist, User, Posts, Songs).
<br />
 This search has pagination.
* **URL**

  `some_path/?key=<search key>`
  
  OR
  
  `some_path?key=<search_key>`
  
  OR if model has tags
  
  `some_path/?key=<search_key>&tags[]=tag1&tags[]=tag2&tags=#tag3`

* **Method:**
  
  `GET`
  
*  **URL Params**

   * Required:
     
     `key=[some string]`


* **Success Response:**
  
  * **Code:** 200 <br />
    Content will be just like the target serialized list with Pagination.
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br/>
    When search key is not string or exists.
  
  * **Code:** 501 <br />
    When search for this model hs not implemented yet.


* **Notes:**
  
  Result is in pagination format.