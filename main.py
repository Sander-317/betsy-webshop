# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line
import models
from textblob import TextBlob
from rich.traceback import install

install()


def search(term):
    search_term = TextBlob(term)
    terms = [term, search_term.correct()]
    products = models.Product.select()
    search_results = []
    for i in terms:
        [
            search_results.append(product)
            for product in products
            if str(i.lower()) in str(product.name).lower()
            or str(i.lower()) in str(product.description).lower()
        ]
    return set(search_results)
    ...


# search("shirt")
# search("disigner")
# search("verry")


def list_user_products(user_id):
    user_products = models.OwnedProducts.select().where(
        models.OwnedProducts.user_id == user_id
    )
    product_list = []
    [
        product_list.append(models.Product.get(models.Product.id == i))
        for i in user_products
    ]
    return product_list
    ...


# list_user_products(1)
# list_user_products(2)
# list_user_products(3)
# list_user_products(4)
# list_user_products(5)
# list_user_products(6)
# list_user_products(7)
# list_user_products(8)
# list_user_products(9)
# list_user_products(10)


def list_products_per_tag(tag_id):
    query = (
        models.ProductTags.select()
        .where(models.ProductTags.tag_id == tag_id)
        .join(models.Product)
    )
    list_of_product_per_tag = []
    [list_of_product_per_tag.append(i.product) for i in query]
    return list_of_product_per_tag

    # list_per_tag = models.ProductTags.select().where(
    #     models.ProductTags.tag_id == tag_id
    # )
    # list_of_products_per_tag = []
    # [
    #     list_of_products_per_tag.append(
    #         models.Product.get(models.Product.id == i.product_id)
    #     )
    #     for i in list_per_tag
    # ]

    # return list_of_products_per_tag
    ...


# list_products_per_tag(7)
# list_products_per_tag(2)
# list_products_per_tag(5)


def add_product_to_catalog(user_id, product):
    check_if_product_exists = models.Product.select().where(
        models.Product.name == product[0]
    )
    if check_if_product_exists.exists():
        return
    new_product = models.Product.create(
        name=product[0],
        description=product[1],
        price_in_cents=product[2],
        quantity=product[3],
    )

    for i in product[4]:
        current_tags = []
        [current_tags.append(i.name) for i in models.Tag.select(models.Tag.name)]
        if i not in current_tags:
            models.Tag.create(name=i)
        new_product.tag.add(models.Tag.get(models.Tag.name == i).id)

    owner = models.User.get(models.User.id == user_id)
    owner.owned_products.add(models.Product.get(models.Product.name == product[0]))
    owner.save()
    ...


# add_product_to_catalog(
#     1, ["xbox", "best console ever", 10000, 75, ["game_console", "awesome"]]
# )


def update_stock(product_id, new_quantity):
    product = models.Product.get(models.Product.id == product_id)
    product.quantity = new_quantity
    product.save()
    return
    ...


# update_stock(2, 20000)


def purchase_product(product_id, buyer_id, quantity):
    models.Transaction.create(
        buyer=buyer_id,
        product=product_id,
        quantity=quantity,
    )
    product = models.Product.get(models.Product.id == product_id)
    product.quantity = product.quantity - quantity
    product.save()

    ...


# purchase_product(1, 1, 1)
# purchase_product(2, 5, 6)


def remove_product(product_id):
    product = models.Product.get(models.Product.id == product_id)
    product.delete_instance()
    ...


# remove_product(1)
