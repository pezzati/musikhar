**Like**
----

 Get an Like's info

* **URL**

  * **Get full like's of a Post -- Pagination** `/analysis/like/<post_pk>/full`
  * **Like a Post** `/analysis/like/<post_pk>/like/`

* **Method:**

  * **Get full like's of a Post -- Pagination** `GET`
  * **Like a Post** `POST`

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
