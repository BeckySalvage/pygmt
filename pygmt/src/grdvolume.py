"""
grdvolume - Calculate grid volume and area constrained by a contour.
"""
import numpy as np
import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    C="plane",
    Cr="outside_volume",
    D="slice",
    R="region",
    S="unit",
    V="verbose",
)
@kwargs_to_strings(C="sequence", R="sequence")
def grdvolume(grid, data_format="a", **kwargs):
    r"""
    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
        This is the only required parameter.
    {R}
    {V}

    Returns
    -------
    volume : str
        A string with the volume between the surface and specified plane.
    """
    with GMTTempFile() as outfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                arg_str = " ".join(
                    [infile, build_arg_string(kwargs), "->" + outfile.name]
                )
                lib.call_module("grdvolume", arg_str)
        result = outfile.read()
    if data_format == "s":
        return result
    data_list = []
    for string_entry in result.strip().split("\n"):
        float_entry = []
        string_list = string_entry.strip().split()
        for i in string_list:
            float_entry.append(float(i))
        data_list.append(float_entry)
    data_array = np.array(data_list)
    if data_format == "a":
        result = data_array
    elif data_format == "d":
        result = pd.DataFrame(data_array)
    else:
        raise GMTInvalidInput("""Must specify format as either a, d, or s.""")
    return result
