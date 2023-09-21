# Copyright 2023 Wonder Dynamics

# This source code is licensed under the GNU GPLv3
# found in the LICENSE file in the root directory of this source tree.

"""Module for all the Requirement validator classes."""

import os
import re

import bmesh
import bpy

from .validator import Validator

# The way Validator is inherited by child classes currently do change check signature
# This is something to refactor in the future, but it would take time. TODO:
# pylint: disable=arguments-renamed,arguments-differ


class ValidatorRequirement:
    """Class that validates that the requirements are filled. All the validation work is done by
    delegating the work to classes like ValidatorRequirementMainPoseArmatureName, ValidatorRequirementOneBodyArmature,
    ValidatorRequirementHipsBone, ValidatorRequirementPolyCount,
    ValidatorRequirementParticleCount, ValidatorRequirementTextureFilesExist,
    ValidatorRequirementMainFaceMeshName, ValidatorRequirementBlendshapes and
    ValidatorRequirementOneFaceMesh.

    Note: classes used by this validator are prefixed with ValidatorRequirement_.
    """

    def __call__(self, metadata: dict, textures_path: str) -> dict:
        report_dict = {}

        main_pose_armature_name_object = ValidatorRequirementMainPoseArmatureName(metadata)
        report_dict[main_pose_armature_name_object.key] = main_pose_armature_name_object()

        one_body_armature_object = ValidatorRequirementOneBodyArmature()
        report_dict[one_body_armature_object.key] = one_body_armature_object()

        hips_bone_object = ValidatorRequirementHipsBone(metadata)
        report_dict[hips_bone_object.key] = hips_bone_object()

        poly_count_object = ValidatorRequirementPolyCount()
        report_dict[poly_count_object.key] = poly_count_object()

        hairstrand_count_object = ValidatorRequirementHairStrandCount()
        report_dict[hairstrand_count_object.key] = hairstrand_count_object()

        texture_files_exist_object = ValidatorRequirementTextureFilesExist(textures_path)
        report_dict[texture_files_exist_object.key] = texture_files_exist_object()

        if metadata['face']['mesh_name']:
            main_face_mesh_name_object = ValidatorRequirementMainFaceMeshName(metadata)
            report_dict[main_face_mesh_name_object.key] = main_face_mesh_name_object()

            blendshapes_object = ValidatorRequirementBlendshapes(metadata)
            report_dict[blendshapes_object.key] = blendshapes_object()

            one_face_mesh_object = ValidatorRequirementOneFaceMesh()
            report_dict[one_face_mesh_object.key] = one_face_mesh_object()

        return report_dict


class ValidatorRequirementMainPoseArmatureName(Validator):
    """Validates that the main armature ends with the _BODY suffix."""

    def __init__(self, metadata: dict) -> None:
        super().__init__()
        self.message = 'Wrong skeleton/armature name! The main skeleton/armature name does not end with the tag "BODY"!'
        self.key = 'armature_name_check'
        self.tag = 'BODY'

        self.metadata = metadata

    def get(self) -> str:
        armature_name = self.metadata['body']['armature_name']
        return armature_name

    def check(self, armature_name: str) -> bool:
        return armature_name.endswith(self.tag)


class ValidatorRequirementOneBodyArmature(Validator):
    """Validates that only one armature ends with the _BODY suffix."""

    def __init__(self) -> None:
        super().__init__()
        self.message = 'Multiple main skeleton/armature! More than one skeleton/armature with the tag "BODY" detected!'
        self.key = 'one_body_armature_check'
        self.tag = 'BODY'

    def get(self) -> list:
        armature_object_names = [
            obj.name for obj in bpy.data.objects if obj.type == 'ARMATURE' and obj.name.endswith(self.tag)
        ]
        return armature_object_names

    def check(self, data: list) -> bool:
        if len(data) > 1:
            return False
        else:
            return True


class ValidatorRequirementHipsBone(Validator):
    """Validates that Hip bone is defined in metadata."""

    def __init__(self, metadata: dict) -> None:
        super().__init__()
        self.message = 'Hips bone not found!'
        self.key = 'hips_bone_check'

        self.metadata = metadata

    def get(self) -> str:
        hips_bone_name = self.metadata['body']['bone_names']['Hips']
        return hips_bone_name

    def check(self, hips_bone_name: str) -> bool:
        if hips_bone_name:
            return True
        else:
            return False


class ValidatorRequirementPolyCount(Validator):
    """Validates that the sum of all meshes polygons are below the polygon limit."""

    def __init__(self) -> None:
        super().__init__()
        self.poly_count_limit = 1500000

        self.message = (
            f'Poly count limit exceeded! Poly count exceeds the allowed amount of {self.poly_count_limit} polygons per'
            ' character! Note that subdivision counts towards your poly count.'
        )
        self.key = 'poly_count_check'

    def get(self) -> int:
        poly_count_sum = 0

        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                if obj in bpy.context.scene.view_layers[0].objects.values():
                    this_bmesh = bmesh.new()
                    this_bmesh.from_object(obj, bpy.context.evaluated_depsgraph_get())
                    poly_count_sum += len(this_bmesh.faces)

        return poly_count_sum

    def check(self, poly_count_sum: int) -> bool:
        if poly_count_sum > self.poly_count_limit:
            return False
        else:
            return True


