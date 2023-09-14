# Copyright 2023 Wonder Dynamics

# This source code is licensed under the GNU GPLv3
# found in the LICENSE file in the root directory of this source tree.

"""Module that defines all the types for checking the metadata."""

from dataclasses import dataclass
from re import match
from typing import List
from typing import Optional
from typing import Union

from .type_validator import TypeValidator

# attribute names in data validator internal properties
# are not pylint compliant. Changing this might take a while and
# not sure if it is worth the time. TODO:
# pylint: disable=invalid-name


@dataclass
class MetadataMaterialSurface(TypeValidator):
    """Class to validate by type (and some values) at initialization time a Material Surface definition."""

    material_name: str
    material_type: str  # can be: surface, flat, hair
    mesh_names: List[str]
    render_engine: str  # can be: arnold
    diffuseWeight_value: Optional[float]
    diffuseWeight_texture: Optional[str]
    diffuse_value: Optional[List[float]]  # 3 floats
    diffuse_texture: Optional[str]
    metalness_value: Optional[float]
    metalness_texture: Optional[str]
    specularWeight_value: Optional[float]
    specularWeight_texture: Optional[str]
    specular_value: Optional[List[float]]  # 3 floats
    specular_texture: Optional[str]
    roughness_value: Optional[float]
    roughness_texture: Optional[str]
    anisotropic_value: Optional[float]
    anisotropic_texture: Optional[str]
    anisotropicRotation_value: Optional[float]
    anisotropicRotation_texture: Optional[str]
    transmissionWeight_value: Optional[float]
    transmissionWeight_texture: Optional[str]
    transmission_value: Optional[List[float]]  # 3 floats
    transmission_texture: Optional[str]
    ior_value: Optional[float]
    ior_texture: Optional[str]
    sssWeight_value: Optional[float]
    sssWeight_texture: Optional[str]
    sss_value: Optional[List[float]]  # 3 floats
    sss_texture: Optional[str]
    sssRadius_value: Optional[List[float]]  # 3 floats
    sssRadius_texture: Optional[str]
    coatWeight_value: Optional[float]
    coatWeight_texture: Optional[str]
    coat_value: Optional[List[float]]  # 3 floats
    coat_texture: Optional[str]
    emissionWeight_value: Optional[float]
    emissionWeight_texture: Optional[str]
    emission_value: Optional[List[float]]  # 3 floats
    emission_texture: Optional[str]
    opacity_value: Optional[List[float]]  # 3 floats
    opacity_texture: Optional[str]
    bump_type: Optional[str]  # can be: bump, normal_tangent_space, normal_object_space
    bump_flip: bool
    bump_texture: Optional[str]
    bumpWeight_value: Optional[float]

    def __post_init__(self):
        """Enforces some additional constraints that cannot be defined by type alone,
        and some values that need to be one of a list of valid options.
        material type needs to be 'surface', 'flat' or 'hair'.
        render_engine needs to be 'arnold'.
        bump_type needs to be 'bump', 'normal_tangent_space' or 'normal_object_space'.
        and color values need to be a list of 3 values.
        """
        super().__post_init__()

        supported_material_types = ['surface', 'flat', 'hair']
        if self.material_type not in supported_material_types:
            raise ValueError(
                f'Unsupported material type. Currently supported material types: {supported_material_types}'
            )

        supported_render_engines = ['arnold']
        if self.render_engine not in supported_render_engines:
            raise ValueError(
                f'Unsupported render engine. Currently supported render engines: {supported_render_engines}'
            )

        vector_3_values = [
            'diffuse_value',
            'specular_value',
            'transmission_value',
            'sss_value',
            'sssRadius_value',
            'coat_value',
            'emission_value',
            'opacity_value',
        ]

        for atr_name in vector_3_values:
            val = getattr(self, atr_name)
            if isinstance(val, list) and len(val) != 3:
                raise ValueError(f'Wrong {atr_name} format. Expected list of 3 float values.')

        supported_bump_types = ['bump', 'normal_tangent_space', 'normal_object_space']
        if self.bump_type is not None and self.bump_type not in supported_bump_types:
            raise ValueError(f'Unsupported bump map type. Currently supported bump map types: {supported_bump_types}')


