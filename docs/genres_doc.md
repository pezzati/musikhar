**Genre**
----
Get info of genres

* **URL**

 * **Get All Root Genres -- Pagination** `/song/genre/`
 * **Get The Genre** `/song/genre/<id>`
 * **Get The Genre's Songs -- Pagination** `/song/genre/<id>/songs`

    
* **Method:**
  
  `GET`
  
*  **URL Params**

   **Required:**
 
   `id=[integer]`


* **Success Response:**
  
  * **Genre's object** <br />
    **Content:** 
    
        {
            "link": "http://127.0.0.1:8000/song/genre/1",
            "files_link": "http://127.0.0.1:8000/song/genre/1/songs",
            "name": "new-genre-test3",
            "children": [
                {
                    "link": "http://127.0.0.1:8000/song/genre/3",
                    "files_link": "http://127.0.0.1:8000/song/genre/3/songs",
                    "name": "new-genre2"
                },
                {
                    "link": "http://127.0.0.1:8000/song/genre/4",
                    "files_link": "http://127.0.0.1:8000/song/genre/4/songs",
                    "name": "new-genre3"
                }
            ]
        }
        
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{"detail": "Not found."}`

  OR

  * **Code:** 403 FORBIDDEN <br />
    **Content:** `{"error": "forbiden"}`