
class inputFormApiPara:

    input_form_data_POST_request = {"form_id": {"type": int, "default": -1}}
    input_form_data_POST_response = {"form_id": {"type": int, "default": -1}}

    input_form_data_PUT_request = {"form_id": {"type": int, "default": -1},
                                   "id": {"type": int, "default": -1}}
    input_form_data_PUT_response = {"form_id": {"type": int, "default": -1},
                                    "id": {"type": int, "default": -1}}
    deleteForm_POST_request = {}
    deleteForm_POST_response = {}

    comment_POST_request = {}
    comment_POST_response = {}
    comment_PUT_request = {}
    comment_PUT_response = {}
    comment_DELETE_request = {}
    comment_DELETE_response = {}
