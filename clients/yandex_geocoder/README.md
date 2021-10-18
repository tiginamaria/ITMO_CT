### Yandex Geocoder Client

[Yandex Geocoder API](https://yandex.com/dev/maps/geocoder/) provides information about GPS location by text address.


Current client implementation ```YandexGeocoderClient``` contains following methods:
* ```get_location_by_address``` - for given address (```address```) return location (```lat```, ```lon```) in json format, which is parsed to ```YandexGeocoderResponse``` object.
    
    *Request*:
    ```http request 
    https://geocode-maps.yandex.ru/1.x/?apikey={API key}&geocode={address}
    ```

    *Response*:
    
    ```json
    {
      "response": {
        "GeoObjectCollection": {
          "metaDataProperty": {
            "GeocoderResponseMetaData": {
              "request": "Sultanahmet Camii \u0130\u00e7 Yollar\u0131",
              "found": "2",
              "results": "10"
            }
          },
          "featureMember": [
            {
              "GeoObject": {
                "metaDataProperty": {
                  "GeocoderMetaData": {
                    "kind": "station",
                    "text": "Turkey, Istanbul, T1, Sultanahmet Tramvay \u0130stasyonu",
                    "precision": "other",
                    "Address": {
                      "country_code": "TR",
                      "formatted": "Istanbul, T1, Sultanahmet Tramvay \u0130stasyonu",
                      "Components": [
                        {
                          "kind": "country",
                          "name": "Turkey"
                        },
                        {
                          "kind": "province",
                          "name": "\u0130stanbul"
                        },
                        {
                          "kind": "locality",
                          "name": "Istanbul"
                        },
                        {
                          "kind": "route",
                          "name": "T1"
                        },
                        {
                          "kind": "station",
                          "name": "Sultanahmet Tramvay \u0130stasyonu"
                        }
                      ]
                    },
                    "AddressDetails": {
                      "Country": {
                        "AddressLine": "Istanbul, T1, Sultanahmet Tramvay \u0130stasyonu",
                        "CountryNameCode": "TR",
                        "CountryName": "Turkey",
                        "AdministrativeArea": {
                          "AdministrativeAreaName": "\u0130stanbul",
                          "Locality": {
                            "LocalityName": "Istanbul",
                            "Thoroughfare": {
                              "ThoroughfareName": "T1",
                              "Premise": {
                                "PremiseName": "Sultanahmet Tramvay \u0130stasyonu"
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                },
                "description": "T1, Istanbul, Turkey",
                "name": "Sultanahmet Tramvay \u0130stasyonu",
                "boundedBy": {
                  "Envelope": {
                    "lowerCorner": "28.967326 41.001841",
                    "upperCorner": "28.983783 41.014307"
                  }
                },
                "Point": {
                  "pos": "28.975555 41.008074"
                }
              }
            },
            {
              "GeoObject": {
                "metaDataProperty": {
                  "GeocoderMetaData": {
                    "kind": "other",
                    "text": "Turkey, \u0130stanbul, Fatih, Sultanahmet Semti",
                    "precision": "other",
                    "Address": {
                      "country_code": "TR",
                      "formatted": "\u0130stanbul, Fatih, Sultanahmet Semti",
                      "Components": [
                        {
                          "kind": "country",
                          "name": "Turkey"
                        },
                        {
                          "kind": "province",
                          "name": "\u0130stanbul"
                        },
                        {
                          "kind": "area",
                          "name": "Fatih"
                        },
                        {
                          "kind": "other",
                          "name": "Sultanahmet Semti"
                        }
                      ]
                    },
                    "AddressDetails": {
                      "Country": {
                        "AddressLine": "\u0130stanbul, Fatih, Sultanahmet Semti",
                        "CountryNameCode": "TR",
                        "CountryName": "Turkey",
                        "AdministrativeArea": {
                          "AdministrativeAreaName": "\u0130stanbul",
                          "SubAdministrativeArea": {
                            "SubAdministrativeAreaName": "Fatih",
                            "Locality": {
                              "Premise": {
                                "PremiseName": "Sultanahmet Semti"
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                },
                "description": "Fatih, \u0130stanbul, Turkey",
                "name": "Sultanahmet Semti",
                "boundedBy": {
                  "Envelope": {
                    "lowerCorner": "28.938921 40.982047",
                    "upperCorner": "29.004804 41.031955"
                  }
                },
                "Point": {
                  "pos": "28.971863 41.007006"
                }
              }
            }
          ]
        }
      }
    }
    ```