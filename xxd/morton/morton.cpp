/*
 *  C++ source file for module xxd.morton
 */


// See http://people.duke.edu/~ccc14/cspy/18G_C++_Python_pybind11.html for examples on how to use pybind11.
// The example below is modified after http://people.duke.edu/~ccc14/cspy/18G_C++_Python_pybind11.html#More-on-working-with-numpy-arrays
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <algorithm>

namespace py = pybind11;

// Expands a 10-bit integer into 30 bits
// by inserting 2 zeros after each bit.
unsigned int expandBits(unsigned int v)
{
    v = (v * 0x00010001u) & 0xFF0000FFu;
    v = (v * 0x00000101u) & 0x0F00F00Fu;
    v = (v * 0x00000011u) & 0xC30C30C3u;
    v = (v * 0x00000005u) & 0x49249249u;
    return v;
}

// Calculates a 30-bit Morton code for the
// given 3D point located within the unit cube [0,1].
unsigned int morton3D(float x, float y, float z)
{
    x = std::min(std::max(x * 1024.0f, 0.0f), 1023.0f);
    y = std::min(std::max(y * 1024.0f, 0.0f), 1023.0f);
    z = std::min(std::max(z * 1024.0f, 0.0f), 1023.0f);
    unsigned int xx = expandBits((unsigned int)x);
    unsigned int yy = expandBits((unsigned int)y);
    unsigned int zz = expandBits((unsigned int)z);
    return xx * 4 + yy * 2 + zz;
}

// compute the morton codes of a collection of 3D points.
void morton3Da( float* x, float* y, float* z, unsigned int* m , unsigned int n)
{// ?? does this vectorize ??
    for(unsigned int i=0; i<n; ++i ) {
        m[i] = morton3D(x[i], y[i], z[i]);
    }
    
}


void
code
    ( py::array_t<float> x // input
    , py::array_t<float> y // input
    , py::array_t<float> z // input
    , py::array_t<unsigned int> m
    )
{
    auto bufx = x.request()
       , bufy = y.request()
       , bufz = z.request()
       , bufm = m.request()
       ;
    if( bufx.ndim != 1 ) throw std::runtime_error("x must be 1D.");
    if( bufy.ndim != 1 ) throw std::runtime_error("y must be 1D.");
    if( bufz.ndim != 1 ) throw std::runtime_error("z must be 1D.");
    if( bufm.ndim != 1 ) throw std::runtime_error("m must be 1D.");
    
    if( (bufx.shape[0] != bufy.shape[0])
     || (bufx.shape[0] != bufz.shape[0])
     || (bufx.shape[0] != bufm.shape[0]) )
    {
        throw std::runtime_error("Input shapes must match");
    }

 // because the Numpy arrays are mutable by default, py::array_t is mutable too.
 // Below we declare the raw C++ arrays for x , y and z as const to make their intent clear.
    float const  *px = static_cast<float const *>(bufx.ptr);
    float const  *py = static_cast<float const *>(bufy.ptr);
    float const  *pz = static_cast<float const *>(bufz.ptr);
    unsigned int *pm = static_cast<unsigned int*>(bufm.ptr);

 // Do the actual work
     unsigned int n = bufx.shape[0];    
    for (size_t i = 0; i < n; i++)
        pm[i] = morton3D(px[i], py[i], pz[i]);
}


PYBIND11_MODULE(morton, m)
{// optional module doc-string
    m.doc() = "pybind11 morton plugin"; // optional module docstring
 // list the functions you want to expose:
 // m.def("exposed_name", function_pointer, "doc-string for the exposed function");
    m.def("code", &code, "Compute the morton code for a collection of points.");
    m.def("code1", &morton3D, "Compute the morton code for a single points.");
}
