#!/usr/bin/env python3
"""
DÉFI 8: OÙ EST LA CHAMBRE DES SECRETS ? – Plan 3D animé (Blender)
Script Blender pour générer un plan 3D de Poudlard avec la Chambre des Secrets mise en évidence.

Usage:
    blender --background --python build_hogwarts_plan.py
    ou
    blender hogwarts_plan.blend --python build_hogwarts_plan.py
"""

import bpy
import math
from mathutils import Vector

# ============================================================================
# CONFIGURATION & PARAMÈTRES GLOBAUX
# ============================================================================

# Dimensions de base
WALL_THICKNESS = 0.3
WALL_HEIGHT = 3.0
DOOR_WIDTH = 1.0
DOOR_HEIGHT = 2.2
FLOOR_THICKNESS = 0.2

# Couleurs et matériaux (RGB)
COLOR_WALL = (0.7, 0.7, 0.8, 1.0)
COLOR_FLOOR = (0.5, 0.5, 0.6, 1.0)
COLOR_DOOR = (0.6, 0.4, 0.2, 1.0)
COLOR_CHAMBER = (0.0, 1.0, 0.3, 1.0)  # Vert lumineux pour la Chambre
COLOR_TEXT = (1.0, 1.0, 0.0, 1.0)      # Jaune pour le texte

# Animation
ANIMATION_FRAMES = 240  # 10 secondes à 24 FPS
CAMERA_RADIUS = 30.0
CAMERA_HEIGHT = 20.0


# ============================================================================
# 1. INITIALISATION
# ============================================================================

def initialize_scene():
    """Initialise la scène Blender: supprime tous les objets et configure les unités."""
    print("🧹 Initialisation de la scène...")
    
    # Supprimer tous les objets existants
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Supprimer toutes les collections sauf la principale
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)
    
    # Configurer les unités métriques
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1.0
    
    # Créer la collection principale
    collection = bpy.data.collections.new("HogwartsPlan")
    bpy.context.scene.collection.children.link(collection)
    
    print("✅ Scène initialisée")
    return collection


# ============================================================================
# 2. FONCTIONS DE CRÉATION DE MATÉRIAUX
# ============================================================================

def create_material(name, color, emission=0.0):
    """Crée un matériau avec couleur et émission optionnelle."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Shader de base
    output = nodes.new(type='ShaderNodeOutputMaterial')
    if emission > 0:
        # Matériau émissif pour la Chambre des Secrets
        emission_node = nodes.new(type='ShaderNodeEmission')
        emission_node.inputs['Color'].default_value = color
        emission_node.inputs['Strength'].default_value = emission
        mat.node_tree.links.new(emission_node.outputs['Emission'], output.inputs['Surface'])
    else:
        # Matériau diffus standard
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = 0.7
        mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat


def setup_materials():
    """Crée tous les matériaux nécessaires."""
    print("🎨 Création des matériaux...")
    materials = {
        'Wall': create_material('Wall', COLOR_WALL),
        'Floor': create_material('Floor', COLOR_FLOOR),
        'Door': create_material('Door', COLOR_DOOR),
        'Chamber': create_material('ChamberSecrets', COLOR_CHAMBER, emission=3.0),
        'Text': create_material('Text', COLOR_TEXT, emission=2.0)
    }
    print("✅ Matériaux créés")
    return materials


# ============================================================================
# 3. FONCTIONS DE CRÉATION DE GÉOMÉTRIE
# ============================================================================

def create_wall(name, start, end, height, thickness, material, collection):
    """Crée un mur entre deux points."""
    # Calculer les dimensions et la position
    length = (Vector(end) - Vector(start)).length
    center = Vector([(start[0] + end[0]) / 2, (start[1] + end[1]) / 2, height / 2])
    
    # Calculer l'angle de rotation
    direction = Vector(end) - Vector(start)
    angle = math.atan2(direction.y, direction.x)
    
    # Créer le cube pour le mur
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    wall = bpy.context.active_object
    wall.name = name
    wall.scale = (length, thickness, height)
    wall.rotation_euler = (0, 0, angle)
    
    # Appliquer le matériau
    if wall.data.materials:
        wall.data.materials[0] = material
    else:
        wall.data.materials.append(material)
    
    # Ajouter à la collection
    for coll in wall.users_collection:
        coll.objects.unlink(wall)
    collection.objects.link(wall)
    
    return wall


def create_floor(name, center, width, depth, thickness, material, collection):
    """Crée un sol rectangulaire."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(center[0], center[1], -thickness/2))
    floor = bpy.context.active_object
    floor.name = name
    floor.scale = (width, depth, thickness)
    
    # Appliquer le matériau
    if floor.data.materials:
        floor.data.materials[0] = material
    else:
        floor.data.materials.append(material)
    
    # Ajouter à la collection
    for coll in floor.users_collection:
        coll.objects.unlink(floor)
    collection.objects.link(floor)
    
    return floor


