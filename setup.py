from setuptools import setup

setup(name='pyfusionbrain',
      version='0.1',
      description='Python interface to the FusionBrain multi-function I/O module',
      url='http://github.com/willmeyer/pyfusionbrain',
      author='Flying Circus',
      author_email='will@willmeyer.com',
      license='MIT',
      packages=['pyfusionbrain'],
      install_requires=['pyusb'],
      zip_safe=False)