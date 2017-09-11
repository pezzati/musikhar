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
            "gender": 0,
            "birth_date": "2017-09-10T16:28:02Z",
            "image": <url>
            "mobile": "09366626525",
            "email": "peyman@test.ir",
            "bio": "this is a simple bio",
            "first_name": "peyman",
            "last_name": "ezzati",
            "follower_count": 0,
            "following_count": 0,
            "post_count": 39,
            "poems": [<Array of serialized Poems],
            "songs": [<Array of serialized Songs]
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
