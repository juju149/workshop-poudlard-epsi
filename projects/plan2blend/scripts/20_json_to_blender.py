#!/usr/bin/env blender -P
"""
Script 20: Generate Blender 3D model from floorplan JSON.

This script uses Blender Python API (bpy) to create a 3D building model.

Usage:
    blender -b -P 20_json_to_blender.py -- input.json output.blend --wall_thickness 0.20 --wall_height 2.80
"""

import sys
import os
import json
import math

# Find the '--' separator to get script arguments
try:
    argv = sys.argv[sys.argv.index("--") + 1:]
except ValueError:
    argv = []

# Parse arguments
if len(argv) < 2:
    print("Usage: blender -b -P 20_json_to_blender.py -- input.json output.blend [--wall_thickness 0.20] [--wall_height 2.80]")
    sys.exit(1)

input_json = argv[0]
output_blend = argv[1]
wall_thickness = 0.20  # Default 20cm
wall_height = 2.80     # Default 2.80m

# Parse optional arguments
for i, arg in enumerate(argv):
    if arg == '--wall_thickness' and i + 1 < len(argv):
        wall_thickness = float(argv[i + 1])
    elif arg == '--wall_height' and i + 1 < len(argv):
        wall_height = float(argv[i + 1])

print(f"Loading floorplan from: {input_json}")
print(f"Wall thickness: {wall_thickness}m")
print(f"Wall height: {wall_height}m")
print(f"Output: {output_blend}")

try:
    import bpy
    import bmesh
    from mathutils import Vector
except ImportError:
    print("Error: This script must be run with Blender's Python")
    print("Example: blender -b -P 20_json_to_blender.py -- input.json output.blend")
    sys.exit(1)


def load_json(filepath):
    """Load JSON data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def clear_scene():
    """Clear all objects from the scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()


