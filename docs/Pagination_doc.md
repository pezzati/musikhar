**Pagintion**
----
 Pagination of this project is implemented by Django Rest Framework Page Number
 Pagination. </br> Not all endpoints has pagination but those who has it
 mentioned in their document.

*  **URL Pattern**

   `/url/or/path?page=<page number>` </br>
   
   * page number is 1 based not Zero based !!! (sorry for that :D)
   * If page number does not exist in url django assume it as 1
   * If page number is wrong django returns 404-HttpResponse

* **Success Response:**
  
    All pagination results are same and they only difference in value of
     `results`, so in other documents we will only describe the content of
     this key (`results`).

  * **Code:** 200 <br />
    **Content:** 
    
        {
            "count": 4,
            "next": <url or null>,
            "previous": <url or null,
            "results": []
        }
    
    * `next` is the absolute urls of the next page that if does not exist
    will be null
    * `previous` is the absolute urls of the previous page that if does not exist
    will be null
* **Error Response:**

    If page number is wrong, smaller or greater than count of objects,
    you will get below response.

  * **Code:** 404 Not Found <br />
    **Content:** 
    
        {
            "detail": "Invalid page."
        }
