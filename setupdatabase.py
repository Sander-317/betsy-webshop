import models
import os
import csv
import random
from rich.traceback import install

install()


def main():
    delete_database()
    setup_data()


# Read csv files
def get_csv_data(file):
    with open(f"csv_data/{file}", "r") as user_csv:
        csv_reader = csv.reader(user_csv, delimiter=",")
        data = []
        for i in csv_reader:
            data.append(i)
        return data


# sets up the data base and fils it with data
def setup_data():
    models.db.connect()
    models.db.create_tables(
        [
            models.Tag,
            models.User,
            models.Product,
            models.ProductTags,
            models.OwnedProducts,
            models.Transaction,
        ]
    )
    # create users
    [
        models.User.create(name=user[0], address=user[1], billing_info=user[2])
        for user in get_csv_data("users.csv")
    ]

    # finds total amount of users
    number_of_users = len(models.User.select())

    # creates the product
    for product in get_csv_data("product.csv"):
        new_product = models.Product.create(
            name=product[0],
            description=product[1],
            price_in_cents=product[2],
            quantity=product[3],
        )
        # creates the tags and checks for duplicates
        for i in product[4].split():
            current_tags = []
            [current_tags.append(i.name) for i in models.Tag.select(models.Tag.name)]
            if i not in current_tags:
                models.Tag.create(name=i)
            new_product.tag.add(models.Tag.get(models.Tag.name == i).id)

        # assings owner to the product
        owner = models.User.get(models.User.id == random.randint(1, number_of_users))
        owner.owned_products.add(models.Product.get(models.Product.name == product[0]))
        owner.save()

    # find total amount of products
    number_of_products = len(models.Product.select())

    # creates some transactions
    for i in range((number_of_users + number_of_products) * 2):
        new_buyer = random.randint(1, number_of_users)
        new_product = random.randint(1, number_of_products)
        bought_quantity = random.randint(1, 5)
        models.Transaction.create(
            buyer=new_buyer,
            product=new_product,
            quantity=bought_quantity,
        )

    # corrects the inventory
    product = models.Product.get(models.Product.id == new_product)
    product.quantity = product.quantity - bought_quantity
    product.save()


# deletes the data base
def delete_database():
    cwd = os.getcwd()
    database_path = os.path.join(cwd, "betsy-database.db")
    if os.path.exists(database_path):
        os.remove(database_path)


if __name__ == "__main__":
    main()