def create_material(name, color, alpha=1.0):
    """Create a simple material."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Create nodes
    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    
    # Set color
    node_bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    node_bsdf.inputs['Alpha'].default_value = alpha
    
    # Link nodes
    mat.node_tree.links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])
    
    return mat


def create_wall_from_polygon(polygon, thickness, height, name="Wall"):
    """
    Create a wall mesh from a polygon with given thickness and height.
    
    Args:
        polygon: List of [x, y] coordinates
        thickness: Wall thickness in meters
        height: Wall height in meters
        name: Object name
    
    Returns:
        Created object
    """
    # Create mesh and object
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    # Create mesh from polygon
    bm = bmesh.new()
    
    # Create bottom vertices
    bottom_verts = []
    for x, y in polygon:
        v = bm.verts.new((x, y, 0))
        bottom_verts.append(v)
    
    # Create bottom face
    if len(bottom_verts) >= 3:
        bm.faces.new(bottom_verts)
    
    # Update mesh
    bm.to_mesh(mesh)
    bm.free()
    
    # Select the object
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Extrude to create walls
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, height)})
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Add solidify modifier for wall thickness
    solidify = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = thickness
    solidify.offset = 0
    
    return obj


def create_floor_from_polygon(polygon, thickness, z_offset, name="Floor"):
    """
    Create a floor slab from a polygon.
    
    Args:
        polygon: List of [x, y] coordinates
        thickness: Floor thickness in meters
        z_offset: Z position
        name: Object name
    
    Returns:
        Created object
    """
    # Create mesh and object
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    # Create mesh from polygon
    bm = bmesh.new()
    
    # Create vertices at z_offset
    verts = []
    for x, y in polygon:
        v = bm.verts.new((x, y, z_offset))
        verts.append(v)
    
    # Create face
    if len(verts) >= 3:
        bm.faces.new(verts)
    
    # Update mesh
    bm.to_mesh(mesh)
    bm.free()
    
    # Extrude downward for thickness
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, -thickness)})
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return obj


def create_opening_cutter(start, end, width, height, z_offset, opening_type="door"):
    """
    Create a boolean cutter for doors or windows.
    
    Args:
        start: [x, y] start point
        end: [x, y] end point
        width: Opening width (for thickness)
        height: Opening height
        z_offset: Z offset (for windows)
        opening_type: 'door' or 'window'
    
    Returns:
        Created cutter object
    """
    # Calculate position and rotation
    start_v = Vector((start[0], start[1], 0))
    end_v = Vector((end[0], end[1], 0))
    
    center = (start_v + end_v) / 2
    direction = end_v - start_v
    length = direction.length
    
    # Calculate rotation
    angle = math.atan2(direction.y, direction.x)
    
    # Create cube
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(center.x, center.y, z_offset + height/2)
    )
    cutter = bpy.context.active_object
    cutter.name = f"Cutter_{opening_type}"
    
    # Scale to opening dimensions
    cutter.scale = (length, width * 2, height)  # Width * 2 for wall thickness
    cutter.rotation_euler = (0, 0, angle)
    
    # Apply transformations
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    
    return cutter


def apply_boolean_difference(target, cutter):
    """Apply boolean difference modifier."""
    modifier = target.modifiers.new(name="Boolean", type='BOOLEAN')
    modifier.operation = 'DIFFERENCE'
    modifier.object = cutter
    
    # Hide the cutter
    cutter.hide_render = True
    cutter.hide_viewport = True


def create_camera(location, rotation, name="Camera"):
    """Create a camera."""
    bpy.ops.object.camera_add(location=location, rotation=rotation)
    camera = bpy.context.active_object
    camera.name = name
    return camera


def create_light(location, energy=1000, name="Light"):
    """Create a light source."""
    bpy.ops.object.light_add(type='POINT', location=location)
    light = bpy.context.active_object
    light.name = name
    light.data.energy = energy
    return light


def process_floorplan(data, wall_thickness, wall_height):
    """
    Process floorplan JSON and create 3D model.
    
    Args:
        data: Floorplan JSON data
        wall_thickness: Wall thickness in meters
        wall_height: Wall height in meters
    """
    # Clear scene
    clear_scene()
    
    # Set units to meters
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.length_unit = 'METERS'
    
    # Create materials
    mat_wall = create_material("Wall", (0.9, 0.9, 0.85))
    mat_floor = create_material("Floor", (0.6, 0.6, 0.6))
    mat_opening = create_material("Opening", (0.7, 0.5, 0.3))
    
    # Process each floor
    for floor_idx, floor in enumerate(data.get('floors', [])):
        floor_code = floor.get('code', f'FLOOR_{floor_idx}')
        print(f"Processing floor: {floor_code}")
        
        # Create collection for this floor
        collection = bpy.data.collections.new(floor_code)
        bpy.context.scene.collection.children.link(collection)
        
        z_offset = floor_idx * wall_height
        
        # Process each room
        for room_idx, room in enumerate(floor.get('rooms', [])):
            room_name = room.get('name', f'ROOM_{room_idx}')
            polygon = room.get('polygon', [])
            
            if len(polygon) < 3:
                print(f"Warning: Room {room_name} has invalid polygon")
                continue
            
            print(f"  Creating room: {room_name}")
            
            # Create walls
            wall = create_wall_from_polygon(
                polygon, wall_thickness, wall_height,
                name=f"{room_name}_Walls"
            )
            wall.data.materials.append(mat_wall)
            
            # Move to collection
            for coll in wall.users_collection:
                coll.objects.unlink(wall)
            collection.objects.link(wall)
            
            # Create floor
            floor_obj = create_floor_from_polygon(
                polygon, 0.20, z_offset,
                name=f"{room_name}_Floor"
            )
            floor_obj.data.materials.append(mat_floor)
            
            # Move to collection
            for coll in floor_obj.users_collection:
                coll.objects.unlink(floor_obj)
            collection.objects.link(floor_obj)
            
            # Process doors
            features = room.get('features', {})
            for door_idx, door in enumerate(features.get('doors', [])):
                start = door.get('start', [0, 0])
                end = door.get('end', [0, 0])
                width = door.get('width', 1.0)
                
                cutter = create_opening_cutter(
                    start, end, wall_thickness, 2.05, z_offset,
                    opening_type=f"door_{door_idx}"
                )
                
                # Move to collection
                for coll in cutter.users_collection:
                    coll.objects.unlink(cutter)
                collection.objects.link(cutter)
                
                # Apply boolean
                apply_boolean_difference(wall, cutter)
            
            # Process windows
            for window_idx, window in enumerate(features.get('windows', [])):
                start = window.get('start', [0, 0])
                end = window.get('end', [0, 0])
                height = window.get('height', 1.1)
                sill_height = window.get('sill_height', 0.9)
                
                cutter = create_opening_cutter(
                    start, end, wall_thickness, height, z_offset + sill_height,
                    opening_type=f"window_{window_idx}"
                )
                
                # Move to collection
                for coll in cutter.users_collection:
                    coll.objects.unlink(cutter)
                collection.objects.link(cutter)
                
                # Apply boolean
                apply_boolean_difference(wall, cutter)
    
    # Add cameras
    create_camera(
        location=(10, -10, 15),
        rotation=(math.radians(60), 0, math.radians(45)),
        name="Camera_Perspective"
    )
    
    create_camera(
        location=(0, 0, 30),
        rotation=(0, 0, 0),
        name="Camera_Top"
    )
    
    # Add lights
    create_light(location=(10, -10, 20), energy=2000, name="Light_Main")
    create_light(location=(-10, 10, 15), energy=1000, name="Light_Fill")


def export_gltf(blend_path):
    """Export to glTF format."""
    gltf_path = blend_path.replace('.blend', '.glb')
    
    try:
        # Select all visible objects
        bpy.ops.object.select_all(action='SELECT')
        
        # Export to glTF
        bpy.ops.export_scene.gltf(
            filepath=gltf_path,
            export_format='GLB',
            use_selection=False
        )
        print(f"✓ Exported glTF: {gltf_path}")
    except Exception as e:
        print(f"Warning: Could not export glTF: {e}")


# Main execution
def main():
    # Load JSON
    try:
        data = load_json(input_json)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        sys.exit(1)
    
    # Process floorplan
    process_floorplan(data, wall_thickness, wall_height)
    
    # Save blend file
    os.makedirs(os.path.dirname(output_blend) or '.', exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=output_blend)
    print(f"✓ Blend file saved: {output_blend}")
    
    # Export glTF
    export_gltf(output_blend)


if __name__ == '__main__':
    main()
