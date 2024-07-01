# Copyright 2023 Wonder Dynamics

# This source code is licensed under the GNU GPLv3
# found in the LICENSE file in the root directory of this source tree.

"""Module for all the validator classes."""

import bpy

from .validator import Validator

# The way Validator is inherited by child classes currently do change check signature
# This is something to refactor in the future, but it would take time. TODO:
# pylint: disable=arguments-renamed,arguments-differ


class ValidatorWarning:
    """Class that looks for potential defects that could affect the quality of the results.
    All work is is done by delegating the work to classes like
    ValidatorWarningMissingBones, ValidatorWarningMissingIKChains,
    ValidatorWarningDisabledInRenders, ValidatorWarningMissingBlendshapes,
    ValidatorWarningMissingEyeControls and ValidatorWarningMutedBlendshapes,.

    Note: classes used by this validator are prefixed with ValidatorWarning_.
    """

    def __call__(self, metadata: dict, toggle_usd: bool) -> dict:
        report_dict = {}

        missing_bones_object = ValidatorWarningMissingBones(metadata)
        report_dict[missing_bones_object.key] = missing_bones_object()

        missing_ik_chains_object = ValidatorWarningMissingIKChains(metadata)
        report_dict[missing_ik_chains_object.key] = missing_ik_chains_object()

        disabled_in_renders_object = ValidatorWarningDisabledInRenders()
        report_dict[disabled_in_renders_object.key] = disabled_in_renders_object()

        if metadata['face']['mesh_name']:
            missing_blendshapes_object = ValidatorWarningMissingBlendshapes(metadata)
            report_dict[missing_blendshapes_object.key] = missing_blendshapes_object()

            missing_eye_controls_object = ValidatorWarningMissingEyeControls(metadata)
            report_dict[missing_eye_controls_object.key] = missing_eye_controls_object()

            muted_blendshapes_object = ValidatorWarningMutedBlendshapes(metadata)
            report_dict[muted_blendshapes_object.key] = muted_blendshapes_object()
        
        if toggle_usd:
            usd_shader_nodes_object = ValidatorUSDShaderNodes()
            report_dict[usd_shader_nodes_object.key] = usd_shader_nodes_object()

            usd_modifiers_object = ValidatorWarningUSDModifiers()
            report_dict[usd_modifiers_object.key] = usd_modifiers_object()

        return report_dict


class ValidatorWarningMissingBones(Validator):
    """Warns if any of the expected bones in the skeleton is not assigned."""

    def __init__(self, metadata: dict) -> None:
        super().__init__()
        self.message = (
            'Pose bones missing! Missing bones may negatively impact animation quality.'
            ' Please make sure missing bones are left out intentionally.'
        )
        self.key = 'missing_bones_check'

        self.metadata = metadata

    def get(self) -> list:
        missing_bones = [key for key, item in self.metadata['body']['bone_names'].items() if not item]
        return missing_bones

    def check(self, missing_bones: list) -> bool:
        if missing_bones:
            self.expand_message(f'Missing bones: {", ".join(missing_bones)}')
            return False
        return True


