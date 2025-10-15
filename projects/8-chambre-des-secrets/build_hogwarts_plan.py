#!/usr/bin/env python3
"""
DÉFI 8 - OÙ EST LA CHAMBRE DES SECRETS ?
Script de génération automatique du plan 3D de Poudlard dans Blender
Basé sur le fichier JSON context/plans/plan.json

Usage:
    blender --background --python build_hogwarts_plan.py
    ou
    blender --python build_hogwarts_plan.py  (avec interface)
"""

import bpy
import json
import math
import os
from pathlib import Path
from mathutils import Vector

# ==============================================================================
# CONFIGURATION ET CHEMINS
# ==============================================================================

# Obtenir le chemin du script et du projet
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CONTEXT_DIR = PROJECT_ROOT / "context"
PLAN_JSON = CONTEXT_DIR / "plans" / "plan.json"
RENDERS_DIR = SCRIPT_DIR / "renders"
OUTPUT_BLEND = SCRIPT_DIR / "hogwarts_plan.blend"

# Créer le dossier de rendus s'il n'existe pas
RENDERS_DIR.mkdir(exist_ok=True)

print(f"📂 Script directory: {SCRIPT_DIR}")
print(f"📂 Plan JSON: {PLAN_JSON}")
print(f"📂 Renders output: {RENDERS_DIR}")

# ==============================================================================
# CHARGEMENT DES DONNÉES
# ==============================================================================

def load_plan_data():
    """Charge le fichier JSON du plan."""
    print(f"\n📖 Chargement du plan depuis {PLAN_JSON}...")
    if not PLAN_JSON.exists():
        raise FileNotFoundError(f"Le fichier {PLAN_JSON} n'existe pas!")
    
    with open(PLAN_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ Plan chargé: {data['project']['name']}")
    print(f"   Niveaux: {len(data['levels'])}")
    return data

# ==============================================================================
# NETTOYAGE DE LA SCÈNE
# ==============================================================================

def clear_scene():
    """Supprime tous les objets de la scène."""
    print("\n🧹 Nettoyage de la scène...")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Nettoyer les collections orphelines
    for collection in bpy.data.collections:
        if collection.users == 0:
            bpy.data.collections.remove(collection)
    
    print("✅ Scène nettoyée")

# ==============================================================================
# CRÉATION DES MATÉRIAUX
# ==============================================================================

def create_materials():
    """Crée les matériaux pour les différents types de pièces."""
    print("\n🎨 Création des matériaux...")
    
    materials = {}
    
    # Matériau pour les salles de cours (bleu clair)
    mat = bpy.data.materials.new(name="Mat_SalleCours")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.3, 0.5, 0.8, 1.0)
    nodes["Principled BSDF"].inputs["Metallic"].default_value = 0.0
    nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.5
    materials["salle_cours"] = mat
    
    # Matériau pour les amphithéâtres (bleu foncé)
    mat = bpy.data.materials.new(name="Mat_Amphi")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.2, 0.3, 0.6, 1.0)
    materials["amphi"] = mat
    
    # Matériau pour les bureaux (vert)
    mat = bpy.data.materials.new(name="Mat_Bureau")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.4, 0.7, 0.4, 1.0)
    materials["bureau"] = mat
    materials["bureau_equipe"] = mat
    materials["direction"] = mat
    materials["administration"] = mat
    
    # Matériau pour les sanitaires (gris clair)
    mat = bpy.data.materials.new(name="Mat_Sanitaires")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.7, 0.7, 0.7, 1.0)
    materials["sanitaires"] = mat
    
    # Matériau pour les espaces techniques (gris foncé)
    mat = bpy.data.materials.new(name="Mat_Technique")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.4, 0.4, 0.4, 1.0)
    materials["technique"] = mat
    materials["stockage"] = mat
    materials["archives"] = mat
    
    # Matériau pour les espaces de circulation (beige)
    mat = bpy.data.materials.new(name="Mat_Circulation")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.9, 0.85, 0.7, 1.0)
    materials["circulation"] = mat
    materials["accueil"] = mat
    
    # Matériau pour le coworking (orange)
    mat = bpy.data.materials.new(name="Mat_Coworking")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.9, 0.6, 0.3, 1.0)
    materials["coworking"] = mat
    
    # Matériau pour les espaces polyvalents (violet)
    mat = bpy.data.materials.new(name="Mat_Polyvalente")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.6, 0.4, 0.7, 1.0)
    materials["polyvalente"] = mat
    materials["flex"] = mat
    
    # Matériau pour les laboratoires (cyan)
    mat = bpy.data.materials.new(name="Mat_Labo")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.3, 0.8, 0.8, 1.0)
    materials["labo"] = mat
    
    # Matériau par défaut (blanc)
    mat = bpy.data.materials.new(name="Mat_Default")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1.0)
    materials["default"] = mat
    
    # MATÉRIAU SPÉCIAL : CHAMBRE DES SECRETS (émissif vert émeraude)
    mat = bpy.data.materials.new(name="Mat_ChambreSecrets")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes["Principled BSDF"]
    
    # Retirer le BSDF et ajouter un Emission
    nodes.remove(bsdf)
    emission = nodes.new(type="ShaderNodeEmission")
    emission.location = (0, 0)
    emission.inputs["Color"].default_value = (0.0, 1.0, 0.5, 1.0)  # Vert émeraude
    emission.inputs["Strength"].default_value = 2.0
    
    output = nodes["Material Output"]
    mat.node_tree.links.new(emission.outputs["Emission"], output.inputs["Surface"])
    materials["chambre_secrets"] = mat
    
    # Matériau pour les murs (gris neutre)
    mat = bpy.data.materials.new(name="Mat_Mur")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.85, 0.85, 0.85, 1.0)
    nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.8
    materials["mur"] = mat
    
    print(f"✅ {len(materials)} matériaux créés")
    return materials

