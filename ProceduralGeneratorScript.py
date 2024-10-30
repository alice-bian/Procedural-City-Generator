import bpy
import random

################################################################
# helper functions BEGIN
################################################################


def purge_orphans():
    """
    Remove all orphan data blocks
    """
    if bpy.app.version >= (3, 0, 0):
        # only for Blender versions 3.0 and higher
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    else:
        # only for Blender versions lower than 3.0
        # call purge_orphans() recursively until there are no more orphan data blocks to purge
        result = bpy.ops.outliner.orphans_purge()
        if result.pop() != "CANCELLED":
            purge_orphans()


def clean_scene():
    """
    Removing all of the objects, collection, materials, particles,
    textures, images, curves, meshes, actions, nodes, and worlds from the scene
    """
    # make sure the active object is not in Edit Mode
    if bpy.context.active_object and bpy.context.active_object.mode == "EDIT":
        bpy.ops.object.editmode_toggle()

    # make sure non of the objects are hidden from the viewport, selection, or disabled
    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.hide_viewport = False

    # select all the object and delete them (just like pressing A + X + D in the viewport)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    # find all the collections and remove them
    collection_names = [col.name for col in bpy.data.collections]
    for name in collection_names:
        bpy.data.collections.remove(bpy.data.collections[name])

    # in the case when you modify the world shader
    # delete and recreate the world object
    world_names = [world.name for world in bpy.data.worlds]
    for name in world_names:
        bpy.data.worlds.remove(bpy.data.worlds[name])
    # create a new world data block
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]

    purge_orphans()


################################################################
# helper functions END
###############################################################

def procedural_generator(grid_size_x, grid_size_y, cube_size, cube_spacing, red_mat, black_mat):
    for x in range(grid_size_x):
        for y in range (grid_size_y):
            location = (x * cube_spacing, y * cube_spacing, random.random() * 2)
            
            bpy.ops.mesh.primitive_cube_add(
                size = cube_size,
                enter_editmode = False,
                align = 'WORLD',
                location = location,
                scale = (1,1,1)
            )
            
            item = bpy.context.object
            if random.random() < 0.1:
                item.data.materials.append(red_mat)
            else:
                item.data.materials.append(black_mat)


def main():
    """
    Python code that creates a grid of procedurally generated cubes of various heights and colors
    """
    
    all_cubes = []
    cube_size = 2
    cube_spacing = 2.2
    
    red_mat = bpy.data.materials.new("Red")
    red_mat.use_nodes = True
    red_mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (1,0,0,0.8)
    
    black_mat = bpy.data.materials.new("Black")
    black_mat.use_nodes = True
    black_mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0,0,0,1)

    grid_size_x = 20;
    grid_size_y = 20;
    
    procedural_generator(grid_size_x, grid_size_y, cube_size, cube_spacing, red_mat, black_mat)


if __name__ == "__main__":
    clean_scene()
    main()