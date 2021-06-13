from setuptools import setup, find_packages

try:
    from pip._internal.network.session import PipSession
    from pip._internal.req import parse_requirements

    install_requires = parse_requirements("requirements.txt", session=PipSession())
    dependencies = [str(package.requirement) for package in install_requires]
except ImportError:
    msg = "Your pip version is out of date, please run `pip install --upgrade pip setuptools`"
    raise ImportError(msg)

for package_index in range(len(dependencies)):
    if dependencies[package_index].startswith("git+"):
        dependencies[package_index] = dependencies[package_index].split("=")[1]

setup(
    name="creditrisk_poc",
    version='0.0.1',
    description='Hydra powered API for creditrisk management',
    author="Hydra Ecosystem",
    author_email="collective@hydraecosystem.org",
    url="https://github.com/HTTP-APIs/hydrus",
    py_modules=["cli"],
    python_requires=">=3.6",
    install_requires=dependencies,
    packages=find_packages()
)
