# (C) Daniel Strano and the Qrack contributors 2017-2021. All rights reserved.
#
# "QrackSystem" is a central access point, in Python, to the vm6502q/qrack
# shared library, in C++11. For ease, it wraps all Qrack shared library
# functions with native Python method signatures.
#
# The "QrackSystem" references underlying distinct Qrack simulator instances
# via integer IDs that are created upon request to allocate a new simulator.
# While you can directly use QrackSystem to manage all your simulators, we
# suggest that you instead instantiate an instance of "QrackSimulator", which
# requests its own new simulator ID and supplies it to "QrackSystem" for all
# Qrack shared library calls, therefore acting as an independent Qrack
# simulator object.
#
# Use of this source code is governed by an MIT-style license that can be
# found in the LICENSE file or at https://opensource.org/licenses/MIT.

import os
from ctypes import *
from sys import platform as _platform
import platform
import struct


class QrackSystem:

    def __init__(self):
        shared_lib_path = "/usr/local/lib/libqrack_pinvoke.so"
        if _platform == "linux" or _platform == "linux2":
            machine = platform.machine()
            if machine == "armv71":
                shared_lib_path = "qrack_lib/Linux/ARMv7/libqrack_pinvoke.so"
            elif machine == "aarch64":
                shared_lib_path = "qrack_lib/Linux/ARM64/libqrack_pinvoke.so"
            else:
                shared_lib_path = "qrack_lib/Linux/x86_64/libqrack_pinvoke.so"
        elif _platform == "darwin":
            shared_lib_path = "qrack_lib/Mac/x86_64/libqrack_pinvoke.so"
        elif _platform == "win32":
            struct_size = struct.calcsize("P") * 8
            if struct_size == 32:
                shared_lib_path = "qrack_lic\\Windows\\x86\\qrack_pinvoke.dll"
            else:
                shared_lib_path = "qrack_lic\\Windows\\x86_64\\qrack_pinvoke.dll"
        try:
            basedir = os.path.abspath(os.path.dirname(__file__))
            self.qrack_lib = CDLL(os.path.join(basedir, shared_lib_path))
        except Exception as e:
            print(e)

        # Define function signatures, up front

        # non-quantum

        self.qrack_lib.init.restype = c_uint
        self.qrack_lib.init.argTypes = []

        self.qrack_lib.init_count.restype = c_uint
        self.qrack_lib.init_count.argTypes = [c_uint]

        self.qrack_lib.init_clone.restype = c_uint
        self.qrack_lib.init_clone.argTypes = [c_uint]

        self.qrack_lib.destroy.restype = None
        self.qrack_lib.destroy.argTypes = [c_uint]

        self.qrack_lib.seed.restype = None
        self.qrack_lib.seed.argTypes = [c_uint, c_uint]

        self.qrack_lib.set_concurrency.restype = None
        self.qrack_lib.set_concurrency.argTypes = [c_uint, c_uint]

        # pseudo-quantum

        self.qrack_lib.Prob.restype = c_double
        self.qrack_lib.Prob.argTypes = [c_uint, c_uint]

        self.qrack_lib.PermutationExpectation.restype = c_double
        self.qrack_lib.PermutationExpectation.argTypes = [c_uint, c_uint, POINTER(c_uint)]

        self.qrack_lib.JointEnsembleProbability.resType = c_double
        self.qrack_lib.JointEnsembleProbability.argTypes = [c_uint, c_uint, POINTER(c_int), c_uint]

        self.qrack_lib.ResetAll.resType = None
        self.qrack_lib.ResetAll.argTypes = [c_uint]

        # allocate and release

        self.qrack_lib.allocateQubit.resType = None
        self.qrack_lib.allocateQubit.argTypes = [c_uint, c_uint]

        self.qrack_lib.release.resType = c_bool
        self.qrack_lib.release.argTypes = [c_uint, c_uint]

        self.qrack_lib.num_qubits.resType = c_uint
        self.qrack_lib.num_qubits.argTypes = [c_uint]

        # single-qubit gates

        self.qrack_lib.X.resType = None
        self.qrack_lib.X.argTypes = [c_uint, c_uint]

        self.qrack_lib.Y.resType = None
        self.qrack_lib.Y.argTypes = [c_uint, c_uint]

        self.qrack_lib.Z.resType = None
        self.qrack_lib.Z.argTypes = [c_uint, c_uint]

        self.qrack_lib.H.resType = None
        self.qrack_lib.H.argTypes = [c_uint, c_uint]

        self.qrack_lib.S.resType = None
        self.qrack_lib.S.argTypes = [c_uint, c_uint]

        self.qrack_lib.T.resType = None
        self.qrack_lib.T.argTypes = [c_uint, c_uint]

        self.qrack_lib.AdjS.resType = None
        self.qrack_lib.AdjS.argTypes = [c_uint, c_uint]

        self.qrack_lib.AdjT.resType = None
        self.qrack_lib.AdjT.argTypes = [c_uint, c_uint]

        self.qrack_lib.U.resType = None
        self.qrack_lib.U.argTypes = [c_uint, c_uint, c_double, c_double, c_double]

        self.qrack_lib.Mtrx.resType = None
        self.qrack_lib.Mtrx.argTypes = [c_uint, POINTER(c_double), c_uint]

        # multi-controlled single-qubit gates

        self.qrack_lib.MCX.resType = None
        self.qrack_lib.MCX.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint]

        self.qrack_lib.MCY.resType = None
        self.qrack_lib.MCY.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint]

        self.qrack_lib.MCZ.resType = None
        self.qrack_lib.MCZ.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint]

        self.qrack_lib.MCH.resType = None
        self.qrack_lib.MCH.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint]

        self.qrack_lib.MCS.resType = None
        self.qrack_lib.MCS.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint]

        self.qrack_lib.MCT.resType = None
        self.qrack_lib.MCT.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint]

        self.qrack_lib.MCAdjS.resType = None
        self.qrack_lib.MCAdjS.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint]

        self.qrack_lib.MCAdjT.resType = None
        self.qrack_lib.MCAdjT.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint]

        self.qrack_lib.MCU.resType = None
        self.qrack_lib.MCU.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint, c_double, c_double, c_double]

        self.qrack_lib.MCMtrx.resType = None
        self.qrack_lib.MCMtrx.argTypes = [c_uint, c_uint, POINTER(c_uint), POINTER(c_double), c_uint]

        # multi-anti-controlled single-qubit gates

        self.qrack_lib.MACX.resType = None
        self.qrack_lib.MACX.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint]

        self.qrack_lib.MACY.resType = None
        self.qrack_lib.MACY.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint]

        self.qrack_lib.MACZ.resType = None
        self.qrack_lib.MACZ.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint]

        self.qrack_lib.MACH.resType = None
        self.qrack_lib.MACH.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint]

        self.qrack_lib.MACS.resType = None
        self.qrack_lib.MACS.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint]

        self.qrack_lib.MACT.resType = None
        self.qrack_lib.MACT.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint]

        self.qrack_lib.MACAdjS.resType = None
        self.qrack_lib.MACAdjS.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint]

        self.qrack_lib.MACAdjT.resType = None
        self.qrack_lib.MACAdjT.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint]

        self.qrack_lib.MACU.resType = None
        self.qrack_lib.MACU.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint, c_double, c_double, c_double]

        self.qrack_lib.MACMtrx.resType = None
        self.qrack_lib.MACMtrx.argTypes = [c_uint, c_uint, POINTER(c_uint), POINTER(c_double), c_uint]

        # rotations

        self.qrack_lib.R.resType = None
        self.qrack_lib.R.argTypes = [c_uint, c_uint, c_double, c_uint]

        self.qrack_lib.MCR.resType = None
        self.qrack_lib.MCR.argTypes = [c_uint, c_uint, c_double, c_uint, POINTER(c_uint), c_uint]

        # exponential of Pauli operators

        self.qrack_lib.Exp.resType = None
        self.qrack_lib.Exp.argTypes = [c_uint, c_uint, POINTER(c_int), c_double, POINTER(c_uint)]

        self.qrack_lib.MCExp.resType = None
        self.qrack_lib.MCExp.argTypes = [c_uint, c_uint, POINTER(c_int), c_double, c_uint, POINTER(c_uint), POINTER(c_uint)]

        # measurements

        self.qrack_lib.M.resType = c_uint
        self.qrack_lib.M.argTypes = [c_uint, c_uint]

        self.qrack_lib.Measure.resType = c_uint
        self.qrack_lib.Measure.argTypes = [c_uint, c_uint, POINTER(c_int), POINTER(c_uint)]

        self.qrack_lib.MeasureShots.resType = None
        self.qrack_lib.MeasureShots.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint, POINTER(c_uint)]

        # swap

        self.qrack_lib.SWAP.resType = None
        self.qrack_lib.SWAP.argTypes = [c_uint, c_uint, c_uint]

        self.qrack_lib.CSWAP.resType = None
        self.qrack_lib.CSWAP.argTypes = [c_uint, c_uint, POINTER(c_uint), c_uint, c_uint]

        # (quasi-)Boolean gates

        self.qrack_lib.AND.resType = None
        self.qrack_lib.AND.argTypes = [c_uint, c_uint, c_uint, c_uint]

        self.qrack_lib.OR.resType = None
        self.qrack_lib.OR.argTypes = [c_uint, c_uint, c_uint, c_uint]

        self.qrack_lib.XOR.resType = None
        self.qrack_lib.XOR.argTypes = [c_uint, c_uint, c_uint, c_uint]

        self.qrack_lib.NAND.resType = None
        self.qrack_lib.NAND.argTypes = [c_uint, c_uint, c_uint, c_uint]

        self.qrack_lib.NOR.resType = None
        self.qrack_lib.NOR.argTypes = [c_uint, c_uint, c_uint, c_uint]

        self.qrack_lib.XNOR.resType = None
        self.qrack_lib.XNOR.argTypes = [c_uint, c_uint, c_uint, c_uint]

        # half classical (quasi-)Boolean gates

        self.qrack_lib.CLAND.resType = None
        self.qrack_lib.CLAND.argTypes = [c_uint, c_bool, c_uint, c_uint]

        self.qrack_lib.CLOR.resType = None
        self.qrack_lib.CLOR.argTypes = [c_uint, c_bool, c_uint, c_uint]

        self.qrack_lib.CLXOR.resType = None
        self.qrack_lib.CLXOR.argTypes = [c_uint, c_bool, c_uint, c_uint]

        self.qrack_lib.CLNAND.resType = None
        self.qrack_lib.CLNAND.argTypes = [c_uint, c_bool, c_uint, c_uint]

        self.qrack_lib.CLNOR.resType = None
        self.qrack_lib.CLNOR.argTypes = [c_uint, c_bool, c_uint, c_uint]

        self.qrack_lib.CLXNOR.resType = None
        self.qrack_lib.CLXNOR.argTypes = [c_uint, c_bool, c_uint, c_uint]

        # Fourier transform

        self.qrack_lib.QFT.resType = None
        self.qrack_lib.QFT.argTypes = [c_uint, c_uint, POINTER(c_uint)]

        self.qrack_lib.IQFT.resType = None
        self.qrack_lib.IQFT.argTypes = [c_uint, c_uint, POINTER(c_uint)]

        # miscellaneous

        self.qrack_lib.TrySeparate1Qb.resType = c_bool
        self.qrack_lib.TrySeparate1Qb.argTypes = [c_uint, c_uint]

        self.qrack_lib.TrySeparate2Qb.resType = c_bool
        self.qrack_lib.TrySeparate2Qb.argTypes = [c_uint, c_uint, c_uint]

        self.qrack_lib.TrySeparateTol.resType = c_bool
        self.qrack_lib.TrySeparateTol.argTypes = [c_uint, c_uint, POINTER(c_uint), c_double]

        self.qrack_lib.SetReactiveSeparate.resType = c_bool
        self.qrack_lib.SetReactiveSeparate.argTypes = [c_uint, c_bool]
