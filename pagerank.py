import numpy as np
import numpy.linalg as la
from io import StringIO

L = np.array([
    [0,   1/2, 1/3, 0, 0,   0  ],
    [1/3, 0,   0,   0, 1/2, 0  ],
    [1/3, 1/2, 0,   1, 0,   1/2],
    [1/3, 0,   1/3, 0, 1/2, 1/2],
    [0,   0,   0,   0, 0,   0  ],
    [0,   0,   1/3, 0, 0,   0  ]
])


s = StringIO()
np.savetxt(s, L, fmt="%.3f")
print(s.getvalue())

e_vals, e_vecs = la.eig(L)

# print(e_vals)
# print(e_vecs)

vec = np.transpose(e_vecs)[0].real

print(vec)
