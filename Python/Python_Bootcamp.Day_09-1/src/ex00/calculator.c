#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject *c_add(PyObject *self, PyObject *args) {
    int i_a = 0; 
    int i_b = 0;
    double f_a = 0; 
    double f_b = 0;

    if (!PyArg_ParseTuple(args, "ii", &i_a, &i_b)) {
        PyErr_Clear();
    } else {
        return PyLong_FromLong((int)(i_a + i_b));
    }
    if (!PyArg_ParseTuple(args, "dd", &f_a, &f_b)) {
        PyErr_SetString(PyExc_TypeError, "Arguments must be int or float");
        return NULL;
    }
    return PyFloat_FromDouble((double)(f_a + f_b));
}

static PyObject *c_sub(PyObject *self, PyObject *args) {
    int i_a = 0; 
    int i_b = 0;
    double f_a = 0; 
    double f_b = 0;

    if (!PyArg_ParseTuple(args, "ii", &i_a, &i_b)) {
        PyErr_Clear();
    } else {
        return PyLong_FromLong((int)(i_a - i_b));
    }
    if (!PyArg_ParseTuple(args, "dd", &f_a, &f_b)) {
        PyErr_SetString(PyExc_TypeError, "Arguments must be int or float");
        return NULL;
    }
    return PyFloat_FromDouble((double)(f_a - f_b));
}

static PyObject *c_mul(PyObject *self, PyObject *args) {
    int i_a = 0; 
    int i_b = 0;
    double f_a = 0; 
    double f_b = 0;

    if (!PyArg_ParseTuple(args, "ii", &i_a, &i_b)) {
        PyErr_Clear();
    } else {
        return PyLong_FromLong((int)(i_a * i_b));
    }
    if (!PyArg_ParseTuple(args, "dd", &f_a, &f_b)) {
        PyErr_SetString(PyExc_TypeError, "Arguments must be int or float");
        return NULL;
    }
    return PyFloat_FromDouble((double)(f_a * f_b));
}

static PyObject *c_div(PyObject *self, PyObject *args) {
    int i_a = 0; 
    int i_b = 0;
    double f_a = 0; 
    double f_b = 0;

    if (!PyArg_ParseTuple(args, "ii", &i_a, &i_b)) {
        PyErr_Clear();
    } else {
        if (i_b == 0) {
            PyErr_SetString(PyExc_ZeroDivisionError, "Division by zero");
            return NULL;
        }
        return PyLong_FromLong((int)(i_a / i_b));
    }
    if (!PyArg_ParseTuple(args, "dd", &f_a, &f_b)) {
        PyErr_SetString(PyExc_TypeError, "Arguments must be int or float");
        return NULL;
    }
    if (f_b == 0) {
        PyErr_SetString(PyExc_ZeroDivisionError, "Division by zero");
        return NULL;
    }
    return PyFloat_FromDouble((double)(f_a / f_b));
}

static PyMethodDef CalcMethods[] = {
    {"add", c_add, METH_VARARGS, "Python interface for C version of addition of 2 numbers"},
    {"sub", c_sub, METH_VARARGS, "Python interface for C version of subtraction of 2 numbers"},
    {"mul", c_mul, METH_VARARGS, "Python interface for C version of multiplication of 2 numbers"},
    {"div", c_div, METH_VARARGS, "Python interface for C version of division of 2 numbers"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef calcmodule = {
    PyModuleDef_HEAD_INIT,
    "calculator",
    "Python interface for the C version of basic arithmetic operations",
    -1,
    CalcMethods
};

PyMODINIT_FUNC PyInit_calculator(void) {
    return PyModule_Create(&calcmodule);
};
