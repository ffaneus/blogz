title_error = 'Need a title'
body_error = 'Need some words'

def valid_title(title):
    if title is None or title == "":
        return False
    else:
        return True

def valid_body(body):
    if body is None or body == "":
        return False
    else:
        return True

def valid_entry(title, body):
    title_error = 'Need a title'
    body_error = 'Need some words'

    new_title = valid_title(title)
    new_body = valid_body(body)

    if new_title and body:
        return True
    elif not new_title and not new_body:
        return [title_error, body_error]
    elif not new_title:
        return title_error
    elif not new_body:
        return body_error