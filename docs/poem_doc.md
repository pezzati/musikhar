**Poem**
----

* **URL**

    * **Get List of Poems - has Pagination** </br> `/song/poems`
    * **Get Single Poem** </br> `/song/poems/<id>`
    * **Get Popular Poems - has Pagination** </br> `/song/poems/popular`
    * **Get New Poems - has Pagination** </br> `/song/poems/news`
    * **Post new Poem** </br> `/song/poems/` 
    
* **Method:**
  
     * get actions `GET`
     * post action `POST`
     
     obvious ha? :))
  
*  **URL Params**

   **Required:** </br>
   To get the single Poem object

   `id=[integer]`


* **Data Params**
    
    
        {
            "name": "test poem",
            "poet": null,
            "text": "lalalalalalalalal",
            "description": "test poem desc",
            "cover_photo": <upload id>
        }
    
    * `poet` is an Artist object that are serialized, but only its `id` is essential
    * Except  `name` |  `text` other attributes could be null

    

* **Success Response:**
  
  * **Code:** 200 <br />
    **Content:** 
    
    Every element of the json serialized Poem object has shown below.
    
        {
            "id": 2,
            "name": "test poem",
            "poet": <Json serialized Artist object>,
            "link": <url>,
            "text": "lalalalalalalalal",
            "description": "test poem desc",
            "cover_photo": null,
            "created_date": "2017-09-05T10:32:43.911600Z",
            "owner": <Json serialized user object>,
            "liked_it": true/false
        }

    * `poet` is an Artist object that are serialized
    * `owner` is a User object that is serialized
    * Except `id` | `link` | `name` | `created_date` | `text` | `owner` other attributes might be null

* **Error Response:**

  * **Code:** 403 UNAUTHORIZED <br />

  OR

  * **Code:** 400 BAD REQUEST <br />