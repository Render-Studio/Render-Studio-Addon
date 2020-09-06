bl_info = {
    "name": "Render Studio",
    "description": "Render Studio",
    "author": "DJABHipHop",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "3D View > Render Studio",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Render"
}
import logging
import os

import bpy, bmesh

def get_data_path():
    addon_directory = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(addon_directory, "data")
    return data_dir

def get_blendlibrary_path():
    data_path = get_data_path()
    if data_path:
        return os.path.join(data_path, "Render_Studio.blend")


def init_light_controller(self, context):
    #Light_SRC
    
    # Init Laynot
    layout = self.layout
    
    # Get Object By Name
    obj = context

    # Gat Collections By Name.
    rs = bpy.data.collections.get("Render Studio")
    
    # Gat Object By Name
    ls = bpy.data.objects.get(obj.name_full)
    
    # Gat Materials By Name
    lsm = bpy.data.materials.get(obj.name_full)
    
    # Check to see if the collection had Not Been Delete, Renamed.
    if rs is not None:
        # Check to see if the object had Not Been Delete, Renamed.
        if ls is not None:
            # Check to see if the materials had Not Been Delete, Swaped, Renamed, Altered, Or Replaced.
            if lsm is not None:
                # Create a Lighting Ajustment Controls.
                # Get Nodes By Name.
                lsmn = lsm.node_tree.nodes["Emission"]
                lsc = layout.column()
                lsc.use_property_split = False
                lsc.label(text=obj.name, icon='LIGHT')
                lsc.prop(lsmn.inputs[0], "default_value", text="Color")
                lsc.prop(lsmn.inputs[1], "default_value", text="Strength")
        lsc.prop(obj, 'location')

def init_camera_controller(self, context):
    #Light_SRC
    
    # Init Laynot
    layout = self.layout
    
    # Get Object By Name
    obj = context

    # Gat Collections By Name.
    rs = bpy.data.collections.get("Render Studio")
    
    # Gat Object By Name
    cam = bpy.data.objects.get(obj.name_full)
    
    # Check to see if the collection had Not Been Delete, Renamed.
    if rs is not None:
        # Check to see if the object had Not Been Delete, Renamed.
        if cam is not None:
            # Create a Lighting Ajustment Controls.
            cam = layout.column()
            cam.use_property_split = False
            cam.label(text=obj.name, icon='VIEW_CAMERA')
            cam.prop(obj, 'location')

class AddRenderStudioOperator(bpy.types.Operator):
    bl_idname = "scene.add_render_studio_operator"
    bl_label = "Add Render Studio"

    def execute(self, context):
    
        lib_filepath = get_blendlibrary_path()
        directory = os.path.join(lib_filepath, "Collection/")
    
        bpy.ops.wm.append(filepath=lib_filepath, directory=directory, filename="Render Studio")

        return {'FINISHED'}

class RenderStudioPanel(bpy.types.Panel):
    bl_label = "Create"
    bl_idname = "RS_PT_CREAT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Render Studio"
    bl_icon='OUTLINER_OB_MESH'

    def draw(self, context):
        # self.layout
        layout = self.layout
        
        # context.scene
        scene = context.scene
        
        # context.object
        obj = context.object
        
        # Create a Creat Sections.
        add = layout.column()
        add.use_property_split = False
#        add.label(text="Create/Edit:",icon='OUTLINER_OB_MESH')
        add.operator("scene.add_render_studio_operator", icon="SHADING_RENDERED")

class RenderStudeoCamerasPanel(bpy.types.Panel):
    bl_label = "Cameras"
    bl_idname = "RS_PT_CAMERAS"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Render Studio"
    bl_icon='OBJECT_DATA'
    
    def draw(self, context):
        # self.layout
        
        layout = self.layout
        
        scene = context.scene
        
        cam = layout.column()
        cam.use_property_split = False
        cam.label(text="Select Camere", icon='VIEW_CAMERA')
        cam.prop(scene, "camera")
        
        init_camera_controller(self, context.scene.objects['Fromt_Camera'])
        
        init_camera_controller(self, context.scene.objects['Fromt_Camera_45'])

        init_camera_controller(self, context.scene.objects['Left_Camera'])

        init_camera_controller(self, context.scene.objects['Right_Camera'])