# ==============================================================================
# GÉNÉRATION DE LA GÉOMÉTRIE
# ==============================================================================

def create_room(name, room_type, area_m2, position, level_z, materials, wall_height):
    """Crée un objet 3D représentant une pièce."""
    
    # Calculer une taille approximative basée sur la surface
    # On crée des rectangles de proportions variées
    if area_m2 is None:
        area_m2 = 10.0  # Valeur par défaut
    
    # Ratio longueur/largeur variable selon le type
    ratio = 1.5 if room_type in ["salle_cours", "amphi"] else 1.2
    width = math.sqrt(area_m2 / ratio)
    length = area_m2 / width
    
    # Créer le sol de la pièce
    bpy.ops.mesh.primitive_cube_add(size=1, location=(position[0], position[1], level_z))
    floor = bpy.context.active_object
    floor.name = f"Floor_{name}"
    floor.scale = (length / 2, width / 2, 0.1)
    
    # Appliquer le matériau approprié
    mat_key = room_type if room_type in materials else "default"
    if name == "Chambre des Secrets":
        mat_key = "chambre_secrets"
    
    floor.data.materials.append(materials[mat_key])
    
    # Créer les murs
    wall_thickness = 0.15
    walls = []
    
    # Mur avant (Y+)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(position[0], position[1] + width/2, level_z + wall_height/2))
    wall = bpy.context.active_object
    wall.name = f"Wall_{name}_Front"
    wall.scale = (length / 2, wall_thickness / 2, wall_height / 2)
    wall.data.materials.append(materials["mur"])
    walls.append(wall)
    
    # Mur arrière (Y-)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(position[0], position[1] - width/2, level_z + wall_height/2))
    wall = bpy.context.active_object
    wall.name = f"Wall_{name}_Back"
    wall.scale = (length / 2, wall_thickness / 2, wall_height / 2)
    wall.data.materials.append(materials["mur"])
    walls.append(wall)
    
    # Mur gauche (X-)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(position[0] - length/2, position[1], level_z + wall_height/2))
    wall = bpy.context.active_object
    wall.name = f"Wall_{name}_Left"
    wall.scale = (wall_thickness / 2, width / 2, wall_height / 2)
    wall.data.materials.append(materials["mur"])
    walls.append(wall)
    
    # Mur droit (X+)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(position[0] + length/2, position[1], level_z + wall_height/2))
    wall = bpy.context.active_object
    wall.name = f"Wall_{name}_Right"
    wall.scale = (wall_thickness / 2, width / 2, wall_height / 2)
    wall.data.materials.append(materials["mur"])
    walls.append(wall)
    
    return floor, walls

