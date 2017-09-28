**Favorite**
----


* **URL**

  * **Get favorite posts of user -- Pagination** `/analysis/favorite`
  * **Favorite a Post** `/analysis/favorite/post_id/favorite/`

* **Method:**

  * **Get favorite posts of user -- Pagination** `GET`
  * **Favorite a Post** `POST`

*  **URL Params**

   **Required:**

   Post id that is integer

* **Success Response:**

  * **Code:** 201_CREATED <br /> Post is liked

  * **Code:** 200 <br />
    **Content:**
    
        {
            "user": <User info serialized>,
            "time": "2017-09-05T09:51:10.789845Z",
            "post": <Post serialized>
        }


* **Error Response:**


  * **Code:** 400  <br />
    **Content:** When given post id is wrong
