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

import bpy
import subprocess

arm_image = False
arm_animation = False

class ShutdownPanel(bpy.types.Panel):
    bl_idname = 'PREFERENCES_PT_shutdownpanel'
    bl_label = 'Shutdown after Render'
    bl_space_type = 'PREFERENCES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    def draw_header(self,context):
        # Example property to display a checkbox, can be anything
        self.layout.prop(context.scene.render, "use_border", text="")

    def draw(self, context):
        self.layout.label(text='Hello there')

def register():
    bpy.utils.register_class(ShutdownPanel)

def unregister():
    bpy.utils.unregister_class(ShutdownPanel)

if __name__ == "__main__":
    register()