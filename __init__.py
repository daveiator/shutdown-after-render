########## INFO ##########

bl_info = {
    "name": "Shutdown after Render",
    "version": (0, 1, 0),
    "author": "David Bühler",
    "blender": (3, 0, 0),
    "description": "Shuts down your PC after your render finishes",
    "location": "Properties > Auto-Shutdown",
    # "doc_url": "",
    "category": "System",
}


########## IMPORTS ##########

import bpy
from bpy.app.handlers import persistent
import subprocess


########## VARIABLES ##########

bpy.types.WindowManager.arm_shutdown = bpy.props.BoolProperty(default=0)
bpy.types.WindowManager.shutdown_in_process = bpy.props.BoolProperty(default=0)

bpy.types.WindowManager.shutdown_modes = bpy.props.EnumProperty(
    name = "Shutdown Mode",
    default = 0,
    description = "Choose the shutdown mode",
    items = [
        ("shutdown", "Shutdown", "Shuts down your PC"),
        ("hibernate", "Hibernate", "Sets your PC to hibernate"),
        ("quit", "Quit Blender", "Closes Blender"),
    ]
)


########## FUNCTIONS ##########

def shutdown(mode):
    extra_time = "60"
    if mode == "shutdown":
        subprocess.call(["shutdown", "-s", "-t", extra_time])
        bpy.types.WindowManager.shutdown_in_process = True
    elif mode == "hibernate":
        subprocess.call(["shutdown", "-h", "-t", extra_time])
    elif mode == "quit":
        bpy.ops.wm.quit_blender()

def ShowMessageBox(message = "", title = "Info", icon = "INFO"):
    def draw(self, context):
        self.layout.label(text = message)

    context.window_manager.popup_menu(draw, title = title, icon = icon)

########## Operators ##########
class CancelShutdown(bpy.types.Operator):
    bl_idname = "wd.cancel_shutdown"
    bl_label = "Cancel Shutdown"

    @classmethod
    def description(cls, context, properties):
        return "Cancel the shutdown"
    
    def execute(self, context):
        subprocess.call(["shutdown", "-a"])
        bpy.types.WindowManager.shutdown_in_process = False
        print("Shutdown cancelled!")
        return {'FINISHED'}

class RenderStillToOutput(bpy.types.Operator):
    bl_idname = "wd.render_still"
    bl_label = "Render Image to Output-Folder"

    @classmethod
    def description(cls, context, properties):
        return "Saves the rendered image automatically to the output folder"

    def execute(self, context):
        bpy.ops.render.render('INVOKE_DEFAULT', animation=False, write_still=True)
        return {'FINISHED'}

class RenderAnimation(bpy.types.Operator):
    bl_idname = "wd.render_animation"
    bl_label = "Render Animation to Output-Folder"

    @classmethod
    def description(cls, context, properties):
        return "Renders the animation automatically to the output folder (SAME AS DEFAULT)"

    def execute(self, context):
        bpy.ops.render.render('INVOKE_DEFAULT',animation=True)
        return {'FINISHED'}

########## HANDLERS ##########

@persistent
def render_complete(scene):
    print("Render complete! Checking for shutdown...")
    if bpy.context.window_manager.arm_shutdown:
        print("Shutdown after render enabled!\nShutting down...")
        shutdown(bpy.context.window_manager.shutdown_modes)
    

@persistent
def render_init(scene):
    print("Initialized render!")
    if bpy.context.window_manager.arm_shutdown:
        ShowMessageBox("Shutdown-after-Render is active!", "REMINDER", "QUIT")


########## PANELS ##########

# Location Panel
class ShutdownPanelContainer():
    """Creates a Panel in the Output properties window"""
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'output'
# MAIN PANEL
class ShutdownPanel(ShutdownPanelContainer, bpy.types.Panel):
    bl_idname = 'OUTPUT_PT_shutdownpanel'
    bl_label = 'Shutdown after Render'

    def draw_header(self,context):
        # Example property to display a checkbox, can be anything
        layout = self.layout
        layout.prop(context.window_manager, 'arm_shutdown', text='', icon='QUIT')


    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.enabled = context.window_manager.arm_shutdown
        split = row.split(factor=.4)
        col = split.column()
        col.alignment = 'RIGHT'
        col.label(text='Type')

        col = split.column()
        col.prop(context.window_manager, 'shutdown_modes', text = '', icon = 'NONE')

        if context.window_manager.shutdown_in_process:
            row = layout.row()
            row = layout.row()
            row.alignment = 'CENTER'
            row.label(text="Shutdown in process...")
            row = layout.row()
            row.alignment = 'CENTER'
            row.operator('wd.cancel_shutdown', text="CANCEL SHUTDOWN", icon='CANCEL')
        else:
            row = layout.row()
        pass

#Extras Panel
class ShutdownExtrasPanel(ShutdownPanelContainer, bpy.types.Panel):
    bl_parent_id = 'OUTPUT_PT_shutdownpanel'
    bl_label = 'Extras'

    def draw(self, context):
        layout = self.layout
        split = layout.split(factor=.05)
        col = split.column()
        col = split.column()
        row = col.row()
        row.operator('wd.render_still', text="Render Image to Output Folder", icon='RENDER_STILL')
        row = col.row()
        row.operator('wd.render_animation', text="Render Animation to Output Folder", icon='RENDER_ANIMATION')



########## REGISTRATION ##########

classes = (
    ShutdownPanel,
    ShutdownExtrasPanel,
    CancelShutdown,
    RenderStillToOutput,
    RenderAnimation)

def register():
    # Handlers
    bpy.app.handlers.render_init.append(render_init)
    bpy.app.handlers.render_complete.append(render_complete)

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    # Handlers
    bpy.app.handlers.render_init.remove(render_init)
    bpy.app.handlers.render_complete.remove(render_complete)

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()