def create_door(name, position, width, height, material, collection):
    """Crée une porte (simple ouverture pour l'instant)."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(position[0], position[1], height / 2))
    door = bpy.context.active_object
    door.name = name
    door.scale = (width, WALL_THICKNESS, height)
    
    # Appliquer le matériau
    if door.data.materials:
        door.data.materials[0] = material
    else:
        door.data.materials.append(material)
    
    # Ajouter à la collection
    for coll in door.users_collection:
        coll.objects.unlink(door)
    collection.objects.link(door)
    
    return door


def create_room(name, x, y, width, depth, materials, collection, is_chamber=False):
    """Crée une pièce complète avec murs et sol."""
    print(f"  🏠 Création de {name}...")
    
    # Sol
    floor_mat = materials['Chamber'] if is_chamber else materials['Floor']
    create_floor(f"{name}_Floor", (x, y), width, depth, FLOOR_THICKNESS, floor_mat, collection)
    
    # Murs (4 murs externes)
    wall_mat = materials['Chamber'] if is_chamber else materials['Wall']
    hw = width / 2
    hd = depth / 2
    
    # Mur Nord
    create_wall(f"{name}_WallN", (x - hw, y + hd, 0), (x + hw, y + hd, 0), 
                WALL_HEIGHT, WALL_THICKNESS, wall_mat, collection)
    # Mur Sud
    create_wall(f"{name}_WallS", (x - hw, y - hd, 0), (x + hw, y - hd, 0), 
                WALL_HEIGHT, WALL_THICKNESS, wall_mat, collection)
    # Mur Est
    create_wall(f"{name}_WallE", (x + hw, y - hd, 0), (x + hw, y + hd, 0), 
                WALL_HEIGHT, WALL_THICKNESS, wall_mat, collection)
    # Mur Ouest
    create_wall(f"{name}_WallW", (x - hw, y - hd, 0), (x - hw, y + hd, 0), 
                WALL_HEIGHT, WALL_THICKNESS, wall_mat, collection)


def create_3d_text(text, location, size, material, collection):
    """Crée un texte 3D."""
    bpy.ops.object.text_add(location=location)
    text_obj = bpy.context.active_object
    text_obj.data.body = text
    text_obj.data.size = size
    text_obj.data.extrude = 0.1
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'
    
    # Appliquer le matériau
    if text_obj.data.materials:
        text_obj.data.materials[0] = material
    else:
        text_obj.data.materials.append(material)
    
    # Ajouter à la collection
    for coll in text_obj.users_collection:
        coll.objects.unlink(text_obj)
    collection.objects.link(text_obj)
    
    return text_obj


# ============================================================================
# 4. CONSTRUCTION DU PLAN DE POUDLARD
# ============================================================================

def build_hogwarts_layout(materials, collection):
    """Construit le plan simplifié de Poudlard avec plusieurs pièces."""
    print("🏰 Construction du plan de Poudlard...")
    
    # Rez-de-chaussée - Configuration simplifiée inspirée d'un plan de bâtiment
    
    # Grande Salle (centre)
    create_room("GreatHall", 0, 0, 15, 20, materials, collection)
    
    # Salles de classe autour
    create_room("Classroom1", -12, 12, 8, 8, materials, collection)
    create_room("Classroom2", 12, 12, 8, 8, materials, collection)
    create_room("Classroom3", -12, -12, 8, 8, materials, collection)
    create_room("Classroom4", 12, -12, 8, 8, materials, collection)
    
    # Couloirs
    create_room("Corridor1", 0, 15, 10, 4, materials, collection)
    create_room("Corridor2", 0, -15, 10, 4, materials, collection)
    
    # Bibliothèque
    create_room("Library", -20, 0, 10, 12, materials, collection)
    
    # Tour (petite pièce circulaire simulée par un carré)
    create_room("Tower", 20, 0, 6, 6, materials, collection)
    
    # ⭐ CHAMBRE DES SECRETS - Sous le sol, sous la Grande Salle
    chamber_y_offset = -5  # Position sous le sol
    create_room("ChamberOfSecrets", 0, 0, 10, 10, materials, collection, is_chamber=True)
    
    # Déplacer la Chambre sous le sol
    for obj in collection.objects:
        if "ChamberOfSecrets" in obj.name:
            obj.location.z -= 4  # 4 mètres sous le niveau principal
    
    # Ajouter le texte 3D au-dessus de la Chambre
    create_3d_text("Chambre des Secrets", (0, 0, -2), 1.5, materials['Text'], collection)
    
    print("✅ Plan de Poudlard construit")


# ============================================================================
# 5. ÉCLAIRAGE
# ============================================================================

def setup_lighting(collection):
    """Configure l'éclairage de la scène."""
    print("💡 Configuration de l'éclairage...")
    
    # Lumière principale (type Sun pour un éclairage uniforme)
    bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
    sun = bpy.context.active_object
    sun.name = "MainLight"
    sun.data.energy = 2.0
    sun.rotation_euler = (math.radians(45), 0, math.radians(45))
    
    for coll in sun.users_collection:
        coll.objects.unlink(sun)
    collection.objects.link(sun)
    
    # Lumière d'ambiance
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 15))
    area = bpy.context.active_object
    area.name = "AmbientLight"
    area.data.energy = 500
    area.data.size = 30
    
    for coll in area.users_collection:
        coll.objects.unlink(area)
    collection.objects.link(area)
    
    print("✅ Éclairage configuré")


