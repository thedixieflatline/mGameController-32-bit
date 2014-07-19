"""
mGameController 0.5
GitHub Page: https://github.com/thedixieflatline/mGameController
mGameController an app for the game Assetto Corsa.
Provides the ability to get control inputs from game devices in Assetto Corsa
App developed by David Trenear

Please submit bugs or requests to the Assetto Corsa forum
http://www.assettocorsa.net/forum/index.php

You will need to use the Pygame I have supplied in the source as it is compiled to run in Python 3.3

To activate copy mGameController folder to C:\Program Files (x86)\Steam\steamapps\common\assettocorsa\apps\python

This app is more of a tutorial on how to do this. I have developed this for something I am working on in my own Assetto Corsa apps.
I thought other app developers would appreciate knowing how to do this and perhaps even use the technique.
I will continue to develop this into a more generic class to handle a lot of this so developers can just plug and go on more easily integrate it into their own work if they wish.
If there is a lot of interest I might even look at adding in serial device support in the future
This code is setup to be a demo and also I have combined some logic together rather than split it all up to make it easier to read
Also some of the processing in the main loop could be moved out and some vales stored on start up and not updated every frame
Again this was for readability and to make it easier to follow as well as to show beginners how to handle the inputs and how to scan for and work changes to capabilities of using different devices

I have commented throughout but the best place to start the tutorial from is the acUpdate function near the bottom
First read the comments in acUpdate that explain the 2 ways to get inputs and the pros and cons and features of each method
Then go and look at the 2 different class descriptions. Start with class GameController and then read class DisplayClass
Take note of what happens when each class is initialized and the secondary init of DisplayClass
DisplayClass also contains the 2 functions that run the program and do all of the work.

Here I have put the Pygame object method calls for convenience but you can check out the full docs here

Pygame docs online here http://www.pygame.org/docs/

Possible joystick event types: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
    JOYAXISMOTION    joy, axis, value
    JOYBALLMOTION    joy, ball, rel
    JOYHATMOTION     joy, hat, value
    JOYBUTTONUP      joy, button
    JOYBUTTONDOWN    joy, button

Top level joystick class methods
    pygame.joystick.init	—	Initialize the joystick module.
    pygame.joystick.quit	—	Uninitialize the joystick module.
    pygame.joystick.get_init	—	Returns True if the joystick module is initialized.
    pygame.joystick.get_count	—	Returns the number of joysticks.

joystick object instance methods
    pygame.joystick.Joystick.init	—	initialize the Joystick
    pygame.joystick.Joystick.quit	—	uninitialize the Joystick
    pygame.joystick.Joystick.get_init	—	check if the Joystick is initialized
    pygame.joystick.Joystick.get_id	—	get the Joystick ID
    pygame.joystick.Joystick.get_name	—	get the Joystick system name
    pygame.joystick.Joystick.get_numaxes	—	get the number of axes on a Joystick
    pygame.joystick.Joystick.get_axis	—	get the current position of an axis
    pygame.joystick.Joystick.get_numballs	—	get the number of trackballs on a Joystick
    pygame.joystick.Joystick.get_ball	—	get the relative position of a trackball
    pygame.joystick.Joystick.get_numbuttons	—	get the number of buttons on a Joystick
    pygame.joystick.Joystick.get_button	—	get the current button state
    pygame.joystick.Joystick.get_numhats	—	get the number of hat controls on a Joystick
    pygame.joystick.Joystick.get_hat —	get the position of a joystick hat
"""

"""Add Built In Modules"""
import sys
import os
import os.path
"""Add AC Modules"""
import ac
import acsys
"""Add External Modules to Python path"""
sys.path.insert(0, "apps/python/mGameController/pygame")
"""Add External Modules"""
import pygame

def CheckPythonPath():
    """Report Modules on Python path"""
    for d in sys.path:
        ac.console("{0}".format(d))

