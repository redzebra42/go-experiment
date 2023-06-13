import numpy as np
import matplotlib.pyplot as plt

res_list = [11, 13, 16, 17, 22, 19, 26, 23, 26, 22, 23, 27, 30, 27, 27, 25, 28, 30, 26, 26, 28, 27, 25, 28, 26, 28, 28, 27, 28, 29, 29, 30, 30, 29, 29, 29, 28, 30, 30, 30, 30, 30, 30, 29, 30, 30, 30, 30, 28, 30, 30, 30, 29, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
x_coords = [5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57, 61, 65, 69, 73, 77, 81, 85, 89, 93, 97, 101, 105, 109, 113, 117, 121, 125, 129, 133, 137, 141, 145, 149, 153, 157, 161, 165, 169, 173, 177, 181, 185, 189, 193, 197, 201, 205, 209, 213, 217, 221, 225, 229, 233, 237, 241, 245, 249, 253, 257, 261, 265, 269, 273, 277, 281]

np_y_coords = 100/30 * np.array(res_list)
np_x_coords = np.array(x_coords)

plt.plot(np_x_coords, np_y_coords)
plt.title("Performances pour le morpion")
plt.xlabel("nombre de parcours de l'arbre")
plt.ylabel("pourcentage de parties à égalité")
plt.show()

