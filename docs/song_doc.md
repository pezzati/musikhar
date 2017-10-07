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
                "name": "test song",
                "file": {"id":<upload id>},
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
                "cover_photo": {"id":<upload id>},
                "tags": [
                    {"name": "#test_tag3"},
                    {"name": "#test_tag_4"}
                ]
            }
    
    * `poet` | `composer` | `singer` | `owner` are Artist object that are serialized, but only their `id` is essential
    * `genre` is a genre object that is serialized, but only its `id` is essential
    * `related_poem` is a poem object that is serialized, but only its `id` is essential
    * `tags` is the array of serialized Tag objects.
    * Except  `name` |  `file` other attributes could be null

    

* **Success Response:**
  
  * **Code:** 200 <br />
    **Content:** 
    
    Every element of the json serialized Song object has shown below.
    
        {
            "id": 1,
            "owner": <Json serialized User object>,
            "link": <url>,
            "name": "test song",
            "file": {
                "link": <url>,
                "id": <integer>
                },
            "file_url": <url>
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
            "cover_photo": {
                "link": <url>,
                "id": <integer>
                },
            "created_date": "2017-09-05T09:51:10.789845Z",
            "liked_it": true/false,
            "tags": [
                {"name": "#test_tag3"},
                {"name": "#test_tag_4"}
            ],
            "length": "4:39",
            "is_favorite": <True or False boolean>

        }

    * `poet` | `composer` | `singer` are Artist object that are serialized
    * `owner` is a User object that is serialized
    * `genre` is a genre object that is serialized
    * `related_poem` is a poem object that is serialized
    * `tags` is the array of serialized Tag objects.
    * Except `id` | `link` | `name` | `created_date` | `file` | `owner` | `file_url` other attributes might be null
    * `file_url` is the link to download the song file

* **Error Response:**

  * **Code:** 403 UNAUTHORIZED <br />

  OR

  * **Code:** 400 BAD REQUEST <br />