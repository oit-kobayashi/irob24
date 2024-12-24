import numpy as np

class Robot:
    b = 0.3
    def __init__(self, x=0, y=0, th=0):
        self.p = np.array([[x], [y], [th]], dtype=np.float32)
        self.p0 = np.array([[x], [y], [th]], dtype=np.float32)
        self.sigma_p = np.diag([1, 1, 0.25]).astype(np.float32)

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
        sigma_u = np.abs(np.diag([dsr * 0.03, dsl * 0.03]).astype(np.float32))
        th = self.p[2, 0]  # p_theta
        tt = th + (dsr - dsl) / 2 / self.b
        jp = np.array([
            [1, 0, -(dsr + dsl) / 2 * np.sin(tt)],
            [0, 1,  (dsr + dsl) / 2 * np.cos(tt)],
            [0, 0, 1]
        ], dtype=np.float32)
        ju = np.array([
            [np.cos(tt) / 2 - (dsr + dsl) / 4 / self.b * np.sin(tt),
             np.cos(tt) / 2 + (dsr + dsl) / 4 / self.b * np.sin(tt)],
            [np.sin(tt) / 2 + (dsr + dsl) / 4 / self.b * np.cos(tt),
             np.sin(tt) / 2 - (dsr + dsl) / 4 / self.b * np.cos(tt)],
            [1 / self.b, -1 / self.b]
        ], dtype=np.float32)
        self.sigma_p = jp.dot(self.sigma_p).dot(jp.T) + ju.dot(sigma_u).dot(ju.T)
        dsr += np.random.randn() * 0.001
        dsl += np.random.randn() * 0.001
        dth = (dsr - dsl) / self.b
        r = (dsr + dsl) / (2 * dth)
        dx = 2 * r * np.sin(dth / 2) * np.cos(th + dth / 2)
        dy = 2 * r * np.sin(dth / 2) * np.sin(th + dth / 2)
        self.p += [[dx], [dy], [dth]]

    def perception(self,
                   pz: np.ndarray,
                   sz: np.ndarray):
        s1 = self.sigma_p
        s2 = sz
        u1 = self.p
        u2 = pz
        k = s1.dot(np.linalg.inv(s1 + s2))
        u = u1 + k.dot(u2 - u1)
        s = s1 - k.dot(s1 + s2).dot(k.T)
        self.p = u
        self.sigma_p = s

if __name__ == '__main__':
    r = Robot(0, 0, 0.2)
    for _ in range(5):
        r.move(dsr=0.1, dsl=0.101)
        print(r)
    
