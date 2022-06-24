import bpy
from bpy.app.handlers import persistent

@persistent
def render_complete_handler(scene):
    print("Load Handler:", bpy.data.filepath)

@persistent
def render_init_handler(scene):
    print("Initialized render!")
    ShowMessageBox("Shutdown-after-Render is active!", "REMINDER", "QUIT")

def ShowMessageBox(message = "", title = "Info", icon = "INFO"):
    def draw(self, context):
        self.layout.label(text = message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)