import bpy
import json
import math

bl_info = {
    "name": "Velocity Render",
    "author": "Airyz",
    "version": (1, 0, 1),
    "blender": (2, 80, 0),
    "category": "Import-Export",
    "location": "File > Export",
    "description": "Render with Velocity",
}


def render(context, filepath, velopath):

    existing_frames = dict()
    scene = bpy.context.scene
    file_template = filepath[0:-4]
    win = bpy.context.window_manager
    
    #try:
    if True:
        #data  = win.clipboard
        data = open(velopath, "r").read()
        frames = json.loads(data)
        
        i = 0
        length = len(frames)
        
        for frame in frames:
            
            percent = (i / length) * 100
            
            frame_number = frames[frame]
            scene.frame_set(frame_number)
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            scene.render.filepath = file_template + "_" + str(i) + ".png"
            bpy.ops.render.render(write_still=True)
            
            i += 1

    #except:
    #    print("Error")
    print(file_template)
    
    return {'FINISHED'}

# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class VeloExport(Operator, ExportHelper):
    """Render png sequence with Velocity"""
    bl_idname = "velo_render.render"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Render"

    # ExportHelper mixin class uses this
    filename_ext = ".png"
    
    filter_glob: StringProperty(
        default="*.png",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    
    veloPath: bpy.props.StringProperty(
        name="Velo File",
        description="Path of .velo file"
    )

    def execute(self, context):
        return render(context, self.filepath, self.veloPath)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    print('lol')
    self.layout.operator(VeloExport.bl_idname, text="Velocity Render (.png)")


def register():
    bpy.utils.register_class(VeloExport)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(VeloExport)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.velo_render.render('INVOKE_DEFAULT')
