# Copyright 2025 Wonder Dynamics (an Autodesk Company)

# This source code is licensed under the GNU GPLv3
# found in the LICENSE file in the root directory of this source tree.

"""Static data for the add-on except for text messages. Those are in lib/text_static"""

BLENDER_ADDON_VERSION = (1, 2, 3)
METADATA_VERSION = (1, 1, 1)

DOCUMENTATION_URL = 'https://help.wonderdynamics.com/character-creation-getting-started'

EXPORT_FOLDER_NAME = 'flow_studio_character_data'

# Bone naming
standard_bone_names = [
    'Hips',
    'LeftUpLeg',
    'RightUpLeg',
    'Spine',
    'LeftLeg',
    'RightLeg',
    'Spine1',
    'LeftFoot',
    'RightFoot',
    'Spine2',
    'LeftToeBase',
    'RightToeBase',
    'Neck',
    'LeftShoulder',
    'RightShoulder',
    'Head',
    'LeftArm',
    'RightArm',
    'LeftForeArm',
    'RightForeArm',
    'LeftHand',
    'RightHand',
    'LeftHandIndex1',
    'LeftHandIndex2',
    'LeftHandIndex3',
    'LeftHandMiddle1',
    'LeftHandMiddle2',
    'LeftHandMiddle3',
    'LeftHandPinky1',
    'LeftHandPinky2',
    'LeftHandPinky3',
    'LeftHandRing1',
    'LeftHandRing2',
    'LeftHandRing3',
    'LeftHandThumb1',
    'LeftHandThumb2',
    'LeftHandThumb3',
    'RightHandIndex1',
    'RightHandIndex2',
    'RightHandIndex3',
    'RightHandMiddle1',
    'RightHandMiddle2',
    'RightHandMiddle3',
    'RightHandPinky1',
    'RightHandPinky2',
    'RightHandPinky3',
    'RightHandRing1',
    'RightHandRing2',
    'RightHandRing3',
    'RightHandThumb1',
    'RightHandThumb2',
    'RightHandThumb3',
]

# Bone name groups
torso_bones = [
    standard_bone_names[3],
    standard_bone_names[6],
    standard_bone_names[9],
    standard_bone_names[13],
    standard_bone_names[14],
]
head_bones = [
    standard_bone_names[12],
    standard_bone_names[15],
]
leg_bones = [
    standard_bone_names[1],
    standard_bone_names[2],
    standard_bone_names[4],
    standard_bone_names[5],
    standard_bone_names[7],
    standard_bone_names[8],
    standard_bone_names[10],
    standard_bone_names[11],
]
arm_bones = standard_bone_names[16:22]
hand_bones_left = standard_bone_names[22:37]
hand_bones_right = standard_bone_names[37:]

# Other Bone Naming Conventions
quickRig_bone_names = [
    'QuickRigCharacter_Hips',
    'QuickRigCharacter_LeftUpLeg',
    'QuickRigCharacter_RightUpLeg',
    'QuickRigCharacter_Spine',
    'QuickRigCharacter_LeftLeg',
    'QuickRigCharacter_RightLeg',
    'QuickRigCharacter_Spine1',
    'QuickRigCharacter_LeftFoot',
    'QuickRigCharacter_RightFoot',
    'QuickRigCharacter_Spine2',
    'QuickRigCharacter_LeftToeBase',
    'QuickRigCharacter_RightToeBase',
    'QuickRigCharacter_Neck',
    'QuickRigCharacter_LeftShoulder',
    'QuickRigCharacter_RightShoulder',
    'QuickRigCharacter_Head',
    'QuickRigCharacter_LeftArm',
    'QuickRigCharacter_RightArm',
    'QuickRigCharacter_LeftForeArm',
    'QuickRigCharacter_RightForeArm',
    'QuickRigCharacter_LeftHand',
    'QuickRigCharacter_RightHand',
    'QuickRigCharacter_LeftHandIndex1',
    'QuickRigCharacter_LeftHandIndex2',
    'QuickRigCharacter_LeftHandIndex3',
    'QuickRigCharacter_LeftHandMiddle1',
    'QuickRigCharacter_LeftHandMiddle2',
    'QuickRigCharacter_LeftHandMiddle3',
    'QuickRigCharacter_LeftHandPinky1',
    'QuickRigCharacter_LeftHandPinky2',
    'QuickRigCharacter_LeftHandPinky3',
    'QuickRigCharacter_LeftHandRing1',
    'QuickRigCharacter_LeftHandRing2',
    'QuickRigCharacter_LeftHandRing3',
    'QuickRigCharacter_LeftHandThumb1',
    'QuickRigCharacter_LeftHandThumb2',
    'QuickRigCharacter_LeftHandThumb3',
    'QuickRigCharacter_RightHandIndex1',
    'QuickRigCharacter_RightHandIndex2',
    'QuickRigCharacter_RightHandIndex3',
    'QuickRigCharacter_RightHandMiddle1',
    'QuickRigCharacter_RightHandMiddle2',
    'QuickRigCharacter_RightHandMiddle3',
    'QuickRigCharacter_RightHandPinky1',
    'QuickRigCharacter_RightHandPinky2',
    'QuickRigCharacter_RightHandPinky3',
    'QuickRigCharacter_RightHandRing1',
    'QuickRigCharacter_RightHandRing2',
    'QuickRigCharacter_RightHandRing3',
    'QuickRigCharacter_RightHandThumb1',
    'QuickRigCharacter_RightHandThumb2',
    'QuickRigCharacter_RightHandThumb3',
]

