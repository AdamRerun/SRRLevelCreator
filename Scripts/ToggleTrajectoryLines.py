import bpy
import mathutils

# === Constants ===
TRAJECTORY_RESOLUTION = 15
TRAJECTORY_FRICTION = 0
TRAJECTORY_ACCELERATION = 0
MAX_TRAJECTORY_LENGTH = 50.0
MAX_TRAJECTORY_LINE_TIME = 2.0
TRAJECTORY_GRAVITY = 42.5
TRAJECTORY_OBJECT_NAME = "TrajectoryLine"

# === Properties ===
def get_launch_direction(obj):
    local_x = mathutils.Vector((0, -1, 0))
    local_z = mathutils.Vector((0, 0, 1))

    name = obj.name.lower()
    if "spring" in name:
        return (obj.matrix_world.to_3x3() @ local_z).normalized()
    elif "dashring" in name:
        return (obj.matrix_world.to_3x3() @ local_x).normalized()
    elif "panel" in name:
        return (obj.matrix_world.to_3x3() @ (local_x + local_z)).normalized()
    else:
        return (obj.matrix_world.to_3x3() @ local_x).normalized()

def draw_trajectory(obj):
    if "LaunchSpeed" not in obj:
        return
    name = obj.name.lower()
    if "panel" in name:
        return
    old = bpy.data.objects.get(TRAJECTORY_OBJECT_NAME)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)

    direction = get_launch_direction(obj)
    speed = obj["LaunchSpeed"]
    velocity = direction * speed

    origin = obj.location + direction.normalized()
    prev_point = origin.copy()
    points = []

    horizontal = mathutils.Vector((velocity.x, 0, 0))
    initial_horizontal_speed = horizontal.length
    horizontal_dir = horizontal.normalized() if initial_horizontal_speed > 0 else mathutils.Vector((0, 0, 0))
    vertical_velocity = velocity.z
    current_length = MAX_TRAJECTORY_LENGTH

    for i in range(1, TRAJECTORY_RESOLUTION + 1):
        t = i * (MAX_TRAJECTORY_LINE_TIME / TRAJECTORY_RESOLUTION)

        horizontal_speed = max(0.0, initial_horizontal_speed - TRAJECTORY_FRICTION * t)
        horizontal_displacement = horizontal_dir * horizontal_speed * t
        vertical_displacement = vertical_velocity * t + 0.5 * -TRAJECTORY_GRAVITY * t * t

        displacement = horizontal_displacement + mathutils.Vector((0, 0, vertical_displacement))
        current_point = origin + displacement

        points.append(current_point)

        current_length -= (current_point - prev_point).length
        if current_length <= 0:
            break

        prev_point = current_point

    curve_data = bpy.data.curves.new(TRAJECTORY_OBJECT_NAME, type='CURVE')
    curve_data.dimensions = '3D'
    polyline = curve_data.splines.new('POLY')
    polyline.points.add(len(points) - 1)

    for i, p in enumerate(points):
        polyline.points[i].co = (p.x, p.y, p.z, 1)

    curve_obj = bpy.data.objects.new(TRAJECTORY_OBJECT_NAME, curve_data)
    curve_obj.hide_select = True
    bpy.context.collection.objects.link(curve_obj)

def remove_trajectory():
    traj = bpy.data.objects.get(TRAJECTORY_OBJECT_NAME)
    if traj:
        bpy.data.objects.remove(traj, do_unlink=True)

def selection_handler(scene):
    if not bpy.context.scene.show_trajectory_preview:
        remove_trajectory()
        return

    sel = bpy.context.selected_objects
    if len(sel) == 1 and "LaunchSpeed" in sel[0]:
        draw_trajectory(sel[0])
    else:
        remove_trajectory()

# === UI Panel ===
class TrajectoryPanel(bpy.types.Panel):
    bl_label = "Trajectory Preview"
    bl_idname = "VIEW3D_PT_trajectory_preview"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Trajectory'

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "show_trajectory_preview")

# === Register/Unregister ===
classes = [TrajectoryPanel]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.show_trajectory_preview = bpy.props.BoolProperty(
        name="Show Trajectory",
        description="Show preview trajectory for objects with LaunchSpeed",
        default=True,
        update=lambda self, ctx: None
    )

    if selection_handler not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(selection_handler)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    if hasattr(bpy.types.Scene, "show_trajectory_preview"):
        del bpy.types.Scene.show_trajectory_preview
    if selection_handler in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(selection_handler)

if __name__ == "__main__":
    register()
    print("Trajectory preview with toggle icon is enabled.")
