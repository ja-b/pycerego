import json
import requests
from pycerego.core.mappings import language_code

__author__ = 'jacob'


def _root_call(method, endpoint, cerego_misc, params={}, response_type="text"):

    response = ""
    headers = _get_header_from_misc(cerego_misc)
    if method == "GET":
        response = requests.get(cerego_misc.host + endpoint, params=params, headers=headers)
    elif method == "POST":
        response = requests.post(cerego_misc.host + endpoint, data=params, headers=headers)

    if response_type == "text":
        return response.text
    elif response_type == "json":
        return response.json()['response']
    elif response_type == "binary":
        return response.content

def _get_profile(cerego_misc):

    return _root_call("GET", "my/profile", cerego_misc=cerego_misc, response_type="json")

def _get_set(cerego_misc, set_id):

    return _root_call("GET", "sets/" + set_id, cerego_misc=cerego_misc, response_type="json")

def _get_items_in_set(cerego_misc, set_id):

    return _root_call("GET", "sets/" + set_id + "/items", cerego_misc=cerego_misc, response_type="json")

def _get_series_index(cerego_misc):

    return _root_call("GET", "my/series/", cerego_misc=cerego_misc, response_type="json")

def _create_set(cerego_misc, name, lang):

    params = {"name": name, "language_id": _get_lang_id(lang)}
    return _root_call("POST", "sets", cerego_misc=cerego_misc, response_type="json", params=params)

def _create_set_concept(cerego_misc, set_id, params):

    return _root_call("POST", "sets/" + set_id + "/concepts", cerego_misc=cerego_misc, response_type="json", params=params)

def _create_set_item(cerego_misc, set_id, concept_id):

    params = {"association_collection[concept_id]": concept_id}
    return _root_call("POST", "sets/" + set_id + "/items", cerego_misc=cerego_misc, response_type="json", params=params)

def _create_set_facet(cerego_misc, item_id, set_id, association_concept_id):

    params = {"set_id": set_id, "concept_id": association_concept_id}
    return _root_call("POST", "items/" + str(item_id) + "/facets", cerego_misc=cerego_misc, response_type="json", params=params)

def _createImage():

    pass

def _get_header_from_misc(misc):

    headers = {"Authorization": "Bearer " + misc.token}
    return headers

def _get_lang_id(lang_name):

    return language_code[lang_name]