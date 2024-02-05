import numpy as np
from svgpathtools import svg2paths, wsvg
import svgpathtools as svg
import os
import glob
from tqdm import tqdm
import sys


def simplify(draw, delta=0.1, eps=1e-8):
    new_draw = []

    i = 0
    while i < (len(draw[0]) - 1):
        s1, s2 = draw[0][i], draw[0][i+1]
        
        s1_norm = np.sqrt(s1[0]**2 + s1[1]**2)    
        if s1_norm < eps:
            i += 1
            continue
        
        s2_norm = np.sqrt(s2[0]**2 + s2[1]**2)
        if np.sqrt((s1[0]/s1_norm - s2[0]/s2_norm)**2 + (s1[1]/s1_norm - s2[1]/s2_norm)**2) < delta: # if two strokes are small enough to remove,
            s1 = s1 + s2
            i += 1
        
        new_draw.append(s1)
        i += 1
    new_draw.append(draw[0][-1])
    len(new_draw)

    return np.stack([new_draw])

def bazier2line(bazier_svg, num_of_segments=3):
    paths, _ = svg2paths(bazier_svg)
    
    new_paths = []
    for path in paths:
        new_paths_raw = svg.Path()
        for stroke in path:
            if isinstance(stroke, svg.path.CubicBezier):
                bazier = stroke
                
                P0 = np.array((bazier.start.real, bazier.start.imag))
                P1 = np.array((bazier.control1.real, bazier.control1.imag))
                P2 = np.array((bazier.control2.real, bazier.control2.imag))
                P3 = np.array((bazier.end.real, bazier.end.imag))

                cur_pos = P0
                for t in np.linspace(0., 1., num_of_segments + 1):
                    next_pos = np.power((1-t), 3)*P0 + 3*(1-t)**2*t*P1 + 3*(1-t)*t**2*P2 + t**3*P3
                    new_paths_raw.append(svg.Line(complex(cur_pos[0], cur_pos[1]), complex(next_pos[0], next_pos[1])))
                    
                    cur_pos = next_pos
            else:
                new_paths_raw.append(stroke)
            
        new_paths.append(new_paths_raw)
    return new_paths


if __name__ == "__main__":
    N = int(sys.argv[1])
    print(f"[INFO] N: {N}")
    
    if not os.path.isdir("./Output/svg_line"):
        os.mkdir("./Output/svg_line")    
    
    bazier_svgs = sorted(glob.glob("./Output/svg/*.svg"))

    for bazier_svg in tqdm(bazier_svgs):
        line_svg = bazier2line(bazier_svg, num_of_segments=N)
        wsvg(line_svg, filename=f"./Output/svg_line/{os.path.basename(bazier_svg)}")
    