@dataclass
class MetadataMaterialFlat(TypeValidator):
    """Class to validate by type (and some values) at initialization time a Material Flat definition."""

    material_name: str
    material_type: str  # can be: surface, flat, hair
    mesh_names: List[str]
    render_engine: str  # can be: arnold
    emission_value: Optional[List[float]]  # 3 floats
    emission_texture: Optional[str]

    def __post_init__(self):
        """Enforces some additional constraints that cannot be defined by type alone,
        and some values that need to be one of a list of valid options.
        material type needs to be 'surface', 'flat' or 'hair'.
        render_engine needs to be 'arnold'.
        """
        super().__post_init__()

        supported_material_types = ['surface', 'flat', 'hair']
        if self.material_type not in supported_material_types:
            raise ValueError(
                f'Unsupported material type. Currently supported material types: {supported_material_types}'
            )

        supported_render_engines = ['arnold']
        if self.render_engine not in supported_render_engines:
            raise ValueError(
                f'Unsupported render engine. Currently supported render engines: {supported_render_engines}'
            )

        if isinstance(self.emission_value, list) and len(self.emission_value) != 3:
            raise ValueError('Wrong emission_value format. Expected list of 3 float values.')


@dataclass
class MetadataMaterialHair(TypeValidator):
    """Class to validate by type (and some values) at initialization time a Material Hair definition."""

    material_name: str
    material_type: str  # can be: surface, flat, hair
    groom_names: List[str]
    render_engine: str  # can be: arnold
    diffuse_value: Optional[List[float]]  # 3 floats
    diffuse_texture: Optional[str]
    melanin_value: Optional[float]
    melanin_texture: Optional[str]
    melaninRedness_value: Optional[float]
    melaninRedness_texture: Optional[str]
    melaninRandomize_value: Optional[float]
    melaninRandomize_texture: Optional[str]
    roughness_value: Optional[float]
    roughness_texture: Optional[str]
    ior_value: Optional[float]
    ior_texture: Optional[str]

    def __post_init__(self):
        """Enforces some additional constraints that cannot be defined by type alone,
        and some values that need to be one of a list of valid options.
        material type needs to be 'surface', 'flat' or 'hair'.
        render_engine needs to be 'arnold'.
        diffuse_value needs to be a 3 values list.
        """
        super().__post_init__()

        supported_material_types = ['surface', 'flat', 'hair']
        if self.material_type not in supported_material_types:
            raise ValueError(
                f'Unsupported material type. Currently supported material types: {supported_material_types}'
            )

        supported_render_engines = ['arnold']
        if self.render_engine not in supported_render_engines:
            raise ValueError(
                f'Unsupported render engine. Currently supported render engines: {supported_render_engines}'
            )

        if isinstance(self.diffuse_value, list) and len(self.diffuse_value) != 3:
            raise ValueError('Wrong diffuse_value format. Expected list of 3 float values.')


@dataclass
class MetadataEyeRig(TypeValidator):
    """Class to validate by type (and some values) at initialization time an Eye Rig definition."""

    bone_name: str
    horizontal_rotation_axis: str  # can be: X, Y, Z
    vertical_rotation_axis: str  # can be: X, Y, Z
    horizontal_min_max_value: List[float]  # 2 floats
    vertical_min_max_value: List[float]  # 2 floats

    def __post_init__(self):
        """Enforces some additional constraints that cannot be defined by type alone,
        and some values that need to be one of a list of valid options.
        horizontal_rotation_axis and vertical_rotation_axis needs to be 'X', 'Y', 'Z',
        horizontal_min_max_value and vertical_min_max_value need to have length of 2.
        """
        super().__post_init__()

        supported_axis = ['X', 'Y', 'Z']
        if self.horizontal_rotation_axis not in supported_axis:
            raise ValueError(
                f'Unsupported horizontal_rotation_axis type. Currently supported axis types: {supported_axis}'
            )

        if self.vertical_rotation_axis not in supported_axis:
            raise ValueError(
                f'Unsupported vertical_rotation_axis type. Currently supported axis types: {supported_axis}'
            )

        if len(self.horizontal_min_max_value) != 2:
            raise ValueError('Wrong horizontal_min_max_value format. Expected list of 2 float values.')

        if len(self.vertical_min_max_value) != 2:
            raise ValueError('Wrong vertical_min_max_value format. Expected list of 2 float values.')


