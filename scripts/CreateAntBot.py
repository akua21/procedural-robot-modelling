# Decide AntBot parameters
# Apply modifiers
# Add armature
#   Add 1 bone for head
#   Add 1 bone for each body part
#   Add a shoulder and 2 bones for each leg
# Add armature to object
# Save in a different file

# Mapping of inputs:
#   - LegLength [int]: Input_2
#   - SegmentNumber [int]: Input_3
#   - BodyOffset [Array[3]]: Input_4
#   - LegOffset [Array[3]]: Input_5
#   - LegPosition [Array[3]]: Input_6

# Measures Body parts:
#   - Head: 1.69 1.97 0.723
#   - Body: 1.89 1.19 0.764
#   - Leg: 0.367 0.529 0.493

# Bone sizes:
#   - Head: 0.59
#   - Body: 0.71

import bpy
import sys
import os
import random
import math

# get seed from parameters
seed = int(sys.argv[-1])
random.seed(seed)

# Decide AntBot parameters
#  - LegLength [int]
#  - SegmentNumber [int]
#  - UpperLegLenth [int]: from 2 to legLength - 2
#  - LowerLegLength [int]: LegLength - UpperLegLength
LEG_LENGTH_MIN = 5
LEG_LENGTH_MAX = 15

SEGMENT_NUMBER_MIN = 4
SEGMENT_NUMBER_MAX = 20

legLength = random.randint(LEG_LENGTH_MIN, LEG_LENGTH_MAX)
segmentNumber = random.randint(SEGMENT_NUMBER_MIN, SEGMENT_NUMBER_MAX)
anteriorLegLength = random.randint(2, legLength - 2)
posteriorLegLength = legLength - anteriorLegLength



antBotObject = bpy.data.objects['AntBot']
antBotGN = antBotObject.modifiers["GeometryNodes"]
antBotObject.data.update()

antBotGN["Input_2"] = legLength
antBotGN["Input_3"] = segmentNumber

# Apply modifiers
bpy.context.view_layer.objects.active = antBotObject
bpy.ops.object.modifier_apply(modifier="GeometryNodes")

# Add armature

# Create instance of armature 
armature = bpy.data.armatures.new("Armature")
# Link the instance to a blender object
armatureObject = bpy.data.objects.new("Armature", armature)
# Create it in the scene
bpy.context.scene.collection.objects.link(armatureObject)
# Set the object as active
bpy.context.view_layer.objects.active = armatureObject
bpy.ops.object.mode_set(mode="EDIT")

# NOTE: While adding the tail, we substract because the model is built in the `-y` direction

#   Add 1 bone for head
headBone = armature.edit_bones.new("HeadBone")
HEAD_OFFSET = -0.16
HEAD_SIZE = 0.55
HEAD_START = HEAD_SIZE/2 + HEAD_OFFSET
HEAD_END = HEAD_START - HEAD_SIZE

headBone.head = (0, HEAD_START, 0)
headBone.tail = (0, HEAD_END, 0)


#   Add 1 bone for each body part
neckBone = armature.edit_bones.new("BodyBone_0")
NECK_SIZE = 0.382
NECK_START = HEAD_END
NECK_END = NECK_START - NECK_SIZE

neckBone.head = headBone.tail
neckBone.tail = (0, NECK_END, 0)
neckBone.parent = headBone
neckBone.use_connect = True


#   Add a shoulder and 2 bones for each leg
LEG_OFFSET = 0.764
LEG_X_OFFSET = 0.94
LEG_SIZE = 0.367 
LEG_START = NECK_END

# Shoulder
shoulderBoneR = armature.edit_bones.new("ShoulderBoneRight_0")
shoulderBoneR.head = neckBone.tail
shoulderBoneR.tail = (LEG_X_OFFSET, NECK_END, 0)
shoulderBoneR.parent = neckBone
shoulderBoneR.use_connect = True

shoulderBoneL = armature.edit_bones.new("ShoulderBoneLeft_0")
shoulderBoneL.head = neckBone.tail
shoulderBoneL.tail = (-LEG_X_OFFSET, NECK_END, 0)
shoulderBoneL.parent = neckBone
shoulderBoneL.use_connect = True

# Legs 
# Anterior
legBoneAR = armature.edit_bones.new("LegBoneAnteriorRight_0")
legBoneAR.head = shoulderBoneR.tail
legBoneAR.tail = (LEG_X_OFFSET + LEG_SIZE * anteriorLegLength, LEG_START, 0)
legBoneAR.parent = shoulderBoneR
legBoneAR.use_connect = True

legBoneAL = armature.edit_bones.new("LegBoneAnteriorLeft_0")
legBoneAL.head = shoulderBoneL.tail
legBoneAL.tail = (-LEG_X_OFFSET - LEG_SIZE * anteriorLegLength, LEG_START, 0)
legBoneAL.parent = shoulderBoneL
legBoneAL.use_connect = True

# Posterior
legBonePR = armature.edit_bones.new("LegBonePosteriorRight_0")
legBonePR.head = legBoneAR.tail
legBonePR.tail = (LEG_X_OFFSET + LEG_SIZE * legLength, LEG_START, 0)
legBonePR.parent = legBoneAR
legBonePR.use_connect = True

legBonePL = armature.edit_bones.new("LegBonePosteriorLeft_0")
legBonePL.head = legBoneAL.tail
legBonePL.tail = (-LEG_X_OFFSET - LEG_SIZE * legLength, LEG_START, 0)
legBonePL.parent = legBoneAL
legBonePL.use_connect = True


# Rest of the body
BODY_SIZE = 0.764

