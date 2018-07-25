**Karaoke**
----

* **URL**

    * **Get List of Karaokes - has Pagination** </br> `/song/karaokes`
    * **Get Single Karaoke** </br> `/song/karaokes/<id>`
    * **Get Popular Karaoke - has Pagination** </br> `/song/karaokes/popular` 
    * **Get New Karaokes - has Pagination** </br> `/song/karaokes/news`
    * **Get Free Karaokes - has Pagination** </br> `/song/karaokes/free`
    * **Search Karaokes -- Pagination** `/song/karaokes/search`

    
* **Method:**
  
     * get actions `GET`
     
  
*  **URL Params**

   **Required:** </br>
   To get the single Song object

   `id=[integer]`


* **Success Response:**
  
  * **Code:** 200 <br />
    **Content:** 
    
    Every element of the json serialized Song object has shown below.
    
        {
            "artist": <Artist Object>,
            "lyric": <Poem Object>,
            "karaoke_file_url": "http://127.0.0.1:8000/song/posts/43/file",
            "original_file_url": "http://127.0.0.1:8000/song/posts/43/file?target=full",
            "link": "http://127.0.0.1:8000/song/posts/43",
            "length": "3:37",
            "midi": [
                        {
                            "text": "Ú©Ù\u0088Ú\u0086Ù\u0087 Ø®Û\u008cÙ\u0084Û\u008c Ø®Ù\u0088Ø¨Ù\u0087 Ø\u008c Ø®Ù\u0088Ù\u0086Ù\u0087 Ø®Û\u008cÙ\u0084Û\u008c Ø¯Ù\u0088Ø±Ù\u0087\\n",
                            "time": 14.930208333333335
                        },
                        {
                            "text": "Ú©Ø¨Ù\u0088ØªØ±Ù\u0087 Ù\u0085Û\u008c Ø®Ù\u0088Ù\u0086Ù\u0087 Ø\u008c Ø§Ù\u0088Ù\u0086 Ú©Ù\u0087 Ø±Ù\u0088Û\u008c Ø¨Ù\u0088Ù\u0085 Ø®Ù\u0088Ù\u0086Ù\u0087\\n",
                            "time": 18.630208333333336
                        }
                    ]
        }

    * `file_url` is the link to download the song file

* **Error Response:**

  * **Code:** 403 UNAUTHORIZED <br />

  OR

  * **Code:** 400 BAD REQUEST <br />