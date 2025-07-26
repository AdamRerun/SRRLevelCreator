import bpy
import json
import os
from mathutils import Vector

class ExportAllCurvesOperator(bpy.types.Operator):
    bl_idname = "object.export_all_curves"
    bl_label = "Export All Curves to JSON"
    bl_description = "Export all curve objects in the scene to a JSON file"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        data = []

        for obj in bpy.data.objects:
            if obj.type == 'CURVE' and 'rail' in obj.name.lower():
                for spline in obj.data.splines:
                    if spline.type == 'BEZIER':
                        curve_points = []
                        reference_up = Vector((0, 1, 0))

                        for i, point in enumerate(spline.bezier_points):
                            p = point.co
                            h1 = point.handle_left
                            h2 = point.handle_right

                            tangent = (h1 - h2).normalized()

                            if abs(tangent.dot(reference_up)) > 0.999:
                                reference_up = Vector((-1, 0, 0))

                            normal = tangent.cross(reference_up).normalized()
                            
                            reference_up = normal.cross(tangent).normalized()

                            curve_points.append({
                                'position': [-p.x, p.z, p.y],
                                'tangentIn': [-h1.x, h1.z, h1.y],
                                'tangentOut': [-h2.x, h2.z, h2.y],
                                'normal': [normal.x, normal.z, normal.y]
                            })
                        data.append({
                            'name': obj.name,
                            'curvePosition': [-obj.location.x, obj.location.z, obj.location.y],
                            'points': curve_points
                        })


        blend_path = bpy.data.filepath
        if not blend_path:
            self.report({'ERROR'}, "Please save your .blend file first.")
            return {'CANCELLED'}

        blend_dir = os.path.dirname(blend_path)
        blend_name = os.path.splitext(os.path.basename(blend_path))[0]
        export_path = os.path.join(blend_dir, f"{blend_name}.json")

        with open(export_path, 'w') as f:
            json.dump(data, f, indent=4)

        self.report({'INFO'}, f"Exported {len(data)} curves to {export_path}")
        return {'FINISHED'}

class ExportAllCurvesPanel(bpy.types.Panel):
    bl_label = "Export Curves to JSON"
    bl_idname = "OBJECT_PT_export_curves"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.export_all_curves", icon="EXPORT")

def register():
    bpy.utils.register_class(ExportAllCurvesOperator)
    bpy.utils.register_class(ExportAllCurvesPanel)

def unregister():
    bpy.utils.unregister_class(ExportAllCurvesOperator)
    bpy.utils.unregister_class(ExportAllCurvesPanel)

if __name__ == "__main__":
    register()