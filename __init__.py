bl_info = {
    'name': 'Flow Studio Character Validation',
    'author': 'Wonder Dynamics (an Autodesk Company)',
    'version': (1, 2, 3),
    'blender': (3, 6, 2),
    'location': 'View3D > Panel',
    'description': 'Validate and export characters for Flow Studio.',
    'doc_url': 'https://help.wonderdynamics.com/character-creation-getting-started',
}

from .wd_blender_tools.addon_core import (
    register,
    unregister,
)
