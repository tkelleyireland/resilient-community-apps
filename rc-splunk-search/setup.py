from __future__ import print_function

import os.path
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

if not sys.version_info[0] == 2:
    print("Warning: splunk-sdk does not support Python 3")

splunk_queries = [u"query_runner/data/queries_splunk/" + filename for filename in os.listdir("query_runner/data/queries_splunk")]

class PyTest(TestCommand):
    user_options = [('pytestargs=', 'a', "Resilient Environment Arguments")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytestargs = []
        self.test_suite = True

    def finalize_options(self):
        import shlex
        TestCommand.finalize_options(self)
        self.test_args = ["-s",] + shlex.split(self.pytestargs)

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='rc-splunk-search',
    namespace_packages=['query_runner', 'query_runner.components', "query_runner.lib"],
    use_scm_version={"root": "../", "relative_to": __file__},
    setup_requires=['setuptools_scm'],
    url='https://github.com/ibmresilient/resilient-circuits-packages',
    license='MIT',
    author='IBM Resilient',
    install_requires=[
        'resilient_circuits>=28.0.0',
        'rc-query-runner',
        'splunk-sdk'
    ],
    tests_require=["pytest",
                   "pytest_resilient_circuits"],
    cmdclass = {"test" : PyTest},
    author_email='support@resilientsystems.com',
    description="Resilient Circuits components for running Splunk searches and updating incidents from the results",
    long_description = "Resilient Circuits components for running Splunk searches and updating incidents from the results",
    packages=find_packages(),
    include_package_data=True,
    data_files = [("query_runner", ["query_runner/LICENSE"]),
                  ("query_runner/data", ["query_runner/data/app.config.splunk"]),
                  ("query_runner/data/queries_splunk", splunk_queries)],
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
    ],
    entry_points={
        # Register the components with resilient_circuits
        "resilient.circuits.components": ["SplunkQueryRunner = query_runner.components.splunk_search:SplunkQueryRunner"],
        "resilient.circuits.configsection": ["splunk_gen_config = query_runner.components.splunk_search:config_section_data"]
    }
)
