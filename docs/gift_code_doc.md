# Gift Code
  
### **URL**

  * To validate a **Code** `POST` `/finance/giftcodes/validate/`
  * To Use a **Code** `POST` `/finance/giftcodes/apply/`

### **Method:**
  
  `POST`
  
### **Data Params**

  * `{"code": "code of gift"}` 
### **Success Response:**
  
  * **Code:** 200
 
### **Error Response:**

  Based on Error protocol.

  * **Code:** 400 BAD_REQUEST means Used_Code <br />
    **Content:** `{ error : 'You have already used this code' }`

  OR

  * **Code:** 404 NOT_FOUND ENTRY <br />
    **Content:** `{ error : "INVLIAD Code" }`