def CheckTypeOf(thing):
    # CheckTypeOf(configuration.fuelwarninglevel) class instance property or stand alone variable
    # CheckTypeOf(configuration.getFuelWarningLevel()) check function or method return value
    if type(thing) is None:
        ac.console("none")
    if type(thing) is bool:
        ac.console("boolean")
    if type(thing) is str:
        ac.console("string")
    if type(thing) is int:
        ac.console("integer")
    if type(thing) is float:
        ac.console("float")
    if type(thing) is object:
        ac.console("object")
    if type(thing) is staticmethod:
        ac.console("static method")
    if type(thing) is classmethod:
        ac.console("class method")

# I prefer to uses clases rather than vanilla functions and variables as they have a global scope and I do not have to add globals everywhere

class DisplayClass:
    """display elements labels buttons and callback functions """
    def __init__(self):
        self.appWindow = None
        self.device_count_label = None
        self.device_get_id_label = None
        self.device_get_name_label = None
        self.device_get_numaxes_label = None
        self.device_get_axis_label = None
        self.axis_string = ""
        self.device_get_axis_label_1 = None
        self.device_get_axis_label_2 = None
        self.device_get_axis_label_3 = None
        self.device_get_axis_label_4 = None
        self.device_get_axis_label_5 = None
        self.device_get_numballs_label = None
        self.device_get_ball_label = None
        self.device_get_numbuttons_label = None
        self.device_get_button_label = None
        self.device_get_numhats_label = None
        self.device_get_hat_label = None
        self.AppActivated = self.AppActivatedFunction
        self.AppDismissed = self.AppDismissedFunction

    def updateEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                ac.console("Event Type {0}".format(event.type))
                ac.console("Event Details {0}".format(str(event)))
                ac.console("Controller Number {0}".format(event.joy))
                ac.console("Button pressed {0}".format(event.button))
                if (event.dict['button'] == 15):
                    ac.console("You pressed the Top Black Button on a Logitech G25 or 27 Shifter")

    def updateObject(self):
        """Update the number of devices attached on the system"""
        gamedevice.device_count = pygame.joystick.get_count()

        if(gamedevice.device_count != 0 or None):
            """If devices detected then run device
            Update label with the value from the number of devices connected"""
            ac.setText(display.device_count_label, "Total Detected Devices : {0}".format(gamedevice.device_count))

            """now we start to get the vales from the device number one created in setInitialStatus above (instance name is gamedevice.device)
            We can now call the instance methods (listed at the top of this script^^^^) on the device to get values for each of it's properties
            Set labels to show device id gamedevice.device.get_id() and device name gamedevice.device.get_name()
            """
            ac.setText(display.device_get_id_label, "Device ID : {0}".format(gamedevice.device.get_id()))
            ac.setText(display.device_get_name_label, "Device Name : {0}".format(gamedevice.device.get_name()))

            """now we have to scan through the device features as each device will have a different set of buttons axis hats etc
            A lot of this could be done once on startup then just updated by the main loop
            I am doing it all here to make it more readable and easier to understand and the program logic better for beginners
            you could also split out the checking for event logic and display stuff out of the main loop
            into different functions and some of it does not need to be updated in the main loop all the time
            I have not built in support here for multiple keys pressed at the same time although it does work
            I might expand this script later to be more generic and to handle multiple devices at the same time and switch between
            So now I will scan down the available features and values and update the values to the labels and add in a little display logic to make it pretty"""

            """Check to see if there are any buttons, I assume all controllers would have at least one but you never know!"""
            if(gamedevice.device.get_numbuttons() != 0):
                """This where I take the number of reported button presses which we get as a boolean
                and loop over the total to see if I got a key press then print the result to the label and change the label colour
                Not truly supporting multiple keys at once here but first key is still there after the second is released
                You have to use the event method to get a callback for key up AND down so check out that method below if you need that functionality
                First display number of available buttons"""
                ac.setText(display.device_get_numbuttons_label, "Total Buttons : {0}".format(gamedevice.device.get_numbuttons()))

                """Now display which button pressed First draw something if no button is pressed"""
                ac.setText(display.device_get_button_label, "Press or Hold Button")
                ac.setFontColor(display.device_get_button_label, 1.0, 0.0, 0.0, 1)
                """Now in this first example I will use a loop to go over only the number of buttons available and if a button has given a true boolean for being pressed then set the label colour and display which number pressed"""
                for i in range(gamedevice.device.get_numbuttons()):
                    if(gamedevice.device.get_button(i)):
                        ac.setFontColor(display.device_get_button_label, 0.0, 1.0, 0.1, 1)
                        ac.setText(display.device_get_button_label, "Button {0} Pressed".format(i))
            else:
                """Update to this if no buttons detected on device"""
                ac.setText(display.device_get_button_label, "No Buttons Found")
                ac.setFontColor(display.device_get_button_label, 1.0, 0.0, 0.0, 1)

            """Check to see if there are any axis controller"""
            if(gamedevice.device.get_numaxes() != 0):
                """Update label with number of axis detected"""
                ac.setText(display.device_get_numaxes_label, "Axis Count: {0}".format(gamedevice.device.get_numaxes()))

                """Draw something if no axis is moving"""
                ac.setText(display.device_get_axis_label, "Move An Axis")
                ac.setFontColor(display.device_get_axis_label, 1.0, 0.0, 0.0, 1)

                """Here I show how to do the loop version again which supports only axis available have to set the string variable reset before the loop to print all values in one line at one time"""
                self.axis_string = ""
                for i in range(gamedevice.device.get_numaxes()):
                    if(gamedevice.device.get_axis(i)):
                        ac.setFontColor(display.device_get_axis_label, 1.0, 1.0, 0.1, 1)
                        self.axis_string += "Axis: {0} Value: {1} | ".format(i,gamedevice.device.get_axis(i))
                        ac.setText(display.device_get_axis_label, self.axis_string)

                """This is a conditional version but if there are more than 5 Axis on a device this would break the script
                 To use a conditional like this you would need to build in your own handler to have enough label objects for the number of device axis
                 COMMENT THIS CONDITIONAL OUT IF YOU ARE USING A DEVICE WITH MORE THAN 5 AXIS or write in the extra objects :)"""
                ac.setText(display.device_get_axis_label_1, "Axis 1 Not Used")
                ac.setText(display.device_get_axis_label_2, "Axis 2 Not Used")
                ac.setText(display.device_get_axis_label_3, "Axis 3 Not Used")
                ac.setText(display.device_get_axis_label_4, "Axis 4 Not Used")
                ac.setText(display.device_get_axis_label_5, "Axis 5 Not Used")
                if(gamedevice.device.get_axis(0)):
                    if(gamedevice.device.get_axis(0) != None):
                        ac.setText(display.device_get_axis_label_1, "Axis 1 Value: {0}".format(gamedevice.device.get_axis(0)))
                    else:
                        ac.setText(display.device_get_axis_label_1, "Axis 1 Not Used")
                if(gamedevice.device.get_axis(1)):
                    if(gamedevice.device.get_axis(1) != None):
                        ac.setText(display.device_get_axis_label_2, "Axis 2 Value: {0}".format(gamedevice.device.get_axis(1)))
                    else:
                        ac.setText(display.device_get_axis_label_2, "Axis 2 Not Used")
                if(gamedevice.device.get_axis(2)):
                    if(gamedevice.device.get_axis(2) != None):
                        ac.setText(display.device_get_axis_label_3, "Axis 3 Value: {0}".format(gamedevice.device.get_axis(2)))
                    else:
                        ac.setText(display.device_get_axis_label_3, "Axis 3 Not Used")
                if(gamedevice.device.get_axis(2)):
                    ac.setText(display.device_get_axis_label_3, "Axis 3 Value: {0}".format(gamedevice.device.get_axis(2)))
                if(gamedevice.device.get_axis(3)):
                    ac.setText(display.device_get_axis_label_4, "Axis 4 Value: {0}".format(gamedevice.device.get_axis(3)))
                if(gamedevice.device.get_axis(4)):
                    ac.setText(display.device_get_axis_label_5, "Axis 5 Value: {0}".format(gamedevice.device.get_axis(4)))
            else:
                """Update to this if no axis controller detected on device"""
                ac.setText(display.device_get_numaxes_label, "No Axis Controller Found")
                ac.setFontColor(display.device_get_numaxes_label, 1.0, 0.0, 0.0, 1)

            ac.setText(display.device_get_numhats_label, "Hat Count : {0}".format(gamedevice.device.get_numhats()))
            ac.setText(display.device_get_hat_label, "Move The Hat")
            ac.setFontColor(display.device_get_hat_label, 1.0, 0.0, 0.0, 1)

            for i in range(gamedevice.device.get_numhats()):
                if(gamedevice.device.get_hat(i)):
                    if (gamedevice.device.get_hat(i) == (0,0)):
                        ac.setText(display.device_get_hat_label, "Move The Hat")
                        ac.setFontColor(display.device_get_hat_label, 1.0, 0.0, 0.0, 1)
                    elif (gamedevice.device.get_hat(i) == (1,0)):
                        ac.setText(display.device_get_hat_label, "Right Hat Pressed - Value : {0}".format(gamedevice.device.get_hat(i)))
                        ac.setFontColor(display.device_get_hat_label, 0.0, 1.0, 0.1, 1)
            # ac.setText(display.device_get_numballs_label, "Track Ball Count : {0}".format(gamedevice.device.get_numballs()))
            # ac.setText(display.device_get_ball_label, "Track Ball Value : {0}".format(gamedevice.device.get_ball(0)))

    # ac.console("Number of joysticks: {}".format(joystick_count))
    # For each joystick:
    # for i in range(joystick_count):
    #     joystick = pygame.joystick.Joystick(i)
    #     joystick.init()
        #
        # ac.console("Joystick {}".format(i))
        # # Get the name from the OS for the controller/joystick
        # name = joystick.get_name()
        # ac.console("Joystick name: {}".format(name))
        #
        # # Usually axis run in pairs, up/down for one, and left/right for
        # # the other.
        # axes = joystick.get_numaxes()
        # ac.console("Number of axes: {}".format(axes))
        # for i in range( axes ):
        #     axis = joystick.get_axis( i )
        #     ac.console("Axis {} value: {:>6.3f}".format(i, axis))

        # buttons = joystick.get_numbuttons()
        # ac.console("Number of buttons: {}".format(buttons))
        # for i in range( buttons ):
        #     button = joystick.get_button( i )
        #     ac.console("Button {:>2} value: {}".format(i,button))
        #
        # # Hat switch. All or nothing for direction, not like joysticks.
        # # Value comes back in an array.
        # hats = joystick.get_numhats()
        # ac.console("Number of hats: {}".format(hats))
        #
        # for i in range( hats ):
        #     hat = joystick.get_hat( i )
        #     ac.console("Hat {} value: {}".format(i, str(hat)))
        else:
            """If no device attached or detected only update the display to say so"""
            ac.setText(display.device_count_label, "Total Detected Devices : {0}".format(gamedevice.device_count))
            ac.setText(display.device_get_id_label, "Device ID : ------")
            ac.setText(display.device_get_name_label, "Device Name : No Compatible Device Connected")
            ac.setText(display.device_get_numbuttons_label, "Total Buttons : ------")
            ac.setText(display.device_get_button_label, "Button  ------")
            ac.setText(display.device_get_numaxes_label, "Axis Count: ------")
            ac.setText(display.device_get_axis_label, "Axis Value 1: ------")
            ac.setText(display.device_get_axis_label, "Axis Value 2: ------")
            ac.setText(display.device_get_axis_label, "Axis Value 3: ------")
            ac.setText(display.device_get_axis_label, "Axis Value 4: ------")
            ac.setText(display.device_get_axis_label, "Axis Value 5: ------")
            ac.setText(display.device_get_numhats_label, "Hat Count : ------")
            ac.setText(display.device_get_hat_label, "Hat Value : ------")

    def AppActivatedFunction(self,val):
        pass

    def AppDismissedFunction(self,val):
        pygame.quit()

