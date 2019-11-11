import unittest
from requests.exceptions import HTTPError

from GitHub import GitHub


class GithubApiTests(unittest.TestCase):

    def test_get_commit_succesfully(self):
        obj = GitHub("octokit", ["octokit.rb"], ["issues", "pull_requests", "commits"])
        commit = obj.get_commit("43d0c71969e11b2cfeb529ffd0846043f6f013b5")
        self.assertTrue("sha" in commit)

    def test_get_commit_failed(self):
        obj = GitHub("octokit", ["octokit.rb"], ["issues", "pull_requests", "commits"])
        commit = obj.get_commit("dfgndfg")
        self.assertTrue("sha" not in commit)

    def test_get_issues(self):
        obj = GitHub("octokit", ["octokit.rb"], ["issues"])
        self.assertTrue(len(obj.read()) > 0)

    def test_get_issues_next_page(self):
        obj = GitHub("octokit", ["octokit.rb"], ["issues"])
        obj.read()
        self.assertTrue(len(obj.read()) > 0)

    def test_get_pull_requests(self):
        obj = GitHub("octokit", ["octokit.rb"], ["pull_requests"])
        self.assertTrue(len(obj.read()) > 0)

    def test_get_pull_requests_next_page(self):
        obj = GitHub("octokit", ["octokit.rb"], ["pull_requests"])
        obj.read()
        self.assertIsNone(obj.read())

    @unittest.skip("Does a lot o requests to github")
    def test_get_commits(self):
        obj = GitHub("octokit", ["octokit.rb"], ["commits"])
        self.assertTrue(len(obj.read()) > 0)

    def test_bad_resource(self):
        obj = GitHub("octokit", ["octokit.rb"], ["sdfssdf"])
        self.assertIsNone(obj.read())

    def test_bad_repo(self):
        obj = GitHub("octokit", ["asddd.rb"], ["sdfssdf"])
        self.assertIsNone(obj.read())

    def test_no_resource(self):
        obj = GitHub("octokit", ["octokit.rb"], [])
        self.assertIsNone(obj.read())

    def test_no_owner(self):
        obj = GitHub("", ["octokit.rb"], ["issues"])
        self.assertTrue(type(obj.read()) is HTTPError)

    def test_bad_owner(self):
        obj = GitHub("gfdfgoossssdfsdfds", ["octokit.rb"], ["issues"])
        self.assertTrue(type(obj.read()) is HTTPError)


if __name__ == '__main__':
    unittest.main()
