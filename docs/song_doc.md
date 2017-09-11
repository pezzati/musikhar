**Song**
----

* **URL**

    * **Get List of Songs - has Pagination** </br> `/song/songs`
    * **Get Single Song** </br> `/song/songs/<id>`
    * **Get Popular Songs - has Pagination** </br> `/song/songs/popular`
    * **Get New Songs - has Pagination** </br> `/song/songs/news`
    * **Post new Song** </br> `/song/songs/` 
    
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
                "name": "test song",
                "file": <upload id>,
                "poet": {
                    "id": 1,
                    "name": "Poet",
                    "link": <url>,
                    "song_poems": [],
                    "poems": [],
                    "composed": [],
                    "singed": []
                },
                "genre": <Json serialized Genre object>,
                "composer": <Json serialized Artist object>,
                "singer": <Json serialized Artist object>,
                "related_poem": {
                    "id": 2,
                    "name": "test poem",
                    "poet": null,
                    "link": <url>,
                    "text": "lalalalalalalalal",
                    "desc": "test poem desc",
                    "cover_photo": null,
                    "created_date": "2017-09-05T10:32:43.911600Z",
                    "owner": <Json serialized Artist object>
                },
                "description": "test desc",
                "cover_photo": <upload id>
            }
    
    * `poet` | `composer` | `singer` | `owner` are Artist object that are serialized, but only their `id` is essential
    * `genre` is a genre object that is serialized, but only its `id` is essential
    * `related_poem` is a poem object that is serialized, but only its `id` is essential
    * Except  `name` |  `file` other attributes could be null

    

* **Success Response:**
  
  * **Code:** 200 <br />
    **Content:** 
    
    Every element of the json serialized Song object has shown below.
    
        {
            "id": 1,
            "owner": <Json serialized User object>,
            "link": <uld>,
            "name": "test song",
            "file": <url>,
            "like": 1,
            "poet": {
                "id": 1,
                "name": "Poet",
                "link": <url>,
                "song_poems": [],
                "poems": [],
                "composed": [],
                "singed": []
            },
            "genre": <Json serialized Genre object>,
            "composer": <Json serialized Artist object>,
            "singer": <Json serialized Artist object>,
            "related_poem": {
                "id": 2,
                "name": "test poem",
                "poet": null,
                "link": <url>,
                "text": "lalalalalalalalal",
                "desc": "test poem desc",
                "cover_photo": null,
                "created_date": "2017-09-05T10:32:43.911600Z",
                "owner": <Json serialized Artist object>
            },
            "description": "test desc",
            "cover_photo": <url>,
            "created_date": "2017-09-05T09:51:10.789845Z",
            "liked_it": true/false
        }

    * `poet` | `composer` | `singer` are Artist object that are serialized
    * `owner` is a User object that is serialized
    * `genre` is a genre object that is serialized
    * `related_poem` is a poem object that is serialized
    * Except `id` | `link` | `name` | `created_date` | `file` | `owner` other attributes might be null

* **Error Response:**

  * **Code:** 403 UNAUTHORIZED <br />

  OR

  * **Code:** 400 BAD REQUEST <br />