# Copyright 2023 Wonder Dynamics

# This source code is licensed under the GNU GPLv3
# found in the LICENSE file in the root directory of this source tree.

"""Module that holds all the blender operators used in the addon."""

import bpy

from .addon_helper import (
    auto_assign_bone_names,
    check_duplicate_assigned_bones,
    check_eye_bones,
    cleanup_character,
    validate_character,
    write_addon_version,
    write_bone_names,
    write_shapekey_names,
    ExportData,
)
from .addon_static import (
    all_supported_bone_names,
)
from .wd_validator import text_static


class GrabSelectedArmOperator(bpy.types.Operator):
    """Operator used for picking the armature from the viewport and adding it
    to the validator properties.
    """

    bl_idname = 'object.grab_selected_arm'
    bl_label = 'Grab Selected Armature'
    bl_description = 'Grab selected armature as Main Pose Armature'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        """Enables the operator button based on whether or not there is an
        armature in active selection.
        """
        obj = context.object
        return obj and obj.type == 'ARMATURE'

    def execute(self, context):
        """Sets armature in active selection to validator properties target_arm."""
        obj = context.object
        context.window_manager.validator_properties.target_arm = obj.name
        return {'FINISHED'}


class GrabSelectedMeshOperator(bpy.types.Operator):
    """Operator used for picking the mesh from the viewport and adding it
    to the validator properties.
    """

    bl_idname = 'object.grab_selected_mesh'
    bl_label = 'Grab Selected Mesh'
    bl_description = 'Grab selected mesh as Main Face Mesh'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        """Enables the operator button based on whether or not there is an
        mesh in active selection.
        """
        obj = context.object
        return obj and obj.type == 'MESH'

    def execute(self, context):
        """Sets mesh in active selection to validator properties target_arm."""
        obj = context.object
        context.window_manager.validator_properties.target_mesh = obj.name
        return {'FINISHED'}


