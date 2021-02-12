#Genocide Engine Extras ~ Kippykip

bl_info = {
    "name": "Genocide Engine Extras",
    "description": "Adds a submenu with really useful functions for creating .b3d models in the Genocide Engine",
    "author": "Kippykip",
    "version": (1, 1, 0),
    "blender": (2, 7, 9),
    "wiki_url": "https://github.com/Kippykip/GE-Extras",
    "tracker_url": "https://github.com/Kippykip/GE-Extras/issues",
    "category": "User Interface",
    }
    
import bpy
import math

#Menu bar
class GE_Menu(bpy.types.Menu):
    bl_label = "GE Extras"
    bl_idname = "OBJECT_MT_ge_extras"

    #GE Submenus
    def draw(self, context):
        layout = self.layout
        layout.operator("ge.translatecursor")
        layout.operator("ge.resetcursor")
        layout.operator("ge.flipx")
        layout.operator("ge.globaltolocal")
        layout.operator("ge.resetpose")
        layout.operator("ge.clearroll")
        
#######################
#Global Functions here#
#######################
def GE_Alert(message = "", title = "Genocide Engine Extras", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)        
    
#Function to turn all keyframes in a armature into 
def GE_GetKeyFrames(obj):
    keyframes = []
    anim = obj.animation_data
    if anim is not None and anim.action is not None:
        for fcu in anim.action.fcurves:
            for keyframe in fcu.keyframe_points:
                x, y = keyframe.co
                if x not in keyframes:
                    keyframes.append((math.ceil(x)))
    return keyframes

#Function to put all disconnected (but parented) bone names in an array
def GE_GetDisconnectedBones(obj):
    disconnectedbones = []
    for bone in obj.data.edit_bones[:]:
        if(bone.use_connect == False and bone.parent):
            disconnectedbones.append(bone.name)
    return disconnectedbones

#Makes an array of posebones from an array of bone names
def GE_GetPBonesFromBones(obj, bonenames):
    posebones = []
    #Loop through posebones in arm object
    for pbone in obj.pose.bones[:]:
        #Check through the array of bone names and add it to the posebones array
        #if the name matches
        for bonename in bonenames[:]:
            if(pbone.name == bonename):
                posebones.append(pbone)
    return posebones

def draw_item(self, context):
    layout = self.layout
    layout.menu(GE_Menu.bl_idname)

    
###########################
#GE SubMenu Functions here#
###########################

#Translate mesh from 3D cursor
class GE_TranslateCursor(bpy.types.Operator):
    """Translates a meshes position  to the opposite direction from the 3D Cursor coordinates. Uses Local coordinates"""
    bl_idname = "ge.translatecursor"
    bl_label = "Translate mesh from 3D Cursor"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if(len(bpy.context.selected_editable_objects) == 1):
            if(bpy.context.selected_editable_objects[0].type == 'MESH'):
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.transform.translate(value=(bpy.context.scene.cursor_location[0]*-1, bpy.context.scene.cursor_location[1]*-1, bpy.context.scene.cursor_location[2]*-1))
                bpy.ops.object.mode_set(mode = 'OBJECT')
                GE_Alert("Translated mesh successfully!", "GE: Translate from 3D Cursor")
            else:
                GE_Alert("Object must be a MESH!", "GE: Translate from 3D Cursor", "ERROR")
        else:
            GE_Alert("Only one mesh may be selected for this function!", "GE: Translate from 3D Cursor", "ERROR")
        return {'FINISHED'}

#Reset 3D Cursor to 0, 0, 0
class GE_ResetCursor(bpy.types.Operator):
    """Simply resets the 3D Cursor to the center of the screen"""
    bl_idname = "ge.resetcursor"
    bl_label = "Reset 3D Cursor to 0, 0, 0"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.context.scene.cursor_location[0] = 0.0
        bpy.context.scene.cursor_location[1] = 0.0
        bpy.context.scene.cursor_location[2] = 0.0
        return {'FINISHED'}

