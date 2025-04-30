import matplotlib.pyplot as plt
import numpy as np

x = np.loadtxt('testdata2.cvs') #for comma separated values

plt.plot(x, label='Data from file')
plt.xlabel('X-axis label')
plt.title('Plot of data from file')
plt.legend()
# plt.show()

plt.savefig('sine_wave.png', dpi=300, bbox_inches='tight')
plt.close()




# https://www.google.com/search?q=python+matlabplot+read+data+from+a+file+and+plot&oq=python+matlabplot+read+data+from+a+file+and+plot&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIJCAEQIRgKGKABMgkIAhAhGAoYoAEyBwgDECEYjwIyBwgEECEYjwLSAQoxNTczMmowajE1qAIIsAIB8QXbDso7HjxoTg&sourceid=chrome&ie=UTF-8

# import matplotlib.pyplot as plt
# x = [2,5, 8]
# plt.plot(x)
# plt.show()