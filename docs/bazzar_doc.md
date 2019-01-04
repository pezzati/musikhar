# Bazzar Payment

  This document describes the procedure of Cafe Bazzar Payment. <br>
  From the server side view there is Three steps:
  * Get tha **Packages** from server and choose one
  * Send **Purchase** request with the `serial_number` of chosen **Package**
    * `serial_number` of package is Bazzar's `SKU`
  * Send a `post` request to **bazzar_payment** end point with `serial_number` and `purchase_token` that *Bazzar* has given you

## Package List

#### **URL**

  * **Get Package list -- Pagination** `/finance/packages/`

#### **Method:**
  
  `GET`
  
####  **Headers**
    
* `devicetype`
    * `ios` for iOS devices
    * `android` for Android devices 

#### **Data Params**

  <_If making a post request, what should the body payload look like? URL Params rules apply here too._>

#### **Success Response:**
  
  * **Code:** 200 <br />
    **Content:** 
    
        {
            "name": "بسته\u200cی جدید",
            "price": 1000,
            "icon": "http://127.0.0.1:8000/uploads/default_icons/pouya.jpg",
            "serial_number": "206497920410",
            "package_type": "time/coin"
        }
 
#### **Error Response:**

  <_Most endpoints will have many ways they can fail. From unauthorized access, to wrongful parameters etc. All of those should be liste d here. It might seem repetitive, but it helps prevent assumptions from being made where they should be._>

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "Log in" }`

  OR

  * **Code:** 422 UNPROCESSABLE ENTRY <br />
    **Content:** `{ error : "Email Invalid" }`
    
## Purchase

#### **URL**

  *  `/finance/purchase`

#### **Method:**
  
  `POST`
  
#### **Data Params**

    {"serial_number": "testforbazzar"}
    
#### **Success Response:**
  
  * **Code:** 200 <br />
    **Content:** 
    
        {
            "serial_number": "6251218724919990",
            "ref_id": null,
            "state": "in_progress"
        }
    
    * This `serial_number` is Serial of requested purchase not the **package**'s serial number that has sent in request body
 

## Bazzar Payment

#### **URL**

  *  `/finance/bazzar_paymnet/`

#### **Method:**
  
  `POST`
  
#### **Data Params**

    {"serial_number": "6251218724919990", "ref_id": "testrefid"}
    
   * This `serial_number` is Serial of purchase that has given to you in last step

    
#### **Success Response:**
  
  * **Code:** 200 <br />
    **Content:** 
    
        {
            "coins": 126
        }
    
#### Error Response:


|status code |meaning  |
|:------------:|:---------:|
|`400`         |`ref_id` or `serial_number` missing|
|`404`         |Server could not find valid purchase or any purchase at all with given data |
|`406`         |validation with Bazzar failed|