def generate_level(level_data, level_index, data, materials):
    """Génère tous les objets pour un niveau donné."""
    print(f"\n🏗️  Génération du niveau: {level_data['name']}")
    
    # Créer une collection pour ce niveau
    collection_name = f"Level_{level_data['name']}"
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)
    
    # Paramètres
    wall_height = data["parametric_generation"]["wall_height_m"]
    level_z = level_index * data["assumptions"]["floor_to_floor_height_m"]
    
    # Calculer une disposition en grille
    rooms = level_data["rooms"]
    grid_size = math.ceil(math.sqrt(len(rooms)))
    spacing = 15.0  # Espacement entre les pièces
    
    room_objects = []
    
    for idx, room in enumerate(rooms):
        # Position en grille
        row = idx // grid_size
        col = idx % grid_size
        x = col * spacing
        y = row * spacing
        
        # Créer la pièce
        floor, walls = create_room(
            room["name"],
            room["type"],
            room.get("area_m2"),
            (x, y),
            level_z,
            materials,
            wall_height
        )
        
        # Ajouter à la collection
        for obj in [floor] + walls:
            if obj.name not in collection.objects:
                collection.objects.link(obj)
                # Retirer de la collection de scène principale
                if obj.name in bpy.context.scene.collection.objects:
                    bpy.context.scene.collection.objects.unlink(obj)
        
        room_objects.append((floor, walls))
    
    print(f"✅ {len(rooms)} pièces créées pour {level_data['name']}")
    return collection, room_objects

# ==============================================================================
# CHAMBRE DES SECRETS
# ==============================================================================

def create_chamber_of_secrets(materials):
    """Crée la Chambre des Secrets sous le niveau principal."""
    print("\n🐍 Création de la Chambre des Secrets...")
    
    # Créer une collection spéciale
    collection_name = "ChambreDesSecrets"
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)
    
    # Position sous le RdC
    position = (0, 0, -5.0)
    wall_height = 4.0
    
    # Créer la chambre (grande salle mystérieuse)
    floor, walls = create_room(
        "Chambre des Secrets",
        "chambre_secrets",
        150.0,  # Grande surface
        (position[0], position[1]),
        position[2],
        materials,
        wall_height
    )
    
    # Ajouter à la collection
    for obj in [floor] + walls:
        if obj.name not in collection.objects:
            collection.objects.link(obj)
            if obj.name in bpy.context.scene.collection.objects:
                bpy.context.scene.collection.objects.unlink(obj)
    
    # Créer le texte 3D "Chambre des Secrets"
    bpy.ops.object.text_add(location=(position[0], position[1], position[2] + wall_height + 1.0))
    text_obj = bpy.context.active_object
    text_obj.name = "Text_ChambreSecrets"
    text_obj.data.body = "Chambre des Secrets"
    text_obj.data.size = 1.5
    text_obj.data.extrude = 0.1
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'
    
    # Matériau émissif pour le texte
    text_mat = bpy.data.materials.new(name="Mat_TextSecrets")
    text_mat.use_nodes = True
    nodes = text_mat.node_tree.nodes
    nodes.clear()
    
    emission = nodes.new(type="ShaderNodeEmission")
    emission.inputs["Color"].default_value = (0.0, 1.0, 0.5, 1.0)
    emission.inputs["Strength"].default_value = 3.0
    
    output = nodes.new(type="ShaderNodeOutputMaterial")
    text_mat.node_tree.links.new(emission.outputs["Emission"], output.inputs["Surface"])
    
    text_obj.data.materials.append(text_mat)
    
    # Ajouter le texte à la collection
    if text_obj.name not in collection.objects:
        collection.objects.link(text_obj)
        if text_obj.name in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.unlink(text_obj)
    
    print("✅ Chambre des Secrets créée avec effet lumineux")
    return collection

# ==============================================================================
# CAMÉRA ET ANIMATION
# ==============================================================================

