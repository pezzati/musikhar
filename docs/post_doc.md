**Post**
----
Every content (Song, Poem and in future maybe videos) 
is a type of a post. <br />
But it will used only for representation.

* **Serialized Data**
  

  * **Code:** 200 <br />
    **Content:**
    
        {
            "id": 1,
            "name": "test duration",
            "description": null,
            "cover_photo": null,
            "created_date": "2017-09-23T13:34:43.977634Z",
            "type": "song/poem/video",
            "content": {
                "id": 1,
                "owner": <User info serialized>,
                "link": "http://127.0.0.1:8000/song/songs/1",
                "name": "test duration",
                "file": {
                    "link": "http://127.0.0.1:8000/uploads/posts/peyman/songs/2017_9/2017-09-23_01-dudu.mp3",
                    "id": 1
                },
                "like": 1,
                "poet": null,
                "genre": null,
                "composer": null,
                "singer": null,
                "related_poem": null,
                "description": null,
                "cover_photo": null,
                "created_date": "2017-09-23T13:34:43.977634Z",
                "liked_it": true,
                "tags": [],
                "length": "4:39",
                "is_favorite": false
            },
            "owner": <User info serialized>,
            "liked_it": true
        }
 