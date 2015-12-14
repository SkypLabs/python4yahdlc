#include <Python.h>
#include "yahdlc.h"

#define MAX_FRAME_PAYLOAD		512
#define HEADERS_LENGTH			8

#define TOTAL_FRAME_LENGTH		MAX_FRAME_PAYLOAD + HEADERS_LENGTH

static PyObject *Yahdlc_MessageError;
static PyObject *Yahdlc_FCSError;

/* ---------- yahdlc function ---------- */

/*
 * Retrieves data from specified buffer containing the HDLC frame.
 */
static PyObject *get_data(PyObject *self, PyObject *args)
{
	int ret;
	const char *frame_data;
	char recv_data[TOTAL_FRAME_LENGTH];
	unsigned int buf_length = 0, recv_length = 0;
	yahdlc_control_t control;

	if (!PyArg_ParseTuple(args, "s#", &frame_data, &buf_length))
		return NULL;

	if (buf_length > TOTAL_FRAME_LENGTH)
	{
		PyErr_SetString(PyExc_ValueError, "buffer too long");
		return NULL;
	}

	ret = yahdlc_get_data(&control, frame_data, buf_length, recv_data, &recv_length);

	/* If success */
	if (ret >= 0)
	{
		PyObject *t;

		t = PyTuple_New(3);
		PyTuple_SetItem(t, 0, PyBytes_FromStringAndSize(recv_data, recv_length));
		PyTuple_SetItem(t, 1, PyLong_FromUnsignedLong(control.frame));
		PyTuple_SetItem(t, 2, PyLong_FromUnsignedLong(control.seq_no));

		return t;
	}
	else if (ret == -EINVAL)
	{
		PyErr_SetString(PyExc_ValueError, "invalid parameter");
		return NULL;
	}
	else if (ret == -ENOMSG)
	{
		PyErr_SetString(Yahdlc_MessageError, "invalid message");
		return NULL;
	}
	else if (ret == -EIO)
	{
		PyErr_SetString(Yahdlc_FCSError, "invalid FCS");
		return NULL;
	}
	else
	{
		PyErr_SetString(PyExc_RuntimeError, "unknown error");
		return NULL;
	}
}

/*
 * Resets values used in yahdlc_get_data function
 * to keep track of received buffers.
 */
static PyObject *get_data_reset(PyObject *self, PyObject *args)
{
	yahdlc_get_data_reset();

	Py_RETURN_NONE;
}

/*
 * Creates HDLC frame with specified data buffer.
 */
static PyObject *frame_data(PyObject *self, PyObject *args)
{
	int ret;
	const char *send_data;
	char frame_data[TOTAL_FRAME_LENGTH];
	unsigned int data_length = 0, frame_length = 0, frame_type = YAHDLC_FRAME_DATA, seq_no = 0;
	yahdlc_control_t control;

	if (!PyArg_ParseTuple(args, "s#|II", &send_data, &data_length, &frame_type, &seq_no))
		return NULL;

	if (data_length > MAX_FRAME_PAYLOAD)
	{
		PyErr_SetString(PyExc_ValueError, "data too long");
		return NULL;
	}
	else if (frame_type != YAHDLC_FRAME_DATA && frame_type != YAHDLC_FRAME_ACK && frame_type != YAHDLC_FRAME_NACK)
	{
		PyErr_SetString(PyExc_ValueError, "bad frame type");
		return NULL;
	}
	else if (seq_no < 0 || seq_no > 7)
	{
		PyErr_SetString(PyExc_ValueError, "invalid sequence number");
		return NULL;
	}

	control.frame = frame_type;
	control.seq_no = seq_no;
	ret = yahdlc_frame_data(&control, send_data, data_length, frame_data, &frame_length);

	/* If success */
	if (ret == 0)
		return PyBytes_FromStringAndSize(frame_data, frame_length);
	else
	{
		PyErr_SetString(PyExc_ValueError, "invalid parameter");
		return NULL;
	}
}

/* ---------- Settings ---------- */

/*
	Python module's methods.
*/
static PyMethodDef YahdlcMethods[] = {
	{"get_data", get_data, METH_VARARGS, "Retrieves data from specified buffer containing the HDLC frame"},
	{"get_data_reset", get_data_reset, METH_VARARGS, "Resets values used in get_data method to keep track of received buffers"},
	{"frame_data", frame_data, METH_VARARGS, "Creates HDLC frame with specified data buffer"},
	{NULL, NULL, 0, NULL}
};

/*
 * Python module itself.
 */
static struct PyModuleDef yahdlc_module =
{
	PyModuleDef_HEAD_INIT,
	"yahdlc",
	"HDLC implementation",
	-1,
	YahdlcMethods
};

/*
	Python module initialization.
*/
PyMODINIT_FUNC PyInit_yahdlc(void)
{
	PyObject *m;

	m = PyModule_Create(&yahdlc_module);

	if (m == NULL)
		return NULL;

	Yahdlc_MessageError = PyErr_NewException("yahdlc.MessageError", NULL, NULL);
	Py_INCREF(Yahdlc_MessageError);
	PyModule_AddObject(m, "MessageError", Yahdlc_MessageError);

	Yahdlc_FCSError = PyErr_NewException("yahdlc.FCSError", NULL, NULL);
	Py_INCREF(Yahdlc_FCSError);
	PyModule_AddObject(m, "FCSError", Yahdlc_FCSError);

	PyModule_AddIntConstant(m, "FRAME_DATA", YAHDLC_FRAME_DATA);
	PyModule_AddIntConstant(m, "FRAME_ACK", YAHDLC_FRAME_ACK);
	PyModule_AddIntConstant(m, "FRAME_NACK", YAHDLC_FRAME_NACK);

	return m;
}
