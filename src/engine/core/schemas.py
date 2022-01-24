from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Product():
    ID: int
    name: str
    sku: str
    barCode: str
    price: int
    priceUSD: int
    discountAmount: int
    qty: 681
    properties: Dict
    offices: Dict
    totalRows: int
    imageUrls: Optional[List] = None



billz_response_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
      "id": {
        "type": "string"
      },
      "jsonrpc": {
        "type": "string"
      },
      "result": {
        "type": "array",
        "items": [
          {
            "type": "object",
            "properties": {
              "ID": {
                "type": "integer"
              },
              "name": {
                "type": "string"
              },
              "sku": {
                "type": "string"
              },
              "barCode": {
                "type": "string"
              },
              "price": {
                "type": "integer"
              },
              "priceUSD": {
                "type": "integer"
              },
              "discountAmount": {
                "type": "integer"
              },
              "qty": {
                "type": "integer"
              },
              "properties": {
                "type": "object",
                "properties": {
                  "BRAND": {
                    "type": "string"
                  },
                  "CATEGORY": {
                    "type": "string"
                  },
                  "COLLECTION": {
                    "type": "string"
                  },
                  "COLOR": {
                    "type": "string"
                  },
                  "DESCRIPTION": {
                    "type": "string"
                  },
                  "GENDER": {
                    "type": "string"
                  },
                  "MODEL_NAME": {
                    "type": "string"
                  },
                  "SEASON": {
                    "type": "string"
                  },
                  "SIZE": {
                    "type": "string"
                  },
                  "SUB_CATEGORY": {
                    "type": "string"
                  },
                  "ИДЕНТИФИКАЦИОННЫЙ_НОМЕР": {
                    "type": "string"
                  },
                  "ПАСПОРТ_НОМЕР": {
                    "type": "string"
                  }
                },
                "required": [
                  "BRAND",
                  "CATEGORY",
                  "COLLECTION",
                  "COLOR",
                  "DESCRIPTION",
                  "GENDER",
                  "MODEL_NAME",
                  "SEASON",
                  "SIZE",
                  "SUB_CATEGORY",
                  "ИДЕНТИФИКАЦИОННЫЙ_НОМЕР",
                  "ПАСПОРТ_НОМЕР"
                ]
              },
              "offices": {
                "type": "array",
                "items": [
                  {
                    "type": "object",
                    "properties": {
                      "officeID": {
                        "type": "integer"
                      },
                      "officeName": {
                        "type": "string"
                      },
                      "price": {
                        "type": "integer"
                      },
                      "priceUSD": {
                        "type": "integer"
                      },
                      "discountAmount": {
                        "type": "integer"
                      },
                      "qty": {
                        "type": "integer"
                      }
                    },
                    "required": [
                      "officeID",
                      "officeName",
                      "price",
                      "priceUSD",
                      "discountAmount",
                      "qty"
                    ]
                  },
                  {
                    "type": "object",
                    "properties": {
                      "officeID": {
                        "type": "integer"
                      },
                      "officeName": {
                        "type": "string"
                      },
                      "price": {
                        "type": "integer"
                      },
                      "priceUSD": {
                        "type": "integer"
                      },
                      "discountAmount": {
                        "type": "integer"
                      },
                      "qty": {
                        "type": "integer"
                      }
                    },
                    "required": [
                      "officeID",
                      "officeName",
                      "price",
                      "priceUSD",
                      "discountAmount",
                      "qty"
                    ]
                  },
                  {
                    "type": "object",
                    "properties": {
                      "officeID": {
                        "type": "integer"
                      },
                      "officeName": {
                        "type": "string"
                      },
                      "price": {
                        "type": "integer"
                      },
                      "priceUSD": {
                        "type": "integer"
                      },
                      "discountAmount": {
                        "type": "integer"
                      },
                      "qty": {
                        "type": "integer"
                      }
                    },
                    "required": [
                      "officeID",
                      "officeName",
                      "price",
                      "priceUSD",
                      "discountAmount",
                      "qty"
                    ]
                  },
                  {
                    "type": "object",
                    "properties": {
                      "officeID": {
                        "type": "integer"
                      },
                      "officeName": {
                        "type": "string"
                      },
                      "price": {
                        "type": "integer"
                      },
                      "priceUSD": {
                        "type": "integer"
                      },
                      "discountAmount": {
                        "type": "integer"
                      },
                      "qty": {
                        "type": "integer"
                      }
                    },
                    "required": [
                      "officeID",
                      "officeName",
                      "price",
                      "priceUSD",
                      "discountAmount",
                      "qty"
                    ]
                  },
                  {
                    "type": "object",
                    "properties": {
                      "officeID": {
                        "type": "integer"
                      },
                      "officeName": {
                        "type": "string"
                      },
                      "price": {
                        "type": "integer"
                      },
                      "priceUSD": {
                        "type": "integer"
                      },
                      "discountAmount": {
                        "type": "integer"
                      },
                      "qty": {
                        "type": "integer"
                      }
                    },
                    "required": [
                      "officeID",
                      "officeName",
                      "price",
                      "priceUSD",
                      "discountAmount",
                      "qty"
                    ]
                  },
                  {
                    "type": "object",
                    "properties": {
                      "officeID": {
                        "type": "integer"
                      },
                      "officeName": {
                        "type": "string"
                      },
                      "price": {
                        "type": "integer"
                      },
                      "priceUSD": {
                        "type": "integer"
                      },
                      "discountAmount": {
                        "type": "integer"
                      },
                      "qty": {
                        "type": "integer"
                      }
                    },
                    "required": [
                      "officeID",
                      "officeName",
                      "price",
                      "priceUSD",
                      "discountAmount",
                      "qty"
                    ]
                  },
                  {
                    "type": "object",
                    "properties": {
                      "officeID": {
                        "type": "integer"
                      },
                      "officeName": {
                        "type": "string"
                      },
                      "price": {
                        "type": "integer"
                      },
                      "priceUSD": {
                        "type": "integer"
                      },
                      "discountAmount": {
                        "type": "integer"
                      },
                      "qty": {
                        "type": "integer"
                      }
                    },
                    "required": [
                      "officeID",
                      "officeName",
                      "price",
                      "priceUSD",
                      "discountAmount",
                      "qty"
                    ]
                  }
                ]
              },
              "imageUrls": {
                "type": "array",
                "items": [
                  {
                    "type": "object",
                    "properties": {
                      "url": {
                        "type": "string"
                      }
                    },
                    "required": [
                      "url"
                    ]
                  }
                ]
              },
              "totalRows": {
                "type": "integer"
              }
            },
            "required": [
              "ID",
              "name",
              "sku",
              "barCode",
              "price",
              "priceUSD",
              "discountAmount",
              "qty",
              "properties",
              "offices",
              "imageUrls",
              "totalRows"
            ]
          }
        ]
      }
    },
    "required": [
      "id",
      "jsonrpc",
      "result"
    ]
  }