class ValidatorWarningMissingIKChains(Validator):
    """Warns if ik chains for limbs cannot be established.
    Notes:
        This validator will change the scene since it establishes the parent attirbutes for
            child bone.
    """

    def __init__(self, metadata: dict) -> None:
        super().__init__()
        self.message = (
            'Unable to establish all IK bone chains! IK features, in Live Action Advanced'
            ' projects, may not be applied for some limbs.'
        )
        self.key = 'missing_ik_chains_check'

        self.metadata = metadata

    def get(self) -> list:
        missing_ik_pairs = list()
        ik_pairs = [
            ['LeftArm', 'LeftHand'],
            ['RightArm', 'RightHand'],
            ['LeftUpLeg', 'LeftFoot'],
            ['RightUpLeg', 'RightFoot'],
        ]
        for ik_pair in ik_pairs:
            if (
                not self.metadata['body']['bone_names'][ik_pair[0]]
                or not self.metadata['body']['bone_names'][ik_pair[1]]
            ):
                missing_ik_pairs.append(f'{ik_pair[0]} <- {ik_pair[1]}')
                continue

            ik_chain_exists = self.check_ik_chain(
                self.metadata['body']['armature_name'],
                self.metadata['body']['bone_names'][ik_pair[0]],
                self.metadata['body']['bone_names'][ik_pair[1]],
            )

            if not ik_chain_exists:
                missing_ik_pairs.append(f'{ik_pair[0]} <- {ik_pair[1]}')

        return missing_ik_pairs

    def check(self, missing_ik_pairs: list) -> bool:
        if missing_ik_pairs:
            self.expand_message(f'Missing IK chains: {", ".join(missing_ik_pairs)}')
            return False
        return True

    @staticmethod
    def check_ik_chain(armature_name: str, root_bone_name: str, target_bone_name: str) -> bool:
        """Returns whether or not your can navigate the hierarchy up from the target bone
        up to the root bone.
        Args:
            armature_name (str): the name of the armature related to the bones.
            root_bone_name (str): the root (parent) bone fo the chain to tests.
            target_bone_name (str): the target (child) bone fo the chain to tests.
        Returns:
            bool: wheter or not target boneis a child (there might be intermediate bones) of root bone.
        """
        armature = bpy.data.objects.get(armature_name)
        root_bone = armature.pose.bones.get(root_bone_name)
        target_bone = armature.pose.bones.get(target_bone_name)

        while target_bone.parent:
            if target_bone.parent == root_bone:
                return True
            target_bone = target_bone.parent

        return False


class ValidatorWarningDisabledInRenders(Validator):
    """Warns if there are objects or collections that are disabled for rendering."""

    def __init__(self) -> None:
        super().__init__()
        self.message = (
            'Disabled objects in the render! Objects or collections are disabled in the renderer!'
            'This may result in parts of your character not being rendered.'
        )
        self.key = 'disabled_in_renders_check'

    def get(self) -> dict:
        view_layer = bpy.context.view_layer.objects.values()

        disabled_in_renders = {
            'collections': [],
            'objects': [],
        }
        disabled_in_renders['collections'] = [
            collection.name for collection in bpy.data.collections if collection.hide_render
        ]
        disabled_in_renders['objects'] = [obj.name for obj in bpy.data.objects if obj.hide_render and obj in view_layer]
        return disabled_in_renders

    def check(self, disabled_in_renders: dict) -> bool:
        if disabled_in_renders['collections'] or disabled_in_renders['objects']:
            if disabled_in_renders['collections']:
                self.expand_message(f'Disabled Collections: {", ".join(disabled_in_renders["collections"])}')
            if disabled_in_renders['objects']:
                self.expand_message(f'Disabled Objects: {", ".join(disabled_in_renders["objects"])}')
            return False
        else:
            return True


class ValidatorWarningMissingBlendshapes(Validator):
    """Warns if in the face mesh there are any blendshape missing (of all possible in the face)."""

    def __init__(self, metadata: dict) -> None:
        super().__init__()
        self.message = (
            'Some face blendshapes missing! Missing blendshapes may negatively impact facial animation'
            ' quality. Please make sure missing blendshapes are left out intentionally.'
        )
        self.key = 'missing_blendshapes_check'

        self.metadata = metadata

    def get(self) -> list:
        missing_blendshapes = [key for key, item in self.metadata['face']['blendshape_names'].items() if not item]
        return missing_blendshapes

    def check(self, missing_blendshapes: list) -> bool:
        if missing_blendshapes:
            self.expand_message(f'Missing blendshapes: {", ".join(missing_blendshapes)}')
            return False
        else:
            return True


class ValidatorWarningMissingEyeControls(Validator):
    """Warns if there are eye rigs but the gaze blendshapes are not defined."""

    def __init__(self, metadata: dict) -> None:
        super().__init__()
        self.message = (
            'Eye control blendshapes missing! Missing face blendshapes for eye control, but eye bones are assigned!'
            'As a result, the gaze may not function correctly.'
        )
        self.key = 'missing_eye_controls_check'

        self.metadata = metadata
        self.gaze_blendshapes = ['eyeDn', 'eyeL', 'eyeR', 'eyeUp']

    def get(self) -> list:
        missing_gaze_blendshapes = []
        for gaze_blendshape in self.gaze_blendshapes:
            if not self.metadata['face']['blendshape_names'][gaze_blendshape]:
                missing_gaze_blendshapes.append(gaze_blendshape)
        return missing_gaze_blendshapes

    def check(self, missing_gaze_blendshapes: list) -> bool:
        if missing_gaze_blendshapes and self.metadata['eyes_rig']:
            self.expand_message(f'Missing gaze blendshapes: {", ".join(missing_gaze_blendshapes)}')
            return False
        else:
            return True


