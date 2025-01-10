########## INFO ##########

bl_info = {
    "name": "Shutdown after Render",
    "version": (0, 3, 2),
    "author": "David Bühler",
    "blender": (4, 3, 0),
    "description": "Automatically shuts down your PC after your render finishes",
    "location": "Properties > Render > Shutdown after Render",
    "doc_url": "https://github.com/daveiator/shutdown-after-render",
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

########## ENVIRONMENT ##########

class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    # Shutdown command
    shutdown_command: bpy.props.StringProperty(
        name = "Shutdown Command",
        default = "shutdown /s /t 60",
    )

    # Hibernate command
    hibernate_command: bpy.props.StringProperty(
        name = "Hibernate Command",
        default = "shutdown /h",
    )

    # Abort command
    abort_command: bpy.props.StringProperty(
        name = "Abort Command",
        default = "shutdown /a",
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Shutdown Command:")
        layout.prop(self, "shutdown_command", text="")
        layout.label(text="Hibernate Command:")
        layout.prop(self, "hibernate_command", text="")
        layout.label(text="Abort Command:")
        layout.prop(self, "abort_command", text="")

########## FUNCTIONS ##########

def shutdown(mode):
    if mode == "shutdown":
        shutdown_command = bpy.context.preferences.addons[__package__].preferences.shutdown_command
        subprocess.run(shutdown_command)
        bpy.types.WindowManager.shutdown_in_process = True
    elif mode == "hibernate":
        hibernate_command = bpy.context.preferences.addons[__package__].preferences.hibernate_command
        subprocess.run(hibernate_command)
        bpy.types.WindowManager.shutdown_in_process = True
    elif mode == "quit":
        bpy.ops.wm.quit_blender()

########## Operators ##########
class CancelShutdown(bpy.types.Operator):
    bl_idname = "wd.cancel_shutdown"
    bl_label = "Cancel Shutdown"
 
    @classmethod
    def description(cls, context, properties):
        return "Cancel the shutdown"
    
    def execute(self, context):
        abort_command = bpy.context.preferences.addons[__package__].preferences.abort_command
        subprocess.run(abort_command)
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
    if bpy.context.window_manager.arm_shutdown:
        print("Shutdown after render enabled!\nShutting down...")
        shutdown(bpy.context.window_manager.shutdown_modes)
    

@persistent
def render_init(scene):
    if bpy.context.window_manager.arm_shutdown:
        print("Initialized render! Shutdown after render enabled!")


########## PANELS ##########

# Location Panel
class ShutdownPanelContainer():
    """Creates a Panel in the Render properties window"""
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
# MAIN PANEL
class RENDER_PT_ShutdownPanel(ShutdownPanelContainer, bpy.types.Panel):
    bl_label = 'Shutdown after Render'
    bl_order = 999

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
class RENDER_PT_ShutdownExtrasPanel(ShutdownPanelContainer, bpy.types.Panel):
    bl_parent_id = 'RENDER_PT_ShutdownPanel'
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
    AddonPreferences,
    RENDER_PT_ShutdownPanel,
    RENDER_PT_ShutdownExtrasPanel,
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