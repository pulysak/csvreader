# csvreader

## Description
Simple project which download csv file every day and write data to db.  

One api point is provided - localhost/product/list  
Which return list of products with pagination interface  
Use 'producer' get param to filter products  
For example - localhost/product/list?producer=McLaughlin-Bosco

## Installation

* Clone project
* Fill in .env file
* docker-compose up

### Example of .env file

```POSTGRES_DB=db_name
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_pass
HOSTNAME=productlist.com
```


### etc

If you want to run updating process manually just do:

1) docker-compose exec back bash
2) Import reader class and start the process

python manage.py shell
```python
from product.reader import ProductReader
ProductReader().update_products()
```

To run test just go into back container and run pytest.
```bash
docker-compose exec back bash
pytest
```