class AutoAssignBones(bpy.types.Operator):
    """Operator to run the automatic bone assignment based on naming conventions."""

    supported_naming_conventions = [bn_n.split('_')[0].replace('-', ' ') for bn_n in all_supported_bone_names]

    bl_idname = 'object.auto_assign_bones'
    bl_label = 'Auto Assign Bones'
    desc = 'Auto assign bones if they have a familiar bone naming convention.'
    bl_description = desc + f' Supported naming conventions: {supported_naming_conventions}'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Look for bones in the armature that matches the expected naming convention and adds them
        to the validator properties.
        """
        auto_assign_bone_names(self, context, context.window_manager.validator_properties.target_arm)
        return {'FINISHED'}


class AddEyeBone(bpy.types.Operator):
    """Operator that adds an eye rig data to the metadata dictionary. Before doing this
    the eye bone has to pass some checks.
    """

    bl_idname = 'object.add_eye_bone'
    bl_label = 'Add Eye Bone'
    bl_description = 'Add eye bone to the list'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        """This button in enabled when there is a bone in the Eye Bone Name field"""
        return context.window_manager.validator_properties.eye_bone_name

    def execute(self, context):
        """Add the bone and other eye rig data to the metadata dictionary. Before doing this
        the eye bone has to pass some checks:
            - eye bone cannot be in multiple bones.
            - eye bone cannot be in skeleton bones.
            - eye horizontal axis and vertical axis must be different.
        There are also warnings about bone having constraints and not having XYZ rotation order, but
        this won't fail the process.
        """
        validator_properties = context.window_manager.validator_properties

        registered_eye_bones = [eye_dict['bone_name'] for eye_dict in validator_properties.metadata['eyes_rig']]
        pose_bones = list(validator_properties.metadata['body']['bone_names'].values())

        if validator_properties.eye_bone_name in registered_eye_bones:
            self.report({'ERROR'}, text_static.ADD_EYE_BONE_REGISTERED)
            return {'CANCELLED'}

        if validator_properties.eye_bone_name in pose_bones:
            self.report({'ERROR'}, text_static.ADD_EYE_BONE_REGISTERED_AS_POSE)
            return {'CANCELLED'}

        if validator_properties.eye_horizontal_axis == validator_properties.eye_vertical_axis:
            self.report({'ERROR'}, text_static.ADD_EYE_BONE_SAME_AXIS)
            return {'CANCELLED'}

        if bpy.data.objects[validator_properties.target_arm].pose.bones[validator_properties.eye_bone_name].constraints:
            self.report({'WARNING'}, text_static.ADD_EYE_BONE_CONSTRAINTS)

        if (
            bpy.data.objects[validator_properties.target_arm]
            .pose.bones[validator_properties.eye_bone_name]
            .rotation_mode
            != 'XYZ'
        ):
            self.report(
                {'WARNING'},
                text_static.ADD_EYE_BONE_ROTATION_MODE,
            )

        add_eye = {
            'bone_name': validator_properties.eye_bone_name,
            'horizontal_rotation_axis': validator_properties.eye_horizontal_axis,
            'vertical_rotation_axis': validator_properties.eye_vertical_axis,
            'horizontal_min_max_value': [
                validator_properties.eye_look_left,
                validator_properties.eye_look_right,
            ],  # Left, Right
            'vertical_min_max_value': [
                validator_properties.eye_look_down,
                validator_properties.eye_look_up,
            ],  # Down, Up
        }

        validator_properties.metadata['eyes_rig'].append(add_eye)
        validator_properties.eye_bone_name = ''

        return {'FINISHED'}


class RemoveEyeBone(bpy.types.Operator):
    """Operator that removes a previously registered eye bone from the metadata
    dictionary.
    """

    bl_idname = 'object.remove_eye_bone'
    bl_label = 'Remove Eye Bone'
    bl_description = 'Remove eye bone from the list'
    bl_options = {'REGISTER', 'UNDO'}

    index: bpy.props.IntProperty()

    def execute(self, context):
        """Removes eye rig data at index from the metadata."""
        context.window_manager.validator_properties.metadata['eyes_rig'].pop(self.index)
        return {'FINISHED'}


class ValidateInfo(bpy.types.Operator):
    """Operator for showing information about the validation section."""

    bl_idname = 'object.validate_info'
    bl_label = 'Validation Info'
    bl_icon = 'INFO'
    bl_description = 'Click for more info'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):  # pylint: disable=unused-argument
        """reports the info in the status bar."""
        self.report({'INFO'}, text_static.VALIDATE_EXPAND_STR)
        return {'FINISHED'}

    def invoke(self, context, event):  # pylint: disable=unused-argument
        """Shows popup of predefined width with the information."""
        return context.window_manager.invoke_props_dialog(self, width=600)

    def draw(self, context):  # pylint: disable=unused-argument
        """Draws the info in the popup."""
        layout = self.layout
        text_lines = text_static.VALIDATE_EXPAND_STR.split('\n')
        for text_line in text_lines:
            layout.label(text=text_line)


class IntroInfo(bpy.types.Operator):
    """Operator for showing information about the add-on in general."""

    bl_idname = 'object.intro_info'
    bl_label = 'Intro Info'
    bl_icon = 'INFO'
    bl_description = 'Click for more info'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):  # pylint: disable=unused-argument
        """reports the info in the status bar."""
        self.report({'INFO'}, text_static.INTRO_STR_EXTENDED)
        return {'FINISHED'}

    def invoke(self, context, event):  # pylint: disable=unused-argument
        """Shows popup of predefined width with the information."""
        return context.window_manager.invoke_props_dialog(self, width=600)

    def draw(self, context):  # pylint: disable=unused-argument
        """Draws the info in the popup."""
        layout = self.layout
        text_lines = text_static.INTRO_STR_EXTENDED.split('\n')
        for text_line in text_lines:
            layout.label(text=text_line)


class FaceInfo(bpy.types.Operator):
    """Operator for showing information about the face section in general."""

    bl_idname = 'object.face_info'
    bl_label = 'Face Info'
    bl_icon = 'INFO'
    bl_description = 'Click for more info'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):  # pylint: disable=unused-argument
        """reports the info in the status bar."""
        self.report({'INFO'}, text_static.MESH_OBJECT_STR_EXTENDED)
        return {'FINISHED'}

    def invoke(self, context, event):  # pylint: disable=unused-argument
        """Shows popup of predefined width with the information."""
        return context.window_manager.invoke_props_dialog(self, width=600)

    def draw(self, context):  # pylint: disable=unused-argument
        """Draws the info in the popup."""
        layout = self.layout
        text_lines = text_static.MESH_OBJECT_STR_EXTENDED.split('\n')
        for text_line in text_lines:
            layout.label(text=text_line)


class EyeBoneAutoRiggingInfo(bpy.types.Operator):
    """Operator for showing information about the eye rigging section."""

    bl_idname = 'object.eye_bone_auto_rigging_info'
    bl_label = 'Eye Bone Auto Rigging Info'
    bl_icon = 'INFO'
    bl_description = 'Click for more info'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):  # pylint: disable=unused-argument
        """reports the info in the status bar."""
        self.report({'INFO'}, text_static.EYE_SELECTION_EXPAND_STR)
        return {'FINISHED'}

    def invoke(self, context, event):  # pylint: disable=unused-argument
        """Shows popup of predefined width with the information."""
        return context.window_manager.invoke_props_dialog(self, width=600)

    def draw(self, context):  # pylint: disable=unused-argument
        """Draws the info in the popup."""
        layout = self.layout
        text_lines = text_static.EYE_SELECTION_EXPAND_STR.split('\n')
        for text_line in text_lines:
            layout.label(text=text_line)


class CleanupCharacter(bpy.types.Operator):
    """Operator that runs the character clean-up."""

    bl_idname = 'object.cleanup_character'
    bl_label = 'Cleanup Character'
    bl_description = 'Automatically cleanup the character, resolve cleanup messages and proceed with validation'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Runs the character cleanup and updates the validation status accordingly."""
        validator_properties = context.window_manager.validator_properties
        cleanup_character(self, context)
        validator_properties.cleanup_required = False
        self.report(
            {'INFO'},
            text_static.CLEANUP_COMPLETE,
        )
        validator_properties.validation_cleanup_messages.clear()
        validator_properties.validation_status['status'] = text_static.CLEANUP_COMPLETE_STATUS
        return {'FINISHED'}

    def invoke(self, context, event):  # pylint: disable=unused-argument
        """Shows popup of predefined width with the information."""
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):  # pylint: disable=unused-argument
        """Draws the info in the popup."""
        for message in text_static.CLEANUP_CHECK.split(text_static.TEXT_SEPARATOR):
            self.layout.label(text=message)

    def execute_confirm(self, context):  # pylint: disable=unused-argument
        """Runs the character clean-up as soon as the user confirms the popup."""
        return self.execute(context)


