#
# Example of how to run the Python code, and access the output
# This case is identical to the default setup of CLASS (the version with interface)
#

import matplotlib.pyplot as plt
from classmodel.model import Model, ModelInput

run1input = ModelInput()
r1 = Model(run1input)
r1.run()

# Plot output
plt.figure()
plt.subplot(311)
plt.plot(r1.out.t, r1.out.h)
plt.xlabel("time [h]")
plt.ylabel("h [m]")

plt.subplot(312)
plt.plot(r1.out.t, r1.out.theta)
plt.xlabel("time [h]")
plt.ylabel("theta [K]")

plt.subplot(313)
plt.plot(r1.out.t, r1.out.q * 1000.0)
plt.xlabel("time [h]")
plt.ylabel("q [g kg-1]")
