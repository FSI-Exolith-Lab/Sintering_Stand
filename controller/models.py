"""

models.py

Definitions of classes and interfaces for the sintering stand

"""

import enum


class DIRECTION(enum.IntEnum):
    """
    Direction enum for motor control
    """
    LEFT: 0
    RIGHT: 1


class INTERFACE(enum.IntEnum):
    """
    Interface enum for sensor control
    """
    I2C: 0
    UART: 1
    SPI: 2


class Sensor:
    """
    Parent sensor class. Derives sensors from this class.

    == Variables ==

    interface: Interface
        interface that this sensor uses for control

    pins:
        pins (if any) that control this sensor

    == Functions ==

    connect
        attempt to connect to the sensor

    disconnect
        attempt to disconnect from the sensor

    read
        attempt to read data from the sensor

    """

    def __init__(self, interface: INTERFACE, pins: list[int] | None = None):
        """
        Creates a new sensor object.
        :param interface:
            interface that this sensor uses for control
        :param pins:
            pins (if any) that control this sensor
        """
        self.interface = interface

        # check if pins were specified
        if pins is None:
            pins = []

        # set pins to pins
        self.pins = pins

    def connect(self):
        pass

    def disconnect(self):
        pass

    def read(self):
        pass


class LimitSwitch:
    """
    Limit switch class

    == Variables ==

    signal_pin: int
        pin that limit switch signal will be on
    """

    def __init__(self, signal_pin: int):
        """
        Creates a new LimitSwitch object
        :param signal_pin:
            pin that limit switch signal will be on
        """

        self.signal_pin = signal_pin

    def check_limit(self):
        pass


class Motor:
    """
    Motor class. Handles control of individual motors.

    == Variables ==

    dir_pin: int
        what pin is the direction controller for this motor connected to?

    step_pin: int
        what pin is the drive pin of this motor controller connected to?

    steps_per_rotation: float
        how many "steps" are in a 360 degree (full) rotation of the stepper motor?

    default_travel_direction: DIRECTION
        the default direction that this motor spins

    limit_switch: LimitSwitch
        limit switch associated with this motor (if any)

    _axis: Axis | None
        Internal variable for assigned axis reference. Do not assign to.

    == Functions ==

    step -> None

    """

    def __init__(self, dir_pin: int, step_pin: int, steps_per_rotation: float, default_direction: DIRECTION,
                 limit_switch: LimitSwitch = None) -> None:
        """
        Creates a new motor object

        :param dir_pin:
            what pin is the direction controller for this motor connected to?
        :param step_pin:
            what pin is the drive pin of this motor controller connected to?
        :param steps_per_rotation:
            how many "steps" are in a 360 degree (full) rotation of the stepper motor?
        :param default_direction:
            the default direction that this motor spins
        :param limit_switch:
            limit switch associated with this motor (if any)
        """
        # pin information
        self.dir_pin = dir_pin
        self.step_pint = step_pin

        # stepper motor information
        self.steps_per_rotation = steps_per_rotation

        # standard travel direction
        self.default_direction = default_direction

        # associated limit switch
        self.limit_switch: LimitSwitch | None = limit_switch

        # internal variables
        self._axis: Axis | None = None

    def step(self, distance: float) -> None:
        pass


class Axis:
    """
    Axis class. Controls axis movement and maintains list of associated motors.

    == Variables ==

    axis_designation: str
        string representation of the axis this model is associated with (for example, x-axis or y-axis)
    can_home: bool = False
        does this axis have limit switches? (and therefore, is it able to home?)
    min_distance: float = 0
        what is the minimum distance from the motor this axis can travel to?
    max_distance: float = 0
        what is the maximum distance from the motor this axis can travel to?

    current_distance: float
        how far from motor is this axis currently?

    motors: list[Motor]
        list of motors associated with this axis

    == Functions ==

    add_motor -> bool
        attempts a new motor to the axis motor list.

    remove_motor -> bool
        attempts to remove a motor from the axis motor list

    move -> None

    move_to -> None

    """

    def __init__(self, axis_designation: str, can_home: bool = False, min_distance: float = 0,
                 max_distance: float = 0) -> None:
        """
        Creates a new Axis object.

        :param axis_designation:
            string representation of the axis this model is associated with (for example, x-axis or y-axis)
        :param can_home:
            does this axis have limit switches? (and therefore, is it able to home?)
        :param min_distance:
            what is the minimum distance from the motor this axis can travel to?
        :param max_distance:
            what is the maximum distance from the motor this axis can travel to?
        """
        # axis meta data
        self.axis_designation = axis_designation
        self.can_home = can_home

        # distance variables
        self.min_distance = min_distance
        self.max_distance = max_distance
        self.current_distance = 0

        # motor list
        self.motors: list[Motor] = []

    def add_motor(self, motor: Motor) -> bool:
        """
        Attempts a new motor to the axis motor list.
        :param motor:
            Motor to add to axis motor list
        :return:
            True/False representing if the motor was added to the motor list
        """

        # if homing is enabled, motors must have limit switch
        if self.can_home and motor.limit_switch is None:
            raise RuntimeError("Attempted to add a motor without a limit switch to a homing axis.")

        if motor not in self.motors:
            self.motors.append(motor)
            return True

        return False

    def remove_motor(self, motor: Motor) -> bool:
        """
        Attempts to remove a motor from the axis motor list

        :param motor:
            Motor to remove from the motor list
        :return:
            True/Fase representing if the motor was removed from the motor list
        """

        # remove motor
        if motor in self.motors:
            self.motors.remove(motor)

        # ensure motor is not in list
        if motor not in self.motors:
            return True

        return False

    def move(self):
        pass

    def move_to(self):
        pass
