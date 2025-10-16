#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blender integration script for ML Plan2Blend.
Converts floorplan JSON to Blender .blend and .glb files.

Usage:
    blender -b -P json_to_blender.py -- input.json output.blend [options]
"""
import json
import math
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional

# Blender imports (available when run inside Blender)
try:
    import bpy
    import bmesh
    from mathutils import Vector
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False
    print("Warning: bpy not available. This script must be run inside Blender.")


def clear_scene():
    """Clear all objects from scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Clear collections
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)


def set_units_to_meters():
    """Set Blender units to meters."""
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.length_unit = 'METERS'
    bpy.context.scene.unit_settings.scale_length = 1.0


def create_wall_mesh(polygon: List[Tuple[float, float]], 
                    thickness: float = 0.20,
                    height: float = 2.80,
                    name: str = "Wall") -> bpy.types.Object:
    """
    Create wall mesh from 2D polygon.
    
    Args:
        polygon: List of (x, y) points defining wall centerline
        thickness: Wall thickness in meters
        height: Wall height in meters
        name: Object name
    
    Returns:
        Blender wall object
    """
    # Create mesh and object
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    
    # Link to scene
    bpy.context.collection.objects.link(obj)
    
    # Create bmesh
    bm = bmesh.new()
    
    # Create bottom face from polygon
    verts_bottom = []
    for x, y in polygon:
        v = bm.verts.new((x, y, 0.0))
        verts_bottom.append(v)
    
    # Create bottom face
    if len(verts_bottom) >= 3:
        bm.faces.new(verts_bottom)
    
    # Update bmesh
    bm.to_mesh(mesh)
    bm.free()
    
    # Add solidify modifier for thickness
    solidify = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = thickness
    solidify.offset = 0  # Centered
    
    # Extrude upward
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    bpy.ops.object.modifier_apply(modifier="Solidify")
    
    # Extrude to height
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value": (0, 0, height)}
    )
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return obj


def create_simple_wall_extrusion(polygon: List[Tuple[float, float]],
                                 thickness: float = 0.20,
                                 height: float = 2.80,
                                 name: str = "Wall") -> bpy.types.Object:
    """
    Create wall with simple extrusion (more stable than solidify).
    
    Args:
        polygon: List of (x, y) points
        thickness: Wall thickness
        height: Wall height
        name: Object name
    
    Returns:
        Blender object
    """
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    
    # Create vertices at bottom
    verts_bottom = []
    for x, y in polygon:
        v = bm.verts.new((x, y, 0.0))
        verts_bottom.append(v)
    
    # Create vertices at top
    verts_top = []
    for x, y in polygon:
        v = bm.verts.new((x, y, height))
        verts_top.append(v)
    
    # Create faces
    n = len(verts_bottom)
    
    # Bottom face
    if n >= 3:
        bm.faces.new(verts_bottom)
    
    # Top face
    if n >= 3:
        bm.faces.new(reversed(verts_top))
    
    # Side faces
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([
            verts_bottom[i],
            verts_bottom[j],
            verts_top[j],
            verts_top[i]
        ])
    
    bm.to_mesh(mesh)
    bm.free()
    
    return obj


def create_door_cutter(pos: List[List[float]], 
                      width: float,
                      height: float = 2.10,
                      name: str = "DoorCutter") -> bpy.types.Object:
    """
    Create boolean cutter for door opening.
    
    Args:
        pos: Door position [[x1, y1], [x2, y2]]
        width: Door width
        height: Door height
        name: Object name
    
    Returns:
        Cutter object
    """
    p1, p2 = pos[0], pos[1]
    cx = (p1[0] + p2[0]) / 2
    cy = (p1[1] + p2[1]) / 2
    
    # Create cube as cutter
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(cx, cy, height / 2)
    )
    obj = bpy.context.active_object
    obj.name = name
    
    # Scale to door size
    obj.scale = (width, 0.1, height)
    
    # Hide cutter
    obj.hide_set(True)
    obj.hide_render = True
    
    return obj