@dataclass
class MetadataBodyBones(TypeValidator):
    """Class to validate by type (and some values) at initialization time a Body Bones definition.
    Hips need to be defined as a str, all other bones can be a str or None.
    """

    Hips: str
    LeftUpLeg: Optional[str]
    RightUpLeg: Optional[str]
    Spine: Optional[str]
    LeftLeg: Optional[str]
    RightLeg: Optional[str]
    Spine1: Optional[str]
    LeftFoot: Optional[str]
    RightFoot: Optional[str]
    Spine2: Optional[str]
    LeftToeBase: Optional[str]
    RightToeBase: Optional[str]
    Neck: Optional[str]
    LeftShoulder: Optional[str]
    RightShoulder: Optional[str]
    Head: Optional[str]
    LeftArm: Optional[str]
    RightArm: Optional[str]
    LeftForeArm: Optional[str]
    RightForeArm: Optional[str]
    LeftHand: Optional[str]
    RightHand: Optional[str]
    LeftHandIndex1: Optional[str]
    LeftHandIndex2: Optional[str]
    LeftHandIndex3: Optional[str]
    LeftHandMiddle1: Optional[str]
    LeftHandMiddle2: Optional[str]
    LeftHandMiddle3: Optional[str]
    LeftHandPinky1: Optional[str]
    LeftHandPinky2: Optional[str]
    LeftHandPinky3: Optional[str]
    LeftHandRing1: Optional[str]
    LeftHandRing2: Optional[str]
    LeftHandRing3: Optional[str]
    LeftHandThumb1: Optional[str]
    LeftHandThumb2: Optional[str]
    LeftHandThumb3: Optional[str]
    RightHandIndex1: Optional[str]
    RightHandIndex2: Optional[str]
    RightHandIndex3: Optional[str]
    RightHandMiddle1: Optional[str]
    RightHandMiddle2: Optional[str]
    RightHandMiddle3: Optional[str]
    RightHandPinky1: Optional[str]
    RightHandPinky2: Optional[str]
    RightHandPinky3: Optional[str]
    RightHandRing1: Optional[str]
    RightHandRing2: Optional[str]
    RightHandRing3: Optional[str]
    RightHandThumb1: Optional[str]
    RightHandThumb2: Optional[str]
    RightHandThumb3: Optional[str]


@dataclass
class MetadataBody(TypeValidator):
    """Class to validate by type (and some values) at initialization time a Body Metadata definition.
    armature name needs to be a str and bone names need to satisfy MetadataBodyBones
    type.
    """

    armature_name: str
    bone_names: MetadataBodyBones