def create_animated_camera(center=(0, 0, 0), radius=40, height=15, frames=240):
    """Crée une caméra orbitale animée autour du plan."""
    print("\n📹 Création de la caméra animée...")
    
    # Créer la caméra
    bpy.ops.object.camera_add(location=(center[0] + radius, center[1], center[2] + height))
    camera = bpy.context.active_object
    camera.name = "Camera_Orbital"
    
    # Définir comme caméra active
    bpy.context.scene.camera = camera
    
    # Ajouter une contrainte de suivi
    constraint = camera.constraints.new(type='TRACK_TO')
    
    # Créer un objet vide au centre pour le suivi
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=center)
    target = bpy.context.active_object
    target.name = "Camera_Target"
    
    constraint.target = target
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'
    
    # Animer la caméra en rotation
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = frames
    
    for frame in range(1, frames + 1):
        angle = (frame / frames) * 2 * math.pi
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        z = center[2] + height
        
        camera.location = (x, y, z)
        camera.keyframe_insert(data_path="location", frame=frame)
    
    print(f"✅ Caméra orbitale créée avec {frames} frames")
    return camera, target

# ==============================================================================
# ÉCLAIRAGE
# ==============================================================================

def setup_lighting():
    """Configure l'éclairage de la scène."""
    print("\n💡 Configuration de l'éclairage...")
    
    # Lumière principale (key light)
    bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
    sun = bpy.context.active_object
    sun.name = "Sun_Key"
    sun.data.energy = 1.5
    sun.rotation_euler = (math.radians(45), 0, math.radians(45))
    
    # Lumière d'ambiance
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 30))
    area = bpy.context.active_object
    area.name = "Area_Fill"
    area.data.energy = 500
    area.data.size = 50
    
    print("✅ Éclairage configuré")

# ==============================================================================
# RENDU
# ==============================================================================

def setup_render_settings(output_path):
    """Configure les paramètres de rendu."""
    print("\n🎬 Configuration du rendu...")
    
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
    
    # Chemin de sortie
    scene.render.filepath = str(output_path)
    
    # Paramètres EEVEE
    scene.eevee.use_bloom = True
    scene.eevee.bloom_intensity = 0.1
    
    print(f"✅ Rendu configuré: {output_path}")

# ==============================================================================
# FONCTION PRINCIPALE
# ==============================================================================

def main():
    """Fonction principale du script."""
    print("=" * 80)
    print("🏰 GÉNÉRATION DU PLAN 3D DE POUDLARD - DÉFI 8")
    print("=" * 80)
    
    try:
        # 1. Charger les données
        data = load_plan_data()
        
        # 2. Nettoyer la scène
        clear_scene()
        
        # 3. Créer les matériaux
        materials = create_materials()
        
        # 4. Générer les niveaux
        for idx, level in enumerate(data["levels"]):
            generate_level(level, idx, data, materials)
        
        # 5. Créer la Chambre des Secrets
        create_chamber_of_secrets(materials)
        
        # 6. Configurer l'éclairage
        setup_lighting()
        
        # 7. Créer la caméra animée
        create_animated_camera(center=(30, 30, 0), radius=60, height=25, frames=240)
        
        # 8. Sauvegarder le fichier Blender
        print(f"\n💾 Sauvegarde du fichier Blender: {OUTPUT_BLEND}")
        bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT_BLEND))
        print("✅ Fichier .blend sauvegardé")
        
        # 9. Configurer et lancer le rendu
        output_video = RENDERS_DIR / "plan_turntable.mp4"
        setup_render_settings(output_video)
        
        print("\n🎬 Lancement du rendu de l'animation...")
        print("⏳ Cela peut prendre plusieurs minutes...")
        bpy.ops.render.render(animation=True, write_still=False)
        
        print("\n" + "=" * 80)
        print("✅ GÉNÉRATION TERMINÉE AVEC SUCCÈS!")
        print("=" * 80)
        print(f"\n📦 Fichiers générés:")
        print(f"   • Scène Blender: {OUTPUT_BLEND}")
        print(f"   • Animation MP4:  {output_video}")
        print("\n🎉 La Chambre des Secrets attend d'être découverte!")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
