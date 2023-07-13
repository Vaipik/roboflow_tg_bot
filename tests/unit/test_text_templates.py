from bot.utils.text_templates import roboflow_success_response


def test_success_response(text_for_success_response, success_response):
    list_with_predictions = success_response["predictions"]

    dct = {}
    for item in sorted(
        list_with_predictions, key=lambda x: (len(x["class"]), x["class"])
    ):
        label = item["class"]
        dct[label] = dct.get(label, 0) + 1

    assert text_for_success_response == roboflow_success_response(dct)
