**Song**
----

* **URL**

    * **Get List of Songs - has Pagination** </br> `/song/songs`
    * **Get Single Song** </br> `/song/songs/<id>`
    * **Get Popular Songs - has Pagination** </br> `/song/songs/popular`
    * **Get New Songs - has Pagination** </br> `/song/songs/news`
    * **Get Free Songs - has Pagination** </br> `/song/songs/free`
    * **Search Song -- Pagination** `/song/songs/search`

    
* **Method:**
  
     * get actions `GET`
     
  
*  **URL Params**

   **Required:** </br>
   To get the single Song object

   `id=[integer]`


* **Data Params**
    
    To create new Song first you must upload file after that you must 
    send below data in the `content` part of Post structure.
    </br>
    
        {
            "file": {"id":<upload id>},
            "karaoke": {"id": <karaoke_id>}
        }
    
    <!-- * `poet` | `composer` | `singer` | `owner` are Artist object that are serialized, but only their `id` is essential -->
    <!-- * `related_poem` is a poem post object that is serialized, but only its `id` is essential -->
    <!-- * Except  `file` other attributes could be null -->

    

* **Success Response:**
  
  * **Code:** 200 <br />
    **Content:** 
    
    Every element of the json serialized Song object has shown below.
    
        {
            "length": "3:37",
            "file_url": "http://127.0.0.1:8000/song/posts/7/file",
            "link": <some_absolute_url>,
            "karaoke": <Karaoke Object>
        }

    * `file_url` is the link to download the song file

* **Error Response:**

  * **Code:** 403 UNAUTHORIZED <br />

  OR

  * **Code:** 400 BAD REQUEST <br />