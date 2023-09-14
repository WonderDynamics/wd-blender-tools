# Copyright 2023 Wonder Dynamics

# This source code is licensed under the GNU GPLv3
# found in the LICENSE file in the root directory of this source tree.

"""Module that implements the helper functions and classes that are used by blender objects."""

import bpy
from pathlib import Path
import json
import shutil
from typing import List
from typing import Optional
from typing import Union
from glob import glob
import re
from .addon_static import (
    all_supported_bone_names,
    all_supported_shapekey_names,
    blender_addon_version,
    standard_bone_names,
    EXPORT_FOLDER_NAME,
)
from .wd_validator import text_static

from .wd_validator.character_validation_cleanup import (
    ValidatorCleanup,
    ValidatorCleanupArmaturePosePosition,
    ValidatorCleanupAutoSmooth,
    ValidatorCleanupBoneRotationMode,
    ValidatorCleanupCurvesGeoNodes,
    ValidatorCleanupHipsBoneRelations,
    ValidatorCleanupObjectNaming,
    ValidatorCleanupTextFiles,
    ValidatorCleanupTransforms,
)


from .wd_validator.character_validation_metadata import ValidatorMetadata
from .wd_validator.character_validation_requirement import ValidatorRequirement
from .wd_validator.character_validation_warning import ValidatorWarning


def save_file():
    '''Cleanup and save the Blender file.
    Notes:
        This function has the side effect of purging orphan data blocks and saving the file.'''
    bpy.ops.outliner.orphans_purge(do_recursive=True)
    bpy.ops.wm.save_mainfile()


def register_bone_selector_collection():
    """Extends the bone collection in the scene if it is empty  with the standard
    bones names for the armature.
    """
    if bpy.context.scene.bone_selector_collection and bpy.context.scene.bone_selector_collection[0].name != 'Hips':
        bpy.context.scene.bone_selector_collection.clear()
    if not bpy.context.scene.bone_selector_collection:
        for bone_name in standard_bone_names:
            param = bpy.context.scene.bone_selector_collection.add()
            param.name = bone_name


def write_addon_version(metadata):
    """Updates metadata with current add-on version as a string.
    Version is taken form static data.
    Args:
        metadata (dict): the metadata dictionary defined in ValidatorProperties
    """
    metadata['version'] = addon_version_tuple_to_str(blender_addon_version)


def addon_version_tuple_to_str(version: tuple):
    """Converts a semantic version tuple to a dotted string representation
    Args:
        version (tuple): the version number, for example (1, 2, 3))
    Returns:
        str: the string representation, for example 1.2.3
    """
    return '.'.join(map(str, version))


def write_armature_name(self, context):
    """Update callback that updates the metadata with the armature in target_arm
    property or sets it to None if there is no armature in property. It also ensures
    that the scene has the bone selector collection initialized.
    Args:
        self (ValidatorProperties): The property group with the addon data.
        context (bpy.context): the current blender context
    """
    if self.target_arm == '':
        context.window_manager.validator_properties.metadata['body']['armature_name'] = None
    else:
        context.window_manager.validator_properties.metadata['body']['armature_name'] = self.target_arm

    register_bone_selector_collection()


def write_bone_name(self, context):
    """Transfer a bone set in the bone selector collection to the metadata dictionary.
    Bones not defined are set as None.
    Args:
        self (BoneSelectorStringProperty): the property representing a bone in the armature.
        context (bpy.context): the current blender context.
    Notes:
        This function is not used currently.
    """
    validator_properties = context.window_manager.validator_properties
    index = standard_bone_names.index(self.name)
    bone_key = standard_bone_names[index]
    if self.bone_name == '':
        validator_properties.metadata['body']['bone_names'][bone_key] = None
    else:
        validator_properties.metadata['body']['bone_names'][bone_key] = self.bone_name


def write_bone_names(context):
    """Transfer all bones set in the bone selector collection to the metadata dictionary.
    Bones not defined are set as None.
    Args:
        context (bpy.context): the current blender context
    """
    validator_properties = context.window_manager.validator_properties
    bone_selector_collection = context.scene.bone_selector_collection
    for bone_selector in bone_selector_collection:
        if bone_selector.bone_name == '':
            validator_properties.metadata['body']['bone_names'][bone_selector.name] = None
        else:
            validator_properties.metadata['body']['bone_names'][bone_selector.name] = bone_selector.bone_name


def write_face_name(self, context):
    """Transfer a bone set in the bone selector collection to the metadata dictionary.
    Bones not defined are set as None.
    Args:
        self (BoneSelectorStringProperty): the property representing a bone in the armature.
        context (bpy.context): the current blender context.
    Notes:
        This function is not used currently.
    """
    if self.target_mesh == '':
        context.window_manager.validator_properties.metadata['face']['mesh_name'] = None
    else:
        context.window_manager.validator_properties.metadata['face']['mesh_name'] = self.target_mesh


