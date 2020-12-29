import openhtf as htf


# def range_validator(values):
# for value
# return 18 =< value =< 22

def get_criteria(criterion):
    criteria_dict = {
        "voltage_criterion": htf.Measurement('voltage_criterion').with_dimensions('name', 'voltage')#.in_range(3, 6)
    }

    return criteria_dict[criterion]
