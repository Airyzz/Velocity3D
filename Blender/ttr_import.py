import bpy

bl_info = {
    "name": "Velo Import (TTR)",
    "author": "Airyz",
    "version": (1, 0, 1),
    "blender": (2, 80, 0),
    "category": "Import-Export",
    "location": "File > Import",
    "description": "Import Velo",
}

#attempt to get an attribute from True Time Remapping plugin. 
def is_ttr_installed():
    try:
        type = bpy.context.scene.ttr.type
        return True
    except:
        return False

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
import json

class ImportVeloTTR(Operator, ImportHelper):
    """Import .Velo file to True Time Remapping Plugin"""
    bl_idname = "velo_import.importvelo"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Import Velo (.velo)"

    # ImportHelper mixin class uses this
    filename_ext = ".velo"

    filter_glob: StringProperty(
        default="*.velo",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        return self.read_velo(context, self.filepath)

    def read_velo(self, context, filepath):
    
        if not is_ttr_installed():
            self.report({'ERROR'}, "True Time Remapping is not installed. See console for more details")
            print("This importer requires the use of the True Time Remapping plugin by Andrey Sokolov")
            print("This plugin can be found here: https://youtu.be/FmV1t2MzMKk")
        else:
            #Read data from file
            f = open(filepath, 'r', encoding='utf-8')
            data = f.read()
            f.close()
            velo = json.loads(data)

            #Set time remap mode to Frames    
            bpy.context.scene.ttr.type = 'FRAMES'
            
            
            
            #If action doesnt exist, create a new one
            if(bpy.context.scene.animation_data.action == None):
                bpy.context.scene.animation_data.action = bpy.data.actions.new('Velocity')
    
    
            fc = bpy.context.scene.animation_data.action.fcurves
            
            #Delete any existing FCurves
            for curve in fc:
                if curve.data_path == 'ttr.frame':
                    fc.remove(curve)
            
            #Create new FCurve
            fcurve = fc.new("ttr.frame")
            fcurve.keyframe_points.add(len(velo))

            #Create keys
            for frame in velo:
                fcurve.keyframe_points[int(frame)].co = int(frame), velo[frame]   
                fcurve.keyframe_points[int(frame)].interpolation = 'LINEAR'


            #Calculate and set 'Skip from End'
            last_frame = int(list(velo.keys())[-1]) 
            frame_end = bpy.context.scene.frame_end
            bpy.context.scene.ttr.skip_end = -(frame_end - last_frame)


        return {'FINISHED'}

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportVeloTTR.bl_idname, text="Import Velo to TTR (.velo)")


def register():
    bpy.utils.register_class(ImportVeloTTR)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportVeloTTR)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.velo_import.importvelo('INVOKE_DEFAULT')
