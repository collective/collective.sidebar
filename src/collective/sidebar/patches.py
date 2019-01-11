# -*- coding: utf-8 -*-
"""All patches that should be applied to the Plone environment on startup."""
import logging


logger = logging.getLogger('collective.sidebar')

MEMBER_IMAGE_SCALE = (400, 400)
MEMBER_IMAGE_QUALITY = 90


def apply_portrait_patch():
    logger.info(
        'patching portrait scale to {0} @ {1}% quality'.format(
            MEMBER_IMAGE_SCALE,
            MEMBER_IMAGE_QUALITY,
        ),
    )
    from Products.PlonePAS import config
    config.MEMBER_IMAGE_SCALE = MEMBER_IMAGE_SCALE
    config.IMAGE_SCALE_PARAMS['scale'] = MEMBER_IMAGE_SCALE
    config.IMAGE_SCALE_PARAMS['quality'] = MEMBER_IMAGE_QUALITY
