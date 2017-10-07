**Favorite**
----


* **URL**

  * **Get favorite posts of user -- Pagination** `/analysis/favorite`
  * **Favorite a Post and Undo** `/analysis/favorite/post_id/favorite/`

* **Method:**

  * **Get favorite posts of user -- Pagination** `GET`
  * **Favorite a Post** `POST`
  * **Undo** `DELETE`

*  **URL Params**

   **Required:**

   Post id that is integer

* **Success Response:**

  * **Code:** 201_CREATED <br /> Post is liked

  * **Code:** 200 <br />
    Get list of favorite posts <br />
    **Content:**
    
        {
            "user": <User info serialized>,
            "time": "2017-09-05T09:51:10.789845Z",
            "post": <Post serialized>
        }

  * **Code:** 200 <br />
    Undo


* **Error Response:**


  * **Code:** 400  <br />
    **Content:** When given post id is wrong
    
  * **Code:** 405  <br />
    **Content:** Method not allowed