#Flip X
class GE_FlipX(bpy.types.Operator):
    """Mirrors a mesh from the X coordinate"""
    bl_idname = "ge.flipx"
    bl_label = "Flip Meshes X Axis"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        #Switch back to object mode if currently on something else
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except:
            pass
        
        #Loop through all selected objects
        sel_objs = [obj for obj in bpy.context.selected_editable_objects]
        bpy.ops.object.select_all(action='DESELECT')

        for obj in sel_objs:
            #Only do this to meshes though
            if(obj.type == 'MESH'):
                #Select the object
                bpy.context.scene.objects.active = obj
                obj.select = True
                #CHange to edit mode
                bpy.ops.object.mode_set(mode = 'EDIT')
                #Select all polygons
                bpy.ops.mesh.select_all(action='SELECT')
                #Mirror it
                bpy.ops.transform.resize(value=(-1, 1, 1), center_override=(0, 0, 0))
                #Invert the polygons from inside out
                bpy.ops.mesh.flip_normals()
                bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        GE_Alert("Updated " + str(len(sel_objs)) + " object(s)!", "GE: Flip X")
        return {'FINISHED'}

#Global To Local
class GE_GlobalToLocal(bpy.types.Operator):
    """Converts all global coordinates selected objects to their local equivalents"""
    bl_idname = "ge.globaltolocal"
    bl_label = "Convert Global to Local"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    #Script starts here
    def execute(self, context):        
        #Switch back to object mode if currently on something else
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except:
            pass

        #Object mode stuff
        sel_objs = [obj for obj in bpy.context.selected_editable_objects]
        bpy.ops.object.select_all(action='DESELECT')

        for obj in sel_objs:
            #Select current object
            bpy.context.scene.objects.active = obj
            obj.select = True    
            
            #Only mess with these type of objects
            if(obj.type == 'MESH' or obj.type == 'ARMATURE'):
                #Record all the global coordinates
                gx = obj.location[0]
                gy = obj.location[1]
                gz = obj.location[2]
                gpitch = obj.rotation_euler[0]
                gyaw = obj.rotation_euler[1]
                groll = obj.rotation_euler[2]
                gscalex = obj.scale[0]
                gscaley = obj.scale[1]
                gscalez = obj.scale[2]
                
                #Reset all global coordinates
                print("Resetting global coordinates")
                obj.location[0] = 0
                obj.location[1] = 0
                obj.location[2] = 0
                #Rotation (MESH only rn otherwise it breaks animations)
                #The B3D Exporter exports the armature 
                #properly despite with different global rotation coordinates anyway
                if(obj.type == 'MESH'):
                    obj.rotation_euler[0] = 0
                    obj.rotation_euler[1] = 0
                    obj.rotation_euler[2] = 0
                #Scale
                obj.scale[0] = 1
                obj.scale[1] = 1
                obj.scale[2] = 1
                
                #Switch to edit mode
                print("Switching to edit mode")
                bpy.ops.object.mode_set(mode='EDIT')

                #Select all + Rotation (MESH only here too otherwise it breaks animations like before)
                if(obj.type == 'MESH'):
                    print("Rotating mesh")
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.transform.rotate(value=(gpitch), axis=(1,0,0), center_override=(0, 0, 0))
                    bpy.ops.transform.rotate(value=(gyaw), axis=(0,1,0), center_override=(0, 0, 0))
                    bpy.ops.transform.rotate(value=(groll), axis=(0,0,1), center_override=(0, 0, 0))
                #Select all bones for armatures
                elif(obj.type == 'ARMATURE'):     
                    bpy.ops.armature.select_all(action='SELECT')
                
                #Scale
                print("Resizing")
                bpy.ops.transform.resize(value=(gscalex, gscaley, gscalez), center_override=(0, 0, 0))
                
                #XYZ Translate
                print("Translating")
                bpy.ops.transform.translate(value=(gx, gy, gz))
                
                #If it's an armature, fix animations after scaling
                if(obj.type == 'ARMATURE' and gscalex != 1 and gscaley != 1 and gscalez != 1):
                    print("Correcting armature scaling")
                    bpy.ops.object.mode_set(mode='EDIT')
                    kf = GE_GetKeyFrames(obj)
                    db = GE_GetDisconnectedBones(obj)
                    bpy.ops.object.mode_set(mode='POSE')
                    pb = GE_GetPBonesFromBones(obj, db)
                    
                    #Loop through all frames
                    for frame in kf:
                        bpy.context.scene.frame_set(frame)
                        #Loop through all pose bones
                        for pbone in pb[:]:
                            #Scale the XYZ positions of these lonely bones to what our scaler is
                            pbone.location[0] *= gscalex
                            pbone.location[1] *= gscaley
                            pbone.location[2] *= gscalez
                            
                        #Update the keyframe
                        bpy.ops.anim.keyframe_insert()
                        
            #Reset
            try:
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
            except:
                pass
        GE_Alert("Updated " + str(len(sel_objs)) + " object(s)!", "GE: Global To Local")
        return {'FINISHED'}
    
