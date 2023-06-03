
from api.v1.product.models import Category
import requests
import time

url = 'https://api.uzum.uz/api/main/root-categories?eco=false'
headers = {
    "authorization": "Basic YjJjLWZyb250OmNsaWVudFNlY3JldA==",
}


res = requests.get(url=url, headers=headers)
res.raise_for_status()
res_json = res.json()['payload']


def save_categories(res_json, parent_id=None):
    for r_json in res_json:
        category = Category(title_uz=r_json['title'], parent_id=parent_id)
        category.save()
        time.sleep(3)
        if r_json.get("children"):
            save_categories(r_json.get("children"), category.id)


def start():
    save_categories(res_json, parent_id=None)
