from __future__ import print_function
from sot_talos_balance.simple_zmp_estimator import SimpleZmpEstimator
from numpy.testing import assert_almost_equal as assertApprox
import numpy as np

# --- Create estimator

print("--- Create estimator ---")

estimator = SimpleZmpEstimator("ciao")

print("\nSignals (at creation):")
estimator.displaySignals()

# --- First test

print()
print("--- First test ---")

estimator.wrenchLeft.value  = [0.0,0.0,10.0,0.0,0.0,0.0]
estimator.wrenchRight.value = [0.0,0.0,10.0,0.0,0.0,0.0]

estimator.poseLeft.value  = [ [1.0, 0.0, 0.0, 1.0],
                              [0.0, 1.0, 0.0, 0.0],
                              [0.0, 0.0, 1.0, 0.1],
                              [0.0, 0.0, 0.0, 1.0]
                            ]
estimator.poseRight.value = [ [1.0, 0.0, 0.0, 0.0],
                              [0.0, 1.0, 0.0, 1.0],
                              [0.0, 0.0, 1.0, 0.1],
                              [0.0, 0.0, 0.0, 1.0]
                            ]

print()
print( "wrenchLeft:  %s" % (estimator.wrenchLeft.value,) )
print( "wrenchRight: %s" % (estimator.wrenchRight.value,) )
print( "poseLeft:\n%s" % (np.matrix(estimator.poseLeft.value),) )
print( "poseRight:\n%s" % (np.matrix(estimator.poseRight.value),) )

estimator.init()

estimator.zmp.recompute(0)

copLeft  = (1.0, 0.0, 0.0)
copRight = (0.0, 1.0, 0.0)
zmp = (0.5, 0.5, 0.0)

print()
print( "copLeft:  %s" % (estimator.copLeft.value,) )
assertApprox(estimator.copLeft.value, copLeft)
print( "copRight: %s" % (estimator.copRight.value,) )
assertApprox(estimator.copRight.value, copRight)
print( "zmp:      %s" % (estimator.zmp.value,) )
assertApprox(estimator.zmp.value, zmp)

# --- Second test

print()
print("--- Second test ---")

import pinocchio as pin

model = pin.buildSampleModelHumanoid()
data = model.createData()
rightId = model.getFrameId('rlegeffector_body')
leftId = model.getFrameId('llegeffector_body')

q = pin.neutral(model)
q[:3] = np.matrix([1.0,  0.0,  0.0]).T                         # displace freeflyer along x for testing 
q[3:7] = np.matrix([np.sqrt(2)/2,  0.0,  np.sqrt(2)/2, 0.0]).T # orient the base so that the feet are flat
pin.framesForwardKinematics(model,data,q)

poseRight = data.oMf[rightId].homogeneous.tolist()
poseLeft = data.oMf[leftId].homogeneous.tolist()

com = pin.centerOfMass(model,data,q).flatten().tolist()[0]

m = sum([inertia.mass for inertia in model.inertias[1:] ])
g = 9.81
fz = m*g/2.0
forceLeft  = [0.0, 0.0, fz]
forceRight = [0.0, 0.0, fz]
lever = com[0] - data.oMf[rightId].translation[0]
tauy = -fz*lever
wrenchLeft  = forceLeft  + [0.0, tauy, 0.0]
wrenchRight = forceRight + [0.0, tauy, 0.0]

estimator.wrenchLeft.value  = wrenchLeft
estimator.wrenchRight.value = wrenchRight
estimator.poseLeft.value  = poseLeft
estimator.poseRight.value = poseRight

print()
print( "wrenchLeft:  %s" % (estimator.wrenchLeft.value,) )
print( "wrenchRight: %s" % (estimator.wrenchRight.value,) )
print( "poseLeft:\n%s" % (np.matrix(estimator.poseLeft.value),) )
print( "poseRight:\n%s" % (np.matrix(estimator.poseRight.value),) )

estimator.init()

estimator.zmp.recompute(1)

print( "copLeft:  %s" % (estimator.copLeft.value,) )
print( "copRight: %s" % (estimator.copRight.value,) )
print( "zmp:      %s" % (estimator.zmp.value,) )
print( "com:      %s" % (com,) )

assertApprox(estimator.zmp.value[:2], com[:2])