unrealEngine_bone_names = [
    'pelvis',
    'thigh_l',
    'thigh_r',
    'spine_03',
    'calf_l',
    'calf_r',
    'spine_04',
    'foot_l',
    'foot_r',
    'spine_05',
    'ball_l',
    'ball_r',
    'neck_01',
    'clavicle_l',
    'clavicle_r',
    'head',
    'upperarm_l',
    'upperarm_r',
    'lowerarm_l',
    'lowerarm_r',
    'hand_l',
    'hand_r',
    'index_01_l',
    'index_02_l',
    'index_03_l',
    'middle_01_l',
    'middle_02_l',
    'middle_03_l',
    'pinky_01_l',
    'pinky_02_l',
    'pinky_03_l',
    'ring_01_l',
    'ring_02_l',
    'ring_03_l',
    'thumb_01_l',
    'thumb_02_l',
    'thumb_03_l',
    'index_01_r',
    'index_02_r',
    'index_03_r',
    'middle_01_r',
    'middle_02_r',
    'middle_03_r',
    'pinky_01_r',
    'pinky_02_r',
    'pinky_03_r',
    'ring_01_r',
    'ring_02_r',
    'ring_03_r',
    'thumb_01_r',
    'thumb_02_r',
    'thumb_03_r',
]

daz3d_bone_names = [
    'hip',
    'lThigh',
    'rThigh',
    'abdomen',
    'lShin',
    'rShin',
    'abdomen2',
    'lFoot',
    'rFoot',
    'chest',
    'lToe',
    'rToe',
    'neck',
    'lCollar',
    'rCollar',
    'head',
    'lShldr',
    'rShldr',
    'lForeArm',
    'rForeArm',
    'lHand',
    'rHand',
    'lIndex1',
    'lIndex2',
    'lIndex3',
    'lMid1',
    'lMid2',
    'lMid3',
    'lPinky1',
    'lPinky2',
    'lPinky3',
    'lRing1',
    'lRing2',
    'lRing3',
    'lThumb1',
    'lThumb2',
    'lThumb3',
    'rIndex1',
    'rIndex2',
    'rIndex3',
    'rMid1',
    'rMid2',
    'rMid3',
    'rPinky1',
    'rPinky2',
    'rPinky3',
    'rRing1',
    'rRing2',
    'rRing3',
    'rThumb1',
    'rThumb2',
    'rThumb3',
]

characterCreator4_bone_names = [
    'CC_Base_Hip',
    'CC_Base_L_Thigh',
    'CC_Base_R_Thigh',
    'CC_Base_Waist',
    'CC_Base_L_Calf',
    'CC_Base_R_Calf',
    'CC_Base_Spine01',
    'CC_Base_L_Foot',
    'CC_Base_R_Foot',
    'CC_Base_Spine02',
    'CC_Base_L_ToeBase',
    'CC_Base_R_ToeBase',
    'CC_Base_NeckTwist01',
    'CC_Base_L_Clavicle',
    'CC_Base_R_Clavicle',
    'CC_Base_Head',
    'CC_Base_L_Upperarm',
    'CC_Base_R_Upperarm',
    'CC_Base_L_Forearm',
    'CC_Base_R_Forearm',
    'CC_Base_L_Hand',
    'CC_Base_R_Hand',
    'CC_Base_L_Index1',
    'CC_Base_L_Index2',
    'CC_Base_L_Index3',
    'CC_Base_L_Mid1',
    'CC_Base_L_Mid2',
    'CC_Base_L_Mid3',
    'CC_Base_L_Pinky1',
    'CC_Base_L_Pinky2',
    'CC_Base_L_Pinky3',
    'CC_Base_L_Ring1',
    'CC_Base_L_Ring2',
    'CC_Base_L_Ring3',
    'CC_Base_L_Thumb1',
    'CC_Base_L_Thumb2',
    'CC_Base_L_Thumb3',
    'CC_Base_R_Index1',
    'CC_Base_R_Index2',
    'CC_Base_R_Index3',
    'CC_Base_R_Mid1',
    'CC_Base_R_Mid2',
    'CC_Base_R_Mid3',
    'CC_Base_R_Pinky1',
    'CC_Base_R_Pinky2',
    'CC_Base_R_Pinky3',
    'CC_Base_R_Ring1',
    'CC_Base_R_Ring2',
    'CC_Base_R_Ring3',
    'CC_Base_R_Thumb1',
    'CC_Base_R_Thumb2',
    'CC_Base_R_Thumb3',
]

