import os
import bpy

bl_info = {
    "name": "Blend Log",
    "blender": (2, 80, 0),
    "category": "Development",
    "description": "Logs and saves executable commands from the Blender Info area"
}

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

    with open(os.path.join(filepath, f"{filename}.py"), "a") as file: 
        for command in commands:
            file.write(f"\t{command}\n")


def register():
    bpy.app.handlers.save_post.append(savePostHandler)


def unregister():
    bpy.app.handlers.save_post.remove(savePostHandler)


if __name__ == '__main__':
    register()




#this code makes it not crash once addon is disabled
#     def savePostHandler(scene):
#     filepath = bpy.path.abspath("//")
#     filename = bpy.path.basename(bpy.data.filepath).split(".")[0]

#     commands = getCommands()

#     try:
#         with open(os.path.join(filepath, f"{filename}.py"), "a") as file: 
#             for command in commands:
#                 file.write(f"\t{command}\n")
#     except Exception as e:
#         print("Error saving log:", str(e))

# def register():
#     try:
#         bpy.app.handlers.save_post.append(savePostHandler)
#         print("Handler registered successfully")
#     except Exception as e:
#         print("Error registering handler:", str(e))

# def unregister():
#     try:
#         bpy.app.handlers.save_post.remove(savePostHandler)
#         print("Handler unregistered successfully")
#     except ValueError:
#         print("Handler not found in save_post handlers list")

# if __name__ == '__main__':
#     register()