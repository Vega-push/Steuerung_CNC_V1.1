from cebomsr import LibraryInterface, DeviceType

# Search for devices ...
devices = LibraryInterface.enumerate(DeviceType.CeboLC)

def messwert_auslesen():
    try:

        # If at least one has been found, use the first one ...
        if (len(devices) > 0):
            device = devices[0]

            # Open device, nothing can be done without doing this.
            device.open()
            value = device.getSingleEndedInputs()[0].read()
            print(value)

            # Finalize device usage, this free's up the device, so it can be used
            # again, including other applications.
            device.close()
            return value
    except Exception as e:
        print(e)
