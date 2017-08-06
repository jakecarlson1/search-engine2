def build_request(method='empty', data={}):
    request = {
        'method': method,
        'data': data
    }

    return request

def build_response(status=-1, data={}, error_msg=''):
    response = {
        'status': status,
        'data': data,
        'error_msg': error_msg
    }

    return response
