import pytest


@pytest.fixture()
def success_response():
    return {
        "predictions": [
            {
                "x": 406,
                "y": 96.5,
                "width": 168,
                "height": 149,
                "confidence": 0.982,
                "class": "4672",
            },
            {
                "x": 474,
                "y": 185.5,
                "width": 62,
                "height": 67,
                "confidence": 0.971,
                "class": "76371",
            },
            {
                "x": 369,
                "y": 278,
                "width": 62,
                "height": 64,
                "confidence": 0.964,
                "class": "51409",
            },
            {
                "x": 336.5,
                "y": 172,
                "width": 67,
                "height": 70,
                "confidence": 0.954,
                "class": "3437",
            },
            {
                "x": 247,
                "y": 271.5,
                "width": 62,
                "height": 65,
                "confidence": 0.933,
                "class": "3437",
            },
            {
                "x": 178.5,
                "y": 110.5,
                "width": 207,
                "height": 117,
                "confidence": 0.932,
                "class": "51704",
            },
            {
                "x": 497.5,
                "y": 332.5,
                "width": 69,
                "height": 67,
                "confidence": 0.928,
                "class": "3437",
            },
            {
                "x": 561,
                "y": 254,
                "width": 86,
                "height": 104,
                "confidence": 0.922,
                "class": "65084",
            },
            {
                "x": 506,
                "y": 82.5,
                "width": 66,
                "height": 51,
                "confidence": 0.892,
                "class": "51409",
            },
            {
                "x": 234.5,
                "y": 408,
                "width": 99,
                "height": 118,
                "confidence": 0.829,
                "class": "3011",
            },
            {
                "x": 307,
                "y": 324,
                "width": 104,
                "height": 80,
                "confidence": 0.784,
                "class": "40666",
            },
            {
                "x": 456,
                "y": 291.5,
                "width": 78,
                "height": 87,
                "confidence": 0.766,
                "class": "98252",
            },
            {
                "x": 456,
                "y": 291,
                "width": 78,
                "height": 86,
                "confidence": 0.561,
                "class": "98223",
            },
            {
                "x": 242.5,
                "y": 210,
                "width": 77,
                "height": 78,
                "confidence": 0.518,
                "class": "4890",
            },
        ]
    }


@pytest.fixture()
def unsuccess_response():
    return {"predictions": []}


@pytest.fixture()
def text_for_success_response():
    return """I have following answer according to your request:
Label <b>3011</b>: met <b>1</b> times
Label <b>3437</b>: met <b>3</b> times
Label <b>4672</b>: met <b>1</b> times
Label <b>4890</b>: met <b>1</b> times
Label <b>40666</b>: met <b>1</b> times
Label <b>51409</b>: met <b>2</b> times
Label <b>51704</b>: met <b>1</b> times
Label <b>65084</b>: met <b>1</b> times
Label <b>76371</b>: met <b>1</b> times
Label <b>98223</b>: met <b>1</b> times
Label <b>98252</b>: met <b>1</b> times"""
