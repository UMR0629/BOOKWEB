import numpy as np
import matplotlib.pyplot as plt

# 设计复数序列
def design_sequence(N, tau):
    n = np.arange(-N//2, N//2)
    x = np.exp(-np.abs(n)/tau)
    return x, n

# 计算傅里叶变换
def fourier_transform(x):
    X = np.fft.fft(x)
    omega = np.fft.fftfreq(len(x), d=1)
    return X, omega

# 绘制序列和傅里叶变换
def plot_sequence_and_transform(x, X, omega):
    plt.figure(figsize=(12, 6))
    
    plt.subplot(2, 1, 1)
    plt.stem(x, np.real(x), 'b', basefmt="-b")
    plt.title('Time Domain Signal')
    plt.xlabel('n')
    plt.ylabel('x[n]')
    
    plt.subplot(2, 1, 2)
    plt.stem(omega, np.abs(X), 'r', basefmt="-r")
    plt.title('Frequency Domain Signal (Magnitude)')
    plt.xlabel('Frequency (rad/sample)')
    plt.ylabel('|X(ω)|')
    
    plt.tight_layout()
    plt.show()

# 参数设置
N = 1024  # 序列长度
tau = 5    # 衰减常数

# 生成序列
x, n = design_sequence(N, tau)

# 计算傅里叶变换
X, omega = fourier_transform(x)

# 绘制结果
plot_sequence_and_transform(x, X, omega)