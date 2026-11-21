import os
from dotenv import load_dotenv

load_dotenv()
YANDEX_API_KEY = os.getenv("API_KEY", "")

HTML_CODE = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>FishSpot Map</title>

    <script
        src="https://api-maps.yandex.ru/2.1/?apikey={YANDEX_API_KEY}&lang=ru_RU"
        type="text/javascript">
    </script>

    <style>
        html, body {{
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }}

        #map {{
            width: 100%;
            height: 100%;
        }}
    </style>
</head>

<body>

<div id="map"></div>

<script>
    window.myMap = null;
    window.mapReady = false;
    window.pendingLocation = null;

    ymaps.ready(function () {{

        window.myMap = new ymaps.Map("map", {{
            center: [59.4370, 24.7536],
            zoom: 10,
            controls: [
                'zoomControl',
                'fullscreenControl',
                'typeSelector'
            ]
        }});

        window.mapReady = true;

        console.log("карта загружена");

        if (window.pendingLocation !== null) {{
            window.showWaterbody(
                window.pendingLocation.latitude,
                window.pendingLocation.longitude,
                window.pendingLocation.name
            );

            window.pendingLocation = null;
        }}
    }});


    window.showWaterbody = function(latitude, longitude, name) {{

        latitude = Number(latitude);
        longitude = Number(longitude);

        if (!Number.isFinite(latitude) ||
            !Number.isFinite(longitude)) {{
            console.error("неправильные координаты");
            return;
        }}

        if (!window.mapReady || !window.myMap) {{
            window.pendingLocation = {{
                latitude: latitude,
                longitude: longitude,
                name: name || "Водоём"
            }};
            return;
        }}

        var coordinates = [latitude, longitude];

        window.myMap.geoObjects.removeAll();

        var placemark = new ymaps.Placemark(
            coordinates,
            {{
                balloonContent: '<b>' + String(name || "Водоём") + '</b>',
                hintContent: String(name || "Водоём")
            }},
            {{
                preset: 'islands#redIcon'
            }}
        );

        window.myMap.geoObjects.add(placemark);

        window.myMap.setCenter(coordinates, 13);

        placemark.balloon.open();

        console.log("FishSpot: водоём отображён");
    }};

</script>

</body>
</html>
"""
