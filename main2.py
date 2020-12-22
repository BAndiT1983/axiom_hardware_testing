# main.py
import random

import openhtf as htf
from openhtf.plugs.user_input import UserInput
from spintop_openhtf import TestPlan

""" Test Plan """

# This defines the name of the testbench.
plan = TestPlan('hello')

voltage_criterion = htf.Measurement("vcc_test").with_dimensions('name', 'value').in_range(3, 6)
voltage2_criterion = htf.Measurement("vdd_test").in_range(3, 6)


@plan.testcase('Hello-Test')
@plan.plug(prompts=UserInput)
def hello_world(test, prompts):
    """Greet user"""
    prompts.prompt('Hello Operator!')
    # test.dut_id = 'hello'  # Manually set the DUT Id to same value every test


#@plan.testcase('I2C-Test')
@htf.measures(voltage_criterion)
def hello_world2(test):
    """Test I2C connections"""
    # prompts.prompt('Hello Operator!')
    # test.dut_id = 'hello'  # Manually set the DUT Id to same value every test
    test.measurements['vcc_test']['Test1', 3] = 5.1
    test.measurements['vcc_test']['name', 4.8] = 3.8


@plan.testcase('Voltage-Test')
@htf.measures(
        htf.Measurement('power_time_series').with_dimensions('ms', 'V', 'A'))
@htf.measures(htf.Measurement('average_voltage').with_units('V'))
@htf.measures(htf.Measurement('average_current').with_units('A'))
@htf.measures(htf.Measurement('resistance').with_units('ohm').in_range(9, 11))
def multdim_measurements(test):
    """Phase with a multidimensional measurement."""
    # Create some fake current and voltage over time data
    for t in range(10):
        resistance = 10
        voltage = 10 + 10.0 * t
        current = voltage / resistance + .01 * random.random()
        dimensions = (t, voltage, current)
        test.measurements['power_time_series'][dimensions] = 0

    # When accessing your multi-dim measurement a DimensionedMeasuredValue
    # is returned.
    dim_measured_value = test.measurements['power_time_series']

    # Let's convert that to a pandas dataframe
    power_df = dim_measured_value.to_dataframe(columns=['ms', 'V', 'A', 'n/a'])
    test.logger.info('This is what a dataframe looks like:\n%s', power_df)
    test.measurements['average_voltage'] = power_df['V'].mean()

    # We can convert the dataframe to a numpy array as well
    power_array = power_df.values
    test.logger.info('This is the same data in a numpy array:\n%s', power_array)
    test.measurements['average_current'] = power_array.mean(axis=0)[2]

    # Finally, let's estimate the resistance
    test.measurements['resistance'] = (
            test.measurements['average_voltage'] /
            test.measurements['average_current'])


if __name__ == '__main__':
    # plan.no_trigger()
    plan.run()
