# Info

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


# Imports

import bpy
from bpy.app.handlers import persistent
import subprocess


# Variables

bpy.types.WindowManager.arm_shutdown = bpy.props.BoolProperty(default=0)
bpy.types.WindowManager.shutdown_in_process = bpy.props.BoolProperty(default=0)

bpy.types.WindowManager.shutdown_modes = bpy.props.EnumProperty(
    name = "Shutdown Mode",
    default = 0,
    description = "Choose Shutdown Mode",
    items = [
        ('shutdown', "Shutdown", "Shuts down the computer"),
        ('hibernate', "Hibernate", "Sets the computer to hibernate"),
        ('quit', "Quit Blender", "Closes Blender"),
    ]
)

#  Preferences

class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

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
        layout.label(text = "Shutdown Command:")
        layout.prop(self, 'shutdown_command', text = "")
        layout.label(text = "Hibernate Command:")
        layout.prop(self, 'hibernate_command', text = "")
        layout.label(text = "Abort Command:")
        layout.prop(self, 'abort_command', text = "")

# Functions

def shutdown(mode):
    if mode == 'shutdown':
        shutdown_command = bpy.context.preferences.addons[__package__].preferences.shutdown_command
        subprocess.run(shutdown_command)
        bpy.types.WindowManager.shutdown_in_process = True
    elif mode == 'hibernate':
        hibernate_command = bpy.context.preferences.addons[__package__].preferences.hibernate_command
        subprocess.run(hibernate_command)
        bpy.types.WindowManager.shutdown_in_process = True
    elif mode == 'quit':
        bpy.ops.wm.quit_blender()

def draw_render_still_to_disk(self, context):
    layout = self.layout
    layout.operator('wd.render_still_to_disk', text = "Render Image to Disk", icon = 'RENDER_STILL')

# Operators
class AbortShutdown(bpy.types.Operator):
    bl_idname = 'wd.abort_shutdown'
    bl_label = "Abort Shutdown"
 
    @classmethod
    def description(cls, context, properties):
        return "Abort shutdown"
    
    def execute(self, context):
        abort_command = bpy.context.preferences.addons[__package__].preferences.abort_command
        subprocess.run(abort_command)
        bpy.types.WindowManager.shutdown_in_process = False
        print("Shutdown aborted!")
        return {'FINISHED'}

class RenderStillToDisk(bpy.types.Operator):
    bl_idname = 'wd.render_still_to_disk'
    bl_label = "Render Image to Disk"

    @classmethod
    def description(cls, context, properties):
        return "Renders active scene to output path"

    def execute(self, context):
        bpy.ops.render.render('INVOKE_DEFAULT', animation=False, write_still=True)
        return {'FINISHED'}

# Handlers

@persistent
def render_write(scene):
    if bpy.context.window_manager.arm_shutdown:
        print("Shutdown after render enabled!\nShutting down...")
        shutdown(bpy.context.window_manager.shutdown_modes)
    

@persistent
def render_init(scene):
    if bpy.context.window_manager.arm_shutdown:
        print("Initialized render! Shutdown after render enabled!")


# Panels

# Location Panel
class ShutdownPanelContainer():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'

# Main Panel  
class RENDER_PT_ShutdownPanel(ShutdownPanelContainer, bpy.types.Panel):
    bl_label = "Shutdown After Render"
    bl_order = 999

    def draw_header(self,context):
        layout = self.layout
        layout.prop(context.window_manager, 'arm_shutdown', text = '', icon = 'QUIT')


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
            row.label(text="Shutdown in progress...")
            row = layout.row()
            row.operator('wd.abort_shutdown', text="Abort Shutdown", icon='CANCEL')
        else:
            row = layout.row()
        pass

# Register

classes = (
    AddonPreferences,
    RENDER_PT_ShutdownPanel,
    AbortShutdown,
    RenderStillToDisk
    )

def register():
    # Handlers
    bpy.app.handlers.render_init.append(render_init)
    bpy.app.handlers.render_complete.append(render_write)
    
    bpy.types.TOPBAR_MT_render.prepend(draw_render_still_to_disk)

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    # Handlers
    bpy.app.handlers.render_init.remove(render_init)
    bpy.app.handlers.render_complete.remove(render_write)

    bpy.types.TOPBAR_MT_render.remove(draw_render_still_to_disk)

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __package__ == '__main__':
    register()