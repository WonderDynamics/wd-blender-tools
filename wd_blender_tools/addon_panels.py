# Copyright 2023 Wonder Dynamics

# This source code is licensed under the GNU GPLv3
# found in the LICENSE file in the root directory of this source tree.

"""Module that holds all the panels used in the add-on."""

import textwrap

import bpy

from .addon_operators import (
    AddEyeBone,
    AutoAssignBones,
    CleanupCharacter,
    EyeBoneAutoRiggingInfo,
    FaceInfo,
    GrabSelectedArmOperator,
    GrabSelectedMeshOperator,
    IntroInfo,
    RemoveEyeBone,
    ValidateCharacter,
    ValidateInfo,
)
from .addon_static import (
    arm_bones,
    DOCUMENTATION_URL,
    hand_bones_left,
    hand_bones_right,
    head_bones,
    leg_bones,
    standard_bone_names,
    torso_bones,
)
from .wd_validator import text_static


def label_multiline(context, parent, text: str, icon: str, scale: float, padding: int = 0) -> None:
    """Adds a multiline text field with word wrap.
    Args:
        context (bpy.context): the current blender context.
        parent (bpy.types.UILayout): the parent layout.
        text (str): the text to display.
        icon (str): the icon name, for example 'ERROR'
        scale (float): ui scale to be able to adjust with global scale.
        padding (int, optional): horizontal padding. Defaults to 0.
    """
    col = parent.column(align=True)

    width = (context.region.width / scale) - padding
    chars = int((0.2071429 * width - 17.14286) * 0.95)
    wrapper = textwrap.TextWrapper(width=max(1, chars))

    text_segments = text.split('\n')
    text_lines = []

    for text_segment in text_segments:
        text_lines.extend(wrapper.wrap(text=text_segment))

    for i, text_line in enumerate(text_lines):
        if i == 1 and icon != 'NONE':
            icon = 'BLANK1'
        col.label(text=text_line, icon=icon)


class WSCharacterValidator:
    """Base class for all add-on panels. Defines the space type and the region type."""

    bl_idname = 'OBJECT_PT_WSCharVal'
    bl_category = 'Wonder Studio Character Validator'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


class Intro(WSCharacterValidator, bpy.types.Panel):
    """Add-on Intro panel. Shows information and links to documentation."""

    bl_label = 'Introduction'
    bl_idname = 'OBJECT_PT_WSCharVal_Intro'

    def draw(self, context):
        """Draws the widgets on the panel."""
        ui_scale = context.preferences.view.ui_scale

        split = self.layout.split(factor=1 - (30 * ui_scale / context.region.width))
        label_multiline(
            context=context, parent=split, text=text_static.INTRO_STR, icon='NONE', scale=ui_scale, padding=30
        )
        split.operator(IntroInfo.bl_idname, text='', icon=IntroInfo.bl_icon)

        operator = self.layout.operator(
            'wm.url_open',
            text='Open Documentation',
            icon='HELP',
        )
        operator.url = DOCUMENTATION_URL