#Simply resets the pose, makes editing keyframes easier.
class GE_ResetPose(bpy.types.Operator):
    """Simply resets the pose of the selected armature in Pose Mode"""
    bl_idname = "ge.resetpose"
    bl_label = "Reset Pose"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if(bpy.context.active_object.type == "ARMATURE"):
            if(bpy.context.active_object.mode == "POSE"):
                for pbone in bpy.context.active_object.pose.bones[:]:
                        #Reset rotation to 0
                        pbone.rotation_quaternion[1] = 0
                        pbone.rotation_quaternion[2] = 0
                        pbone.rotation_quaternion[3] = 0
                        #Reset coordinates to 0 too
                        pbone.location[0] = 0
                        pbone.location[1] = 0
                        pbone.location[2] = 0
            else:
                GE_Alert("Only for use in pose mode!", "GE: Reset Pose", "ERROR")
        else:
            GE_Alert("Object must be an ARMATURE!", "GE: Reset Pose", "ERROR")

        return {'FINISHED'}

#Goes through each bone in an armature and resets its roll to 0.
#Should be done before you start animating, or things can be wacky
class GE_ClearRoll(bpy.types.Operator):
    """Sets each bone roll in an armature to 0.0"""
    bl_idname = "ge.clearroll"
    bl_label = "Clear Armature Roll"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if(bpy.context.active_object.type == "ARMATURE"):
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.armature.select_all(action='SELECT')
            bpy.ops.armature.roll_clear(roll=0.0)
            GE_Alert("Modified '" + bpy.context.active_object.name + "' to have 0.0 roll on all its bones!", "GE: Clear Armature Roll")
        else:
            GE_Alert("Object must be an ARMATURE!", "GE: Clear Armature Roll", "ERROR")

        return {'FINISHED'}


#Final Touches to GE Extras
def register():
    # Main Header
    bpy.utils.register_class(GE_Menu)
    bpy.types.INFO_HT_header.append(draw_item)
    
    #Sub functions
    bpy.utils.register_class(GE_TranslateCursor)
    bpy.utils.register_class(GE_ResetCursor)
    bpy.utils.register_class(GE_FlipX)
    bpy.utils.register_class(GE_GlobalToLocal)    
    bpy.utils.register_class(GE_ResetPose)
    bpy.utils.register_class(GE_ClearRoll)

def unregister():
    # Main Header
    bpy.utils.unregister_class(GE_Menu)
    bpy.types.INFO_HT_header.remove(draw_item)
    
    #Sub Functions
    bpy.utils.unregister_class(GE_TranslateCursor)
    bpy.utils.unregister_class(GE_ResetCursor)
    bpy.utils.unregister_class(GE_FlipX)
    bpy.utils.unregister_class(GE_GlobalToLocal)
    bpy.utils.unregister_class(GE_ResetPose)
    bpy.utils.unregister_class(GE_ClearRoll)

if __name__ == "__main__":
    register()
