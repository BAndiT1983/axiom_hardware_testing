# main.py
import openhtf as htf
from openhtf.plugs.user_input import UserInput
from spintop_openhtf import TestPlan

""" Test Plan """

# This defines the name of the testbench.
plan = TestPlan('hello')

voltage_criterion = htf.Measurement("vcc_test").in_range(3, 6)
voltage2_criterion = htf.Measurement("vdd_test").in_range(3, 6)


@plan.testcase('Hello-Test')
@plan.plug(prompts=UserInput)
def hello_world(test, prompts):
    """Greet user"""
    prompts.prompt('Hello Operator!')
    # test.dut_id = 'hello'  # Manually set the DUT Id to same value every test


@plan.testcase('I2C-Test')
@htf.measures(voltage_criterion, voltage2_criterion)
def hello_world2(test):
    """Test I2C connections"""
    # prompts.prompt('Hello Operator!')
    # test.dut_id = 'hello'  # Manually set the DUT Id to same value every test
    test.measurements.vcc_test = 7
    test.measurements.vdd_test = 4.8


if __name__ == '__main__':
    # plan.no_trigger()
    plan.run()
