**Song**
----

* **URL**

    * **Get List of Songs - has Pagination** </br> `/song/songs`
    * **Get Single Song** </br> `/song/songs/<id>`
    * **Get Popular Songs - has Pagination** </br> `/song/songs/popular`
    * **Get New Songs - has Pagination** </br> `/song/songs/news`
    * **Post new Song** </br> `/song/songs/` 
    * **Search Song -- Pagination** `/song/songs/search`

    
* **Method:**
  
     * get actions `GET`
     * post action `POST`
     
     obvious ha? :))
  
*  **URL Params**

   **Required:** </br>
   To get the single Song object

   `id=[integer]`


* **Data Params**
    
    To create new Song first you must upload file after that you must send below data
    </br>
    
        {
                "file": {"id":<upload id>},
                "poet": {"id": <artist_id>},
                "composer": {"id": <artist_id>},
                "singer": {"id": <artist_id>},
                "related_poem": {"id": <post_id>},
            }
    
    * `poet` | `composer` | `singer` | `owner` are Artist object that are serialized, but only their `id` is essential
    * `related_poem` is a poem post object that is serialized, but only its `id` is essential
    * Except  `file` other attributes could be null

    

* **Success Response:**
  
  * **Code:** 200 <br />
    **Content:** 
    
    Every element of the json serialized Song object has shown below.
    
        {
            "poet": <Artists Object>,
            "composer": <Artists Object>,
            "singer": <Artists Object>,
            "related_poem": <Poem Object>,
            "length": "3:37",
            "file_url": "http://127.0.0.1:8000/song/posts/7/file",
            "link": <some_absolute_url>
        }

    * `file_url` is the link to download the song file

* **Error Response:**

  * **Code:** 403 UNAUTHORIZED <br />

  OR

  * **Code:** 400 BAD REQUEST <br />