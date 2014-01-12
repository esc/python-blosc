########################################################################
#
#       License: MIT
#       Created: May 4, 2013
#       Author:  Valentin Haenel - valentin@haenel.co
#       Author:  Francesc Alted - faltet@gmail.com
#
########################################################################

"""
Small benchmark that compares a plain NumPy array copy against
compression through different compressors in Blosc.
"""

from __future__ import print_function
import numpy
import time
import blosc

N = 1e7
clevel = 9

print("Creating a large NumPy array with %d int64 elements..." % N)
in_ = numpy.arange(N, dtype=numpy.int64)
print(in_)

tic = time.time()
out_ = in_.copy()
toc = time.time()
print("Time for copy array:     %.3f s." % (toc-tic,))
print()

for cname in blosc.compressor_list():
    print("Using *** %s *** compressor" % cname)
    tic = time.time()
    c = blosc.pack_array(in_, clevel=clevel, shuffle=True, cname=cname)
    ctoc = time.time()
    out = blosc.unpack_array(c)
    dtoc = time.time()
    assert((in_ == out).all())
    print("Time for pack_array/unpack_array:     %.3f/%.3f s." % \
          (ctoc-tic, dtoc-tic), end='')
    print("\tCompr ratio: %.2f" % (in_.size*in_.dtype.itemsize*1. / len(c)))

    tic = time.time()
    c = blosc.compress_ptr(in_.__array_interface__['data'][0],
                           in_.size, in_.dtype.itemsize,
                           clevel=clevel, shuffle=True, cname=cname)
    ctoc = time.time()
    out = numpy.empty(in_.size, dtype=in_.dtype)
    dtoc = time.time()
    blosc.decompress_ptr(c, out.__array_interface__['data'][0])
    assert((in_ == out).all())
    print("Time for compress_ptr/decompress_ptr: %.3f/%.3f s." % \
          (ctoc-tic, dtoc-tic), end='')
    print("\tCompr ratio: %.2f" % (in_.size*in_.dtype.itemsize*1. / len(c)))

