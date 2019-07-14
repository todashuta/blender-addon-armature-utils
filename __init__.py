bl_info = {
    "name" : "Armature Utility",
    "author" : "Toda Shuta",
    "version" : (0, 1),
    "blender" : (2, 79, 0),
    "location" : "3D View > Tool Shelf > Tools > Armature Utility",
    "description" : "",
    "warning" : "",
    "wiki_url" : "",
    "tracker_url" : "",
    "category" : "Animation"
}


if "bpy" in locals():
    import importlib
    importlib.reload(armature_utility)
else:
    from . import armature_utility


import bpy


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