def create_window_cutter(pos: List[List[float]],
                        width: float,
                        height: float = 1.20,
                        sill: float = 0.90,
                        name: str = "WindowCutter") -> bpy.types.Object:
    """
    Create boolean cutter for window opening.
    
    Args:
        pos: Window position [[x1, y1], [x2, y2]]
        width: Window width
        height: Window height
        sill: Sill height from floor
        name: Object name
    
    Returns:
        Cutter object
    """
    p1, p2 = pos[0], pos[1]
    cx = (p1[0] + p2[0]) / 2
    cy = (p1[1] + p2[1]) / 2
    
    # Create cube as cutter
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(cx, cy, sill + height / 2)
    )
    obj = bpy.context.active_object
    obj.name = name
    
    # Scale to window size
    obj.scale = (width, 0.1, height)
    
    # Hide cutter
    obj.hide_set(True)
    obj.hide_render = True
    
    return obj


def create_floor_slab(polygon: List[Tuple[float, float]],
                     thickness: float = 0.20,
                     z_offset: float = 0.0,
                     name: str = "Floor") -> bpy.types.Object:
    """
    Create floor slab from polygon.
    
    Args:
        polygon: Floor boundary
        thickness: Slab thickness
        z_offset: Z position
        name: Object name
    
    Returns:
        Floor object
    """
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    
    # Create vertices
    verts = []
    for x, y in polygon:
        v = bm.verts.new((x, y, z_offset))
        verts.append(v)
    
    # Create face
    if len(verts) >= 3:
        bm.faces.new(verts)
    
    bm.to_mesh(mesh)
    bm.free()
    
    # Add solidify for thickness
    solidify = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = -thickness
    solidify.offset = 1.0
    
    return obj


def apply_boolean_difference(target: bpy.types.Object, 
                            cutter: bpy.types.Object) -> None:
    """
    Apply boolean difference operation.
    
    Args:
        target: Object to cut
        cutter: Cutting object
    """
    modifier = target.modifiers.new(name="Boolean", type='BOOLEAN')
    modifier.operation = 'DIFFERENCE'
    modifier.object = cutter
    modifier.solver = 'EXACT'
    
    # Apply modifier
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier="Boolean")


