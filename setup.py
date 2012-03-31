from distutils.core import setup

setup(name='dpscope',
      version='1.0',
      description='Cross-platform software for the DPScope oscilloscope',
      author='Pepijn de Vos',
      author_email='pepijndevos@gmail.com',
      url='https://github.com/pepijndevos/DPScope',
      packages=['dpscope'],
      requires=["pyserial", "matplotlib"],
     )
