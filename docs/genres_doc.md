**Genre**
----
Get info of genres

* **URL**

  * **Get All Root Genres -- Pagination** `/song/genre/`
  * **Get The Genre** `/song/genre/<id>`
  * **Get The Genre's Songs -- Pagination** `/song/genre/<id>/songs`
  * **Get The Genre's Karaokes -- Pagination** `/song/genre/<id>/karaokes`
  * **Favorite/Unfavorite Genres and Get Favorite Genres** `/song/genre/favorite/`

* **Method:**
  
  * **Get All Root Genres -- Pagination** `GET`
  * **Get The Genre** `GET`
  * **Get The Genre's Songs -- Pagination** `GET`
  * **Get The Genre's Karaokes -- Pagination** `/song/genre/<id>/karaokes`
  * **Favorite/Unfavorite Genres and Get Favorite Genres** 
  `POST` | `DELETE` | `GET`
  
*  **URL Params**

   **Required:**
 
   `id=[integer]`

* **Data Params:**

  To favorite or delete the favorite:
             
      ["genre1_name", "ژانر دوم"]
    
    
* **Success Response:**
  
  * **Genre's object** <br />
    **Content:** 
    
        {
            "link": "http://127.0.0.1:8000/song/genre/1",
            "files_link": "http://127.0.0.1:8000/song/genre/1/songs",
            "name": "new-genre-test3",
            "cover_photo": <url>,
            "children": [
                {
                    "link": "http://127.0.0.1:8000/song/genre/3",
                    "files_link": "http://127.0.0.1:8000/song/genre/3/songs",
                    "name": "new-genre2",
                    "cover_photo": <url>
                },
                {
                    "link": "http://127.0.0.1:8000/song/genre/4",
                    "files_link": "http://127.0.0.1:8000/song/genre/4/songs",
                    "name": "new-genre3",
                    "cover_photo": <url>
                }
            ]
        }
        
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{"detail": "Not found."}`

  OR

  * **Code:** 403 FORBIDDEN <br />
    **Content:** `{"error": "forbiden"}`