class ValidateCharacter(bpy.types.Operator):
    """Runs the full validation for a character."""

    bl_idname = 'object.validate_character'
    bl_label = 'Validate Character'
    bl_description = 'Check if the character is compatible with the Wonder Studio platform'
    bl_options = {'REGISTER', 'UNDO'}

    def pre_check_pose_armature(self, target_arm) -> bool:
        '''Check if pose armature is assigned and if it is of right type.
        Args:
            target_arm: bpy.types.Object
                Object to check.
        Returns:
            bool
        '''
        if not target_arm:
            self.report({'ERROR'}, text_static.VALIDATE_NO_ARM)
            return False

        if target_arm.type != 'ARMATURE':
            self.report(
                {'ERROR'},
                f'{text_static.VALIDATE_ARM_TYPE} {target_arm.type}.',
            )
            return False
        return True

    def pre_check_pose_armature_hips_bone(self, target_arm_bones: dict) -> bool:
        '''Check if the Hips bone is assigned.
        Args:
            target_arm_bones: dict
                Bone mapping dictionary.
        Returns:
            bool
        '''
        if not target_arm_bones['Hips']:
            self.report({'ERROR'}, text_static.VALIDATE_NO_HIPS)
            return False
        return True

    def pre_check_pose_armature_duplicate_bones(self, target_arm_bones: dict) -> bool:
        '''Check if the bone is assigned more than once.
        Args:
            target_arm_bones: dict
                Bone mapping dictionary.
        Returns:
            bool
        '''
        duplicate_bones = check_duplicate_assigned_bones(target_arm_bones)
        if duplicate_bones:
            self.report({'ERROR'}, f'{text_static.VALIDATE_DUPLICATE_BONES} {", ".join(duplicate_bones)}')
            return False
        return True

    def pre_check_face_mesh(self, target_mesh) -> bool:
        '''If the face object is assigned check if it is of right type.
        Args:
            target_mesh: bpy.types.Object
                Object to check.
        Returns:
            bool
        '''
        if target_mesh and target_mesh.type != 'MESH':
            self.report(
                {'ERROR'},
                f'{text_static.VALIDATE_MESH_TYPE} {target_mesh.type}',
            )
            return False
        return True

    def pre_check_face_mesh_blendshapes(self, target_mesh) -> bool:
        '''If the face object is assigned check if it has any eligible blendshapes.
        Args:
            target_mesh: bpy.types.Object
                Object to check.
        Returns:
            bool
        '''
        if target_mesh and not target_mesh.data.shape_keys:
            self.report(
                {'ERROR'},
                text_static.VALIDATE_NO_BS,
            )
            return False
        return True

    def pre_check_eye_bones(self, target_arm_bones: dict, eye_bones_dict: dict) -> bool:
        '''Check if bones are assigned as body and eye bones.
        Args:
            target_arm_bones: dict
                Bone mapping dictionary.
            eye_bones_dict: dict
                Eye bone mapping dictionary.
        Returns:
            bool
        '''
        conflict_eye_bones = check_eye_bones(target_arm_bones, eye_bones_dict)
        if conflict_eye_bones:
            self.report(
                {'ERROR'},
                f'{text_static.VALIDATE_SAME_EYE_AND_POSE_BONES} {conflict_eye_bones}',
            )
            return False
        return True

    def execute(self, context):
        """Executes the full validation process, extract data, and saves the metadata.json file.
        Before doing that, it check that:
        - there is an armature assigned in the properties
        - there is at least a hip bone
        - there is a mesh assigned in the properties, that it has blend shapes
        - there are no eye rig bones that are used in the skeleton
        """
        validator_properties = context.window_manager.validator_properties
        target_arm = bpy.data.objects.get(validator_properties.target_arm)
        target_arm_bones = validator_properties.metadata['body']['bone_names']
        eye_bones_dict = validator_properties.metadata['eyes_rig']
        target_mesh = bpy.data.objects.get(validator_properties.target_mesh)

        # Refresh bone names list
        write_bone_names(context)

        # Pre-Checks
        if not self.pre_check_pose_armature(target_arm):
            return {'CANCELLED'}
        if not self.pre_check_pose_armature_hips_bone(target_arm_bones):
            return {'CANCELLED'}
        if not self.pre_check_pose_armature_duplicate_bones(target_arm_bones):
            return {'CANCELLED'}
        if not self.pre_check_face_mesh(target_mesh):
            return {'CANCELLED'}
        if not self.pre_check_face_mesh_blendshapes(target_mesh):
            return {'CANCELLED'}
        if not self.pre_check_eye_bones(target_arm_bones, eye_bones_dict):
            return {'CANCELLED'}

        # Pre Validation Data-Dump
        write_shapekey_names(validator_properties.target_mesh, validator_properties.metadata)
        write_addon_version(validator_properties.metadata)

        # Start Validation
        call = validate_character(self, context)

        if call == 'metadata':
            self.report(
                {'ERROR'},
                text_static.VALIDATION_FAILED_METADATA,
            )
            validator_properties.validation_status['alert'] = True
            validator_properties.validation_status['status'] = text_static.VALIDATION_FAILED_METADATA_STATUS
            return {'CANCELLED'}

        if call == 'cleanup':
            self.report(
                {'ERROR'},
                text_static.VALIDATION_FAILED_CLEANUP,
            )
            validator_properties.validation_status['alert'] = True
            validator_properties.validation_status['status'] = text_static.VALIDATION_FAILED_CLEANUP_STATUS
            return {'CANCELLED'}

        if call == 'fail':
            self.report(
                {'ERROR'},
                text_static.VALIDATION_FAILED,
            )
            validator_properties.validation_status['alert'] = True
            validator_properties.validation_status['status'] = text_static.VALIDATION_FAILED_STATUS
            return {'CANCELLED'}

        if call == 'warning':
            self.report(
                {'WARNING'},
                text_static.VALIDATION_PASSED_WARNINGS,
            )
            validator_properties.validation_status['alert'] = False
            validator_properties.validation_status['status'] = text_static.VALIDATION_PASSED_WARNINGS_STATUS

        if call == 'clean':
            self.report(
                {'INFO'},
                text_static.VALIDATION_PASSED,
            )
            validator_properties.validation_status['alert'] = False
            validator_properties.validation_status['status'] = text_static.VALIDATION_PASSED_STATUS

        try:
            ExportData(validator_properties.metadata)

        except FileNotFoundError as exception:
            print(f'Error exporting data to disk: {exception}')
            self.report(
                {'ERROR'},
                str(exception),
            )
            return {'CANCELLED'}

        except Exception as exception:
            print(f'Error exporting data to disk: {exception}')
            self.report(
                {'ERROR'},
                text_static.VALIDATION_EXPORT_FAILED,
            )
            return {'CANCELLED'}

        return {'FINISHED'}