class BodySelection(WSCharacterValidator, bpy.types.Panel):
    """Add-on Body Elements Panel. Defines the armature and the bone mapping."""

    bl_label = 'Select Body Elements'
    bl_idname = 'OBJECT_PT_WSCharVal_BodySelection'

    def draw_bone_elements(self, context, parent, bone_list: list, label: str, pair: bool):
        """Draws all the fields needed to map the bones for a skeleton section.
        Args:
            context (bpy.context): the current blender context.
            parent (bpy.types.UILayout): the parent layout.
            bone_list (list): List of bones to draw.
            label (str): Title for this bone section.
            pair (bool): Whether or not the bones are symmetric limbs, for example
                legs, arms, etc.
        """
        validator_properties = context.window_manager.validator_properties

        box = parent.box()
        if label != '':
            box.label(text=label)
        box_parent = box

        for i, bone in enumerate(bone_list):
            index = standard_bone_names.index(bone)
            if pair and ((i + 1) % 2) != 0:
                box_parent = box.row()
            box_parent.prop_search(
                context.scene.bone_selector_collection[index],
                'bone_name',
                bpy.data.objects[validator_properties.target_arm].data,
                'bones',
                text=context.scene.bone_selector_collection[index].name,
            )

    def draw(self, context):
        """Draws the panel. It holds the information for the armature, toggles
        for adding optional limb bones and the bone mapping for all bones (body only).
        Args:
            context (bpy.context): the current blender context.
        """
        filepath = bpy.path.abspath('//')
        ui_scale = context.preferences.view.ui_scale

        if not filepath:
            box = self.layout.box()
            label_multiline(
                context=context,
                parent=box,
                text=text_static.SAVE_BLENDER_FILE_STR,
                icon='ERROR',
                scale=ui_scale,
                padding=30,
            )
            box = self.layout.box()
            label_multiline(
                context=context,
                parent=box,
                text=text_static.TEXTURES_LOCATION_STR,
                icon='ERROR',
                scale=ui_scale,
                padding=30,
            )
            return

        validator_properties = context.window_manager.validator_properties

        # Assign Main Pose Armature
        self.layout.separator()
        label_multiline(
            context=context,
            parent=self.layout,
            text=text_static.ARMATURE_OBJECT_STR,
            icon='NONE',
            scale=ui_scale,
            padding=20,
        )
        row = self.layout.row()
        split = row.split(factor=1 - (60 * ui_scale / context.region.width))
        split.prop_search(validator_properties, 'target_arm', bpy.data, 'objects')
        split.operator(GrabSelectedArmOperator.bl_idname, text='', icon='TRACKING_BACKWARDS')
        self.layout.separator()

        # Pose Bone Selection Elements
        if not bpy.data.objects.get(validator_properties.target_arm):
            return
        if not bpy.data.objects.get(validator_properties.target_arm).type == 'ARMATURE':
            return

        # Assign Pose Bones
        box_m = self.layout.box()
        box_m.label(text='Assign Pose Bones:', icon='UV_SYNC_SELECT')
        label_multiline(
            context=context,
            parent=box_m,
            text=text_static.assign_bones_str,
            icon='NONE',
            scale=ui_scale,
        )

        box = box_m.box()
        row = box.row()
        row.label(text='Show/Hide Bone Groups:', icon='HIDE_OFF')
        row = box.row(align=True)
        row.prop(validator_properties, 'toggle_torso', toggle=True)
        row.prop(validator_properties, 'toggle_head', toggle=True)
        row.prop(validator_properties, 'toggle_legs', toggle=True)
        row.prop(validator_properties, 'toggle_arms', toggle=True)
        row.prop(validator_properties, 'toggle_hands', toggle=True)
        box_m.separator()

        split = box_m.split(factor=0.7)
        split1 = split.split(factor=0.42857)
        row = split1.row()
        row = split1.row()
        row.operator(AutoAssignBones.bl_idname, text=AutoAssignBones.bl_label, icon='UV_SYNC_SELECT')
        row = split.row()
        box_m.separator()

        col = box_m.column()
        box_pelvis = col.box()
        box_pelvis.label(text='[Mandatory] Main Translation Bone:')
        box_pelvis.prop_search(
            context.scene.bone_selector_collection[0],
            'bone_name',
            bpy.data.objects[validator_properties.target_arm].data,
            'bones',
            text=context.scene.bone_selector_collection[0].name,
        )
        col.separator()

        if validator_properties.toggle_torso is True:
            self.draw_bone_elements(context, col, torso_bones, 'Torso Bones:', False)
            col.separator()

        if validator_properties.toggle_head is True:
            self.draw_bone_elements(context, col, head_bones, 'Head Bones:', False)
            col.separator()

        if validator_properties.toggle_legs is True:
            self.draw_bone_elements(context, col, leg_bones, 'Leg Bones:', True)
            col.separator()

        if validator_properties.toggle_arms is True:
            self.draw_bone_elements(context, col, arm_bones, 'Arm Bones:', True)
            col.separator()

        if validator_properties.toggle_hands is True:
            box_hands = col.box()
            box_hands.label(text='Hand Bones:')
            row = box_hands.row()
            left_col = row.column()
            self.draw_bone_elements(context, left_col, hand_bones_left, '', False)
            right_col = row.column()
            self.draw_bone_elements(context, right_col, hand_bones_right, '', False)
            col.separator()

        col.separator()
        self.layout.separator()


