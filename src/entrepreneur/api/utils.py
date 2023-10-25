from entrepreneur.api.selectors import entrepreneur_form_list

def change_all_entrepreneur_form_is_active_field(old_is_active=False, new_is_active=True):
    entrepreneur_forms = entrepreneur_form_list().filter(is_active=old_is_active).all()
    for ef in entrepreneur_forms:
        ef.is_active = new_is_active
        ef.save()
