# Copyright 2023 Wonder Dynamics

# This source code is licensed under the GNU GPLv3
# found in the LICENSE file in the root directory of this source tree.

"""Module for all the Cleanup validator classes."""

import math
import re
from typing import Any

import bpy

from .validator import Validator

# The way Validator is inherited by child classes currently do change check signature
# This is something to refactor in the future, but it would take time. TODO:
# pylint: disable=arguments-renamed,arguments-differ


class ValidatorCleanup:
    """Class that diagnose and cleanup if needed and also executes the cleanup.
    all the validation and cleanup work is done by delegating the work to
    classes like ValidatorCleanupTextFiles, ValidatorCleanupArmaturePosePosition,
    ValidatorCleanupHipsBoneRelations, ValidatorCleanupBoneRotationMode,
    ValidatorCleanupTransforms, ValidatorCleanupAutoSmooth and
    ValidatorCleanupObjectNaming.

    Note: classes used by this validator are prefixed with ValidatorCleanup_.
    """

    def __call__(self, metadata: dict) -> dict:
        """Do the metadata validation.
        Args:
            metadata (dict): the metadata dictionary to inspect.
            current_addon_version (str): The addon version, for example 1.0.2
        Returns:
            dict: a dictionary holding the results of all the validations run where
                keys are the identifier of the validation and values are dictionaries
                with the following keys:
                    check (bool): whether or not the check passed.
                    message (str): the explanation of what was being checked.
        """
        report_dict = {}

        text_files_object = ValidatorCleanupTextFiles()
        report_dict[text_files_object.key] = text_files_object()

        armature_pose_position_object = ValidatorCleanupArmaturePosePosition(metadata)
        report_dict[armature_pose_position_object.key] = armature_pose_position_object()

        hips_parent_connected_object = ValidatorCleanupHipsBoneRelations(metadata)
        report_dict[hips_parent_connected_object.key] = hips_parent_connected_object()

        bone_rotation_mode_object = ValidatorCleanupBoneRotationMode(metadata)
        report_dict[bone_rotation_mode_object.key] = bone_rotation_mode_object()

        # transforms_object = ValidatorCleanupTransforms()
        # report_dict[transforms_object.key] = transforms_object()

        auto_smooth_object = ValidatorCleanupAutoSmooth()
        report_dict[auto_smooth_object.key] = auto_smooth_object()

        object_naming_object = ValidatorCleanupObjectNaming()
        report_dict[object_naming_object.key] = object_naming_object()

        curves_geo_nodes_object = ValidatorCleanupCurvesGeoNodes()
        report_dict[curves_geo_nodes_object.key] = curves_geo_nodes_object()

        return report_dict


class ValidatorCleanupTextFiles(Validator):
    """Validates that there are no text files. This is a security measurement since we don't know
    what those file can contain. It can also cleanup this issue if requested.
    """

    def __init__(self) -> None:
        super().__init__()
        self.message = 'Text files detected!'
        self.key = 'text_files_check'

    def get(self) -> list:
        text_file_names = []
        for text in bpy.data.texts:
            text_file_names.append(text.name)
        return text_file_names

    def check(self, text_file_names: list) -> bool:
        if text_file_names:
            self.expand_message(f'The following text files will be removed: {", ".join(text_file_names)}')
            return False
        else:
            return True

    @staticmethod
    def cleanup() -> None:
        """Clean up method deletes all text files in scene."""
        for text in bpy.data.texts:
            bpy.data.texts.remove(text)


class ValidatorCleanupArmaturePosePosition(Validator):
    """Validates that the armature is in pose position and fixes this issue if requested."""

    def __init__(self, metadata: dict) -> None:
        super().__init__()
        self.message = (
            'Armature is not in Pose Position! Having the armature in Rest Position'
            ' will prevent character from being animated.'
        )
        self.key = 'armature_pose_position_check'

        self.metadata = metadata

    def get(self) -> str:
        armature = bpy.data.objects.get(self.metadata['body']['armature_name'])
        pose_position = armature.data.pose_position
        return pose_position

    def check(self, pose_position: str) -> bool:
        if pose_position == 'POSE':
            return True
        else:
            self.expand_message('Armature will be set to Pose Position mode.')
            return False

    @staticmethod
    def cleanup(armature_name: str) -> None:
        """Clean up method sets the pose_position to 'POSE'."""
        armature = bpy.data.objects.get(armature_name)
        armature.data.pose_position = 'POSE'


