# Upload Song
  

### **URL**

  `/song/create`

### **Method:**
  
  `POST`
  
### **Data Params**

* Send a `form-data` `POST` request with below fields
    
    * `file`: The file that user generated
    * `name`: String
    * `tags`(**OPTIONAL**): send tags seprated with `,`.
        * tag1,#tag2,shaving
    * `desc` (**OPTIONAL**): String
    * `karaoke`: `id` of Karaoke


### **Success Response:**
  
  * **Code:** 201
 
### **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "Object not foun" }`

  OR

  * **Code:** 400 BAD REQUEST ENTRY <br />
    **Content:** `{ error : "Fill the fields" }`