class ValidatorRequirementHairStrandCount(Validator):
    """Validates that the sum of all particles (and particle children) are below the particle limit."""

    def __init__(self) -> None:
        super().__init__()
        self.particle_count_limit = 100000

        self.message = (
            f'Hair strand limit exceeded! Hair strand count exceeds the allowed amount of {self.particle_count_limit} hair strands per character!'
        )
        self.key = 'particle_count_check'

    def get(self) -> int:
        particle_count_sum = 0
        for obj in bpy.data.objects:
            for modifier in obj.modifiers:
                if modifier.type == 'PARTICLE_SYSTEM':
                    particle_count = modifier.particle_system.settings.count
                    if (
                        modifier.particle_system.settings.child_type != 'NONE'
                        and modifier.particle_system.settings.rendered_child_count > 0
                    ):
                        particle_count = particle_count * modifier.particle_system.settings.rendered_child_count
                    particle_count_sum += particle_count
                if obj.type == 'CURVES' and modifier.type == 'NODES':
                    particle_count_sum += len(obj.data.curves)
        return particle_count_sum

    def check(self, particle_count_sum: int) -> bool:
        if particle_count_sum > self.particle_count_limit:
            return False
        else:
            return True


class ValidatorRequirementTextureFilesExist(Validator):
    """Validates that the all the textures in the allowed formats can be found. UDIM textures are also supported."""

    def __init__(self, textures_path: str) -> None:
        super().__init__()
        self.allowed_formats = ['jpg', 'jpeg', 'png', 'tif', 'tiff', 'exr']
        self.message = (
            'Missing or unsupported texture files detected! Please provide all texture files used'
            ' by the character in one of the supported file formats. Supported file '
            f'formats: {", ".join(self.allowed_formats)}'
        )
        self.key = 'texture_files_check'

        self.textures_path = textures_path

    def get(self) -> list:
        texture_paths = list()
        missing_textures = list()

        for dirpath, _, file_names in os.walk(self.textures_path):
            texture_paths += [
                os.path.join(dirpath, file_name)
                for file_name in file_names
                if file_name.split('.')[-1] in self.allowed_formats
            ]

        texture_names = [os.path.basename(texture_path) for texture_path in texture_paths]
        texture_names_udim = [re.sub(r'_(\d{4})_', '_<UDIM>_', texture_name) for texture_name in texture_names]
        ignore_images = ['Render Result', 'Viewer Node']

        if bpy.context.scene.world:
            for node in bpy.context.scene.world.node_tree.nodes:
                if node.type == 'TEX_ENVIRONMENT' and node.image:
                    ignore_images.append(node.image.name)

        for image in bpy.data.images:
            texture_name = os.path.basename(image.filepath.replace('\\', '//'))

            if not image.users or image.packed_file or image.name in ignore_images:
                continue

            if texture_name not in texture_names_udim and texture_name not in texture_names:
                missing_textures.append(texture_name)

        return missing_textures

    def check(self, missing_textures: list) -> bool:
        if missing_textures:
            self.expand_message(f'Missing or unsupported texture files: {", ".join(missing_textures)}')
            return False
        else:
            return True


class ValidatorRequirementMainFaceMeshName(Validator):
    """Validates that the main face mesh defined in the metadata ends with the _FACE suffix."""

    def __init__(self, metadata: dict) -> None:
        super().__init__()
        self.message = 'Wrong face mesh name! Main face mesh name does not end with the tag "FACE"!'
        self.key = 'face_name_check'
        self.tag = 'FACE'

        self.metadata = metadata

    def get(self) -> str:
        armature_name = self.metadata['face']['mesh_name']
        return armature_name

    def check(self, armature_name: str) -> bool:
        return armature_name.endswith(self.tag)


class ValidatorRequirementBlendshapes(Validator):
    """Validates that the main face mesh has blendshapes. Blendshape names are not checked and the list
    returned from validator is coming form the metadata not the scene.
    """

    def __init__(self, metadata: dict) -> None:
        super().__init__()
        self.message = 'No valid blendshapes! There are no blendshapes to apply animation data to.'
        self.key = 'blendshapes_check'

        self.metadata = metadata

    def get(self) -> list:
        blendshapes = []
        mesh_obj = bpy.data.objects.get(self.metadata['face']['mesh_name'])
        if not mesh_obj.data.shape_keys:
            return blendshapes
        blendshapes = [value for value in list(self.metadata['face']['blendshape_names'].values())[1:] if value]
        return blendshapes

    def check(self, blendshapes: list) -> bool:
        print(blendshapes)
        if blendshapes:
            return True
        else:
            self.expand_message(
                f'Please check that {self.metadata["face"]["mesh_name"]} mesh has correctly named blendshapes.',
            )
            return False


class ValidatorRequirementOneFaceMesh(Validator):
    """Validates that only one mesh ends with the _FACE suffix."""

    def __init__(self) -> None:
        super().__init__()
        self.message = 'Multiple main face meshes! More than one mesh with the tag "FACE" detected!'
        self.key = 'one_face_mesh_check'
        self.tag = 'FACE'

    def get(self) -> list:
        armature_object_names = [
            obj.name for obj in bpy.data.objects if obj.type == 'MESH' and obj.name.endswith(self.tag)
        ]
        return armature_object_names

    def check(self, armature_object_names: list) -> bool:
        if len(armature_object_names) > 1:
            return False
        else:
            return True