def create_floorplan_3d(data: Dict, 
                       wall_thickness: float = 0.20,
                       wall_height: float = 2.80) -> None:
    """
    Create complete 3D model from floorplan JSON.
    
    Args:
        data: Floorplan JSON data
        wall_thickness: Default wall thickness
        wall_height: Default wall height
    """
    clear_scene()
    set_units_to_meters()
    
    floors = data.get('floors', [])
    
    for floor_idx, floor in enumerate(floors):
        floor_code = floor.get('code', f'Floor{floor_idx}')
        print(f"Processing floor: {floor_code}")
        
        # Create collection for this floor
        collection = bpy.data.collections.new(floor_code)
        bpy.context.scene.collection.children.link(collection)
        
        # Calculate Z offset
        z_offset = floor_idx * wall_height
        
        # Create walls
        walls = floor.get('walls', [])
        wall_objects = []
        
        for i, wall in enumerate(walls):
            poly = wall.get('poly', [])
            if len(poly) < 3:
                continue
            
            # Convert to tuples and offset Z
            poly_3d = [(p[0], p[1]) for p in poly]
            
            wall_obj = create_simple_wall_extrusion(
                poly_3d,
                thickness=wall_thickness,
                height=wall_height,
                name=f"{floor_code}_Wall_{i}"
            )
            
            # Move to correct Z
            wall_obj.location.z = z_offset
            
            wall_objects.append(wall_obj)
            
            # Move to floor collection
            bpy.context.collection.objects.unlink(wall_obj)
            collection.objects.link(wall_obj)
        
        print(f"  Created {len(wall_objects)} walls")
        
        # Create doors
        doors = floor.get('doors', [])
        for i, door in enumerate(doors):
            pos = door.get('pos', [[0, 0], [0, 0]])
            width = door.get('width', 0.90)
            
            cutter = create_door_cutter(
                pos, width,
                height=2.10,
                name=f"{floor_code}_DoorCutter_{i}"
            )
            cutter.location.z = z_offset
            
            # Apply to nearby walls
            # (simplified - in production would check proximity)
            if wall_objects:
                apply_boolean_difference(wall_objects[0], cutter)
                bpy.data.objects.remove(cutter)
        
        print(f"  Created {len(doors)} doors")
        
        # Create windows
        windows = floor.get('windows', [])
        for i, window in enumerate(windows):
            pos = window.get('pos', [[0, 0], [0, 0]])
            width = window.get('width', 1.20)
            sill = window.get('sill', 0.90)
            
            cutter = create_window_cutter(
                pos, width,
                height=1.20,
                sill=sill,
                name=f"{floor_code}_WindowCutter_{i}"
            )
            cutter.location.z = z_offset
            
            # Apply to nearby walls
            if wall_objects:
                apply_boolean_difference(wall_objects[0], cutter)
                bpy.data.objects.remove(cutter)
        
        print(f"  Created {len(windows)} windows")
        
        # Create floor slabs for rooms
        rooms = floor.get('rooms', [])
        for i, room in enumerate(rooms):
            poly = room.get('poly', [])
            if len(poly) < 3:
                continue
            
            poly_2d = [(p[0], p[1]) for p in poly]
            
            slab = create_floor_slab(
                poly_2d,
                thickness=0.20,
                z_offset=z_offset,
                name=f"{floor_code}_Slab_{i}"
            )
            
            # Move to collection
            bpy.context.collection.objects.unlink(slab)
            collection.objects.link(slab)
        
        print(f"  Created {len(rooms)} floor slabs")
    
    # Add camera
    bpy.ops.object.camera_add(location=(0, 0, 10))
    camera = bpy.context.active_object
    camera.name = "Camera_TopView"
    camera.rotation_euler = (0, 0, 0)
    
    # Add light
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    light = bpy.context.active_object
    light.name = "Sun"
    
    print("✓ 3D model created successfully")


def main():
    """Main entry point."""
    if not BLENDER_AVAILABLE:
        print("Error: This script must be run inside Blender")
        print("Usage: blender -b -P json_to_blender.py -- input.json output.blend")
        sys.exit(1)
    
    # Parse arguments after --
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        print("Usage: blender -b -P json_to_blender.py -- input.json output.blend [options]")
        sys.exit(1)
    
    if len(argv) < 2:
        print("Error: input.json and output.blend are required")
        sys.exit(1)
    
    input_json = argv[0]
    output_blend = argv[1]
    
    # Optional parameters
    wall_thickness = 0.20
    wall_height = 2.80
    
    for i in range(2, len(argv)):
        if argv[i] == '--wall_thickness' and i + 1 < len(argv):
            wall_thickness = float(argv[i + 1])
        elif argv[i] == '--wall_height' and i + 1 < len(argv):
            wall_height = float(argv[i + 1])
    
    print(f"Loading JSON: {input_json}")
    
    # Load JSON
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create 3D model
    print("Creating 3D model...")
    create_floorplan_3d(data, wall_thickness, wall_height)
    
    # Save .blend
    print(f"Saving .blend file: {output_blend}")
    bpy.ops.wm.save_as_mainfile(filepath=output_blend)
    
    # Export .glb
    output_glb = str(Path(output_blend).with_suffix('.glb'))
    print(f"Exporting .glb file: {output_glb}")
    bpy.ops.export_scene.gltf(
        filepath=output_glb,
        export_format='GLB',
        use_selection=False
    )
    
    print("✓ Complete!")


if __name__ == "__main__":
    main()
