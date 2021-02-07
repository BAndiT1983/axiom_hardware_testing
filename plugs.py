import subprocess

from openhtf.plugs import BasePlug
from spintop_openhtf.plugs.iointerface.comport import ComportInterface


class LinuxPlug(ComportInterface):

    def __init__(self, comport, baudrate=115200):
        super().__init__(comport, baudrate)

    def execute_shell(self, filename):
        return self.com_target("sh {}".format(filename), timeout=10, keeplines=0)


class ShellScriptPlug(BasePlug):
    def run(self, shell_script):
        return subprocess.check_output(['sh', shell_script])
