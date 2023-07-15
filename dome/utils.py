from logging import getLogger
from typing import Final
import serial
import time

from alpaca.telescope import Telescope
from alpaca.exceptions import NotImplementedException


log = getLogger(__name__)
RAW_COMMAND: Final[bool] = True


class SerialDummy:
    """
    Dummy-Class for the case that a serial modul is not there
    """
    def __init__(self, debug):
        self.debug = debug

    def write(self, text):
        log.debug(text)
        self.dummy()

    def open(self):
        self.dummy()

    def close(self):
        self.dummy()

    def dummy(self):
        self.debug.add('Serial Dummy')


class SerialDome:
    ser_light = None

    def __init__(self, debug=None):

        self.debug = debug
        if self.debug is not None:
            self.debug.add('init SerialDome')
        self.connect()

    def connect(self):
        try:
            self.ser_light = serial.Serial()

            self.ser_light.port = 'COM4'
            self.ser_light.baudrate = 19200
            self.ser_light.parity = serial.PARITY_NONE
            self.ser_light.stopbits = serial.STOPBITS_ONE
            self.ser_light.bytesize = serial.EIGHTBITS
            if self.debug is not None:
                self.debug.add('connect SerialDome')
        except NameError as e:
            log.error(e)
            if self.debug is not None:
                self.debug.add('nameerror connect SerialDome')
            self.ser_light = SerialDummy(self.debug)

    def close_connection(self):
        try:
            self.ser_light.close()
            if self.debug is not None:
                self.debug.add('closeConnection SerialDome')
        except NameError as e:
            log.error(e)
            if self.debug is not None:
                self.debug.add('nameerror closeConnection SerialDome')

    def lights_on(self):
        """
        DESCRIPTION
        -----------
        Turns ON the lights in the dome connected via serial port
        """
        try:
            # dome lights ON
            self.ser_light.open()
            # self.ser_light.isOpen()
            self.ser_light.write('SE15\r\n')  # + chr(13))
            time.sleep(.100)
            self.ser_light.write('SO1\r\n')  # + chr(13))
            time.sleep(.100)
            #        self.ser_light.close()

            self.ser_light.close()
            log.info('Dome lights ON.')
        except serial.SerialException:
            pass

    def lights_off(self):
        """
        DESCRIPTION
        -----------
        Turns OFF the lights in the dome connected via serial port
        """
        try:
            # dome lights OFF
            self.ser_light.open()
            # self.ser_light.isOpen()
            self.ser_light.write('SE15\r\n')  # + chr(13))
            time.sleep(.100)
            self.ser_light.write('SO0\r\n')  # + chr(13))
            time.sleep(.100)
            #        self.ser_light.close()

            self.ser_light.close()
            log.info('Dome lights OFF.')
        except serial.SerialException:
            pass

    def humidifier_on(self):
        self.ser_light.open()
        self.ser_light.write('SE15\r\n')  # + chr(13))
        time.sleep(.100)
        self.ser_light.write('SO2\r\n')
        time.sleep(.100)
        self.ser_light.close()


