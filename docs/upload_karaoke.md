# Upload Karaoke
  

### **URL**

  `/song/createkaraoke`

### **Method:**
  
  `POST`
  
### **Data Params**

* Send a `form-data` `POST` request with below fields
    
    * `file`: The file that user generated
    * `name`: String
    * `tags`(**OPTIONAL**): send tags seprated with `,`.
        * tag1,#tag2,shaving
    * `desc` (**OPTIONAL**): String
    * `mid`: lyric dict


### **Success Response:**
  
  * **Code:** 201
 
### **Error Response:**
  * **Code:** 400 BAD REQUEST ENTRY <br />
    **Content:** `{ error : "Fill the fields" }`
