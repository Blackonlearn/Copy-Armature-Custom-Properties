# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy

bl_info = {
    "name": "Copy Armature Custom Properties",
    "author": "BongQhi",
    "version": (1, 0, 1),
    "blender": (2, 80, 0),
    "location": "Object > Custom Properties Copy > Copy Armature Custom Properties",
    "description": "Copies custom properties from active armature data to selected armatures",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

def set_prop(data, name, value):
    data[name] = value

def get_props(data):
    names = list(set(data.keys()) - set(('_RNA_UI',)))
    values = [(name, data[name]) for name in names]
    return values

class CopyArmatureCustomProperties(bpy.types.Operator):
    """Copy Custom Properties from Active Armature Data to Selected Armatures"""
    bl_idname = "object.armature_custom_property_copy"
    bl_label = "Copy Armature Custom Properties"

    @classmethod
    def poll(cls, context):
        active = context.active_object
        return active and active.type == 'ARMATURE'

    def execute(self, context):
        active = bpy.context.active_object
        selected = [
            obj for obj in bpy.context.selected_objects
            if obj.type == 'ARMATURE' and obj != active
        ]

        if not selected:
            self.report({'WARNING'}, "No other selected armatures to copy to.")
            return {'CANCELLED'}

        for ob in selected:
            for name, value in get_props(active.data):
                set_prop(ob.data, name, value)

        self.report({'INFO'}, f"Copied properties to {len(selected)} armatures.")
        return {'FINISHED'}

class ArmatureCopyPanel(bpy.types.Panel):
    """Creates a Custom Property Panel in the Object properties window"""
    bl_label = "Armature Data Custom Properties"
    bl_idname = "OBJECT_PT_armature_customprop"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"  # This places the panel in the "Data" tab

    def draw(self, context):
        layout = self.layout
        layout.operator("object.armature_custom_property_copy")

def register():
    bpy.utils.register_class(CopyArmatureCustomProperties)
    bpy.utils.register_class(ArmatureCopyPanel)

def unregister():
    bpy.utils.unregister_class(ArmatureCopyPanel)
    bpy.utils.unregister_class(CopyArmatureCustomProperties)

if __name__ == "__main__":
    register()
