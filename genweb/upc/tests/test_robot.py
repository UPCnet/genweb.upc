import unittest
import robotsuite

from genweb.upc.testing import GENWEB_UPC_ROBOT_TESTING
from plone.testing import layered

def setUP(testCase=None):
    # Inicialitzar el entorn de proves
    pass

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite(
                './robot/test_plone_is_installed.robot',
                setUp=setUP
            ),
            layer=GENWEB_UPC_ROBOT_TESTING
        ),
        layered(robotsuite.RobotTestSuite(
                './robot/test_initial_checks.robot',
                setUp=setUP
            ),
            layer=GENWEB_UPC_ROBOT_TESTING
        ),
        layered(robotsuite.RobotTestSuite(
                './robot/test_news_item.robot',
                setUp=setUP
            ),
            layer=GENWEB_UPC_ROBOT_TESTING
        ),
        layered(robotsuite.RobotTestSuite(
                './robot/test_collection.robot',
                setUp=setUP
            ),
            layer=GENWEB_UPC_ROBOT_TESTING
        ),
        layered(robotsuite.RobotTestSuite(
                './robot/test_event.robot',
                setUp=setUP
            ),
            layer=GENWEB_UPC_ROBOT_TESTING
        ),
    ])
    return suite
