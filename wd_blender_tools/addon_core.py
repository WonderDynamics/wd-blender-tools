# Copyright 2025 Wonder Dynamics (an Autodesk Company)

# This source code is licensed under the GNU GPLv3
# found in the LICENSE file in the root directory of this source tree.

"""Flow Studio Character Validation Add-on register functions."""

import bpy
from bpy.props import PointerProperty
from bpy.utils import register_class, unregister_class

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
from .addon_panels import BodySelection, FaceSelection, Intro, Validate
from .addon_properties import BoneSelectorStringProperty, ValidatorProperties


_classes = [
    # Properties
    ValidatorProperties,
    BoneSelectorStringProperty,
    # Panels
    Intro,
    BodySelection,
    FaceSelection,
    Validate,
    # Operators
    GrabSelectedArmOperator,
    GrabSelectedMeshOperator,
    AutoAssignBones,
    ValidateCharacter,
    RemoveEyeBone,
    AddEyeBone,
    CleanupCharacter,
    ValidateInfo,
    EyeBoneAutoRiggingInfo,
    IntroInfo,
    FaceInfo,
]


def register():
    """Function called by Blender to register the add-on."""
    for cls in _classes:
        register_class(cls)
    bpy.types.WindowManager.validator_properties = PointerProperty(type=ValidatorProperties)
    bpy.types.Scene.bone_selector_collection = bpy.props.CollectionProperty(type=BoneSelectorStringProperty)


def unregister():
    """Function called by Blender to un-register the add-on. Needs to clear
    everything defined by register function."""
    for cls in _classes:
        unregister_class(cls)

    del bpy.types.WindowManager.validator_properties
    del bpy.types.Scene.bone_selector_collection
