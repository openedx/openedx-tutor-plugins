import io
import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    with io.open(os.path.join(HERE, "README.rst"), "rt", encoding="utf8") as f:
        return f.read()


def load_about():
    about = {}
    with io.open(
        os.path.join(HERE, "tutor_learner_dashboard_mfe", "__about__.py"),
        "rt",
        encoding="utf-8",
    ) as f:
        exec(f.read(), about)  # pylint: disable=exec-used
    return about


ABOUT = load_about()


setup(
    name="tutor-contrib-learner-dashboard-mfe",
    version=ABOUT["__version__"],
    url="https://github.com/openedx/openedx-tutor-plugins",
    project_urls={
        "Code": "https://github.com/openedx/openedx-tutor-plugins",
        "Issue tracker": "https://github.com/openedx/openedx-tutor-plugins/issues",
    },
    license="AGPLv3",
    author="Adolfo R. Brandes",
    description="learner-dashboard-mfe plugin for Tutor",
    long_description=load_readme(),
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=["tutor>=16.0.0,<17.0.0", "tutor-mfe>=16.0.0,<17.0.0"],
    extras_require={"dev": ["tutor[dev]>=16.0.0,<17.0.0"]},
    entry_points={
        "tutor.plugin.v1": [
            "learner-dashboard-mfe = tutor_learner_dashboard_mfe.plugin"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
