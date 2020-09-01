from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    category= models.CharField(max_length=50, default="")
    sub_category= models.CharField(max_length=50, default="")
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=300)
    pub_date=models.DateField()
    image= models.ImageField(upload_to="shop/images",default="")

    def __str__(self):
        return self.product_name

class orders(models.Model):
    order_id=models.AutoField(primary_key=True)
    items_json=models.CharField(max_length=5000)
    amount=models.IntegerField(default=0)

    name=models.CharField(max_length=5000)
    email=models.CharField(max_length=110)
    address=models.CharField(max_length=110)
    city=models.CharField(max_length=110)
    phone=models.CharField(max_length=110,default=" ")
    state=models.CharField(max_length=110)
    zip_code=models.CharField(max_length=110)

class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)+" "+self.update_desc[0:7] + "..."

