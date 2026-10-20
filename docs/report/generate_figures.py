import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

fig_dir = "/home/kitti/Documents/GitHub/calculus-integration-app/docs/report/figures"
os.makedirs(fig_dir, exist_ok=True)

# Style settings: academic clean black & white / grayscale
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.edgecolor': '#222222',
    'axes.linewidth': 1.0,
    'grid.color': '#DDDDDD',
    'grid.linestyle': ':',
    'figure.autolayout': True,
})

# 1. Tangent line at x=1 for f(x) = x^2
fig, ax = plt.subplots(figsize=(5.5, 3.8), dpi=300)
x = np.linspace(-0.5, 2.2, 300)
y = x**2
ax.plot(x, y, 'k-', linewidth=2.0, label=r'$f(x) = x^2$')

# Tangent line: y = 2x - 1
x_tan = np.linspace(0.2, 2.0, 100)
y_tan = 2*x_tan - 1
ax.plot(x_tan, y_tan, 'k--', linewidth=1.5, label=r'Tangent line: $y = 2x - 1$')

# Secant line between (1, 1) and (1.8, 3.24)
x_sec = np.linspace(0.5, 2.1, 100)
m_sec = 2.8
y_sec = m_sec*(x_sec - 1) + 1
ax.plot(x_sec, y_sec, 'gray', linestyle='-.', linewidth=1.2, label=r'Secant line ($h = 0.8$)')

ax.plot([1, 1.8], [1, 3.24], 'ko', markersize=6)
ax.annotate(r'$P(1, 1)$', (1, 1), textcoords="offset points", xytext=(-25, 8), fontweight='bold')
ax.annotate(r'$Q(1+h, f(1+h))$', (1.8, 3.24), textcoords="offset points", xytext=(-70, 8))

ax.axhline(0, color='black', linewidth=0.8)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlim(-0.3, 2.3)
ax.set_ylim(-1.0, 4.5)
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.grid(True)
ax.legend(loc='upper left', frameon=True, edgecolor='#AAAAAA')
fig.savefig(os.path.join(fig_dir, "fig-2-1-tangent.png"))
plt.close(fig)

# 2. Riemann sums: Left vs Right for f(x) = x^2 on [0, 2], n=4
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.5), dpi=300)
x_fine = np.linspace(0, 2, 200)
y_fine = x_fine**2

# Left Sum
ax1.plot(x_fine, y_fine, 'k-', linewidth=1.8)
x_pts = np.linspace(0, 2, 5) # 0, 0.5, 1, 1.5, 2
dx = 0.5
for i in range(4):
    xi = x_pts[i]
    yi = xi**2
    ax1.bar(xi, yi, width=dx, align='edge', edgecolor='black', facecolor='#DDDDDD', alpha=0.8, linewidth=1.0)
ax1.set_title(r'(a) Left Riemann Sum ($L_4 = 1.75$)', fontsize=10.5, fontweight='bold')
ax1.set_xlim(-0.1, 2.2)
ax1.set_ylim(0, 4.5)
ax1.set_xlabel('$x$')
ax1.set_ylabel('$y$')
ax1.grid(True)

# Right Sum
ax2.plot(x_fine, y_fine, 'k-', linewidth=1.8)
for i in range(4):
    xi = x_pts[i]
    yi = x_pts[i+1]**2
    ax2.bar(xi, yi, width=dx, align='edge', edgecolor='black', facecolor='#B0B0B0', alpha=0.8, linewidth=1.0)
ax2.set_title(r'(b) Right Riemann Sum ($R_4 = 3.75$)', fontsize=10.5, fontweight='bold')
ax2.set_xlim(-0.1, 2.2)
ax2.set_ylim(0, 4.5)
ax2.set_xlabel('$x$')
ax2.grid(True)

fig.savefig(os.path.join(fig_dir, "fig-2-2-riemann.png"))
plt.close(fig)

# 3. Area between curves: y = 2x and y = x^2
fig, ax = plt.subplots(figsize=(5.5, 3.8), dpi=300)
x_span = np.linspace(-0.5, 2.5, 200)
ax.plot(x_span, 2*x_span, 'k-', linewidth=1.8, label=r'$y = 2x$ (Upper curve)')
ax.plot(x_span, x_span**2, 'k--', linewidth=1.8, label=r'$y = x^2$ (Lower curve)')

# Shaded area on [0, 2]
x_shade = np.linspace(0, 2, 100)
ax.fill_between(x_shade, x_shade**2, 2*x_shade, color='#CCCCCC', alpha=0.8, label=r'Enclosed Area $A = 4/3$')

ax.plot([0, 2], [0, 4], 'ko', markersize=6)
ax.annotate(r'$(0, 0)$', (0, 0), textcoords="offset points", xytext=(8, -12), fontweight='bold')
ax.annotate(r'$(2, 4)$', (2, 4), textcoords="offset points", xytext=(-35, 8), fontweight='bold')

ax.axhline(0, color='black', linewidth=0.8)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlim(-0.3, 2.4)
ax.set_ylim(-0.5, 4.8)
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.grid(True)
ax.legend(loc='upper left', frameon=True, edgecolor='#AAAAAA')
fig.savefig(os.path.join(fig_dir, "fig-2-3-area.png"))
plt.close(fig)

# 4. Improper integral: 1/x^2 on [1, inf)
fig, ax = plt.subplots(figsize=(5.5, 3.5), dpi=300)
x_imp = np.linspace(0.4, 5.0, 300)
ax.plot(x_imp, 1/(x_imp**2), 'k-', linewidth=2.0, label=r'$f(x) = 1/x^2$')

x_tail = np.linspace(1.0, 5.0, 200)
ax.fill_between(x_tail, 0, 1/(x_tail**2), color='#B0B0B0', alpha=0.7, label=r'Area $= \int_1^{\infty} \frac{1}{x^2} dx = 1$')

ax.axvline(1, color='black', linestyle=':', linewidth=1.2)
ax.axhline(0, color='black', linewidth=0.8)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlim(0, 5.2)
ax.set_ylim(-0.1, 3.5)
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.grid(True)
ax.legend(loc='upper right', frameon=True, edgecolor='#AAAAAA')
fig.savefig(os.path.join(fig_dir, "fig-2-4-improper.png"))
plt.close(fig)

print("ALL 4 FIGURES GENERATED SUCCESSFULLY!")
