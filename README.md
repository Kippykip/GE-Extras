# Genocide Engine Extras Toolbar for Blender 2.79 & Bforartists 1.0.0
Here's a little addon that adds some useful buttons for creating .b3d models for the Genocide Engine (and possibly other Blitz3D/OpenB3D projects).  
Intended to be used along with the [B3DExport](https://github.com/Kippykip/B3DExport/) plugin.  
![Genocide Engine Extras Submenus](https://i.imgur.com/H9xh3B0.png)  
  
This menu adds the following:  
* Translate mesh from 3D Cursor  
  - Translates a meshes position  to the opposite direction from the 3D Cursor coordinates. Uses Local coordinates.  
  - Handy for making gibbable objects in the Genocide Engine specifically.  
* Reset 3D Cursor to 0, 0, 0  
  - Simply resets the 3D Cursor to the center of the screen. Simple but incredibly useful.  
* Flip Meshes X Axis  
  - Another simple useful button, it just mirrors a mesh from the X coordinate (in local coordinates) and automatically handles inverting the polygons (aka flip normals).  
* Convert Global to Local
  - One of the most useful functions, and the main reason for this menus development. It converts all global coordinates selected objects to their local equivalents  
  - The main reasoning for changing an objects global transformations into the mesh/armatures local coordinates, is that the B3D model export doesn't actually use the global coordinates at all (*with some minor trial and error exceptions when animated bones are involved*).   
Exporting a .b3d mesh with multiple different global coordinates can easily result in exporting a glitchy model with the wrong positions and rotations.  
  - This button handles changing multiple different objects global coordinates (for location, rotation and scale) to their local equivalents in one click.  
  - This also fixes all the wrong XYZ transformation positions for all animated keyframes if a scaled armature is involved.  
  - Currently doesn't support rotating the local coordinates for *armatures* however, as it breaks the animation in very wacky ways. Thankfully however, the B3D Exporter seems to handle rotated armatures in their global coordinates anyway.  
Scaling and translating within armatures are properly handled though and work fine.  
  
**Installation:**  
In your Blender 2.79b or Bforartists application, follow these steps.  
1. Click the **File** tab  
2. Click **User Preferences**  
3. Click the **Add-ons** tab  
4. On the bottom, click **Install Add-on from File...**  
5. Select the downloaded **GE-Extras.py** file  
6. Tick the addon  
7. Click **Save User Settings** and Enjoy!  
