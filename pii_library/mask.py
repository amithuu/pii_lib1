def mask_data(data, fields_to_mask):
    masked_data = {}

    # Assuming `MASKING_FUNCTIONS` maps masking types to their respective functions
    MASKING_FUNCTIONS = {
        'email_masking': email_mask,
        'mask_last_4': mask_last_4,
        'number_masking': number_mask,
        'gst_masking': gst_mask,
        'address_masking': address_mask,
        'mask_first_4': mask_first_4,  # Default if no masking type is provided
    }

    for field, masking_type in fields_to_mask.items():
        if field in data:
            value = str(data[field]).lower() if data[field] else ''
            if value:  # Proceed with masking only if value is not empty
                mask_function = MASKING_FUNCTIONS.get(masking_type, mask_first_4)
                masked_value = mask_function(value)
                masked_data[field] = masked_value
            else:
                masked_data[field] = ''  # Handle empty or None values by setting empty string
        else:
            masked_data[field] = data[field]  # If field not in data, copy the original value

    return masked_data

def mask_first_4(value):
    if value:
        value = str(value)
        if len(value) > 4:
            masked_value = '*' * 4 + value[4:]
        elif len(value) > 1:
            masked_value = value[0] + '*' * (len(value) - 1)
        else:
            masked_value = '*' * len(value)
        return masked_value
    return value


def mask_last_4(value):
    if value:
        value = str(value)
        if len(value) > 4:
            masked_value = value[:-4] + '*' * 4
        elif len(value) > 1:
            masked_value = value[0] + '*' * (len(value) - 1)
        else:
            masked_value = '*' * len(value)
        return masked_value
    return value


def mask_middle_4(value):
    if value:
        value = str(value)
        length = len(value)
        if length > 8:
            masked_value = value[:4] + '*' * (length - 8) + value[-4:]
        elif length > 4:
            masked_value = value[:2] + '*' * (length - 4) + value[-2:]
        elif length > 2:
            masked_value = value[0] + '*' * (length - 2) + value[-1]
        else:
            masked_value = '*' * len(value)
        return masked_value
    return value


def email_mask(value):
    if value:
        value = str(value)
        try:
            local_part, domain = value.split('@')
            if len(local_part) > 2:
                masked_local = local_part[:2] + '*' * (len(local_part) - 2)
            elif len(local_part) == 2:
                masked_local = local_part[0] + '*'
            else:
                masked_local = '*' * len(local_part)
            return masked_local + '@' + domain
        except ValueError:
            return mask_first_4(value)  # Handle non-email strings
    return value


def number_mask(value):
    if value:
        value = str(value)
        length = len(value)
        if length > 4:
            masked_value = value[:2] + '*' * (length - 4) + value[-2:]
        elif length == 4:
            masked_value = value[0] + '**' + value[-1]
        elif length == 3:
            masked_value = value[0] + '**'
        elif length == 2:
            masked_value = value[0] + '*'
        else:
            masked_value = '*' * len(value)
        return masked_value
    return value


def gst_mask(value):
    if value:
        value = str(value)
        length = len(value)
        if length > 3:
            masked = '*' * min(3, length - 3)
            if length > 6:
                masked += '-'
                masked += '*' * min(2, length - 6)
            if length > 8:
                masked += '-'
            masked += value[-3:]
            masked_value = masked
        elif length == 3:
            masked_value = '**' + value[-1]
        elif length == 2:
            masked_value = '*' + value[-1]
        else:
            masked_value = '*' * len(value)
        return masked_value
    return value


def address_mask(value):
    if value:
        value = str(value)
        names = value.split()
        masked_names = [name[0] + '*' * (len(name) - 1) for name in names]
        masked_value = " ".join(masked_names)
        return masked_value
    return value



# def mask_data(data, fields_to_mask):
#     masked_data = {}
#     # masking_types = {}
#     for field in fields_to_mask:
#         if field in data:
#             value = str(data[field]).lower() if data[field] else ''
#             if value:  # Proceed with masking only if value is not empty
#                 if field == "email":
#                     masked_value = email_mask(value)
#                     # masking_type = 'email_mask'
#                 elif field == "pan":
#                     masked_value = mask_last_4(value)
#                     # masking_type = 'mask_last_4'
#                 elif field == "contact_person_mobile_number":
#                     masked_value = number_mask(value)
#                     # masking_type = 'number_mask'
#                 elif field in ["gst", "tan", "cin"]:
#                     masked_value = gst_mask(value)
#                     # masking_type = 'gst_mask'
#                 elif field in ["contact_person_name", "address1", "address2"]:
#                     masked_value = address_mask(value)
#                     # masking_type = 'address_mask'
#                 else:
#                     masked_value = mask_first_4(value)
#                     masking_type = 'mask_first_4'
#                 masked_data[field] = masked_value
#                 # masking_types[field] = masking_type
#             else:
#                 masked_data[field] = ''  # Handle empty or None values by setting empty string
#                 # masking_types[field] = None  # No masking type for empty values
#         else:
#             masked_data[field] = data[field]  # If field not in data, copy the original value

#     return masked_data #, masking_types
