**Follow**
----

 Get an Follow's info

* **URL**

 /user/follow/`

* **Method:**

    * a user follows another user `POST`
    * get followers of a user `GET`
    * show the people , who user has followed `GET`
*  **URL Params**

   **Required:**

   `id=[integer]`

* **Data Params**
    To follow a user

        {
            "user": <obj>,
            "user": <obj>
        }

* **Success Response:**
 * **Code:** 201_CREATED

  * **Get followers of a user**  <br />
    **Content:**

        {
            "user":<obj>
        }

  * ** Get the people , who user has followed**  <br />
    **Content:**

        {
            "user":<obj>
        }

* **Success Response:**

  * **Code:** 200_OK

* **Error Response:**


  * **Code:** 400  <br />
    **Content:** `{"detail": "BAD REQUEST."}`