def write_shapekey_names(target_mesh_name, metadata):
    """Dumps shape key names into metadata dictionary. Before doing this, it checks
    that at least a bone has a naming that is in the expected naming conventions.
    If no bone matching any template it won't edit the metadata.
    Expected bones in the naming convention not found will be saved as None.

    Args:
        target_mesh_name (str): The mesh with shapekeys
        metadata (dict): The dictionary holding the metadata
    """
    target_mesh = bpy.data.objects.get(target_mesh_name)

    if not target_mesh or target_mesh.type != 'MESH' or not target_mesh.data.shape_keys:
        for key in metadata['face']['blendshape_names'].keys():
            metadata['face']['blendshape_names'][key] = None
        metadata['eyes_rig'].clear()
        return

    shapekey_names = [key_block.name for key_block in target_mesh.data.shape_keys.key_blocks]
    shapekey_naming_convention = None

    for shapekey_convention, supported_shapekey_names in all_supported_shapekey_names.items():
        for shapekey_name in shapekey_names:
            # if shapekey_name.split(':')[-1] in supported_shapekey_names:
            if shapekey_name in supported_shapekey_names:
                shapekey_naming_convention = shapekey_convention
                break

    if not shapekey_naming_convention:
        return

    for i, supported_shapekey_name in enumerate(all_supported_shapekey_names[shapekey_naming_convention]):
        key = list(metadata['face']['blendshape_names'].keys())[i]
        metadata['face']['blendshape_names'][key] = None
        for shapekey_name in shapekey_names:
            # if shapekey_name.split(':')[-1] == supported_shapekey_name:
            if shapekey_name == supported_shapekey_name:
                metadata['face']['blendshape_names'][key] = shapekey_name
                continue


def check_duplicate_assigned_bones(bones_dict: dict):
    """Return duplicate values in a dictionary that are not None. Each values will
    appear only once in the duplicate list returned.
    Args:
        bones_dict (dict): the bones dictionary in the metadata
    Returns:
        list[str]: A list of all duplicated bones
    """
    seen = []
    duplicates = []

    for value in bones_dict.values():
        if value in seen and value not in duplicates and value is not None:
            duplicates.append(value)
        else:
            seen.append(value)

    return duplicates


def check_eye_bones(bones_dict: dict, eye_bones_dict: dict):
    """Returns the eye bones that are already used in other eye setups
    Args:
        bones_dict (dict): the eye setup dictionary to check
        eye_bones_dict (list[dict]): the list of other eye rigs
    Returns:
        list[str]: the list of conflicting bones (duplicated)
    """
    conflicts = []

    for eye_bone_dict in eye_bones_dict:
        if eye_bone_dict['bone_name'] in list(bones_dict.values()):
            conflicts.append(eye_bone_dict['bone_name'])

    return conflicts


def auto_assign_bone_names(self, context, target_arm_name: str):
    """Assign all bones found in the specified armature that matches the naming
    convention to bone selector. Naming convention is defined by what matches
    the Hip bone.
    Args:
        self (AutoAssignBones): the Operator for auto assigning bones.
        context (bpy.context): the current blender context.
    """
    armature = bpy.data.objects.get(target_arm_name)

    if not armature:
        self.report({'ERROR'}, f"Couldn't find armature with name {target_arm_name}!")
        return

    bone_names = [bone.name for bone in armature.pose.bones]
    bone_naming_convention = None

    for bone_convention, supported_bone_names in all_supported_bone_names.items():
        for bone_name in bone_names:
            if bone_name.split(':')[-1] == supported_bone_names[0]:
                bone_naming_convention = bone_convention
                bone_naming_label = bone_convention.split('_', maxsplit=1)[0].replace('-', ' ')
                self.report(
                    {'INFO'},
                    f"Auto assigning bones based on the {bone_naming_label} naming convention.",
                )
                break
        if bone_naming_convention:
            break

    if not bone_naming_convention:
        self.report({'ERROR'}, 'Bone naming convention not found! Please assign bones manually.')
        return

    for i, supported_bone_name in enumerate(all_supported_bone_names[bone_naming_convention]):
        context.scene.bone_selector_collection[i].bone_name = ''
        for bone_name in bone_names:
            if bone_name.split(':')[-1] == supported_bone_name:
                context.scene.bone_selector_collection[i].bone_name = bone_name


def blender_specific_messages(validation_messages):
    """Adds an extra message to the texture files check if it failed.
    Args:
        validation_messages (dict): The dictionary holding the validation messages.
    """
    if 'texture_files_check' in validation_messages.keys():
        validation_messages['texture_files_check']['message'] += text_static.TEXTURE_FILES_EXTEND_STR


