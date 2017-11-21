**Like**
----

 Get an Like's info

* **URL**

  `/songs/post/<post_pk>/like/`

* **Method:**

  * **Get full like's of a Post -- Pagination** `GET`
  * **Like a Post** `POST`
  * **Unlike a Post** `DELETE`

*  **URL Params**

   **Required:**

   Post id that is integer

* **Success Response:**

  * **Code:** 201_CREATED <br /> Post is liked

  * **Code:** 200<br />
    Get list of likes <br />
    **Content:**
    
        {
            "user": <User info serialized>,
            "time": "2017-09-05T09:51:10.789845Z",
            "post": <Post serialized>
        }
  
  * **Code:** 200 <br />
    Unlike a post


* **Error Response:**


  * **Code:** 400  <br />
    **Content:** When given post id is wrong
    
  * **Code:** 405  <br />
    **Content:** Method not allowed
