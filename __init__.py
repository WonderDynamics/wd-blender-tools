bl_info = {
    'name': 'Wonder Studio Character Validation',
    'author': 'Wonder Dynamics',
    'version': (1, 2, 1),
    'blender': (3, 6, 2),
    'location': 'View3D > Panel',
    'description': 'Validate characters for Wonder Studio.',
    'doc_url': 'https://help.wonderdynamics.com/character-creation/getting-started',
}

from .wd_blender_tools.addon_core import (
    register,
    unregister,
)
