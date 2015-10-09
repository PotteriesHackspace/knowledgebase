from os import walk
import os
import unittest


class MdTestCase(unittest.TestCase):
    def test_articles(self):
        for (dirpath, dirnames, filenames) in walk("md"):
                for x in filenames:
                    path = dirpath + os.path.sep + x
                    htmlpath = path.replace("md" + os.path.sep, "pages" + os.path.sep).replace(".md", ".html")
                    self.assertTrue(os.path.exists(htmlpath), msg="Article found with no matching page! Article = {}".format(path))

if __name__ == '__main__':
    unittest.main()
