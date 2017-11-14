**Poem**
----

* **URL**

    * **Get List of Poems - has Pagination** </br> `/song/poems`
    * **Get Single Poem** </br> `/song/poems/<id>`
    * **Get Popular Poems - has Pagination** </br> `/song/poems/popular`
    * **Get New Poems - has Pagination** </br> `/song/poems/news`
    * **Post new Poem** </br> `/song/poems/` 
    * **Search Poem -- Pagination** `/song/poems/search`

    
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
            "poet": {"id": <artist_id>},
            "text": "lalalalalalalalal \n slalskam ",
        }
    
  * `poet` is an Artist object that are serialized, but only its `id` is essential
  * `poet` could be null

    

* **Success Response:**
  
  * **Code:** 200 <br />
    **Content:** 
    
    Every element of the json serialized Poem object has shown below.
    
        {
            "poet": <Artist Object>,
            "text": "la la la la la la \n na na na na",
            "link": <some_absolute_url>
        }
    
* **Error Response:**

  * **Code:** 403 UNAUTHORIZED <br />

  OR

  * **Code:** 400 BAD REQUEST <br />