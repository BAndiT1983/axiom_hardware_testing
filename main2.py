# main.py
import subprocess
from tabulate import tabulate

import openhtf as htf
from openhtf.plugs import BasePlug
from spintop_openhtf import TestPlan

""" Test Plan """

# This defines the name of the testbench.
plan = TestPlan('hello')

voltage_criterion = htf.Measurement("vcc_test").with_dimensions('name', 'value').in_range(3, 6)
voltage2_criterion = htf.Measurement("vdd_test").in_range(3, 6)


class ShellScriptPlug(BasePlug):
    def run(self, shell_script):
        return subprocess.check_output(['sh', shell_script])


# @plan.testcase('Hello-Test')
# @plan.plug(prompts=UserInput)
# def hello_world(test, prompts):
#    """Greet user"""
#    prompts.prompt('Hello Operator!')
# test.dut_id = 'hello'  # Manually set the DUT Id to same value every test


names = ["Test1", "VCC", "VDD", "REF", "GND", "GND2", "GND3", "GND4"]


def define_voltage_measurements():
    new_measurements_list = []
    for name in names:
        # m_name = sub_dict['Signal_Name']  # One of the signal names is 'V_3P3'
        # m_min = sub_dict['Min_Value']
        # m_max = sub_dict['Max_Value']
        # m_doc = sub_dict['Info']
        m = htf.Measurement(name).in_range(3, 5).doc(name + " test").with_units('volt')
        new_measurements_list.append(m)
    return htf.measures(*new_measurements_list)


# @plan.testcase('I2C-Test')
@define_voltage_measurements()
def hello_world2(test):
    """Test I2C connections"""
    value = 8
    for i in range(8):
        test.measurements[names[i]] = i


@plan.testcase('Voltage-Test')
@plan.plug(shell_plug=ShellScriptPlug)
def voltage_measurement(test, shell_plug):
    reference_output = shell_plug.run('./return_voltage_table.sh')
    split_data = reference_output.strip().splitlines()
    split_data2 = [x.split() for x in split_data]
    test.logger.info(tabulate(split_data2))


# @plan.testcase('Voltage-Test')
# @htf.measures(
#         htf.Measurement('power_time_series').with_dimensions('ms', 'V', 'A'))
# @htf.measures(htf.Measurement('average_voltage').with_units('V'))
# @htf.measures(htf.Measurement('average_current').with_units('A'))
# @htf.measures(htf.Measurement('resistance').with_units('ohm').in_range(9, 11))
# def multdim_measurements(test):
#     """Phase with a multidimensional measurement."""
#     # Create some fake current and voltage over time data
#     for t in range(10):
#         resistance = 10
#         voltage = 10 + 10.0 * t
#         current = voltage / resistance + .01 * random.random()
#         dimensions = (t, voltage, current)
#         test.measurements['power_time_series'][dimensions] = 0
#
#     # When accessing your multi-dim measurement a DimensionedMeasuredValue
#     # is returned.
#     dim_measured_value = test.measurements['power_time_series']
#
#     # Let's convert that to a pandas dataframe
#     power_df = dim_measured_value.to_dataframe(columns=['ms', 'V', 'A', 'n/a'])
#     test.logger.info('This is what a dataframe looks like:\n%s', power_df)
#     test.measurements['average_voltage'] = power_df['V'].mean()
#
#     # We can convert the dataframe to a numpy array as well
#     power_array = power_df.values
#     test.logger.info('This is the same data in a numpy array:\n%s', power_array)
#     test.measurements['average_current'] = power_array.mean(axis=0)[2]
#
#     # Finally, let's estimate the resistance
#     test.measurements['resistance'] = (
#             test.measurements['average_voltage'] /
#             test.measurements['average_current'])


if __name__ == '__main__':
    # plan.no_trigger()
    plan.run()
    # p = subprocess.Popen(['sh', './return_voltage_table.sh'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # reference_output, err = p.communicate(b"input data that is passed to subprocess' stdin")

    # reference_output = subprocess.check_output(['sh', './return_voltage_table.sh'])
    # split_data = reference_output.strip().splitlines()
    # split_data2 = [x.split() for x in split_data]
    # print(split_data2)
