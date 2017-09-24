**Like**
----

 Get an Like's info

* **URL**

 /analysis/like/`

* **Method:**

    * to like a post `POST`
    * to get likes of a post `GET`

*  **URL Params**

   **Required:**

   `id=[integer]`

* **Data Params**
    To like a post

        {
            "post": <obj>,
            "user": <obj>
        }

* **Success Response:**

  * **Get the users that liked a post**  <br />
    **Content:**

        {
            "user":<obj>
        }

* for liking a post *
* **Success Response:**

  * **Code:** 201_CREATED

* **Error Response:**


  * **Code:** 400  <br />
    **Content:** `{"detail": "BAD REQUEST."}`