class FaceSelection(WSCharacterValidator, bpy.types.Panel):
    """Add-on Face Elements Panel. Defines the face mesh with blendshapes and optionally
    the eye bones mapping."""

    bl_label = 'Select Face Elements'
    bl_idname = 'OBJECT_PT_WSCharVal_FaceSelection'

    def draw(self, context):
        """Draws the panel. It holds the information for the face mesh, a widget
        for adding new eye bones with their settings and a list of already assigned
        eyes bones.
        Args:
            context (bpy.context): the current blender context.
        """
        filepath = bpy.path.abspath('//')
        ui_scale = context.preferences.view.ui_scale

        if not filepath:
            self.layout.label(text='', icon='ERROR')
            return

        validator_properties = context.window_manager.validator_properties

        # Assign Main Face Mesh
        self.layout.separator()

        split = self.layout.split(factor=1 - (30 * ui_scale / context.region.width))
        label_multiline(
            context=context, parent=split, text=text_static.MESH_OBJECT_STR, icon='NONE', scale=ui_scale, padding=30
        )
        split.operator(FaceInfo.bl_idname, text='', icon=FaceInfo.bl_icon)

        row = self.layout.row()
        split = row.split(factor=1 - (60 * ui_scale / context.region.width))
        split.prop_search(validator_properties, 'target_mesh', bpy.data, 'objects')
        split.operator(GrabSelectedMeshOperator.bl_idname, text='', icon='TRACKING_BACKWARDS')
        self.layout.separator()

        # Eye Bone Elements
        if not bpy.data.objects.get(validator_properties.target_arm):
            return
        if not bpy.data.objects.get(validator_properties.target_arm).type == 'ARMATURE':
            return
        if not bpy.data.objects.get(validator_properties.target_mesh):
            return
        if not bpy.data.objects.get(validator_properties.target_mesh).type == 'MESH':
            return

        box_m = self.layout.box()
        box_m.label(text='Assign New Eye Bone:', icon='UV_SYNC_SELECT')

        split = box_m.split(factor=1 - (30 * ui_scale / context.region.width))
        label_multiline(
            context=context,
            parent=split,
            text=text_static.EYE_SELECTION_STR,
            icon='NONE',
            scale=ui_scale,
            padding=40,
        )
        split.operator(EyeBoneAutoRiggingInfo.bl_idname, text='', icon=EyeBoneAutoRiggingInfo.bl_icon)

        col = box_m.column()
        col.prop_search(
            validator_properties,
            'eye_bone_name',
            bpy.data.objects[validator_properties.target_arm].data,
            'bones',
        )

        col.prop(validator_properties, 'eye_horizontal_axis')
        split = col.split(factor=0.5)
        split.prop(validator_properties, 'eye_look_left')
        split.prop(validator_properties, 'eye_look_right')

        col.prop(validator_properties, 'eye_vertical_axis')
        split = col.split(factor=0.5)
        split.prop(validator_properties, 'eye_look_down')
        split.prop(validator_properties, 'eye_look_up')

        box_m.separator()
        split = box_m.split(factor=0.7)
        split1 = split.split(factor=0.42857)
        row = split1.row()
        row = split1.row()
        row.operator(AddEyeBone.bl_idname, text=AddEyeBone.bl_label, icon='PLUS')
        row = split.row()
        box_m.separator()

        self.layout.separator()

        eye_bones_list = validator_properties.metadata['eyes_rig']
        if eye_bones_list:
            box_m = self.layout.box()
            box_m.label(text='Assigned Eye Bones', icon='CHECKBOX_HLT')
            for i, eye_dict in enumerate(eye_bones_list):
                eye_bone_name = eye_dict.get('bone_name')
                if eye_bone_name:
                    box = box_m.box()
                    split = box.split(factor=1 - (60 * ui_scale / context.region.width))
                    split.label(text=f'{i}. Eye bone: {eye_bone_name}')
                    operator = split.operator(RemoveEyeBone.bl_idname, text='', icon='CANCEL')
                    operator.index = i
            self.layout.separator()


