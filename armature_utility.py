import bpy
from bpy.props import PointerProperty


def scene_armature_utility_armature_obj_poll(self, ob):
    return ob.type == "ARMATURE"

#def scene_armature_utility_armature_obj_set(self, val):
#    if val.type == "ARMATURE":
#        self["armature_utility_armature_obj"] = value

bpy.types.Scene.armature_utility_armature_obj = PointerProperty(
        name="Armature Name",
        type=bpy.types.Object, poll=scene_armature_utility_armature_obj_poll)


class AddArmatureModifier(bpy.types.Operator):
    bl_idname = "object.armatureutility_add_armature_modifier"
    bl_label = "Add Armature Modifier"

    @classmethod
    def poll(self, context):
        o = context.active_object
        if o is None:
            return False
        if o.type != "MESH":
            return False
        has_armature_modifier = len([m for m in o.modifiers if m.type == "ARMATURE"]) > 0
        if has_armature_modifier:
            return False
        if context.scene.armature_utility_armature_obj is None:
            return False
        if context.scene.armature_utility_armature_obj.type != "ARMATURE":
            return False
        return True

    def execute(self, context):
        active_object = context.active_object
        mod = active_object.modifiers.new("Armature", "ARMATURE")
        mod.object = context.scene.armature_utility_armature_obj
        return {"FINISHED"}


class AssignObjectNameVertexGroup(bpy.types.Operator):
    bl_idname = "object.armatureutility_assign_object_name_vertex_group"
    bl_label = "Assign Object Name Vertex Group"

    @classmethod
    def poll(cls, context):
        o = context.active_object
        return o and o.type == "MESH"

    def execute(self, context):
        ob = context.active_object
        name = ob.name
        vg = ob.vertex_groups.get(name)
        if vg is None:
            vg = ob.vertex_groups.new(name)
        for v in ob.data.vertices:
            vg.add([v.index], 1.0, "REPLACE")
        return {"FINISHED"}


class AddMissingVertexGroup(bpy.types.Operator):
    bl_idname = "object.armatureutility_add_missing_vertex_group"
    bl_label = "Add Missing Vertex Group"

    @classmethod
    def poll(cls, context):
        active_object = context.active_object
        return (active_object is not None
                and active_object.type == "MESH"
                and active_object.parent is not None
                and active_object.parent.type == "ARMATURE")

    def execute(self, context):
        active_object = context.active_object
        parent = active_object.parent
        deform_bone_names = [b.name for b in parent.data.bones if b.use_deform]
        vert_group_names = [g.name for g in active_object.vertex_groups]
        missing_vert_groups = set(deform_bone_names) - set(vert_group_names)
        for name in missing_vert_groups:
            active_object.vertex_groups.new(name)
            self.report({"INFO"}, "New Vertex Group: {}".format(name))
        return {"FINISHED"}


class RemoveUnnecessaryVertexGroup(bpy.types.Operator):
    bl_idname = "object.armatureutility_remove_unnecessary_vertex_group"
    bl_label = "Remove Unnecessary Vertex Group"

    @classmethod
    def poll(cls, context):
        active_object = context.active_object
        return (active_object is not None
                and active_object.type == "MESH"
                and active_object.parent is not None
                and active_object.parent.type == "ARMATURE")

    def execute(self, context):
        active_object = context.active_object
        parent = active_object.parent
        deform_bone_names = [b.name for b in parent.data.bones if b.use_deform]
        vert_group_names = [g.name for g in active_object.vertex_groups]
        unnecessary_vert_groups = set(vert_group_names) - set(deform_bone_names)
        for name in unnecessary_vert_groups:
            g = active_object.vertex_groups.get(name)
            active_object.vertex_groups.remove(g)
            self.report({"INFO"}, "Remove Vertex Group: {}".format(name))
        return {"FINISHED"}


class ArmatureUtilityCustomPanel(bpy.types.Panel):
    bl_label = "Armature Utility"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context):
        #return context.active_object is not None
        return True

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "armature_utility_armature_obj")
        layout.operator(AddArmatureModifier.bl_idname)
        layout.operator(AssignObjectNameVertexGroup.bl_idname)
        layout.separator()
        layout.operator(AddMissingVertexGroup.bl_idname)
        layout.operator(RemoveUnnecessaryVertexGroup.bl_idname)
