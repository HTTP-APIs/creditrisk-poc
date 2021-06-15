# Making CRUD operations to Creditrisk-poc via POSTMAN

> Please make sure hydrus is up & running.

To check if hydrus is up and running, open Postman and make a GET request to http://localhost:8080/creditrisk_api/. You should see the following response on Postman:
![Screenshot from 2021-06-15 19-00-01](https://user-images.githubusercontent.com/49719371/122061389-16a87400-ce0c-11eb-8f07-0b19896f6e89.png)

## Adding Borrower
 To add a borrower, we need to make a PUT Request to http://localhost:8080/creditrisk_api/Borrower with the following request body.
 ```json
{
    "@type" : "Borrower",
    "TotalAssets" : 10000,
    "LegalEntityIdentifier" : " ",
    "DateOfIncorporation": "2021-06-15-18:00:00"
}
 ```
 ![Screenshot from 2021-06-15 19-11-33](https://user-images.githubusercontent.com/49719371/122063036-8bc87900-ce0d-11eb-83bd-0295d28a1d30.png)

The object was successfully added. To see the object we need to make GET request to `http://localhost:8080/creditrisk_api/Borrower/<object-id>`
  
  ## Modifying Borrower
  To change the Borrower object we need to make POST request to `http://localhost:8080/creditrisk_api/Borrower/<object-id>` Object will be modified with the following request body.
 ```json
{
    "@type" : "Borrower",
    "TotalAssets" : 50000,
    "LegalEntityIdentifier" : " ",
    "DateOfIncorporation": "2021-06-15-18:00:00"
}
 ```
 
 
 ## Adding Loan
  For creating loan object we will need the borrower object-id as FOREIGN KEY for Loan class.
  we need to make PUT request to http://localhost:8080/creditrisk_api/Loan , with the following request body.
  ```json
  {
    "@type" : "Loan",
    "CounterpartyId" : "0f55898b-6a70-4c9c-aeba-92e603dcfb3a",
    "TotalBalance" : 50000,
    "ChannelOfOrigination": "[]"
}
```
![Screenshot from 2021-06-15 19-27-05](https://user-images.githubusercontent.com/49719371/122065605-b4ea0900-ce0f-11eb-9242-176c61146cfe.png)

## Creating Borrower Collection
For adding Borrower collection we need to make the PUT request to http://localhost:8080/creditrisk_api/Borrowers , add the borrower with the following request body.
```json
{
    "@type" : "Borrowers",
    "members" : [
        {
            "@id" : "http://localhost:8080/creditrisk_api/Borrower/0f55898b-6a70-4c9c-aeba-92e603dcfb3a",
            "@type": "Borrower"
        }
    ]
}
```
![Screenshot from 2021-06-15 19-39-27](https://user-images.githubusercontent.com/49719371/122067719-6fc6d680-ce11-11eb-9b39-71637a352e05.png)

## Get Collection
To retrive a collection we need to make GET request to `http://localhost:8080/creditrisk_api/Borrowers/collection-id`
![Screenshot from 2021-06-15 19-43-30](https://user-images.githubusercontent.com/49719371/122068413-0398a280-ce12-11eb-91fc-0e4b6a1d3b5f.png)

## Deleting Class Instances and Collection Instances
To delete a resource make a DELETE operation on the http://localhost:8080/creditrisk/Loan/<resource-id>. Similarly to delete a collection, make DELETE operation to http://localhost:8080/api/Borrowers/<collection-id>.
