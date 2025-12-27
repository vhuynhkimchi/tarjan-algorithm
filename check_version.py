import sys
import networkx
import matplotlib
import tkinter

print("-" * 30)
print(f"Python version:     {sys.version.split()[0]}") # Lấy số phiên bản chính
print(f"NetworkX version:   {networkx.__version__}")
print(f"Matplotlib version: {matplotlib.__version__}")
print(f"Tkinter version:    {tkinter.TkVersion}")
print("-" * 30)