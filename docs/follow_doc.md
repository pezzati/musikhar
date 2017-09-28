**Follow**
----

* **URL**
    
    * **Get Followers -- Pagination** `/user/follow/followers`
    * **Get Followings -- Pagination** `/user/follow/followings`
    * **Follow a User -- Pagination** `/user/follow/follow/`
    * **Get user's Followers -- Pagination** `/user/follow/followers?user=<username>`
    * **Get users's Followings -- Pagination** `/user/follow/followings?user=<username>`

* **Method:**
    * **Get Followers -- Pagination** `GET`
    * **Get Followings -- Pagination** `GET`
    * **Follow a User -- Pagination** `POST`
    * **Get user's Followers -- Pagination** `GET`
    * **Get users's Followings -- Pagination** `GET`

    
*  **URL Params**

   **Required:**

    * **Get user's Followers -- Pagination** `user=<username>`
    * **Get users's Followings -- Pagination** `user=<username>`

* **Data Params**

    To follow a user

        {
            "followed": <username>
        }

* **Success Response:**

 * **Code:** 200

   * Get Followers or Followings of a user.  <br />
    Content is just like User Info document.


 * **Code:** 201
 
    * Follow the given user successfully finished


* **Error Response:**

  * **Code:** 400  <br />
    **Content:** missing required data
    
  * **Code:** 404  <br />
    **Content:** username not found
    
    
