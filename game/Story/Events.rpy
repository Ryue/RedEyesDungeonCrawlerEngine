init:
    $ event002Triggered = False
    $ event001Triggered = False

label Event001:
    if (not event001Triggered):
        if (dungeonCrawl3DEngine.viewLastY > dungeonCrawl3DEngine.viewY):
            "You triggered an event! Congratulations. You can now choose to fail or succeed on the event. Have no fear though as you can try again until  you succeed on the event!"
            menu:
                "Failure":
                    "You failed, but have no fear you can try again!"
                "Success":
                    "You succeeded"
                    $ event001Triggered = True
    return

label Event002:
    if (not event002Triggered):
        "If you enter the cave from the south you will trigger an event which won't be triggered if you leave the cave. This here will only be shown once!"
        $ event002Triggered = True

    return

label Event003:
    "If you enter the cave north from here you will trigger an event"

    return
