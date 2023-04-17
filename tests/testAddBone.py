import bpy
 
# Create instance of armature 
armature = bpy.data.armatures.new("Armature")

# Link the instance to a blender object
object = bpy.data.objects.new("Armature", armature)

# Create it in the scene
bpy.context.scene.collection.objects.link(object)

# Set the object as active
bpy.context.view_layer.objects.active = object
bpy.ops.object.mode_set(mode="EDIT")

# Creates a bone and sets its position
bone = armature.edit_bones.new("Bone")
bone.head = (0, 0, 0)
bone.tail = (0, 7, 0)

bone2 = armature.edit_bones.new("Bone2")
bone2.head = bone.tail
bone2.tail = (0, 7, 3)

#bone2.parent = bone # the same
armature.edit_bones["Bone2"].parent = armature.edit_bones["Bone"]

# print(armature.edit_bones)
bpy.ops.object.mode_set(mode="OBJECT")


bpy.data.objects["Cube"].select_set(True)
bpy.data.objects["Armature"].select_set(True)

bpy.ops.object.parent_set(type='ARMATURE_AUTO')


