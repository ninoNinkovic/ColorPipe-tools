""" Christophe Lorenz Colour Cube LUT format (extension .cc) helpers

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
import datetime
from utils.abstract_lut_helper import AbstractLUTHelper
import utils.lut_presets as presets
from utils.color_log_helper import print_error_message, print_success_message


class CLCCHelperException(Exception):
    """Module custom exception

    Args:
        Exception

    """
    pass


class CLCCHelper(AbstractLUTHelper):
    """ Clcc Helper

    """
    @staticmethod
    def get_default_preset():
        return {
                presets.TYPE: "3D",
                presets.EXT: '.cc',
                presets.IN_RANGE: [0.0, 1.0],
                presets.OUT_RANGE: [0.0, 1.0],
                presets.CUBE_SIZE: 32,
                presets.TITLE: "Christophe Lorenz CC LUT",
                presets.COMMENT: ("Generated by ColorPipe-tools, clcc_helper "
                                 "{0}").format(__version__),
                presets.VERSION: "1"
                }

    @staticmethod
    def get_header(preset):
        """Return clcc header

        Args:
            preset (dict): preset

        """
        header = ("Colour Cube data {4}\n"
                  "{4}\n\n"
                  "Name\n"
                  "{0}\n"
                  "Description\n"
                  "{1}\n"
                  "Input Colour space - RGB=1, CIEXYZ=2, DENSITY=3\n"
                  "1\n"
                  "Output Colour space - RGB=1, CIEXYZ=2, DENSITY=3\n"
                  "1\n"
                  "Size x,y,z\n"
                  "{2},{2},{2}\n"
                  "Name component A\n"
                  "component A\n"
                  "Name component B\n"
                  "component B\n"
                  "Name component C\n"
                  "component C\n"
                  "Creation Date\n"
                  "{3}\n"
                  "Data\n"
                  ).format(preset[presets.TITLE],
                           preset[presets.COMMENT],
                           preset[presets.CUBE_SIZE],
                           datetime.datetime.now(),
                           preset[presets.VERSION]
                           )
        return header

    def _write_1d_2d_lut(self, process_function, file_path, preset,
                         line_function):
        message = "1D/2D  LUT is not supported in 3DL format"
        print_error_message(message)
        raise CLCCHelperException(message)

    @staticmethod
    def _get_pattern(preset):
        return "{0:.6f},{1:.6f},{2:.6f}\n"

    def write_3d_lut(self, process_function, file_path, preset):
        data = self._get_3d_data(process_function, preset)[1]
        # Test output range
        self._check_output_range(preset)
        lutfile = open(file_path, 'w+')
        lutfile.write(self.get_header(preset))
        # data
        for rgb in data:
            lutfile.write(self._get_rgb_value_line(preset, rgb))
        lutfile.close()
        print_success_message(self.get_export_message(file_path))

    @staticmethod
    def _get_range_message(output_range):
        """ Get range warning/error message

        Returns:
            .str

        """
        return ("Cl CC output range is expected to be float."
                "Ex: [0.0, 1.0].\nYour range {0}"
                ).format(output_range)

    def _check_output_range(self, preset):
        """ Check output range. Cube LUT are float.
        Print a warning or raise an error

        """
        output_range = preset[presets.OUT_RANGE]
        presets.check_range_is_float(output_range,
                                     self._get_range_message(output_range))

    def _validate_preset(self, preset, mode=presets.RAISE_MODE,
                         default_preset=None):
        default_preset = self.get_default_preset()
        # type must be 3D, there's no 1d/2d cc
        if presets.TYPE in preset and not preset[presets.TYPE] == '3D':
            if mode == presets.RAISE_MODE:
                raise CLCCHelperException(("'{0}' is not a valid type for 3dl "
                                           "LUT. Choose '3D'"
                                           ).format(preset[presets.TYPE]))
            preset[presets.TYPE] = default_preset[presets.TYPE]
        # check basic arguments
        return AbstractLUTHelper._validate_preset(self, preset, mode,
                                                  default_preset)

CLCC_HELPER = CLCCHelper()
