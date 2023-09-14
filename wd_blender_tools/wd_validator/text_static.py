# Copyright 2023 Wonder Dynamics

# This source code is licensed under the GNU GPLv3
# found in the LICENSE file in the root directory of this source tree.

"""Module storing all the text constants used in the add-on."""

from ..addon_static import (
    all_supported_bone_names,
)

supported_naming_conventions = [bn_n.split('_')[0].replace('-', ' ') for bn_n in all_supported_bone_names]
TEXT_SEPARATOR = '\n'

# Panels messages
INTRO_STR = '''Validate your characters for the Wonder Studio platform.
Generate the metadata.json file after the successful and submit it with your character.
Easily cleanup the scene and your character with a built-in automatic cleanup function.
Auto-map bones if your character uses one of the supported bone naming conventions.'''
INTRO_STR_EXTENDED = (
    '''This addon will help you validate that your character '''
    '''is compatible with the Wonder Studio platform.
After a successful validation metadata.json file will be generated.
You will have to provide this metadata.json file along with the blender file and texture files.
To get started, this Blender file needs to be saved on your local drive.
The metadata.json file will be created at the same location.
Any textures used by your character also need to be to be saved at the same location.
Before Validation starts you may be prompted with Cleanup messages.
Cleanup messages will have to be resolved before proceeding.
This can also be done automatically by clicking the Cleanup Character button.'''
)
SAVE_BLENDER_FILE_STR = '''Please save your Blender file before proceeding.'''

TEXTURES_LOCATION_STR = (
    '''Please make sure that all textures used by your characters '''
    '''are located at the same location as the Blender file.'''
)

ARMATURE_OBJECT_STR = '''[Mandatory] Select the armature object that will drive your characters body animation.'''

assign_bones_str = (
    '''Use Auto Assign Bones feature if your bones follow one of these '''
    f'''naming conventions: 
{", ".join(supported_naming_conventions)}, or assign bone names manually.'''
)

MESH_OBJECT_STR = '''[Optional] Select the mesh object that will drive your characters facial animation.'''
MESH_OBJECT_STR_EXTENDED = '''If your character has blendshapes, please select the mesh object that will drive
your characters facial performance.
When uploading a character with blendshapes on multiple objects, 
as long as the blendshape names match and blendshapes are not already connected, 
they will automatically be connected to the blendshapes on the Main Mesh.'''

EYE_SELECTION_STR = (
    '''[Optional] By providing the rotation data for your eye bones below, '''
    '''Auto Eye Rigging will link eye control blendshapes to listed bones upon uploading your character.'''
)

EYE_SELECTION_EXPAND_STR = (
    '''Characters gaze can be driven by facial performance only '''
    '''if eye bones are connected to blendshapes.
Eye control blendshapes can drive your eye bones based on the angles and local axis that you define.
You will need to have the following blendshapes: eyeL, eyeR, EyeUp, EyeDn.
Eye bone is registered by filling out the information and clicking Add Eye Bone button.
You can register multiple eye bones.
Alternatively, eye bones can be linked to eye control blendshapes manually and this step can be skipped.'''
)

VALIDATE_STR = '''[Mandatory] Validation process will take place in 3 simple steps:
Cleanup > Validation > Warning.
After the Validation step passes successfully metadata.json file will be generated.'''
VALIDATE_EXPAND_STR = '''Cleanup is a pre-validation step.
You can resolve cleanup messages by clicking the Cleanup Character button that will appear.
The Validation step will check for all conditions that can result in a failed upload.
If this step passes, a metadata.json will be generated and you will be able to upload your character.
The Warning step will point out issues with your character that can lead to suboptimal performance. 
It is recommended to resolve warning messages but it is not mandatory.'''

# Operators messages
ADD_EYE_BONE_REGISTERED = 'Selected eye bone is already registered!'
ADD_EYE_BONE_REGISTERED_AS_POSE = 'Eye bone already registered as pose bone!'
ADD_EYE_BONE_SAME_AXIS = 'Horizontal and vertical axis are the same!'
ADD_EYE_BONE_CONSTRAINTS = 'Bone constraints detected! Please note that bone constraints might affect animation.'
ADD_EYE_BONE_ROTATION_MODE = (
    'Bone rotation mode is not XYZ! Bone rotation mode will automatically be set as XYZ on upload.'
)

CLEANUP_COMPLETE = 'Cleanup completed. Please re-run Validation!'
CLEANUP_COMPLETE_STATUS = 'STATUS: Run Validation.'
CLEANUP_CHECK = '''Cleanup may change the properties of your objects.
Your file may be altered and elements removed.
Characters naming, scale, and more may change.
Do you wish to proceed?'''

VALIDATE_NO_ARM = 'Main Pose Armature is not assigned!'
VALIDATE_ARM_TYPE = 'Main Pose Armature object must be of type ARMATURE, not'
VALIDATE_NO_HIPS = 'Hips bone is not assigned!'
VALIDATE_DUPLICATE_BONES = 'Duplicate bones detected! Following bones are assigned more than once:'
VALIDATE_MESH_TYPE = 'Main Mesh with Blendshapes object must be of type MESH, not'
VALIDATE_NO_BS = 'Main Face Mesh does not contain any blendshapes!'
VALIDATE_SAME_EYE_AND_POSE_BONES = 'Invalid eye bones detected! Following eye bones are assigned as body bones:'

VALIDATION_FAILED_METADATA = 'Validation Failed! \nMetadata file does not match the scene information!'
VALIDATION_FAILED_METADATA_STATUS = 'STATUS: Run Validation.'

VALIDATION_FAILED_CLEANUP = (
    'Validation Failed! \nCleanup required! \nPlease review validation result '
    'messages and initiate cleanup before proceeding.'
)
VALIDATION_FAILED_CLEANUP_STATUS = 'STATUS: Run Cleanup.'

VALIDATION_FAILED = 'Validation Failed! \nMain requirements not fulfilled! \nPlease review validation result messages.'
VALIDATION_FAILED_STATUS = 'STATUS: Failed.'

VALIDATION_PASSED_WARNINGS = 'Validation Passed with Warnings.'
VALIDATION_PASSED_WARNINGS_STATUS = 'STATUS: Passed with Warnings.'

VALIDATION_PASSED = 'Validation Passed.'
VALIDATION_PASSED_STATUS = 'STATUS: Passed.'

VALIDATION_EXPORT_FAILED = 'Export failed! Data could not be saved! Please make sure that you have write permissions in the folder you are working in.'

# Blender specific validator extension messages
TEXTURE_FILES_EXTEND_STR = (
    '''\nNOTE: All texture files (or folders containing texture files) used '''
    '''by the character need to be placed in the same directory as the characters blender file.'''
)
