**Artist**
----

 Get an Artist's info 

* **URL**

  * **Get All Artist -- Pagination** `/user/artists/`
  * **Get the Artist** `/user/artist/<id>`
  * **Get all Singed Songs by the Artist -- Pagination** `/user/artist/<id>/full_singer`
  * **Get all Songs that the Artist is the poet -- Pagination** `/user/artist/<id>/full_song_poems`
  * **Get all Poems by the Artist -- Pagination** `/user/artist/<id>/full_poems`
  * **Get all Songs that composed by the Artist -- Pagination** `/user/artist/<id>/full_composed`
  


* **Method:**
  
  `GET`
  
*  **URL Params**

   **Required:**
 
   `id=[integer]`


* **Success Response:**
  
  * **Get All Artist and The Artist**  <br />
    **Content:** 
    
        {
            "id": 1,
            "name": "Jon Renone",
            "link": "http://127.0.0.1:8000/user/artists/1",
            "image": null,
            "song_poems_count": 11,
            "poems_count": 2,
            "composed_count": 1,
            "singed_count": 2
        }
  
  * **All Others are just like their own documentation**
 
* **Error Response:**


  * **Code:** 404 NOT FOUND <br />
    **Content:** `{"detail": "Not found."}`

  OR

  * **Code:** 403 FORBIDDEN <br />
    **Content:** `{"error": "forbiden"}`