def validate_character(self, context):  # pylint: disable=unused-argument
    """Runs all validators defined and keeps track of their messages on the validator
    properties. Based on the result of the validators, it will return the validation
    status.
    Args:
        context (ValidateCharacter): The operator calling this validation function.
    Returns:
        str: The validation status that can be either:
            'metadata': a problem with metadata.
            'cleanup': there are issues that can be cleaned up so the character is
                usable.
            'fail': the validation failed and the character can not be used in this state.
            'warning': the character can be used, but will not be feature full.
            'clean': the character is good to go.
    Notes:
        This function has the side effect of purging orphan data blocks and saving the file.
    """
    save_file()

    if bpy.context.view_layer.objects.active:
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    validator_properties = context.window_manager.validator_properties

    validator_properties.validation_metadata_message.clear()
    validator_properties.validation_cleanup_messages.clear()
    validator_properties.validation_fail_messages.clear()
    validator_properties.validation_warning_messages.clear()

    validator_metadata_object = ValidatorMetadata()
    validation_metadata_message = validator_metadata_object(
        validator_properties.metadata, addon_version_tuple_to_str(blender_addon_version)
    )
    for key, value in validation_metadata_message.items():
        validator_properties.validation_metadata_message[key] = value
    if any(not item['check'] for item in validation_metadata_message.values()):
        return 'metadata'

    validator_cleanup_object = ValidatorCleanup()
    validation_cleanup_messages = validator_cleanup_object(validator_properties.metadata)
    for key, value in validation_cleanup_messages.items():
        validator_properties.validation_cleanup_messages[key] = value
    if any(not item['check'] for item in validation_cleanup_messages.values()):
        validator_properties.cleanup_required = True
        return 'cleanup'

    validator_requirement_object = ValidatorRequirement()
    validation_fail_messages = validator_requirement_object(validator_properties.metadata, bpy.path.abspath('//'))
    for key, value in validation_fail_messages.items():
        validator_properties.validation_fail_messages[key] = value
    blender_specific_messages(validator_properties.validation_fail_messages)
    if any(not item['check'] for item in validation_fail_messages.values()):
        return 'fail'

    validator_warning_object = ValidatorWarning()
    validation_warning_messages = validator_warning_object(validator_properties.metadata)
    for key, value in validation_warning_messages.items():
        validator_properties.validation_warning_messages[key] = value
    if any(not item['check'] for item in validation_warning_messages.values()):
        return 'warning'

    return 'clean'


def cleanup_character(self, context):  # pylint: disable=unused-argument
    """Run all cleanup actions based on what the validation messages are stored in
    the validator properties. To have the messages there, make sure you called
    validate_character before this.
    Args:
        context (CleanupCharacter): The operator calling this function.
    Notes:
        This function has the side effect of purging orphan data blocks and saving the file.
    """
    file_path = Path(bpy.data.filepath)
    shutil.copyfile(file_path, file_path.parent/(file_path.stem+'_backup.blend'))

    if bpy.context.view_layer.objects.active:
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    validator_properties = context.window_manager.validator_properties

    validation_cleanup_messages = validator_properties.validation_cleanup_messages
    if validation_cleanup_messages.get('text_files_check'):
        ValidatorCleanupTextFiles.cleanup()
    if validation_cleanup_messages.get('armature_pose_position_check'):
        ValidatorCleanupArmaturePosePosition.cleanup(
            validator_properties.metadata['body']['armature_name'],
        )
    if validation_cleanup_messages.get('hips_bone_relations_check'):
        ValidatorCleanupHipsBoneRelations.cleanup(
            validator_properties.metadata['body']['armature_name'],
            validator_properties.metadata['body']['bone_names']['Hips'],
        )
    if validation_cleanup_messages.get('bone_rotation_mode_check'):
        ValidatorCleanupBoneRotationMode.cleanup(validator_properties.metadata['body']['armature_name'])
    if validation_cleanup_messages.get('transforms_check'):
        ValidatorCleanupTransforms.cleanup()
    if validation_cleanup_messages.get('auto_smooth_check'):
        ValidatorCleanupAutoSmooth.cleanup()
    if validation_cleanup_messages.get('syntax_check'):
        ValidatorCleanupObjectNaming.cleanup()
    if validation_cleanup_messages.get('curves_geo_nodes_check'):
        ValidatorCleanupCurvesGeoNodes.cleanup()

    save_file()


