
def method_not_found_response():
    return {
        "status": False,
        "error": "Method not found or not given!"
    }


def lang_not_found():
    return {
        'status': False,
        "error": "Given language not found!"
    }


def exception_error_response(e):
    return {
        "status": False,
        "error": str(e)
    }

