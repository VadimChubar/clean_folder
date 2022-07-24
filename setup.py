from setuptools import setup, find_namespace_packages

setup(name='clean_folder',
      version='0.0.1',
      description='Clean Folder Package',
      author='Vadim Chubar',
      author_email='chvagr@gmail.com',
      license='MIT',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['clean-folder=clean_folder.clean:main']}
      # clean-folder - команда, яка повинна виконатись у терміналі
      # після '=' пишемо шлях до файлу, де знаходиться функція => clean_folder.clean
      # після ':' пишемо назву функції main
      )