class ValidatorCleanupHipsBoneRelations(Validator):
    """Validates that the Hip bone has use_connect disabled and use_local_location enabled.
    Can cleanup this issue in the scene if requested.
    """

    def __init__(self, metadata: dict) -> None:
        super().__init__()
        self.message = (
            'Wrong Hips bone relations settings! Hips bone must be disconnected from its '
            'parent bone and local location turned on to allow for the translation of the character.'
        )
        self.key = 'hips_bone_relations_check'

        self.metadata = metadata

    def get(self) -> dict:
        armature = bpy.data.objects.get(self.metadata['body']['armature_name'])
        hips_bone = armature.data.bones.get(self.metadata['body']['bone_names']['Hips'])

        connected_checks = {'use_connect': hips_bone.use_connect, 'use_local_location': hips_bone.use_local_location}

        return connected_checks

    def check(self, connected_checks: dict) -> bool:
        if connected_checks['use_connect'] or not connected_checks['use_local_location']:
            self.expand_message(
                'Under Relations settings for the Hips bone, Connected option will be disabled'
                ' and Local Location option enabled.',
            )
            return False
        else:
            return True

    @staticmethod
    def cleanup(armature_name: str, hips_bone_name: str) -> None:
        """Clean up method sets Hip bone in armature to user_connect = False and use_local_location = True."""
        armature = bpy.data.objects.get(armature_name)

        if bpy.context.view_layer.objects.active:
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')

        hips_bone = armature.data.edit_bones.get(hips_bone_name)

        hips_bone.use_connect = False
        hips_bone.use_local_location = True

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = None
        bpy.ops.object.select_all(action='DESELECT')


class ValidatorCleanupBoneRotationMode(Validator):
    """Validates that the rotation mode (or order) in armature bones are set to XYZ.
    Can cleanup this issue in the scene if requested.
    """

    def __init__(self, metadata: dict) -> None:
        super().__init__()
        self.message = 'Wrong bone rotation mode! Rotation mode for all main pose armature bones must be XYZ.'
        self.key = 'bone_rotation_mode_check'
        self.rotation_mode = 'XYZ'

        self.metadata = metadata

    def get(self) -> list:
        bone_rotation_modes = list()
        main_pose_armature = bpy.data.objects.get(self.metadata['body']['armature_name'])
        for pose_bone in main_pose_armature.pose.bones:
            if pose_bone.rotation_mode not in bone_rotation_modes:
                bone_rotation_modes.append(pose_bone.rotation_mode)
        return bone_rotation_modes

    def check(self, bone_rotation_modes: list) -> bool:
        for bone_rotation_mode in bone_rotation_modes:
            if bone_rotation_mode != 'XYZ':
                self.expand_message('Bone rotation mode will be set to XYZ for all main pose armature bones.')
                return False
        return True

    @staticmethod
    def cleanup(armature_name: str) -> None:
        """Clean up method sets bone rotation_mode to XYZ for all bones in armature."""
        main_pose_armature = bpy.data.objects.get(armature_name)
        for pose_bone in main_pose_armature.pose.bones:
            pose_bone.rotation_mode = 'XYZ'


class ValidatorCleanupTransforms(Validator):
    """Validates that the transforms have the identity matrix (or close ot it). The tolerance for
    translation, rotation and scale is 1e-6. Can cleanup this issue in the scene if requested.
    """

    def __init__(self) -> None:
        super().__init__()
        self.message = (
            'Transforms are not applied to some objects! Objects can not have any initial location, rotation, or scale.'
        )
        self.key = 'transforms_check'

        self.supported_object_types = ['ARMATURE', 'CURVE', 'GPENCIL', 'LATTICE', 'MESH', 'META', 'SURFACE']

    def get(self) -> dict:
        # transform_values = {'location': [], 'rotation': [], 'scale': []}
        obj_transforms = {}
        view_layer = bpy.context.view_layer.objects.values()

        for obj in bpy.data.objects:
            if obj.type not in self.supported_object_types or obj not in view_layer:
                continue
            obj_transforms[obj.name] = [obj.location, obj.rotation_euler, obj.scale]
        return obj_transforms

    def check(self, obj_transforms: dict) -> bool:
        tol = 1e-6
        object_names = []
        for key, value in obj_transforms.items():
            if any(not math.isclose(val, 0.0, rel_tol=tol, abs_tol=tol) for val in value[0]): # loc
                object_names.append(key)
                continue
            if any(not math.isclose(val, 0.0, rel_tol=tol, abs_tol=tol) for val in value[1]): # rot
                object_names.append(key)
                continue
            if any(not math.isclose(val, 1.0, rel_tol=tol, abs_tol=tol) for val in value[2]): # scale
                object_names.append(key)
                continue

        if object_names:
            self.expand_message(f'Scale will be applied to following objects: {", ".join(object_names)}')
            return False
        return True

    @staticmethod
    def cleanup() -> None:
        """Applies the transformation to the objects of the supported types so translation, rotation and scale are
        clean.
        """
        supported_object_types = ['ARMATURE', 'CURVE', 'GPENCIL', 'LATTICE', 'MESH', 'META', 'SURFACE']
        view_layer = bpy.context.view_layer.objects.values()

        if bpy.context.view_layer.objects.active:
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        for obj in bpy.data.objects:
            if obj.type not in supported_object_types or obj not in view_layer:
                continue
            obj.select_set(True)

        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.select_all(action='DESELECT')


