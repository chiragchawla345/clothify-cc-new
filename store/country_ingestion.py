from .models import Countries
# from . import Countries
file1 = open("C:\\Users\\DELL\\OneDrive\\Desktop\\Full Stack Web Development\\Django\\Django project\\ecommerce\\clothify\\static\\python\\country.csv", "r")
countries = file1.readlines()
for country in countries:
    c = Countries(country=country)
    c.save()