# ============================================================================
# 6. CAMÉRA ET ANIMATION
# ============================================================================

def setup_camera_animation(collection):
    """Configure la caméra avec animation turntable."""
    print("🎥 Configuration de la caméra et animation...")
    
    # Créer la caméra
    bpy.ops.object.camera_add(location=(CAMERA_RADIUS, 0, CAMERA_HEIGHT))
    camera = bpy.context.active_object
    camera.name = "MainCamera"
    
    # Orienter la caméra vers le centre
    direction = Vector((0, 0, 0)) - camera.location
    camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    
    # Définir comme caméra active
    bpy.context.scene.camera = camera
    
    # Configuration de l'animation
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = ANIMATION_FRAMES
    bpy.context.scene.render.fps = 24
    
    # Créer un Empty au centre pour faire tourner la caméra autour
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 5))
    empty = bpy.context.active_object
    empty.name = "CameraTarget"
    
    # Parenter la caméra à l'Empty
    camera.parent = empty
    camera.location = (CAMERA_RADIUS, 0, CAMERA_HEIGHT - 5)
    
    # Animer la rotation de l'Empty (360 degrés)
    empty.rotation_euler = (0, 0, 0)
    empty.keyframe_insert(data_path="rotation_euler", frame=1)
    
    empty.rotation_euler = (0, 0, math.radians(360))
    empty.keyframe_insert(data_path="rotation_euler", frame=ANIMATION_FRAMES)
    
    # Rendre l'interpolation linéaire
    for fcurve in empty.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'LINEAR'
    
    # Ajouter à la collection
    for coll in camera.users_collection:
        coll.objects.unlink(camera)
    collection.objects.link(camera)
    
    for coll in empty.users_collection:
        coll.objects.unlink(empty)
    collection.objects.link(empty)
    
    print("✅ Caméra et animation configurées")


# ============================================================================
# 7. CONFIGURATION DU RENDU
# ============================================================================

def setup_render_settings():
    """Configure les paramètres de rendu."""
    print("⚙️  Configuration du rendu...")
    
    scene = bpy.context.scene
    
    # Moteur de rendu
    scene.render.engine = 'BLENDER_EEVEE'
    
    # Résolution
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    
    # Format de sortie
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'HIGH'
    scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
    
    # Filepath pour l'animation
    scene.render.filepath = "//renders/plan_turntable.mp4"
    
    # Eevee settings pour de meilleurs rendus
    scene.eevee.use_bloom = True
    scene.eevee.bloom_intensity = 0.1
    scene.eevee.use_ssr = True
    scene.eevee.use_soft_shadows = True
    
    # Monde (background)
    world = bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes['Background']
    bg_node.inputs['Color'].default_value = (0.05, 0.05, 0.1, 1.0)  # Bleu sombre
    bg_node.inputs['Strength'].default_value = 0.5
    
    print("✅ Rendu configuré")


# ============================================================================
# 8. FONCTION PRINCIPALE
# ============================================================================

def main():
    """Point d'entrée principal du script."""
    print("=" * 70)
    print("🧙 DÉFI 8: OÙ EST LA CHAMBRE DES SECRETS ?")
    print("   Génération du plan 3D de Poudlard")
    print("=" * 70)
    
    # 1. Initialiser la scène
    collection = initialize_scene()
    
    # 2. Créer les matériaux
    materials = setup_materials()
    
    # 3. Construire le plan
    build_hogwarts_layout(materials, collection)
    
    # 4. Configurer l'éclairage
    setup_lighting(collection)
    
    # 5. Configurer la caméra et l'animation
    setup_camera_animation(collection)
    
    # 6. Configurer le rendu
    setup_render_settings()
    
    # 7. Sauvegarder le fichier
    output_path = "//hogwarts_plan.blend"
    bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath(output_path))
    print(f"💾 Fichier sauvegardé: hogwarts_plan.blend")
    
    print("=" * 70)
    print("✅ Script terminé avec succès!")
    print("=" * 70)
    print("\n📝 Prochaines étapes:")
    print("  1. Ouvrir hogwarts_plan.blend dans Blender")
    print("  2. Vérifier la scène (la Chambre des Secrets brille en vert)")
    print("  3. Lancer le rendu: Render > Render Animation")
    print("  4. La vidéo sera générée dans renders/plan_turntable.mp4")
    print()


# ============================================================================
# EXÉCUTION
# ============================================================================

if __name__ == "__main__":
    main()