class TcpDome:

    def __init__(self, mount: Telescope):
        self.mount = mount
        self.shutter_status_options = {'0#': 'moving', '1#': 'closed', '2#': 'open'}

    def open_shutter(self):
        """
        DESCRIPTION
        -----------
        Opens the shutter by checking if it is open already or not.
        """
        # self.mount.CommandString('#')
        shutter = self.mount.CommandString(':GDS#', RAW_COMMAND)
        if shutter == '2#':
            log.warning('Shutter is open already.')
        elif shutter == '1#':
            response = self.mount.CommandString(':SDS2#', RAW_COMMAND)
            log.info('Opening shutter.')

            return response
        else:
            log.warning('Shutter is moving.')

        stat = self.mount.CommandString(':GDS#', RAW_COMMAND)
        while stat != '2#':
            stat = self.mount.CommandString(':GDS#', RAW_COMMAND)
        else:
            log.warning('Shutter open.')

    def close_shutter(self):
        """
        DESCRIPTION
        -----------
        Closes the shutter by checking if it is closed already or not.
        """

        # self.mount.CommandString('#')
        shutter = self.mount.CommandString(':GDS#', RAW_COMMAND)
        if shutter == '1#':
            log.warning('Shutter is closed already.')
        elif shutter == '2#':
            response = self.mount.CommandString(':SDS1#', RAW_COMMAND)
            log.info('Closing shutter.')

            return response
        else:
            log.warning('Shutter is moving.')

        stat = self.mount.CommandString(':GDS#', RAW_COMMAND)
        while stat != '1#':
            stat = self.mount.CommandString(':GDS#', RAW_COMMAND)
        else:
            log.info('Shutter closed.')

    def get_shutter_status(self):
        """
        Returns the current status of the shutter. Options are 'open', 'close' and 'moving'
        """
        try:
            shutter = self.mount.CommandString(':GDS#', RAW_COMMAND)
            return self.shutter_status_options[shutter]
        except NotImplementedException as e:
            log.error(e)
            return 'moving'

    def get_az(self):
        """
        DESCRIPTION
        -----------
        Gets the dome azimuth, if a dome is connected.
        Returns:
            XXXX#
            The current azimuth of the dome in tenths of degree from 0 to 3599. In case of error,
            returns 9999#.
        """

        az = self.mount.CommandString(':GDA#', RAW_COMMAND)
        try:
            az = az.split('#')[0]
            try:
                az = float(az) / 10
                az = str("%05.1f" % az) + ' deg'
            except ValueError:
                az = '000.0  deg'
            if az == "9999#":
                log.error("Error. Cannot read the dome azimuth.")
        except AttributeError:
            az = '000.0  deg'

        return az

    def get_homing_status(self):
        """
        DESCRIPTION
        -----------
        Gets the homing operation status on the dome.
        Returns:
            0# no homing operation
            1# homing operation in progress
            2# homing operation completed
        """

        home = self.mount.CommandString(':GDH#', RAW_COMMAND)

        if home == '0#':
            log.warning("No homing operation.")
        elif home == '1#':
            log.info("Homing operation in progress.")
        else:
            log.info("Homing operation completed.")

    def get_slew_status(self):
        """
        DESCRIPTION
        -----------
        Gets the status of the slew operation for the dome. Use this command in place of :D# if
        you want to check if both the telescope and the dome have arrived at target. The result is
        valid only if the dome is under the control of the internal mount logic.
        Returns:
            0# no slew in progress, dome at internally computed target
            1# slew in progress or dome not at internally computed target
        """

        command = self.mount.CommandString(':GDW#', RAW_COMMAND)

        if command == "0#":
            log.warning("No slew in progress, dome at internally computed target.")
        else:
            log.info("Slew in progress or dome not at internally computed target.")

        return command

    def get_slew_status2(self):
        """
        DESCRIPTION
        -----------
        Gets the status of the slew operation for the dome. The result is valid only if the dome is
        under external control via :SDA commands.
        Returns:
            0# no slew in progress, dome at manually set target
            1# slew in progress, dome not at manually set target
        """

        command = self.mount.CommandString(':GDw#', RAW_COMMAND)

        if command == "0#":
            log.warning("No slew in progress, dome at manually set target.")
        else:
            log.info("Slew in progress, dome not at manually set target.")

        return command

    def start_homing(self) -> bool:
        """
        Starts homing on the dome. Note that this command succeeds even if no dome is
        connected. Please use :GDA# or :GDS# to check if a dome is connected.

        :returns: True, if the homing operation started, else False.
        """

        command = self.mount.CommandString(':SDH#', RAW_COMMAND)

        if command == '1':
            log.info("Success.")
            return True
        return False

    def dome_radius(self, x):
        """
        DESCRIPTION
        -----------
        Sets the dome radius to XXXX mm.
        Returns:
            nothing
        """

        radius = str("%04d" % x)

        command = self.mount.CommandString(f':SDR{radius}#', RAW_COMMAND)

        return command

    def set_dome_update_int(self, s):
        """
        DESCRIPTION
        -----------
        Sets the dome update interval to SS seconds (i.e. the dome is commanded to an updated
        position every SS seconds).
        Returns:
            nothing
        """

        second = str("%02d" % s)

        command = self.mount.CommandString(f':SDU{second}', RAW_COMMAND)

        return command

    def slew_dome(self, x):
        """
        DESCRIPTION
        -----------
        Slews the dome to the given azimuth (from 0 to 3600). This overrides the internal logic
        of the mount in order to give direct control of the dome azimuth to the controlling
        program. Setting any dome parameter from the keypad, or any of the following
        commands will give control again to the internal logic of the mount: :SDR, :SDT, :SDU,
        :SDXM, :SDYM, :SDZM, :SDX, :SDY, :SDAr.
        Returns:
            0 invalid (angle out of ammissible range)
            1 valid
        """

        azimuth = str("%04d" % x)

        command = self.mount.CommandString(f':SDA{azimuth}#', RAW_COMMAND)

        if command == 1:
            log.info("Slew done.")
        else:
            log.warning("Invalid azimuth for the dome.")
        return command

    def auto_dome(self):
        """
        DESCRIPTION
        -----------
        Release the dome control to the internal logic of the mount.
        Returns:
            nothing
        """

        command = self.mount.CommandString(':SDAr#', RAW_COMMAND)

        return command