"""I could have included this in the display class but I kept it separate to make it read easier
This class creates an instance that contains the device object as a property and also the total devices on the system
we need a secondary setInitialStatus after instance init because pygame needs to be running first to work"""

class GameController:
    """Contains the device object and its initialize method """
    def __init__(self):
        """Will contain the number of devices detected on the system."""
        self.device_count = None
        """Will contain the device object"""
        self.device = None

    def setInitialStatus(self):
        """Update the number of devices detected on the system
        You can access this directly (via pygame.joystick.get_count()) but I am storing variable here to show how many devices are on the system
        also can be used in main loop (as I do using updateStatus below) to detect when devices are added and removed BUT not while the game is running (See Bellow)
        Because the device order and list would change when devices are added and changed or removed you would have to create support to detect and seup devices on app startup
        by match devices by ID name etc and handle the change of the number of devices and each set of control types in your code :)
        I am only supporting ONE DEVICE at a time in this test code. You can change to different devices if you have several connected (See Bellow)
        I probably will expand this later to handle multiple devices at the same time and switch between
        This is why I am just allowing to set a single device and report the number of devices so you can switch manually or write code to automate switching so I do not have to :)"""
        self.device_count = pygame.joystick.get_count()

        """The following creates the device object in the specified variable. device number one is set below which is located at 0
        If you have several devices and you want to use a different device, steeering wheel, joystick or game pad change this number (if you have 3 devices connected they would be numbered 0,1,2)
        1st we make sure a compatible device is detected if not then do not create"""
        if(self.device_count == 0 or None):
            """Here I do nothing if there is no device detected"""
            pass
            """Handling device connect or disconnects at runtime
            I did a lot of testing trying to build a way to handle devices being added or removed in game in a live session
            But what happens is during a session once a wheel or other device is removed and then added back the connection to tyhe wheel gets lost and you have to exit and restart the session anyway
            You can have multiple devices (Up to 8 I think) in Pygame and create code to either statically or dynamically create objects on startup
            But the devices need to be plugged in and ready when the game session starts to be detected properly and if they get pulled during the session then this method of access to the devices breaks as well
            So all that is possible is no devices or a number of devices that are ready when the game starts
            You code must scan the device, query it's type and number of features and values (which will change for different devices) and then setup for your needs accordingly
            you will get errors trying to access properties that do not exist"""
        else:
            """create the device object at ID number 0 (the 1st/default device on your USB game device chain
            #TO CHANGE TO A DIFFERENT DEVICE CHANGE THIS VALUE ie if you have 3 devices to use the third device set to (2)
            #I am only supporting ONE DEVICE in this test code. I probably will expand this later to handle multiple devices at the same time and switch"""
            self.device = pygame.joystick.Joystick(0)

            """Must initialize before being used, The main reason this function (setInitialStatus)exists and is outside the instance init method is
            pygame must be started and inititalised so this method will be called after pygame started see below"""
            self.device.init()

