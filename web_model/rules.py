from hdcloud.utils import dateutil
from hdcloud.utils.validator import *

common_ruls = {
    "start_date": [Required, Datetime(dateutil.DATE_FORMAT_D)],
    "end_date": [Required, Datetime(dateutil.DATE_FORMAT_D)],
    "data_types": [Required, IsSplitDigit()],
    "day_types": [Required, IsSplitDigit()]
}
province_load = {
    "start_date": [Required, Datetime(dateutil.DATE_FORMAT_D)],
    "end_date": [Required, Datetime(dateutil.DATE_FORMAT_D)],
    "data_types": [Required, IsSplitDigit()],
    "day_types": [Required, IsSplitDigit()]
}
device_substation_ruls = {
    "run_date": [Required, Datetime(dateutil.DATE_FORMAT_D)],
    "data_types": [Required, IsSplitDigit()],
    "dev_types": [Required, InCartesian(["主变", "线路"])]
}
section_constraint_ruls = {
    "run_date": [Required, Datetime(dateutil.DATE_FORMAT_D)],
    "data_types": [Required, IsSplitDigit()]
}
unit_on_off_cap_ruls = {
    "start_date": [Required, Datetime(dateutil.DATE_FORMAT_D)],
    "end_date": [Required, Datetime(dateutil.DATE_FORMAT_D)],
    "data_types": [Required, IsSplitDigit()],
    "unit_types": [Required, In([1, 2, "1", "2"])]
}
unit_on_off_ruls = {
    "start_date": [Required, Datetime(dateutil.DATE_FORMAT_D)],
    "end_date": [Required, Datetime(dateutil.DATE_FORMAT_D)],
    "data_types": [Required, IsSplitDigit()],
    "unit_types": [Required, InCartesian([1, 2])],
    "day_types": [Required, IsSplitDigit()]
}

weather_rules = {
    "prov_id": [Required, Isdigit()],
    "city_id": [Required, Isdigit()],
    "county_id": [Required, Isdigit()],
    "start_date": [Required, Datetime(dateutil.DATE_FORMAT_D)],
    "end_date": [Required, Datetime(dateutil.DATE_FORMAT_D)],
    "data_types": [Required, InCartesian([1, 2])],
    "day_types": [Required, InCartesian([1, 2, 3, 4, 5])]
}

weather_avg_rules = {
    "prov_id": [Required, Isdigit()],
    "start_date": [Required, Datetime(dateutil.DATE_FORMAT_D)],
    "end_date": [Required, Datetime(dateutil.DATE_FORMAT_D)]
}

comparision_rules = {
    "start_date": [Required, Datetime(dateutil.DATE_FORMAT_D)],
    "end_date": [Required, Datetime(dateutil.DATE_FORMAT_D)],
    "data_types": [Required, InCartesian([1, 2])]
}