@dataclass
class MetadataFaceBlendshapes(TypeValidator):
    """Class to validate by type (and some values) at initialization time a Blend shape definition."""

    Basis: Optional[str]
    browInnerDnL: Optional[str]
    browInnerDnR: Optional[str]
    browInnerUpL: Optional[str]
    browInnerUpR: Optional[str]
    browOuterDnL: Optional[str]
    browOuterDnR: Optional[str]
    browOuterUpL: Optional[str]
    browOuterUpR: Optional[str]
    browSqueezeL: Optional[str]
    browSqueezeR: Optional[str]
    cheekBlowL: Optional[str]
    cheekBlowR: Optional[str]
    cheekUpL: Optional[str]
    cheekUpR: Optional[str]
    eyeBlinkL: Optional[str]
    eyeBlinkR: Optional[str]
    eyeCompressL: Optional[str]
    eyeCompressR: Optional[str]
    eyeDn: Optional[str]
    eyeL: Optional[str]
    eyeR: Optional[str]
    eyeSquintL: Optional[str]
    eyeSquintR: Optional[str]
    eyeUp: Optional[str]
    eyeWidenLowerL: Optional[str]
    eyeWidenLowerR: Optional[str]
    eyeWidenUpperL: Optional[str]
    eyeWidenUpperR: Optional[str]
    jawClenchL: Optional[str]
    jawClenchR: Optional[str]
    jawIn: Optional[str]
    jawL: Optional[str]
    jawOpen: Optional[str]
    jawOut: Optional[str]
    jawR: Optional[str]
    lipChinRaiserL: Optional[str]
    lipChinRaiserR: Optional[str]
    lipCloseLower: Optional[str]
    lipCloseUpper: Optional[str]
    lipCornerDnL: Optional[str]
    lipCornerDnR: Optional[str]
    lipCornerUpL: Optional[str]
    lipCornerUpR: Optional[str]
    lipDimplerL: Optional[str]
    lipDimplerR: Optional[str]
    lipFunnelerLower: Optional[str]
    lipFunnelerUpper: Optional[str]
    lipLowerDnL: Optional[str]
    lipLowerDnR: Optional[str]
    lipLowerPullDnL: Optional[str]
    lipLowerPullDnR: Optional[str]
    lipLowerUpL: Optional[str]
    lipLowerUpR: Optional[str]
    lipNarrowL: Optional[str]
    lipNarrowR: Optional[str]
    lipPoutLower: Optional[str]
    lipPoutUpper: Optional[str]
    lipPresserL: Optional[str]
    lipPresserR: Optional[str]
    lipPucker: Optional[str]
    lipPullL: Optional[str]
    lipPullR: Optional[str]
    lipPushLower: Optional[str]
    lipPushUpper: Optional[str]
    lipSmileClosedL: Optional[str]
    lipSmileClosedR: Optional[str]
    lipSmileOpenL: Optional[str]
    lipSmileOpenR: Optional[str]
    lipSneerL: Optional[str]
    lipSneerR: Optional[str]
    lipStickyL: Optional[str]
    lipStickyR: Optional[str]
    lipSuckLower: Optional[str]
    lipSuckUpper: Optional[str]
    lipSwingL: Optional[str]
    lipSwingR: Optional[str]
    lipTightnerL: Optional[str]
    lipTightnerR: Optional[str]
    lipUpperDnL: Optional[str]
    lipUpperDnR: Optional[str]
    lipUpperUpL: Optional[str]
    lipUpperUpR: Optional[str]
    lipWidenL: Optional[str]
    lipWidenR: Optional[str]
    noseCompress: Optional[str]
    noseFlare: Optional[str]
    noseSneerL: Optional[str]
    noseSneerR: Optional[str]
    noseWrinklerL: Optional[str]
    noseWrinklerR: Optional[str]


@dataclass
class MetadataFace(TypeValidator):
    """Class to validate by type (and some values) at initialization time a Face Metadata definition.
    mesh_name can be a str or None, and blendshape_names need to satisfy MetadataFaceBlendshapes
    specification.
    """

    mesh_name: Optional[str]
    blendshape_names: MetadataFaceBlendshapes


@dataclass
class CharacterMetadata(TypeValidator):
    """Class to validate by type (and some values) at initialization time a Character Metadata definition.
    materials need to be either MetadataMaterialSurface, MetadataMaterialFlat or MetadataMaterialHair,
    eyes_rigs need to be a MetadataEyeRig, body needs to be a MetadataBody and face needs to be a
    MetadataFace. Software needs to be 'blender' or 'maya' and version needs to be a #.#.# formatted str.
    """

    software: str
    version: str
    materials: List[Union[MetadataMaterialSurface, MetadataMaterialFlat, MetadataMaterialHair]]
    eyes_rig: List[MetadataEyeRig]
    body: MetadataBody
    face: MetadataFace

    def __post_init__(self):
        """Enforces some additional constraints that cannot be defined by type alone,
        and some values that need to be one of a list of valid options.
        software needs to be 'blender' or 'maya'.
        version needs to be a #.#.# formatted str.
        """

        super().__post_init__()

        supported_software = ['blender', 'maya']
        if self.software not in supported_software:
            raise ValueError(f'Unsupported software type. Currently supported software types: {supported_software}')

        if not match(r'^\d+\.\d+\.\d+$', self.version):
            raise ValueError('Unsupported version format. Expected format X.Y.Z where X, Y, and Z are integer numbers.')
