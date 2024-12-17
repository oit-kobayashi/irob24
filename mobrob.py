import numpy as np

class Robot:
    b = 0.3
    def __init__(self, x=0, y=0, th=0):
        self.p = np.array([[x], [y], [th]], dtype=np.float32)
        self.p0 = np.array([[x], [y], [th]], dtype=np.float32)

    def __str__(self):
        return f'--- robot ---p: {str(self.p)}\np0: {str(self.p0)}\n'

    def move(self, dsr=0, dsl=0):
        # true
        th = self.p0[2, 0]  # p0_theta
        dth = (dsr - dsl) / self.b
        r = (dsr + dsl) / (2 * dth)
        dx = 2 * r * np.sin(dth / 2) * np.cos(th + dth / 2)
        dy = 2 * r * np.sin(dth / 2) * np.sin(th + dth / 2)
        self.p0 += [[dx], [dy], [dth]]
        # estimated
        th = self.p[2, 0]  # p_theta
        dsr += np.random.randn() * 0.002
        dsl += np.random.randn() * 0.002
        dth = (dsr - dsl) / self.b
        r = (dsr + dsl) / (2 * dth)
        dx = 2 * r * np.sin(dth / 2) * np.cos(th + dth / 2)
        dy = 2 * r * np.sin(dth / 2) * np.sin(th + dth / 2)
        self.p += [[dx], [dy], [dth]]

if __name__ == '__main__':
    r = Robot(0, 0, 0.2)
    for _ in range(5):
        r.move(dsr=0.1, dsl=0.101)
        print(r)
    
