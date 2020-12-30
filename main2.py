# main.py
import difflib
import subprocess

import openhtf as htf
from openhtf.plugs import BasePlug
from spintop_openhtf import TestPlan
from tabulate import tabulate

from expected_data import expected_i2c_data

""" Test Plan """

# This defines the name of the testbench.
plan = TestPlan('hello')

voltage_criterion = htf.Measurement("vcc_test").with_dimensions('name', 'value').in_range(3, 6)
voltage2_criterion = htf.Measurement("vdd_test").in_range(3, 6)


class ShellScriptPlug(BasePlug):
    def run(self, shell_script):
        return subprocess.check_output(['sh', shell_script])


names = ["Test1", "VCC", "VDD", "REF", "GND", "GND2", "GND3", "GND4"]


def define_voltage_measurements():
    new_measurements_list = []
    for name in names:
        m = htf.Measurement(name).in_range(3, 5).doc(name + " test").with_units('volt')
        new_measurements_list.append(m)
    return htf.measures(*new_measurements_list)


@plan.testcase('I2C-Test')
# @define_voltage_measurements()
@htf.measures(htf.Measurement('i2c_response'))
@plan.plug(shell_plug=ShellScriptPlug)
def hello_world2(test, shell_plug):
    """Test I2C connections"""
    reference_output = shell_plug.run('./return_matrix.sh')
    output_equal = (expected_i2c_data == str(reference_output))
    if output_equal is not True:
        diff = difflib.ndiff(str(reference_output), expected_i2c_data)
        test.logger.info(''.join(list(diff)))
    test.i2c_response = output_equal


@plan.testcase('Voltage-Test')
@plan.plug(shell_plug=ShellScriptPlug)
def voltage_measurement(test, shell_plug):
    reference_output = shell_plug.run('./return_voltage_table.sh')
    split_data = reference_output.strip().splitlines()
    split_data2 = [x.split() for x in split_data]
    test.logger.info(tabulate(split_data2))


if __name__ == '__main__':
    plan.no_trigger()
    plan.run()
