from setuptools import setup

package_name = 'primebot_1'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('lib/' + package_name, ['primebot_1/line_follower_node.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='fire_enigma',
    maintainer_email='fire_enigma@todo.todo',
    description='PrimeBot Line Follower Robot',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'line_follower_node = primebot_1.line_follower_node:main',
        ],
    },
)
