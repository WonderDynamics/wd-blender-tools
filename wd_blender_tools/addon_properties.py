# Copyright 2025 Wonder Dynamics (an Autodesk Company)

# This source code is licensed under the GNU GPLv3
# found in the LICENSE file in the root directory of this source tree.

"""Module that defines the custom properties used in the add-on."""

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, StringProperty
from bpy.types import PropertyGroup

from .addon_helper import write_armature_name, write_face_name


class ValidatorProperties(PropertyGroup):
    """Class that holds all the information needed for the validation."""

    validation_metadata_message = {}
    validation_cleanup_messages = {}
    validation_fail_messages = {}
    validation_warning_messages = {}
    cleanup_required: BoolProperty(default=False)
    validation_status = {'status': 'STATUS: Run Validation.', 'alert': True}

    test_bool: BoolProperty(
        name='Test Bool 2',
        default=False,
        description='Test.',
    )
    toggle_torso: BoolProperty(name='Torso', default=True)
    toggle_head: BoolProperty(name='Head', default=True)
    toggle_legs: BoolProperty(name='Legs', default=True)
    toggle_arms: BoolProperty(name='Arms', default=True)
    toggle_hands: BoolProperty(name='Hands', default=True)

    toggle_usd: BoolProperty(name='Enable USD Support', default=False, description='Required for USD, Maya and Unreal Engine export')

    target_arm: StringProperty(
        name='Body Armature with Bones',
        description='Armature which contains bones for body animation',
        default='',
        update=write_armature_name,
    )
    target_mesh: StringProperty(
        name='Face Mesh with Blendshapes',
        description='Mesh which contains blendshapes for facial animation',
        default='',
        update=write_face_name,
    )

    eye_bone_name: StringProperty(name='Eye Bone Name', description='Name of the eye bone to be rigged', default='')
    all_available_axis = ['X', 'Y', 'Z']
    eye_horizontal_axis: EnumProperty(
        name='Horizontal Axis (local)',
        description='Chose horizontal local axis of rotation for the selected eye bone',
        items=[(axis, axis, '') for axis in all_available_axis],
        default='X',
    )
    eye_look_left: FloatProperty(name='Look Left (°)', default=-40.0, min=-180.0, max=180.0)
    eye_look_right: FloatProperty(name='Look Right (°)', default=30.0, min=-180.0, max=180.0)
    eye_vertical_axis: EnumProperty(
        name='Vertical Axis (local)',
        description='Chose vertical local axis of rotation for the selected eye bone',
        items=[(axis, axis, '') for axis in all_available_axis],
        default='Z',
    )
    eye_look_down: FloatProperty(name='Look Down (°)', default=-20.0, min=-180.0, max=180.0)
    eye_look_up: FloatProperty(name='Look Up (°)', default=25.0, min=-180.0, max=180.0)

    # METADATA JSON INIT
    metadata = {
        'software': 'blender',
        'version': '0.0.0',
        'materials': [],
        'eyes_rig': [],
        'body': {
            'armature_name': None,
            'bone_names': {
                'Hips': None,
                'LeftUpLeg': None,
                'RightUpLeg': None,
                'Spine': None,
                'LeftLeg': None,
                'RightLeg': None,
                'Spine1': None,
                'LeftFoot': None,
                'RightFoot': None,
                'Spine2': None,
                'LeftToeBase': None,
                'RightToeBase': None,
                'Neck': None,
                'LeftShoulder': None,
                'RightShoulder': None,
                'Head': None,
                'LeftArm': None,
                'RightArm': None,
                'LeftForeArm': None,
                'RightForeArm': None,
                'LeftHand': None,
                'RightHand': None,
                'LeftHandIndex1': None,
                'LeftHandIndex2': None,
                'LeftHandIndex3': None,
                'LeftHandMiddle1': None,
                'LeftHandMiddle2': None,
                'LeftHandMiddle3': None,
                'LeftHandPinky1': None,
                'LeftHandPinky2': None,
                'LeftHandPinky3': None,
                'LeftHandRing1': None,
                'LeftHandRing2': None,
                'LeftHandRing3': None,
                'LeftHandThumb1': None,
                'LeftHandThumb2': None,
                'LeftHandThumb3': None,
                'RightHandIndex1': None,
                'RightHandIndex2': None,
                'RightHandIndex3': None,
                'RightHandMiddle1': None,
                'RightHandMiddle2': None,
                'RightHandMiddle3': None,
                'RightHandPinky1': None,
                'RightHandPinky2': None,
                'RightHandPinky3': None,
                'RightHandRing1': None,
                'RightHandRing2': None,
                'RightHandRing3': None,
                'RightHandThumb1': None,
                'RightHandThumb2': None,
                'RightHandThumb3': None,
            },
        },
        'face': {
            'mesh_name': None,
            'blendshape_names': {
                'Basis': None,
                'browInnerDnL': None,
                'browInnerDnR': None,
                'browInnerUpL': None,
                'browInnerUpR': None,
                'browOuterDnL': None,
                'browOuterDnR': None,
                'browOuterUpL': None,
                'browOuterUpR': None,
                'browSqueezeL': None,
                'browSqueezeR': None,
                'cheekBlowL': None,
                'cheekBlowR': None,
                'cheekUpL': None,
                'cheekUpR': None,
                'eyeBlinkL': None,
                'eyeBlinkR': None,
                'eyeCompressL': None,
                'eyeCompressR': None,
                'eyeDn': None,
                'eyeL': None,
                'eyeR': None,
                'eyeSquintL': None,
                'eyeSquintR': None,
                'eyeUp': None,
                'eyeWidenLowerL': None,
                'eyeWidenLowerR': None,
                'eyeWidenUpperL': None,
                'eyeWidenUpperR': None,
                'jawIn': None,
                'jawL': None,
                'jawOpen': None,
                'jawOut': None,
                'jawR': None,
                'lipChinRaiserL': None,
                'lipChinRaiserR': None,
                'lipCloseLower': None,
                'lipCloseUpper': None,
                'lipCornerDnL': None,
                'lipCornerDnR': None,
                'lipCornerUpL': None,
                'lipCornerUpR': None,
                'lipDimplerL': None,
                'lipDimplerR': None,
                'lipFunnelerLower': None,
                'lipFunnelerUpper': None,
                'lipLowerDnL': None,
                'lipLowerDnR': None,
                'lipLowerPullDnL': None,
                'lipLowerPullDnR': None,
                'lipLowerUpL': None,
                'lipLowerUpR': None,
                'lipNarrowL': None,
                'lipNarrowR': None,
                'lipPoutLower': None,
                'lipPoutUpper': None,
                'lipPresserL': None,
                'lipPresserR': None,
                'lipPucker': None,
                'lipPullL': None,
                'lipPullR': None,
                'lipPushLower': None,
                'lipPushUpper': None,
                'lipSmileClosedL': None,
                'lipSmileClosedR': None,
                'lipSmileOpenL': None,
                'lipSmileOpenR': None,
                'lipSneerL': None,
                'lipSneerR': None,
                'lipStickyL': None,
                'lipStickyR': None,
                'lipSuckLower': None,
                'lipSuckUpper': None,
                'lipSwingL': None,
                'lipSwingR': None,
                'lipTightnerL': None,
                'lipTightnerR': None,
                'lipUpperDnL': None,
                'lipUpperDnR': None,
                'lipUpperUpL': None,
                'lipUpperUpR': None,
                'lipWidenL': None,
                'lipWidenR': None,
                'noseCompress': None,
                'noseFlare': None,
                'noseSneerL': None,
                'noseSneerR': None,
                'noseWrinklerL': None,
                'noseWrinklerR': None,
            },
        },
    }


class BoneSelectorStringProperty(bpy.types.PropertyGroup):
    """Property that can hold a bone mapping."""

    bone_name: StringProperty(name='bone_name', description='bone_name', default='')
