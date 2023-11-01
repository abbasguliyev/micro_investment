from entrepreneur.api.selectors import entrepreneur_form_list

def change_all_entrepreneur_form_is_active_field(old_is_active=True, new_is_active=False):
    return entrepreneur_form_list().filter(is_active=old_is_active).update(is_active=new_is_active)
