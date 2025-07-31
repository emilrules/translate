"""Generate a Blender script from OpenPose keypoints."""

import json
from pathlib import Path
from typing import Dict, Any


BONE_MAP = {
    "Nose": "head",
    "Neck": "neck",
    "RShoulder": "upper_arm.R",
    "RElbow": "forearm.R",
    "RWrist": "hand.R",
    "LShoulder": "upper_arm.L",
    "LElbow": "forearm.L",
    "LWrist": "hand.L",
    # Add more mappings as needed
}


def generate_blender_script(keypoints_path: Path, output_path: Path, script_path: Path = Path("generated_script.py")) -> Path:
    """Create a Blender Python script that animates an armature using the given keypoints."""
    keypoints_path = Path(keypoints_path)
    output_path = Path(output_path)
    script_path = Path(script_path)

    script_lines = [
        "import bpy, json",
        f"with open(r'{keypoints_path}', 'r') as f:",
        "    data = json.load(f)",
        "arm = bpy.data.objects['Armature']",
        "bone_map = {" + ", ".join(f'\"{k}\":\"{v}\"' for k, v in BONE_MAP.items()) + "}",
        "for frame, kp in enumerate(data['people']):",
        "    bpy.context.scene.frame_set(frame+1)",
        "    for joint, coords in kp.items():",
        "        if joint not in bone_map: continue",
        "        bone = arm.pose.bones[bone_map[joint]]",
        "        x, y = coords[0], coords[1]",
        "        bone.location = (x, y, 0)",
        "        bone.keyframe_insert(data_path='location', frame=frame+1)",
        "bpy.context.scene.render.filepath = r'%s'" % output_path,
        "bpy.ops.render.render(animation=True)",
    ]

    script_path.write_text("\n".join(script_lines))
    return script_path


__all__ = ["generate_blender_script"]
