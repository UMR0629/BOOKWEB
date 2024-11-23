
from database import *

# create_book('Python', 'Guido', 5.0, 6)
# create_book('Java', 'James', 4.0, 4)
# create_book('C++', 'Bjarne', 3.0, 3)
# create_book('C', 'Dennis', 2.0, 2)
book_list = get_top_rated_books_sql()
for i in book_list:
    print(i.title)
book_list_2 = search_book_name('Python')
for i in book_list_2:
    print(i.title)