### Open Weather Client

[Open Weather API](https://openweathermap.org/history) provides an ability to get weather forecast for given location
and data (current or past).

Current client implementation ```OpenWeatherClient``` contains following methods:
* ```get_history_weather``` - for given location (```lat```, ```lon```) and datetime (```start```, ```end```) return for weather information in json format, which is parsed to ```OpenWeatherResponse``` object.
    
    *Request*:
    ```http request
    http://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start}&end={end}&appid={API key}
    ```
    
    *Response*:
    ```json
      {
       "message":"",
       "cod":"200",
       "city_id":4887398,
       "calctime":0.0863,
       "cnt":4,
       "list":[
       {
          "main":{
             "temp":268.987,
             "temp_min":268.987,
             "temp_max":268.987,
             "pressure":1001.11,
             "sea_level":1024.68,
             "grnd_level":1001.11,
             "humidity":100
          },
          "wind":{
             "speed":5.06,
             "deg":291.002
          },
          "clouds":{
             "all":48
          },
          "weather":[
             {
                "id":802,
                "main":"Clouds",
                "description":"scattered clouds",
                "icon":"03d"
             }
          ],
          "dt":1485703465
       },
       {
          "main":{
             "temp":268.097,
             "temp_min":268.097,
             "temp_max":268.097,
             "pressure":1003.57,
             "sea_level":1027.08,
             "grnd_level":1003.57,
             "humidity":100
          },
          "wind":{
             "speed":8.56,
             "deg":314.007
          },
          "clouds":{
             "all":44
          },
          "weather":[
             {
                "id":802,
                "main":"Clouds",
                "description":"scattered clouds",
                "icon":"03d"
             }
          ],
          "dt":1485730032
       },
       {
          "main":{
             "temp":266.787,
             "temp_min":266.787,
             "temp_max":266.787,
             "pressure":1005.73,
             "sea_level":1029.63,
             "grnd_level":1005.73,
             "humidity":100
          },
          "wind":{
             "speed":6.79,
             "deg":316.012
          },
          "clouds":{
             "all":0
          },
          "weather":[
             {
                "id":800,
                "main":"Clear",
                "description":"Sky is Clear",
                "icon":"01n"
             }
          ],
          "dt":1485755383
       },
       {
          "main":{
             "temp":263.64,
             "pressure":1015,
             "humidity":57,
             "temp_min":262.15,
             "temp_max":265.15
          },
          "wind":{
             "speed":2.6,
             "deg":280
          },
          "clouds":{
             "all":1
          },
          "weather":[
             {
                "id":800,
                "main":"Clear",
                "description":"sky is clear",
                "icon":"01n"
             }
          ],
          "dt":1485780512
       }
       ]
    }
    ```

