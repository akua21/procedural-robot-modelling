# Decide AntBot parameters
# Apply modifiers
# Add armature
#   Add 1 bone for head
#   Add 1 bone for body
#   Add 2 bones for each leg
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

# get seed from parameters
seed = int(sys.argv[-1])
random.seed(seed)

# Decide AntBot parameters
LEG_LENGTH_MIN = 6
LEG_LENGTH_MAX = 10

SEGMENT_NUMBER_MIN = 5
SEGMENT_NUMBER_MAX = 15

legLength = random.randint(LEG_LENGTH_MIN, LEG_LENGTH_MAX)
segmentNumber = random.randint(SEGMENT_NUMBER_MIN, SEGMENT_NUMBER_MAX)

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
HEAD_OFFSET = -0.2
HEAD_SIZE = 0.59
HEAD_START = HEAD_SIZE/2 + HEAD_OFFSET
HEAD_END = HEAD_START - HEAD_SIZE

headBone.head = (0, HEAD_START, 0)
headBone.tail = (0, HEAD_END, 0)

#   Add 1 bone for body
bodyBone = armature.edit_bones.new("BodyBone")
BODY_OFFSET = 0
BODY_SIZE = 0.71
BODY_START = HEAD_END + BODY_OFFSET
BODY_END = BODY_START - BODY_SIZE * segmentNumber

bodyBone.head = (0, BODY_START, 0)
bodyBone.tail = (0, BODY_END, 0)

bodyBone.parent = headBone


bpy.ops.object.mode_set(mode="OBJECT")

# Deselect all
bpy.ops.object.select_all(action='DESELECT')

antBotObject.select_set(True)
armatureObject.select_set(True)

# Add armature to object
bpy.ops.object.parent_set(type='ARMATURE_AUTO')


# Print parameters
print(f"legLength: {legLength}")
print(f"segmentNumber: {segmentNumber}")

# Save in a different file
bpy.ops.wm.save_as_mainfile(filepath=f"{os.getcwd()}/outputs/antBot_{seed}.blend")