class RenderStudeoLightingPanel(bpy.types.Panel):
    bl_label = "Lighting"
    bl_idname = "RS_PT_LIGHTING"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Render Studio"
    bl_icon='OBJECT_DATA'
    
    def draw(self, context):
        # self.layout
        layout = self.layout
        
        init_light_controller(self, context.scene.objects['Master_Light'])
        
        init_light_controller(self, context.scene.objects['Light_Source_Left'])
         
        init_light_controller(self, context.scene.objects['Light_Source_Front'])
        
        init_light_controller(self, context.scene.objects['Light_Source_Right'])

class RenderStudioBackDropPanel(bpy.types.Panel):
    bl_label = "Back Drop"
    bl_idname = "RS_PT_BACK_DROP"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Render Studio"
    bl_icon='NODE_MATERIAL'
    
    def draw(self, context):
        # self.layout
        layout = self.layout

        # Gat Collections By Name.
        rs = bpy.data.collections.get("Render Studio")
        
        # Gat Objects By Name
        bd = bpy.data.objects.get("Back_Drop")
        
        # Gat Materials By Name
        bdm = bpy.data.materials.get("Back_Drop")

        # Check to see if the collection had Not Been Delete, Renamed.
        if rs is not None:
        # Check to see if the object had Not Been Delete, Renamed.
            if bd is not None:
                # Create a Scale Sections.
                scale = layout.column()
                scale.use_property_split = False
                scale.label(text="Scale:", icon="OBJECT_DATA")
                scale.prop(bd.modifiers["X"], 'threshold', text="X:")
                scale.prop(bd.modifiers["Y"], 'threshold', text="Y:")
                scale.prop(bd.modifiers["Z"], 'threshold', text="Z:")

                #Create a Bevel Sections.
                bevel = layout.column()
                bevel.use_property_split = False
                bevel.label(text="Shape:", icon="MOD_BEVEL")
                bevel.prop(bd.modifiers["Bevel"], 'width_pct')
                bevel.prop(bd.modifiers["Bevel"], 'segments')
                bevel.prop(bd.modifiers["Bevel"], 'profile', text="Shape:")

                # Check to see if the material had Not Been Delete, Swaped, Renamed, Altered, Or Replaced.
                if bdm is not None:

                    # Create a Material Ajustment Sections.
                    material = layout.column()
                    material.use_property_split = False
                    material.prop(bdm, "use_nodes", icon='NODETREE')
                    if bdm.use_nodes:
                        # Get Nodes By Name.
                        bdmn = bdm.node_tree.nodes["Principled BSDF"]
                        material.prop(bdmn, "distribution", text="")
                        material.prop(bdmn, "subsurface_method", text="")
                        material.prop(bdmn.inputs[0], "default_value", text="Base Color")
                        material.prop(bdmn.inputs[1], "default_value", text="Subsurface")
                        material.prop(bdmn.inputs[2], "default_value", text="Subsurface Radius")
                        material.prop(bdmn.inputs[3], "default_value", text="Subsurface Color")
                        material.prop(bdmn.inputs[5], "default_value", text="Metallic")
                        material.prop(bdmn.inputs[6], "default_value", text="Roughness")
                        material.prop(bdmn.inputs[14], "default_value", text="IOR")
                        material.prop(bdmn.inputs[17], "default_value", text="Emission")
                        material.prop(bdmn.inputs[18], "default_value", text="Alpha")
                    else:
                        material.prop(bdm, "diffuse_color", text="Base Color")
                        material.prop(bdm, "metallic")
                        material.prop(bdm, "specular_intensity", text="Specular")
                        material.prop(bdm, "roughness")

def register():
    bpy.utils.register_class(RenderStudioPanel)
    bpy.utils.register_class(RenderStudeoCamerasPanel)
    bpy.utils.register_class(RenderStudeoLightingPanel)
    bpy.utils.register_class(RenderStudioBackDropPanel)
    bpy.utils.register_class(AddRenderStudioOperator)
    bpy.utils.register_class(ToggleEditModeOperator)

def unregister():
    bpy.utils.unregister_class(RenderStudioPanel)
    bpy.utils.unregister_class(RenderStudeoCamerasPanel)
    bpy.utils.unregister_class(RenderStudeoLightingPanel)
    bpy.utils.unregister_class(RenderStudioBackDropPanel)
    bpy.utils.unregister_class(AddRenderStudioOperator)
    bpy.utils.unregister_class(ToggleEditModeOperator)


if __name__ == "__main__":
    register()

