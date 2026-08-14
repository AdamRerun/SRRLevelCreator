import bpy
import csv
import os
import zipfile
import tempfile
import shutil
import json

from bpy.types import Panel, Operator
from bpy.props import StringProperty
from mathutils import Vector

DEFAULT_OUTPUT_FILE = r"C:\UnityProject.rrn"

CONFIG_FILE = os.path.join(
    bpy.utils.user_resource('CONFIG'),
    "unity_export_settings.json"
)


def load_last_path():

    try:
        if os.path.isfile(CONFIG_FILE):

            with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                settings = json.load(file)

            path = settings.get("last_path", "")

            if path:
                return path

    except Exception as e:
        print(f"Could not load Unity export settings: {e}")

    return DEFAULT_OUTPUT_FILE


def save_last_path(path):

    try:

        config_dir = os.path.dirname(CONFIG_FILE)

        os.makedirs(
            config_dir,
            exist_ok=True
        )

        with open(CONFIG_FILE, "w", encoding="utf-8") as file:

            json.dump(
                {
                    "last_path": path
                },
                file,
                indent=4
            )

        print(f"Saved last export path: {path}")

    except Exception as e:

        print(f"Could not save Unity export settings: {e}")


def ensure_rrn_extension(path):

    path = path.strip()

    if not path:
        return path

    if not path.lower().endswith(".rrn"):
        path += ".rrn"

    return path


def export_glb(filepath):

    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        use_selection=False,
        export_extras=True,
        export_apply=True,
        export_normals=True,
        export_texcoords=True,
    )

    if not os.path.isfile(filepath):
        raise RuntimeError(
            f"GLB export failed. File was not created:\n{filepath}"
        )

    print(f"GLB exported: {filepath}")


def export_spline(obj, filepath):

    with open(filepath, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "X",
            "Y",
            "Z",
            "TangentX",
            "TangentY",
            "TangentZ",
            "Tangent2X",
            "Tangent2Y",
            "Tangent2Z",
            "NormalX",
            "NormalY",
            "NormalZ"
        ])

        for spline in obj.data.splines:

            if spline.type != 'BEZIER':
                continue

            for point in spline.bezier_points:

                position = obj.matrix_world @ point.co
                right_handle = obj.matrix_world @ point.handle_right
                left_handle = obj.matrix_world @ point.handle_left
                reference_up = obj.matrix_world.to_3x3() @ Vector((0, 1, 0))

                tangent = right_handle - left_handle
                tangent.normalize()
                
                
                
                normal = reference_up.cross(tangent)
                if normal.length < 0.0001:
                    reference_up = obj.matrix_world.to_3x3() @ Vector((0, 0, 1))
                    normal = reference_up.cross(tangent)

                normal.normalize()
                
                
                writer.writerow([
                    -position.x,
                    position.z,
                    -position.y,
                    -left_handle.x,
                    left_handle.z,
                    -left_handle.y,
                    -right_handle.x,
                    right_handle.z,
                    -right_handle.y,
                    -normal.x,
                    normal.z,
                    -normal.y
                ])


def get_spline_filename(obj):

    name_lower = obj.name.lower()

    if "rail" in name_lower:
        return f"{obj.name}.csv"

    if "path" in name_lower:

        if obj.parent is not None:
            return f"{obj.parent.name}.csv"

        return f"{obj.name}.csv"

    return f"{obj.name}.csv"


