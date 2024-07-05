import os
import bpy
import functools

bl_info = {
    "name": "Blend Log",
    "blender": (2, 80, 0),
    "category": "Development",
    "description": "Logs and saves executable commands from the Blender Info area"
}



class BlenditSubscriber:
    """Subscriber to different event publishers"""
    
    def __repr__(self):
        return self.__doc__
        

blenditSubscriber = BlenditSubscriber()


def writeToFile(lines):
    """Writes list of lines to associated python file"""

    filepath = bpy.path.abspath("//")
    filename = bpy.path.basename(bpy.data.filepath).split(".")[0]

    # Save .blend file (Writes commands to Python file and clears reports)
    bpy.ops.wm.save_mainfile(filepath=os.path.join(filepath, f"{filename}.blend"))

    # Append lines to Python file
    with open(os.path.join(filepath, f"{filename}.py"), "a") as file:
        for line in lines:
            file.write(f"\t{line}\n")


def activeObjectCallback():
    """Called when active object changes"""

    objectsToSelect  = bpy.context.view_layer.objects.selected.keys()
    objectToActivate = bpy.context.view_layer.objects.active.__repr__()
    lines = (
        "[obj.select_set(False) for obj in bpy.context.view_layer.objects.selected.values()]",
        f"[bpy.context.view_layer.objects.get(obj).select_set(True) for obj in {objectsToSelect}]",
        f"bpy.context.view_layer.objects.active = {objectToActivate}",
    )
    bpy.app.timers.register(functools.partial(writeToFile, lines))


def subscribe():
    """Subscribes to different event publishers"""

    # Active Object
    bpy.msgbus.subscribe_rna(
        key=(bpy.types.LayerObjects, "active"),
        owner=blenditSubscriber,
        args=(),
        notify=activeObjectCallback,
        options={'PERSISTENT'}
    )


def unsubscribe():
    """Unsubscribes to all event publishers"""
    bpy.msgbus.clear_by_owner(blenditSubscriber)


def getReports():
    """Returns a list of reports as seen in the Info area"""
    
    window = bpy.context.window_manager.windows[0]
    area = window.screen.areas[0]
    with bpy.context.temp_override(window=window, area=area):

        # Current area type
        currentType = area.type

        # Copy all info to clipboard
        area.type = 'INFO'
        bpy.ops.info.select_all(action='SELECT')
        bpy.ops.info.report_copy()
        bpy.ops.info.select_all(action='DESELECT')

        # Restore context
        area.type = currentType
        
    # Transfer from clipboard
    reports = bpy.context.window_manager.clipboard
    return reports.splitlines()


def ignoreReport(report):
    """Returns True if report should be ignored, else False"""

    ignoreReportList = [
        "bpy.context.space_data.",
        "bpy.data.window_managers[",
        "bpy.context.window_manager.blendit"
    ]
    for s in ignoreReportList:
        if report.startswith(s):
            return True
    return False


def getCommands():
    """Extract executable commands from reports"""

    reports = getReports()
    commands = []
    for i in range(len(reports)):
        report = reports[i]
        if (report.startswith("Deleted") and
            reports[i - 1] != "bpy.ops.object.delete(use_global=True, confirm=False)"):
            commands.append("bpy.ops.object.delete(use_global=False, confirm=False)")
            continue
        
        if not report.startswith("bpy."):
            continue
        
        if ignoreReport(report):
            continue
        
        commands.append(report)
        
        if report == "bpy.ops.material.new()":
            commands.append("bpy.context.object.active_material = bpy.data.materials[-1]")

    return commands


def savePostHandler(scene):
    filepath = bpy.path.abspath("//")
    filename = bpy.path.basename(bpy.data.filepath).split(".")[0]

    commands = getCommands()

    try:
        with open(os.path.join(filepath, f"{filename}.py"), "a") as file: 
            for command in commands:
                file.write(f"\t{command}\n")
    except Exception as e:
        print("Error saving log:", str(e))

def loadPostHandler(_):
    bpy.ops.wm.splash('INVOKE_DEFAULT')
    
    # Message bus subscription
    subscribe()


def register():
    bpy.app.handlers.save_post.append(savePostHandler)
    bpy.app.handlers.load_post.append(loadPostHandler)
    print("Blend Log addon registered")
    
    # Enable add-on on startup
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons.get(__name__).preferences
    if addon_prefs is not None:
        addon_prefs.startup = True

def unregister():
    bpy.app.handlers.save_post.remove(savePostHandler)
    bpy.app.handlers.load_post.remove(loadPostHandler)
    bpy.app.handlers.load_factory_startup_post.remove(loadPreferencesHandler)
    print("Blend Log addon unregistered")

def loadPreferencesHandler(_):
    print("Changing Preference Defaults!")

    prefs = bpy.context.preferences
    prefs.use_preferences_save = False

    view = prefs.view
    view.show_splash = True

if __name__ == '__main__':
    register()

