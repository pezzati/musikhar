**Get Karaoke**
----

* **URL**

    * **Get List of Karaokes - has Pagination** </br> `/song/karaoke`
    * **Get Single Karaoke** </br> `/song/karaoke/<id>`
    * **Get Popular Karaokes - has Pagination** </br> `/song/karaoke/popular`
    * **Get New Karaokes - has Pagination** </br> `/song/karaoke/news`
    
* **Method:**
  
     `GET`
  
*  **URL Params**

   **Required:** </br>
   For get the single karaoke object

   `id=[integer]`


* **Success Response:**
  
  * **Code:** 200 <br />
    **Content:** 
    
    Every element of the json serialized Karaoke object has shown below.
    
        {
            "link": <url>,
            "name": "Poems",
            "file": <url>,
            "rate": 0,
            "rate_count": 0,
            "cover_photo": <url>,
            "poet": {
                "name": "peyman ezzati",
                "link": <url>,
                "poetried": [],
                "composed": [],
                "singed": []
            },
            "genre": {
                "link": <url>,
                "files_link": <url>,
                "name": "new-genre1"
            },
            "composer": <Json serialized Artist object>,
            "singer": <Json serialized Artist object>,
            "lyrics": [
                {
                    "text": "text1",
                    "start_time": 0,
                    "end_time": 1000
                },
                {
                    "text": "text2",
                    "start_time": 2000,
                    "end_time": 4000
                }
            ]
        }

    * `poet` | `composer` | `singer` are Artist object that are serialized
    * `genre` is a genre object that is serialized

* **Error Response:**

  * **Code:** 403 UNAUTHORIZED <br />
    <!-- **Content:** `{ error : "Log in" }` -->

  OR

  * **Code:** 404 NOT Found <br />
    <!-- **Content:** `{ error : "Email Invalid" }` -->