"""declare class instance objects"""

display = DisplayClass()
gamedevice = GameController()

def acMain(ac_version):
    """main init function which runs on game startup."""
    display.appWindow = ac.newApp("mGameController")
    ac.addRenderCallback(display.appWindow, onFormRender)
    ac.addOnAppActivatedListener(display.appWindow, display.AppActivated)
    ac.addOnAppDismissedListener(display.appWindow, display.AppDismissed)
    ac.setSize(display.appWindow, 1100, 420)

    """setting up all of the labels I could have done this in display class but put it here to make it familiar to assetto corsa developers"""

    display.device_count_label = ac.addLabel(display.appWindow, "device_count")
    ac.setPosition(display.device_count_label, 10, 50)
    ac.setFontColor(display.device_count_label, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(display.device_count_label,'left')

    display.device_get_id_label = ac.addLabel(display.appWindow, "device_get_id")
    ac.setPosition(display.device_get_id_label, 10, 70)
    ac.setFontColor(display.device_get_id_label, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(display.device_get_id_label,'left')

    display.device_get_name_label = ac.addLabel(display.appWindow, "device_get_name")
    ac.setPosition(display.device_get_name_label, 10, 90)
    ac.setFontColor(display.device_get_name_label, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(display.device_get_name_label,'left')

    display.device_get_numbuttons_label = ac.addLabel(display.appWindow, "device_get_numbuttons")
    ac.setPosition(display.device_get_numbuttons_label, 10, 110)
    ac.setFontColor(display.device_get_numbuttons_label, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(display.device_get_numbuttons_label,'left')

    display.device_get_button_label = ac.addLabel(display.appWindow, "device_get_button")
    ac.setPosition(display.device_get_button_label, 10, 130)
    ac.setFontColor(display.device_get_button_label, 1.0, 0.0, 0.0, 1)
    ac.setFontAlignment(display.device_get_button_label,'left')

    display.device_get_numaxes_label = ac.addLabel(display.appWindow, "device_get_numaxes")
    ac.setPosition(display.device_get_numaxes_label, 10, 150)
    ac.setFontColor(display.device_get_numaxes_label, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(display.device_get_numaxes_label,'left')

    display.device_get_axis_label = ac.addLabel(display.appWindow, "device_get_axis")
    ac.setPosition(display.device_get_axis_label, 10, 170)
    ac.setFontColor(display.device_get_axis_label, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(display.device_get_axis_label,'left')

    display.device_get_axis_label_1 = ac.addLabel(display.appWindow, "device_get_axis 1")
    ac.setPosition(display.device_get_axis_label_1, 10, 190)
    ac.setFontColor(display.device_get_axis_label_1, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(display.device_get_axis_label_1,'left')

    display.device_get_axis_label_2 = ac.addLabel(display.appWindow, "device_get_axis 2")
    ac.setPosition(display.device_get_axis_label_2, 10, 210)
    ac.setFontColor(display.device_get_axis_label_2, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(display.device_get_axis_label_2,'left')

    display.device_get_axis_label_3 = ac.addLabel(display.appWindow, "device_get_axis 3")
    ac.setPosition(display.device_get_axis_label_3, 10, 230)
    ac.setFontColor(display.device_get_axis_label_3, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(display.device_get_axis_label_3,'left')

    display.device_get_axis_label_4 = ac.addLabel(display.appWindow, "device_get_axis 4")
    ac.setPosition(display.device_get_axis_label_4, 10, 250)
    ac.setFontColor(display.device_get_axis_label_4, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(display.device_get_axis_label_4,'left')

    display.device_get_axis_label_5 = ac.addLabel(display.appWindow, "device_get_axis 5")
    ac.setPosition(display.device_get_axis_label_5, 10, 270)
    ac.setFontColor(display.device_get_axis_label_5, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(display.device_get_axis_label_5,'left')

    display.device_get_axis_label_6 = ac.addLabel(display.appWindow, "device_get_axis 6")
    ac.setPosition(display.device_get_axis_label_6, 10, 290)
    ac.setFontColor(display.device_get_axis_label_6, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(display.device_get_axis_label_6,'left')

    display.device_get_numballs_label = ac.addLabel(display.appWindow, "device_get_numballs")
    ac.setPosition(display.device_get_numballs_label, 10, 310)
    ac.setFontColor(display.device_get_numballs_label, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(display.device_get_numballs_label,'left')

    display.device_get_ball_label = ac.addLabel(display.appWindow, "device_get_ball")
    ac.setPosition(display.device_get_ball_label, 10, 330)
    ac.setFontColor(display.device_get_ball_label, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(display.device_get_ball_label,'left')

    display.device_get_numhats_label = ac.addLabel(display.appWindow, "device_get_numhats")
    ac.setPosition(display.device_get_numhats_label, 10, 350)
    ac.setFontColor(display.device_get_numhats_label, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(display.device_get_numhats_label,'left')

    display.device_get_hat_label = ac.addLabel(display.appWindow, "device_get_hat_label")
    ac.setPosition(display.device_get_hat_label, 10, 370)
    ac.setFontColor(display.device_get_hat_label, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(display.device_get_hat_label,'left')

    """Must init Pygame first"""
    pygame.init()
    """then set initial status on gamedevice object"""
    gamedevice.setInitialStatus()
    return "mGameController"

def acUpdate(deltaT):
    """main loop"""
    """pump/update the event queue in Pygame"""
    pygame.event.pump()
    """The event queue style approach"""
    #display.updateEvent()
    """The object property style approach"""
    display.updateObject()

def onFormRender(deltaT):
    """only update app when app form is visible then update only the following note call back method for this function defined in acMain above."""
    pass

def acShutdown():
    """on shut down quit pygame so no crash or lockup."""
    pygame.quit()