bl_info = {
    "name": "Vertex Group batch rename",
    "author": "Torusxo",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Properties > Object Data > Vertex Groups",
    "description": "Find and replace characters in vertex groups, and add prefix/suffix.",
    "category": "Object",
}

import bpy


class VertexGroupModifierProps(bpy.types.PropertyGroup):
    prefix: bpy.props.StringProperty(name="Prefix")
    suffix: bpy.props.StringProperty(name="Suffix")
    find: bpy.props.StringProperty(name="Find")
    replace: bpy.props.StringProperty(name="Replace")


def main(context, props):
    for i in context.object.vertex_groups:
        old_name = i.name
        
        # Find and Replace
        new_name = old_name.replace(props.find, props.replace)
        
        # Add Prefix/Suffix
        prefix = props.prefix
        suffix = props.suffix
        new_name = prefix + new_name + suffix
        
        i.name = new_name


class OBJECT_OT_vertex_group_modifier(bpy.types.Operator):
    bl_idname = "object.vertex_group_modifier"
    bl_label = "Vertex Group Modifier"
    bl_description = "Find and replace characters in vertex groups, and add prefix/suffix."
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.vertex_group_modifier_props
        main(context, props)
        return {'FINISHED'}


def draw_vertex_group_modifier(self, context):
    layout = self.layout
    
    props = context.scene.vertex_group_modifier_props
    
    col = layout.column()
    col.prop(props, "prefix")
    col.prop(props, "suffix")
    col.prop(props, "find")
    col.prop(props, "replace")
    
    row = layout.row()
    row.operator(OBJECT_OT_vertex_group_modifier.bl_idname, text="Apply")


def register():
    bpy.utils.register_class(VertexGroupModifierProps)
    bpy.utils.register_class(OBJECT_OT_vertex_group_modifier)
    
    bpy.types.Scene.vertex_group_modifier_props = bpy.props.PointerProperty(type=VertexGroupModifierProps)
    bpy.types.DATA_PT_vertex_groups.append(draw_vertex_group_modifier)


def unregister():
    bpy.utils.unregister_class(VertexGroupModifierProps)
    bpy.utils.unregister_class(OBJECT_OT_vertex_group_modifier)
    
    bpy.types.DATA_PT_vertex_groups.remove(draw_vertex_group_modifier)
    del bpy.types.Scene.vertex_group_modifier_props


if __name__ == "__main__":
    register()
