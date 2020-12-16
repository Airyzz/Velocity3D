# Velocity3D
 A series of scripts to apply velocity from After Effects and Sony Vegas to 3D Packages
 


## .Velo File Format

JSON Serialized dictionary

Key = String index for frame (real time)

Value = Frame number to be mapped to real time frame.


 
 
 ## How To Use:

### Blender:

1. Apply a time remap to slow down the current animation

![](tutorial_gifs/how_to_time_remap.gif)

2. Viewport render to AVI

![](tutorial_gifs/how_to_viewport_render.gif)

3. Apply Time Remapping to that render in After Effects

![](tutorial_gifs/apply_velo_ae.gif)

4. Export Velocity File

![](tutorial_gifs/export_velocity.gif)

5. Use Velocity Render script in Blender to render only the required frames

![](tutorial_gifs/velocity_render.gif)

6. DONE!

![](tutorial_gifs/Comp.gif)

### Maya:

1. Use Velocity plugin to create Velocity Controller

2. Use Velocity Controller to set a desired timescale

3. Apply this timescale using Velocity Plugin

4. Playblast render viewport to avi

5. Apply Time Remapping in After Effects

6. Export Velocity File

7. Apply Velocity in Maya using Velocity Plugin
