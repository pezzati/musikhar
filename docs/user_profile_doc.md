**User Profile**
----

To get user's post and profile info 
    
* **URL**

  * **Get Profile** `/user/users/`
  * **Get User's Poems -- Pagination** `/user/users/my_poems`
  * **Get User's Song -- Pagination** `/user/users/my_songs`
  * **Get Others Profile** `/user/users/<username>`
  * **Get Other's Poems -- Pagination** `/user/users/<username>/poems`
  * **Get Other's Songs -- Pagination** `/user/users/<username>/songs`
  * **Search User -- Pagination** `/user/users/search`

* **Method:**
  
  `GET` 
  
*  **URL Params**

   **Required:**
 
   `username=target user's username`

* **Success Response:**
  
  * **Get Profile** 200 <br />
    **Content:** 
    
        {
            "username": "peymanezzati",
            "mobile": "09366626525",
            "email": "peyman@test.ir",
            "first_name": "peyman",
            "last_name": "ezzati",
            "coins": 123,
            "premium_days": 12,
            "avatar": {
                        "link": "http://127.0.0.1:8000/uploads/default_avatars/bored-student.jpg",
                        "id": 1
                       }
        }
  * **Get Poems** 200 <br />
    just like poems array
    
  * **Get Songs** 200 <br />
    just like songs array
  
 
* **Error Response:**


  * **Code:** 403 UNAUTHORIZED <br />
    **Content:** `{ error : "Log in" }`

  OR

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "Email Invalid" }`
