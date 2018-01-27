**Post**
----
Every content (Song, Poem and in future maybe videos) 
is a type of a post. <br />
It has the attributes of it's own and based on type of the content (Song/Poem) 
the content will be filled.

* **URL**

  * **Get All Posts -- Pagination** `/songs/posts`
  * **Get Single Post** `/songs/posts/<post_id>` 
  * **Create a Post** `/songs/posts/`
  * **Get Popular Karaoke - has Pagination** </br> `/song/posts/popular` 
  * **Get New Karaokes - has Pagination** </br> `/song/posts/news`
  * **Get Free Karaokes - has Pagination** </br> `/song/posts/free`
    
  

* **Method:**

  * **Get All Posts -- Pagination** `GET`
   * **Create a Post** `POST`


* **Data Params:**

    To create new post, any of them, you must `POST` below structure.<br/>
    
      {
          "name": "test_post",
          "description": "ha ha ha ha",
          "cover_photo": {"id":<upload id>},
          "type": "song/poem/karaoke",
          "content": {
              <CONTENT BASED ON TYPE>
          },
          "tags": [
              {"name": "#test_tag3"},
              {"name": "#test_tag_4"}
          ],
          "genre": {"id":<genre_id>}
      }
      
    * `content` is described in each models document.
    * `description` | `tags` | `genre` could be null

* **Success Response:**
  
  * **Code:** 200 <br />
    **Content:**
    
        {
            "id": 38,
            "name": "test_post",
            "description": "ha ha ha ha",
            "cover_photo": null,
            "created_date": "2017-11-12T13:58:12.694235Z",
            "type": "song/poem/karaoke",
            "content": {
                <CONTENT BASED ON TYPE>
            },
            "owner": {
                <USER_INFO_DOC>
            },
            "tags": [<TAG OBJECT>],
            "link": "http://127.0.0.1:8000/song/posts/38",
            "like": 0,
            "liked_it": false,
            "is_favorite": false,
            "genre": <Genre Object>,
            "is_premium": True/False
        }
        
    * `owner` is a User object that is serialized
    * `genre` is a genre object that is serialized
    * `tags` is the array of serialized Tag objects
    * `description` | `tags` | `genre` could be null
    