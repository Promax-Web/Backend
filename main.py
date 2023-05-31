from api.v1.product.models import Category
import requests, json
from django.db import transaction


url = 'https://api.uzum.uz/api/main/root-categories?eco=false'

headers = {
    "authorization": "Basic YjJjLWZyb250OmNsaWVudFNlY3JldA=="
}
res = requests.get(url=url, headers=headers)
res_json = json.loads(res.content)['payload']

def save_categories():
    categories_list = []
    for r_json in res_json:
        obj = Category(title_uz=r_json['title'])
        obj.save()
        # categories_list.append(
        #     obj
        # )
        if r_json.get("children"):
            for r_child in r_json['children']:
                obj_child = Category(title_uz=r_child['title'], parent=obj)
                obj_child.save()
                # categories_list.append(
                #     obj_child
                # )
                if r_child.get("children"):
                    for r_child_child in r_child['children']:
                        obj_ch = Category(title_uz=r_child_child['title'], parent=obj_child)
                        obj_ch.save()
                        # categories_list.append(
                        # )
    # with transaction.atomic():
    #     Category.objects.bulk_create(categories_list)

# res_paython = json.dumps(res_json, indent=4)


# with open('categories.json', 'w') as file:
    # file.write(f"{res_paython}")