rigify_bone_names = [
    'torso',
    'thigh_fk.L',
    'thigh_fk.R',
    '',
    'shin_fk.L',
    'shin_fk.R',
    'spine_fk.002',
    'foot_fk.L',
    'foot_fk.R',
    'spine_fk.003',
    'toe_fk.L',
    'toe_fk.R',
    'neck',
    'shoulder.L',
    'shoulder.R',
    'head',
    'upper_arm_fk.L',
    'upper_arm_fk.R',
    'forearm_fk.L',
    'forearm_fk.R',
    'hand_fk.L',
    'hand_fk.R',
    'f_index.01.L',
    'f_index.02.L',
    'f_index.03.L',
    'f_middle.01.L',
    'f_middle.02.L',
    'f_middle.03.L',
    'f_pinky.01.L',
    'f_pinky.02.L',
    'f_pinky.03.L',
    'f_ring.01.L',
    'f_ring.02.L',
    'f_ring.03.L',
    'thumb.01.L',
    'thumb.02.L',
    'thumb.03.L',
    'f_index.01.R',
    'f_index.02.R',
    'f_index.03.R',
    'f_middle.01.R',
    'f_middle.02.R',
    'f_middle.03.R',
    'f_pinky.01.R',
    'f_pinky.02.R',
    'f_pinky.03.R',
    'f_ring.01.R',
    'f_ring.02.R',
    'f_ring.03.R',
    'thumb.01.R',
    'thumb.02.R',
    'thumb.03.R',
]

blenRig_bone_names = [
    'master_torso',
    'thigh_fk_L',
    'thigh_fk_R',
    'spine_1_fk',
    'shin_fk_L',
    'shin_fk_R',
    'spine_2_fk',
    'foot_fk_L',
    'foot_fk_R',
    'spine_3_fk',
    'foot_toe_1_fk_L',
    'foot_toe_1_fk_R',
    'neck_fk_ctrl',
    'shoulder_L',
    'shoulder_R',
    'head_fk',
    'arm_fk_L',
    'arm_fk_R',
    'forearm_fk_L',
    'forearm_fk_R',
    'hand_fk_L',
    'hand_fk_R',
    'fing_ind_2_L',
    'fing_ind_3_L',
    'fing_ind_4_L',
    'fing_mid_2_L',
    'fing_mid_3_L',
    'fing_mid_4_L',
    'fing_lit_2_L',
    'fing_lit_3_L',
    'fing_lit_4_L',
    'fing_ring_2_L',
    'fing_ring_3_L',
    'fing_ring_4_L',
    'fing_thumb_1_L',
    'fing_thumb_2_L',
    'fing_thumb_3_L',
    'fing_ind_2_R',
    'fing_ind_3_R',
    'fing_ind_4_R',
    'fing_mid_2_R',
    'fing_mid_3_R',
    'fing_mid_4_R',
    'fing_lit_2_R',
    'fing_lit_3_R',
    'fing_lit_4_R',
    'fing_ring_2_R',
    'fing_ring_3_R',
    'fing_ring_4_R',
    'fing_thumb_1_R',
    'fing_thumb_2_R',
    'fing_thumb_3_R',
]

