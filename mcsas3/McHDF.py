import numpy as np
import h5py

class McHDF(object):
    """Helper functions for HDF5 storage of items"""

    def __init__(self):
        pass

    def _HDFstoreKV(self, filename = None, path = None, key = None, value = None):
        assert filename is not None, "filename (output filename) cannot be empty"
        assert path is not None, "HDF5 path cannot be empty"
        assert key is not None, "key cannot be empty"

        """stores the settings in an output file (HDF5)"""
        with h5py.File(filename) as h5f:
            h5g = h5f.require_group(path)

            # store arrays:
            # convert all compatible data types to arrays:
            if type(value) is tuple or type(value) is list:
                value = np.array(value)
            if value is not None and type(value) is np.ndarray:
                # HDF cannot store unicode string arrays, these need to be stored as a special type:
                if value.dtype == '<U6':
                    value = value.astype(h5py.special_dtype(vlen=str))
                # store the data in the prefiously defined group:
                h5g.require_dataset(key, data = value, shape = value.shape, dtype = value.dtype)

            # non-array values are stored here:
            elif value is not None:
                # try and see if the destination already exists.. This can be done by require_dataset, but that requires shape and dtype to be specified. This method doesn't:
                dset = h5g.get(key, None)
                if dset is None:
                    h5g.create_dataset(key, data = value)
                else:
                    dset[()] = value

            # we are skipping None values for now, that case should be caught on load.