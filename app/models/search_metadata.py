"""Centralized search config: area codes, pricing, number types."""

AREA_CODES = {
    '212': 'New York, NY',
    '213': 'Los Angeles, CA',
    '312': 'Chicago, IL',
    '415': 'San Francisco, CA',
    '305': 'Miami, FL',
}

PRICE_TABLE = {
    'US': {'Local': '$1.00', 'TollFree': '$2.00'},
    'CA': {'Local': '$1.20', 'TollFree': '$2.20'},
    'GB': {'Local': '$1.30', 'Mobile': '$1.50', 'TollFree': '$2.50'},
    'AU': {'Local': '$1.40', 'Mobile': '$1.60', 'TollFree': '$2.60'},
}

COUNTRY_NUMBER_TYPES = {
    'US': ['Local', 'TollFree'],
    'CA': ['Local', 'TollFree'],
    'GB': ['Local', 'Mobile', 'TollFree'],
    'AU': ['Local', 'Mobile', 'TollFree'],
}

REGIONS = {
    "US": {
        "name": "United States",
        "region_data": {
            "Alabama": {"code": "AL", "area_codes": [205, 251, 256, 334, 938]},
            "Alaska": {"code": "AK", "area_codes": [907]},
            "Arizona": {"code": "AZ", "area_codes": [480, 520, 602, 623, 928]},
            "Arkansas": {"code": "AR", "area_codes": [479, 501, 870]},
            "California": {"code": "CA", "area_codes": [209, 213, 310, 415, 510, 530, 559, 619, 626, 650, 661, 707, 714, 805, 818, 858, 909, 916, 925, 949]},
            "Colorado": {"code": "CO", "area_codes": [303, 719, 720, 970]},
            "Connecticut": {"code": "CT", "area_codes": [203, 475, 860, 959]},
            "Delaware": {"code": "DE", "area_codes": [302]},
            "Florida": {"code": "FL", "area_codes": [305, 321, 352, 386, 407, 561, 727, 754, 772, 786, 813, 850, 863, 904, 941, 954]},
            "Georgia": {"code": "GA", "area_codes": [229, 404, 470, 478, 678, 706, 762, 770, 912]},
            "Hawaii": {"code": "HI", "area_codes": [808]},
            "Idaho": {"code": "ID", "area_codes": [208, 986]},
            "Illinois": {"code": "IL", "area_codes": [217, 224, 309, 312, 331, 618, 630, 708, 773, 779, 815, 847]},
            "Indiana": {"code": "IN", "area_codes": [219, 260, 317, 463, 574, 765, 812, 930]},
            "Iowa": {"code": "IA", "area_codes": [319, 515, 563, 641, 712]},
            "Kansas": {"code": "KS", "area_codes": [316, 620, 785, 913]},
            "Kentucky": {"code": "KY", "area_codes": [270, 364, 502, 606, 859]},
            "Louisiana": {"code": "LA", "area_codes": [225, 318, 337, 504, 985]},
            "Maine": {"code": "ME", "area_codes": [207]},
            "Maryland": {"code": "MD", "area_codes": [240, 301, 410, 443, 667]},
            "Massachusetts": {"code": "MA", "area_codes": [339, 351, 413, 508, 617, 774, 781, 857, 978]},
            "Michigan": {"code": "MI", "area_codes": [231, 248, 269, 313, 517, 586, 616, 734, 810, 906, 947, 989]},
            "Minnesota": {"code": "MN", "area_codes": [218, 320, 507, 612, 651, 763, 952]},
            "Mississippi": {"code": "MS", "area_codes": [228, 601, 662, 769]},
            "Missouri": {"code": "MO", "area_codes": [314, 417, 573, 636, 660, 816, 975]},
            "Montana": {"code": "MT", "area_codes": [406]},
            "Nebraska": {"code": "NE", "area_codes": [308, 402, 531]},
            "Nevada": {"code": "NV", "area_codes": [702, 725, 775]},
            "New Hampshire": {"code": "NH", "area_codes": [603]},
            "New Jersey": {"code": "NJ", "area_codes": [201, 551, 609, 732, 848, 856, 862, 908, 973]},
            "New Mexico": {"code": "NM", "area_codes": [505, 575]},
            "New York": {"code": "NY", "area_codes": [212, 315, 332, 347, 516, 518, 585, 607, 631, 646, 680, 716, 718, 838, 845, 914, 917, 929]},
            "North Carolina": {"code": "NC", "area_codes": [252, 336, 704, 743, 828, 910, 919, 980, 984]},
            "North Dakota": {"code": "ND", "area_codes": [701]},
            "Ohio": {"code": "OH", "area_codes": [216, 220, 234, 283, 330, 380, 419, 440, 513, 567, 614, 740, 937]},
            "Oklahoma": {"code": "OK", "area_codes": [405, 539, 580, 918]},
            "Oregon": {"code": "OR", "area_codes": [458, 503, 541, 971]},
            "Pennsylvania": {"code": "PA", "area_codes": [215, 223, 267, 272, 412, 445, 484, 570, 582, 610, 717, 724, 814, 878]},
            "Rhode Island": {"code": "RI", "area_codes": [401]},
            "South Carolina": {"code": "SC", "area_codes": [803, 839, 843, 854, 864]},
            "South Dakota": {"code": "SD", "area_codes": [605]},
            "Tennessee": {"code": "TN", "area_codes": [423, 615, 629, 731, 865, 901, 931]},
            "Texas": {"code": "TX", "area_codes": [210, 214, 254, 281, 325, 346, 361, 409, 430, 432, 469, 512, 682, 713, 737, 806, 817, 830, 832, 903, 915, 936, 940, 956, 972, 979]},
            "Utah": {"code": "UT", "area_codes": [385, 435, 801]},
            "Vermont": {"code": "VT", "area_codes": [802]},
            "Virginia": {"code": "VA", "area_codes": [276, 434, 540, 571, 703, 757, 804]},
            "Washington": {"code": "WA", "area_codes": [206, 253, 360, 425, 509]},
            "West Virginia": {"code": "WV", "area_codes": [304, 681]},
            "Wisconsin": {"code": "WI", "area_codes": [262, 274, 414, 534, 608, 715, 920]},
            "Wyoming": {"code": "WY", "area_codes": [307]},
            "Washington DC": {"code": "DC", "area_codes": [202]},
            "Any region (Country-wide)": {"code": None, "area_codes": []}
        }
    },
    "CA": {
        "name": "Canada",
        "region_data": {
            "British Columbia": {"code": "BC", "area_codes": [236, 250, 604, 672, 778]},
            "Alberta": {"code": "AB", "area_codes": [403, 587, 780, 825, 368]},
            "Ontario": {"code": "ON", "area_codes": [226, 289, 343, 416, 519, 613, 647, 705, 807, 905]},
            "Quebec": {"code": "QC", "area_codes": [367, 418, 438, 450, 514, 579, 581, 819, 873]},
            "Yukon": {"code": "YT", "area_codes": [867]},
            "Any region (Country-wide)": {"code": None, "area_codes": []}
        }
    },
    "AU": {
        "name": "Australia",
        "region_data": {
            "New South Wales": {"code": "New South Wales", "area_codes": [612]},
            "Victoria": {"code": "Victoria", "area_codes": [613]},
            "Queensland": {"code": "Queensland", "area_codes": [617]},
            "South Australia": {"code": "South Australia", "area_codes": [618]},
            "Western Australia": {"code": "Western Australia", "area_codes": [618]},
            "Tasmania": {"code": "Tasmania", "area_codes": [613]},
            "Australian Capital Territory": {"code": "New South Wales", "area_codes": [612]},
            "Northern Territory": {"code": "South Australia", "area_codes": [618]},
            "Any region (Country-wide)": {"code": None, "area_codes": []}
        }
    }
}


PRICE_MAP = {
        ("US", "local"): 1.15,
        ("US", "tollfree"): 2.15,
        ("US", "mobile"): 1.15,
        ("GB", "local"): 1.15,
        ("GB", "mobile"): 1.15,
        ("GB", "tollfree"): 2.15,
        ("AU", "local"): 3.00,
        ("AU", "mobile"): 6.50,
        ("AU", "tollfree"): 16.00,
        ("CA", "local"): 1.15,
        ("CA", "tollfree"): 2.15,
    }