#   Add 2 bones for each leg
for i in range(1, segmentNumber):
    # previous bone
    previousBone = armature.edit_bones[f"BodyBone_{i-1}"]

    # Body bone
    bodyBone = armature.edit_bones.new(f"BodyBone_{i}")
    bodyBone.head = previousBone.tail
    bodyBone.tail = (0, previousBone.tail[1] - BODY_SIZE, 0)
    bodyBone.parent = previousBone
    bodyBone.use_connect = True

    # Shoulder bones
    shoulderBoneR = armature.edit_bones.new(f"ShoulderBoneRight_{i}")
    shoulderBoneR.head = bodyBone.tail
    shoulderBoneR.tail = (LEG_X_OFFSET, bodyBone.tail[1], 0)
    shoulderBoneR.parent = bodyBone
    shoulderBoneR.use_connect = True

    shoulderBoneL = armature.edit_bones.new(f"ShoulderBoneLeft_{i}")
    shoulderBoneL.head = bodyBone.tail
    shoulderBoneL.tail = (-LEG_X_OFFSET, bodyBone.tail[1], 0)
    shoulderBoneL.parent = bodyBone
    shoulderBoneL.use_connect = True

    # Leg bones
    # Anterior
    legBoneAR = armature.edit_bones.new(f"LegBoneAnteriorRight_{i}")
    legBoneAR.head = shoulderBoneR.tail
    legBoneAR.tail = (LEG_X_OFFSET + LEG_SIZE * anteriorLegLength, bodyBone.tail[1], 0)
    legBoneAR.parent = shoulderBoneR
    legBoneAR.use_connect = True

    legBoneAL = armature.edit_bones.new(f"LegBoneAnteriorLeft_{i}")
    legBoneAL.head = shoulderBoneL.tail
    legBoneAL.tail = (-LEG_X_OFFSET - LEG_SIZE * anteriorLegLength, bodyBone.tail[1], 0)
    legBoneAL.parent = shoulderBoneL
    legBoneAL.use_connect = True

    # Posterior
    legBonePR = armature.edit_bones.new(f"LegBonePosteriorRight_{i}")
    legBonePR.head = legBoneAR.tail
    legBonePR.tail = (LEG_X_OFFSET + LEG_SIZE * legLength, bodyBone.tail[1], 0)
    legBonePR.parent = legBoneAR
    legBonePR.use_connect = True

    legBonePL = armature.edit_bones.new(f"LegBonePosteriorLeft_{i}")
    legBonePL.head = legBoneAL.tail
    legBonePL.tail = (-LEG_X_OFFSET - LEG_SIZE * legLength, bodyBone.tail[1], 0)
    legBonePL.parent = legBoneAL
    legBonePL.use_connect = True


bpy.ops.object.mode_set(mode="OBJECT")

# Deselect all
bpy.ops.object.select_all(action='DESELECT')

antBotObject.select_set(True)
armatureObject.select_set(True)

# Add armature to object
bpy.ops.object.parent_set(type='ARMATURE_AUTO')



bpy.ops.object.mode_set(mode="POSE")

# Select all right anterior
for i in range(0, segmentNumber):
    # Select bones
    armatureObject.data.bones[f"LegBoneAnteriorRight_{i}"].select = True

# rotate bone
#   If the size is minimum (2), the rotation is 45 degrees
#   If the size is maximum (legLength-2), the rotation is 0 degrees
rotationAnterior = math.radians(45 * (1 - (anteriorLegLength - 2) / (legLength - 4)))
bpy.ops.transform.rotate(value=rotationAnterior, orient_axis='Y')

# Select all left anterior
for i in range(0, segmentNumber):
    # Select bones
    armatureObject.data.bones[f"LegBoneAnteriorRight_{i}"].select = False
    armatureObject.data.bones[f"LegBoneAnteriorLeft_{i}"].select = True

# rotate bone
bpy.ops.transform.rotate(value=-rotationAnterior, orient_axis='Y')

# Select all right posterior
for i in range(0, segmentNumber):
    # Select bones
    armatureObject.data.bones[f"LegBoneAnteriorLeft_{i}"].select = False
    armatureObject.data.bones[f"LegBonePosteriorRight_{i}"].select = True

# rotate bone
#   The posterior will always be perpendicular to the ground, so the inverse rotation is applied
#   plus 90 degrees
rotationPosterior = math.radians(-75) - rotationAnterior
bpy.ops.transform.rotate(value=rotationPosterior, orient_axis='Y')

# Select all left posterior
for i in range(0, segmentNumber):
    # Select bones
    armatureObject.data.bones[f"LegBonePosteriorRight_{i}"].select = False
    armatureObject.data.bones[f"LegBonePosteriorLeft_{i}"].select = True

# rotate bone
bpy.ops.transform.rotate(value=-rotationPosterior, orient_axis='Y')

# Deselect all
for i in range(0, segmentNumber):
    # Select bones
    armatureObject.data.bones[f"LegBonePosteriorLeft_{i}"].select = False




# Print parameters
print(f"legLength: {legLength}")
print(f"segmentNumber: {segmentNumber}")
print(f"anteriorLegLength: {anteriorLegLength}")
print(f"posteriorLegLength: {posteriorLegLength}")

# Save in a different file
# Blender
bpy.ops.wm.save_as_mainfile(filepath=f"{os.getcwd()}/outputs/blenderFiles/antBot_{seed}.blend")
# FBX
bpy.ops.export_scene.fbx(filepath=f"{os.getcwd()}/outputs/fbxFiles/antBot_{seed}.fbx", use_selection=True, path_mode='COPY', object_types={'ARMATURE', 'MESH'})