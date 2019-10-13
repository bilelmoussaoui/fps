import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fps",
    version="0.1",
    author="Bilal Elmoussaoui",
    author_email="bil.elmoussaoui@gmail.com",
    description="Flathub Packages State",
    long_description_content_type="text/markdown",
    long_description=long_description,
    license='MIT',
    include_package_data=True,
    url="https://github.com/bilelmoussaoui/fps",
    entry_points={
        'console_scripts': ['fps=fps.cli:run'],
    },
    packages=[
        'fps',
        'fps.migrations',
        'fps.templates'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Topic :: Utilities',
    ],
    test_suite='tests'
)
