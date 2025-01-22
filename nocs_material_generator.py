bl_info = {
    "name": "NOCS Material Generator",
    "blender": (2, 82, 0),  # Adjust for your Blender version
    "category": "Object",
    "author": "Hannes Reichert",
    "version": (1, 0, 0),
    "description": "Generate NOCS (Normalized Object Coordinate Space) textures for objects",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
}

import bpy
from mathutils import Vector


def create_nocs_texture_for_object(obj):
    """
    This function generates a NOCS (Normalized Object Coordinate Space) texture for the given object.
    
    :param obj: The object to generate NOCS for.
    """
    # Check if the object has geometry
    if len(obj.data.vertices) == 0 or len(obj.data.polygons) == 0:
        print(f"Skipping {obj.name} because it has no geometry.")
        return

    # 1. Compute the bounding box dimensions in local space
    bbox_corners = [Vector(corner) for corner in obj.bound_box]
    min_corner = Vector([min(corner[i] for corner in bbox_corners) for i in range(3)])
    max_corner = Vector([max(corner[i] for corner in bbox_corners) for i in range(3)])
    bbox_size = max_corner - min_corner

    # Ensure no zero division (handle flat objects)
    bbox_size = Vector([max(dim, 1e-6) for dim in bbox_size])

    # 2. Create a vertex color map to visualize the normalized object space
    if "NOCS" not in obj.data.vertex_colors:
        vcol_layer = obj.data.vertex_colors.new(name="NOCS")
    else:
        vcol_layer = obj.data.vertex_colors["NOCS"]

    for loop_index, loop in enumerate(obj.data.loops):
        loop_vert_index = loop.vertex_index
        vertex = obj.data.vertices[loop_vert_index]

        # Normalize vertex coordinates in object space
        normalized_coord = Vector([
	    (vertex.co.x - min_corner.x) / (max_corner.x - min_corner.x),
	    (vertex.co.y - min_corner.y) / (max_corner.y - min_corner.y),
	    (vertex.co.z - min_corner.z) / (max_corner.z - min_corner.z),
	])
        normalized_coord.x = max(0.0, min(1.0, normalized_coord.x))
        normalized_coord.y = max(0.0, min(1.0, normalized_coord.y))
        normalized_coord.z = max(0.0, min(1.0, normalized_coord.z))
        
        # Assign normalized coordinates as vertex colors (RGBA with alpha = 1.0)
        vcol_layer.data[loop_index].color = (normalized_coord.x, normalized_coord.y, normalized_coord.z, 1.0)

    obj.data.vertex_colors.active = vcol_layer

    # 3. Create and assign a new material to visualize the vertex colors
    mat_name = f"{obj.name}_NOCS_Material"
    if mat_name not in bpy.data.materials:
        mat = bpy.data.materials.new(mat_name)
        mat.use_nodes = True  # Enable shader nodes

        # Get the material nodes
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        # Add necessary nodes
        vertex_color_node = nodes.new(type='ShaderNodeAttribute')
        vertex_color_node.attribute_name = vcol_layer.name
        diffuse_shader = nodes.new(type='ShaderNodeBsdfDiffuse')
        output_shader = nodes.new(type='ShaderNodeOutputMaterial')

        # Link the nodes
        links.new(vertex_color_node.outputs["Color"], diffuse_shader.inputs["Color"])
        links.new(diffuse_shader.outputs["BSDF"], output_shader.inputs["Surface"])
    else:
        mat = bpy.data.materials[mat_name]

    # Assign the material to the object
    obj.data.materials.append(mat)

    return obj


class NOCSMaterialOperator(bpy.types.Operator):
    """Generate and assign a NOCS material to the selected object"""
    bl_idname = "object.create_nocs_material"
    bl_label = "Create NOCS Material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Apply only to the selected object
        obj = context.active_object
        if obj and obj.type == 'MESH':
            create_nocs_texture_for_object(obj)
            self.report({'INFO'}, f"Created NOCS material for {obj.name}.")
        else:
            self.report({'ERROR'}, "No mesh object selected.")
            return {'CANCELLED'}
        
        return {'FINISHED'}


class NOCSMaterialPanel(bpy.types.Panel):
    """Creates a Panel in the Sidebar to generate NOCS materials"""
    bl_label = "NOCS Material Generator"
    bl_idname = "VIEW3D_PT_nocs_material_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "NOCS"  # This will create a new tab called 'NOCS' in the Sidebar

    def draw(self, context):
        layout = self.layout

        # Add description
        layout.label(text="Generate NOCS material to visualize object space.")

        # Button to generate NOCS material
        layout.operator("object.create_nocs_material", text="Generate NOCS Material")


def register():
    bpy.utils.register_class(NOCSMaterialOperator)
    bpy.utils.register_class(NOCSMaterialPanel)


def unregister():
    bpy.utils.unregister_class(NOCSMaterialOperator)
    bpy.utils.unregister_class(NOCSMaterialPanel)


if __name__ == "__main__":
    register()