class ValidatorCleanupAutoSmooth(Validator):
    """Validates that auto smooth is disabled. Can clean up the issues in the scene if requested."""

    def __init__(self) -> None:
        super().__init__()
        self.message = (
            'Auto Smooth is enabled on some mesh objects! In some cases,'
            ' Auto Smooth can create artifacts during rendering.'
        )
        self.key = 'auto_smooth_check'

    def get(self) -> list:
        auto_smooth_values = [mesh.use_auto_smooth for mesh in bpy.data.meshes]
        return auto_smooth_values

    def check(self, auto_smooth_values: list) -> bool:
        if any(auto_smooth_values):
            self.expand_message('Auto Smooth will be disabled on all Mesh objects.')
            return False
        else:
            return True

    @staticmethod
    def cleanup() -> None:
        """Sets the use_auto_smooth to False for all meshes in the scene."""
        for mesh in bpy.data.meshes:
            if mesh.use_auto_smooth:
                mesh.use_auto_smooth = False


class ValidatorCleanupObjectNaming(Validator):
    """Validates that no object is named with a . (dot). Can clean up the issue in the scene if requested."""

    def __init__(self) -> None:
        super().__init__()
        self.message = 'Detected objects with . in their name!'
        self.key = 'syntax_check'

    def get(self) -> list:
        all_names = list()
        all_names.extend([armature.name for armature in bpy.data.armatures])
        all_names.extend([material.name for material in bpy.data.materials])
        all_names.extend([mesh.name for mesh in bpy.data.meshes])
        all_names.extend([obj.name for obj in bpy.data.objects])
        return all_names

    def check(self, all_names: list) -> bool:
        for name in all_names:
            if '.' in name:
                self.expand_message(
                    'All armature, material, mesh, and object names will be changed to include _ instead of . symbol.',
                )
                return False
        return True

    @staticmethod
    def cleanup() -> None:
        """Renames all objects that has a . (dot) in the name replacing it with a _ (underscore).
        if the resulting name collides with other in the scene, the renamed object will add a _#
        suffix.
        """
        ValidatorCleanupObjectNaming.string_swap(bpy.data.armatures)
        ValidatorCleanupObjectNaming.string_swap(bpy.data.materials)
        ValidatorCleanupObjectNaming.string_swap(bpy.data.meshes)
        ValidatorCleanupObjectNaming.string_swap(bpy.data.objects)

    @staticmethod
    def string_swap(objects) -> None:
        """Renames all objects provided that has a . (dot) in the name replacing it with a _ (underscore).
        if the resulting name collides with other in the scene, the renamed object will add a _#
        suffix.
        Args:
            objects (list[bpy.types.Object]): _description_
        """
        for obj in objects:
            if '.' not in obj.name:
                continue
            base_name = re.sub(r'\.', '_', obj.name)
            new_name = base_name
            count = 0
            while bpy.data.objects.get(new_name):
                count += 1
                new_name = f'{base_name}_{count}'
            obj.name = new_name


class ValidatorCleanupCurvesGeoNodes(Validator):
    """Validates that no object has live geometry nodes. Can cleanup the issue if requested."""

    def __init__(self) -> None:
        super().__init__()
        self.message = 'Detected curves objects with geometry nodes! All geometry nodes will be applied.'
        self.key = 'curves_geo_nodes_check'

    def get(self) -> list:
        view_layer = bpy.context.view_layer.objects.values()
        curves_objects = [obj for obj in bpy.data.objects if obj.type == 'CURVES' and obj in view_layer]
        return curves_objects

    def check(self, curves_objects: list) -> bool:
        for curves_obj in curves_objects:
            for mod in curves_obj.modifiers:
                if self._is_applyable(mod):
                    return False
        return True

    @staticmethod
    def _is_applyable(mod: Any) -> bool:
        # check type
        if mod.type != 'NODES':
            return False
        # check child nodes
        mod_node_types = [
            node.type for node in mod.node_group.nodes if node.type not in ['GROUP_INPUT', 'GROUP_OUTPUT']
        ]
        if len(mod_node_types) == 1 and mod_node_types[0] == 'DEFORM_CURVES_ON_SURFACE':
            return False
        return True

    @classmethod
    def cleanup(cls) -> None:
        """Applies all geometry nodes modifiers. If a modifier cannot be applied, it is removed."""
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = None

        view_layer = bpy.context.view_layer.objects.values()
        curves_objects = [obj for obj in bpy.data.objects if obj.type == 'CURVES' and obj in view_layer]

        for curves_obj in curves_objects:
            for mod in curves_obj.modifiers:
                if not cls._is_applyable(mod):
                    continue
                bpy.context.view_layer.objects.active = curves_obj
                try:
                    bpy.ops.object.modifier_apply(modifier=mod.name)
                except Exception:  # pylint: disable=broad-exception-caught
                    bpy.ops.object.modifier_remove(modifier=mod.name)
