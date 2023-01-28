"""Utility function for the workshop."""

import datetime as dt


def mpl_svg_config(hashsalt):
    """Help configure the SVG backend for Matplotlib and make it reproducible."""
    from matplotlib import rc
    rc('svg', hashsalt=hashsalt)

    return {
        'metadata': {
            'Date': f'(c) 2021-{dt.date.today().year} Stefanie Molin'
        }
    }