def create_rrn(output_path):

    temp_dir = tempfile.mkdtemp()

    try:

        glb_path = os.path.join(
            temp_dir,
            "scene.glb"
        )

        export_glb(glb_path)

        rail_dir = os.path.join(
            temp_dir,
            "Rails"
        )

        spline_dir = os.path.join(
            temp_dir,
            "Splines"
        )

        os.makedirs(
            rail_dir,
            exist_ok=True
        )

        os.makedirs(
            spline_dir,
            exist_ok=True
        )

        curve_objects = [
            obj
            for obj in bpy.context.scene.objects
            if obj.type == 'CURVE'
            and any(
                spline.type == 'BEZIER'
                for spline in obj.data.splines
            )
        ]

        rail_files = []
        spline_files = []

        for obj in curve_objects:

            name_lower = obj.name.lower()
            is_rail = "rail" in name_lower

            filename = get_spline_filename(obj)

            if is_rail:
                export_dir = rail_dir
                archive_dir = "Rails"
            else:
                export_dir = spline_dir
                archive_dir = "Splines"

            filepath = os.path.join(
                export_dir,
                filename
            )

            if os.path.exists(filepath):

                base, extension = os.path.splitext(
                    filename
                )

                counter = 1

                while os.path.exists(filepath):

                    filename = (
                        f"{base}_{counter}"
                        f"{extension}"
                    )

                    filepath = os.path.join(
                        export_dir,
                        filename
                    )

                    counter += 1

            export_spline(
                obj,
                filepath
            )

            archive_path = (
                f"{archive_dir}/{filename}"
            )

            if is_rail:

                rail_files.append(
                    (
                        filepath,
                        archive_path
                    )
                )

            else:

                spline_files.append(
                    (
                        filepath,
                        archive_path
                    )
                )

            print(
                f"{'Rail' if is_rail else 'Path'} exported: "
                f"{obj.name} -> {archive_path}"
            )

        output_directory = os.path.dirname(
            os.path.abspath(output_path)
        )

        if output_directory:
            os.makedirs(
                output_directory,
                exist_ok=True
            )

        with zipfile.ZipFile(
            output_path,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9
        ) as rrn_file:

            rrn_file.write(
                glb_path,
                "scene.glb"
            )

            for filepath, archive_path in rail_files:

                rrn_file.write(
                    filepath,
                    archive_path
                )

            for filepath, archive_path in spline_files:

                rrn_file.write(
                    filepath,
                    archive_path
                )

        print("")
        print("===================================")
        print("RRN EXPORT COMPLETE")
        print("===================================")
        print("GLB: scene.glb")
        print(f"Rails: {len(rail_files)}")
        print(f"Paths: {len(spline_files)}")
        print(f"RRN: {output_path}")
        print("===================================")

    finally:

        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )


class UNITY_EXPORT_OT_export(Operator):

    bl_idname = "unity_export.export"

    bl_label = "Export Unity Project"

    bl_description = (
        "Export GLB and all Bezier splines "
        "as a compressed RRN file"
    )

    filepath: StringProperty(
        name="Output File",
        subtype='FILE_PATH'
    )

    def invoke(self, context, event):

        self.filepath = load_last_path()

        self.filepath = ensure_rrn_extension(
            self.filepath
        )

        context.window_manager.fileselect_add(self)

        return {'RUNNING_MODAL'}

    def execute(self, context):

        try:

            path = ensure_rrn_extension(
                self.filepath
            )

            if not path:
                raise RuntimeError(
                    "No output path was specified."
                )

            save_last_path(path)

            create_rrn(path)

            self.report(
                {'INFO'},
                "Unity project exported successfully!"
            )

            return {'FINISHED'}

        except Exception as e:

            self.report(
                {'ERROR'},
                str(e)
            )

            print("===================================")
            print("EXPORT ERROR")
            print("===================================")
            print(e)

            return {'CANCELLED'}


class UNITY_EXPORT_PT_panel(Panel):

    bl_label = "Unity Export"

    bl_idname = "UNITY_EXPORT_PT_panel"

    bl_space_type = 'VIEW_3D'

    bl_region_type = 'UI'

    bl_category = "Unity"

    def draw(self, context):

        layout = self.layout

        layout.label(
            text="Export Project"
        )

        layout.separator()

        layout.operator(
            "unity_export.export",
            text="Export Unity Project",
            icon='EXPORT'
        )


classes = (
    UNITY_EXPORT_OT_export,
    UNITY_EXPORT_PT_panel,
)


def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()