class ValidatorWarningMutedBlendshapes(Validator):
    """Warns if any of the blendshapes are muted."""

    def __init__(self, metadata: dict) -> None:
        super().__init__()
        self.message = (
            'Muted blendshapes detected! Muted blendshapes will receive animation'
            ' data but will not display the animation.'
        )
        self.key = 'muted_blendshapes_check'

        self.metadata = metadata

    def get(self) -> list:
        muted_blendshapes = []
        mesh_object = bpy.data.objects.get(self.metadata['face']['mesh_name'])

        for key, item in self.metadata['face']['blendshape_names'].items():
            if not item:
                continue
            if mesh_object.data.shape_keys.key_blocks[item].mute:
                muted_blendshapes.append(key)

        return muted_blendshapes

    def check(self, muted_blendshapes: list) -> bool:
        if muted_blendshapes:
            self.expand_message(f'Muted blendshapes: {", ".join(muted_blendshapes)}')
            return False
        else:
            return True


class ValidatorUSDShaderNodes(Validator):
    """Validates that only USD supported shader nodes are used.
    """

    def __init__(self) -> None:
        super().__init__()
        self.message = 'USD incompatible shader nodes detected!'
        self.key = 'usd_shader_nodes_check'

    def get(self) -> list:
        materials = bpy.data.materials
        whitelisted_nodes = [
            'BSDF_PRINCIPLED',
            'TEX_IMAGE',
            'NORMAL_MAP',
            'MAPPING',
            'BSDF_HAIR_PRINCIPLED',
            'OUTPUT_MATERIAL',
            'REROUTE',
            'TEX_COORD',
        ]
        material_status = []

        for material in materials:
            if material.use_nodes:
                nodes = material.node_tree.nodes
                unsupported_nodes = [node.name for node in nodes if node.type not in whitelisted_nodes]

                principled_shaders = [node for node in nodes if node.type == 'BSDF_PRINCIPLED']
                shader = []
                for principled_shader in principled_shaders:
                    translucency = principled_shader.inputs[17].default_value
                    if translucency > 0.0:
                        shader.append(principled_shader)

                material_dict = {
                    'material_name': material.name,
                    'unsupported_nodes': unsupported_nodes,
                    'translucency': None
                    if not shader
                    else f'Translucency set on {len(shader)} BSDF shaders. Replace with alpha opacity.',
                }

                material_status.append(material_dict)

        return material_status

    def check(self, material_status: list) -> bool:
        bad_materials = []
        for mat_status in material_status:
            if mat_status['unsupported_nodes'] or mat_status['translucency']:
                bad_materials.append(mat_status['material_name'])
        
        if bad_materials:
            self.expand_message(f'Check materials: {", ".join(bad_materials)}')
            return False
        return True


class ValidatorWarningUSDModifiers(Validator):
    """Validates that only Armature modifier is present in geometry."""

    def __init__(self) -> None:
        super().__init__()
        self.message = 'Unsuported modifiers detected! USD has support for only one armature modifier per mesh object.'
        self.key = 'usd_modifiers_check'

    def get(self) -> list:
        modifiers_status = []

        mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
        for obj in mesh_objects:
            modifiers = [modifier.name for modifier in obj.modifiers if modifier.type != 'ARMATURE']
            modifiers_dict = {'object_name': obj.name, 'breaking_modifiers': modifiers}
            modifiers_status.append(modifiers_dict)
        
        return modifiers_status

    def check(self, modifiers_status: list) -> bool:
        bad_mesh_objects = []
        for mod_status in modifiers_status:
            if mod_status['breaking_modifiers']:
                bad_mesh_objects.append(mod_status['object_name'])
        
        if bad_mesh_objects:
            self.expand_message(f'Check objects: {", ".join(bad_mesh_objects)}')
            return False
        return True