class Validate(WSCharacterValidator, bpy.types.Panel):
    """Add-on Character Validation Panel. Displays the validation messages and can
    launch validation or cleanup processes."""

    bl_label = 'Character Validation'
    bl_idname = 'OBJECT_PT_WSCharVal_Validate'

    def draw(self, context):
        """Draws the panel. It holds the validation messages and can
        launch validation or cleanup processes.
        Args:
            context (bpy.context): the current blender context.
        """
        filepath = bpy.path.abspath('//')
        ui_scale = context.preferences.view.ui_scale

        if not filepath:
            self.layout.label(text='', icon='ERROR')
            return

        validator_properties = context.window_manager.validator_properties

        split = self.layout.split(factor=1 - (30 * ui_scale / context.region.width))
        label_multiline(
            context=context, parent=split, text=text_static.VALIDATE_STR, icon='NONE', scale=ui_scale, padding=30
        )
        split.operator(ValidateInfo.bl_idname, text='', icon=ValidateInfo.bl_icon)

        box_m = self.layout.box()
        box_m.label(text='Validation result messages:', icon='FAKE_USER_ON')

        # Fail and Warning Messages
        for metadata_message in validator_properties.validation_metadata_message.values():
            if metadata_message['check']:
                continue
            box = box_m.box()
            label_multiline(
                context=context,
                parent=box,
                text=f'FILE ERROR:   {metadata_message["message"]}',
                icon='CANCEL',
                scale=ui_scale,
                padding=42,
            )

        for cleanup_message in validator_properties.validation_cleanup_messages.values():
            if cleanup_message['check']:
                continue
            box = box_m.box()
            label_multiline(
                context=context,
                parent=box,
                text=f'CLEANUP:   {cleanup_message["message"]}',
                icon='BRUSH_DATA',
                scale=ui_scale,
                padding=42,
            )

        for fail_message in validator_properties.validation_fail_messages.values():
            if fail_message['check']:
                continue
            box = box_m.box()
            label_multiline(
                context=context,
                parent=box,
                text=f'ERROR:   {fail_message["message"]}',
                icon='ERROR',
                scale=ui_scale,
                padding=42,
            )

        for warning_message in validator_properties.validation_warning_messages.values():
            if warning_message['check']:
                continue
            box = box_m.box()
            label_multiline(
                context=context,
                parent=box,
                text=f'WARNING:   {warning_message["message"]}',
                icon='INFO',
                scale=ui_scale,
                padding=42,
            )

        box_m.separator()

        # Validate and Cleanup Buttons
        self.layout.separator()
        box_m = self.layout.box()
        box_m.separator()

        split = box_m.split(factor=0.8)
        split1 = split.split(factor=0.25)
        row = split1.row()
        row = split1.row()
        row.alert = validator_properties.validation_status['alert']
        row.label(text=validator_properties.validation_status['status'])
        row = split.row()
        box_m.separator()

        if validator_properties.cleanup_required:
            split = box_m.split(factor=0.8)
            split1 = split.split(factor=0.25)
            row = split1.row()
            row = split1.row()
            row.operator(CleanupCharacter.bl_idname, text=CleanupCharacter.bl_label)
            row = split.row()
            box_m.separator()

        split = box_m.split(factor=0.8)
        split1 = split.split(factor=0.25)
        row = split1.row()
        row = split1.row()
        row.operator(ValidateCharacter.bl_idname, text=ValidateCharacter.bl_label)
        row = split.row()
        box_m.separator()

        self.layout.separator()
