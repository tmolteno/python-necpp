%module PyNEC

%include <pycomplex.swg>
%include <std_complex.i>

%{
#include "Python.h"
#include "numpy/arrayobject.h"
#include "numpy/ndarraytypes.h"
#include "src/math_util.h"
#include "src/nec_context.h"
#include "src/c_geometry.h"
#include "src/nec_radiation_pattern.h"
#include "src/nec_structure_currents.h"
#include "src/nec_results.h"
#include "src/nec_ground.h"
#include "src/safe_array.h"
#include "src/nec_exception.h"
#include <complex>
%}

/*! Exception handling stuff */

%include exception.i       
%exception
{
  try {
    $action
  }
  catch (nec_exception* nex)  {
    SWIG_exception(SWIG_RuntimeError,nex->get_message().c_str());
  }
  catch (const char* message) {
    SWIG_exception(SWIG_RuntimeError,message);
  }
  catch (...) {
    SWIG_exception(SWIG_RuntimeError,"Unknown exception");
  }       
}

/*! The following typemaps allow the automatic conversion of vectors and safe_arrays into numpy arrays */

%typemap (out) real_matrix {
  int nd = 2;
  npy_intp rows = $1.rows();
  npy_intp cols = $1.cols();
  npy_intp size[2] = {rows, cols};
  PyArrayObject* ret =(PyArrayObject *)(PyArray_SimpleNew(nd, &size[0], NPY_FLOAT64));
  for (int32_t i=0; i<rows; i++) {
    for (int32_t j=0; j<cols; j++) {
      *((double *) PyArray_GETPTR2(ret, i, j)) = $1.getItem(i,j);
    }
  }
  $result = (PyObject*) ret;
}

%typemap (out) real_array {
  int nd = 1;
  npy_intp size = $1.size();
  PyArrayObject* ret =(PyArrayObject *)(PyArray_SimpleNew(nd, &size, NPY_FLOAT64));
  for (int64_t i=0; i<size; i++)
      *((double *) PyArray_GETPTR1(ret, i)) = $1.getItem(i);
  $result = (PyObject*) ret;
}

%typemap (out) int_array {
  int nd = 1;
  npy_intp size = $1.size();
  PyArrayObject* ret =(PyArrayObject *)(PyArray_SimpleNew(nd, &size, NPY_INT32));
  for (int64_t i=0; i<size; i++)
      *((int32_t *) PyArray_GETPTR1(ret, i)) = $1.getItem(i);
  $result = (PyObject*) ret;
}

%typemap (out) complex_array {
  int nd = 1;
  npy_intp size = $1.size();
  PyArrayObject* ret =(PyArrayObject *)(PyArray_SimpleNew(nd, &size, NPY_COMPLEX64));
  for (int64_t i=0; i<size; i++)
      *((nec_complex *) PyArray_GETPTR1(ret, i)) = $1.getItem(i);
  $result = (PyObject*) ret;
}

%typemap (out) vector<nec_float> {
  vector<nec_float>::pointer ptr = &($1[0]);
  int nd = 1;
  npy_intp size = $1.size();
  PyArrayObject* ret =(PyArrayObject *)(PyArray_SimpleNew(nd, &size, NPY_FLOAT64));
  for (int64_t i=0; i<size; i++)
      *((nec_float *) PyArray_GETPTR1(ret, i)) = $1[i];
  $result = (PyObject*) ret;
}

%typemap (out) vector<int> {
  vector<int>::pointer ptr = &($1[0]);
  int nd = 1;
  npy_intp size = $1.size();
  // $result =(PyObject *)(PyArray_SimpleNewFromData(nd, &size, NPY_INT32, (void *)(ptr)));
  PyArrayObject* ret =(PyArrayObject *)(PyArray_SimpleNew(nd, &size, NPY_INT32));
  for (int64_t i=0; i<size; i++)
      *((int *) PyArray_GETPTR1(ret, i)) = $1[i];
  $result = (PyObject*) ret;
}

%typemap (out) vector<nec_complex> {
  vector<nec_complex>::pointer ptr = &($1[0]);
  int nd = 1;
  npy_intp size = $1.size();
  // $result =(PyObject *)(PyArray_SimpleNewFromData(nd, &size, NPY_COMPLEX64, (void *)(ptr) ));
  PyArrayObject* ret =(PyArrayObject *)(PyArray_SimpleNew(nd, &size, NPY_COMPLEX64));
  for (int64_t i=0; i<size; i++)
      *((nec_complex *) PyArray_GETPTR1(ret, i)) = $1[i];
  $result = (PyObject*) ret;
}

/*! The two following interface files have only been created to avoid errors during the wrapping process. */

%import "interface_files/math_util.i"
%include "interface_files/safe_array.i"


/*! For each of the following interface files a corresponding python file has been created. 
    The python generated file has been used as a starting point, then it has been improved to
    provide a more user-friendly module.
*/
%include "interface_files/nec_context.i"
%include "interface_files/c_geometry.i"
%include "interface_files/nec_radiation_pattern.i"
%include "interface_files/nec_norm_rx_pattern.i"
%include "interface_files/nec_structure_excitation.i"
%include "interface_files/nec_antenna_input.i"
%include "interface_files/nec_near_field_pattern.i"
%include "interface_files/nec_structure_currents.i"
%include "interface_files/nec_ground.i"

/* The function below is added to the init function of the wrapped module.
 * It's mandatory to do so before to use the numarray API 
 */
%init %{
import_array();
%} 