class ExportData():
    '''Export and prepare Blender data for upload to Wonder Studio.'''
    def __init__(self, metadata) -> None:
        file_path = Path(bpy.data.filepath)
        output_path = file_path.parent/EXPORT_FOLDER_NAME

        # Make paths absolut to avoid issues when copying files
        bpy.ops.file.make_paths_absolute()

        # Remove the export folder if it exists
        # if output_path.exists():
        #     self.change_permissions_recursive(target_path=output_path, mode=0o777)
        #     shutil.rmtree(output_path)

        # Create an output dir
        output_path.mkdir(parents=True, exist_ok=True)

        # Copy the character file
        shutil.copyfile(file_path, output_path/(file_path.stem+'_output.blend'))

        # Copy textures
        self.copy_texture_files(output_path)

        # Save Metadata
        with open(output_path/'metadata.json', 'w', encoding="utf-8") as outfile:
            json.dump(metadata, outfile, indent=4)

        # Set read, execture permissions to owner and group
        # self.change_permissions_recursive(target_path=output_path, mode=0o555)

    def copy_texture_files(self, output_path:Path):
        '''Copy all texture files in use to the output location.
        Args:
            output_path: Path
                Output location for all character files.
        '''
        # Create textures folder
        output_textures_path = output_path/'textures'
        output_textures_path.mkdir(parents=True, exist_ok=True)

        # Ignore images
        ignore_images = ['Render Result', 'Viewer Node']
        for node in bpy.context.scene.world.node_tree.nodes:
            if node.type == 'TEX_ENVIRONMENT' and node.image:
                ignore_images.append(node.image.name)

        # Get texture file paths
        texture_paths = list()
        for image in bpy.data.images:
            if not image.users or image.packed_file or image.name in ignore_images:
                continue
            if image.source == 'FILE':
                new_paths = self.get_flat_image_path(image)
            if image.source == 'TILED':
                new_paths = self.get_udim_tiles_paths(image)
            if image.source == 'SEQUENCE':
                new_paths = self.get_image_sequence_paths(image)
            # NOTE: Video files are not currently supported.
            # if image.source == 'MOVIE':
            #     new_paths = self.get_movie_path(image)

            if new_paths:
                texture_paths.extend(new_paths)

        # Copy texture files
        for texture_path in texture_paths:
            shutil.copyfile(texture_path, output_textures_path/texture_path.name)

    @classmethod
    def get_flat_image_path(cls, image) -> List[Path]:
        '''Get image file path for FILE type of image source.
        Args:
            image: bpy.types.Image
                Image object to return path or paths for.
        Returns:
            extracted_paths: List[Path]
                List of Path objects for the provided image object.
        '''
        extracted_paths = [Path(bpy.path.abspath(image.filepath))]
        return extracted_paths

    @classmethod
    def get_udim_tiles_paths(cls, image) -> List[Path]:
        '''Get image file path for TILED type of image source.
        Args:
            image: bpy.types.Image
                Image object to return path or paths for.
        Returns:
            extracted_paths: List[Path]
                List of Path objects for the provided image object.
        '''
        image_path = Path(bpy.path.abspath(image.filepath)).parent
        udim_texture_name = Path(image.filepath).name
        glob_search_pattern = udim_texture_name.replace('<UDIM>', '[0-9][0-9][0-9][0-9]')
        extracted_paths = glob(str(image_path/glob_search_pattern))
        extracted_paths = [Path(extracted_path) for extracted_path in extracted_paths]
        return extracted_paths

    @classmethod
    def get_image_sequence_paths(cls, image) -> List[Path]:
        '''Get image file path for SEQUENCE type of image source.
        Args:
            image: bpy.types.Image
                Image object to return path or paths for.
        Returns:
            extracted_paths: List[Path]
                List of Path objects for the provided image object.
        '''
        max_images = 200
        extracted_paths = []
        images_path = Path(bpy.path.abspath(image.filepath)).parent

        first_image_name = Path(image.filepath).name
        parts = re.split(r'(\d+)', first_image_name)
        prefix = parts[0]
        digits = int(parts[1])
        suffix = parts[2]
        width = len(parts[1])

        counter = 1
        while counter <= max_images:
            image_name = f'{prefix}{digits:0{width}}{suffix}'
            image_path = images_path/image_name
            if not image_path.is_file():
                break
            extracted_paths.append(image_path)
            digits += 1
            counter += 1

        return extracted_paths

    @classmethod
    def get_movie_path(cls, image) -> Path:
        '''Get image file path for MOVIE type of image source.
        Args:
            image: bpy.types.Image
                Image object to return path or paths for.
        Returns:
            extracted_paths: List[Path]
                List of Path objects for the provided image object.
        Notes:
            Video files are not currently supported.
        '''
        extracted_paths = [Path(bpy.path.abspath(image.filepath))]
        return extracted_paths

    @classmethod
    def change_permissions_recursive(cls, target_path: Path, mode: int = 0o777) -> None:
        '''Change permissions recursively for all files and subfolders in the directory.
        Args:
            target_path: Path
                Blender file path.
            mode: int
                Chmod value for permissions.
        Note:
            Not in use for now.
        '''
        for path in target_path.glob('**/*'):
            path.chmod(mode)