autoRigPro_bone_names = [
    'c_root_master.x',
    'c_thigh_fk.l',
    'c_thigh_fk.r',
    'c_spine_01.x',
    'c_leg_fk.l',
    'c_leg_fk.r',
    'c_spine_02.x',
    'c_foot_fk.l',
    'c_foot_fk.r',
    'c_spine_03.x',
    'c_toes_fk.l',
    'c_toes_fk.r',
    'c_neck_master.x',
    'c_shoulder.l',
    'c_shoulder.r',
    'c_head.x',
    'c_arm_fk.l',
    'c_arm_fk.r',
    'c_forearm_fk.l',
    'c_forearm_fk.r',
    'c_hand_fk.l',
    'c_hand_fk.r',
    'c_index1.l',
    'c_index2.l',
    'c_index3.l',
    'c_middle1.l',
    'c_middle2.l',
    'c_middle3.l',
    'c_pinky1.l',
    'c_pinky2.l',
    'c_pinky3.l',
    'c_ring1.l',
    'c_ring2.l',
    'c_ring3.l',
    'c_thumb1.l',
    'c_thumb2.l',
    'c_thumb3.l',
    'c_index1.r',
    'c_index2.r',
    'c_index3.r',
    'c_middle1.r',
    'c_middle2.r',
    'c_middle3.r',
    'c_pinky1.r',
    'c_pinky2.r',
    'c_pinky3.r',
    'c_ring1.r',
    'c_ring2.r',
    'c_ring3.r',
    'c_thumb1.r',
    'c_thumb2.r',
    'c_thumb3.r',
]

# All bone naming conventions
all_supported_bone_names = {
    'Flow-Studio,-Mixamo,-Human-IK_bone_names': standard_bone_names,
    'Quick-Rig_bone_names': quickRig_bone_names,
    'Character-Creator-4_bone_names': characterCreator4_bone_names,
    'Daz-3D_bone_names': daz3d_bone_names,
    'Unreal-Engine_bone_names': unrealEngine_bone_names,
    'BlenRig_bone_names': blenRig_bone_names,
    'Rigify_bone_names': rigify_bone_names,
    'Auto-Rig-Pro_bone_names': autoRigPro_bone_names,
}

# Shapekey naming
standard_shapekey_names = [
    'Basis',
    'browInnerDnL',
    'browInnerDnR',
    'browInnerUpL',
    'browInnerUpR',
    'browOuterDnL',
    'browOuterDnR',
    'browOuterUpL',
    'browOuterUpR',
    'browSqueezeL',
    'browSqueezeR',
    'cheekBlowL',
    'cheekBlowR',
    'cheekUpL',
    'cheekUpR',
    'eyeBlinkL',
    'eyeBlinkR',
    'eyeCompressL',
    'eyeCompressR',
    'eyeDn',
    'eyeL',
    'eyeR',
    'eyeSquintL',
    'eyeSquintR',
    'eyeUp',
    'eyeWidenLowerL',
    'eyeWidenLowerR',
    'eyeWidenUpperL',
    'eyeWidenUpperR',
    'jawIn',
    'jawL',
    'jawOpen',
    'jawOut',
    'jawR',
    'lipChinRaiserL',
    'lipChinRaiserR',
    'lipCloseLower',
    'lipCloseUpper',
    'lipCornerDnL',
    'lipCornerDnR',
    'lipCornerUpL',
    'lipCornerUpR',
    'lipDimplerL',
    'lipDimplerR',
    'lipFunnelerLower',
    'lipFunnelerUpper',
    'lipLowerDnL',
    'lipLowerDnR',
    'lipLowerPullDnL',
    'lipLowerPullDnR',
    'lipLowerUpL',
    'lipLowerUpR',
    'lipNarrowL',
    'lipNarrowR',
    'lipPoutLower',
    'lipPoutUpper',
    'lipPresserL',
    'lipPresserR',
    'lipPucker',
    'lipPullL',
    'lipPullR',
    'lipPushLower',
    'lipPushUpper',
    'lipSmileClosedL',
    'lipSmileClosedR',
    'lipSmileOpenL',
    'lipSmileOpenR',
    'lipSneerL',
    'lipSneerR',
    'lipStickyL',
    'lipStickyR',
    'lipSuckLower',
    'lipSuckUpper',
    'lipSwingL',
    'lipSwingR',
    'lipTightnerL',
    'lipTightnerR',
    'lipUpperDnL',
    'lipUpperDnR',
    'lipUpperUpL',
    'lipUpperUpR',
    'lipWidenL',
    'lipWidenR',
    'noseCompress',
    'noseFlare',
    'noseSneerL',
    'noseSneerR',
    'noseWrinklerL',
    'noseWrinklerR',
]

# All shapekey naming conventions
all_supported_shapekey_names = {
    'WD_shapekey_names': standard_shapekey_names,
}
