from ipykernel.kernelapp import IPKernelApp
from .kernel import KdbQKernel
IPKernelApp.launch_instance(kernel_class=KdbQKernel)
