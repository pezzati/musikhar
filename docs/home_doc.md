**Home**
----

* **URL**

  `/song/home`

* **Method:**
  
  `GET`
  

* **Success Response:**
  
  * **Code:** 200 <br />
    **Content:** 
    
        [
            {
                "link": "http://127.0.0.1:8000/song/genre/1",
                "files_link": "http://127.0.0.1:8000/song/genre/1/karaokes",
                "name": "پاپ",
                "cover_photo": null,
                "posts": [<Post Array>]
            },
            {
                "link": "http://127.0.0.1:8000/song/genre/3",
                "files_link": "http://127.0.0.1:8000/song/genre/3/karaokes",
                "name": "آذری",
                "cover_photo": null,
                "posts": [<Post Array>]
            },
            {
                "link": "",
                "name": "تازه‌ها",
                "posts": [<Post Array>],
                "files_link": "http://127.0.0.1:8000/song/posts/news/"
            },
            {
                "link": "",
                "name": "محبوب‌ها",
                "posts": [<Post Array>],
                "files_link": "http://127.0.0.1:8000/song/posts/popular/"
            }
        ]
 