from . import lslga_utils
from .db import get_db

class Set:

    def __init__(self, id_string, pretty_string, list_create_func):
        self.id_string = id_string
        self.pretty_string = pretty_string
        self.list_create_func = list_create_func
        self.galaxy_list = self.list_create_func()

set_list = []

def all_list():
    t = lslga_utils.get_t()
    list = [id for id, in_desi in zip(t['LSLGA_ID'], t['IN_DESI']) if in_desi]
    return list

def string_match_list(catalog):
    def inner_function():
        t = lslga_utils.get_t()
        list = [id for id, galaxy, in_desi in zip(t['LSLGA_ID'], t['GALAXY'], t['IN_DESI']) if galaxy[:len(catalog)] == catalog and in_desi]
        return list
    return inner_function

set_list.append(Set('all', '', all_list)) # string_match_list('') would probably work as well
set_list.append(Set('ngc', 'NGC', string_match_list('NGC')))
set_list.append(Set('sdss', 'SDSS', string_match_list('SDSS')))
set_list.append(Set('2mas', '2MASS/2MASX', string_match_list('2MAS'))) # Change to '2MASS' for testing, only matches 4 galaxies

set_dict = {item.id_string : item.pretty_string for item in set_list}

def get_list(id_string):
    for set in set_list:
        if set.id_string == id_string:
            return set.galaxy_list
    return []
    # Returning None on failure might be bad practice

# Not sure this is the best module for this method
def get_inspected(user_id):
    db = get_db()
    inspections = db.execute("SELECT lslga_id FROM inspection WHERE user_id = ?", (user_id,)).fetchall()
    inspections = [row[0] for row in inspections]
    return inspections
